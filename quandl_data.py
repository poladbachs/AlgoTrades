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
def download_contract_from_nasdaq(contract, dl_dir, api_key):
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

    if response.status_code == 200:
        data = response.text
        # Ensure the link exists
        os.makedirs(dl_dir, exist_ok=True)
        # Store the data to disk
        with open(f'{dl_dir}/{contract}.csv', 'w') as fc:
            fc.write(data)
        print(f"Successfully downloaded contract: {contract}")
    else:
        print(f"Failed to download data for contract {contract}. HTTP Status: {response.status_code}")

# Function to download all contracts within a date range
def download_historical_contracts(symbol, dl_dir, start_year=2020, end_year=2024, api_key=API_KEY):
    """
    Downloads all futures contracts for a specified symbol between a start_year and an end_year.
    """
    contracts = construct_futures_symbols(symbol, start_year, end_year)
    for c in contracts:
        download_contract_from_nasdaq(c, dl_dir, api_key)