from SearchDistribute.Search import GoogleSearch
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.SearchExtractorErrors import InvalidSearchParameterException
from SearchDistribute.SearchExtractorErrors import MissingSearchParameterException
from SearchDistribute.SearchExtractorErrors import SERPPageLoadingException
from SearchDistribute import Enums
import time
import datetime

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
    workers = []  ## An array of the *Search objects. Their `time_of_last_retrieved_query` allows us to choose the one which has cooled down the most, to assign to fetch the next SERP.

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
                "proxy_browser_type" : Enums.ProxyBrowsers.PhantomJS,
                "proxy_args" : {
                    "proxy_type" : Enums.ProxyTypes.Socks5,
                    "hostname" : "proxy-nl.privateinternetaccess.com",
                    "port" : 1080,
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


        PARAMETERS CHECKED IN THIS FILE (Distribute.py):
         - search_engine
         - query
         - num_workers
         - num_results
         - num_results_per_page
         - cooldown_time
         - save_to_db

        PARAMETERS CHECKED OTHER FILES (Search.py, ProxyBrowser.py):
        '''

        get_default_if_not_found_in_config = lambda param_name: config.get(param_name) if config.get(param_name) is not None else self.default_values(param_name)

        ## Optional parameter `search_engine`
        self.search_engine = get_default_if_not_found_in_config("search_engine")
        if type(self.search_engine) != type("") or len(self.search_engine) == 0:    ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "search_engine", self.search_engine, "must be a non-empty string")

        ## Optional parameter `search_engine`, handled in Search.py
        self.country = config.get("country")

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
            ## Optional parameter `db_config`, handled in Search.py
            self.db_config = get_default_if_not_found_in_config("db_config")  ## checked in Search.py

        ## Optional parameter `proxy_browser_config`, handled in ProxyBrowser.py
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


    def _spawn_worker(self):     ## Can be extended to use multithreading or multiprocessing.
        worker_config = {
            "country" : self.country,
            "proxy_browser_config" : self.proxy_browser_config,
            "db_config" : self.db_config
        }

        if self.search_engine == SearchEngines.Google:
            return GoogleSearch(worker_config)


    def _get_index_of_coolest_worker(self):
        index_of_coolest_worker = -1
        time_of_last_retrieved_query_of_coolest_worker = time.time()
        for i in range(0, len(self.workers)):
            if self.workers[i].time_of_last_retrieved_query < time_of_last_retrieved_query_of_coolest_worker:
                index_of_coolest_worker = i
                time_of_last_retrieved_query_of_coolest_worker = self.workers[i].time_of_last_retrieved_query
        time_passed_since_last_fetched_from_coolest_worker = time.time() - self.workers[
            index_of_coolest_worker].time_of_last_retrieved_query
        return (index_of_coolest_worker, time_passed_since_last_fetched_from_coolest_worker)


    ## Ready, set, GO!
    def start(self):
        return self.distribute_query(self.query, self.num_results, self.num_workers, self.num_results_per_page, self.cooldown_time, self.save_to_db)

    def distribute_query(self, query, num_results, num_workers, num_results_per_page, cooldown_time, save_to_db):
        parsed_serps = []  ## an array of parsed SERPs
        print("\nStarting the %s search with query `%s`" % (self.search_engine, self.query))



        ## The first worker the stage for the other workers, getting the basic url which is then modified by each worker.
        worker = self._spawn_worker()
        basic_url = worker.perform_search_from_main_page(query, num_results_per_page)
        self.workers.append(worker)

        start_offset_so_far = 0
        for i in range(1, num_workers):
            worker = self._spawn_worker()
            parsed_serp = worker.get_SERP_results(basic_url, start_offset_so_far, num_results_per_page, save_to_db)
            if parsed_serp is None:
                raise SERPPageLoadingException(self.search_engine,
                                               self.proxy_browser_config.get("proxy_browser_type"),
                                               url = worker._update_url_number_of_results_per_page(worker._update_url_start(basic_url, start_offset_so_far), num_results_per_page))
            parsed_serps.append(parsed_serp)
            start_offset_so_far += parsed_serps[-1].num_results
            print("Results %s-%s\n%s\n\n" % (start_offset_so_far-parsed_serps[-1].num_results, start_offset_so_far, parsed_serps[-1].results))
            self.workers.append(worker)     ## Can be extended to use multithreading or multiprocessing.

        num_completed = start_offset_so_far

        while num_completed < num_results:
            index_of_coolest_worker, time_passed_since_last_fetched_from_coolest_worker = self._get_index_of_coolest_worker()
            if time_passed_since_last_fetched_from_coolest_worker < cooldown_time:
                sleep_for = cooldown_time - time_passed_since_last_fetched_from_coolest_worker ## Sleep for the remaining time.
                now = datetime.datetime.now()
                wakeup_datetime = now + datetime.timedelta(seconds=sleep_for) ## Source: http://stackoverflow.com/a/3240493/4900327
                time_str = "%s-%s-%s %s:%s:%s"%(wakeup_datetime.year, wakeup_datetime.month, wakeup_datetime.day, wakeup_datetime.hour, wakeup_datetime.minute, wakeup_datetime.second)
                print("<-----All workers need to cooldown, sleeping till: %s----->" % time_str)
                time.sleep(sleep_for)
            parsed_serps.append(
                self.workers[index_of_coolest_worker].get_SERP_results(
                    basic_url, num_completed, num_results_per_page, save_to_db))
            num_completed += parsed_serps[-1].num_results
            print("Results %s-%s\n%s\n\n" % (num_completed-parsed_serps[-1].num_results, num_completed, parsed_serps[-1].results))

        return parsed_serps












