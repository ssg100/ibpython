# ***********************************************************************
# Interactive Brokers Python Framework
#
# Complete framework to interact with IB for:
#       Order management
#       Account management
#       Market data
#
# Leveraging Python Object-oriented programming to implement the framework
# Use the classes as components for designing trading systems or others
#
# @author:  Sani Gosali
# @Copyright 2015
# This is not an open source
# ************************************************************************
__author__ = 'ssgosali'

from classes.ibevents import IBEvents

class IBFramework(object):
    def __init__(self, client_id=10, port=7496, account_code=None):
        # no need acc code?????
        #if account_code is None:
        #    raise ValueError("Account number is needed. Please pass acc number.")
        #    return
        self.client_id = client_id
        # self.order_id = 1
        # self.qty = qty
        #self.symbol_id, self.symbol = 0, symbol
        #self.resample_interval = resample_interval
        #self.averaging_period = averaging_period
        self.port = port
        self.tws_conn = None
        #self.bid_price, self.ask_price = 0, 0
        #self.last_prices = pd.DataFrame(columns=[self.symbol_id])
        #self.average_price = 0
        #self.is_position_opened = False
        self.account_code = None
        self.unrealized_pnl, self.realized_pnl = 0, 0
        self.position = 0


