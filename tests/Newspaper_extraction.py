import sys
sys.path.append("..")
from SearchDistribute.Distribute import *
from SearchDistribute.SearchQuery import GoogleSearchQuery as GSQ
from datetime import date

query_obj = GSQ({
    "daterange": (date(2016, 1, 1), date(2017, 3, 10)),
    "in_url": "infosys",
    "necessary_sites":[
        'financialexpress.com/article/',
		'business-standard.com/article/',
		# 'livemint.com/companies',
		'timesofindia.indiatimes.com/business/india-business/',
		# 'articles.economictimes.indiatimes.com/', 'economictimes.indiatimes.com/markets/stocks/news/',
		# 'thehindubusinessline.com/markets/stock-markets/', 'thehindubusinessline.com/companies/'
    ]
})

config = {
    "search_engine" : SearchEngines.Google,
    "country" : "IND",
    "query" : query_obj.generate_query(),
    "num_workers" : 10,
    "num_results" : 3000,
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
print("Starting Newspaper Extraction:\n")
d.start()
