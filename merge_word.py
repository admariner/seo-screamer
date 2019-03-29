# from __future__ import print_function
import os
from mailmerge import MailMerge
from datetime import date

from functions.domain import Domain
from functions.crawl_overview import CrawlOverview

import requests

import locale
locale.setlocale(locale.LC_TIME, "nl_NL")


class MergeWord:
    def __init__(self, url=None, domein=None):
        self.datum = '{:%d-%b-%Y}'.format(date.today())
        if url is None or domein is None:
            return None

        self.url = url
        self.domein = domein
        self.template = "word_templates/seo_doc.docx"
        self.frog_data = self.get_frog_folder()
        self.co_data = self.get_CrawlOverview_data()
        self.data = {}

    def get_frog_folder(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data = os.path.join(dir_path, "data")
        return os.path.join(data, self.domein)

    def get_CrawlOverview_data(self):
        c = CrawlOverview(self.frog_data)
        return c.crawl_data

    def write_document(self):
        document = MailMerge(self.template)
        print(document.get_merge_fields())

        self.data = {'datum': "{}".format(self.datum)}
        self.data = {'url': "{}".format(self.domain)}

        document.merge(

        )
        #
        # document.write("word_output/{}_{}.docx".format(self.domain, self.datum))


if __name__ == '__main__':
    url = "https://oesterbaron.nl"
    url = input('Welk domein?')

    d = Domain(url)

    m = MergeWord(url, d.domain)
    m.write_document()
    # m.get_pagespeed_data()

"""
/Applications/Screaming\ Frog\ SEO\ Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher --crawl https://oesterbaron.nl --config /Users/theovandersluijs/PycharmProjects/seowork/data/oesterbaron.nl/crawl.seospiderconfig --headless --save-crawl --overwrite --output-folder /Users/theovandersluijs/PycharmProjects/seowork/data/oesterbaron.nl/  --save-report "Crawl Overview" --export-format "csv"


--use-google-analytics [google account] [account] [property] [view] [segment]
--use-google-search-console [google account] [website]
"""
