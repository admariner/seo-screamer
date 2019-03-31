import csv
import os
from pathlib import Path

class ParceCSV:
    def __init__(self, file=None):
        self.crawl_data = {}
        self.ready_data = {}

        if file is None:
            return None

        self.file = file

        self.headers = []
        self.ready_data = []

        my_file = Path(self.file)
        if not my_file.is_file():
            return None

        self.get_csv()

    def get_csv(self):
        import pandas as pd
        df = pd.read_csv(self.file, skiprows=1)
        col_headers = list(df.columns)

        self.headers = col_headers
        self.ready_data = df.to_dict(orient='records')

if __name__ == '__main__':
    #if you want to see the dict in a viewable style, go to :
    #https://jsoneditoronline.org/?id=4c5e36491ec04ff697710bb13132c5e3

    csv_file = "../data/oesterbaron.nl/protocol_http.csv"
    c = ParceCSV(csv_file)
    print(c.ready_data)

# protocol_http.csv
# h1_missing.csv
# h1_multiple.csv
# h1_over_70_characters.csv
# h1_duplicate.csv