import random
import time
import platform
import random

from search_medium.search_medium import SearchMedium
from utils.exceptions import SearchMediumNotAvailable

phantom_path = None
system = platform.system()
if system == 'Darwin':
    phantom_path = './ExternalLibs/PhantomJS/Mac/phantomjs'
elif system == 'Linux':
    phantom_path = './ExternalLibs/PhantomJS/Linux/phantomjs'
else:
    phantom_path = './ExternalLibs/PhantomJS/Windows/phantomjs.exe'


class SplinterBrowser(SearchMedium):

    def __init__(self, use_phantom):
        self.use_phantom = use_phantom
        self.browser = None

    def start_browser(self, proxy=None, user_agent=None):
        try:
            import splinter

            if proxy:
                proxy_settings = {
                    'network.proxy.type': 1,
                    'network.proxy.http': proxy['ip'],
                    'network.proxy.http_port': proxy['port'],
                    'network.proxy.ssl': proxy['ip'],
                    'network.proxy.ssl_port': proxy['port'],
                    'network.proxy.socks': proxy['ip'],
                    'network.proxy.socks_port': proxy['port'],
                    'network.proxy.ftp': proxy['ip'],
                    'network.proxy.ftp_port': proxy['port']
                }

                if not self.use_phantom:
                    self.browser = splinter.Browser(profile_preferences=proxy_settings, user_agent=user_agent)
                else:
                    self.browser = splinter.Browser('phantomjs', executable_path=phantom_path, profile_preferences=proxy_settings, user_agent=user_agent)
            else:
                if not self.use_phantom:
                    self.browser = splinter.Browser()
                else:
                    self.browser = splinter.Browser('phantomjs', executable_path=phantom_path)
        except:
            if not self.use_phantom:
                raise SearchMediumNotAvailable('Splinter')
            else:
                raise SearchMediumNotAvailable('PhantomJS')

    def __del__(self):
        try:
            self.browser.quit()
        except:
            pass

    def get_htmls_from_urls(self, urls):
        self.start_browser()
        for url in urls:
            self.browser.visit(url)
            time.sleep(random.randint(3, 5))
            yield self.browser.html

    def get_htmls_from_urls_use_proxy(self, urls, proxies, user_agents):
        for url in urls:
            random_proxy = random.choice(proxies)
            random_agent = random.choice(user_agents)

            self.start_browser(random_proxy, random_agent)
            self.browser.visit(url)
            time.sleep(5)
            yield self.browser.html
