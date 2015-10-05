__author__ = 'ssg'
from time import sleep
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from ib.opt import Connection

def my_account_handler(msg):
    print(msg)


def my_tick_handler(msg):
    print(msg)


if __name__ == '__main__':
    # con = ibConnection()
    client_id = 1
    port = 7496
    con = Connection.create(port=port, clientId=client_id)

    con.register(my_account_handler, 'UpdateAccountValue')
    con.register(my_tick_handler, message.tickSize, message.tickPrice)
    con.connect()

    def inner():

        con.reqAccountUpdates(1, '')
        qqqq = Contract()
        qqqq.m_symbol = 'QQQ'
        qqqq.m_secType = 'STK'
        qqqq.m_exchange = 'SMART'
        con.reqMktData(1, qqqq, '', False)

    inner()
    sleep(5)
    print('disconnected', con.disconnect())
    sleep(3)
    print('reconnected', con.reconnect())
    inner()
    sleep(3)

    print('again disconnected', con.disconnect())
