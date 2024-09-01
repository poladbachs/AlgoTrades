from __future__ import print_function

import datetime 
import time

from ib_insync import *

from event import FillEvent, OrderEvent 
from execution import ExecutionHandler

class IBExecutionHandler(ExecutionHandler):
    """
    Handles order execution via the Interactive Brokers
    API, for use against accounts when trading live
    directly.
    """
    def __init__(self, events, order_routing="SMART", currency="USD"):
        """
        Initialises the IBExecutionHandler instance.
        """
        self.events = events
        self.order_routing = order_routing
        self.currency = currency
        self.fill_dict = {}
        self.ib = IB()  # Initialize IB instance
        self.order_id = 1  # Starting order ID
        self.connect()  # Connect to IB
        self.register_handlers()

    def connect(self):
        """
        Connect to the Trader Workstation (TWS) or IB Gateway.
        """
        self.ib.connect('127.0.0.1', 7496, clientId=1)
        
    def register_handlers(self):
        """
        Register event handlers.
        """
        self.ib.errorEvent += self._error_handler
        self.ib.orderStatusEvent += self._reply_handler

    def _error_handler(self, err):
        """
        Handles the capturing of error messages
        """
        print(f"Server Error: {err}")

    def _reply_handler(self, order, status, filled, remaining, avgFillPrice, permId, parentId, lastLiquidity):
        """
        Handles server replies for order status
        """
        if status == "Filled":
            if order.orderId not in self.fill_dict:
                self.create_fill_dict_entry(order)
            self.create_fill(order)

    def create_contract(self, symbol, sec_type, exch, prim_exch, curr):
        """
        Create a Contract object defining what will
        be purchased, at which exchange and in which currency.
        """
        contract = Stock(symbol, exch, curr)
        contract.primaryExchange = prim_exch
        return contract

    def create_order(self, order_type, quantity, action):
        """
        Create an Order object (Market/Limit) to go long/short.
        """
        order = MarketOrder(action, quantity) if order_type == 'MKT' else LimitOrder(action, quantity, 0)
        return order

    def create_fill_dict_entry(self, order):
        """
        Creates an entry in the Fill Dictionary that lists
        orderIds and provides security information.
        """
        self.fill_dict[order.orderId] = {
            "symbol": order.contract.symbol,
            "exchange": order.contract.exchange,
            "direction": order.action,
            "filled": False
        }

    def create_fill(self, order):
        """
        Handles the creation of the FillEvent that will be
        placed onto the events queue subsequent to an order
        being filled.
        """
        fd = self.fill_dict[order.orderId]
        symbol = fd["symbol"]
        exchange = fd["exchange"]
        filled = order.filled
        direction = fd["direction"]
        fill_cost = order.avgFillPrice

        # Create a fill event object
        fill = FillEvent(
            datetime.datetime.utcnow(), symbol,
            exchange, filled, direction, fill_cost
        )

        # Ensure that multiple messages don't create additional fills.
        self.fill_dict[order.orderId]["filled"] = True
        # Place the fill event onto the event queue
        self.events.put(fill)

    def execute_order(self, event):
        """
        Creates the necessary InteractiveBrokers order object
        and submits it to IB via their API.
        """
        if event.type == 'ORDER':
            asset = event.symbol
            asset_type = "STK"
            order_type = event.order_type
            quantity = event.quantity
            direction = event.direction

            # Create the Interactive Brokers contract via the 
            # passed Order event
            ib_contract = self.create_contract(
                asset, asset_type, self.order_routing,
                self.order_routing, self.currency
            )

            # Create the Interactive Brokers order via the 
            # passed Order event
            ib_order = self.create_order(
                order_type, quantity, direction
            )

            # Use the connection to send the order to IB
            self.ib.placeOrder(
                self.order_id, ib_contract, ib_order
            )

            # Increment the order ID for this session
            self.order_id += 1

    def disconnect(self):
        """
        Disconnect from the IB API.
        """
        self.ib.disconnect()
