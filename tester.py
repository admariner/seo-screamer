import os
import sys
import logging
from datetime import datetime

# import locale
# locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

now = datetime.now()
today = "{}-{}-{}".format(now.year, now.month, now.day)
sf = os.path.dirname(os.path.realpath(__file__))
folder = os.path.join(sf, 'logging')
log_file = os.path.join(folder, "{}.log".format(today))

print(os.environ['HOME'])

if os.environ['HOME'] == '/Users/theovandersluijs':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
else:
    os.makedirs(folder, exist_ok=True)
    logging.basicConfig(filename=log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.CRITICAL)

class test:
    def __init__(self):
        try:
            print('init')
            self.compare_me(1)
            self.get_file()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def compare_me(self, nr=1):
        if 1 == nr:
            print('correct')
        else:
            raise Exception("We have found an error")

    def get_file(self):
        try:
            file = "theo.txt"
            with open(file, newline='') as f:
                line = f.readline()
        except Exception as e:
            raise Exception("File problem {}".format(e))


if __name__ == '__main__':
    t = test()
