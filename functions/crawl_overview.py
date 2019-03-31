import csv
import os
from pathlib import Path

class CrawlOverview:
    def __init__(self, crawl_file=None):
        self.crawl_data = {}
        self.ready_data = {}

        if crawl_file is None:
            return None

        self.file = crawl_file  #os.path.join(cralw_data, "crawl_overview.csv")

        my_file = Path(self.file)
        if not my_file.is_file():
            return None

        self.data = self.get_csv()

        self.get_csv()
        self.get_data()

        self.ready_data = {
            'Date': "{}".format(self.crawl_data['Date'][0]),
            'Time': "{}".format(self.crawl_data['Time'][0]),
            'Crawled': "{}".format(self.crawl_data['Summary']['Total URLs Crawled'][0]),
            'Encountered': "{}".format(self.crawl_data['Summary']['Total URLs Encountered'][0]),
            'Internal': "{}".format(self.crawl_data['URLs Displayed']['Total Internal URLs'][0]),
            'External': "{}".format(self.crawl_data['URLs Displayed']['Total External URLs'][0]),
            'robots_blocked': "{}".format(self.crawl_data['Summary']['Total Internal blocked by robots.txt']),
            'robots_blocked_external': "{}".format(self.crawl_data['Summary']['Total External blocked by robots.txt']),

            'amp_general_errors': "{}".format(self.crawl_data['AMP']['Other Validation Errors'][0]),
            'amp_missing_viewport': "{}".format(self.crawl_data['AMP']['Missing/Invalid <meta viewport> Tag'][0]),
            'amp_missing_script': "{}".format(self.crawl_data['AMP']['Missing/Invalid AMP Script'][0]),
            'amp_non_canonical': "{}".format(self.crawl_data['AMP']['Missing Canonical'][0]),
            'amp_missing_boiler': "{}".format(self.crawl_data['AMP']['Missing/Invalid AMP Boilerplate'][0]),
            'amp_missing_html': "{}".format(self.crawl_data['AMP']['Missing <html amp> Tag'][0]),
            'amp_missing_canonical': "{}".format(self.crawl_data['AMP']['Missing Canonical'][0]),
            'amp_missing_head': "{}".format(self.crawl_data['AMP']['Missing <head> Tag'][0]),
            'amp_canonical': "{}".format(self.crawl_data['AMP']['Non-Confirming Canonical'][0]),
            'amp_missing_body': "{}".format(self.crawl_data['AMP']['Missing <body> Tag'][0]),
            'amp_missing_meta': "{}".format(self.crawl_data['AMP']['Missing/Invalid <meta charset> Tag'][0]),
            'amp_missing_doctype': "{}".format(self.crawl_data['AMP']['Missing/Invalid <!doctype html> Tag'][0]),
            'amp_not_200': "{}".format(self.crawl_data['AMP']['Non-200 Response'][0]),
            'amp_non_index': "{}".format(self.crawl_data['AMP']['Non-Indexable'][0]),
            'amp_index_canonical': "{}".format(self.crawl_data['AMP']['Non-Indexable Canonical'][0]),
            'amp_wong_html': "{}".format(self.crawl_data['AMP']['Contains Disallowed HTML'][0]),

            'protocol_http': "{}".format(self.crawl_data['Protocol']['HTTP'][0]),
            'protocol_https': "{}".format(self.crawl_data['Protocol']['HTTPS'][0]),

            'responsecodes_redirect_jv': "{}".format(self.crawl_data['Response Codes']['Redirection (JavaScript)'][0]),
            'responsecodes_redirect_meta': "{}".format(self.crawl_data['Response Codes']['Redirection (Meta Refresh)'][0]),
            'responsecodes_200': "{}".format(self.crawl_data['Response Codes']['Success (2xx)'][0]),
            'responsecodes_300': "{}".format(self.crawl_data['Response Codes']['Redirection (3xx)'][0]),
            'responsecodes_400': "{}".format(self.crawl_data['Response Codes']['Client Error (4xx)'][0]),
            'responsecodes_500': "{}".format(self.crawl_data['Response Codes']['Server Error (5xx)'][0]),
            'responsecodes_blocked_source': "{}".format(self.crawl_data['Response Codes']['Blocked Resource'][0]),
            'responsecodes_no_answer': "{}".format(self.crawl_data['Response Codes']['No Response'][0]),
            'responsecodes_blocked_robots': "{}".format(self.crawl_data['Response Codes']['Blocked by Robots.txt'][0]),

            'image_100_chars': "{}".format(self.crawl_data['Images']['Alt Text Over 100 Characters'][0]),
            'image_alt': "{}".format(self.crawl_data['Images']['Missing Alt Text'][0]),
            'image_100kb': "{}".format(self.crawl_data['Images']['Over 100 KB'][0]),

            'title_missing': "{}".format(self.crawl_data['Page Titles']['Missing'][0]),
            'title_double': "{}".format(self.crawl_data['Page Titles']['Duplicate'][0]),
            'title_65': "{}".format(self.crawl_data['Page Titles']['Over 65 Characters'][0]),
            'title_30': "{}".format(self.crawl_data['Page Titles']['Below 30 Characters'][0]),
            'title_568': "{}".format(self.crawl_data['Page Titles']['Over 568 Pixels'][0]),
            'title_200': "{}".format(self.crawl_data['Page Titles']['Below 200 Pixels'][0]),
            'title_h1': "{}".format(self.crawl_data['Page Titles']['Same as H1'][0]),
            'title_multiple': "{}".format(self.crawl_data['Page Titles']['Multiple'][0]),

            'url_double': "{}".format(self.crawl_data['URL']['Duplicate'][0]),
            'url_params': "{}".format(self.crawl_data['URL']['Parameters'][0]),
            'url_underscores': "{}".format(self.crawl_data['URL']['Underscores'][0]),
            'url_ascii': "{}".format(self.crawl_data['URL']['Non ASCII Characters'][0]),
            'url_115': "{}".format(self.crawl_data['URL']['Over 115 Characters'][0]),
            'url_capitals': "{}".format(self.crawl_data['URL']['Uppercase'][0]),

            'h1_missing': "{}".format(self.crawl_data['H1']['Missing'][0]),
            'h1_double': "{}".format(self.crawl_data['H1']['Duplicate'][0]),
            'h1_70': "{}".format(self.crawl_data['H1']['Over 70 Characters'][0]),
            'h1_multiple': "{}".format(self.crawl_data['H1']['Multiple'][0]),

            'h2_missing': "{}".format(self.crawl_data['H2']['Missing'][0]),
            'h2_double': "{}".format(self.crawl_data['H2']['Duplicate'][0]),
            'h2_70': "{}".format(self.crawl_data['H2']['Over 70 Characters'][0]),
            'h2_multiple': "{}".format(self.crawl_data['H2']['Multiple'][0]),

            'schema_missing': "{}".format(self.crawl_data['Structured Data']['Missing Structured Data'][0]),
            'schema_errors': "{}".format(self.crawl_data['Structured Data']['Validation Errors'][0]),
            'schema_invalid': "{}".format(self.crawl_data['Structured Data']['Validation Warnings'][0]),
            'schema_parse_errors': "{}".format(self.crawl_data['Structured Data']['Parse Errors'][0]),
            'schema_urls': "{}".format(self.crawl_data['Structured Data']['Microdata URLs'][0]),
            'schema_json': "{}".format(self.crawl_data['Structured Data']['JSON-LD URLs'][0]),
            'schema_rdf': "{}".format(self.crawl_data['Structured Data']['RDFa URLs'][0]),

            'sitemap_urls': "{}".format(self.crawl_data['Sitemaps']['URLs in Sitemap'][0]),
            'sitemap_urls_missing': "{}".format(self.crawl_data['Sitemaps']['URLs not in Sitemap'][0]),
            'sitemap_orphan': "{}".format(self.crawl_data['Sitemaps']['Orphan URLs'][0]),
            'sitemap_not_index': "{}".format(self.crawl_data['Sitemaps']['Non-Indexable URLs in Sitemap'][0]),
            'sitemap_double': "{}".format(self.crawl_data['Sitemaps']['URLs in Multiple Sitemaps'][0]),
            'sitemap_50mb': "{}".format(self.crawl_data['Sitemaps']['XML Sitemap over 50MB'][0]),
            'sitemap_50000': "{}".format(self.crawl_data['Sitemaps']['XML Sitemap with over 50k URLs'][0]),

            'internal_html': "{}".format(self.crawl_data['Internal']['HTML'][0]),
            'internal_javascript': "{}".format(self.crawl_data['Internal']['JavaScript'][0]),
            'internal_css': "{}".format(self.crawl_data['Internal']['CSS'][0]),
            'internal_images': "{}".format(self.crawl_data['Internal']['Images'][0]),
            'internal_pdf': "{}".format(self.crawl_data['Internal']['PDF'][0]),
            'internal_flash': "{}".format(self.crawl_data['Internal']['Flash'][0]),
            'internal_other': "{}".format(self.crawl_data['Internal']['Other'][0]),
            'internal_unknown': "{}".format(self.crawl_data['Internal']['Unknown'][0]),

            'external_html': "{}".format(self.crawl_data['External']['HTML'][0]),
            'external_javascript': "{}".format(self.crawl_data['External']['JavaScript'][0]),
            'external_css': "{}".format(self.crawl_data['External']['CSS'][0]),
            'external_images': "{}".format(self.crawl_data['External']['Images'][0]),
            'external_pdf': "{}".format(self.crawl_data['External']['PDF'][0]),
            'external_flash': "{}".format(self.crawl_data['External']['Flash'][0]),
            'external_other': "{}".format(self.crawl_data['External']['Other'][0]),
            'external_unknown': "{}".format(self.crawl_data['External']['Unknown'][0]),

            'meta_desc_missing': "{}".format(self.crawl_data['Meta Description']['Missing'][0]),
            'meta_desc_multiple': "{}".format(self.crawl_data['Meta Description']['Multiple'][0]),
            'meta_desc_double': "{}".format(self.crawl_data['Meta Description']['Duplicate'][0]),
            'meta_desc_155': "{}".format(self.crawl_data['Meta Description']['Over 155 Characters'][0]),
            'meta_desc_70': "{}".format(self.crawl_data['Meta Description']['Below 70 Characters'][0]),
            'meta_desc_940': "{}".format(self.crawl_data['Meta Description']['Over 940 Pixels'][0]),
            'meta_desc_400': "{}".format(self.crawl_data['Meta Description']['Below 400 Pixels'][0]),

            'meta_key_double': "{}".format(self.crawl_data['Meta Keywords']['Missing'][0]),
            'meta_key_missing': "{}".format(self.crawl_data['Meta Keywords']['Duplicate'][0]),
            'meta_key_multiple': "{}".format(self.crawl_data['Meta Keywords']['Multiple'][0]),

            'content_big': "{}".format(self.crawl_data['Content']['Large Pages (Over 100KB)'][0]),
            'content_words': "{}".format(self.crawl_data['Content']['Low Content Pages (Under 300 Words)'][0]),
            }

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


if __name__ == '__main__':
    #if you want to see the dict in a viewable style, go to :
    #https://jsoneditoronline.org/?id=4c5e36491ec04ff697710bb13132c5e3

    csv_file = "../data/oesterbaron.nl/crawl_overview.csv"
    c = CrawlOverview(csv_file)
    print(c.ready_data)

