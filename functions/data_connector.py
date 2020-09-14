import os
import sys
import logging
import sqlite3
from sqlite3 import Error


class DataConnector:
    def __init__(self, datafile=None):
        try:
            if datafile is None:
                raise Exception("datafile is None")

            self.datafile = datafile
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.datafile)
            print(sqlite3.version)
        except Error as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False
        finally:
            conn.close()


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(dir_path, "..", "data",
                             "oesterbaron.nl", "site_data.db")
    dc = DataConnector(data_file)
    dc.create_connection()
