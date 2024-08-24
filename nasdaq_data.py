from __future__ import print_function

import matplotlib.pyplot as plt
import pandas as pd
import requests
import os

# Set your Nasdaq Data Link API key here
API_KEY = "3fcLPCxYwGms3sVVn9NX"

# Function to download a contract from Nasdaq Data Link
def download_contract_from_nasdaq(dl_dir, api_key):
    """
    Download the continuous futures contract data from Nasdaq Data Link and then
    store it to disk in the 'dl_dir' directory.
    """
    # Construct the API call
    api_call = "https://data.nasdaq.com/api/v3/datasets/CHRIS/CME_ES1.csv"
    params = f"?api_key={api_key}&order=asc"
    full_url = f"{api_call}{params}"

    # Download the data from Nasdaq Data Link
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.text
        # Ensure the directory exists
        os.makedirs(dl_dir, exist_ok=True)
        # Store the data to disk
        with open(f'{dl_dir}/CME_ES1.csv', 'w') as fc:
            fc.write(data)
        print(f"Successfully downloaded contract data.")
    else:
        print(f"Failed to download data. HTTP Status: {response.status_code}")

# Main function to execute the script
if __name__ == "__main__":
    dl_dir = 'nasdaq_data/futures/ES'  # Directory to save the data

    # Download the continuous contract data
    download_contract_from_nasdaq(dl_dir, API_KEY)

    # Open up the downloaded contract via read_csv and plot the settle price
    contract_file = f"{dl_dir}/CME_ES1.csv"
    if os.path.exists(contract_file):
        es = pd.read_csv(contract_file, index_col="Date")
        es["Settle"].plot()
        plt.title("Continuous E-Mini S&P 500 Futures - Settle Price")
        plt.xlabel("Date")
        plt.ylabel("Settle Price")
        plt.show()
    else:
        print(f"File {contract_file} not found. Please check the download process.")