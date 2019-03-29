import sys

#pip install pyyaml
import yaml


class readConfig:

    config = ""

    def __init__(self):
        try:
            with open('./config/config.yml') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
            f.close
        except Exception as e:
            print("We could not open the config file!")
            sys.exit()
