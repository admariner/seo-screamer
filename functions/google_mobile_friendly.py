import requests


class GoogleMobileFriendly:
    def __init__(self, api=None, url=None):
        if api is None or url is None:
            return

        self.api = api
        self.url = url
        self.data = {}

        self.get_data()


    def get_data(self):
        self.get_google_data()

    def get_google_data(self):

        google_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key={}".format(self.api)
        data = {"url": self.url}
        r = requests.post(google_url, data)
        self.data = r.text


if __name__ == '__main__':
    url = "https://www.vandersluijs.nl"
    api = ""
    g = GoogleMobileFriendly(api, url)
    print(g.data)
