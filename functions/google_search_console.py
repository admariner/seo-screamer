# https://github.com/joshcarty/google-searchconsole
import searchconsole
import os


class GoogleSearchConsole:
    def __init__(self, url=None, start_day='today', days=-30):
        if url is None:
            return

        self.start_day = start_day
        self.days_back = days

        if os.path.exists('../config/credentials.json'):
            account = searchconsole.authenticate(client_config='../config/client_secrets.json',
                                                 credentials='../config/credentials.json')
        else:
            account = searchconsole.authenticate(client_config='../config/client_service_secret.json',
                                                 serialize='../config/credentials.json')

        self.webproperty = account[url]
        if self.webproperty is None:
            return False

    def devices(self):
        dimension = 'device'
        report = self.webproperty.query.range(self.start_day, days=self.days_back).dimension(dimension).get()
        return report.rows

    def queries(self):
        dimension = 'query'
        report = self.webproperty.query.range(self.start_day, days=self.days_back).dimension(dimension).get()
        return report.rows

    def countries(self):
        dimension = 'country'
        report = self.webproperty.query.range(self.start_day, days=self.days_back).dimension(dimension).get()
        return report.rows

    def pages(self):
        dimension = 'page'
        report = self.webproperty.query.range(self.start_day, days=self.days_back).dimension(dimension).get()
        return report.rows


if __name__ == '__main__':
    g = GoogleSearchConsole('https://oesterbaron.nl/')
    report = g.countries()

    print(report)

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
