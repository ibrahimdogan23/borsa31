# Implementation Plan: Engineering-Based Investment Framework

This plan outlines the staged development of a quantitative trading framework for BIST, built on engineering and mathematical principles from the "Yatırım Metodolojisi" research document.

> [!IMPORTANT]
> All file names, variable names, and function names follow **camelCase** convention throughout the project.

---

## Phase 1: BIST-Specific Data Infrastructure (`marketData.py`)

The module is built as a **5-layer architecture**, each with a single responsibility:

### Layer 1: Data Contract & Types

Define the guarantees that every downstream consumer (statistical models, signals, risk) can rely on.

| Property | Specification |
|---|---|
| **Index** | `DatetimeIndex`, timezone-aware (`Europe/Istanbul`), sorted ascending |
| **Columns** | `open`, `high`, `low`, `close`, `volume`, `adjClose` |
| **Types** | `open/high/low/close/adjClose`: `float64`, `volume`: `int64` |
| **Integrity** | No duplicate bars, no NaN in OHLC, chronological order enforced |
| **Missing Bar Policy** | Drop (no forward-fill for OHLC; holidays excluded via calendar) |

```python
class Timeframe(Enum):
    daily = "1d"
    hourly = "1h"
    fifteenMin = "15m"
```

### Layer 2: `BaseProvider` Interface

Abstract class defining the contract for all data sources.

```python
class BaseProvider(ABC):
    def fetchBars(self, symbol, timeframe, startDate, endDate) -> pd.DataFrame
    def getSupportedTimeframes(self) -> list[Timeframe]
```

- `YFinanceProvider`: First implementation (BIST tickers end in `.IS`).
- Future: `MatriksProvider`, `BrokerApiProvider` — drop-in replacements.

### Layer 3: `MathematicalCleaner`

The **single normalization gate** between raw provider data and the analysis layer.

- Timezone normalization → `Europe/Istanbul`
- Dividend/split adjustment validation (`adjClose` consistency)
- Duplicate bar removal, chronological sort
- BIST calendar awareness (filter non-trading days)
- Metadata logging: provider, fetch time, bar count, min/max date, missing/duplicate counts

### Layer 4: `ParquetCache`

Read-through / write-through cache with **versioned keys**.

```
data/{provider}/{symbol}/{timeframe}/v{schemaVersion}_{cleanerVersion}.parquet
```

- **Cache hit**: File exists AND covers requested date range → read from disk (fast path).
- **Cache miss/stale**: Fetch from provider → clean → write parquet → return.
- Schema or cleaner version change → automatic invalidation.

### Layer 5: `MarketData` Facade

The single public API that the user interacts with.

```python
class MarketData:
    def load(self, symbols, timeframe, startDate, endDate) -> dict[str, pd.DataFrame]
```

- Orchestrates: Cache check → Provider fetch → Cleaner → Cache write → Return.
- Accepts single symbol or list of symbols.

---

## Phase 2: Statistical Arbitrage & Mean Reversion

#### [NEW] [statisticalArbitrage.py](file:///c:/Users/ibrah/PycharmProjects/borsa31/statisticalArbitrage.py)
- `adfTest` — Augmented Dickey-Fuller for stationarity.
- `cointegrationTest` — Engle-Granger for pair validation.
- `zScore` — Entry/exit signal generation for mean-reversion.

---

## Phase 3: Algorithmic Signal Processing

#### [NEW] [signalProcessing.py](file:///c:/Users/ibrah/PycharmProjects/borsa31/signalProcessing.py)
- `rsi`, `macd`, `bollingerBands` — Confluence logic.
- Automated pattern detection filters.

---

## Phase 4: Risk Engineering

#### [NEW] [riskManagement.py](file:///c:/Users/ibrah/PycharmProjects/borsa31/riskManagement.py)
- `kellyCriterion` — Optimal position sizing.
- `valueAtRisk` — Portfolio maximum loss boundary.

---

## Verification Plan

### Automated Tests
- Run `marketData.py` to verify data retrieval + contract validation for `THYAO.IS`.
- Unit tests for `zScore` and `kellyCriterion` with hardcoded values.
- Cache invalidation test: change cleaner version → verify re-fetch.

### Manual Verification
- Compare fetched OHLC data against TradingView chart for a known date range.
- Verify VaR calculations against manual spreadsheet.
