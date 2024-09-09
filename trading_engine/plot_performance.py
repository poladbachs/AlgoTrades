import os.path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv(
            "equity.csv", header=0,
            parse_dates=True, index_col=0
    ).sort_index()

    # Plot three charts: Equity curve, 
    # period returns, drawdowns
    fig = plt.figure()
    # Set the outer colour to white
    fig.patch.set_facecolor('white')