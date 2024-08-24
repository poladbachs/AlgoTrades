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

# Function to download a contract from Nasdaq Data Link
def download_contract_from_quandl(contract, dl_dir, api_key):
    """
    Download an individual futures contract from Nasdaq Data Link and then
    store it to disk in the 'dl_dir' directory.
    """
    # Construct the API call from the contract and api_key
    api_call = f"https://data.nasdaq.com/api/v3/datasets/CHRIS/CME_{contract}.csv"
    params = f"?api_key={api_key}&order=asc"
    full_url = f"{api_call}{params}"

    # Download the data from Nasdaq Data Link
    response = requests.get(full_url)