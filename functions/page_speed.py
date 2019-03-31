import requests

from datetime import date


class PageSpeed:
    def __init__(self, ps_api=None, url=None, domain=None, strategy="mobile", locale="nl"):
        if url is None or ps_api is None:
            return None

        self.datum = '{:%d-%b-%Y}'.format(date.today())
        self.ready_data = {}
        self.google_api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.url = url
        self.strategy = strategy
        self.category = ['performance', 'accessibility', 'seo', 'best-practices', 'pwa']
        self.locale = locale
        self.ps_data = ""
        self.data_file = "../data/{}-{}.csv".format(self.datum, domain)
        self.google_url = ""

        self.ps_api = ps_api # PageSpeed API
        self.get_pagespeed_data()

    def get_pagespeed_data(self):
        new_category = ""
        if isinstance(self.category, list):
            for c in self.category:
                new_category += "&category={}".format(c)
        else:
            new_category = "&category={}".format(self.category)

        self.google_url = "{}" \
                     "?url={}" \
                     "{}" \
                     "&strategy={}" \
                     "&locale={}" \
                     "&key={}".format(self.google_api, self.url, new_category, self.strategy, self.locale, self.ps_api)

        resp = requests.get(url=self.google_url)
        self.ps_data = resp.json()

    # def mobile_data(self):
    #     print('mobile')
    #
    # def desktop_data(self):
    #     print('desktop')

    def create_data(self):
        ps_data = self.ps_data['lighthouseResult']
        for c in self.category:
            self.ready_data['mob_{}_score'.format(c)] = ps_data['categories'][c]['score']
            self.ready_data['desk_{}_score'.format(c)] = ps_data['categories'][c]['score']


# Toegankelijkheid
# Deze controles markeren mogelijkheden om [de toegankelijkheid van uw web-app te verbeteren] (https://developers.google.com/web/fundamentals/accessibility). Alleen een deel van de toegankelijkheidsproblemen kan automatisch worden gedetecteerd, zodat handmatig testen ook wordt aangemoedigd.
# Deze items behandelen gebieden die een geautomatiseerde testtool niet kan dekken. Lees meer in onze handleiding over het uitvoeren van een beoordeling van de toegankelijkheid (https://developers.google.com/web/fundamentals/accessibility/how-to-review).

# SEO
# Deze controles zorgen ervoor dat uw pagina is geoptimaliseerd voor het rangschikken van zoekmachines. Er zijn nog andere factoren die Lighthouse niet controleert en die van invloed kan zijn op uw positie in de zoekresultaten. Meer informatie (https://support.google.com/webmasters/answer/35769).
# Voer deze extra validators uit op uw site om aanvullende SEO-best practices te controleren.

# PWA
# Deze controles valideren de aspecten van een Progressive Web App. Meer informatie (https://developers.google.com/web/progressive-web-apps/checklist).
# Deze controles zijn vereist door de basislijn PWA-checklist (https://developers.google.com/web/progressive-web-apps/checklist) maar worden niet automatisch gecontroleerd door Lighthouse. Ze hebben geen invloed op je score, maar het is belangrijk dat je ze handmatig verifieert.


    def save_file_with_contents(self, file=None):
        if file is not None:
            self.data_file = file

        with open(self.data_file, 'w+') as f:
            f.write(str(self.ps_data))


if __name__ == '__main__':

    #https://jsoneditoronline.org/?id=241176c2533b4dfa8804972405f91059 mobile seo
    #https://jsoneditoronline.org/?id=73a278b6ebeb46a39f867c485285120e desktop performance
    category = "performance"
    category = "accessibility"
    category = "seo"

    strategy = "mobile"
    strategy = "desktop"

    url = "https://www.vandersluijs.nl"
    domain = "vandersluijs.nl"
    ps_api = ""

    p = PageSpeed(ps_api, url, domain, strategy)

    lighthouseResult = p.ps_data['lighthouseResult']

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

