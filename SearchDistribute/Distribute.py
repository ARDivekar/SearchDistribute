from SearchDistribute.Search import GoogleSearch
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.SearchExtractorErrors import InvalidSearchParameterException


class Distribute:
    ''' Each distribute object runs one query string, across multiple *Search objects (each of which have identical parameters).
        It essentially runs a 'map' function, distributing the fetching of the results of the query across several workers (*Search objects).
    '''
    search_engine = ""          ## A string of the search engine to use, must be present in SearchDistribute.Enums.SearchEngines
    query_str = ""              ## The query string
    num_workers = -1            ## (optional, defaults to 1) The number of workers we instantiate and assign to fetch parts of the total result set.
    num_results = -1            ## The total number of results we want for the query.
    num_results_per_page =- 1   ## The number of results per SERP
    save_to_db = False          ## Whether to save the results in an SQLite database or not
    results_db_config = {}      ## A hashtable with these fields: db_path, db_table. See Search.py for how they are handled.
                                    ## The path (relative or otherwise) to the SQLite database file.
                                    ## The table of the SQLite database in which to save the results.
    proxy_browser_config = {}   ## A hashtable with these fields: proxy_browser_type, proxy_args. See Search.py for how they are handled.


    def __init__(self, config):
        get_default_if_not_found_in_config = lambda config_key, default: config.get(config_key) if config.get(config_key) is not None else default  ## Optional parameters
        self.search_engine = config.get("search_engine")
        if type(self.query_str) != type("") or len(self.query_str) == 0:
            raise InvalidSearchParameterException(self.search_engine, "search_engine", self.search_engine, "must be a non-empty string")
        if self.search_engine not in SearchEngines:
            raise InvalidSearchParameterException(self.search_engine, "search_engine", self.search_engine, "must exist in Enums.SearchEngines")

        self.query_str = config.get("query_str")
        if type(self.query_str) != type("") or len(self.query_str) == 0:
            raise InvalidSearchParameterException(self.search_engine, "query_str", self.query_str, "must be a non-empty string")

        ##  Check the optional params, and set to their default values if not passed in config:
        self.num_workers = get_default_if_not_found_in_config("num_workers", 1)
        if type(self.num_workers) != type(0) and self.num_workers <= 0:
            raise InvalidSearchParameterException(self.search_engine, "num_workers", self.num_workers, "must be an integer greater than zero")

        self.num_results = get_default_if_not_found_in_config("num_results", 10)
        if type(self.num_results) != type(0) and self.num_results <= 0:
            raise InvalidSearchParameterException(self.search_engine, "num_results", self.num_results, "must be an integer greater than zero")

        self.num_results_per_page = get_default_if_not_found_in_config("num_results_per_page", 10)
        if type(self.num_results_per_page) != type(0) and self.num_results_per_page <= 0:
            raise InvalidSearchParameterException(self.search_engine, "num_results_per_page", self.num_results_per_page, "must be an integer greater than zero")

        self.save_to_db = config.get("save_to_db")
        if self.save_to_db == True:
            self.results_db_config = config.get("results_db_config")
        else:
            self.results_db_config = None








