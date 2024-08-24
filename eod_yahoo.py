from __future__ import print_function
import datetime
import yfinance as yf

if __name__ == "__main__":
    spy = yf.download(
        "SPY", 
        start="2007-01-01", 
        end="2015-06-15"
    )
    print(spy.tail())