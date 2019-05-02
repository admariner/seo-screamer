import os
from functions.readConfig import readConfig

class Screaming:
    def __init__(self, folder=None, url=None, search_console_url=None):
        if folder is None or url is None:
            return None

        self.folder = folder
        self.url = url
        self.search_console_url = search_console_url

        self.tabs = ["Internal:All", "Internal:HTML", "Internal:JavaScript", "Internal:CSS", "Internal:images",
                      "Internal:PDF", "Internal:Flash", "Internal:Other", "Internal:Unknown", "External:All",
                      "External:HTML", "External:JavaScript", "External:CSS", "External:images", "External:PDF",
                      "External:Flash", "External:Other", "External:Unknown", "Protocol:All", "Protocol:HTTP",
                      "Protocol:HTTPS", "Response Codes:All", "Response Codes:Blocked by Robots.txt",
                      "Response Codes:Blocked Resource", "Response Codes:No Response", "Response Codes:Success (2xx)",
                      "Response Codes:Redirection (3xx)", "Response Codes:Redirection (JavaScript)",
                      "Response Codes:Redirection (Meta Refresh)", "Response Codes:Client Error (4xx)",
                      "Response Codes:Server Error (5xx)", "URL:All", "URL:Non ASCII Characters", "URL:Underscores",
                      "URL:Uppercase", "URL:Duplicate", "URL:Parameters", "URL:Over X Characters", "Page Titles:All",
                      "Page Titles:Missing", "Page Titles:Duplicate", "Page Titles:Over X Characters",
                      "Page Titles:Below X Characters", "Page Titles:Over X pixels", "Page Titles:Below X pixels",
                      "Page Titles:Same as H1", "Page Titles:Multiple", "Meta Description:All",
                      "Meta Description:Missing", "Meta Description:Duplicate", "Meta Description:Over X Characters",
                      "Meta Description:Below X Characters", "Meta Description:Over X Pixels",
                      "Meta Description:Below X Pixels", "Meta Description:Multiple",
                      "Meta Keywords:All", "Meta Keywords:Missing", "Meta Keywords:Duplicate", "Meta Keywords:Multiple",
                      "H1:All", "H1:Missing", "H1:Duplicate", "H1:Over X Characters", "H1:Multiple", "H2:All", "H2:Missing",
                      "H2:Duplicate", "H2:Over X Characters", "H2:Multiple", "Images:All", "Images:Over X KB",
                      "Images:Missing Alt Text", "Images:Alt Text over X Characters", "Canonicals:All",
                      "Canonicals:Contains Canonical", "Canonicals:Self Referencing", "Canonicals:Canonicalised",
                      "Canonicals:Missing", "Canonicals:Multiple", "Canonicals:Non-Indexable Canonical",
                      "Hreflang:All", "Hreflang:Contains hreflang", "Hreflang:Non-200 hreflang URLs",
                      "Hreflang:Unlinked hreflang URLs", "Hreflang:Missing Confirmation Links",
                      "Hreflang:Inconsistent Language & Region Confirmation Links",
                      "Hreflang:Non-Canonical Confirmation Links", "Hreflang:Noindex Confirmation Links",
                      "Hreflang:Incorrect Language & Region Codes", "Hreflang:Multiple Entries",
                      "Hreflang:Missing Self Reference",
                      "Hreflang:Not Using Canonical", "Hreflang:Missing X-Default", "Hreflang:Missing", "AJAX:All",
                      "AJAX:With Hash Fragment", "AJAX:Without Hash Fragment", "AMP:All", "AMP:Non-200 Response",
                      "AMP:Non-Confirming Canonical", "AMP:Missing Non-AMP Canonical", "AMP:Non-Indexable Canonical",
                      "AMP:Indexable", "AMP:Non-Indexable", "AMP:Missing <html amp> Tag",
                      "AMP:Missing/invalid <!doctype html> Tag",
                      "AMP:Missing <body> Tag", "AMP:Missing <head> Tag", "AMP:Missing Canonical",
                      "AMP:Missing/invalid <meta charset> Tag",
                      "AMP:Missing/invalid <meta viewport> Tag", "AMP:Missing/invalid AMP Script",
                      "AMP:Missing/invalid AMP Boilerplate", "AMP:Contains Disallowed HTML",
                      "AMP:Other Validation Errors",
                      "Structured Data:All", "Structured Data:Contains Structured Data",
                      "Structured Data:Missing Structured Data",
                      "Structured Data:Validation Errors", "Structured Data:Validation Warnings",
                      "Structured Data:Parse Errors",
                      "Structured Data:Microdata URLs", "Structured Data:JSON-LD URLs", "Structured Data:RDFa URLs",
                      "Sitemaps:All", "Sitemaps:URLs in Sitemap", "Sitemaps:URLs not in Sitemap", "Sitemaps:Orphan URLs",
                      "Sitemaps:Non-Indexable URLs in Sitemap", "Sitemaps:URLs in Multiple Sitemaps",
                      "Sitemaps:XML Sitemap with over 50k URLs", "Sitemaps:XML Sitemap over 50MB", "Analytics:All",
                      "Analytics:Sessions Above 0", "Analytics:No GA Data",
                      "Analytics:Non-Indexable with GA Data", "Analytics:Orphan URLs", "Search Console:All",
                      "Search Console:Clicks Above 0", "Search Console:No GSC Data",
                      "Search Console:Non-Indexable with GSC Data",
                      "Search Console:Orphan URLs", "Link Metrics:All"]

                        # "Analytics:Bounce Rate Above 70%",

    def run_screamer(self):
        os.system("/Applications/Screaming\ Frog\ SEO\ Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher "
                      "--crawl {} "
                      "--config /Users/theovandersluijs/PycharmProjects/seowork/data/crawl.seospiderconfig "
                      "--headless --save-crawl --overwrite  "
                      "--use-google-search-console prive {} "
                      "--output-folder {}/crawl/ "
                      "--save-report 'Crawl Overview' "
                      "--export-tabs '{}' "
                      "--export-format 'csv'".format(self.url, self.search_console_url, self.folder, ','.join(map(str, self.tabs))))

# --use-google-analytics [google account] [account] [property] [view] [segment]


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(dir_path, "../data")

    for domain in os.listdir(folder):
        if domain is 'ORGS':
            continue
        domain_folder = os.path.join(folder, domain)
        config_file = os.path.join(domain_folder, "config.yml")

        if not os.path.isfile(config_file):
            continue

        c = readConfig(config_file)

        url = c.config['url']
        domain = c.config['domain']
        search_console_url = c.config['search_console_url']

        s = Screaming(domain_folder, url, search_console_url)
        s.run_screamer()


# "Directives:All","Directiv
# es:Index","Directives:Noindex","Directives:Follow","Directives:Nofollow",
#         "Directives:None","Directives:NoArcH1ve","Directives:NoSnippet","Directives:NoODP","Directives:NoYDlR",
#         "Directives:NoImageIndex","Directives:NoTranslate","Directives:Unavailable_After","Directives:Refresh",

# "Pagination:All","Pagination:Contains Pagination",
#         "Pagination:First Page","Pagination:Paginated 2+ Pages","Pagination:Pagination URL Not In Anchor Tag",
#         "Pagination:Non-200 Pagination URLs","Pagination:Unlinked Pagination URLs","Pagination:Non-Indexable",
#         "Pagination:Multiple Pagination URLs","Pagination:Pagination Loop","Pagination:Sequence Error",



"""
Internal:All 
Internal:HTML 
Internal:JavaScript 
Internal:CSS 
Internal:images 
Internal:PDF 
Internal:Flash 
Internal:Other 
Internal:Unknown 
External:All 
External:HTML 
External:JavaScript 
External:CSS 
External:images 
External:PDF 
External:Flash 
External:Other 
External:Unknown 
Protocol:All 
Protocol:HTTP 
Protocol:HTTPS 
Response Codes:All 
Response Codes:Blocked by Robots.txt 
Response Codes:Blocked Resource 
Response Codes:No Response 
Response Codes:Success (2xx) 
Response Codes:Redirection (3xx) 
Response Codes:Redirection (JavaScript) 
Response Codes:Redirection (Meta Refresh) 
Response Codes:Client Error (4xx) 
Response Codes:Server Error (5xx) 
URL:All 
URL:Non ASCII Characters 
URL:Underscores 
URL:Uppercase 
URL:Duplicate 
URL:Parameters 
URL:Over X Characters 
Page Titles:All 
Page Titles:Missing 
Page Titles:Duplicate 
Page Titles:Over X Characters 
Page Titles:Below X Characters 
Page Titles:Over X pixels 
Page Titles:Below X pixels 
Page Titles:Same as H1 
Page Titles:Multiple 
Meta Description:All 
Meta Description:Missing 
Meta Description:Duplicate 
Meta Description:Over X Characters 
Meta Description:Below X Characters 
Meta Description:Over X Pixels 
Meta Description:Below X Pixels 
Meta Description:Multiple 
Meta Keywords:All 
Meta Keywords:Missing 
Meta Keywords:Duplicate 
Meta Keywords:Multiple 
H1:All 
H1:Missing 
H1:Duplicate 
H1:Over X Characters 
H1:Multiple 
H2:All 
H2:Missing 
H2:Duplicate 
H2:Over X Characters 
H2:Multiple 
Images:All 
Images:Over X KB 
Images:Missing Alt Text 
Images:Alt Text over X Characters 
Canonicals:All 
Canonicals:Contains Canonical 
Canonicals:Self Referencing 
Canonicals:Canonicalised 
Canonicals:Missing 
Canonicals:Multiple 
Canonicals:Non-Indexable Canonical 
Pagination:All 
Pagination:Contains Pagination 
Pagination:First Page 
Pagination:Paginated 2+ Pages 
Pagination:Pagination URL Not In Anchor Tag 
Pagination:Non-200 Pagination URLs 
Pagination:Unlinked Pagination URLs 
Pagination:Non-Indexable 
Pagination:Multiple Pagination URLs 
Pagination:Pagination Loop 
Pagination:Sequence Error 
Directives:All 
Directives:Index 
Directives:Noindex 
Directives:Follow 
Directives:Nofollow 
Directives:None 
Directives:NoArcH1ve 
Directives:NoSnippet 
Directives:NoODP 
Directives:NoYDlR 
Directives:NoImageIndex 
Directives:NoTranslate 
Directives:Unavailable_After 
Directives:Refresh 
Hreflang:All 
Hreflang:Contains hreflang 
Hreflang:Non-200 hreflang URLs 
Hreflang:Unlinked hreflang URLs 
Hreflang:Missing Confirmation Links 
Hreflang:Inconsistent Language & Region Confirmation Links
Hreflang:Non-Canonical Confirmation Links 
Hreflang:Noindex Confirmation Links 
Hreflang:Incorrect Language & Region Codes 
Hreflang:Multiple Entries 
Hreflang:Missing Self Reference 
Hreflang:Not Using Canonical 
Hreflang:Missing X-Default 
Hreflang:Missing 
AJAX:All
AJAX:With Hash Fragment 
AJAX:Without Hash Fragment 
AMP:All 
AMP:Non-200 Response 
AMP:Non-Confirming Canonical 
AMP:Missing Non-AMP Canonical 
AMP:Non-Indexable Canonical 
AMP:Indexable 
AMP:Non-Indexable 
AMP:Missing <html amp> Tag 
AMP:Missing/invalid <!doctype html> Tag 
AMP:Missing <body> Tag 
AMP:Missing <head> Tag 
AMP:Missing Canonical 
AMP:Missing/invalid <meta charset> Tag 
AMP:Missing/invalid <meta viewport> Tag 
AMP:Missing/invalid AMP Script 
AMP:Missing/invalid AMP Boilerplate 
AMP:Contains Disallowed HTML 
AMP:Other Validation Errors 
Structured Data:All 
Structured Data:Contains Structured Data 
Structured Data:Missing Structured Data 
Structured Data:Validation Errors 
Structured Data:Validation Warnings 
Structured Data:Parse Errors 
Structured Data:Microdata URLs 
Structured Data:JSON-LD URLs 
Structured Data:RDFa URLs 
Sitemaps:All 
Sitemaps:URLs in Sitemap 
Sitemaps:URLs not in Sitemap 
Sitemaps:Orphan URLs 
Sitemaps:Non-Indexable URLs in Sitemap 
Sitemaps:URLs in Multiple Sitemaps 
Sitemaps:XML Sitemap with over 50k URLs 
Sitemaps:XML Sitemap over 50MB 
Analytics:All 
Analytics:Sessions Above 0 
Analytics:Bounce Rate Above 70% 
Analytics:No GA Data 
Analytics:Non-Indexable with GA Data 
Analytics:Orphan URLs 
Search Console:All 
Search Console:Clicks Above 0 
Search Console:No GSC Data 
Search Console:Non-Indexable with GSC Data 
Search Console:Orphan URLs 
Link Metrics:All 
"""