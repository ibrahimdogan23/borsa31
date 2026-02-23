"""
statisticalArbitrage.py — Phase 2: Statistical Arbitrage & Mean Reversion

3-Layer Architecture:
    Layer 1: Math Core       — Pure, stateless mathematical functions.
    Layer 2: Statistical Tests — Scientific validation of pair viability.
    Layer 3: PairAnalyzer     — Facade for discovery, diagnostics, and signals.

Engineering Decisions:
    - All cointegration uses ln(adjClose) to avoid nominal price bias.
    - Rolling window defaults to 60 days (BIST regime dynamics).
    - Stop-loss at |Z| > 3.5 is embedded in signal generation.
    - Hurst Exponent serves as a regime quality filter.
"""

import logging
import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

logger = logging.getLogger("statisticalArbitrage")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# ──────────────────────────────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────────────────────────────

@dataclass
class AdfResult:
    """Result of an Augmented Dickey-Fuller test."""
    isStationary: bool
    pValue: float
    testStatistic: float
    criticalValues: Dict[str, float]


@dataclass
class CointegrationResult:
    """Result of an Engle-Granger cointegration test."""
    isCointegrated: bool
    hedgeRatio: float
    intercept: float
    adfResult: AdfResult
    hurstExponent: float


@dataclass
class PairDiagnostic:
    """Full diagnostic summary for a single pair."""
    symbolA: str
    symbolB: str
    cointegration: CointegrationResult
    currentZScore: float
    spreadMean: float
    spreadStd: float
    volumeA: float
    volumeB: float


@dataclass
class PairSignal:
    """Trading signal for a pair at a specific point in time."""
    date: pd.Timestamp
    zScore: float
    action: str  # "BUY_SPREAD", "SELL_SPREAD", "EXIT", "STOP_LOSS", "HOLD"


# ── BIST Sector Map (for overlap warning) ────────────────────────────

BIST_SECTORS: Dict[str, str] = {
    "AKBNK": "Banking", "GARAN": "Banking", "ISCTR": "Banking",
    "YKBNK": "Banking", "HALKB": "Banking", "VAKBN": "Banking",
    "THYAO": "Aviation", "PGSUS": "Aviation",
    "TUPRS": "Energy", "EREGL": "Steel",
    "BIMAS": "Retail", "MGROS": "Retail",
    "KOZAL": "Mining", "KOZAA": "Mining",
    "KCHOL": "Holding", "SAHOL": "Holding", "SISE": "Holding",
    "TCELL": "Telecom", "TTKOM": "Telecom",
    "ASELS": "Defense", "SASA": "Chemicals",
    "TAVHL": "Aviation", "EKGYO": "REIT",
    "PETKM": "Chemicals", "TOASO": "Automotive",
    "FROTO": "Automotive", "ARCLK": "Electronics",
    "ENKAI": "Construction", "GUBRF": "Chemicals",
    "SOKM": "Retail",
}


# ══════════════════════════════════════════════════════════════════════
# LAYER 1: MATH CORE — Pure, stateless functions
# ══════════════════════════════════════════════════════════════════════

def calculateLogReturns(series: pd.Series) -> pd.Series:
    """
    Calculate log-returns: r_t = ln(P_t / P_{t-1}).

    Why log-returns?
    - Additive across time (sum of daily log-returns = total period return).
    - Approximately normally distributed (required for Z-score validity).
    - Symmetric: +10% and -10% have equal magnitude.
    """
    return np.log(series / series.shift(1)).dropna()


def calculateSpread(seriesA: pd.Series, seriesB: pd.Series,
                    hedgeRatio: float) -> pd.Series:
    """
    Calculate the spread between two log-price series.
    
    Formula: z_t = ln(P_A) - gamma * ln(P_B)
    
    The hedge ratio (gamma) tells you how many units of B to hold
    for every unit of A. If this spread is stationary, it will
    mean-revert — and that's where the profit opportunity lives.
    """
    logA = np.log(seriesA)
    logB = np.log(seriesB)
    return logA - hedgeRatio * logB


def calculateZScore(spread: pd.Series, window: int = 60) -> pd.Series:
    """
    Normalize the spread to a rolling Z-score.

    Formula: Z = (z_t - mean_rolling) / std_rolling

    Why rolling (not static)?
    BIST regimes change frequently due to TCMB decisions and inflation.
    A static mean from 2 years ago is meaningless if the macro environment
    has shifted. The 60-day window captures ~3 months of data, which matches
    the typical BIST regime duration.
    """
    rollingMean = spread.rolling(window=window).mean()
    rollingStd = spread.rolling(window=window).std()
    # Avoid division by zero
    rollingStd = rollingStd.replace(0, np.nan)
    return ((spread - rollingMean) / rollingStd).dropna()


def calculateHurst(series: pd.Series) -> float:
    """
    Calculate the Hurst Exponent using Rescaled Range (R/S) analysis.

    Interpretation:
        H < 0.5  → Mean-reverting (our target for pairs trading)
        H = 0.5  → Random walk (no edge — do not trade)
        H > 0.5  → Trending (requires different strategy)

    Why this matters:
    ADF tells us "is this series stationary?" (yes/no).
    Hurst tells us "HOW STRONGLY does it mean-revert?" (quality score).
    A pair can pass ADF but have H ≈ 0.48 (barely mean-reverting) vs
    H ≈ 0.3 (strongly mean-reverting). We want the latter.

    Implementation note:
    R/S analysis is applied to the RETURNS (first differences) of the
    series, not the raw levels. This is critical for financial data
    where price levels are non-stationary by nature.
    """
    values = series.dropna().values
    n = len(values)
    if n < 100:
        logger.warning("Hurst: series too short (%d points), need >= 100", n)
        return 0.5

    # Work on returns (first differences) — not raw levels
    returns = np.diff(values)
    nRet = len(returns)

    # Use log-spaced window sizes for better scale coverage
    minWindow = 10
    maxWindow = nRet // 2
    if maxWindow < minWindow:
        return 0.5

    windowSizes = np.unique(
        np.logspace(np.log10(minWindow), np.log10(maxWindow),
                    num=30, dtype=int)
    )

    sizes = []
    rsValues = []

    for size in windowSizes:
        nSubSeries = nRet // size
        if nSubSeries < 1:
            continue

        rsForSize = []
        for i in range(nSubSeries):
            chunk = returns[i * size:(i + 1) * size]
            mean = np.mean(chunk)
            deviations = chunk - mean
            cumulativeDeviation = np.cumsum(deviations)
            R = np.max(cumulativeDeviation) - np.min(cumulativeDeviation)
            S = np.std(chunk, ddof=1)
            if S > 1e-12:
                rsForSize.append(R / S)

        if rsForSize:
            sizes.append(size)
            rsValues.append(np.mean(rsForSize))

    if len(sizes) < 3:
        logger.warning("Hurst: insufficient window sizes for regression")
        return 0.5

    # Linear regression on log(size) vs log(R/S) → slope = H
    logSizes = np.log(np.array(sizes, dtype=float))
    logRS = np.log(np.array(rsValues, dtype=float))
    coefficients = np.polyfit(logSizes, logRS, 1)
    H = coefficients[0]

    # Clamp to [0, 1] range
    return float(np.clip(H, 0.0, 1.0))



# ══════════════════════════════════════════════════════════════════════
# LAYER 2: STATISTICAL TESTS — Scientific validation
# ══════════════════════════════════════════════════════════════════════

def runAdfTest(series: pd.Series, significance: float = 0.05) -> AdfResult:
    """
    Run the Augmented Dickey-Fuller test for stationarity.

    Null Hypothesis: The series has a unit root (non-stationary).
    If p-value < significance → reject null → series IS stationary.

    Why this is the first gate:
    You cannot run meaningful regressions on non-stationary data.
    If two price series are both non-stationary but their spread is
    stationary, we have cointegration — the mathematical "rubber band."
    """
    clean = series.dropna()
    result = adfuller(clean, autolag="AIC")

    testStat = result[0]
    pValue = result[1]
    critValues = result[4]

    return AdfResult(
        isStationary=(pValue < significance),
        pValue=round(pValue, 6),
        testStatistic=round(testStat, 6),
        criticalValues={k: round(v, 6) for k, v in critValues.items()}
    )


def runCointegrationTest(seriesA: pd.Series, seriesB: pd.Series,
                         significance: float = 0.05) -> CointegrationResult:
    """
    Run the Engle-Granger two-step cointegration test.

    Step 1: OLS regression → y1 = gamma * y2 + mu + epsilon
    Step 2: ADF test on residuals (epsilon_t)
    
    If residuals are stationary → the pair is cointegrated.

    The hedge ratio (gamma) from Step 1 tells you how to construct
    the market-neutral position: Long 1 unit of A, Short gamma units of B.
    """
    # Use log prices for percentage-based spread
    logA = np.log(seriesA).dropna()
    logB = np.log(seriesB).dropna()

    # Align indices
    aligned = pd.concat([logA, logB], axis=1).dropna()
    aligned.columns = ["A", "B"]

    # Step 1: OLS regression (with constant)
    X = sm.add_constant(aligned["B"])
    model = sm.OLS(aligned["A"], X).fit()
    hedgeRatio = model.params.iloc[1]
    intercept = model.params.iloc[0]
    residuals = model.resid

    # Step 2: ADF on residuals
    adfResult = runAdfTest(residuals, significance)

    # Quality check: Hurst exponent on residuals
    hurstH = calculateHurst(residuals)

    result = CointegrationResult(
        isCointegrated=adfResult.isStationary,
        hedgeRatio=round(hedgeRatio, 6),
        intercept=round(intercept, 6),
        adfResult=adfResult,
        hurstExponent=round(hurstH, 4)
    )

    logger.info("Cointegration test: cointegrated=%s, hedgeRatio=%.4f, "
                "ADF p=%.4f, Hurst=%.4f",
                result.isCointegrated, hedgeRatio,
                adfResult.pValue, hurstH)

    return result


def calculateRollingHedgeRatio(seriesA: pd.Series, seriesB: pd.Series,
                               window: int = 60) -> pd.Series:
    """
    Calculate a dynamic hedge ratio using Rolling OLS.

    Why rolling (not static)?
    In BIST, TCMB interest rate decisions and inflation data cause
    frequent macro regime shifts. A hedge ratio calculated over the
    entire history may be dominated by old, irrelevant data.

    The 60-day window adapts dynamically:
    - If AKBNK starts fundamentally outperforming ISCTR, gamma shifts.
    - Your position sizing adjusts automatically.
    """
    logA = np.log(seriesA).dropna()
    logB = np.log(seriesB).dropna()

    aligned = pd.concat([logA, logB], axis=1).dropna()
    aligned.columns = ["A", "B"]

    X = sm.add_constant(aligned["B"])
    rollingModel = RollingOLS(aligned["A"], X, window=window)
    rollingResult = rollingModel.fit()

    # The hedge ratio is the coefficient of B (second column)
    return rollingResult.params["B"]


# ══════════════════════════════════════════════════════════════════════
# LAYER 3: PAIR ANALYZER — Facade & Logic Gate
# ══════════════════════════════════════════════════════════════════════

class PairAnalyzer:
    """
    The single public API for Statistical Arbitrage.

    Orchestrates:
    - Pair discovery from a universe of stocks.
    - Full pair diagnostics (hedge ratio, ADF, Hurst, Z-score).
    - Signal generation with embedded stop-loss.
    - Sector overlap warnings.

    Usage:
        from marketData import MarketData, Timeframe
        from statisticalArbitrage import PairAnalyzer

        md = MarketData()
        data = md.load(["AKBNK", "ISCTR", "GARAN"], Timeframe.daily, "2024-01-01")
        analyzer = PairAnalyzer(data)
        pairs = analyzer.findCointegratedPairs()
    """

    def __init__(self, dataset: Dict[str, pd.DataFrame],
                 window: int = 60,
                 minVolume: float = 1_000_000):
        """
        Args:
            dataset:   Dict from MarketData.load() → {symbol: DataFrame}
            window:    Rolling window for Z-score and hedge ratio (default: 60 days)
            minVolume: Minimum average daily volume to consider a stock tradeable
        """
        self.dataset = dataset
        self.window = window
        self.minVolume = minVolume

    def _getAdjClose(self, symbol: str) -> pd.Series:
        """Extract adjClose series for a symbol."""
        return self.dataset[symbol]["adjClose"]

    def _getAvgVolume(self, symbol: str) -> float:
        """Calculate average daily volume for a symbol."""
        return float(self.dataset[symbol]["volume"].mean())

    def _checkSectorOverlap(self, pairs: List[Tuple[str, str]]) -> None:
        """Log a warning if multiple pairs come from the same sector."""
        sectorCounts: Dict[str, int] = {}
        for symbolA, symbolB in pairs:
            sectorA = BIST_SECTORS.get(symbolA, "Unknown")
            sectorB = BIST_SECTORS.get(symbolB, "Unknown")
            if sectorA == sectorB and sectorA != "Unknown":
                sectorCounts[sectorA] = sectorCounts.get(sectorA, 0) + 1

        for sector, count in sectorCounts.items():
            if count > 1:
                logger.warning(
                    "⚠ SECTOR OVERLAP: %d pairs in '%s' sector — "
                    "trading all simultaneously is effectively a single "
                    "sector bet. Defer to Phase 4 risk limits.", count, sector
                )

    def findCointegratedPairs(self,
                              significance: float = 0.05,
                              maxHurst: float = 0.5
                              ) -> List[Tuple[str, str, CointegrationResult]]:
        """
        Scan the entire universe for cointegrated pairs.

        Filters:
        1. Both stocks must have avg daily volume > minVolume.
        2. Engle-Granger cointegration test must pass (p < significance).
        3. Hurst exponent of residuals must be < maxHurst.
        """
        symbols = list(self.dataset.keys())
        validPairs = []

        # Filter by liquidity first
        liquidSymbols = [
            s for s in symbols
            if self._getAvgVolume(s) >= self.minVolume
        ]

        if len(liquidSymbols) < 2:
            logger.warning("Fewer than 2 liquid symbols (minVolume=%d). "
                           "Cannot find pairs.", self.minVolume)
            return []

        logger.info("Scanning %d liquid symbols (%d combinations)...",
                     len(liquidSymbols),
                     len(list(combinations(liquidSymbols, 2))))

        for symbolA, symbolB in combinations(liquidSymbols, 2):
            try:
                priceA = self._getAdjClose(symbolA)
                priceB = self._getAdjClose(symbolB)

                result = runCointegrationTest(priceA, priceB, significance)

                if result.isCointegrated and result.hurstExponent < maxHurst:
                    validPairs.append((symbolA, symbolB, result))
                    logger.info("✓ PAIR FOUND: %s — %s | hedge=%.4f | "
                                "ADF p=%.4f | H=%.4f",
                                symbolA, symbolB, result.hedgeRatio,
                                result.adfResult.pValue, result.hurstExponent)
            except Exception as e:
                logger.debug("Skipping %s-%s: %s", symbolA, symbolB, e)

        # Sector overlap check
        pairTuples = [(a, b) for a, b, _ in validPairs]
        self._checkSectorOverlap(pairTuples)

        logger.info("Found %d cointegrated pairs out of %d combinations.",
                     len(validPairs),
                     len(list(combinations(liquidSymbols, 2))))

        return validPairs

    def analyzePair(self, symbolA: str, symbolB: str) -> PairDiagnostic:
        """
        Full diagnostic for a specific pair.

        Returns a PairDiagnostic with:
        - Cointegration test results (hedge ratio, ADF, Hurst)
        - Current Z-score
        - Spread statistics (mean, std)
        - Average volumes for both legs
        """
        priceA = self._getAdjClose(symbolA)
        priceB = self._getAdjClose(symbolB)

        cointegration = runCointegrationTest(priceA, priceB)
        spread = calculateSpread(priceA, priceB, cointegration.hedgeRatio)
        zScores = calculateZScore(spread, self.window)

        currentZ = float(zScores.iloc[-1]) if len(zScores) > 0 else 0.0

        return PairDiagnostic(
            symbolA=symbolA,
            symbolB=symbolB,
            cointegration=cointegration,
            currentZScore=round(currentZ, 4),
            spreadMean=round(float(spread.mean()), 6),
            spreadStd=round(float(spread.std()), 6),
            volumeA=self._getAvgVolume(symbolA),
            volumeB=self._getAvgVolume(symbolB)
        )

    @staticmethod
    def generateSignals(spread: pd.Series,
                        window: int = 60,
                        entryZ: float = 2.0,
                        exitZ: float = 0.5,
                        stopLossZ: float = 3.5
                        ) -> List[PairSignal]:
        """
        Generate trading signals from a spread series.

        Signal Logic:
            Z > +entryZ     → SELL_SPREAD (short A, long B)
            Z < -entryZ     → BUY_SPREAD  (long A, short B)
            |Z| < exitZ     → EXIT        (take profit at mean)
            |Z| > stopLossZ → STOP_LOSS   (structural break)
            otherwise       → HOLD

        The ±3.5 stop-loss is critical for BIST:
        Under a normal distribution, |Z| > 3.5 has < 0.05% probability.
        If reached, the cointegration assumption has likely suffered a
        structural break — holding the position is mathematically unjustified.
        """
        zScores = calculateZScore(spread, window)
        signals = []

        for date, z in zScores.items():
            zVal = float(z)
            if abs(zVal) > stopLossZ:
                action = "STOP_LOSS"
            elif zVal > entryZ:
                action = "SELL_SPREAD"
            elif zVal < -entryZ:
                action = "BUY_SPREAD"
            elif abs(zVal) < exitZ:
                action = "EXIT"
            else:
                action = "HOLD"

            signals.append(PairSignal(date=date, zScore=round(zVal, 4),
                                      action=action))

        return signals


# ══════════════════════════════════════════════════════════════════════
# SELF-TEST
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 2: Statistical Arbitrage — Self-Test")
    print("=" * 60)

    # --- Unit Test: Math Core ---
    print("\n[UNIT TEST: Math Core]")

    # Test calculateLogReturns
    testPrices = pd.Series([100, 105, 110, 108, 112])
    logRet = calculateLogReturns(testPrices)
    print(f"  Log-returns of [100,105,110,108,112]: {logRet.values.round(4)}")

    # Test calculateHurst on synthetic mean-reverting series
    np.random.seed(42)
    meanRevertingSeries = pd.Series(np.cumsum(np.random.randn(500) * 0.5)
                                    + np.sin(np.linspace(0, 20, 500)))
    H = calculateHurst(meanRevertingSeries)
    print(f"  Hurst of synthetic series: {H:.4f} (expect < 0.5 for mean-reversion)")

    # Test calculateZScore
    testSpread = pd.Series(np.random.randn(100))
    zScores = calculateZScore(testSpread, window=20)
    print(f"  Z-Score series length: {len(zScores)} (from 100 spread values, "
          f"window=20)")
    print(f"  Z-Score range: [{zScores.min():.2f}, {zScores.max():.2f}]")

    # --- Unit Test: ADF ---
    print("\n[UNIT TEST: ADF Test]")
    stationarySeries = pd.Series(np.random.randn(200))
    adf = runAdfTest(stationarySeries)
    print(f"  White noise: stationary={adf.isStationary}, p={adf.pValue}")

    randomWalk = pd.Series(np.cumsum(np.random.randn(200)))
    adf2 = runAdfTest(randomWalk)
    print(f"  Random walk: stationary={adf2.isStationary}, p={adf2.pValue}")

    # --- Integration Test: Real BIST Data ---
    print("\n[INTEGRATION TEST: AKBNK vs ISCTR]")
    try:
        from marketData import MarketData, Timeframe

        md = MarketData()
        data = md.load(["AKBNK", "ISCTR"], Timeframe.daily, "2024-06-01")

        analyzer = PairAnalyzer(data, window=60)
        diag = analyzer.analyzePair("AKBNK", "ISCTR")

        print(f"  Cointegrated: {diag.cointegration.isCointegrated}")
        print(f"  Hedge Ratio (γ): {diag.cointegration.hedgeRatio}")
        print(f"  ADF p-value: {diag.cointegration.adfResult.pValue}")
        print(f"  Hurst Exponent: {diag.cointegration.hurstExponent}")
        print(f"  Current Z-Score: {diag.currentZScore}")
        print(f"  Spread μ: {diag.spreadMean}, σ: {diag.spreadStd}")
        print(f"  Avg Volume: AKBNK={diag.volumeA:,.0f}, "
              f"ISCTR={diag.volumeB:,.0f}")

        # Generate signals
        priceA = data["AKBNK"]["adjClose"]
        priceB = data["ISCTR"]["adjClose"]
        spread = calculateSpread(priceA, priceB, diag.cointegration.hedgeRatio)
        signals = PairAnalyzer.generateSignals(spread, window=60)

        # Count signal types
        actionCounts: Dict[str, int] = {}
        for sig in signals:
            actionCounts[sig.action] = actionCounts.get(sig.action, 0) + 1
        print(f"\n  Signal distribution: {actionCounts}")

        # Show last 5 signals that are not HOLD
        activeSignals = [s for s in signals if s.action != "HOLD"]
        print(f"  Active signals (non-HOLD): {len(activeSignals)}")
        if activeSignals:
            print("  Last 5 active signals:")
            for sig in activeSignals[-5:]:
                print(f"    {sig.date.strftime('%Y-%m-%d')} | Z={sig.zScore:+.2f} "
                      f"| {sig.action}")

    except ImportError:
        print("  ⚠ marketData module not found — skipping integration test.")
    except Exception as e:
        print(f"  ⚠ Integration test error: {e}")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)
