import csv
import sys
import os
import logging

from pathlib import Path
from collections import OrderedDict, defaultdict
import pandas as pd


class CrawlOverview:
    def __init__(self, crawl_file: str = None, crawl_yml: dict = None):
        try:
            self.crawl_data = {}
            self.ready_data = {}

            if crawl_file is None:
                raise Exception("crawl_file is None")

            if crawl_yml is None:
                raise Exception("crawl_yml is None")

            self.file = crawl_file
            self.crawl_yml = crawl_yml

            if not os.path.isfile(self.file):
                raise Exception(
                    "file is not a file or is None {}".format(self.file))

            self.data = self.get_csv()

            # self.get_csv()
            self.get_data()

            self.table_headers = []
            for k, v in self.crawl_yml.items():
                try:
                    # if v['overview'] >= 1:
                    if 0 < v['overview'] < 3:
                        self.table_headers.append(k)
                        if k == "Meta Description":
                            self.table_headers.append('Meta Keywords')
                except KeyError as e:
                    print(k, e)

            self.readydata = {}
            self.readydata['Info'] = []
            try:
                self.readydata['Info'].append(
                    self.happy_data("Datum laatste crawl", self.crawl_data['Info']['Date'][0]))
                self.readydata['Info'].append(self.happy_data(
                    "Found pages & content", round(self.crawl_data['Summary']['Total URLs Encountered'][0])))
                self.readydata['Info'].append(self.happy_data(
                    "Crawled pages & content", self.crawl_data['Summary']['Total URLs Crawled'][0]))
                self.readydata['Info'].append(self.happy_data(
                    "Total internal urls", self.crawl_data['Summary']['Total Internal URLs'][0]))
                self.readydata['Info'].append(self.happy_data(
                    "Total external urls", self.crawl_data['Summary']['Total External URLs'][0]))
                self.readydata['Info'].append(self.happy_data(
                    "Total blocked for robots", self.crawl_data['Summary']['Total External blocked by robots.txt'][0]))
            except KeyError as e:
                raise Exception("KeyError: {}".format(e))

            self.readydata['Meta Keywords'] = []
            try:
                meta_aanwezig = (int(self.crawl_data['Internal']['HTML'][0])-int(
                    self.crawl_data['Meta Keywords']['Missing'][0]))
                self.readydata['Meta Keywords'].append(
                    self.happy_data('Present', meta_aanwezig, [0, 1], 1))
            except KeyError as e:
                raise Exception("KeyError: {}".format(e))

            for th in self.table_headers:
                if th == "Meta Keywords":
                    continue

                if 0 < self.crawl_yml[th]['overview'] < 3:
                    # hier gaan we de meest verwerken
                    self.readydata[th] = []
                    for k, v in self.crawl_data[th].items():
                        try:
                            if self.crawl_yml[th]['Data'][k]:
                                self.readydata[th].append(self.happy_data(
                                    k, v[0], self.crawl_yml[th]['Data'][k]['grades'], self.crawl_yml[th]['Data'][k]['difficult']))

                        except KeyError as e:
                            # print("KeyError: {}".format(e))
                            pass

            self.table_headers.insert(0, 'Info')

            '''
            Clicks Above 0 – This simply means the URL in question has 1 or more clicks.
            No GSC Data – This means that the API didn’t return any data for the URLs in the crawl. So the URLs either didn’t receive any impressions, or perhaps the URLs in the crawl are just different to those in GSC for some reason.
            Non-Indexable with GSC Data – This means the URL is non-indexable, but still has data from GSC.
            Orphan URLs – This means the URL was only discovered via GSC, and was not found via an internal link during the crawl.
            '''

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            sys.exit()

    def get_csv(self):
        try:
            datafile = open(self.file, 'r')
            datareader = csv.reader(datafile, delimiter=",")
            data = []
            for row in datareader:
                data.append(row)
            datafile.close()
            return data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def get_column(self, thelist, thecolumn):
        try:
            newlist = []
            for row in thelist:
                if len(row) >= thecolumn + 1:
                    newlist.append(row[thecolumn])
                else:
                    newlist.append("")
            return newlist
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def get_data(self):
        try:

            for k, v in self.crawl_yml.items():

                df = pd.read_csv(self.file, sep=',', skiprows=v['sr'],
                                 nrows=v['nr'], header=v['h'])
                df = df.dropna()
                if v['h'] == 0:
                    print(k)
                    self.crawl_data[k] = df.to_dict('list')
                else:
                    self.crawl_data[k] = df.set_index(0).T.to_dict('list')

        except Exception as e:
            print(e)

    @ staticmethod
    def happy_data(name=None, grade=None, grades=None, difficult=None):
        if name is not grade is None:
            return

        if grades is None:
            grader = ""
        else:
            grade = int(grade)
            count = len(grades)

            if count == 1:
                if grade < int(grades[0]):
                    grader = 3
                else:
                    grader = 0
            elif count > 2:
                if grade <= int(grades[0]):
                    grader = 0
                elif int(grades[0]) < grade <= int(grades[1]):
                    grader = 1
                elif int(grades[1]) < grade <= int(grades[2]):
                    grader = 2
                elif grade > int(grades[2]):
                    grader = 3
            elif count == 2:
                if grade <= int(grades[0]):
                    grader = 0
                else:
                    grader = 3

        how_difficult = ""
        try:
            if int(grader) > 0 and difficult is not None:
                how_difficult = " "*difficult
        except ValueError:
            pass

        return name, str(grade), grader, how_difficult


if __name__ == '__main__':
    # if you want to see the dict in a viewable style, go to :
    # https://jsoneditoronline.org/?id=4c5e36491ec04ff697710bb13132c5e3

    csv_file = "../data/oesterbaron.nl/crawl/crawl_overview.csv"
    c = CrawlOverview(csv_file)
    logging.info(c.readydata)
