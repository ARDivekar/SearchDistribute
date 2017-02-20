from SearchDistribute.SearchQuery import GoogleSearchQuery
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.Enums import ProxyBrowsers
from SearchDistribute.SearchExtractorErrors import *
from SearchDistribute import ProxyBrowser

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
          (c) (optional) db_name  : a string, for the SQLite database name in which to save the results.
          (d) (optional) db_table : a string, for the SQLite database table name in which to save the results.
          (e) (optional) country  : a string, for country where we search. By default it is USA. This is translated to the country where we search.

     [4] To actually search and retrieve results, the search query must be passed explicitly to the `search(...)` function, along with an optional offset and number of results in the SERP.
'''
class GoogleSearch(SearchTemplate):
    search_engine = SearchEngines.Google
    proxy_browser_type = ""             ## taken from SearchDistribute.Enums.ProxyBrowsers
    browser = None
    time_of_last_retrieved_query = 0    ## Seconds since UNIX epoch
    country = ""

    def __init__(self, config={}):
        self.proxy_browser_type = config.get("proxy_browser_type") ## Set to None if does not exist
        if self.proxy_browser_type == ProxyBrowsers.PhantomJS:
            self.browser = ProxyBrowser.PhantomJS(config.get("proxy_type"), config.get("hostname"), config.get("port"), config.get("username"), config.get("password"))
        else:
            raise UnsupportedProxyBrowserException(self.proxy_browser_type)
        self.country = "USA" if config.get("country")  ## Set to None if does not exist


    def get_country_domain(self):
        domain = ""
        ## Source: https://www.wikiwand.com/en/List_of_Google_domains and http://www.nationsonline.org/oneworld/country_code_list.htm
        ## In order: [Country Name,  ISO ALPHA-2 CODE,  ISO ALPHA-3 CODE]
        if self.country in ["Ascension Island"]: domain = "google.ac"
        if self.country in ["Andorra", "AN", "AND"]: domain = "google.ad"
        if self.country in ["United Arab Emirates", "AE", "ARE"]: domain = "google.ae"
        if self.country in ["Afghanistan", "AF", "AFG"]: domain = "google.com.af"
        if self.country in ["Antigua and Barbuda"]: domain = "google.com.ag"
        if self.country in ["Anguilla"]: domain = "google.com.ai"
        if self.country in ["Albania"]: domain = "google.al"
        if self.country in ["Armenia"]: domain = "google.am"
        if self.country in ["Angola"]: domain = "google.co.ao"
        if self.country in ["Argentina"]: domain = "google.com.ar"
        if self.country in ["American Samoa"]: domain = "google.as"
        if self.country in ["Austria"]: domain = "google.at"
        if self.country in ["Australia"]: domain = "google.com.au"
        if self.country in ["Azerbaijan"]: domain = "google.az"
        if self.country in ["Bosnia and Herzegovina"]: domain = "google.ba"
        if self.country in ["Bangladesh"]: domain = "google.com.bd"
        if self.country in ["Belgium"]: domain = "google.be"
        if self.country in ["Burkina Faso"]: domain = "google.bf"
        if self.country in ["Bulgaria"]: domain = "google.bg"
        if self.country in ["Bahrain"]: domain = "google.com.bh"
        if self.country in ["Burundi"]: domain = "google.bi"
        if self.country in ["Benin"]: domain = "google.bj"
        if self.country in ["Brunei"]: domain = "google.com.bn"
        if self.country in ["Bolivia"]: domain = "google.com.bo"
        if self.country in ["Brazil"]: domain = "google.com.br"
        if self.country in ["Bahamas"]: domain = "google.bs"
        if self.country in ["Bhutan"]: domain = "google.bt"
        if self.country in ["Botswana"]: domain = "google.co.bw"
        if self.country in ["Belarus"]: domain = "google.by"
        if self.country in ["Belize"]: domain = "google.com.bz"
        if self.country in ["Canada"]: domain = "google.ca"
        if self.country in ["Cambodia"]: domain = "google.com.kh"
        if self.country in ["Cocos (Keeling) Islands"]: domain = "google.cc"
        if self.country in ["Democratic Republic of the Congo"]: domain = "google.cd"
        if self.country in ["Central African Republic"]: domain = "google.cf"
        if self.country in ["Catalonia Catalan Countries"]: domain = "google.cat"
        if self.country in ["Republic of the Congo"]: domain = "google.cg"
        if self.country in ["Switzerland"]: domain = "google.ch"
        if self.country in ["Ivory Coast"]: domain = "google.ci"
        if self.country in ["Cook Islands"]: domain = "google.co.ck"
        if self.country in ["Chile"]: domain = "google.cl"
        if self.country in ["Cameroon"]: domain = "google.cm"
        if self.country in ["China"]: domain = "google.cn"
        if self.country in ["Colombia"]: domain = "google.com.co"
        if self.country in ["Costa Rica"]: domain = "google.co.cr"
        if self.country in ["Cuba"]: domain = "google.com.cu"
        if self.country in ["Cape Verde"]: domain = "google.cv"
        if self.country in ["Christmas Island"]: domain = "google.cx"
        if self.country in ["Cyprus"]: domain = "google.com.cy"
        if self.country in ["Czech Republic"]: domain = "google.cz"
        if self.country in ["Germany"]: domain = "google.de"
        if self.country in ["Djibouti"]: domain = "google.dj"
        if self.country in ["Denmark"]: domain = "google.dk"
        if self.country in ["Dominica"]: domain = "google.dm"
        if self.country in ["Dominican Republic"]: domain = "google.com.do"
        if self.country in ["Algeria"]: domain = "google.dz"
        if self.country in ["Ecuador"]: domain = "google.com.ec"
        if self.country in ["Estonia"]: domain = "google.ee"
        if self.country in ["Egypt"]: domain = "google.com.eg"
        if self.country in ["Spain"]: domain = "google.es"
        if self.country in ["Ethiopia"]: domain = "google.com.et"
        if self.country in ["European Union"]: domain = "google.eu"
        if self.country in ["Finland"]: domain = "google.fi"
        if self.country in ["Fiji"]: domain = "google.com.fj"
        if self.country in ["Federated States of Micronesia"]: domain = "google.fm"
        if self.country in ["France"]: domain = "google.fr"
        if self.country in ["Gabon"]: domain = "google.ga"
        if self.country in ["Georgia"]: domain = "google.ge"
        if self.country in ["French Guiana"]: domain = "google.gf"
        if self.country in ["Guernsey"]: domain = "google.gg"
        if self.country in ["Ghana"]: domain = "google.com.gh"
        if self.country in ["Gibraltar"]: domain = "google.com.gi"
        if self.country in ["Greenland"]: domain = "google.gl"
        if self.country in ["Gambia"]: domain = "google.gm"
        if self.country in ["Guadeloupe"]: domain = "google.gp"
        if self.country in ["Greece"]: domain = "google.gr"
        if self.country in ["Guatemala"]: domain = "google.com.gt"
        if self.country in ["Guyana"]: domain = "google.gy"
        if self.country in ["Hong Kong"]: domain = "google.com.hk"
        if self.country in ["Honduras"]: domain = "google.hn"
        if self.country in ["Croatia"]: domain = "google.hr"
        if self.country in ["Haiti"]: domain = "google.ht"
        if self.country in ["Hungary"]: domain = "google.hu"
        if self.country in ["Indonesia"]: domain = "google.co.id"
        if self.country in ["Iraq"]: domain = "google.iq"
        if self.country in ["Ireland"]: domain = "google.ie"
        if self.country in ["Israel"]: domain = "google.co.il"
        if self.country in ["Isle of Man"]: domain = "google.im"
        if self.country in ["India"]: domain = "google.co.in"
        if self.country in ["British Indian Ocean Territory"]: domain = "google.io"
        if self.country in ["Iceland"]: domain = "google.is"
        if self.country in ["Italy"]: domain = "google.it"
        if self.country in ["Jersey"]: domain = "google.je"
        if self.country in ["Jamaica"]: domain = "google.com.jm"
        if self.country in ["Jordan"]: domain = "google.jo"
        if self.country in ["Japan"]: domain = "google.co.jp"
        if self.country in ["Kenya"]: domain = "google.co.ke"
        if self.country in ["Kiribati"]: domain = "google.ki"
        if self.country in ["Kyrgyzstan"]: domain = "google.kg"
        if self.country in ["South Korea"]: domain = "google.co.kr"
        if self.country in ["Kuwait"]: domain = "google.com.kw"
        if self.country in ["Kazakhstan"]: domain = "google.kz"
        if self.country in ["Laos"]: domain = "google.la"
        if self.country in ["Lebanon"]: domain = "google.com.lb"
        if self.country in ["Saint Lucia"]: domain = "google.com.lc"
        if self.country in ["Liechtenstein"]: domain = "google.li"
        if self.country in ["Sri Lanka"]: domain = "google.lk"
        if self.country in ["Lesotho"]: domain = "google.co.ls"
        if self.country in ["Lithuania"]: domain = "google.lt"
        if self.country in ["Luxembourg"]: domain = "google.lu"
        if self.country in ["Latvia"]: domain = "google.lv"
        if self.country in ["Libya"]: domain = "google.com.ly"
        if self.country in ["Morocco"]: domain = "google.co.ma"
        if self.country in ["Moldova"]: domain = "google.md"
        if self.country in ["Montenegro"]: domain = "google.me"
        if self.country in ["Madagascar"]: domain = "google.mg"
        if self.country in ["Macedonia"]: domain = "google.mk"
        if self.country in ["Mali"]: domain = "google.ml"
        if self.country in ["Myanmar"]: domain = "google.com.mm"
        if self.country in ["Mongolia"]: domain = "google.mn"
        if self.country in ["Montserrat"]: domain = "google.ms"
        if self.country in ["Malta"]: domain = "google.com.mt"
        if self.country in ["Mauritius"]: domain = "google.mu"
        if self.country in ["Maldives"]: domain = "google.mv"
        if self.country in ["Malawi"]: domain = "google.mw"
        if self.country in ["Mexico"]: domain = "google.com.mx"
        if self.country in ["Malaysia"]: domain = "google.com.my"
        if self.country in ["Mozambique"]: domain = "google.co.mz"
        if self.country in ["Namibia"]: domain = "google.com.na"
        if self.country in ["Niger"]: domain = "google.ne"
        if self.country in ["Norfolk Island"]: domain = "google.nf"
        if self.country in ["Nigeria"]: domain = "google.com.ng"
        if self.country in ["Nicaragua"]: domain = "google.com.ni"
        if self.country in ["Netherlands"]: domain = "google.nl"
        if self.country in ["Norway"]: domain = "google.no"
        if self.country in ["Nepal"]: domain = "google.com.np"
        if self.country in ["Nauru"]: domain = "google.nr"
        if self.country in ["Niue"]: domain = "google.nu"
        if self.country in ["New Zealand"]: domain = "google.co.nz"
        if self.country in ["Oman"]: domain = "google.com.om"
        if self.country in ["Pakistan"]: domain = "google.com.pk"
        if self.country in ["Panama"]: domain = "google.com.pa"
        if self.country in ["Peru"]: domain = "google.com.pe"
        if self.country in ["Philippines"]: domain = "google.com.ph"
        if self.country in ["Poland"]: domain = "google.pl"
        if self.country in ["Papua New Guinea"]: domain = "google.com.pg"
        if self.country in ["Pitcairn Islands"]: domain = "google.pn"
        if self.country in ["Puerto Rico"]: domain = "google.com.pr"
        if self.country in ["Palestine[4]"]: domain = "google.ps"
        if self.country in ["Portugal"]: domain = "google.pt"
        if self.country in ["Paraguay"]: domain = "google.com.py"
        if self.country in ["Qatar"]: domain = "google.com.qa"
        if self.country in ["Romania"]: domain = "google.ro"
        if self.country in ["Serbia"]: domain = "google.rs"
        if self.country in ["Russia"]: domain = "google.ru"
        if self.country in ["Rwanda"]: domain = "google.rw"
        if self.country in ["Saudi Arabia"]: domain = "google.com.sa"
        if self.country in ["Solomon Islands"]: domain = "google.com.sb"
        if self.country in ["Seychelles"]: domain = "google.sc"
        if self.country in ["Sweden"]: domain = "google.se"
        if self.country in ["Singapore"]: domain = "google.com.sg"
        if self.country in ["Saint Helena, Ascension and Tristan da Cunha"]: domain = "google.sh"
        if self.country in ["Slovenia"]: domain = "google.si"
        if self.country in ["Slovakia"]: domain = "google.sk"
        if self.country in ["Sierra Leone"]: domain = "google.com.sl"
        if self.country in ["Senegal"]: domain = "google.sn"
        if self.country in ["San Marino"]: domain = "google.sm"
        if self.country in ["Somalia"]: domain = "google.so"
        if self.country in ["São Tomé and Príncipe"]: domain = "google.st"
        if self.country in ["Suriname"]: domain = "google.sr"
        if self.country in ["El Salvador"]: domain = "google.com.sv"
        if self.country in ["Chad"]: domain = "google.td"
        if self.country in ["Togo"]: domain = "google.tg"
        if self.country in ["Thailand"]: domain = "google.co.th"
        if self.country in ["Tajikistan"]: domain = "google.com.tj"
        if self.country in ["Tokelau"]: domain = "google.tk"
        if self.country in ["Timor-Leste"]: domain = "google.tl"
        if self.country in ["Turkmenistan"]: domain = "google.tm"
        if self.country in ["Tonga"]: domain = "google.to"
        if self.country in ["Tunisia"]: domain = "google.tn"
        if self.country in ["Turkey"]: domain = "google.com.tr"
        if self.country in ["Trinidad and Tobago"]: domain = "google.tt"
        if self.country in ["Taiwan"]: domain = "google.com.tw"
        if self.country in ["Tanzania"]: domain = "google.co.tz"
        if self.country in ["Ukraine"]: domain = "google.com.ua"
        if self.country in ["Uganda"]: domain = "google.co.ug"
        if self.country in ["United Kingdom"]: domain = "google.co.uk"
        if self.country in ["United States"]: domain = "google.com"
        if self.country in ["Uruguay"]: domain = "google.com.uy"
        if self.country in ["Uzbekistan"]: domain = "google.co.uz"
        if self.country in ["Saint Vincent and the Grenadines"]: domain = "google.com.vc"
        if self.country in ["Venezuela"]: domain = "google.co.ve"
        if self.country in ["British Virgin Islands"]: domain = "google.vg"
        if self.country in ["United States Virgin Islands"]: domain = "google.co.vi"
        if self.country in ["Vietnam"]: domain = "google.com.vn"
        if self.country in ["Vanuatu"]: domain = "google.vu"
        if self.country in ["Samoa"]: domain = "google.ws"
        if self.country in ["South Africa"]: domain = "google.co.za"
        if self.country in ["Zambia"]: domain = "google.co.zm"
        if self.country in ["Zimbabwe"]: domain = "google.co.zw"

        domain = "https://"+domain+"/?gws_rd=ssl"

    def perform_search_from_main_page(self, search_query):
        ## Takes as input a search query string
        self.browser.visit(self.get_country_domain(self.country))
        self.browser.fill('q', search_query)
        button = self.browser.find_by_name('btnG')  ## btnG was found by looking at google.com's HTML code.
        button.click()








