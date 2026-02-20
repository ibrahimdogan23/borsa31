from marketData import MarketData, Timeframe
from datetime import datetime, timedelta

def main():
    # 1. Initialize the framework
    # This will use YFinance as the default provider and Parquet for caching
    md = MarketData()

    # 2. Select a few tickers from the BIST 30 universe
    symbols = ["THYAO", "GARAN", "KCHOL"]
    
    # Let's look at the last 30 days
    startDate = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"--- FETCHING DATA FOR {symbols} ---")
    print(f"Start Date: {startDate}")
    
    # 3. Load the data
    # The first time you run this, it will fetch from Yahoo Finance.
    # The second time, it will be near-instant using the Parquet cache.
    dataset = md.load(symbols, timeframe=Timeframe.daily, startDate=startDate)

    # 4. Observe the results
    print("\n[RESULT STRUCTURE]")
    print(f"Type of output: {type(dataset)}")
    print(f"Loaded symbols: {list(dataset.keys())}")

    # Inspect one specific DataFrame (e.g., THYAO)
    symbol = "THYAO"
    df = dataset[symbol]

    print(f"\n[INSPECTING {symbol}]")
    print(f"Shape: {df.shape} (Rows, Columns)")
    print(f"Timezone: {df.index.tz}")
    
    print("\n[CONTRACT CONFORMITY - COLUMN TYPES]")
    print(df.dtypes)

    print("\n[LAST 5 TRADING DAYS]")
    # Printing the tail to see the most recent data points
    print(df.tail())

    print("\n[LOG-RETURNS CALCULATION - READY FOR PHASE 2]")
    # Showing how easy it is to prepare for math now that data is clean
    import numpy as np
    logReturns = np.log(df['adjClose'] / df['adjClose'].shift(1))
    print(f"Volatility (Std Dev of Log-Returns): {logReturns.std():.4f}")

if __name__ == "__main__":
    main()
