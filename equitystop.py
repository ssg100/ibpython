#
# Equity Stop
#
# If a certain equity stop threshold is violated, account will be liquidated
#   except the passed symbols during init (in case, certain symbols should not be liquidated)
#

from time import sleep
import misc.ibdata_types as datatype
from classes.ibaccount import IBAccount
from classes.ibevents import IBEvents
from ibframework import IBFramework
import ctypes
from time import gmtime, strftime

# MACROS
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

# GLOBAL VARIABLES
ACCOUNT_CODES = ['U129661', 'U1465027']

def __event_handler(msg):
    if msg.typeName == datatype.MSG_TYPE_UPDATE_PORTFOLIO:
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


def __on_account_summary(msg):
    global equity_stop
    if msg.tag == "NetLiquidation":
        net_liquidation = msg.value
        print "Net Liquidation $ = " + net_liquidation
        print "Account = " + msg.account

        equity_stop.process_net_liquidation_data(net_liquidation, msg.account)

    print msg

"""
        key  value  currency  accountName
"""


def __on_account_value(msg):
    if msg.key == datatype.MSG_KEY_NET_LIQUIDATION:
        print msg

    print msg.accountName


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


class EquityStopLoss(object):
    def __init__(self, equity_stop_loss, acc_code):
        print "EquityStopLoss init(). stop_loss = " + str(equity_stop_loss)
        self.equity_stop_loss = equity_stop_loss        # threshold constant
        self.acc_code = acc_code
        self.is_stopped_out = False

    def get_is_stopped_out(self):
        return self.is_stopped_out

    def set_is_stopped_out(self, value):
        self.is_stopped_out = value
        
    def process_net_liquidation_data(self, net_liquidation, acc_code):
        print "Net Liquidation $ = " + str(net_liquidation)
        print "Equity stop loss $ = " + str(self.equity_stop_loss)

        if (float(net_liquidation) < float(self.equity_stop_loss)) and (self.acc_code == acc_code):
            print "***  STOP loss is hit ***"
            msg = "Equity Stop is EXCEEDED below " + str(self.equity_stop_loss) + "\nAUTO CLOSE all positions?"
            self.is_stopped_out = True

            result = ctypes.windll.user32.MessageBoxA(0, msg, "Warning!!", MB_YESNO | ICON_EXLAIM)
            print result
            
            # check result and close positions, except the ignore symbol list

        else:
            self.is_stopped_out = False
        
        

if __name__ == "__main__":
    # init framework that contains symbols, position, etc
    ib_framework = IBFramework()

    acc = IBAccount(3)  # client id = 3
    acc.connect_to_tws()
    sleep(1)

    # Instantiate equity stop loss class with (stop loss $, account code)
    equity_stop = EquityStopLoss(25000.00, ACCOUNT_CODES[1])

    # Register events using IB Events
    events = IBEvents(acc.tws_conn)
    # Types of events:                 other events,    error handlers,   market data (ticks)
    events.register_callback_functions(__event_handler, __error_handler, __tick_event_handler)

    while True:
        try:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            if not equity_stop.is_stopped_out:
                print "Request account summary   " + time_now
                acc.tws_conn.reqAccountSummary(2, 'All', 'NetLiquidation')
            else:
                acc.tws_conn.cancelAccountSummary(2)
                print "Portfolio has been STOPPED OUT - Please take action, if have not done so ! " + time_now
            sleep(10)
                
        except Exception,e:
            print e
            print('disconnect from IB', acc.disconnect_from_tws())
