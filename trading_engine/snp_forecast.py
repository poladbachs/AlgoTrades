

from __future__ import print_function
import datetime
import queue
import pandas as pd
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from create_lagged_series import create_lagged_series

class SPYDailyForecastStrategy(Strategy):
    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.datetime_now = datetime.datetime.utcnow()
        self.model_start_date = datetime.datetime(2001, 1, 10)
        self.model_end_date = datetime.datetime(2005, 12, 31)
        self.model_start_test_date = datetime.datetime(2005, 1, 1)
        self.long_market = False
        self.short_market = False
        self.bar_index = 0
        self.model = self.create_symbol_forecast_model()

    def create_symbol_forecast_model(self):
        snpret = create_lagged_series(
            self.symbol_list[0], self.model_start_date, 
            self.model_end_date, lags=5
        )
        X = snpret[["Lag1", "Lag2"]]
        y = snpret["Direction"]

        start_test = self.model_start_test_date
        X_train = X[X.index < start_test]
        X_test = X[X.index >= start_test]
        y_train = y[y.index < start_test]
        y_test = y[y.index >= start_test]
       
        model = QDA()
        model.fit(X_train, y_train)
        return model

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            self.bar_index += 1
            if self.bar_index > 5:
                lags = self.bars.get_latest_bars_values(
                    self.symbol_list[0], "returns", N=3
                )
                pred_series = pd.Series(
                    {
                        'Lag1': lags[1]*100.0, 
                        'Lag2': lags[2]*100.0
                    }
                )
                pred = self.model.predict([pred_series])[0]
                if pred > 0 and not self.long_market:
                    self.long_market = True
                    signal = SignalEvent(1, self.symbol_list[0], self.datetime_now, 'LONG', 1.0)
                    self.events.put(signal)

                if pred < 0 and self.long_market:
                    self.long_market = False
                    signal = SignalEvent(1, self.symbol_list[0], self.datetime_now, 'EXIT', 1.0)
                    self.events.put(signal)


if __name__ == "__main__":
    csv_dir = '/Users/polad/AlgoTrades/trading_engine'
    symbol_list = ['SPY']
    events = queue.Queue()
    bars = HistoricCSVDataHandler(events, csv_dir, symbol_list)
    initial_capital = 100000.0
    heartbeat = 0.0
    start_date = datetime.datetime(2006, 1, 3)

    backtest = Backtest(
        csv_dir, symbol_list, initial_capital, heartbeat, 
        start_date, HistoricCSVDataHandler, SimulatedExecutionHandler, 
        Portfolio, SPYDailyForecastStrategy
    )
    backtest.simulate_trading()
