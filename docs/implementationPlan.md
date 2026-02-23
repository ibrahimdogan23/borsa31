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

## Phase 2: Statistical Arbitrage & Mean Reversion (`statisticalArbitrage.py`)

#### [NEW] [statisticalArbitrage.py](file:///c:/Users/ibrah/PycharmProjects/borsa31/statisticalArbitrage.py)

### Why This Phase Exists

In the BIST market, which is characterized by **higher volatility** and **lower efficiency** than US markets, mean-reversion strategies—specifically **Pairs Trading**—often yield superior risk-adjusted returns. Price series are typically non-stationary (Random Walks), so we cannot run regressions directly on prices. Instead, we look for pairs of assets whose **spread** is stationary (mean-reverting), meaning the pair is "tied together by a rubber band."

> [!IMPORTANT]
> Always use the **natural log of prices** (`ln(adjClose)`) when testing for cointegration. This ensures spreads represent **percentage deviations** rather than absolute TL differences, which is critical for BIST where nominal prices vary widely.

### 3-Layer Architecture

#### Layer 1: Math Core — Pure, Stateless Functions

Deterministic mathematical building blocks with no side effects.

| Function | What It Does | Why |
|---|---|---|
| `calculateLogReturns(series)` | $r_t = \ln(P_t / P_{t-1})$ | Log-returns are additive across time and normally distributed — required for Z-score validity. |
| `calculateSpread(seriesA, seriesB, hedgeRatio)` | $z_t = \ln(P_A) - \gamma \cdot \ln(P_B)$ | The "rubber band" between two assets. If stationary, this is where profit lives. |
| `calculateZScore(spread, window)` | $Z = (z_t - \mu_{rolling}) / \sigma_{rolling}$ | Normalizes the spread to standard deviations from the rolling mean. |
| `calculateHurst(series)` | Rescaled Range (R/S) analysis → $H$ exponent | **Quality filter**: $H<0.5$ = mean-reverting, $H=0.5$ = random walk, $H>0.5$ = trending. ADF says "yes/no"; Hurst says "how strongly." |

> [!NOTE]
> The Hurst Exponent serves as a **regime filter**. If $H$ climbs toward 0.5, the cointegration "rubber band" has snapped and trading should stop — regardless of what the ADF test says.

#### Layer 2: Statistical Tests — Scientific Validation

Functions that validate whether a pair is mathematically viable for trading.

| Function | What It Does | Why |
|---|---|---|
| `runAdfTest(series)` | Augmented Dickey-Fuller test → `(isStationary: bool, pValue: float)` | Rejects the null hypothesis of a unit root. $p < 0.05$ = stationary. |
| `runCointegrationTest(seriesA, seriesB)` | OLS regression $y_1 = \gamma y_2 + \mu + \epsilon$, then ADF on residuals $\epsilon_t$ | If residuals are stationary → the pair is cointegrated. Returns hedge ratio $\gamma$ and test results. |
| `calculateRollingHedgeRatio(seriesA, seriesB, window)` | Rolling OLS via `statsmodels.regression.rolling.RollingOLS` | **BIST-specific**: A static $\gamma$ breaks during macro regime shifts (TCMB decisions, inflation data). A **60-day rolling window** adapts dynamically. |

**Why 60-day rolling window?**
- **20 days**: Too short — captures market noise, not structure.
- **60 days**: ~3 months — matches BIST's typical "regime duration" between major macro events.
- **120 days**: Too slow — fails to adapt to Turkey's frequent policy shifts.

#### Layer 3: PairAnalyzer — Facade & Logic Gate

The single public API that orchestrates discovery, validation, and signal generation.

| Function | What It Does | Why |
|---|---|---|
| `findCointegratedPairs(universe, startDate, endDate)` | Iterates all combinations, runs cointegration test, filters by Hurst < 0.5 | Automated discovery of viable pairs from a stock universe. |
| `analyzePair(symbolA, symbolB)` | Full diagnostic: hedge ratio, ADF, Hurst, current Z-score | One-call summary of a specific pair's health. |
| `generateSignals(spread, window, entryZ, exitZ, stopLossZ)` | Entry/exit/stop-loss signal generation | The trading logic engine. |

**Signal Logic (Z-Score thresholds):**

| Z-Score | Action | Rationale |
|---|---|---|
| $Z > +2.0$ | **Sell spread** (Short $y_1$, Long $y_2$) | Spread is 2σ above mean — expect reversion. |
| $Z < -2.0$ | **Buy spread** (Long $y_1$, Short $y_2$) | Spread is 2σ below mean — expect reversion. |
| $Z \approx 0$ | **Exit position** | Mean reached — take profit. |
| $|Z| > 3.5$ | **⛔ Stop-Loss** | Structural break — cointegration assumption has failed ($<0.05\%$ probability under normal distribution). |

> [!WARNING]
> The $\pm 3.5$ stop-loss is embedded directly in `generateSignals()` rather than deferred to Phase 4. This ensures the PairAnalyzer never blindly waits for a mean reversion that may never come.

**Sector Overlap Warning:**
`findCointegratedPairs()` includes a **sector overlap check**. If multiple discovered pairs come from the same sector (e.g., AKBNK-ISCTR + GARAN-AKBNK = both Banking), a warning is logged. The actual position-level correlation limit (e.g., "max 40% in one sector") is deferred to Phase 4 (`riskManagement.py`).

### BIST-Specific Engineering Considerations

| Consideration | Implementation |
|---|---|
| **Sector-Based Pairing** | Focus on same-sector stocks (AKBNK vs ISCTR, KOZAL vs KOZAA) that share long-term economic equilibrium. |
| **Minimum Volume Filter** | Use Phase 1 `volume` data to exclude illiquid stocks — a pair may look cointegrated but be untradeable if one leg has no liquidity. |
| **Rolling Parameters** | All windows default to 60 days to match BIST regime dynamics. |
| **Log Prices** | All cointegration tests use `ln(adjClose)` to avoid nominal price bias. |

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
- **Sector correlation limit** — Enforces portfolio-level diversification (max % per sector).

---

## Verification Plan

### Phase 1 Tests
- Run `marketData.py` self-test: data retrieval + contract validation for `THYAO.IS`.
- Cache invalidation test: change cleaner version → verify re-fetch.

### Phase 2 Tests

| Stage | What | How |
|---|---|---|
| **Unit Test** | Math Core correctness | Hardcoded inputs → `calculateZScore([1,2,3])` must equal expected value. `calculateHurst()` on synthetic mean-reverting series must return $H < 0.5$. |
| **Integration Test** | Full pipeline on real BIST data | Load `AKBNK` + `ISCTR` via Phase 1 → run `runCointegrationTest()` → verify hedge ratio and p-value are plausible. |
| **Sanity Check** | Visual validation | Plot Z-score with `matplotlib` → Z should "bounce" between $\pm 2.0$ bands. If it trends constantly, cointegration has failed. |

### Manual Verification
- Compare fetched OHLC data against TradingView chart for a known date range.
- Verify VaR calculations against manual spreadsheet.

---

## Strategic Perspective: Numeric vs. Visual Analysis

The current framework prioritizes the **Numeric & Rule-Based Approach** (Signal Processing) for Phase 2 and 3. However, the architecture is designed to accommodate a potential pivot to **Visual / Computer Vision (CV)** based analysis if needed in future versions.

### Current Choice: Numeric (Signal Processing)
- **Mechanism:** OHLCV data $\rightarrow$ Confluence Rules (RSI, Bollinger, etc.) $\rightarrow$ Signals.
- **Why:** Faster backtesting, objective mathematical ground truth, and lower computational overhead.

### Future Potential: Visual (AI / Computer Vision)
- **Mechanism:** OHLCV data $\rightarrow$ Chart Image/GAF Matrix $\rightarrow$ CNN/Deep Learning Model $\rightarrow$ Pattern Recognition.
- **Why:** Can capture nuanced "market texture" that is hard to define with simple IF-THEN rules.

> [!NOTE]
> The Layered Provider architecture in `marketData.py` ensures that regardless of the mathematical perspective (Numeric or Visual), the underlying data stream remains the definitive "Single Source of Truth."
