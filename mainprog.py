#
# Main program using IBFramework
#
# Features:
# - Reading account value every interval

__author__ = 'ssg'

from time import sleep
from ibframework import IBFramework
import misc.ibdata_types as datatype
from classes.ibevents import IBEvents
from classes.ibaccount import IBAccount

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

def __on_account_value(msg):
    if msg.key == datatype.MSG_KEY_NET_LIQUIDATION:
        print msg

def __on_historical_data(msg):
    print msg

    """
    print msg

    ticker_index = msg.reqId

    if msg.WAP == -1:
        self.__on_historical_data_completed(ticker_index)
    else:
        self.__add_historical_data(ticker_index, msg)
    """

def __on_historical_data_completed(ticker_index):
    pass
    """
    self.lock.acquire()
    try:
        symbol = self.symbols[ticker_index]
        self.stocks_data[symbol].is_storing_data = False
    finally:
        self.lock.release()
    """

def __on_portfolio_update(msg):
    print msg

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

    acc = IBAccount(3)  # client id = 1
    acc.connect_to_tws()

    events = IBEvents(acc.tws_conn)
    events.register_callback_functions(__event_handler, __error_handler, __tick_event_handler)

    acc.tws_conn.reqAccountUpdates(1, 'U129661')
    acc.tws_conn.reqAccountSummary(2, 'All', 'NetLiquidation')

    sleep(5)
    print('disconnected', acc.disconnect_from_tws())
