import yfinance as yf
import pandas as pd
from pathlib import Path


def get_data(start: str,
             end: str):

    """
    Function to get stock data of the top 50 companies in the S&P 500 from Kaggle.
    """

    Path("data").mkdir(parents=True, exist_ok=True)

    if not Path("data/all_stocks_5yr.csv").exists():
        print("Download data from camnugent/sandp500 on Kaggle")
    else:
        df = pd.read_csv("data/all_stocks_5yr.csv", delimiter=",")

        # Calculating ADV to find top 50 stocks using last 60 trading days.
        df["APV"] = df["close"] * df["volume"]

        df["date"] = pd.to_datetime(df["date"])
        mask = (df["date"] >= "2017-12-01") & (df["date"] <= "2018-02-07")

        mean_apv_per_stock = df[mask].groupby("Name")["APV"].mean()

        top_50 = mean_apv_per_stock.sort_values(ascending=False).head(50)

        # Filtering out invalid tickers or replacing ticker with new ticker.
        ticker_map = {
            "BRK.B": "BRK-B",
            "PCLN": "BKNG",
            "CELG": None,
            "FB": "META"
        }

        tickers = [ticker_map.get(t, t) for t in top_50.index if ticker_map.get(t, t) is not None]

        data = yf.download(tickers=tickers, 
                           start=start, end=end,
                           auto_adjust=True,
                           group_by="ticker")
        
        # Getting adjusted close price for each ticker [multi-level dataframe so use .xs()]
        adj_close = data.xs("Close", axis=1, level="Price").resample("W").last()

        adj_close.to_csv("data/adj_close_prices.csv")


if __name__ == "__main__":
    get_data()