# Volatility-Adjusted Momentum Strategy Backtester

### Can a volatilty-filtered momentum strategy applied to liquid equities produce superior risk-adjusted returns compared to a passive benchmark like SPY?

## Fetching Data

- Found the top 50 stocks using Kaggle S&P 500 dataset
  - Used ADV as there was not market cap information available
  - Only used ADV data from most recent trading days (last 60 days)
- Downloaded data using yfinance
  - Filtered out invalid tickers e.g. CELG
  - Changed names of tickers to match yfinance names e.g. BRK.B -> BRK-B
- Created new dataframe of adjusted close prices
- Changed trading period from daily to weekly

## Calculate Returns

- Calculated percentage returns per week from adjusted close prices
  - Weekly data to reduce noise and overtrading
  - Smoother signals - better for medium-term strategies

## Generate Signals

- Defined lookback period of 12 weeks
- Calculated rolling momentum and rolling volatility of stocks in the past 12 weeks
- Calculated risk-adjusted momentum signals by dividing rolling momentum by rolling volatility
  - Reward strong, stable momentum and penalise noisy / erratic price movement
- Shifted signals down by 1 to account for execution delay
- Dropped any invalid entries e.g. inf from dividing by 0 when calculating signals
- Long-only strategy to avoid shorting complexities - no negative signals

## Weights

- Divide signals by rolling volatility - Kelly-optimal sizing (expected return / variance)
  - More cautious sizing for high-volatility assets
  - Bigger bets on stable assets with strong trends
- Capped weights at 10%
  - Avoids concentration risk - ensures diversification
  - Reduce volatility spikes and drawdowns due to overweighted positions
- Normalised weights so that total portfolio is used per week
  - Replaced any invalid entries (dividing by 0) so that no trades happen

## Simulate Portfolio

- Shifted weights to align with returns and account for execution delay
- Loop through each trading week
  - Multiply weights by last week's portfolio value to get value allocated per stock for that week
  - Enforcing 2% portfolio risk per trade
  - Enforcing minimum trade size
    - If allocated value less than minimum trade size then don't trade
  - Rebalanced portfolio every week to get gross return that week
  - Calculated transaction costs per week
  - Calculated net return per week by taking away transaction cost from gross return
  - Calculated new portfolio value by adding net return to previous week's portfolio value
- Returned dictionary of results
  - Date
  - Gross Return
  - Total Costs
  - Net Return
  - Turnover
  - Portfolio Value
- Looped through different lookback periods - best is 26 week lookback

## Metrics

- CAGR: 0.122
- Sharpe Ratio: 1.31
- Maximum Drawdown: -10.7%
- Profit Factor: 1.68
- Win Rate: 57.8%
- Calmar Ratio: 1.14
- Sortino Ratio: 1.37

## Conclusion

Over the period 2013 - 2018, the volatility-adjusted momentum strategy achieved a compound annual growth rate of 12.2%, beating a passive market return of ~9%. Drawdowns were well contained (max -10.7%) with a win rate of 57.8%, confirming the success of this strategy.

However, our risk adjusted metrics - Sharpe ratio 1.31, Calmar ratio 1.14 Sortino ratio 1.37, and profit factor 1.37 - falls short of our objectives. This indicates that returns are too volatile versus downside risk and drawdown, and profitable weeks do not offset losing ones.

In practical terms, this strategy demonstrates:

- Robust absolute performance against a tough benchmark, with limited drawdowns.
- Signal validity, capturing medium-term momentum more often than not.

To improve on this strategy, we will focus on:

- Sharpe/Sortino ratio enhancement via parameter refinement.
- Turnover & cost-control with volume-adaptive slippage models and reduced trading frequency.
- Portfolio-level controls (volatility targeting and stop-loss rules) to smooth returns and raise Calmar ratio.
- Out-of-sample validation through walk-forward tests to lock in robust parameter choices.
