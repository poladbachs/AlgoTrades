from __future__ import print_function

import datetime
import numpy as np
import pandas as pd
import yfinance as yf

def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods, N. N defaults to 252, which then assumes a stream of daily returns.
    The function assumes that the returns are the excess of
    those compared to a benchmark.
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def equity_sharpe(ticker): 
    """
    Calculates the annualised Sharpe ratio based on the daily
    returns of an equity ticker symbol listed in Google Finance.

    The dates have been hardcoded here for brevity. 
    """
    start = datetime.datetime(2020,1,1)
    end = datetime.datetime(2023,1,1)

    # Obtain the equities daily historic data for the desired time period 
    # and add to a pandas DataFrame
    pdf = yf.download(ticker, 'google', start=start, end=end)

