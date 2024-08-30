from __future__ import print_function

import datetime 
import time

from ib.ext.Contract import Contract 
from ib.ext.Order import Order
from ib.opt import ibConnection, message

from event import FillEvent, OrderEvent 
from execution import ExecutionHandler

class IBExecutionHandler(ExecutionHandler): 
    """
    Handles order execution via the Interactive Brokers
    API, for use against accounts when trading live
    directly.
    """
    def __init__(
        self, events, order_routing="SMART", currency="USD" 
    ):
        """
        Initialises the IBExecutionHandler instance. 
        """
        self.events = events
        self.order_routing = order_routing
        self.currency = currency
        self.fill_dict = {}
        self.tws_conn = self.create_tws_connection() 
        self.order_id = self.create_initial_order_id()
        self.register_handlers()

    def _error_handler(self, msg): 
        """
        Handles the capturing of error messages 
        """
        # Currently no error handling. 
        print("Server Error: %s" % msg)

    def _reply_handler(self, msg): 
        """
        Handles of server replies
        """
        # Handle open order orderId processing
        if msg.typeName == "openOrder" and \
            msg.orderId == self.order_id and \
            not self.fill_dict.has_key(msg.orderId): 
            self.create_fill_dict_entry(msg)
        # Handle Fills
        if msg.typeName == "orderStatus" and \
            msg.status == "Filled" and \
            self.fill_dict[msg.orderId]["filled"] == False: 
            self.create_fill(msg)
        print("Server Response: %s, %s\n" % (msg.typeName, msg))