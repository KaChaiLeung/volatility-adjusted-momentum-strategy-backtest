import pandas as pd


def compute_weights_from_signals(signals: pd.DataFrame,
                                 rolling_vol: pd.DataFrame,
                                 lookback: int = 12,
                                 epsilon: float = 1e-4):
    
    weights = signals / (rolling_vol + epsilon)

    # Enforcing 10% weight limit
    weights = weights.clip(upper=0.1)

    # Replace invalid weights with 0
    weights = weights.replace([float("inf"), -float("inf")], 0)

    normalised_weights = weights.div(weights.sum(axis=1), axis=0)
    normalised_weights = normalised_weights.replace([float("inf"), -float("inf")], 0)
    normalised_weights = normalised_weights.fillna(0)

    return normalised_weights