__author__ = 'ssgosali'

from ib.opt import Connection, message

class IBEvents(object):
        def __init__(self, pass_tws_conn):
            self.tws_conn = pass_tws_conn

        # Class method
        def register_callback_functions(self, event_handler, error_handler, tick_event_handler):
            # Assign server messages handling function.
            self.tws_conn.registerAll(event_handler)

            # Assign error handling function.
            self.tws_conn.register(error_handler, 'Error')

            # Register market data events.
            self.tws_conn.register(tick_event_handler,
                                   message.tickPrice,
                                   message.tickSize)

