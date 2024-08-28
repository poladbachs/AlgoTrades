from __future__ import print_function

# Import the Time Series library
import statsmodels.tsa.stattools as ts

# Import Datetime and the Pandas DataReader
from datetime import datetime 
import yfinance as yf
import numpy as np

# Download the Amazon OHLCV data from 1/1/2000 to 1/1/2015
amzn = yf.download("AMZN", start="2000-1-1", end="2015-1-1")

# Extract the Adjusted Close prices
adj_close_prices = amzn['Adj Close'].values

# Output the results of the Augmented Dickey-Fuller test for Amazon
# with a lag order value of 1
result = ts.adfuller(amzn['Adj Close'], 1)

# Print the test result
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:')
for key, value in result[4].items():
    print(f'   {key}: {value}')

# Save the Adjusted Close prices to a file for Hurst exponent calculation
np.savetxt('amzn_adj_close.txt', adj_close_prices)