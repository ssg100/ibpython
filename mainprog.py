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

ACCOUNT_CODES = ['U129661', 'U146027']


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

    print msg


def __on_account_value(msg):
    if msg.key == datatype.MSG_KEY_NET_LIQUIDATION:
        print msg


def __on_historical_data(msg):
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

    acc = IBAccount(3)  # client id = 1
    acc.connect_to_tws()
    sleep(1)

    events = IBEvents(acc.tws_conn)
    events.register_callback_functions(__event_handler, __error_handler, __tick_event_handler)

    acc.tws_conn.reqAccountUpdates(1, ACCOUNT_CODES[0])
    # acc.tws_conn.reqAccountSummary(2, 'All', 'NetLiquidation,BuyingPower,TotalCashValue')

    sleep(5)
    acc.tws_conn.reqAccountUpdates(0, ACCOUNT_CODES[0])
    print('disconnected', acc.disconnect_from_tws())
