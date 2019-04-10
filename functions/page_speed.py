import requests
import os
import time
import json

from datetime import date


class PageSpeed:
    def __init__(self, ps_api=None, url=None, domain=None, strategy="mobile", locale="nl"):
        if url is None or ps_api is None:
            return None

        self.categorien = {"performance": "Algemene snelheidsscore is:",
                           "accessibility": "Algemene toegankelijkheid-score is:",
                           "seo": "Algemene seo-score is:",
                           "best-practices": "Algemene best-practices score is:"}

        self.audit_list_performance = ['first-contentful-paint', 'speed-index', 'interactive', 'first-meaningful-paint', 'first-cpu-idle',
                      'estimated-input-latency']

        self.datum = '{:%d-%b-%Y}'.format(date.today())
        self.ready_data = {}
        self.google_api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.url = url
        self.strategy = strategy
        self.category = ['performance', 'accessibility', 'seo', 'best-practices'] #pwa
        self.locale = locale
        self.ps_data = ""
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        folder = os.path.join(dir_path, "../data")
        domain_folder = os.path.join(folder, "{}".format(domain))
        data_file_name = "{}_{}_{}.json".format(self.datum, self.strategy, domain)
        self.data_file =  os.path.join(domain_folder, data_file_name)
        
        self.google_url = ""

        self.ps_api = ps_api # PageSpeed API
        # self.get_pagespeed_data()
        self.get_data()
        self.create_data()


    def get_pagespeed_data(self):
        new_category = ""
        if isinstance(self.category, list):
            for c in self.category:
                new_category += "&category={}".format(c)
        else:
            new_category = "&category={}".format(self.category)
            
        if self.ps_api == "":
            key = ""
        else:
            key = "&key={}".format(self.ps_api)
    
        self.google_url = "{}" \
                     "?url={}" \
                     "{}" \
                     "&strategy={}" \
                     "&locale={}" \
                     "{}".format(self.google_api, self.url, new_category, self.strategy, self.locale, key)

        print(self.google_url)

        r = requests.get(url=self.google_url)
        return r.json()

    def create_data(self):
        try:
            ps_data = self.ps_data['lighthouseResult']
        except KeyError:
            print('No Data')
        for c in self.category:
            self.ready_data['{}_{}_score'.format(self.strategy, c)] = round(ps_data['categories'][c]['score']*100)

        for a in self.audit_list_performance:
            self.ready_data['{}_{}_title'.format(self.strategy, a)] = ps_data['audits'][a]['title']
            self.ready_data['{}_{}_score'.format(self.strategy, a)] = round(ps_data['audits'][a]['score']*100)
            self.ready_data['{}_{}_displayValue'.format(self.strategy, a)] = ps_data['audits'][a]['displayValue']
        
    def get_data(self, file=None):
        if file is not None:
            self.data_file = file
        
        exists = os.path.isfile(self.data_file)
        if exists:
            print('Found pagespeed json file')
            
            file = os.path.basename(self.data_file)
            file_date = file.split("_")
            
            if file_date[0] == self.datum:
                print('Using data from pagespeed json file')
                self.ps_data = self.open_file_with_contents(self.data_file)
                return 
    
        self.ps_data = self.get_pagespeed_data()
        print('No pagespeed file found')
        if self.ps_data is not None:
            print('Create file with pagespeed json file')
            self.save_file_with_contents(self.data_file)

    def open_file_with_contents(self, file=None):
        if file is not None:
            self.data_file = file
            
        with open(self.data_file, 'r') as json_file:
            return json.load(json_file)

    def save_file_with_contents(self, file=None):
        if file is not None:
            self.data_file = file

        with open(self.data_file, 'w+') as output:
            json.dump(self.ps_data, output)


if __name__ == '__main__':
    #https://jsoneditoronline.org/?id=241176c2533b4dfa8804972405f91059 mobile seo
    #https://jsoneditoronline.org/?id=73a278b6ebeb46a39f867c485285120e desktop performance
    category = "performance"
    category = "accessibility"
    category = "seo"

    strategy = "mobile"
    strategy = "desktop"

    url = "https://www.vandersluijs.nl"
    domain = "www.vandersluijs.nl"
    ps_api = ""

    p = PageSpeed(ps_api, url, domain, strategy)
    if p is None:
        print('Houston we have a problem')
    else:
        lighthouseResult = p.ps_data['lighthouseResult']
    
        print(p.ready_data)

"""    
        print(lighthouseResult['configSettings']['emulatedFormFactor'])
        print(lighthouseResult['configSettings']['locale'])
    
        for c in category:
            print(c)
            print(lighthouseResult['categories'][c]['title'])
            print(lighthouseResult['categories'][c]['score'])
    
        audit_list = ['first-contentful-paint', 'speed-index', 'interactive', 'first-meaningful-paint', 'first-cpu-idle',
                      'estimated-input-latency']
        audits = lighthouseResult['audits']
    
        for a in audit_list:
            print(audits[a]['title'])
            print(audits[a]['score'])
            print(audits[a]['displayValue'])
            print(audits[a]['description'])
"""
# render-blocking-resources -> css enz wat te lang duurt -> details -> items[0] enz (url, totalBytes, wastedMs)
# uses-optimized-images details -> items[0] enz (url, totalBytes, wastedBytes, overallSavingsBytes)
# uses-text-compression (gzip)
# uses-long-cache-ttl (caching)
# font-display details->items[0] (url, wastedMs)

# server snelheid
# time-to-first-byte

# offscreen-images

# total-byte-weight
# unminified-javascript
# unminified-css
# redirects

# en
# efficient-animated-content


# Toegankelijkheid
# Deze controles markeren mogelijkheden om [de toegankelijkheid van uw web-app te verbeteren] (https://developers.google.com/web/fundamentals/accessibility). Alleen een deel van de toegankelijkheidsproblemen kan automatisch worden gedetecteerd, zodat handmatig testen ook wordt aangemoedigd.
# Deze items behandelen gebieden die een geautomatiseerde testtool niet kan dekken. Lees meer in onze handleiding over het uitvoeren van een beoordeling van de toegankelijkheid (https://developers.google.com/web/fundamentals/accessibility/how-to-review).

# SEO
# Deze controles zorgen ervoor dat uw pagina is geoptimaliseerd voor het rangschikken van zoekmachines. Er zijn nog andere factoren die Lighthouse niet controleert en die van invloed kan zijn op uw positie in de zoekresultaten. Meer informatie (https://support.google.com/webmasters/answer/35769).
# Voer deze extra validators uit op uw site om aanvullende SEO-best practices te controleren.

# PWA
# Deze controles valideren de aspecten van een Progressive Web App. Meer informatie (https://developers.google.com/web/progressive-web-apps/checklist).
# Deze controles zijn vereist door de basislijn PWA-checklist (https://developers.google.com/web/progressive-web-apps/checklist) maar worden niet automatisch gecontroleerd door Lighthouse. Ze hebben geen invloed op je score, maar het is belangrijk dat je ze handmatig verifieert.

