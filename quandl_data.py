from __future__ import print_function

import matplotlib.pyplot as plt 
import pandas as pd
import requests
import os

API_KEY = "3fcLPCxYwGms3sVVn9NX"

# Function to construct futures symbols
def construct_futures_symbols(symbol, start_year=2020, end_year=2024):
    """
    Constructs a list of futures contract codes for a particular symbol and timeframe.
    """
    futures = []
    # March, June, September and
    # December delivery codes
    months = 'HMUZ'
    for y in range(start_year, end_year+1):
        for m in months:
            futures.append("%s%s%s" % (symbol, m, y))
    return futures

