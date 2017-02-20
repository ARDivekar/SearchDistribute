from SearchDistribute.SearchQuery import GoogleSearchQuery
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.Enums import ProxyBrowsers
from SearchDistribute.SearchExtractorErrors import *

class SearchTemplate(object):
    search_engine = ""
    def __init__(self, search_engine):
        self.search_engine = search_engine

    def list_websites_with_top_level_domain(self, top_level_domain):
        query = GoogleSearchQuery(config={"top_level_domains": [top_level_domain], "necessary_topics":[" "]}).generate_query()

''' A *Search object (GoogleSearch, BingSearch etc.) offers an abstraction for retrieving search results for a particular query, and optionally saving them in a database.
    Each *Search object is a worker, waiting for the input query string, and it retrieves SERPs (Search Result Pages). Between searches, it idles in memory. It may be reused for multiple searches, with a sufficient cooldown period so as to not trigger IP blocking from the search engine.
    Rules:
     [1] Each *Search object runs in its own process/thread.

     [2] Each *Search object is tied to a single browser instance for the duration of its existence (the browser instance may be refreshed).

     [3] It's `config` consists of fields which should not be modified during the object's lifetime:
          (a) proxy_browser_type    : a string, taken from `SearchDistribute.Enums.ProxyBrowsers`
          (b) (optional) proxy_args : a dictionary {'proxy_type':"xyz", 'hostname':"xyz", 'port':"xyz", 'username':"xyz", 'password':"xyz"}
              - proxy_type : a string e.g. "Socks5", "HTTP" taken from `SearchDistribute.Enums.ProxyTypes`.
              - hostname   : a string of the IP address or host url of the proxy server. e.g. "proxy-nl.privateinternetaccess.com"
              - port       : a string of the port at which to access the proxy server.
              - (optional) username : the username used for authentication, e.g. Socks5 authentication.
              - (optional) password : the password used for authentication, e.g. Socks5 authentication.
          (c) (optional) db_name    : a string, for the SQLite database name in which to save the results.
          (d) (optional) db_table   : a string, for the SQLite database table name in which to save the results.

     [4] To actually search and retrieve results, the search query must be passed explicitly to the `search(...)` function, along with an optional offset and number of results in the SERP.
'''
class GoogleSearch(SearchTemplate):
    search_engine = SearchEngines.Google
    proxy_browser_type = ""             ## taken from SearchDistribute.Enums.ProxyBrowsers
    browser = None
    search_query = ""
    time_of_last_retrieved_query = 0    ## Seconds since UNIX epoch

    def __init__(self, config={}):
        self.proxy_browser_type = config.get("proxy_browser_type")
        # if self.proxy_browser_type == None or :






