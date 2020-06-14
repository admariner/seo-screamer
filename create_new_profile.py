import os
import sys
import time

from functions.domain import Domain
import logging

sf = os.path.dirname(os.path.realpath(__file__))
folder = os.path.join(sf, 'logging')
log_file = os.path.join(folder, "{}.log".format(str(time.strftime("%Y%m%d"))))
os.makedirs(folder, exist_ok=True)

if(os.environ['HOME'] == '/Users/theovandersluijs'):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(filename=log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.CRITICAL)


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
        try:
            self.domain = ""
            while self.domain == "":
                self.domain = input('What domain? (not the actual url) ')
                if self.domain != "":
                    self.profile_folder = os.path.join(self.profiles_folder, self.domain)
                    try:
                        os.makedirs(self.profile_folder, exist_ok=False)
                    except OSError as e:
                        raise Exception("Sorry, domain already exsists! {}".format(e))

                    # create crawl folder
                    folders = ['crawl', 'page_speed', 'graphs', 'google_search_console']
                    self.create_folders(folders)

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
                self.search_console_url = input('What Google Search Console Url? ([n] for dont use)')
                if self.search_console_url == 'n':
                    self.search_console_url = ""
                    break


            while self.word_template is None:
                standard = ""
                while standard not in ['y','n']:
                    standard = input('Use standard Word template? [y/n] ')
                    if standard == 'y':
                        self.word_template = "test_doc.docx"
                    elif standard == 'n':
                        empty = ""
                        while empty not in ['y', 'n']:
                            empty = input('Use no Word template? [y/n] ')
                            if empty == 'y':
                                self.word_template = ""
                            elif empty == 'n':
                                self.word_template = input('Other Word template? [name] ')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def create_folders(self, folders=None):
        if folders is None:
            raise Exception("Folder variable is None!")

        try:

            for f in folders:
                folder = os.path.join(self.profile_folder, f)
                try:
                    os.makedirs(folder, exist_ok=False)
                except OSError as e:
                    raise Exception("Sorry cannot create folder : {}".format(e))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def create_config_data(self):
        self.conf_data += "active: {}\n".format(1)
        self.conf_data += "domain: {}\n".format(self.domain)
        self.conf_data += "url: {}\n".format(self.url)
        self.conf_data += "search_console_url: {}\n".format(self.search_console_url)
        self.conf_data += "word_template: {}\n".format(self.word_template)

    def create_config(self):
        try:
            file = os.path.join(self.profile_folder, "config.yml")
            with open(file, 'w') as f:
                f.write(self.conf_data)
                f.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))


if __name__ == '__main__':
    p = CreateProfile()
