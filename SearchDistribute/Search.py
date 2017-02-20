from SearchDistribute.SearchQuery import GoogleSearchQuery
from SearchDistribute.Enums import SearchEngines
from SearchDistribute.Enums import ProxyBrowsers
from SearchDistribute.SearchExtractorErrors import *
from SearchDistribute import ProxyBrowser

from selenium.webdriver.common.keys import Keys
import urllib

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
    possible_num_results_per_page = [10, 20, 30, 40, 50, 100]

    def __init__(self, config={}):
        self.proxy_browser_type = config.get("proxy_browser_type") ## Set to None if does not exist
        if self.proxy_browser_type == ProxyBrowsers.PhantomJS:
            self.browser = ProxyBrowser.PhantomJS(config.get("proxy_type"), config.get("hostname"), config.get("port"), config.get("username"), config.get("password"))
        else:
            raise UnsupportedProxyBrowserException(self.proxy_browser_type)
        self.country = config.get("country")  ## Set to None if does not exist, will default to the domain of google.com


    def get_country_domain(self):
        domain = ""
        ## Source: https://www.wikiwand.com/en/List_of_Google_domains and http://www.nationsonline.org/oneworld/country_code_list.htm
        ## In order: [Country Name,  ISO ALPHA-2 CODE,  ISO ALPHA-3 CODE, ISO Numeric Code UN M49 Numerical Code]
        if   str(self.country) in ['Afghanistan', 'AF', 'AFG', '004']: domain = 'google.com.af'
        elif str(self.country) in ['Albania', 'AL', 'ALB', '008']: domain = 'google.al'
        elif str(self.country) in ['Algeria', 'DZ', 'DZA', '012']: domain = 'google.dz'
        elif str(self.country) in ['American Samoa', 'AS', 'ASM', '016']: domain = 'google.as'
        elif str(self.country) in ['Andorra', 'AD', 'AND', '020']: domain = 'google.ad'
        elif str(self.country) in ['Angola', 'AO', 'AGO', '024']: domain = 'google.co.ao'
        elif str(self.country) in ['Anguilla', 'AI', 'AIA', '660']: domain = 'google.com.ai'
        elif str(self.country) in ['Antigua and Barbuda', 'AG', 'ATG', '028']: domain = 'google.com.ag'
        elif str(self.country) in ['Argentina', 'AR', 'ARG', '032']: domain = 'google.com.ar'
        elif str(self.country) in ['Armenia', 'AM', 'ARM', '051']: domain = 'google.am'
        elif str(self.country) in ['Australia', 'AU', 'AUS', '036']: domain = 'google.com.au'
        elif str(self.country) in ['Austria', 'AT', 'AUT', '040']: domain = 'google.at'
        elif str(self.country) in ['Azerbaijan', 'AZ', 'AZE', '031']: domain = 'google.az'
        elif str(self.country) in ['Bahamas', 'BS', 'BHS', '044']: domain = 'google.bs'
        elif str(self.country) in ['Bahrain', 'BH', 'BHR', '048']: domain = 'google.com.bh'
        elif str(self.country) in ['Bangladesh', 'BD', 'BGD', '050']: domain = 'google.com.bd'
        elif str(self.country) in ['Belarus', 'BY', 'BLR', '112']: domain = 'google.by'
        elif str(self.country) in ['Belgium', 'BE', 'BEL', '056']: domain = 'google.be'
        elif str(self.country) in ['Belize', 'BZ', 'BLZ', '084']: domain = 'google.com.bz'
        elif str(self.country) in ['Benin', 'BJ', 'BEN', '204']: domain = 'google.bj'
        elif str(self.country) in ['Bhutan', 'BT', 'BTN', '064']: domain = 'google.bt'
        elif str(self.country) in ['Bolivia', 'BO', 'BOL', '068']: domain = 'google.com.bo'
        elif str(self.country) in ['Bosnia and Herzegovina', 'BA', 'BIH', '070']: domain = 'google.ba'
        elif str(self.country) in ['Botswana', 'BW', 'BWA', '072']: domain = 'google.co.bw'
        elif str(self.country) in ['Brazil', 'BR', 'BRA', '076']: domain = 'google.com.br'
        elif str(self.country) in ['British Indian Ocean Territory', 'IO', 'IOT', '086']: domain = 'google.io'
        elif str(self.country) in ['British Virgin Islands', 'VG', 'VGB', '092']: domain = 'google.vg'
        elif str(self.country) in ['Bulgaria', 'BG', 'BGR', '100']: domain = 'google.bg'
        elif str(self.country) in ['Burkina Faso', 'BF', 'BFA', '854']: domain = 'google.bf'
        elif str(self.country) in ['Burundi', 'BI', 'BDI', '108']: domain = 'google.bi'
        elif str(self.country) in ['Cambodia', 'KH', 'KHM', '116']: domain = 'google.com.kh'
        elif str(self.country) in ['Cameroon', 'CM', 'CMR', '120']: domain = 'google.cm'
        elif str(self.country) in ['Canada', 'CA', 'CAN', '124']: domain = 'google.ca'
        elif str(self.country) in ['Cape Verde', 'CV', 'CPV', '132']: domain = 'google.cv'
        elif str(self.country) in ['Central African Republic', 'CF', 'CAF', '140']: domain = 'google.cf'
        elif str(self.country) in ['Chad', 'TD', 'TCD', '148']: domain = 'google.td'
        elif str(self.country) in ['Chile', 'CL', 'CHL', '152']: domain = 'google.cl'
        elif str(self.country) in ['China', 'CN', 'CHN', '156']: domain = 'google.cn'
        elif str(self.country) in ['Christmas Island', 'CX', 'CXR', '162']: domain = 'google.cx'
        elif str(self.country) in ['Cocos (Keeling) Islands', 'CC', 'CCK', '166']: domain = 'google.cc'
        elif str(self.country) in ['Colombia', 'CO', 'COL', '170']: domain = 'google.com.co'
        elif str(self.country) in ['Cook Islands', 'CK', 'COK', '184']: domain = 'google.co.ck'
        elif str(self.country) in ['Costa Rica', 'CR', 'CRI', '188']: domain = 'google.co.cr'
        elif str(self.country) in ['Croatia', 'HR', 'HRV', '191']: domain = 'google.hr'
        elif str(self.country) in ['Cuba', 'CU', 'CUB', '192']: domain = 'google.com.cu'
        elif str(self.country) in ['Cyprus', 'CY', 'CYP', '196']: domain = 'google.com.cy'
        elif str(self.country) in ['Czech Republic', 'CZ', 'CZE', '203']: domain = 'google.cz'
        elif str(self.country) in ['Denmark', 'DK', 'DNK', '208']: domain = 'google.dk'
        elif str(self.country) in ['Djibouti', 'DJ', 'DJI', '262']: domain = 'google.dj'
        elif str(self.country) in ['Dominica', 'DM', 'DMA', '212']: domain = 'google.dm'
        elif str(self.country) in ['Dominican Republic', 'DO', 'DOM', '214']: domain = 'google.com.do'
        elif str(self.country) in ['Ecuador', 'EC', 'ECU', '218']: domain = 'google.com.ec'
        elif str(self.country) in ['Egypt', 'EG', 'EGY', '818']: domain = 'google.com.eg'
        elif str(self.country) in ['El Salvador', 'SV', 'SLV', '222']: domain = 'google.com.sv'
        elif str(self.country) in ['Estonia', 'EE', 'EST', '233']: domain = 'google.ee'
        elif str(self.country) in ['Ethiopia', 'ET', 'ETH', '231']: domain = 'google.com.et'
        elif str(self.country) in ['Fiji', 'FJ', 'FJI', '242']: domain = 'google.com.fj'
        elif str(self.country) in ['Finland', 'FI', 'FIN', '246']: domain = 'google.fi'
        elif str(self.country) in ['France', 'FR', 'FRA', '250']: domain = 'google.fr'
        elif str(self.country) in ['French Guiana', 'GF', 'GUF', '254']: domain = 'google.gf'
        elif str(self.country) in ['Gabon', 'GA', 'GAB', '266']: domain = 'google.ga'
        elif str(self.country) in ['Gambia', 'GM', 'GMB', '270']: domain = 'google.gm'
        elif str(self.country) in ['Georgia', 'GE', 'GEO', '268']: domain = 'google.ge'
        elif str(self.country) in ['Germany', 'DE', 'DEU', '276']: domain = 'google.de'
        elif str(self.country) in ['Ghana', 'GH', 'GHA', '288']: domain = 'google.com.gh'
        elif str(self.country) in ['Gibraltar', 'GI', 'GIB', '292']: domain = 'google.com.gi'
        elif str(self.country) in ['Greece', 'GR', 'GRC', '300']: domain = 'google.gr'
        elif str(self.country) in ['Greenland', 'GL', 'GRL', '304']: domain = 'google.gl'
        elif str(self.country) in ['Guadeloupe', 'GP', 'GLP', '312']: domain = 'google.gp'
        elif str(self.country) in ['Guatemala', 'GT', 'GTM', '320']: domain = 'google.com.gt'
        elif str(self.country) in ['Guernsey', 'GG', 'GGY', '831']: domain = 'google.gg'
        elif str(self.country) in ['Guyana', 'GY', 'GUY', '328']: domain = 'google.gy'
        elif str(self.country) in ['Haiti', 'HT', 'HTI', '332']: domain = 'google.ht'
        elif str(self.country) in ['Honduras', 'HN', 'HND', '340']: domain = 'google.hn'
        elif str(self.country) in ['Hungary', 'HU', 'HUN', '348']: domain = 'google.hu'
        elif str(self.country) in ['Iceland', 'IS', 'ISL', '352']: domain = 'google.is'
        elif str(self.country) in ['India', 'IN', 'IND', '356']: domain = 'google.co.in'
        elif str(self.country) in ['Indonesia', 'ID', 'IDN', '360']: domain = 'google.co.id'
        elif str(self.country) in ['Iraq', 'IQ', 'IRQ', '368']: domain = 'google.iq'
        elif str(self.country) in ['Ireland', 'IE', 'IRL', '372']: domain = 'google.ie'
        elif str(self.country) in ['Isle of Man', 'IM', 'IMN', '833']: domain = 'google.im'
        elif str(self.country) in ['Israel', 'IL', 'ISR', '376']: domain = 'google.co.il'
        elif str(self.country) in ['Italy', 'IT', 'ITA', '380']: domain = 'google.it'
        elif str(self.country) in ['Jamaica', 'JM', 'JAM', '388']: domain = 'google.com.jm'
        elif str(self.country) in ['Japan', 'JP', 'JPN', '392']: domain = 'google.co.jp'
        elif str(self.country) in ['Jersey', 'JE', 'JEY', '832']: domain = 'google.je'
        elif str(self.country) in ['Jordan', 'JO', 'JOR', '400']: domain = 'google.jo'
        elif str(self.country) in ['Kazakhstan', 'KZ', 'KAZ', '398']: domain = 'google.kz'
        elif str(self.country) in ['Kenya', 'KE', 'KEN', '404']: domain = 'google.co.ke'
        elif str(self.country) in ['Kiribati', 'KI', 'KIR', '296']: domain = 'google.ki'
        elif str(self.country) in ['Kuwait', 'KW', 'KWT', '414']: domain = 'google.com.kw'
        elif str(self.country) in ['Kyrgyzstan', 'KG', 'KGZ', '417']: domain = 'google.kg'
        elif str(self.country) in ['Latvia', 'LV', 'LVA', '428']: domain = 'google.lv'
        elif str(self.country) in ['Lebanon', 'LB', 'LBN', '422']: domain = 'google.com.lb'
        elif str(self.country) in ['Lesotho', 'LS', 'LSO', '426']: domain = 'google.co.ls'
        elif str(self.country) in ['Libya', 'LY', 'LBY', '434']: domain = 'google.com.ly'
        elif str(self.country) in ['Liechtenstein', 'LI', 'LIE', '438']: domain = 'google.li'
        elif str(self.country) in ['Lithuania', 'LT', 'LTU', '440']: domain = 'google.lt'
        elif str(self.country) in ['Luxembourg', 'LU', 'LUX', '442']: domain = 'google.lu'
        elif str(self.country) in ['Madagascar', 'MG', 'MDG', '450']: domain = 'google.mg'
        elif str(self.country) in ['Malawi', 'MW', 'MWI', '454']: domain = 'google.mw'
        elif str(self.country) in ['Malaysia', 'MY', 'MYS', '458']: domain = 'google.com.my'
        elif str(self.country) in ['Maldives', 'MV', 'MDV', '462']: domain = 'google.mv'
        elif str(self.country) in ['Mali', 'ML', 'MLI', '466']: domain = 'google.ml'
        elif str(self.country) in ['Malta', 'MT', 'MLT', '470']: domain = 'google.com.mt'
        elif str(self.country) in ['Mauritius', 'MU', 'MUS', '480']: domain = 'google.mu'
        elif str(self.country) in ['Mexico', 'MX', 'MEX', '484']: domain = 'google.com.mx'
        elif str(self.country) in ['Moldova', 'MD', 'MDA', '498']: domain = 'google.md'
        elif str(self.country) in ['Mongolia', 'MN', 'MNG', '496']: domain = 'google.mn'
        elif str(self.country) in ['Montenegro', 'ME', 'MNE', '499']: domain = 'google.me'
        elif str(self.country) in ['Montserrat', 'MS', 'MSR', '500']: domain = 'google.ms'
        elif str(self.country) in ['Morocco', 'MA', 'MAR', '504']: domain = 'google.co.ma'
        elif str(self.country) in ['Mozambique', 'MZ', 'MOZ', '508']: domain = 'google.co.mz'
        elif str(self.country) in ['Myanmar', 'MM', 'MMR', '104']: domain = 'google.com.mm'
        elif str(self.country) in ['Namibia', 'NA', 'NAM', '516']: domain = 'google.com.na'
        elif str(self.country) in ['Nauru', 'NR', 'NRU', '520']: domain = 'google.nr'
        elif str(self.country) in ['Nepal', 'NP', 'NPL', '524']: domain = 'google.com.np'
        elif str(self.country) in ['Netherlands', 'NL', 'NLD', '528']: domain = 'google.nl'
        elif str(self.country) in ['New Zealand', 'NZ', 'NZL', '554']: domain = 'google.co.nz'
        elif str(self.country) in ['Nicaragua', 'NI', 'NIC', '558']: domain = 'google.com.ni'
        elif str(self.country) in ['Niger', 'NE', 'NER', '562']: domain = 'google.ne'
        elif str(self.country) in ['Nigeria', 'NG', 'NGA', '566']: domain = 'google.com.ng'
        elif str(self.country) in ['Niue', 'NU', 'NIU', '570']: domain = 'google.nu'
        elif str(self.country) in ['Norfolk Island', 'NF', 'NFK', '574']: domain = 'google.nf'
        elif str(self.country) in ['Norway', 'NO', 'NOR', '578']: domain = 'google.no'
        elif str(self.country) in ['Oman', 'OM', 'OMN', '512']: domain = 'google.com.om'
        elif str(self.country) in ['Pakistan', 'PK', 'PAK', '586']: domain = 'google.com.pk'
        elif str(self.country) in ['Panama', 'PA', 'PAN', '591']: domain = 'google.com.pa'
        elif str(self.country) in ['Papua New Guinea', 'PG', 'PNG', '598']: domain = 'google.com.pg'
        elif str(self.country) in ['Paraguay', 'PY', 'PRY', '600']: domain = 'google.com.py'
        elif str(self.country) in ['Peru', 'PE', 'PER', '604']: domain = 'google.com.pe'
        elif str(self.country) in ['Philippines', 'PH', 'PHL', '608']: domain = 'google.com.ph'
        elif str(self.country) in ['Poland', 'PL', 'POL', '616']: domain = 'google.pl'
        elif str(self.country) in ['Portugal', 'PT', 'PRT', '620']: domain = 'google.pt'
        elif str(self.country) in ['Puerto Rico', 'PR', 'PRI', '630']: domain = 'google.com.pr'
        elif str(self.country) in ['Qatar', 'QA', 'QAT', '634']: domain = 'google.com.qa'
        elif str(self.country) in ['Romania', 'RO', 'ROU', '642']: domain = 'google.ro'
        elif str(self.country) in ['Rwanda', 'RW', 'RWA', '646']: domain = 'google.rw'
        elif str(self.country) in ['Saint Lucia', 'LC', 'LCA', '662']: domain = 'google.com.lc'
        elif str(self.country) in ['Samoa', 'WS', 'WSM', '882']: domain = 'google.ws'
        elif str(self.country) in ['San Marino', 'SM', 'SMR', '674']: domain = 'google.sm'
        elif str(self.country) in ['Saudi Arabia', 'SA', 'SAU', '682']: domain = 'google.com.sa'
        elif str(self.country) in ['Senegal', 'SN', 'SEN', '686']: domain = 'google.sn'
        elif str(self.country) in ['Serbia', 'RS', 'SRB', '688']: domain = 'google.rs'
        elif str(self.country) in ['Seychelles', 'SC', 'SYC', '690']: domain = 'google.sc'
        elif str(self.country) in ['Sierra Leone', 'SL', 'SLE', '694']: domain = 'google.com.sl'
        elif str(self.country) in ['Singapore', 'SG', 'SGP', '702']: domain = 'google.com.sg'
        elif str(self.country) in ['Slovakia', 'SK', 'SVK', '703']: domain = 'google.sk'
        elif str(self.country) in ['Slovenia', 'SI', 'SVN', '705']: domain = 'google.si'
        elif str(self.country) in ['Solomon Islands', 'SB', 'SLB', '090']: domain = 'google.com.sb'
        elif str(self.country) in ['Somalia', 'SO', 'SOM', '706']: domain = 'google.so'
        elif str(self.country) in ['South Africa', 'ZA', 'ZAF', '710']: domain = 'google.co.za'
        elif str(self.country) in ['Spain', 'ES', 'ESP', '724']: domain = 'google.es'
        elif str(self.country) in ['Sri Lanka', 'LK', 'LKA', '144']: domain = 'google.lk'
        elif str(self.country) in ['Sweden', 'SE', 'SWE', '752']: domain = 'google.se'
        elif str(self.country) in ['Switzerland', 'CH', 'CHE', '756']: domain = 'google.ch'
        elif str(self.country) in ['Tajikistan', 'TJ', 'TJK', '762']: domain = 'google.com.tj'
        elif str(self.country) in ['Thailand', 'TH', 'THA', '764']: domain = 'google.co.th'
        elif str(self.country) in ['Timor-Leste', 'TL', 'TLS', '626']: domain = 'google.tl'
        elif str(self.country) in ['Togo', 'TG', 'TGO', '768']: domain = 'google.tg'
        elif str(self.country) in ['Tokelau', 'TK', 'TKL', '772']: domain = 'google.tk'
        elif str(self.country) in ['Tonga', 'TO', 'TON', '776']: domain = 'google.to'
        elif str(self.country) in ['Trinidad and Tobago', 'TT', 'TTO', '780']: domain = 'google.tt'
        elif str(self.country) in ['Tunisia', 'TN', 'TUN', '788']: domain = 'google.tn'
        elif str(self.country) in ['Turkey', 'TR', 'TUR', '792']: domain = 'google.com.tr'
        elif str(self.country) in ['Turkmenistan', 'TM', 'TKM', '795']: domain = 'google.tm'
        elif str(self.country) in ['Uganda', 'UG', 'UGA', '800']: domain = 'google.co.ug'
        elif str(self.country) in ['Ukraine', 'UA', 'UKR', '804']: domain = 'google.com.ua'
        elif str(self.country) in ['United Arab Emirates', 'AE', 'ARE', '784']: domain = 'google.ae'
        elif str(self.country) in ['United Kingdom', 'GB', 'GBR', '826']: domain = 'google.co.uk'
        elif str(self.country) in ['Uruguay', 'UY', 'URY', '858']: domain = 'google.com.uy'
        elif str(self.country) in ['Uzbekistan', 'UZ', 'UZB', '860']: domain = 'google.co.uz'
        elif str(self.country) in ['Vanuatu', 'VU', 'VUT', '548']: domain = 'google.vu'
        elif str(self.country) in ['Zambia', 'ZM', 'ZMB', '894']: domain = 'google.co.zm'
        elif str(self.country) in ['Zimbabwe', 'ZW', 'ZWE', '716']: domain = 'google.co.zw'
        else:
            domain = 'google.com'
        domain = "https://www."+domain

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
        if self.browser.wait_for_element_to_load_ajax(15, "search") == False:
            return None
        return self.browser.get_url()



    def disable_google_instant(self):
        ## This allows you to get more than ten results per page.
        self.browser.visit(self.get_country_domain(self.country)+("/preferences"))
        if self.browser.wait_for_element_to_load_ajax(15, "instant-radio") == False:
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








