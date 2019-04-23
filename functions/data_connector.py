import os
import sqlite3
from sqlite3 import Error


class DataConnector:
    def __init__(self, datafile=None):
        if datafile is None:
            return False

        self.datafile = datafile

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.datafile)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            conn.close()


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(dir_path, "../data", "oesterbaron.nl", "crawl", "crawl.db")
    dc = DataConnector(data_file)
    dc.create_connection()
