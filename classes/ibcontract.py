__author__ = 'ssg'

# ***********************************************************************
# Interactive Brokers Python Framework
#
# Contract utilities class
# Sani G.
# ************************************************************************

from ib.ext.Contract import Contract
from ib.ext.Order import Order
import misc.ibdata_types as datatype


class IBContract(object):
    def __init__(self):
        pass

    def create_stock_contract(self, stock):
        contract_tuple = (stock, 'STK', 'SMART', 'USD', '', 0.0, '')
        stock_contract = self.__make_ib_contract(contract_tuple)
        return stock_contract

    # Create futures contract
    #
    # sample params:  'ES', 'GLOBEX', '201512'
    def create_futures_contract(self, futures,  expiry, exchange='GLOBEX'):
        contract_tuple = (futures, 'FUT', exchange, 'USD', expiry, 0.0, '')
        futures_contract = self.__make_ib_contract(contract_tuple)
        return futures_contract

    # Create options contract
    #
    # sample params:  'QQQ', '20150921', 41.0, 'CALL'
    def create_options_contract(self, options,  expiry, strike_price, option_type='CALL'):
        contract_tuple = (options, 'OPT', 'SMART', 'USD', expiry, strike_price, option_type)
        options_contract = self.__make_ib_contract(contract_tuple)
        return options_contract

    # Returns IB Contract object/data structure
    @staticmethod
    def __make_ib_contract(contract_tuple):
        new_contract = Contract()
        new_contract.m_symbol = contract_tuple[0]
        new_contract.m_secType = contract_tuple[1]
        new_contract.m_exchange = contract_tuple[2]
        new_contract.m_currency = contract_tuple[3]
        new_contract.m_expiry = contract_tuple[4]
        new_contract.m_strike = contract_tuple[5]
        new_contract.m_right = contract_tuple[6]
        return new_contract

    def create_stock_order(self, quantity, is_buy, is_market_order=True):
        order = Order()
        order.m_totalQuantity = quantity
        order.m_orderType = \
            datatype.ORDER_TYPE_MARKET if is_market_order else \
            datatype.ORDER_TYPE_LIMIT
        order.m_action = \
            datatype.ORDER_ACTION_BUY if is_buy else \
            datatype.ORDER_ACTION_SELL
        return order