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