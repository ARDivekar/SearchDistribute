import sys
sys.path.append("..")
from SearchDistribute.Distribute import *

config = {
    "search_engine" : SearchEngines.Google,
    "country" : "IND",
    "num_workers" : 2,
    "num_results" : 30,
    "num_results_per_page" : 10,
    "cooldown_time" : 10,
    "proxy_browser_config" : {
        "proxy_browser_type" : Enums.ProxyBrowsers.PhantomJS,
        "proxy_args" : {
            "proxy_type" : Enums.ProxyTypes.Socks5,
            "hostname" : "proxy-nl.privateinternetaccess.com",
            "port" : 1080,
            "username" : "x0666788",
            "password" : "8wvvciCCdJ"
        }
    },
    "save_to_db" : True,
    "db_config" : {
        "db_path" : "./SearchResults.db",
        "db_table" : "GoogleSearchResults"
    }
}


d1 = Distribute(config)

# d1 = Distribute(config)
# d2 = Distribute(config)
# d3 = Distribute(config)
# print("START ALL")
# d1.start("einstien")
# d2.start("tesla")
# d3.start("curie")
# d1.finish()
# print("\n\nAFTER FINISHING 1st: %s result pages"%len(d1.get_results()))
# d2.finish()
# print("\n\nAFTER FINISHING 2nd: %s result pages"%len(d2.get_results()))
# d3.finish()
# print("\n\nAFTER FINISHING 3rd: %s result pages"%len(d3.get_results()))
# print("\nDONE WITH ALL")
