# https://github.com/joshcarty/google-searchconsole
import os
import datetime
import searchconsole
import json


class GoogleSearchConsole:
    def __init__(self, url=None, domain=None, start_date="today", days=-30, dimension=['device', 'query', 'country',
                                                                                       'page'], config_path=None):
        if url == domain == config_path is None:
            return

        self.start_date = start_date
        self.days_back = days
        self.domain = domain
        self.dimensions = dimension
        self.dimension_data = {}

        self.data_file = ""

        credentials = os.path.join(config_path, 'credentials.json')
        client_secrets = os.path.join(config_path, 'client_secrets.json')
        client_service_secret = os.path.join(config_path, 'client_service_secret.json')

        if os.path.exists(credentials):
            account = searchconsole.authenticate(client_config=client_secrets,
                                                 credentials=credentials)
        else:
            account = searchconsole.authenticate(client_config=client_service_secret,
                                                 serialize=credentials)

        self.webproperty = account[url]
        if self.webproperty is None:
            return False

        if isinstance(dimension, (list, tuple)):
            for d in dimension:
                self.get_dimension_data(d)
        else:
            self.get_dimension_data(dimension)

    def get_dimension_data(self, dimension):
        self.data_file = self.file_name(dimension)

        if os.path.isfile(self.data_file):
            print('Found google search console json file')

            file = os.path.basename(self.data_file)
            file_date = file.split("_")

            if file_date[0] == str(self.start_date):
                print('Using data from google search console json file')
                self.dimension_data[dimension] = self.open_file_with_contents(self.data_file)
                return
        print('No google search console file found')

        if dimension in self.dimensions:
            self.dimension_data[dimension] = self.get_data(dimension)

            if self.dimension_data[dimension] is not None:
                print('Create file with google search console json file')
                self.save_file_with_contents(self.data_file, self.dimension_data[dimension])

    def get_data(self, dimension):
        report = self.webproperty.query.range(self.start_date, days=self.days_back).dimension(dimension).get()
        return report.raw

    def file_name(self, dimension=None):
        if dimension is None:
            return False

        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_folder = os.path.join(dir_path, "../data", self.domain, 'google_search_console')
        data_file_name = "{}_{}.json".format(self.start_date, dimension)
        return os.path.join(data_folder, data_file_name)

    def open_file_with_contents(self, file=None):
        if file is not None:
            self.data_file = file

        with open(self.data_file, 'r') as json_file:
            return json.load(json_file)

    def save_file_with_contents(self, file=None, content=None):
        if file == content is not None:
            self.data_file = file

        with open(self.data_file, 'w+') as output:
            json.dump(content, output)


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
    g = GoogleSearchConsole('https://oesterbaron.nl/', domain, today, -30, dimensions, config_path)
    g = GoogleSearchConsole('https://oesterbaron.nl/', domain, today_lastMonth, -30, dimensions, config_path)
    print(g.dimension_data)

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
