import os
from functions.domain import Domain

class CreateProfile:
    def __init__(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.profiles_folder = os.path.join(dir_path, "data")

        self.profile_folder = ""
        self.domain = ""
        self.url = ""
        self.search_console_url = ""
        self.conf_data = ""
        self.word_template = None

        self.startup()
        self.create_config_data()
        self.create_config()

    def startup(self):
        self.domain = ""
        while self.domain == "":
            self.domain = input('What domain? (not the actual url) ')
            if self.domain != "":
                self.profile_folder = os.path.join(self.profiles_folder, self.domain)
                try:
                    os.makedirs(self.profile_folder, exist_ok=False)
                except OSError as e:
                    print('Sorry, this domain already exists!')
                    return False
                # create crawl folder
                crawl_folder = os.path.join(self.profile_folder, 'crawl')
                try:
                    os.makedirs(crawl_folder, exist_ok=False)
                except OSError as e:
                    print('Sorry, {}'.format(e))
                    return False
                # create pagespeed folder
                pagespeed_folder = os.path.join(self.profile_folder, 'page_speed')
                try:
                    os.makedirs(pagespeed_folder, exist_ok=False)
                except OSError as e:
                    print('Sorry, {}'.format(e))
                    return False
                #create google_search_console folder
                    google_search_console = os.path.join(self.profile_folder, 'google_search_console')
                try:
                    os.makedirs(google_search_console, exist_ok=False)
                except OSError as e:
                    print('Sorry, {}'.format(e))
                    return False

        print('Folder {} is created'.format(self.profile_folder))

        yesno = ""
        while yesno not in ['y', 'n']:
            yesno = input('Is the url https://{} ? [y/n] '.format(self.domain))
            if yesno == 'y':
                self.url = "https://{}".format(self.domain)
            elif yesno == 'n':
                yesno = input('Is the url http://{} ? [y/n] '.format(self.domain))
                if yesno == 'y':
                    self.url = "http://{} ? [y/n]".format(self.domain)

        while self.url == "":
            self.url = input('What url? (use http:// or https://) ')
            d = Domain(self.url)
            print(d.scheme)
            if d.scheme not in ['https', 'http']:
                self.url = ""
                print('Url is wrong!')

        while self.search_console_url == "":
            self.search_console_url = input('What Google Search Console Url? ')

        while self.word_template is None:
            standard = ""
            while standard not in ['y','n']:
                standard = input('Use standard Word template [y/n]')
                if standard == 'y':
                    self.word_template = "test_doc.docx"
                elif standard == 'n':
                    empty = ""
                    while empty not in ['y', 'n']:
                        empty = input('Use no Word template [y/n]')
                        if empty == 'y':
                            self.word_template = ""
                        elif empty == 'n':
                            self.word_template = input('Other Word template')


    def create_config_data(self):
        self.conf_data += "domain: {}\n".format(self.domain)
        self.conf_data += "url: {}\n".format(self.url)
        self.conf_data += "search_console_url: {}\n".format(self.search_console_url)
        self.conf_data += "word_template: {}\n".format(self.word_template)

    def create_config(self):
        file = os.path.join(self.profile_folder, "config.yml")
        with open(file, 'w') as f:
            f.write(self.conf_data)
            f.close()


if __name__ == '__main__':
    p = CreateProfile()
