from ib_insync import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Connect to IBKR
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure TWS or Gateway is running

# Define the contracts for the 4 technology equities
contracts = [
    Stock('AAPL', 'SMART', 'USD'),
    Stock('MSFT', 'SMART', 'USD'),
    Stock('GOOGL', 'SMART', 'USD'),
    Stock('META', 'SMART', 'USD')
]

# Request historical data for the past year (1D bars)
def fetch_historical_data(contract, duration='1 Y', barSize='1 day'):
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=barSize,
        whatToShow='ADJUSTED_LAST',
        useRTH=True,
        formatDate=1
    )
    return bars

# Fetch historical data
historical_data = {contract.symbol: fetch_historical_data(contract) for contract in contracts}

# Convert historical data to DataFrame
def bars_to_df(bars):
    df = util.df(bars)
    df.set_index('date', inplace=True)
    return df['close']

df_list = [bars_to_df(historical_data[symbol]) for symbol in historical_data]
prices_df = pd.concat(df_list, axis=1)
prices_df.columns = historical_data.keys()

# Calculate daily returns
returns_df = prices_df.pct_change().dropna()

# Calculate expected returns and covariance matrix
mean_returns = returns_df.mean()
cov_matrix = returns_df.cov()

# Define functions for portfolio optimization
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.dot(weights, mean_returns)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, std

def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    p_returns, p_std = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_returns - risk_free_rate) / p_std

def optimize_portfolio(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = minimize(negative_sharpe_ratio, num_assets * [1. / num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result

# Optimize portfolio
optimized_results = optimize_portfolio(mean_returns, cov_matrix)
optimized_weights = optimized_results.x

# Display optimized portfolio
optimized_portfolio = pd.DataFrame({'Weight': optimized_weights}, index=prices_df.columns)
print("Optimized Portfolio Weights:")
print(optimized_portfolio)

# Total investment amount
total_investment = 1000  # USD

# Calculate dollar amount for each stock
optimized_portfolio['Investment'] = optimized_portfolio['Weight'] * total_investment

# Fetch the latest market price for each stock
def fetch_latest_price(contract):
    ticker = ib.reqMktData(contract, '', False, False)
    ib.sleep(1)  # Give time for market data to be retrieved
    return ticker.last if ticker.last else ticker.close

latest_prices = {contract.symbol: fetch_latest_price(contract) for contract in contracts}
print("Latest Prices:", latest_prices)

# Calculate the number of shares to buy for each stock, allowing fractional shares
optimized_portfolio['Shares'] = optimized_portfolio.apply(lambda row: row['Investment'] / latest_prices[row.name], axis=1)

print("Investment Amounts and Shares to Buy:")
print(optimized_portfolio)

# Place market orders for each stock, allowing fractional shares
for symbol, shares in zip(optimized_portfolio.index, optimized_portfolio['Shares']):
    if shares > 0:
        contract = next(c for c in contracts if c.symbol == symbol)
        order = MarketOrder('BUY', float(shares))  # Use float to enable fractional shares
        trade = ib.placeOrder(contract, order)
        print(f"Placed order for {shares} shares of {symbol}")

# Disconnect from IBKR
ib.disconnect()
