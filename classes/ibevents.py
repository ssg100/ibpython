__author__ = 'ssgosali'

import misc.ibdata_types as datatype

class IBEvents(object):
        def event_handler(self, msg):
            if msg.typeName == datatype.MSG_TYPE_HISTORICAL_DATA:
                self.__on_historical_data(msg)

            elif msg.typeName == datatype.MSG_TYPE_UPDATE_PORTFOLIO:
                self.__on_portfolio_update(msg)

            elif msg.typeName == datatype.MSG_TYPE_MANAGED_ACCOUNTS:
                self.account_code = msg.accountsList

            elif msg.typeName == datatype.MSG_TYPE_NEXT_ORDER_ID:
                self.order_id = msg.orderId
            elif msg.typeName == datatype.MSG_TYPE_UPDATE_ACCOUNT_VALUE:
            else:
                print msg

        def __on_historical_data(self, msg):
            pass
            """
            print msg

            ticker_index = msg.reqId

            if msg.WAP == -1:
                self.__on_historical_data_completed(ticker_index)
            else:
                self.__add_historical_data(ticker_index, msg)
            """
        def __on_historical_data_completed(self, ticker_index):
            pass
            """
            self.lock.acquire()
            try:
                symbol = self.symbols[ticker_index]
                self.stocks_data[symbol].is_storing_data = False
            finally:
                self.lock.release()
            """
        def __on_portfolio_update(self, msg):
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