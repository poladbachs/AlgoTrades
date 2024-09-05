

from __future__ import print_function
import numpy as np
import pandas as pd

def create_sharpe_ratio(returns, risk_free_rate=0.0, trading_days=252):
    """
    Calculates the annualized Sharpe Ratio for a series of returns.
    """
    mean_return = returns.mean() * trading_days
    return_volatility = returns.std() * np.sqrt(trading_days)
    sharpe_ratio = (mean_return - risk_free_rate) / return_volatility
    return sharpe_ratio

def create_drawdowns(equity_curve):
    """
    Calculates drawdowns and their duration.
    """
    drawdowns = pd.Series(index=equity_curve.index)
    peak = equity_curve.cummax()
    drawdowns = (equity_curve - peak) / peak

    max_drawdown = drawdowns.min()
    drawdown_duration = (drawdowns > 0).astype(int).groupby((drawdowns <= 0).astype(int).cumsum()).cumsum().max()

    return drawdowns, max_drawdown, drawdown_duration