import os

from functions.readConfig import readConfig

cf = readConfig()
config = cf.config

ps_api = config['google_page_speed_api']
crawl_files = config['crawl_files']
 
 
print(len(crawl_files))
crawl_files = [i for i in crawl_files if not (i['active'] == 0)] 


# i = 0
# for c in crawl_files:
#   print(c['file'])
#   print(i)
#   i += 1
        
# i = 0
# for i in range(len(crawl_files)):
#     print(i)
#     if crawl_files[i]['active'] == 0:
#         del crawl_files[i]    

print(len(crawl_files))        
for c in crawl_files:
    print(c)
 