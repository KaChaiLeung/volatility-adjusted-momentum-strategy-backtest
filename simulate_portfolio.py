import pandas as pd

def simulate_portfolio(returns: pd.DataFrame,
                       weights: pd.DataFrame,
                       prices: pd.DataFrame,
                       initial_capital: float,
                       slippage: float,
                       commission: float,
                       bid_ask_spread: float,
                       min_trade_size: float,
                       val_at_risk_per_trade: float) -> pd.DataFrame:

    # Aligning for execution lag
    exec_weights = weights.shift(1).fillna(0)

    portfolio_val = initial_capital
    # Value in each asset last week
    prev_alloc = pd.Series(0.0, index=returns.columns)
    records = []


    for date in returns.index:

        r_t = returns.loc[date]
        w_t = exec_weights.loc[date]

        # Value allocated per stock
        alloc = w_t * portfolio_val

        # Enforcing 2% portfolio risk per trade
        max_alloc = portfolio_val * val_at_risk_per_trade
        alloc = alloc.clip(upper=max_alloc)

        # Enforcing minimum trade size (setting to 0 if below minimum)
        alloc = alloc.where(alloc >= min_trade_size, 0.0)

        # Value traded in/out of each position this week
        delta_alloc = (alloc - prev_alloc).abs()
        # Fraction of entire portfolio traded this week
        turnover_frac = delta_alloc.sum() / portfolio_val

        # Weight fraction * return for week gives asset's contribution to portfolio return this week
        gross_return = (alloc / portfolio_val * r_t).sum()

        # Calculating transaction costs
        cost_pct = slippage + commission + bid_ask_spread
        # Fraction of portfolio value payed for fees
        total_cost = turnover_frac * cost_pct

        # Portfolio value after fees
        net_return = gross_return - total_cost

        # Portfolio value for this week
        portfolio_val = portfolio_val * (1 + net_return)

        records.append({
            "date":       date,
            "gross_return": gross_return,
            "total_cost":   total_cost,
            "net_return":   net_return,
            "turnover":     turnover_frac,
            "portfolio_value": portfolio_val
        })

        prev_alloc = alloc.copy()

    result = pd.DataFrame(records).set_index("date").loc[returns.index]
    
    return result