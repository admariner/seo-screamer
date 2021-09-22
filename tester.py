import csv
import json


csv_file = f'/Users/theovandersluijs/PyProjects/seo-screamer/data/paintdecoratie.nl/crawl/crawl_overview.csv'
# csv_file = f'/Users/theovandersluijs/PyProjects/seo-screamer/data/oesterbaron.nl/crawl/crawl_overview.csv'

key = "Site summary"
data = {}
data[key] = []

with open(csv_file, encoding='utf-8-sig') as f:
    cf = csv.reader(f)
    for row in cf:
        if len(row) > 1:
            if row[0] == 'Response Time (Seconds)':
                key = 'Response Time (Seconds)'
                data[key] = []
                continue

            rd = {}
            rd[row[0]] = row[1:]

            data[key].append(rd)
            continue

        if len(row) == 1 and row[0] == "":
            continue

        if len(row) == 1 and row[0] != "":
            key = row[0]
            data[key] = []


with open("/Users/theovandersluijs/PyProjects/seo-screamer/data/crawl.json", 'w') as f:
    json_dumps_str = json.dumps(data, indent=4)
    print(json_dumps_str, file=f)

# # print(data)
# d1 = {}
# for i in data['Site summary']:
#     d1.update(i)

# print(d1)
