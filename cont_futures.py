from __future__ import print_function 

import datetime
import numpy as np 
import pandas as pd
import Quandl

def futures_rollover_weights(start_date, expiry_dates, contracts, rollover_days=5):
    """This constructs a pandas DataFrame that contains weights (between 0.0 and 1.0) 
    of contract positions to hold in order to carry out a rollover of rollover_days 
    prior to the expiration of the earliest contract. The matrix can then be 'multiplied' 
    with another DataFrame containing the settle prices of each
    contract in order to produce a continuous time series
    futures contract."""

    # Construct a sequence of dates beginning
    # from the earliest contract start date to the end
    # date of the final contract
    dates = pd.date_range(start_date, expiry_dates[-1], freq='B')

    # Create the ’roll weights’ DataFrame that will store the multipliers for 
    # each contract (between 0.0 and 1.0)
    roll_weights = pd.DataFrame(np.zeros((len(dates), len(contracts))),
                                index=dates, columns=contracts)
    prev_date = roll_weights.index[0]

    