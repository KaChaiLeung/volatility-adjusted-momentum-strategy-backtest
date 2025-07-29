from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from data_utils import get_data
from signals import generate_signals
from weights import compute_weights_from_signals
from simulate_portfolio import simulate_portfolio
from metrics import get_metrics


LOOKBACK = 12
EPSILON = 1e-4
INITIAL_CAPITAL = 100000
SLIPPAGE = 0.001
COMMISSION = 0.0005
MIN_TRADE_SIZE = 100
BID_ASK_SPREAD = 0.0002
VAL_AT_RISK_PER_TRADE = 0.02
START = "2013-02-08"
END = "2018-02-07"


def main():
    
    if not Path("data/adj_close_prices.csv").exists():
        get_data(start=START, end=END)

    prices = pd.read_csv("data/adj_close_prices.csv",
                       index_col=0,
                       parse_dates=True)

    returns = prices.pct_change(periods=1).dropna()

    signals, rolling_volatility = generate_signals(returns=returns,
                               lookback=LOOKBACK)

    weights = compute_weights_from_signals(signals=signals,
                                           rolling_vol=rolling_volatility,
                                           lookback=LOOKBACK,
                                           epsilon=EPSILON)

    results = simulate_portfolio(returns=returns,
                       weights=weights,
                       prices=prices,
                       initial_capital=INITIAL_CAPITAL,
                       slippage=SLIPPAGE,
                       commission=COMMISSION,
                       bid_ask_spread=BID_ASK_SPREAD,
                       min_trade_size=MIN_TRADE_SIZE,
                       val_at_risk_per_trade=VAL_AT_RISK_PER_TRADE)
    
    metrics = get_metrics(results=results)

    plt.plot(metrics["Drawdown"])
    plt.show()

    print(f"CAGR: {metrics["CAGR"]} \nSharpe Ratio: {metrics["Sharpe Ratio"]} \nMax Drawdown: {metrics["Max Drawdown"]} \nProfit Factor: {metrics["Profit Factor"]} \nWin Rate: {metrics["Win Rate"]} \nCalmar Ratio: {metrics["Calmar Ratio"]} \nSortino Ratio: {metrics["Sortino Ratio"]}")


if __name__ == "__main__":
    main()