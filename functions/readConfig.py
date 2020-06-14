#pip install pyyaml
import os
import sys
import logging

import yaml


class readConfig:

    config = ""

    def __init__(self, file=None):
        try:
            if file is None:
                file = "./config/config.yml"

            with open(file) as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
            f.close
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning("We could not open or parse the config file! " + " | " + str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            sys.exit()
