from SearchDistribute.Search import GoogleSearch
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.SearchExtractorErrors import InvalidSearchParameterException
from SearchDistribute.SearchExtractorErrors import MissingSearchParameterException
from SearchDistribute import Enums
import copy


class Distribute:
    ''' Each distribute object runs one query string on one search engine, across multiple *Search objects (each of which have identical parameters).
        It essentially runs a 'map' function, distributing the fetching of the results of the query across several workers (*Search objects).
    '''
    search_engine = ""          ## (optional, defaults to SearchEngines.Google) A string of the search engine to use, must be present in SearchDistribute.Enums.SearchEngines
    country = ""                ## (optional, defaults to "USA") The country where we want to search. Handled in Search.py
    query = ""                  ## The query string
    num_workers = -1            ## (optional, defaults to 1) The number of workers we instantiate and assign to fetch parts of the total result set.
    num_results = -1            ## (optional, defaults to 10) The total number of results we want for the query.
    num_results_per_page =- 1   ## (optional, defaults to 10) The number of results per SERP
    save_to_db = None           ## (optional, defaults to False) Whether to save the results in an SQLite database or not
    db_config = {}              ## (optional, defaults to None) A hashtable with these fields: db_path, db_table. See Search.py for how they are handled.
    proxy_browser_config = {}   ## A hashtable with these fields: proxy_browser_type, proxy_args. See ProxyBrowser.py for how they are handled.
    cooldown_time = -1          ## The time in seconds, that each worker MUST wait before it can fetch the next SERP. No more SERPs can be fetched before this time expires
    worker_heap = []            ## A min-heap of the *Search objects, organized by their `time_of_last_retrieved_query`. This allows us to choose the one which has cooled down the most


    def __init__(self, config):
        '''For all the parameters in `config`:
            - Necessary parameters:
                - If missing, raise a MissingSearchParameterException.
                - If present but in incorrect format, raise an InvalidSearchParameterException.
            - Optional parameters:
                - If missing, try to use the value from self.default_values().
                - If present but in incorrect format, raise an InvalidSearchParameterException.

        Example config with all parameters set:
        {
            "search_engine" : SearchEngines.Google,
            "country" : "USA",
            "query" : "site:nytimes.com corgi",
            "num_workers" : 1,
            "num_results" : 10,
            "num_results_per_page" : 10,
            "cooldown_time" : 300,
            "proxy_browser_config" : {
                "proxy_browser_type" : ProxyBrowsers.PhantomJS,
                "proxy_args" : {
                    "proxy_type" : Enums.ProxyTypes.Socks5,
                    "hostname" : "proxy-nl.privateinternetaccess.com",
                    "port" : "1080",
                    "username" : "x1237029",
                    "password" : "3iV3za46xD"
                }
            },
            "save_to_db" : True,
            "db_config" : {
                "db_path" : "./SearchResults.db",
                "db_table" : "GoogleSearchResults"
            }
        }
        '''
        get_default_if_not_found_in_config = lambda param_name: config.get(param_name) if config.get(param_name) is not None else self.default_values(param_name)

        ## Optional parameter `search_engine`
        self.search_engine = get_default_if_not_found_in_config("search_engine")
        if type(self.query) != type("") or len(self.query) == 0:    ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "search_engine", self.search_engine, "must be a non-empty string")

        ## Necessary parameter `query`
        self.query = get_default_if_not_found_in_config("query")
        if self.query == None:      ## will only run if the value is not present
            raise MissingSearchParameterException(self.search_engine, "query")
        if type(self.query) != type("") or len(self.query) == 0:    ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "query", self.query, "must be a non-empty string")

        ## Optional parameter `num_workers`
        self.num_workers = get_default_if_not_found_in_config("num_workers")
        if type(self.num_workers) != type(0) or self.num_workers <= 0:     ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "num_workers", self.num_workers, "must be an integer greater than zero")

        ## Optional parameter `num_results`
        self.num_results = get_default_if_not_found_in_config("num_results")
        if type(self.num_results) != type(0) or self.num_results <= 0:     ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "num_results", self.num_results, "must be an integer greater than zero")

        ## Optional parameter `num_results_per_page`
        self.num_results_per_page = get_default_if_not_found_in_config("num_results_per_page")
        if type(self.num_results_per_page) != type(0) or self.num_results_per_page <= 0:   ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "num_results_per_page", self.num_results_per_page, "must be an integer greater than zero")

        ## Optional parameter `cooldown_time`
        self.cooldown_time = get_default_if_not_found_in_config("cooldown_time")
        if type(self.cooldown_time) != type(0) or self.cooldown_time < 0:   ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "cooldown_time", self.cooldown_time, "must be an integer greater than or equal to zero")

        ## Optional parameter `save_to_db`
        self.save_to_db = get_default_if_not_found_in_config("save_to_db")
        if type(self.save_to_db) != type(False):
            raise InvalidSearchParameterException(self.search_engine, "save_to_db", self.save_to_db, "must be either True or false")

        if self.save_to_db == False:
            self.db_config = None
        else:
            ## Optional parameter `db_config`
            self.db_config = get_default_if_not_found_in_config("db_config")  ## checked in Search.py

        ## Optional parameter `proxy_browser_config`:
        self.proxy_browser_config = get_default_if_not_found_in_config("proxy_browser_config")  ## checked in ProxyBrowser.py



    def default_values(self, param):
        ## A concise set of defaults. Also update these values at the top of the function.
        default_config = {
            "search_engine" : SearchEngines.Google,
            "country" : "USA",
            "num_workers" : 1,
            "num_results" : 10,
            "num_results_per_page" : 10,
            "save_to_db" : False,
            "proxy_browser_config" : {"proxy_browser_type" : Enums.ProxyBrowsers.PhantomJS},
            "cooldown_time" : 300
        }
        return default_config.get(param)


    def spawn_worker(self):
        worker_config = {
            "country" : self.country,
            "proxy_browser_config" : self.proxy_browser_config,
            "save_to_db" : self.save_to_db,
            "db_config" : self.db_config
        }

        if self.search_engine == SearchEngines.Google:
            return GoogleSearch(worker_config)





