from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time

''' Note that as of 19 Feb 2017, Firefox and Chrome do not support SOCKS5 authentication [1], but PhantomJS does [2].
[1] https://www.privateinternetaccess.com/forum/discussion/2915/setting-up-the-socks5-proxy-on-chrome-firefox
[2] http://stackoverflow.com/a/16353584/4900327  and  http://stackoverflow.com/a/26931933/4900327
'''

## For PrivateInternetAccess.com : https://www.privateinternetaccess.com/forum/discussion/258/private-internet-access-proxy-now-available-now-open
proxy_service_provider = "privateinternetaccess.com"
socks5_proxies = {
    "privateinternetaccess.com": {
        "socks5_hostname_or_ip" :   "proxy-nl.privateinternetaccess.com",
        "socks5_port" :             "1080",
        "socks5_username" :         "x1237029",
        "socks5_password" :         "3iV3za46xD"
    }
}


phantomjs_socks5_proxy_service_args = [
    '--proxy='+socks5_proxies[proxy_service_provider]["socks5_hostname_or_ip"]+':'+socks5_proxies[proxy_service_provider]["socks5_port"],
    '--proxy-type=socks5',
    '--proxy-auth='+socks5_proxies[proxy_service_provider]["socks5_username"]+':'+socks5_proxies[proxy_service_provider]["socks5_password"]
]  ## Source: http://stackoverflow.com/a/16353584/4900327

proxy_browsers = []
for i in range(0,3):
    b = webdriver.PhantomJS(service_args=phantomjs_socks5_proxy_service_args)
    print("Created browser #%s with id: %s"%(i+1, id(b)))
    proxy_browsers.append(b)

for b in proxy_browsers:
    start_time = time.time()
    b.get('https://www.whoer.net')
    end_time = time.time()
    print("Browser %s visited www.whoer.net in %.3f seconds"%(id(b), end_time-start_time))
    time.sleep(1)

for b in proxy_browsers:
    bs = BS(b.page_source)
    print("Your current IP address: %s"%(bs.find_all(class_="your-ip")[0].text))
