import sys
import os
import logging

from urllib.parse import urlparse


class Domain():
    def __init__(self, domain=None):
        try:
            if domain is None:
                raise Exception("Domain is None")

            self.url = domain
            self.scheme = self.get_uri_scheme()
            self.domain = self.get_uri_domain()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def get_uri_scheme(self):
        parsed_uri = urlparse(self.url)
        return "{uri.scheme}".format(uri=parsed_uri)

    def get_uri_domain(self):
        parsed_uri = urlparse(self.url)
        return "{uri.netloc}".format(uri=parsed_uri)


if __name__ == '__main__':
    url = "https://www.vandersluijs.nl"
    d = Domain(url)

    print(d.scheme)
    print(d.domain)
