# Manual: BIST Data Infrastructure (`marketData.py`)

This document provides a technical and mathematical explanation of the Data Infrastructure layer (Phase 1) within the `borsa31` framework.

---

## 1. What This Block Does

The `marketData.py` module acts as a **Quantitative Data Gateway**. It is responsible for the entire lifecycle of market data before it reaches your trading algorithms:

1.  **Ingestion:** Fetches raw data from providers (starting with Yahoo Finance).
2.  **Normalization:** Converts varied provider formats into a strict **Data Contract**.
3.  **Cleaning:** Removes "noise" such as duplicate bars and non-trading days (holidays/weekends).
4.  **Localization:** Synchronizes all timestamps to the `Europe/Istanbul` timezone.
5.  **Caching:** Stores processed data in high-speed, binary **Parquet** files to minimize latency and API calls.

---

## 2. Why It Was Built This Way (Engineering Rationale)

In quantitative finance, "Garbage In, Garbage Out" is the biggest risk. This module was built as a **5-Layer Architecture** to eliminate data-related errors:

*   **Provider Independence:** By using a `BaseProvider` interface, the project is not "married" to Yahoo Finance. You can swap it for Matriks IQ or a direct Broker API in the future without changing a single line of your analysis code.
*   **Math-Ready Vectors:** Most Python libraries don't handle BIST-specific nuances (like specific holidays or UTC+3 logic). This module guarantees that every `DataFrame` is physically ready for Linear Algebra and Statistical tests.
*   **Versioned Caching:** Unlike traditional CSV logs, our cache is **Versioned**. If the cleaning logic changes (e.g., how dividends are handled), the system detects the version mismatch and automatically re-downloads "fresh" data.

---

## 3. The Output Form: `Dict[str, pd.DataFrame]`

When you run the system, you get a "Dictionary of Matrices."

### The Dictionary Keys
The keys correspond to the **Tickers** (e.g., `"THYAO"`, `"GARAN"`). This allows for multi-symbol operations like:
```python
spread = data["AKBNK"]["adjClose"] - data["GARAN"]["adjClose"]
```

### The DataFrame (The Matrix)
Each value is a **Pandas DataFrame** that follows a strict **Contract**:

| Column | Data Type | Meaning |
| :--- | :--- | :--- |
| **Index** | `datetime64[ns, Europe/Istanbul]` | The "Time Axis". Guaranteed sorted and gap-filtered. |
| **`open`** | `float64` | Initial equilibrium price of the session. |
| **`high`** | `float64` | Maximum liquidity reach; used for resistance analysis. |
| **`low`** | `float64` | Minimum liquidity reach; used for support analysis. |
| **`close`** | `float64` | Final settlement price for the bar. |
| **`volume`** | `int64` | Total turnover; used to weigh the significance of a move. |
| **`adjClose`** | `float64` | **True Economic Value**. Adjusted for splits and dividends. |

---

## 4. How to Interpret the Data

To use this data like a Mathematician, interpret the columns as follows:

### A. The "Real" Price (`adjClose`)
Never use `close` for long-term calculations (especially for BIST stocks which pay frequent dividends). **Interpretation:** If `adjClose` moves from 100 to 105, your net wealth increased by 5%, regardless of whether a dividend was paid or a split happened.

### B. The Sentiment Ratio (`volume`)
**Interpretation:** A price increase on high volume suggests **Institutional accumulation** (Raporda belirtilen "emir akışı"). A price increase on low volume is often "noise" and likely to mean-revert.

### C. Volatility Boundary (`high` - `low`)
**Interpretation:** The distance between High and Low represents the **Intraday Volatility**. For Mean-Reversion models, we look for cases where the price touches these boundaries without high-volume support.

### D. Timezone-Aware Index
**Interpretation:** Because the index is aware of Istanbul time (`+03:00`), you can safely compare this data with local economic events (CBRT announcements at 14:00, etc.) without doing manual hour calculations.

---

## 5. Usage in Mathematical Projects

The output is perfectly shaped for:
1.  **ADF Testing:** Checking if a price series is "Stationary."
2.  **Log-Returns:** Calculating $ln(P_t / P_{t-1})$ for risk distribution.
3.  **Z-Score Analysis:** Measuring how many standard deviations the current price is away from the mean.

> [!TIP]
> Use the `demo.py` script to see these interpretations in action on live BIST 30 data.
