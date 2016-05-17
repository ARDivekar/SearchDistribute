from request_proxy import RequestProxy
from bs4 import BeautifulSoup

# This script uses public proxies. So do not expect blazing fast responses.
# Websites used to collect these proxies are
# http://proxyfor.eu/geo.php
# http://free-proxy-list.net
# There are usually around 300 available proxies combined. But during testing I found many of them are unreachable

def main():
    print("Initializing proxy list. Please wait")
    req_proxy = RequestProxy()
    print('Done initializing proxy list')
    request = None
    while not request:
        request = req_proxy.generate_proxied_request('https://whoer.net/', 30)
    if request:
        print('Finding ip using whoer.net')
        bs = BeautifulSoup(request.text, "html.parser")
        print('Your IP ' + bs.find_all(attrs={"class":"your-ip"})[0].text)
        print('Your location ' + bs.find_all(attrs={"class": "cont offDate overdots"})[0].text)
        open('ip_using_whoer.html', 'w').write(request.text)
        print('Webpage saved at ip_using_whoer.html')


if __name__ == '__main__':
    main()
