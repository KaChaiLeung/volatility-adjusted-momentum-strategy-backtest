import pandas as pd


def generate_signals(returns: pd.DataFrame,
                     lookback: int = 12) -> pd.DataFrame:
    
    rolling_momentum = returns.rolling(window=lookback).sum()
    rolling_volatility = returns.rolling(window=lookback).std()

    signal = rolling_momentum / rolling_volatility

    # Shifting signals for execution delay
    shifted_signals = signal.shift(1)

    # Dropping any infinity values in case rolling_volatility = 0
    shifted_signals = shifted_signals.replace([float("inf"), -float("inf")], pd.NA).dropna()
    shifted_signals = shifted_signals.clip(lower=0)

    return shifted_signals, rolling_volatility