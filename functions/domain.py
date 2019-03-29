from urllib.parse import urlparse


class Domain():
    def __init__(self, domain=None):
        if domain is None:
            return None

        self.url = domain
        self.scheme = self.get_uri_scheme()
        self.domain = self.get_uri_domain()

    def get_uri_scheme(self):
        parsed_uri = urlparse(self.url)
        return "{uri.scheme}".format(uri=parsed_uri)

    def get_uri_domain(self):
        parsed_uri = urlparse(self.url)
        return "{uri.netloc}".format(uri=parsed_uri)


if __name__ == '__main__':
    url = "https://www.vandersluijs.nl"
    d = Domain(url)

    print(d.scheme)
    print(d.domain)
