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
import pandas as pd
from classes.ibcontract import IBContract
from classes.ibstockdata import StockData
import misc.ibdata_types as datatype
import time
import threading


class IBFramework(object):
    def __init__(self): # , client_id=10, port=7496, account_code=None):
        # no need acc code?????
        #if account_code is None:
        #    raise ValueError("Account number is needed. Please pass acc number.")
        #    return
        # self.client_id = client_id
        # self.order_id = 1
        # self.qty = qty
        #self.symbol_id, self.symbol = 0, symbol
        #self.resample_interval = resample_interval
        #self.averaging_period = averaging_period
        # self.port = port
        # self.tws_conn = None
        #self.bid_price, self.ask_price = 0, 0
        #self.last_prices = pd.DataFrame(columns=[self.symbol_id])
        #self.average_price = 0
        #self.is_position_opened = False
        # self.account_code = None
        self.unrealized_pnl, self.realized_pnl = 0, 0
        self.position = 0

        self.stocks_data = {}   # Dictionary storing StockData objects.
        self.symbols = None     # List of current symbols
        self.prices = None      # Store last prices in a DataFrame
        self.lock = threading.Lock()
        self.ib_contract = IBContract()

    def init_stocks_data(self, symbols):
        self.symbols = symbols
        self.prices = pd.DataFrame(columns=symbols)  # Init price storage

        for stock_symbol in symbols:
            contract = self.ib_contract.create_stock_contract(stock_symbol)
            self.stocks_data[stock_symbol] = StockData(contract)

        print self.prices
        print self.stocks_data
        print self.stocks_data.iteritems()

    # Example call:  time.strftime(datatype.DATE_TIME_FORMAT),
    #                datatype.DURATION_1_HR, datatype.BAR_SIZE_5_SEC, datatype.WHAT_TO_SHOW_TRADES, datatype.RTH_ALL
    #     datatype - import misc.ibdata_types as datatype
    def request_historical_data(self, ib_conn, end_time, duration, bar_size, what_to_show, trading_hours):
        self.lock.acquire()
        try:
            for index, (key, stock_data) in enumerate(
                    self.stocks_data.iteritems()):
                print index, key, stock_data
                stock_data.is_storing_data = True
                ib_conn.reqHistoricalData(
                    index,
                    stock_data.contract,
                    end_time,
                    duration,
                    bar_size,
                    what_to_show,
                    trading_hours,
                    datatype.DATEFORMAT_STRING)
                time.sleep(1)
        finally:
            self.lock.release()