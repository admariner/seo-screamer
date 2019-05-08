import csv
import os
from pathlib import Path

class CrawlOverview:
    def __init__(self, crawl_file=None):
        self.crawl_data = {}
        self.ready_data = {}

        if crawl_file is None:
            return None

        self.file = crawl_file

        my_file = Path(self.file)
        if not my_file.is_file():
            return None

        self.data = self.get_csv()

        self.get_csv()
        self.get_data()

        self.table_headers = [
            "Algemene informatie","Interne Urls","Externe Urls","Protocol",
            "Response Codes","Inhoud","URL","Paginatitels",
            "Meta omschrijving","Meta-trefwoorden","H1","H2","Afbeeldingen",
            "Protocol","Gestructureerde gegevens","Sitemaps"
            ]
            
                 
        self.readydata = {}
        self.readydata['Algemene informatie'] = []
        try:
            self.readydata['Algemene informatie'].append(self.happy_data("Datum laatste crawl", self.crawl_data['Date'][0]))
            self.readydata['Algemene informatie'].append(self.happy_data("Aantal gevonden pagina’s & content", self.crawl_data['Summary']['Total URLs Encountered'][0]))
            self.readydata['Algemene informatie'].append(self.happy_data("Aantal gecrawlde pagina’s & content", self.crawl_data['Summary']['Total URLs Crawled'][0]))
            self.readydata['Algemene informatie'].append(self.happy_data("Totaal interne URL's", self.crawl_data['URLs Displayed']['Total Internal URLs'][0]))
            self.readydata['Algemene informatie'].append(self.happy_data("Totaal externe URL's", self.crawl_data['URLs Displayed']['Total External URLs'][0]))
            self.readydata['Algemene informatie'].append(self.happy_data("Totaal intern geblokkeerd voor robots", self.crawl_data['Summary']['Total External blocked by robots.txt'][0]))
        except KeyError as e:
            print('Algemene informatie error : {}'.format(e))
            
        self.readydata['Protocol'] = []
        try:
            self.readydata['Protocol'].append(self.happy_data('http', self.crawl_data['Protocol']['HTTP'][0], [0, 1], 3))
            # short = ( - self.crawl_data['Protocol']['HTTP'][0]) * 1
            self.readydata['Protocol'].append(self.happy_data('https', self.crawl_data['Protocol']['HTTPS'][0], [self.crawl_data['URLs Displayed']['Total Internal URLs'][0]]))
        except KeyError as e:
            print('Protocol error : {}'.format(e))

        self.readydata['AMP'] = []
        try:
            self.readydata['AMP'].append(self.happy_data('Andere valideringsfouten:', self.crawl_data['AMP']['Other Validation Errors'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende / ongeldige <meta viewport> tag:', self.crawl_data['AMP']['Missing/Invalid <meta viewport> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekend / ongeldig AMP-script:', self.crawl_data['AMP']['Missing/Invalid AMP Script'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende AMP Canonical:', self.crawl_data['AMP']['Missing Canonical'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende / ongeldige AMP-boilerplate', self.crawl_data['AMP']['Missing/Invalid AMP Boilerplate'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende <html amp> Tag:', self.crawl_data['AMP']['Missing <html amp> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende Canonical:', self.crawl_data['AMP']['Missing Canonical'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende <head> tag:', self.crawl_data['AMP']['Missing <head> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Canonical kan niet worden bevestigd:', self.crawl_data['AMP']['Non-Confirming Canonical'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekende <body> -tag:', self.crawl_data['AMP']['Missing <body> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekend / ongeldig <meta charset> Tag:', self.crawl_data['AMP']['Missing/Invalid <meta charset> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Ontbrekend / ongeldig <! Doctype html> Tag:', self.crawl_data['AMP']['Missing/Invalid <!doctype html> Tag'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Niet 200 respons:', self.crawl_data['AMP']['Non-200 Response'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Niet-indexeerbaar:', self.crawl_data['AMP']['Non-Indexable'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Niet-indexeerbaar Canonical:', self.crawl_data['AMP']['Non-Indexable Canonical'][0], [0, 1], 5))
            self.readydata['AMP'].append(self.happy_data('Bevat niet toegestane HTML:', self.crawl_data['AMP']['Contains Disallowed HTML'][0], [0, 1], 5))
        except KeyError as e:
            print('Amp error : {}'.format(e))

        self.readydata['Response Codes'] = []
        try:
            self.readydata['Response Codes'].append(self.happy_data('Redirection (JavaScript):', self.crawl_data['Response Codes']['Redirection (JavaScript)'][0], None, 5))
            self.readydata['Response Codes'].append(self.happy_data('Doorverwijzing (Meta Refresh):', self.crawl_data['Response Codes']['Redirection (Meta Refresh)'][0],None, 5))
            self.readydata['Response Codes'].append(self.happy_data('Succes (2xx):', self.crawl_data['Response Codes']['Success (2xx)'][0], [0]))
            self.readydata['Response Codes'].append(self.happy_data('Doorverwijzing (3xx):', self.crawl_data['Response Codes']['Redirection (3xx)'][0]))
            self.readydata['Response Codes'].append(self.happy_data('Clientfout (4xx):', self.crawl_data['Response Codes']['Client Error (4xx)'][0], [0, 1], 5))
            self.readydata['Response Codes'].append(self.happy_data('Serverfout (5xx):', self.crawl_data['Response Codes']['Server Error (5xx)'][0], [0, 1],  5))
            self.readydata['Response Codes'].append(self.happy_data('Geblokkeerde bron:', self.crawl_data['Response Codes']['Blocked Resource'][0], [0, 1], 3))
            self.readydata['Response Codes'].append(self.happy_data('Geen antwoord:', self.crawl_data['Response Codes']['No Response'][0], [0, 1], 5))
            self.readydata['Response Codes'].append(self.happy_data('Geblokkeerd door Robots.txt:', self.crawl_data['Response Codes']['Blocked by Robots.txt'][0], None, 3))
        except KeyError as e:
            print('Responsecode error : {}'.format(e))

        self.readydata['Afbeeldingen'] = []
        try:
            self.readydata['Afbeeldingen'].append(self.happy_data('Ontbrekende Alt-tekst:', self.crawl_data['Images']['Missing Alt Text'][0], [0, 1], 1))
            self.readydata['Afbeeldingen'].append(self.happy_data('Alt-tekst Meer dan 100 tekens:', self.crawl_data['Images']['Alt Text Over 100 Characters'][0], [0, 1], 1))
            self.readydata['Afbeeldingen'].append(self.happy_data('Meer dan 100 KB:', self.crawl_data['Images']['Over 100 KB'][0], [0, 1], 1))
        except KeyError as e:
            print('Afbeeldingen error : {}'.format(e))
            
        self.readydata['Paginatitels'] = []
        try:
            self.readydata['Paginatitels'].append(self.happy_data('Afwezig:', self.crawl_data['Page Titles']['Missing'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Duplicaat:', self.crawl_data['Page Titles']['Duplicate'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Meer dan 65 tekens:', self.crawl_data['Page Titles']['Over 65 Characters'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Onder de 30 tekens:', self.crawl_data['Page Titles']['Below 30 Characters'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Meer dan 568 pixels:', self.crawl_data['Page Titles']['Over 568 Pixels'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Onder 200 pixels:', self.crawl_data['Page Titles']['Below 200 Pixels'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Hetzelfde als H1:', self.crawl_data['Page Titles']['Same as H1'][0], [0, 1], 1))
            self.readydata['Paginatitels'].append(self.happy_data('Meerdere:', self.crawl_data['Page Titles']['Multiple'][0], [0, 1], 1))
        except KeyError as e:
            print('Paginatels error : {}'.format(e))

        self.readydata['URL'] = []
        try:
            self.readydata['URL'].append(self.happy_data('Duplicaat:', self.crawl_data['URL']['Duplicate'][0], [0, 1], 5))
            self.readydata['URL'].append(self.happy_data('Parameters:', self.crawl_data['URL']['Parameters'][0], [0, 1], 5))
            self.readydata['URL'].append(self.happy_data('Underscores:', self.crawl_data['URL']['Underscores'][0], [0, 1], 2))
            self.readydata['URL'].append(self.happy_data('Niet ASCII-tekens:', self.crawl_data['URL']['Non ASCII Characters'][0], [0, 1], 2))
            self.readydata['URL'].append(self.happy_data('Meer dan 115 tekens:', self.crawl_data['URL']['Over 115 Characters'][0], [0, 1], 2))
            self.readydata['URL'].append(self.happy_data('Hoofdletters:', self.crawl_data['URL']['Uppercase'][0], [0, 1], 2))
        except KeyError as e:
            print('Url error : {}'.format(e))

        self.readydata['H1'] = []
        try:
            self.readydata['H1'].append(self.happy_data('Afwezig:', self.crawl_data['H1']['Missing'][0], [0, 1], 1))
            self.readydata['H1'].append(self.happy_data('Duplicaat:', self.crawl_data['H1']['Duplicate'][0], [0, 1], 1))
            self.readydata['H1'].append(self.happy_data('Meer dan 70 tekens:', self.crawl_data['H1']['Over 70 Characters'][0], [0, 1], 1))
            self.readydata['H1'].append(self.happy_data('Meerdere:', self.crawl_data['H1']['Multiple'][0], [0, 1], 1))
        except KeyError as e:
            print('H1 error : {}'.format(e))

        self.readydata['H2'] = []
        try:
            self.readydata['H2'].append(self.happy_data('Afwezig:', self.crawl_data['H2']['Missing'][0], [0, 1], 1))
            self.readydata['H2'].append(self.happy_data('Duplicaat:', self.crawl_data['H2']['Duplicate'][0], [0, 1], 1))
            self.readydata['H2'].append(self.happy_data('Meer dan 70 tekens:', self.crawl_data['H2']['Over 70 Characters'][0], [0, 1], 1))
            self.readydata['H2'].append(self.happy_data('Meerdere:', self.crawl_data['H2']['Multiple'][0], [6], 1))
        except KeyError as e:
            print('H2 error : {}'.format(e))

        self.readydata['Gestructureerde gegevens'] = []
        try:
            self.readydata['Gestructureerde gegevens'].append(self.happy_data('Ontbrekende gestructureerde gegevens:', self.crawl_data['Structured Data']['Missing'][0], [0, 1], 5))
            self.readydata['Gestructureerde gegevens'].append(self.happy_data('Validatiefouten:', self.crawl_data['Structured Data']['Validation Errors'][0], [0, 1], 5))
            self.readydata['Gestructureerde gegevens'].append(self.happy_data('Valideringswaarschuwingen:', self.crawl_data['Structured Data']['Validation Warnings'][0], [0, 1], 5))
            self.readydata['Gestructureerde gegevens'].append(self.happy_data('Verwerkings fouten:', self.crawl_data['Structured Data']['Parse Errors'][0], [0, 1], 5))
            # self.readydata['Gestructureerde gegevens'].append(self.happy_data('Microdata-\'s:', self.crawl_data['Structured Data']['Microdata URLs'][0], [0, 1], 5))
            # self.readydata['Gestructureerde gegevens'].append(self.happy_data('JSON-LD-URL\'s:', self.crawl_data['Structured Data']['JSON-LD URLs'][0], [0, 1], 5))
            # self.readydata['Gestructureerde gegevens'].append(self.happy_data('RDFa-URL\'s:', self.crawl_data['Structured Data']['RDFa URLs'][0], [0, 1], 5))
        except KeyError as e:
            print('Gestructureerde gegevens error : {}'.format(e))
            
        self.readydata['Sitemaps'] = []
        try:        
            self.readydata['Sitemaps'].append(self.happy_data('URL\'s in sitemap:', self.crawl_data['Sitemaps']['All'][0], [self.crawl_data['Internal']['HTML'][0]]))
            self.readydata['Sitemaps'].append(self.happy_data('URL\'s niet in sitemap:', self.crawl_data['Sitemaps']['URLs not in Sitemap'][0], [0, 1], 3))
            self.readydata['Sitemaps'].append(self.happy_data('Orphan URL\'s:', self.crawl_data['Sitemaps']['Orphan URLs'][0], [0, 1], 3))
            self.readydata['Sitemaps'].append(self.happy_data('Niet-indexeerbare URL\'s in sitemap:', self.crawl_data['Sitemaps']['Non-Indexable URLs in Sitemap'][0], [0, 1], 5))
            self.readydata['Sitemaps'].append(self.happy_data('URL\'s in meerdere sitemaps:', self.crawl_data['Sitemaps']['URLs in Multiple Sitemaps'][0], [0, 1], 5))
            self.readydata['Sitemaps'].append(self.happy_data('XML-sitemap van meer dan 50MB:', self.crawl_data['Sitemaps']['XML Sitemap over 50MB'][0], [0, 1], 5))
            self.readydata['Sitemaps'].append(self.happy_data('XML-sitemap met meer dan 50.000 URL\'s:', self.crawl_data['Sitemaps']['XML Sitemap with over 50k URLs'][0], [0, 1], 5))
        except KeyError as e:
            print('Sitemaps error : {}'.format(e))

        self.readydata['Interne Urls'] = []
        try:
            self.readydata['Interne Urls'].append(self.happy_data('HTML', self.crawl_data['Internal']['HTML'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('JavaScript', self.crawl_data['Internal']['JavaScript'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('CSS', self.crawl_data['Internal']['CSS'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('Images', self.crawl_data['Internal']['Images'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('PDF', self.crawl_data['Internal']['PDF'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('Flash', self.crawl_data['Internal']['Flash'][0], None, 1))
            self.readydata['Interne Urls'].append(self.happy_data('Anders', self.crawl_data['Internal']['Other'][0]))
            self.readydata['Interne Urls'].append(self.happy_data('Onbekend', self.crawl_data['Internal']['Unknown'][0]))
        except KeyError as e:
            print('Interne Urls error : {}'.format(e))

        self.readydata['Externe Urls'] = []
        try:
            self.readydata['Externe Urls'].append(self.happy_data('HTML', self.crawl_data['External']['HTML'][0]))
            self.readydata['Externe Urls'].append(self.happy_data('JavaScript', self.crawl_data['External']['JavaScript'][0], None, 5))
            self.readydata['Externe Urls'].append(self.happy_data('CSS', self.crawl_data['External']['CSS'][0], None, 5))
            self.readydata['Externe Urls'].append(self.happy_data('Images', self.crawl_data['External']['Images'][0]))
            self.readydata['Externe Urls'].append(self.happy_data('PDF', self.crawl_data['External']['PDF'][0]))
            self.readydata['Externe Urls'].append(self.happy_data('Flash', self.crawl_data['External']['Flash'][0], None, 1))
            self.readydata['Externe Urls'].append(self.happy_data('Anders', self.crawl_data['External']['Other'][0]))
            self.readydata['Externe Urls'].append(self.happy_data('Onbekend', self.crawl_data['External']['Unknown'][0]))
        except KeyError as e:
            print('Externe Urls error : {}'.format(e))

        self.readydata['Meta omschrijving'] = []
        try:
            self.readydata['Meta omschrijving'].append(self.happy_data('Afwezig:', self.crawl_data['Meta Description']['Missing'][0], [0, 1], 1))
            self.readydata['Meta omschrijving'].append(self.happy_data('Meerdere:', self.crawl_data['Meta Description']['Multiple'][0], [0, 1], 5))
            self.readydata['Meta omschrijving'].append(self.happy_data('Duplicaat:', self.crawl_data['Meta Description']['Duplicate'][0], [0, 1], 1))
            self.readydata['Meta omschrijving'].append(self.happy_data('Meer dan 155 tekens:', self.crawl_data['Meta Description']['Over 155 Characters'][0], [0, 1], 1))
            self.readydata['Meta omschrijving'].append(self.happy_data('Onder 70 tekens:', self.crawl_data['Meta Description']['Below 70 Characters'][0], [0, 1], 1))
            self.readydata['Meta omschrijving'].append(self.happy_data('Meer dan 940 pixels:', self.crawl_data['Meta Description']['Over 940 Pixels'][0], [0, 1], 1))
            self.readydata['Meta omschrijving'].append(self.happy_data('Onder 400 pixels:', self.crawl_data['Meta Description']['Below 400 Pixels'][0], [0, 1], 1))
        except KeyError as e:
            print('Meta omschrijving error : {}'.format(e))

        self.readydata['Meta-trefwoorden'] = []
        try:
            meta_aanwezig = (int(self.crawl_data['Internal']['HTML'][0])-int(self.crawl_data['Meta Keywords']['Missing'][0]))
            self.readydata['Meta-trefwoorden'].append(self.happy_data('Aanwezig:', meta_aanwezig, [0, 1], 1))
            # self.readydata['Meta-trefwoorden'].append(self.happy_data('Duplicaat:', self.crawl_data['Meta Keywords']['Duplicate'][0], [0, 1], 1))
            # self.readydata['Meta-trefwoorden'].append(self.happy_data('Meerdere:', self.crawl_data['Meta Keywords']['Multiple'][0], [0, 1], 5))
        except KeyError as e:
            print('Meta-trefwoorden error : {}'.format(e))
    
        self.readydata['Inhoud'] = []    
        try:
            self.readydata['Inhoud'].append(self.happy_data('Grote pagina\'s (meer dan 100 KB):', self.crawl_data['Content']['Large Pages (Over 100KB)'][0], [0, 1], 1))
            self.readydata['Inhoud'].append(self.happy_data('Lage inhoudspagina\'s (minder dan 300 woorden):', self.crawl_data['Content']['Low Content Pages (Under 300 Words)'][0], [0, 1], 1))
        except KeyError as e:
            print('Inhoud error : {}'.format(e))

        '''
        Clicks Above 0 – This simply means the URL in question has 1 or more clicks.
        No GSC Data – This means that the API didn’t return any data for the URLs in the crawl. So the URLs either didn’t receive any impressions, or perhaps the URLs in the crawl are just different to those in GSC for some reason.
        Non-Indexable with GSC Data – This means the URL is non-indexable, but still has data from GSC.
        Orphan URLs – This means the URL was only discovered via GSC, and was not found via an internal link during the crawl.
        '''
        self.readydata['Google Search Console'] = []
        try:
            self.readydata['Google Search Console'].append(self.happy_data('Pagina\'s doorzocht:', self.crawl_data['Search Console']['All'][0], [self.crawl_data['Internal']['HTML'][0]]))
            half = (int(self.crawl_data['Internal']['HTML'][0])/2)
            self.readydata['Google Search Console'].append(self.happy_data('Kliks boven 0:', self.crawl_data['Search Console']['Clicks Above 0'][0], [0, half, self.crawl_data['Internal']['HTML'][0]]))
            self.readydata['Google Search Console'].append(self.happy_data('Geen GSC data:', self.crawl_data['Search Console']['No GSC Data'][0], [0, ]))
            self.readydata['Google Search Console'].append(self.happy_data('Orphan Url\'s:', self.crawl_data['Search Console']['Orphan URLs'][0], [0, 1]))
        except KeyError as e:
            print('Inhoud error : {}'.format(e))

    def get_csv(self):
        datafile = open(self.file, 'r')
        datareader = csv.reader(datafile, delimiter=",")
        data = []
        for row in datareader:
            data.append(row)
        datafile.close()
        return data

    def get_column(self, thelist, thecolumn):
        newlist = []
        for row in thelist:
            if len(row) >= thecolumn + 1:
                newlist.append(row[thecolumn])
            else:
                newlist.append("")
        return newlist

    def get_data(self):

        chapters = ['Summary', 'URLs Displayed', 'Internal', 'External', 'Protocol', 'Response Codes', 'Content',
                    'URL', 'Page Titles', 'Meta Description', 'Meta Keywords', 'H1', 'H2', 'Images', 'Canonicals',
                    'Pagination', 'Directives', 'Hreflang', 'AJAX', 'AMP', 'Structured Data', 'Sitemaps', 'Custom',
                    'Analytics', 'Search Console', 'Link Metrics', 'Depth (Clicks from Start URL)',
                    'Inlinks (Top 20 URLs)', 'Response Time (Seconds)']

        chapter = None
        for row in self.data:
            name = row[0]
            row.remove(name)

            if name == '':
                chapter = None

            if name in chapters and chapter not in ['Internal', 'External']:
                chapter = name
                self.crawl_data[chapter] = {}
                continue

            if name != '' and row != []:
                if chapter is not None:
                    self.crawl_data[chapter][name] = row
                else:
                    self.crawl_data[name] = row

    @staticmethod
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
    #if you want to see the dict in a viewable style, go to :
    #https://jsoneditoronline.org/?id=4c5e36491ec04ff697710bb13132c5e3

    csv_file = "../data/oesterbaron.nl/crawl/crawl_overview.csv"
    c = CrawlOverview(csv_file)
    print(c.readydata)

