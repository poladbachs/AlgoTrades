from __future__ import print_function

import datetime 
import pprint 
try:
    import Queue as queue 
except ImportError:
    import queue 
import time

class Backtest(object): 
    """
    Enscapsulates the settings and components for carrying out
    an event-driven backtest.
    """
    def __init__(
        self, csv_dir, symbol_list, initial_capital,
            heartbeat, start_date, data_handler,
            execution_handler, portfolio, strategy
    ):
        """
        Initialises the backtest.
        Parameters:
        csv_dir - The hard root to the CSV data directory.
        symbol_list - The list of symbol strings.
        intial_capital - The starting capital for the portfolio. 
        heartbeat - Backtest "heartbeat" in seconds
        start_date - The start datetime of the strategy.
        data_handler - (Class) Handles the market data feed. 
        execution_handler - (Class) Handles the orders/fills for trades. 
        portfolio - (Class) Keeps track of portfolio current
        and prior positions.
        strategy - (Class) Generates signals based on market data. 
        """