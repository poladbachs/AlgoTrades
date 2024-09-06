from __future__ import print_function 

import datetime
import numpy as np 
import pandas as pd
import statsmodels.api as sm

from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from hft_data import HistoricCSVDataHandlerHFT
from hft_portfolio import PortfolioHFT
from execution import SimulatedExecutionHandler

class IntradayOLSMRStrategy(Strategy): 
    """
    Uses ordinary least squares (OLS) to perform 
    a rolling linear regression to determine 
    the hedge ratio between a pair of equities.
    The z-score of the residuals time series is then calculated 
    in a rolling fashion and if it exceeds an interval of thresholds 
    (defaulting to [0.5, 3.0]) then a long/short signal pair are generated 
    (for the high threshold) or an exit signal pair are generated (for the low threshold).
    """

    def __init__(
        self, bars, events, ols_window=100, 
        zscore_low=0.5, zscore_high=3.0
    ):
        """
        Initialises the stat arb strategy.
        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.ols_window = ols_window
        self.zscore_low = zscore_low
        self.zscore_high = zscore_high
        self.pair = ('AREX', 'WLL')
        self.datetime = datetime.datetime.utcnow()

        self.long_market = False
        self.short_market = False

    def calculate_xy_signals(self, zscore_last): 
        """
        Calculates the actual x, y signal pairings
        to be sent to the signal generator.
        Parameters
        zscore_last - The current zscore to test against 
        """
        y_signal = None
        x_signal = None
        p0 = self.pair[0]
        p1 = self.pair[1]
        dt = self.datetime
        hr = abs(self.hedge_ratio)

        # If we're long the market and below the
        # negative of the high zscore threshold
        if zscore_last <= -self.zscore_high and not self.long_market:
            self.long_market = True
            y_signal = SignalEvent(1, p0, dt, 'LONG', 1.0)
            x_signal = SignalEvent(1, p1, dt, 'SHORT', hr)

        # If we're long the market and between the
        # absolute value of the low zscore threshold
        if abs(zscore_last) <= self.zscore_low and self.long_market:
            self.long_market = False
            y_signal = SignalEvent(1, p0, dt, 'EXIT', 1.0)
            x_signal = SignalEvent(1, p1, dt, 'EXIT', 1.0)

        # If we're short the market and above
        # the high zscore threshold
        if zscore_last >= self.zscore_high and not self.short_market:
            self.short_market = True
            y_signal = SignalEvent(1, p0, dt, 'SHORT', 1.0)
            x_signal = SignalEvent(1, p1, dt, 'LONG', hr)

        # If we're short the market and between the
        # absolute value of the low zscore threshold
        if abs(zscore_last) <= self.zscore_low and self.short_market:
            self.short_market = False
            y_signal = SignalEvent(1, p0, dt, 'EXIT', 1.0)
            x_signal = SignalEvent(1, p1, dt, 'EXIT', 1.0)

        return y_signal, x_signal