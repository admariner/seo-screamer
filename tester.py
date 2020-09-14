# import searchconsole
# account = searchconsole.authenticate(client_config='config/client_secrets.json',
#                                      serialize='config/client_service_secret.json')
# webproperty = account['https://oesterbaron.nl/']
# report = webproperty.query.range('today', days=-7).dimension('query').get()
# print(report.rows)

import yaml
import os.path

export = "bulk_exports"
# export = "export_tabs"

with open(f'config/{export}.yml') as file:
    rows = yaml.load(file, Loader=yaml.FullLoader)
    print(len(rows[export]))


#     for r in rows[export]:
#         if not r['file'] or r['file'] == "null":
#             print(r['id'])
#             filename = r['id']
#             filename = filename.replace(" Inlinks", "")
#             filename = filename.replace("-", "")
#             filename = filename.replace(" ", "_")
#             filename = filename.replace(":", "_")
#             filename = f"{filename}.csv"
#             filename = filename.lower()
#             if os.path.isfile(
#                     f'/Users/theovandersluijs/PyProjects/seo-screamer/data/rensini.nl/crawl/{filename}'):
#                 print(f"{filename} bestaat!")
#                 r['file'] = filename
#             else:
#                 print(f"{filename} bestaat niet")

# with open(f'config/{export}.yml', 'w') as file:
#     documents = yaml.dump(rows, file)
