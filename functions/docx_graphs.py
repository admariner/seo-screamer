import os
import sys
import logging
import json
from datetime import date, datetime
from shutil import copyfile

import matplotlib.pyplot as plt
from .gauge import Gauge
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

class DocxGraphs:
    def __init__(self, folder=None):
        try:
            if folder is None:
                raise Exception("Folder is None")

            self.folder = folder
            self.pie_colors = ['#5DA5DA','#FAA43A','#60BD68','#F17CB0','#B2912F','#B276B2','#DECF3F','#F15854', '#4D4D4D']
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def search_console_pie(self, data=None, title="", file_name="pie-chart.png"):
        try:
            if data is None or data == "":
                raise Exception("Data is None")

            image_name = os.path.join(self.folder, file_name)
            labels = []
            sizes = []
            explode = []

            #no more then 9 items!
            # print(data)

            for k, v in data.items():
                labels.append(k)
                sizes.append(v)
                explode.append(0)

            i = len(data)
            if i > 9:  #just checking that there are no more then 9
                return False

            colors = self.pie_colors[:i]

            # labels = 'bodyFat', 'muscleMass', 'boneMass', 'bodyWater'
            # colors = ['#f9ca2f', '#e2310d', '#f4f6f7', '#2285f7']
            # sizes = [self.weight_data['lastval_bodyFat'],
            #          self.weight_data['lastval_muscleMass'],
            #          self.weight_data['lastval_boneMass'],
            #          self.weight_data['lastval_bodyWater']]
            # explode = (0.1, 0, 0, 0)

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    colors=colors, shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title(title)

            plt.savefig(image_name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False
