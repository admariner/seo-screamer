import os
import gspread
import csv
import json


csv_file = f'/Users/theovandersluijs/PyProjects/seo-screamer/data/paintdecoratie.nl/crawl/crawl_overview.csv'

key = "Summary"
data = {}
data[0] = ["category", "name", "URLs", "% of Total", "Total URLs", "Total URLs Description"]

i = 1
with open(csv_file, encoding='utf-8-sig') as f:
    cf = csv.reader(f)
    next(cf)
    next(cf)
    next(cf)
    next(cf)
    next(cf)
    for row in cf:
        if len(row) > 1:
            if row[0] == 'Response Time (Seconds)':
                break

            rd = []
            rd.append(key)
            for r in row:
                rd.append(r)
            data[i] = rd
            i += 1
            continue

        if len(row) == 1 and row[0] == "":
            continue

        if len(row) == 1 and row[0] != "":
            key = row[0]

# with open("/Users/theovandersluijs/PyProjects/seo-screamer/data/crawl.json", 'w') as f:
#     json_dumps_str = json.dumps(data, indent=4)
#     print(json_dumps_str, file=f)

with open('/Users/theovandersluijs/PyProjects/seo-screamer/data/crawl.csv', 'w') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for d, v in data.items():
        wr.writerow(v)

credentials = os.path.join('config', 'google_key.json')

# Check how to get `credentials`:
# https://github.com/burnash/gspread

gc = gspread.service_account(filename=credentials)

# Read CSV file contents
content = open('/Users/theovandersluijs/PyProjects/seo-screamer/data/crawl.csv', 'r').read()

gc.import_csv('1Qs3omfizqAi5jFpK2uWhmhE2QaD_9mfNmZ5pSgtpVkk', content)
# https://docs.google.com/open?id=1JFV-ck-_3cxWoNuZtGjyRBvO8XZaEjl5gu29qvpnywQ
