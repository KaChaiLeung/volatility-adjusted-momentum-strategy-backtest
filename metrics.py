import pandas as pd
import numpy as np


def get_metrics(results: dict):

    V_0 = results.iloc[0]["portfolio_value"]
    V_F = results.iloc[-1]["portfolio_value"]
    days = (results.index[-1] - results.index[0]).days
    years = days / 365.25

    CAGR = (V_F / V_0) ** (1/years) - 1

    rets = results["net_return"].dropna()
    sharpe = rets.mean() / rets.std() * np.sqrt(52)

    downside = rets[rets < 0]
    sortino = rets.mean() / downside.std() * np.sqrt(52) if len(downside) > 1 else np.nan

    net_asset_value = results["portfolio_value"] / V_0
    running_max = net_asset_value.cummax()
    drawdown = (net_asset_value - running_max) / running_max
    max_drawdown = drawdown.min()

    calmar = CAGR / abs(max_drawdown) if max_drawdown < 0 else np.nan

    win_rate = (rets > 0).sum() / len(rets)

    gross_wins = rets[rets > 0].sum()
    gross_losses = -rets[rets < 0].sum()
    profit_factor = gross_wins / gross_losses if gross_losses > 0 else np.nan

    return {
        "CAGR": CAGR,
        "Sharpe Ratio": sharpe,
        "Drawdown": drawdown,
        "Max Drawdown": max_drawdown,
        "Profit Factor": profit_factor,
        "Win Rate": win_rate,
        "Calmar Ratio": calmar,
        "Sortino Ratio": sortino
    }