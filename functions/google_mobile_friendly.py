import sys
import logging

import requests


class GoogleMobileFriendly:
    def __init__(self, api=None, url=None):
        try:
            if api is None or url is None:
                raise Exception("API or URL is None")

            self.api = api
            self.url = url
            self.data = {}

            self.get_data()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def get_data(self):
        self.get_google_data()

    def get_google_data(self):
        try:
            google_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key={}".format(self.api)
            data = {"url": self.url}
            r = requests.post(google_url, data)
            self.data = r.text
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

if __name__ == '__main__':
    url = "https://www.vandersluijs.nl"
    api = ""
    g = GoogleMobileFriendly(api, url)
    print(g.data)
