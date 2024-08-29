from __future__ import print_function

class Event(object):
    """
    Event is base class providing an interface for all subsequent (inherited) events, 
    that will trigger further events in the
    trading infrastructure. 
    """
    pass

class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with
    corresponding bars.
    """

    def __init__(self):
        """
        Initiliases the MarketEvent.
        """
        self.type = 'MARKET'