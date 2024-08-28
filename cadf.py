import datetime
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf
import pprint
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

def plot_price_series(df, ts1, ts2):
    """Plot two time series."""
    fig, ax = plt.subplots(figsize=(14, 7))
    months = mdates.MonthLocator()  # every month
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2023, 1, 1), datetime.datetime(2024, 1, 1))
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title(f'{ts1} and {ts2} Daily Prices')
    plt.legend()
    plt.show()

def plot_scatter_series(df, ts1, ts2):
    """Display a scatter plot of the two time series."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[ts1], df[ts2], alpha=0.5)
    plt.xlabel(f'{ts1} Price ($)')
    plt.ylabel(f'{ts2} Price ($)')
    plt.title(f'{ts1} and {ts2} Price Scatterplot')
    plt.show()

def plot_residuals(df):
    """Plot the residuals."""
    fig, ax = plt.subplots(figsize=(14, 7))
    months = mdates.MonthLocator()  # every month
    ax.plot(df.index, df["res"], label="Residuals")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2023, 1, 1), datetime.datetime(2024, 1, 1))
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Residual')
    plt.title('Residual Plot')
    plt.legend()
    plt.show()

def download_data(ticker, start, end):
    """Download data using yfinance with error handling."""
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise ValueError(f"No data returned for ticker {ticker}.")
        return data
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        return pd.DataFrame()  # return an empty DataFrame if there was an error

if __name__ == "__main__":
    start = '2023-01-01'
    end = '2024-01-01'

    # Download data using yfinance
    apple = download_data("AAPL", start=start, end=end)
    microsoft = download_data("MSFT", start=start, end=end)

    # Check if data is successfully retrieved
    if apple.empty or microsoft.empty:
        print("Error: One or more data sets could not be retrieved. Exiting.")
    else:
        # Create DataFrame
        df = pd.DataFrame(index=apple.index)
        df["AAPL"] = apple["Adj Close"]
        df["MSFT"] = microsoft["Adj Close"]

        # Plot the two time series
        plot_price_series(df, "AAPL", "MSFT")

        # Display a scatter plot of the two time series
        plot_scatter_series(df, "AAPL", "MSFT")
        
        # Calculate optimal hedge ratio "beta" using OLS
        x = sm.add_constant(df["AAPL"])  # add constant term for intercept
        model = sm.OLS(df["MSFT"], x).fit()
        beta_hr = model.params["AAPL"]

        # Calculate the residuals of the linear combination
        df["res"] = df["MSFT"] - beta_hr * df["AAPL"]

        # Plot the residuals
        plot_residuals(df)

        # Calculate and output the CADF test on the residuals
        cadf = ts.adfuller(df["res"])
        pprint.pprint(cadf)
