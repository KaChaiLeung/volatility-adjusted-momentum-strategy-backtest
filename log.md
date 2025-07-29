# Fetching Data

- Found the top 50 stocks using Kaggle S&P 500 dataset
  - Used ADV as there was not market cap information available
  - Only used ADV data from most recent trading days (last 60 days)
- Downloaded data using yfinance
  - Filtered out invalid tickers e.g. CELG
  - Changed names of tickers to match yfinance names e.g. BRK.B -> BRK-B
- Created new dataframe of adjusted close prices
- Changed trading period from daily to weekly

# Calculate Returns

- Calculated percentage returns per week from adjusted close prices
  - Weekly data to reduce noise and overtrading
  - Smoother signals - better for medium-term strategies

# Generate Signals

- Defined lookback period of 12 weeks
- Calculated rolling momentum and rolling volatility of stocks in the past 12 weeks
- Calculated risk-adjusted momentum signals by dividing rolling momentum by rolling volatility
  - Reward strong, stable momentum and penalise noisy / erratic price movement
- Shifted signals down by 1 to account for execution delay
- Dropped any invalid entries e.g. inf from dividing by 0 when calculating signals
- Long-only strategy to avoid shorting complexities - no negative signals

# Weights

- Divide signals by rolling volatility - Kelly-optimal sizing (expected return / variance)
  - More cautious sizing for high-volatility assets
  - Bigger bets on stable assets with strong trends
- Capped weights at 10%
  - Avoids concentration risk - ensures diversification
  - Reduce volatility spikes and drawdowns due to overweighted positions
- Normalised weights so that total portfolio is used per week
  - Replaced any invalid entries (dividing by 0) so that no trades happen
