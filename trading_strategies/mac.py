from __future__ import print_function 

import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm

from trading_engine.strategy import Strategy
from trading_engine.event import SignalEvent
from trading_engine.backtest import Backtest
from trading_engine.data import HistoricCSVDataHandler
from trading_engine.execution import SimulatedExecutionHandler
from trading_engine.portfolio import Portfolio

class MovingAverageCrossStrategy(Strategy): 
    """
    Carries out a basic Moving Average Crossover strategy 
    with a short/long simple weighted moving average. 
    Default short/long windows are 100/400 periods respectively.
    """
    def __init__(
        self, bars, events, short_window=100, long_window=400 
    ):
        """
        Initialises the Moving Average Cross Strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        short_window - The short moving average lookback.
        long_window - The long moving average lookback.
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

        # Set to True if a symbol is in the market
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self): 
        """
        Adds keys to the bought dictionary for all symbols 
        and sets them to 'OUT'.
        """
        bought = {}
        for s in self.symbol_list: 
            bought[s] = 'OUT'
        return bought