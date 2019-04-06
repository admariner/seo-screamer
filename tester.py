import os

from functions.readConfig import readConfig
from functions.page_speed import PageSpeed
from functions.domain import Domain


if __name__ == '__main__':
    category = "performance"
    category = "accessibility"
    category = "seo"

    category = ['performance']

    strategy = "mobile"
    strategy = "desktop"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(dir_path, "data")
    file_name = "{}-{}.json".format(strategy, "oesterbaron.nl")
    data_file = os.path.join(folder, file_name)

    url = "https://oesterbaron.nl"

    cf = readConfig()
    config = cf.config

    ps_api = config['google_page_speed_api']

    d = Domain(url)
    p = PageSpeed(ps_api, url, d.domain, strategy)
    p.save_file_with_contents(data_file)

    p.create_data()
    print(p.ready_data)
    print(p.google_url)

    # print(p.google_url)dir_path = os.path.dirname(os.path.realpath(__file__))

    #
    # lighthouseResult = p.ps_data['lighthouseResult']
    #
    # print(lighthouseResult['configSettings']['emulatedFormFactor'])
    # print(lighthouseResult['configSettings']['locale'])
    #
    # for c in category:
    #     print(c)
    #     print(lighthouseResult['categories'][c]['title'])
    #     print(lighthouseResult['categories'][c]['score'])
    #
    # audit_list = ['first-contentful-paint', 'speed-index', 'interactive', 'first-meaningful-paint', 'first-cpu-idle',
    #               'estimated-input-latency']
    # audits = lighthouseResult['audits']
    #
    # for a in audit_list:
    #     print(audits[a]['title'])
    #     print(audits[a]['score'])
    #     print(audits[a]['displayValue'])
    #     print(audits[a]['description'])

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


"""
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fwww.vandersluijs.nl&category=performance
&category=accessibility&category=seo&strategy=mobile&key=
"""
