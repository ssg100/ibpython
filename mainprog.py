#
# Main program using IBFramework
#
# Features:
# - Reading account value every interval
#
# - Stock data is saved in StockData object class for each stock ticker
#   StockData has the data structure, such as position, symbol, pnl, etc
#   self.symbols = a list contains the symbol list used in the program lifetime
#   self.symbols --> converted to IB Contract Class (java api ref) --> stored in StockData.contract
#
# -


__author__ = 'ssg'

from time import sleep

import misc.ibdata_types as datatype
from classes.ibaccount import IBAccount
from classes.ibevents import IBEvents
from ibframework import IBFramework
import time
import sys
from PyQt4.QtGui import *


ACCOUNT_CODES = ['U129661', 'U1465027']


def __event_handler(msg):
    if msg.typeName == datatype.MSG_TYPE_HISTORICAL_DATA:
        __on_historical_data(msg)

    elif msg.typeName == datatype.MSG_TYPE_UPDATE_PORTFOLIO:
        __on_portfolio_update(msg)

    elif msg.typeName == datatype.MSG_TYPE_MANAGED_ACCOUNTS:
        account_code = msg.accountsList

    elif msg.typeName == datatype.MSG_TYPE_NEXT_ORDER_ID:
        order_id = msg.orderId

    elif msg.typeName == datatype.MSG_TYPE_UPDATE_ACCOUNT_VALUE:
        __on_account_value(msg)

    elif msg.typeName == datatype.MSG_TYPE_ACCOUNT_SUMMARY:
        print msg
        __on_account_summary(msg)
    elif msg.typeName == datatype.MSG_TYPE_POSITION:
        #print msg.typeName
        print msg
        print msg.contract.m_symbol
    elif msg.typeName == datatype.MSG_TYPE_POSITION_END:
        print "PositionEnd()"
    else:
        print msg


def __error_handler(msg):
    if msg.typeName == "error" and msg.id != -1:
        print "Server Error:", msg


def __tick_event_handler(msg):
    pass
    """
    ticker_id = msg.tickerId
    field_type = msg.field

    # Store information from last traded price
    if field_type == datatype.FIELD_LAST_PRICE:
        last_price = msg.price
        self.__add_market_data(ticker_id, dt.datetime.now(), last_price)
        self.__trim_data_series()
    """


def __on_account_summary(msg):
    if msg.tag == "NetLiquidation":
        print "Net Liquidation = " + msg.value
        result = QMessageBox.question(w, 'Message', "Net liquidation exceeds", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    print msg


"""
        key  value  currency  accountName
"""

def __on_account_value(msg):
    if msg.key == datatype.MSG_KEY_NET_LIQUIDATION:
        print msg

    print msg.accountName


def __on_historical_data(msg):
    print msg

    ticker_index = msg.reqId

    if msg.WAP == -1:
        print "Done"
        #self.__on_historical_data_completed(ticker_index)
    else:
        print " "
        #self.__add_historical_data(ticker_index, msg)

    print msg


def __on_historical_data_completed(ticker_index):
    pass


def __on_portfolio_update(msg):
    print msg
    print msg.contract.m_symbol
    print msg.contract.m_expiry
    print msg.contract.m_strike
    print msg.contract.m_tradingClass
    print msg.contract.m_right
    """
    for key, stock_data in self.stocks_data.iteritems():
        if stock_data.contract.m_symbol == msg.contract.m_symbol:
            stock_data.update_position(msg.position,
                                   msg.marketPrice,
                                   msg.marketValue,
                                   msg.averageCost,
                                   msg.unrealizedPNL,
                                   msg.realizedPNL,
                                   msg.accountName)
    return
    """


if __name__ == "__main__":


    # init framework that contains symbols, position, etc
    ib_framework = IBFramework()

    acc = IBAccount(3)  # client id = 3
    acc.connect_to_tws()
    sleep(1)

    # Register events using IB Events
    events = IBEvents(acc.tws_conn)
    # Types of events:                 other events,    error handlers,   market data (ticks)
    events.register_callback_functions(__event_handler, __error_handler, __tick_event_handler)

    acc.tws_conn.reqPositions()

    #acc.tws_conn.reqAccountUpdates(1, ACCOUNT_CODES[1])
    acc.tws_conn.reqAccountSummary(2, 'All', 'NetLiquidation,BuyingPower,TotalCashValue')

    sleep(3)
    #acc.tws_conn.reqAccountUpdates(0, ACCOUNT_CODES[1])

    # Test Historical data
    """
    ib_framework.init_stocks_data(["SPY", "QQQ"])
    ib_framework.request_historical_data(acc.tws_conn,
                                         #time.strftime(datatype.DATE_TIME_FORMAT), # end time is now
                                         '20151118 13:00:00',
                                         datatype.DURATION_1_HR,
                                         datatype.BAR_SIZE_5_MIN,
                                         datatype.WHAT_TO_SHOW_TRADES,
                                         datatype.RTH_ONLY_TRADING_HRS)
    """
    print('disconnected', acc.disconnect_from_tws())


