from __future__ import print_function
import datetime
from math import floor 
try:
    import Queue as queue 
except ImportError:
    import queue

import numpy as np 
import pandas as pd

from event import FillEvent, OrderEvent
from performance import create_sharpe_ratio, create_drawdowns