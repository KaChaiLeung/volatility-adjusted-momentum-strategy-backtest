import yfinance as yf
import pandas as pd
import numpy as np

# 1) Download and prepare SPY data
spy = yf.download("SPY", start="2010-01-01", end="2025-07-01", auto_adjust=True)
spy_weekly = spy["Close"].resample("W-FRI").last()
spy_rets   = spy_weekly.pct_change().dropna()

# 2) Compute SPY’s start and end values
V0 = 100_000
spy_cum = (1 + spy_rets).cumprod() * V0
VT = spy_cum.iloc[-1]

# 3) Compute years elapsed
days = (spy_cum.index[-1] - spy_cum.index[0]).days
years = days / 365.25

# 4) SPY’s CAGR
cagr_spy = (VT / V0) ** (1/years) - 1
sharpe_spy = (spy_rets.mean() / spy_rets.std()) * np.sqrt(52)

print(cagr_spy)
print(sharpe_spy)