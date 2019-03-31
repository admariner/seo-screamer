# from __future__ import print_function

#https://python-docx.readthedocs.io/en/latest/
#https://github.com/python-openxml/python-docx

import os
from mailmerge import MailMerge
from datetime import date

from functions.domain import Domain
from functions.crawl_overview import CrawlOverview

import locale
locale.setlocale(locale.LC_TIME, "nl_NL")


class MergeWord:
    def __init__(self, url=None, domein=None):
        self.datum = '{:%d-%b-%Y}'.format(date.today())
        if url is None or domein is None:
            return None

        self.frog_files = {}
        self.frog_data_folder = None
        self.document_fields = None
        self.document = None
        self.data = {}
        self.co_data = {}

        self.url = url
        self.domein = domein
        self.template = "word_templates/seo_doc.docx"
        self.get_frog_folder()
        self.get_frog_files()

        self.get_crawl_overview_data()
        self.open_document()

    def get_frog_folder(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_folder = os.path.join(dir_path, "data")
        self.frog_data_folder = os.path.join(data_folder, self.domein)

    def get_frog_files(self):
        for r, d, f in os.walk(self.frog_data_folder):
            for file in f:
                if '.csv' in file:
                    self.frog_files[file] = os.path.join(r, file)

    def get_crawl_overview_data(self):
        try:
            c = CrawlOverview(self.frog_files['crawl_overview.csv'])
            self.co_data = c.ready_data
        except KeyError:
            return {}

    def open_document(self):
        self.document = MailMerge(self.template)
        self.document_fields = self.document.get_merge_fields()

    def merge_document(self):
        self.data['datum'] = "{}".format(self.datum)
        self.data['url'] = "{}".format(self.domein)

        self.document.merge(
            **self.data,
            **self.co_data
        )

    def write_document(self):
        self.document.write("word_output/{}_{}.docx".format(self.domein, self.datum))


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(dir_path, "data")

    for domain in os.listdir(folder):
        domain_folder = os.path.join(folder, domain)
        if os.path.isdir(domain_folder) or os.path.islink(domain_folder):
            url = "https://{}".format(domain)
            d = Domain(url)

            m = MergeWord(url, d.domain)
            m.merge_document()
            m.write_document()

    # m.get_pagespeed_data()

"""
/Applications/Screaming\ Frog\ SEO\ Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher --crawl https://oesterbaron.nl --config /Users/theovandersluijs/PycharmProjects/seowork/data/oesterbaron.nl/crawl.seospiderconfig --headless --save-crawl --overwrite --output-folder /Users/theovandersluijs/PycharmProjects/seowork/data/oesterbaron.nl/  --save-report "Crawl Overview" --export-format "csv"


--use-google-analytics [google account] [account] [property] [view] [segment]
--use-google-search-console [google account] [website]
"""
