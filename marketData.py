"""
marketData.py — BIST-Specific Data Infrastructure
===================================================
5-Layer architecture for quantitative market data access.

Layer 1: Data Contract & Types (Timeframe, constants, validation)
Layer 2: BaseProvider interface + YFinanceProvider
Layer 3: MathematicalCleaner (normalization, dedup, timezone, calendar)
Layer 4: ParquetCache (versioned read-through / write-through)
Layer 5: MarketData facade (single public API)

All naming follows camelCase convention.
"""

import os
import json
import hashlib
import logging
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configure module logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("marketData")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(handler)


# ============================================================================
# LAYER 1 — Data Contract & Types
# ============================================================================

class Timeframe(Enum):
    """Supported bar resolutions. Treated as an object, never a raw string."""
    daily = "1d"
    hourly = "1h"
    fifteenMin = "15m"


# Canonical column order & types that every downstream consumer can rely on.
CONTRACT_COLUMNS = ["open", "high", "low", "close", "volume", "adjClose"]
CONTRACT_DTYPES = {
    "open": "float64",
    "high": "float64",
    "low": "float64",
    "close": "float64",
    "volume": "int64",
    "adjClose": "float64",
}
CONTRACT_TIMEZONE = "Europe/Istanbul"

# BIST 30 — fixed universe for MVP (high-liquidity guarantee)
BIST30_TICKERS = [
    "AKBNK", "ARCLK", "ASELS", "BIMAS", "EKGYO",
    "ENKAI", "EREGL", "FROTO", "GARAN", "GUBRF",
    "HEKTS", "ISCTR", "KCHOL", "KONTR", "KOZAA",
    "KOZAL", "KRDMD", "ODAS",  "OYAKC", "PETKM",
    "PGSUS", "SAHOL", "SASA",  "SISE",  "TAVHL",
    "TCELL", "THYAO", "TKFEN", "TOASO", "TUPRS",
]

# BIST official holidays 2024-2026 (simplified — expand as needed)
BIST_HOLIDAYS = {
    # 2024
    "2024-01-01", "2024-04-10", "2024-04-11", "2024-04-12",
    "2024-04-23", "2024-05-01", "2024-06-16", "2024-06-17",
    "2024-06-18", "2024-06-19", "2024-07-15", "2024-08-30",
    "2024-10-29",
    # 2025
    "2025-01-01", "2025-03-30", "2025-03-31", "2025-04-01",
    "2025-04-23", "2025-05-01", "2025-05-19", "2025-06-06",
    "2025-06-07", "2025-06-08", "2025-06-09", "2025-07-15",
    "2025-08-30", "2025-10-29",
    # 2026
    "2026-01-01", "2026-03-20", "2026-03-21", "2026-03-22",
    "2026-04-23", "2026-05-01", "2026-05-19", "2026-05-27",
    "2026-05-28", "2026-05-29", "2026-07-15", "2026-08-30",
    "2026-10-29",
}


def validateContract(df: pd.DataFrame, symbol: str = "") -> pd.DataFrame:
    """
    Validate and enforce the data contract on a DataFrame.
    Raises ValueError if critical violations are found.
    Returns the validated (and potentially corrected) DataFrame.
    """
    prefix = f"[{symbol}] " if symbol else ""

    # --- Column check ---
    missingCols = [c for c in CONTRACT_COLUMNS if c not in df.columns]
    if missingCols:
        raise ValueError(f"{prefix}Missing contract columns: {missingCols}")

    df = df[CONTRACT_COLUMNS].copy()

    # --- Type enforcement ---
    for col, dtype in CONTRACT_DTYPES.items():
        if col == "volume":
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("int64")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # --- Index: must be DatetimeIndex, timezone-aware ---
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(f"{prefix}Index must be DatetimeIndex, got {type(df.index)}")

    if df.index.tz is None:
        df.index = df.index.tz_localize(CONTRACT_TIMEZONE)
    else:
        df.index = df.index.tz_convert(CONTRACT_TIMEZONE)

    df.index.name = "date"

    # --- Integrity: sort, dedup ---
    df = df.sort_index()
    duplicateCount = df.index.duplicated().sum()
    if duplicateCount > 0:
        logger.warning(f"{prefix}Removed {duplicateCount} duplicate bars.")
        df = df[~df.index.duplicated(keep="last")]

    # --- NaN check in OHLC ---
    ohlcNanCount = df[["open", "high", "low", "close"]].isna().sum().sum()
    if ohlcNanCount > 0:
        logger.warning(f"{prefix}Dropping {ohlcNanCount} rows with NaN in OHLC.")
        df = df.dropna(subset=["open", "high", "low", "close"])

    return df


# ============================================================================
# LAYER 2 — BaseProvider Interface + YFinanceProvider
# ============================================================================

class BaseProvider(ABC):
    """Abstract base class for all market data providers."""

    @property
    @abstractmethod
    def providerName(self) -> str:
        """Unique string identifier for this provider (used in cache keys)."""
        ...

    @abstractmethod
    def fetchBars(
        self,
        symbol: str,
        timeframe: Timeframe,
        startDate: str,
        endDate: str,
    ) -> pd.DataFrame:
        """
        Fetch raw OHLCV bars from the data source.
        Must return a DataFrame with at minimum:
            DatetimeIndex, open, high, low, close, volume, adjClose
        Column names may differ — the cleaner will normalize.
        """
        ...

    def getSupportedTimeframes(self) -> list:
        """Return list of Timeframe enums this provider supports."""
        return [Timeframe.daily]


class YFinanceProvider(BaseProvider):
    """
    Data provider using Yahoo Finance (yfinance).
    BIST tickers are suffixed with '.IS' automatically.
    """

    @property
    def providerName(self) -> str:
        return "yfinance"

    def _toBistTicker(self, symbol: str) -> str:
        """Ensure BIST symbol has .IS suffix."""
        if not symbol.upper().endswith(".IS"):
            return f"{symbol.upper()}.IS"
        return symbol.upper()

    def fetchBars(
        self,
        symbol: str,
        timeframe: Timeframe,
        startDate: str,
        endDate: str,
    ) -> pd.DataFrame:
        import yfinance as yf

        ticker = self._toBistTicker(symbol)
        logger.info(f"YFinance: fetching {ticker} | {timeframe.value} | {startDate} → {endDate}")

        data = yf.download(
            ticker,
            start=startDate,
            end=endDate,
            interval=timeframe.value,
            auto_adjust=False,
            progress=False,
        )

        if data.empty:
            raise ValueError(f"YFinance returned no data for {ticker}")

        # Handle MultiIndex columns from yfinance (happens with single ticker too)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Normalize column names to our contract
        columnMap = {
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
            "Adj Close": "adjClose",
        }
        data = data.rename(columns=columnMap)

        # If adjClose is missing (auto_adjust=True case), use close
        if "adjClose" not in data.columns:
            data["adjClose"] = data["close"]

        return data

    def getSupportedTimeframes(self) -> list:
        return [Timeframe.daily, Timeframe.hourly, Timeframe.fifteenMin]


# ============================================================================
# LAYER 3 — MathematicalCleaner
# ============================================================================

# Bump this version whenever cleaner logic changes → invalidates cache.
CLEANER_VERSION = 1
SCHEMA_VERSION = 1


class MathematicalCleaner:
    """
    Single normalization gate between raw provider data and analysis layer.
    Responsibilities:
        - Timezone normalization to Europe/Istanbul
        - Duplicate bar removal, chronological sort
        - BIST calendar filtering (drop non-trading days for daily bars)
        - Contract validation
        - Metadata logging
    """

    def clean(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: Timeframe,
        providerName: str,
    ) -> pd.DataFrame:
        """
        Clean and normalize raw provider data.
        Returns a contract-compliant DataFrame.
        """
        barCountRaw = len(df)

        # Step 1: Contract validation (handles tz, dedup, sort, type cast)
        df = validateContract(df, symbol)

        # Step 2: BIST calendar filter (daily bars only)
        if timeframe == Timeframe.daily:
            df = self._filterBistCalendar(df, symbol)

        barCountClean = len(df)

        # Step 3: Log metadata
        metadata = {
            "symbol": symbol,
            "provider": providerName,
            "timeframe": timeframe.value,
            "cleanerVersion": CLEANER_VERSION,
            "fetchTime": datetime.now().isoformat(),
            "barsRaw": barCountRaw,
            "barsClean": barCountClean,
            "barsDropped": barCountRaw - barCountClean,
            "dateMin": str(df.index.min()) if not df.empty else None,
            "dateMax": str(df.index.max()) if not df.empty else None,
        }
        logger.info(f"Cleaner metadata: {json.dumps(metadata, indent=2)}")

        return df

    def _filterBistCalendar(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Remove bars that fall on known BIST holidays or weekends."""
        holidayDates = {pd.Timestamp(d, tz=CONTRACT_TIMEZONE) for d in BIST_HOLIDAYS}

        # Filter weekends
        isWeekday = df.index.dayofweek < 5
        weekendCount = (~isWeekday).sum()
        if weekendCount > 0:
            logger.warning(f"[{symbol}] Removed {weekendCount} weekend bars.")

        df = df[isWeekday]

        # Filter holidays
        barDates = df.index.normalize()
        isHoliday = barDates.isin(holidayDates)
        holidayCount = isHoliday.sum()
        if holidayCount > 0:
            logger.warning(f"[{symbol}] Removed {holidayCount} holiday bars.")

        df = df[~isHoliday]

        return df


# ============================================================================
# LAYER 4 — ParquetCache
# ============================================================================

class ParquetCache:
    """
    Read-through / write-through cache using Parquet files.
    Cache key: data/{provider}/{symbol}/{timeframe}/v{schema}_{cleaner}.parquet
    """

    def __init__(self, baseDir: str = "data"):
        self.baseDir = Path(baseDir)

    def _buildPath(self, providerName: str, symbol: str, timeframe: Timeframe) -> Path:
        """Build versioned cache file path."""
        return (
            self.baseDir
            / providerName
            / symbol.upper()
            / timeframe.value
            / f"v{SCHEMA_VERSION}_{CLEANER_VERSION}.parquet"
        )

    def read(
        self,
        providerName: str,
        symbol: str,
        timeframe: Timeframe,
        startDate: str,
        endDate: str,
    ) -> Optional[pd.DataFrame]:
        """
        Attempt to read cached data covering [startDate, endDate].
        Returns DataFrame if cache hit, None if miss.
        """
        path = self._buildPath(providerName, symbol, timeframe)
        if not path.exists():
            logger.info(f"Cache MISS (no file): {path}")
            return None

        try:
            df = pd.read_parquet(path)

            # Restore timezone awareness if stripped by parquet
            if df.index.tz is None:
                df.index = df.index.tz_localize(CONTRACT_TIMEZONE)

            requestStart = pd.Timestamp(startDate, tz=CONTRACT_TIMEZONE)
            requestEnd = pd.Timestamp(endDate, tz=CONTRACT_TIMEZONE)

            if df.index.min() <= requestStart and df.index.max() >= requestEnd - timedelta(days=3):
                filtered = df.loc[requestStart:requestEnd]
                logger.info(
                    f"Cache HIT: {path} | {len(filtered)} bars "
                    f"({requestStart.date()} → {requestEnd.date()})"
                )
                return filtered
            else:
                logger.info(
                    f"Cache MISS (date range): cached {df.index.min().date()}→{df.index.max().date()}, "
                    f"requested {requestStart.date()}→{requestEnd.date()}"
                )
                return None

        except Exception as e:
            logger.warning(f"Cache read error: {e}. Will re-fetch.")
            return None

    def write(
        self,
        df: pd.DataFrame,
        providerName: str,
        symbol: str,
        timeframe: Timeframe,
    ) -> Path:
        """Write cleaned DataFrame to parquet cache."""
        path = self._buildPath(providerName, symbol, timeframe)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Merge with existing cache if present
        if path.exists():
            try:
                existing = pd.read_parquet(path)
                if existing.index.tz is None:
                    existing.index = existing.index.tz_localize(CONTRACT_TIMEZONE)
                df = pd.concat([existing, df])
                df = df[~df.index.duplicated(keep="last")]
                df = df.sort_index()
            except Exception:
                pass  # Overwrite if existing file is corrupt

        df.to_parquet(path, engine="pyarrow")
        logger.info(f"Cache WRITE: {path} | {len(df)} total bars")
        return path


# ============================================================================
# LAYER 5 — MarketData Facade
# ============================================================================

class MarketData:
    """
    Single public API for all market data access.

    Usage:
        md = MarketData()
        data = md.load("THYAO", Timeframe.daily, "2024-01-01", "2025-01-01")
        # data is a dict: {"THYAO": pd.DataFrame}
    """

    def __init__(
        self,
        provider: Optional[BaseProvider] = None,
        cacheDir: str = "data",
    ):
        self.provider = provider or YFinanceProvider()
        self.cache = ParquetCache(baseDir=cacheDir)
        self.cleaner = MathematicalCleaner()

    def load(
        self,
        symbols: Union[str, List[str]],
        timeframe: Timeframe = Timeframe.daily,
        startDate: str = "2024-01-01",
        endDate: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch, clean, cache, and return market data.

        Args:
            symbols: Single ticker or list of tickers (e.g. "THYAO" or ["THYAO", "GARAN"])
            timeframe: Timeframe enum member
            startDate: Start date string "YYYY-MM-DD"
            endDate: End date string "YYYY-MM-DD" (defaults to today)

        Returns:
            dict mapping symbol → contract-compliant pd.DataFrame
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        if endDate is None:
            endDate = datetime.now().strftime("%Y-%m-%d")

        result = {}
        for symbol in symbols:
            symbol = symbol.upper().replace(".IS", "")
            df = self._loadSingle(symbol, timeframe, startDate, endDate)
            result[symbol] = df

        return result

    def _loadSingle(
        self,
        symbol: str,
        timeframe: Timeframe,
        startDate: str,
        endDate: str,
    ) -> pd.DataFrame:
        """Load data for a single symbol: cache → fetch → clean → store."""
        providerName = self.provider.providerName

        # 1. Try cache
        cached = self.cache.read(providerName, symbol, timeframe, startDate, endDate)
        if cached is not None:
            return cached

        # 2. Fetch from provider
        rawDf = self.provider.fetchBars(symbol, timeframe, startDate, endDate)

        # 3. Clean
        cleanDf = self.cleaner.clean(rawDf, symbol, timeframe, providerName)

        # 4. Write to cache
        self.cache.write(cleanDf, providerName, symbol, timeframe)

        # 5. Filter to requested range and return
        requestStart = pd.Timestamp(startDate, tz=CONTRACT_TIMEZONE)
        requestEnd = pd.Timestamp(endDate, tz=CONTRACT_TIMEZONE)
        return cleanDf.loc[requestStart:requestEnd]

    def loadBist30(
        self,
        timeframe: Timeframe = Timeframe.daily,
        startDate: str = "2024-01-01",
        endDate: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """Convenience: load all BIST 30 tickers at once."""
        return self.load(BIST30_TICKERS, timeframe, startDate, endDate)


# ============================================================================
# Quick self-test (run: python marketData.py)
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("marketData.py — Self-Test")
    print("=" * 60)

    md = MarketData()

    # Test 1: Single symbol fetch
    print("\n[Test 1] Loading THYAO daily data (last 6 months)...")
    sixMonthsAgo = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    data = md.load("THYAO", Timeframe.daily, sixMonthsAgo)

    if "THYAO" in data and not data["THYAO"].empty:
        df = data["THYAO"]
        print(f"  ✓ Retrieved {len(df)} bars")
        print(f"  ✓ Date range: {df.index.min().date()} → {df.index.max().date()}")
        print(f"  ✓ Columns: {list(df.columns)}")
        print(f"  ✓ Index timezone: {df.index.tz}")
        print(f"  ✓ Dtypes:\n{df.dtypes.to_string()}")
        print(f"\n  Sample (last 5 bars):")
        print(df.tail().to_string())
    else:
        print("  ✗ FAILED: No data returned")

    # Test 2: Cache hit
    print("\n[Test 2] Re-loading THYAO (should be cache HIT)...")
    data2 = md.load("THYAO", Timeframe.daily, sixMonthsAgo)
    if "THYAO" in data2 and not data2["THYAO"].empty:
        print(f"  ✓ Cache returned {len(data2['THYAO'])} bars")
    else:
        print("  ✗ FAILED: Cache miss")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)
