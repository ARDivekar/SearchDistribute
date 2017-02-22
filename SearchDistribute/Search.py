from SearchDistribute.SearchQuery import GoogleSearchQuery
from SearchDistribute.Enums import SearchEngines
from SearchDistribute import Enums
from SearchDistribute.SearchExtractorErrors import *
from SearchDistribute import ProxyBrowser
from SearchDistribute.SERPParser import GoogleParser
import time
import json
import re
from selenium.webdriver.common.keys import Keys
import urllib

class SearchTemplate(object):
    search_engine = ""
    def __init__(self, search_engine):
        self.search_engine = search_engine

''' A *Search object (GoogleSearch, BingSearch etc.) offers an abstraction for retrieving search results for a particular query, and optionally saving them in a database.
    Each *Search object is a worker, waiting for the input query string, and it retrieves SERPs (Search Result Pages). Between searches, it idles in memory. It may be reused for multiple searches, with a sufficient cooldown period so as to not trigger IP blocking from the search engine.
    Rules:
     [1] Each *Search object runs in its own process/thread.

     [2] Each *Search object is tied to worker_configa single browser instance for the duration of its existence (the browser instance may be refreshed).

     [3] It's `config` consists of fields which should not be modified during the object's lifetime:
          (a) proxy_browser_type    : a string, taken from `Enums.ProxyBrowsers`
          (b) (optional) proxy_args : a dictionary {'proxy_type':"xyz", 'hostname':"xyz", 'port':"xyz", 'username':"xyz", 'password':"xyz"}
              - proxy_type : a string e.g. "Socks5", "HTTP" taken from `Enums.ProxyTypes`.
              - hostname   : a string of the IP address or host url of the proxy server. e.g. "proxy-nl.privateinternetaccess.com"
              - port       : a string of the port at which to access the proxy server.
              - (optional) username : the username used for authentication, e.g. Socks5 authentication.
              - (optional) password : the password used for authentication, e.g. Socks5 authentication.
          (c) (optional) db_name  : a string, for the SQLite database name in which to save the results.
          (d) (optional) db_table : a string, for the SQLite database table name in which to save the results.
          (e) (optional) country  : a string, for country where we search. By default it is USA. This is translated to the country where we search.

     [4] To actually search and retrieve results, the search query must be passed explicitly to the `search(...)` function, along with an optional offset and number of results in the SERP.
'''


class GoogleSearch(SearchTemplate):
    search_engine = SearchEngines.Google    ## must be from SearchDistribute.Enums.SearchEngines
    proxy_browser_type = "" ## The type of proxy browser, must be from Enums.ProxyBrowsers
    proxy_args = {}         ## (optional, defaults to None) A hashtable with the following values: proxy_type, hostname, port, username, password. See ProxyBrowser.py to find out how they are handled.
    country = ""            ## (optional, defaults to "USA") Either a Country Name,  ISO ALPHA-2 Code,  ISO ALPHA-3 Code, or ISO Numeric Code UN M49 Numerical Code
    domain = ""             ## (defaults to 'https://www.google.com' when country is 'USA') The base domain on which we try to search, e.g. "https://www.google.com". This may not be the actual domain where the results are retrieved from, due to query forwarding etc.
    db_config = {}          ## (optional, defaults to None) A hashtable with these fields: db_path, db_table.
                            ##  - db_path : The path (relative or otherwise) to the SQLite database file.
                            ##  - db_table : The table of the SQLite database in which to save the results.
    time_of_last_retrieved_query = 0    ## The time in seconds (float) since UNIX epoch, when a page was visited.
    possible_num_results_per_page = [10, 20, 30, 40, 50, 100]
    default_num_results_per_page = 10
    browser = None

    def __init__(self, config):
        '''
        The logic in this function is that: no parameter of the config should be None. Every parameter should have its default value, or a value passed by the user. It is upto this function to check whether the value passed is correct or not.

        Example config with all parameters set:
        {
            "country" : "USA",
            "proxy_browser_config" : {
                "proxy_browser_type" : Enums.ProxyBrowsers.PhantomJS,
                "proxy_args" : {
                    "proxy_type" : Enums.ProxyTypes.Socks5,
                    "hostname" : "proxy-nl.privateinternetaccess.com",
                    "port" : "1080",
                    "username" : "x1237029",
                    "password" : "3iV3za46xD"
                }
            },
            "db_config" : {
                "db_path" : "./SearchResults.db",
                "db_table" : "GoogleSearchResults"
            }
        }
        '''

        ## Optional parameter `country`, will not be None, defaults to "USA":
        self.country = config.get("country")
        if type(self.country) != type("") or len(self.country) == 0:  ## will only run if the value is present, but in the wrong format.
            raise InvalidSearchParameterException(self.search_engine, "country", self.country, "must be a non-empty string")

        self.domain = self.get_country_domain(self.country)  ## defaults to 'https://www.google.com' when the country defaults to "USA"

        ## Optional parameter `proxy_browser_config`, will not be None, defaults to {"proxy_browser_type" : Enums.ProxyBrowsers.PhantomJS}
        proxy_browser_config = config.get("proxy_browser_config")

        self.proxy_browser_type = proxy_browser_config.get("proxy_browser_type")    ## Defaults to Enums.ProxyBrowsers.PhantomJS
        if self.proxy_browser_type not in Enums.ProxyBrowsers:
            raise UnsupportedProxyBrowserException(self.proxy_browser_type)

        self.proxy_args = proxy_browser_config.get("proxy_args")                    ## Defaults to None

        ## Instantiate browser:
        if self.proxy_browser_type == Enums.ProxyBrowsers.PhantomJS:  ## We are equating stings. See Enums.py and /tests/EnumTests.py
            self.browser = ProxyBrowser.PhantomJS(self.proxy_args)

        ## Optional parameter `db_config`, defaults to None
        self.db_config = config.get("db_config")

        print("Spawned %s worker with id : %s. Detected proxy details from `%s`:\n%s"%(self.__class__.__name__, id(self), self.browser.detected_proxy_details.get("proxy_detection_website"), json.dumps(self.browser.detected_proxy_details, sort_keys=True, indent=2)))    ## Source: http://stackoverflow.com/a/3314411/4900327


    def get_country_domain(self, country):
        domain = ""
        ## Source: https://www.wikiwand.com/en/List_of_Google_domains and http://www.nationsonline.org/oneworld/country_code_list.htm
        ## In order: [Country Name,  ISO ALPHA-2 CODE,  ISO ALPHA-3 CODE, ISO Numeric Code UN M49 Numerical Code]
        if   str(country) in ['Afghanistan', 'AF', 'AFG', '004']: domain = 'google.com.af'
        elif str(country) in ['Albania', 'AL', 'ALB', '008']: domain = 'google.al'
        elif str(country) in ['Algeria', 'DZ', 'DZA', '012']: domain = 'google.dz'
        elif str(country) in ['American Samoa', 'AS', 'ASM', '016']: domain = 'google.as'
        elif str(country) in ['Andorra', 'AD', 'AND', '020']: domain = 'google.ad'
        elif str(country) in ['Angola', 'AO', 'AGO', '024']: domain = 'google.co.ao'
        elif str(country) in ['Anguilla', 'AI', 'AIA', '660']: domain = 'google.com.ai'
        elif str(country) in ['Antigua and Barbuda', 'AG', 'ATG', '028']: domain = 'google.com.ag'
        elif str(country) in ['Argentina', 'AR', 'ARG', '032']: domain = 'google.com.ar'
        elif str(country) in ['Armenia', 'AM', 'ARM', '051']: domain = 'google.am'
        elif str(country) in ['Australia', 'AU', 'AUS', '036']: domain = 'google.com.au'
        elif str(country) in ['Austria', 'AT', 'AUT', '040']: domain = 'google.at'
        elif str(country) in ['Azerbaijan', 'AZ', 'AZE', '031']: domain = 'google.az'
        elif str(country) in ['Bahamas', 'BS', 'BHS', '044']: domain = 'google.bs'
        elif str(country) in ['Bahrain', 'BH', 'BHR', '048']: domain = 'google.com.bh'
        elif str(country) in ['Bangladesh', 'BD', 'BGD', '050']: domain = 'google.com.bd'
        elif str(country) in ['Belarus', 'BY', 'BLR', '112']: domain = 'google.by'
        elif str(country) in ['Belgium', 'BE', 'BEL', '056']: domain = 'google.be'
        elif str(country) in ['Belize', 'BZ', 'BLZ', '084']: domain = 'google.com.bz'
        elif str(country) in ['Benin', 'BJ', 'BEN', '204']: domain = 'google.bj'
        elif str(country) in ['Bhutan', 'BT', 'BTN', '064']: domain = 'google.bt'
        elif str(country) in ['Bolivia', 'BO', 'BOL', '068']: domain = 'google.com.bo'
        elif str(country) in ['Bosnia and Herzegovina', 'BA', 'BIH', '070']: domain = 'google.ba'
        elif str(country) in ['Botswana', 'BW', 'BWA', '072']: domain = 'google.co.bw'
        elif str(country) in ['Brazil', 'BR', 'BRA', '076']: domain = 'google.com.br'
        elif str(country) in ['British Indian Ocean Territory', 'IO', 'IOT', '086']: domain = 'google.io'
        elif str(country) in ['British Virgin Islands', 'VG', 'VGB', '092']: domain = 'google.vg'
        elif str(country) in ['Bulgaria', 'BG', 'BGR', '100']: domain = 'google.bg'
        elif str(country) in ['Burkina Faso', 'BF', 'BFA', '854']: domain = 'google.bf'
        elif str(country) in ['Burundi', 'BI', 'BDI', '108']: domain = 'google.bi'
        elif str(country) in ['Cambodia', 'KH', 'KHM', '116']: domain = 'google.com.kh'
        elif str(country) in ['Cameroon', 'CM', 'CMR', '120']: domain = 'google.cm'
        elif str(country) in ['Canada', 'CA', 'CAN', '124']: domain = 'google.ca'
        elif str(country) in ['Cape Verde', 'CV', 'CPV', '132']: domain = 'google.cv'
        elif str(country) in ['Central African Republic', 'CF', 'CAF', '140']: domain = 'google.cf'
        elif str(country) in ['Chad', 'TD', 'TCD', '148']: domain = 'google.td'
        elif str(country) in ['Chile', 'CL', 'CHL', '152']: domain = 'google.cl'
        elif str(country) in ['China', 'CN', 'CHN', '156']: domain = 'google.cn'
        elif str(country) in ['Christmas Island', 'CX', 'CXR', '162']: domain = 'google.cx'
        elif str(country) in ['Cocos (Keeling) Islands', 'CC', 'CCK', '166']: domain = 'google.cc'
        elif str(country) in ['Colombia', 'CO', 'COL', '170']: domain = 'google.com.co'
        elif str(country) in ['Cook Islands', 'CK', 'COK', '184']: domain = 'google.co.ck'
        elif str(country) in ['Costa Rica', 'CR', 'CRI', '188']: domain = 'google.co.cr'
        elif str(country) in ['Croatia', 'HR', 'HRV', '191']: domain = 'google.hr'
        elif str(country) in ['Cuba', 'CU', 'CUB', '192']: domain = 'google.com.cu'
        elif str(country) in ['Cyprus', 'CY', 'CYP', '196']: domain = 'google.com.cy'
        elif str(country) in ['Czech Republic', 'CZ', 'CZE', '203']: domain = 'google.cz'
        elif str(country) in ['Denmark', 'DK', 'DNK', '208']: domain = 'google.dk'
        elif str(country) in ['Djibouti', 'DJ', 'DJI', '262']: domain = 'google.dj'
        elif str(country) in ['Dominica', 'DM', 'DMA', '212']: domain = 'google.dm'
        elif str(country) in ['Dominican Republic', 'DO', 'DOM', '214']: domain = 'google.com.do'
        elif str(country) in ['Ecuador', 'EC', 'ECU', '218']: domain = 'google.com.ec'
        elif str(country) in ['Egypt', 'EG', 'EGY', '818']: domain = 'google.com.eg'
        elif str(country) in ['El Salvador', 'SV', 'SLV', '222']: domain = 'google.com.sv'
        elif str(country) in ['Estonia', 'EE', 'EST', '233']: domain = 'google.ee'
        elif str(country) in ['Ethiopia', 'ET', 'ETH', '231']: domain = 'google.com.et'
        elif str(country) in ['Fiji', 'FJ', 'FJI', '242']: domain = 'google.com.fj'
        elif str(country) in ['Finland', 'FI', 'FIN', '246']: domain = 'google.fi'
        elif str(country) in ['France', 'FR', 'FRA', '250']: domain = 'google.fr'
        elif str(country) in ['French Guiana', 'GF', 'GUF', '254']: domain = 'google.gf'
        elif str(country) in ['Gabon', 'GA', 'GAB', '266']: domain = 'google.ga'
        elif str(country) in ['Gambia', 'GM', 'GMB', '270']: domain = 'google.gm'
        elif str(country) in ['Georgia', 'GE', 'GEO', '268']: domain = 'google.ge'
        elif str(country) in ['Germany', 'DE', 'DEU', '276']: domain = 'google.de'
        elif str(country) in ['Ghana', 'GH', 'GHA', '288']: domain = 'google.com.gh'
        elif str(country) in ['Gibraltar', 'GI', 'GIB', '292']: domain = 'google.com.gi'
        elif str(country) in ['Greece', 'GR', 'GRC', '300']: domain = 'google.gr'
        elif str(country) in ['Greenland', 'GL', 'GRL', '304']: domain = 'google.gl'
        elif str(country) in ['Guadeloupe', 'GP', 'GLP', '312']: domain = 'google.gp'
        elif str(country) in ['Guatemala', 'GT', 'GTM', '320']: domain = 'google.com.gt'
        elif str(country) in ['Guernsey', 'GG', 'GGY', '831']: domain = 'google.gg'
        elif str(country) in ['Guyana', 'GY', 'GUY', '328']: domain = 'google.gy'
        elif str(country) in ['Haiti', 'HT', 'HTI', '332']: domain = 'google.ht'
        elif str(country) in ['Honduras', 'HN', 'HND', '340']: domain = 'google.hn'
        elif str(country) in ['Hungary', 'HU', 'HUN', '348']: domain = 'google.hu'
        elif str(country) in ['Iceland', 'IS', 'ISL', '352']: domain = 'google.is'
        elif str(country) in ['India', 'IN', 'IND', '356']: domain = 'google.co.in'
        elif str(country) in ['Indonesia', 'ID', 'IDN', '360']: domain = 'google.co.id'
        elif str(country) in ['Iraq', 'IQ', 'IRQ', '368']: domain = 'google.iq'
        elif str(country) in ['Ireland', 'IE', 'IRL', '372']: domain = 'google.ie'
        elif str(country) in ['Isle of Man', 'IM', 'IMN', '833']: domain = 'google.im'
        elif str(country) in ['Israel', 'IL', 'ISR', '376']: domain = 'google.co.il'
        elif str(country) in ['Italy', 'IT', 'ITA', '380']: domain = 'google.it'
        elif str(country) in ['Jamaica', 'JM', 'JAM', '388']: domain = 'google.com.jm'
        elif str(country) in ['Japan', 'JP', 'JPN', '392']: domain = 'google.co.jp'
        elif str(country) in ['Jersey', 'JE', 'JEY', '832']: domain = 'google.je'
        elif str(country) in ['Jordan', 'JO', 'JOR', '400']: domain = 'google.jo'
        elif str(country) in ['Kazakhstan', 'KZ', 'KAZ', '398']: domain = 'google.kz'
        elif str(country) in ['Kenya', 'KE', 'KEN', '404']: domain = 'google.co.ke'
        elif str(country) in ['Kiribati', 'KI', 'KIR', '296']: domain = 'google.ki'
        elif str(country) in ['Kuwait', 'KW', 'KWT', '414']: domain = 'google.com.kw'
        elif str(country) in ['Kyrgyzstan', 'KG', 'KGZ', '417']: domain = 'google.kg'
        elif str(country) in ['Latvia', 'LV', 'LVA', '428']: domain = 'google.lv'
        elif str(country) in ['Lebanon', 'LB', 'LBN', '422']: domain = 'google.com.lb'
        elif str(country) in ['Lesotho', 'LS', 'LSO', '426']: domain = 'google.co.ls'
        elif str(country) in ['Libya', 'LY', 'LBY', '434']: domain = 'google.com.ly'
        elif str(country) in ['Liechtenstein', 'LI', 'LIE', '438']: domain = 'google.li'
        elif str(country) in ['Lithuania', 'LT', 'LTU', '440']: domain = 'google.lt'
        elif str(country) in ['Luxembourg', 'LU', 'LUX', '442']: domain = 'google.lu'
        elif str(country) in ['Madagascar', 'MG', 'MDG', '450']: domain = 'google.mg'
        elif str(country) in ['Malawi', 'MW', 'MWI', '454']: domain = 'google.mw'
        elif str(country) in ['Malaysia', 'MY', 'MYS', '458']: domain = 'google.com.my'
        elif str(country) in ['Maldives', 'MV', 'MDV', '462']: domain = 'google.mv'
        elif str(country) in ['Mali', 'ML', 'MLI', '466']: domain = 'google.ml'
        elif str(country) in ['Malta', 'MT', 'MLT', '470']: domain = 'google.com.mt'
        elif str(country) in ['Mauritius', 'MU', 'MUS', '480']: domain = 'google.mu'
        elif str(country) in ['Mexico', 'MX', 'MEX', '484']: domain = 'google.com.mx'
        elif str(country) in ['Moldova', 'MD', 'MDA', '498']: domain = 'google.md'
        elif str(country) in ['Mongolia', 'MN', 'MNG', '496']: domain = 'google.mn'
        elif str(country) in ['Montenegro', 'ME', 'MNE', '499']: domain = 'google.me'
        elif str(country) in ['Montserrat', 'MS', 'MSR', '500']: domain = 'google.ms'
        elif str(country) in ['Morocco', 'MA', 'MAR', '504']: domain = 'google.co.ma'
        elif str(country) in ['Mozambique', 'MZ', 'MOZ', '508']: domain = 'google.co.mz'
        elif str(country) in ['Myanmar', 'MM', 'MMR', '104']: domain = 'google.com.mm'
        elif str(country) in ['Namibia', 'NA', 'NAM', '516']: domain = 'google.com.na'
        elif str(country) in ['Nauru', 'NR', 'NRU', '520']: domain = 'google.nr'
        elif str(country) in ['Nepal', 'NP', 'NPL', '524']: domain = 'google.com.np'
        elif str(country) in ['Netherlands', 'NL', 'NLD', '528']: domain = 'google.nl'
        elif str(country) in ['New Zealand', 'NZ', 'NZL', '554']: domain = 'google.co.nz'
        elif str(country) in ['Nicaragua', 'NI', 'NIC', '558']: domain = 'google.com.ni'
        elif str(country) in ['Niger', 'NE', 'NER', '562']: domain = 'google.ne'
        elif str(country) in ['Nigeria', 'NG', 'NGA', '566']: domain = 'google.com.ng'
        elif str(country) in ['Niue', 'NU', 'NIU', '570']: domain = 'google.nu'
        elif str(country) in ['Norfolk Island', 'NF', 'NFK', '574']: domain = 'google.nf'
        elif str(country) in ['Norway', 'NO', 'NOR', '578']: domain = 'google.no'
        elif str(country) in ['Oman', 'OM', 'OMN', '512']: domain = 'google.com.om'
        elif str(country) in ['Pakistan', 'PK', 'PAK', '586']: domain = 'google.com.pk'
        elif str(country) in ['Panama', 'PA', 'PAN', '591']: domain = 'google.com.pa'
        elif str(country) in ['Papua New Guinea', 'PG', 'PNG', '598']: domain = 'google.com.pg'
        elif str(country) in ['Paraguay', 'PY', 'PRY', '600']: domain = 'google.com.py'
        elif str(country) in ['Peru', 'PE', 'PER', '604']: domain = 'google.com.pe'
        elif str(country) in ['Philippines', 'PH', 'PHL', '608']: domain = 'google.com.ph'
        elif str(country) in ['Poland', 'PL', 'POL', '616']: domain = 'google.pl'
        elif str(country) in ['Portugal', 'PT', 'PRT', '620']: domain = 'google.pt'
        elif str(country) in ['Puerto Rico', 'PR', 'PRI', '630']: domain = 'google.com.pr'
        elif str(country) in ['Qatar', 'QA', 'QAT', '634']: domain = 'google.com.qa'
        elif str(country) in ['Romania', 'RO', 'ROU', '642']: domain = 'google.ro'
        elif str(country) in ['Rwanda', 'RW', 'RWA', '646']: domain = 'google.rw'
        elif str(country) in ['Saint Lucia', 'LC', 'LCA', '662']: domain = 'google.com.lc'
        elif str(country) in ['Samoa', 'WS', 'WSM', '882']: domain = 'google.ws'
        elif str(country) in ['San Marino', 'SM', 'SMR', '674']: domain = 'google.sm'
        elif str(country) in ['Saudi Arabia', 'SA', 'SAU', '682']: domain = 'google.com.sa'
        elif str(country) in ['Senegal', 'SN', 'SEN', '686']: domain = 'google.sn'
        elif str(country) in ['Serbia', 'RS', 'SRB', '688']: domain = 'google.rs'
        elif str(country) in ['Seychelles', 'SC', 'SYC', '690']: domain = 'google.sc'
        elif str(country) in ['Sierra Leone', 'SL', 'SLE', '694']: domain = 'google.com.sl'
        elif str(country) in ['Singapore', 'SG', 'SGP', '702']: domain = 'google.com.sg'
        elif str(country) in ['Slovakia', 'SK', 'SVK', '703']: domain = 'google.sk'
        elif str(country) in ['Slovenia', 'SI', 'SVN', '705']: domain = 'google.si'
        elif str(country) in ['Solomon Islands', 'SB', 'SLB', '090']: domain = 'google.com.sb'
        elif str(country) in ['Somalia', 'SO', 'SOM', '706']: domain = 'google.so'
        elif str(country) in ['South Africa', 'ZA', 'ZAF', '710']: domain = 'google.co.za'
        elif str(country) in ['Spain', 'ES', 'ESP', '724']: domain = 'google.es'
        elif str(country) in ['Sri Lanka', 'LK', 'LKA', '144']: domain = 'google.lk'
        elif str(country) in ['Sweden', 'SE', 'SWE', '752']: domain = 'google.se'
        elif str(country) in ['Switzerland', 'CH', 'CHE', '756']: domain = 'google.ch'
        elif str(country) in ['Tajikistan', 'TJ', 'TJK', '762']: domain = 'google.com.tj'
        elif str(country) in ['Thailand', 'TH', 'THA', '764']: domain = 'google.co.th'
        elif str(country) in ['Timor-Leste', 'TL', 'TLS', '626']: domain = 'google.tl'
        elif str(country) in ['Togo', 'TG', 'TGO', '768']: domain = 'google.tg'
        elif str(country) in ['Tokelau', 'TK', 'TKL', '772']: domain = 'google.tk'
        elif str(country) in ['Tonga', 'TO', 'TON', '776']: domain = 'google.to'
        elif str(country) in ['Trinidad and Tobago', 'TT', 'TTO', '780']: domain = 'google.tt'
        elif str(country) in ['Tunisia', 'TN', 'TUN', '788']: domain = 'google.tn'
        elif str(country) in ['Turkey', 'TR', 'TUR', '792']: domain = 'google.com.tr'
        elif str(country) in ['Turkmenistan', 'TM', 'TKM', '795']: domain = 'google.tm'
        elif str(country) in ['Uganda', 'UG', 'UGA', '800']: domain = 'google.co.ug'
        elif str(country) in ['Ukraine', 'UA', 'UKR', '804']: domain = 'google.com.ua'
        elif str(country) in ['United Arab Emirates', 'AE', 'ARE', '784']: domain = 'google.ae'
        elif str(country) in ['United Kingdom', 'GB', 'GBR', '826']: domain = 'google.co.uk'
        elif str(country) in ['Uruguay', 'UY', 'URY', '858']: domain = 'google.com.uy'
        elif str(country) in ['Uzbekistan', 'UZ', 'UZB', '860']: domain = 'google.co.uz'
        elif str(country) in ['Vanuatu', 'VU', 'VUT', '548']: domain = 'google.vu'
        elif str(country) in ['Zambia', 'ZM', 'ZMB', '894']: domain = 'google.co.zm'
        elif str(country) in ['Zimbabwe', 'ZW', 'ZWE', '716']: domain = 'google.co.zw'
        else:
            domain = 'google.com'
        domain = "https://www."+domain
        return domain

    def perform_search_from_main_page(self, search_query, num_results_per_page = 10):
        '''This function does a basic "search", and retrieves the search url generated by Google, which cannot be spoofed.
            This url is then passed on to all the other workers, who append &num and &start and to it.
            This function should only be called once for the total query execution. '''
        ## Takes as input a search query string
        if num_results_per_page != 10:
            self.disable_google_instant()
        else:
            self.browser.visit(self.get_country_domain(self.country))
        self.browser.webdriver.find_element_by_name('q').send_keys(search_query)
        self.browser.webdriver.find_element_by_name('q').send_keys(Keys.RETURN)     ## Press Enter while focused on the search box.
        # if self.browser.wait_for_element_to_load_ajax(15, "search") == False:
        #     print("THIS CANNOT GO ON")
        #     return None
        return self.browser.get_url()


    def get_SERP_results(self, old_url, start, num_results_per_page, save_to_db = True):
        ## Get a search engine results page from url
        url = self._update_url_number_of_results_per_page(self._update_url_start(old_url, start), num_results_per_page)
        self.browser.visit(url)
        if self.browser.wait_for_element_to_load_ajax(timeout=60, element_css_selector=GoogleParser.css_selector_for_valid_page) == False:
            return None
        self.time_of_last_retrieved_query = time.time()
        parsed_serp = GoogleParser(self.browser.get_html(), url, start)
        if save_to_db:
            self.save_serp_to_db(parsed_serp, self.db_config)
        return parsed_serp



    def save_serp_to_db(self, parsed_page, db_config):
        pass


    def disable_google_instant(self):
        ## This allows you to get more than ten results per page.
        self.browser.visit(self.get_country_domain(self.country)+("/preferences"))
        if self.browser.wait_for_element_to_load_ajax(30, "#instant-radio") == False:
            return False
        ## Click the 'disable' <div>:
        self.browser.webdriver.find_element_by_id('instant-radio').find_elements_by_class_name('jfk-radiobutton')[-1].click()
        ## Save the results:
        if self.browser.webdriver.find_element_by_id('form-buttons').find_elements_by_class_name('jfk-button')[0].text == "Save":
            self.browser.webdriver.find_element_by_id('form-buttons').find_elements_by_class_name('jfk-button')[0].click()
        elif self.browser.webdriver.find_element_by_id('form-buttons').find_elements_by_class_name('jfk-button')[1].text == "Save":
            self.browser.webdriver.find_element_by_id('form-buttons').find_elements_by_class_name('jfk-button')[1].click()
        ## Press 'ok' on the resulting alert:
        try:
            self.browser.webdriver.switch_to_alert().accept()
        except Exception:
            pass
        return True


    def get_url_from_query_string(self, query_string, num_results_per_page=10, start = 0):
        out = self.get_country_domain(self.country) + "?q=" + urllib.parse.quote_plus(query_string)
        if num_results_per_page != 10 and num_results_per_page in self.possible_num_results_per_page:
            out += "&num=%s" % num_results_per_page
        if start != 0:
            out += "&start=%s" % start
        return out


    def _update_url_start(self, url, new_start):
        if new_start == 0:
            url = re.sub('\&start=\d{1,}', '', url)
            return url
        if url.find('&start=') == -1:
            url += "&start=%s" % new_start
        else:
            url = re.sub('&start=\d{1,}', '&start=%s'%new_start, url)
        return url

    def _update_url_number_of_results_per_page(self, url, new_num_results_per_page):
        if new_num_results_per_page == self.default_num_results_per_page:
            url = re.sub('&num=\d{1,}', '', url)
            return url
        if url.find('&num=') == -1:
            url += "&num=%s" % new_num_results_per_page
        else:
            url = re.sub('&num=\d{1,}', '&num=%s'%new_num_results_per_page, url)
        return url






