__author__ = 'ssg'

from ib.opt import Connection


class IBAccount(object):
    #tws_conn = None

    def __init__(self, client_id, port=7496):
        self.tws_conn = Connection.create(clientId=client_id, port=port)

    def connect_to_tws(self):
        self.tws_conn.connect()

    def disconnect_from_tws(self):
         if self.tws_conn is not None:
            self.tws_conn.disconnect()

