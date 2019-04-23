#pip install pyyaml

import sys
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
            print("We could not open or parse the config file! {}".format(e))
            sys.exit()
