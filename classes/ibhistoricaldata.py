__author__ = 'ssg'

import misc.ibdata_types as datatype
import time


def __request_historical_data(self, ib_conn):
    self.lock.acquire()
    try:
        for index, (key, stock_data) in enumerate(self.stocks_data.iteritems()):
            stock_data.is_storing_data = True
            ib_conn.reqHistoricalData(
                index,
                stock_data.contract,
                time.strftime(datatype.DATE_TIME_FORMAT),
                datatype.DURATION_1_HR,
                datatype.BAR_SIZE_5_SEC,
                datatype.WHAT_TO_SHOW_TRADES,
                datatype.RTH_ALL,
                datatype.DATEFORMAT_STRING)

        time.sleep(1)
    finally:
        self.lock.release()