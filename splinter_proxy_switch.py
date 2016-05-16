import splinter
import time
from thread import start_new_thread

## ontainted from http://proxylist.hidemyass.com/search-1797031#listable

## HTTPS proxy:
## NOTE: Google auto-redirects HTTP to HTTPS, so only HTTPS proxies from the above link are valid.
proxyIP = '213.129.39.227'
proxyPort = 3128
def connect_splinter_proxy(url, proxyIP, proxyPort):
    proxy_settings = {'network.proxy.type': 1,
       'network.proxy.http': proxyIP,
       'network.proxy.http_port': proxyPort,
       'network.proxy.ssl': proxyIP,
       'network.proxy.ssl_port':proxyPort,
       'network.proxy.socks': proxyIP,
       'network.proxy.socks_port':proxyPort,
       'network.proxy.ftp': proxyIP,
       'network.proxy.ftp_port':proxyPort
    }
    b= splinter.Browser(profile_preferences=proxy_settings)
    time.sleep(5)
    b.visit(url)

start_new_thread(connect_splinter_proxy('https://whoer.net', proxyIP, proxyPort))
start_new_thread(connect_splinter_proxy('https://www.google.com/search?q=whats+my+ip', proxyIP, proxyPort))
raw_input("\nEnter anything to quit:\n>")


