import sys
sys.path.append("..")
from SearchDistribute.Distribute import *

config = {
    "search_engine" : SearchEngines.Google,
    "country" : "IND",
    "query" : "site:nytimes.com | site:latimes.com | site:washingtonpost.com shiba inu",
    "num_workers" : 3,
    "num_results" : 300,
    "num_results_per_page" : 100,
    "cooldown_time" : 600,
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

d = Distribute(config)
parsed_serps = d.start()