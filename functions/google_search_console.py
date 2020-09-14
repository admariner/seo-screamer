# https://github.com/joshcarty/google-searchconsole
import os
import sys
import logging
import datetime
import searchconsole
import json


class GoogleSearchConsole:
    def __init__(self, webproperty=None, domain=None, start_date="today", days=-30, dimension=['device', 'query', 'country',
                                                                                               'page'], config_path=None):
        try:
            if webproperty == domain == config_path is None:
                raise Exception(
                    "URL or Domain or Config_path variable is None!")

            self.start_date = start_date
            self.days_back = days
            self.domain = domain
            self.dimensions = dimension
            self.webproperty = webproperty
            self.dimension_data = {}

            self.data_file = ""

            self.credentials = os.path.join(config_path, 'credentials.json')
            self.client_secrets = os.path.join(
                config_path, 'client_service_secret.json')

            self.connect_google()  # Connection to Google search

            if isinstance(dimension, (list, tuple)):
                for d in dimension:
                    self.get_dimension_data(d)
            else:
                self.get_dimension_data(dimension)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def connect_google(self):
        if os.path.exists(self.credentials):
            account = searchconsole.authenticate(client_config=self.client_secrets,
                                                 credentials=self.credentials)
        else:
            account = searchconsole.authenticate(client_config=self.client_secrets,
                                                 serialize=self.credentials)

        self.webproperty = account[self.webproperty]
        if self.webproperty is None:
            raise Exception("webproperty is None!")

    def get_dimension_data(self, dimension):
        try:

            self.data_file = self.file_name(dimension)

            if os.path.isfile(self.data_file):
                logging.info(
                    'Found {} google search console json file'.format(dimension))

                file = os.path.basename(self.data_file)
                file_date = file.split("_")

                if file_date[0] == str(self.start_date):
                    logging.info(
                        'Using {} data from google search console json file'.format(dimension))
                    self.dimension_data[dimension] = self.open_file_with_contents(
                        self.data_file)
                    return
            logging.info('No google search console file found')

            if dimension in self.dimensions:
                self.dimension_data[dimension] = self.get_data(dimension)

                if self.dimension_data[dimension] is not None:
                    logging.info(
                        'Create file with {} google search console json file'.format(dimension))
                    self.save_file_with_contents(
                        self.data_file, self.dimension_data[dimension])
            else:
                raise Exception("We found a dimension that's not in our list!")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def get_data(self, dimension):
        try:
            report = self.webproperty.query.range(
                self.start_date, days=self.days_back).dimension(dimension).get()
            return report.raw

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def file_name(self, dimension=None):
        try:
            if dimension is None:
                raise Exception("Dimension is None!")

            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_folder = os.path.join(
                dir_path, "..", "data", self.domain, 'google_search_console')
            data_file_name = "{}_{}.json".format(self.start_date, dimension)
            return os.path.join(data_folder, data_file_name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def open_file_with_contents(self, file=None):
        try:
            if file is not None:
                self.data_file = file

            with open(self.data_file, 'r') as json_file:
                return json.load(json_file)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def save_file_with_contents(self, file=None, content=None):
        try:
            if file == content is not None:
                self.data_file = file

            with open(self.data_file, 'w+') as output:
                json.dump(content, output)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) +
                            " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None


if __name__ == '__main__':
    start_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(start_path, "../config")
    now = datetime.datetime.now()
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    today_lastMonth = lastMonth.strftime("%Y-%m-%d")

    dimensions = ['device', 'query', 'country', 'page']
    domain = 'oesterbaron.nl'
    g = GoogleSearchConsole('https://oesterbaron.nl/',
                            domain, today, -30, dimensions, config_path)
    g = GoogleSearchConsole('https://oesterbaron.nl/',
                            domain, today_lastMonth, -30, dimensions, config_path)
    logging.info(g.dimension_data)

# https://www.purepython.org/
# https://zldsteigerbouw.nl/
# https://www.legendsince75.nl/
# https://theo.vandersluijs.nl/
# https://www.itheo.nl/
# https://www.vandersluijs.nl/
# https://taallesbureau.nl/
# https://112signal.nl/
# https://flashpatterns.nl/
# https://oesterbaron.nl/

# https://www.dejastone.nl/
# https://www.urnenhemel.nl/
# sc-domain:bouwbedrijfjari.nl
# sc-domain:grafkunsten.nl

# sc-domain:theo-van-der-sluijs.nl
# sc-domain:purepython.org

    #
    # clicks = 0
    # for r in report.rows:
    #     print(r.page, r.clicks, r.impressions)
    #     clicks += r.clicks
    # print(clicks)

# deze gegevens komen uit de google zoekmachine

    # * `range` to specify a date range for your query. Queries are still limited
    #   by the 3 month limit and no Exception is raised if you exceed this limit.
    # * `dimension` to specify the dimensions you would like report on (country,
    #   device, page, query, searchAppearance)
    # * `filter` to specify which rows to filter by.
    # * `limit` to specify a subset of results.

# Wat is een klik
# Voor de meeste resultaattypen wordt elke klik waarmee de gebruiker naar een pagina buiten Google Zoeken wordt gestuurd, geteld als klik en wordt een klik op een link waarmee de gebruiker binnen de zoekresultaten blijft, niet geteld als klik.
# Klikken op een zoekresultaat naar een externe pagina en dan terugkeren en nogmaals op dezelfde link klikken, wordt geteld als maar één klik. Klikken op een andere link telt als een klik voor elke link waarop wordt geklikt.

# Impression / Wat is een vertoning?
# Een link-URL registreert een vertoning wanneer deze wordt weergegeven in een zoekresultaat voor een gebruiker. Of de link daadwerkelijk in beeld moet worden gescrolld of anderszins zichtbaar moet zijn, is afhankelijk van het type zoekelement waarin de link is opgenomen, zoals hieronder staat beschreven.
