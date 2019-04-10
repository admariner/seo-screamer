import csv
import os

from pathlib import Path
import pandas as pd

class ParceCSV:
    def __init__(self, file=None):
        self.crawl_data = {}
        self.ready_data = {}

        if file is None:
            return None

        files = {}

        self.file = file
        self.headers = []
        self.ready_data = {}

        my_file = Path(self.file)
        if not my_file.is_file():
            return None

        self.get_csv()

    def get_csv(self):
        df = pd.read_csv(self.file, skiprows=1)
        col_headers = list(df.columns)

        self.headers = col_headers
        name = self.first_row()
        
        self.ready_data[name] = {'headers': self.headers, 'data': df.to_dict(orient='records')}

    def first_row(self):
        with open(self.file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
            # do something here with `row`
                return row[0]


if __name__ == '__main__':
    domain = "oesterbaron.nl"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(dir_path, "../data")
    domain_folder = os.path.join(folder, "{}".format(domain))

    # fileNames = os.listdir(domain_folder)
    # for fileName in fileNames:
    #     if fileName.endswith(".csv") and fileName != 'crawl_overview.csv':
    #         print(fileName)

    csv_file = "../data/oesterbaron.nl/protocol_https.csv"
    c = ParceCSV(csv_file)
    
    for key, val in c.ready_data.items():
        print(val['headers'])
        print(len(val['headers']))
    
    # print(c.headers)
    # print(c.ready_data)

# protocol_http.csv
# h1_missing.csv
# h1_multiple.csv
# h1_over_70_characters.csv
# h1_duplicate.csv

# url_uppercase.csv
# url_parameters.csv
# h1_duplicate.csv
# meta_keywords_multiple.csv
# url_all.csv
# response_codes_client_error_(4xx).csv
# meta_description_over_940_pixels.csv
# response_codes_server_error_(5xx).csv
# url_duplicate.csv
# meta_keywords_duplicate.csv
# internal_pdf.csv
# h2_over_70_characters.csv
# response_codes_all.csv
# h2_multiple.csv
# response_codes_no_response.csv
# response_codes_redirection_(meta_refresh).csv
# meta_keywords_missing.csv
# page_titles_missing.csv
# response_codes_redirection_(3xx).csv
# h1_multiple.csv
# page_titles_below_30_characters.csv
# external_flash.csv
# external_pdf.csv
# response_codes_success_(2xx).csv
# internal_html.csv
# external_javascript.csv
# page_titles_multiple.csv
# meta_description_multiple.csv
# page_titles_below_200_pixels.csv
# page_titles_duplicate.csv
# url_over_115_characters.csv
# external_images.csv
# meta_description_all.csv
# h1_all.csv
# internal_other.csv
# response_codes_blocked_by_robots_txt.csv
# h2_duplicate.csv
# page_titles_over_568_pixels.csv
# page_titles_same_as_h1.csv
# protocol_http.csv
# h2_all.csv
# protocol_all.csv
# meta_description_below_400_pixels.csv
# url_non_ascii_characters.csv
# meta_description_duplicate.csv
# protocol_https.csv
# page_titles_over_65_characters.csv
# external_css.csv
# meta_description_missing.csv
# h2_missing.csv
# internal_unknown.csv
# internal_images.csv
# page_titles_all.csv
# internal_flash.csv
# external_all.csv
# meta_description_below_70_characters.csv
# external_other.csv
# external_html.csv
# internal_css.csv
# url_underscores.csv
# internal_javascript.csv
# internal_all.csv
# meta_description_over_155_characters.csv
# response_codes_blocked_resource.csv
# h1_over_70_characters.csv
# external_unknown.csv
# meta_keywords_all.csv
# h1_missing.csv
# response_codes_redirection_(javascript).csv
