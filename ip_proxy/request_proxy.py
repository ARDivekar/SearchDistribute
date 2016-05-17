import requests
from requests.exceptions import ConnectionError
import random
import os
import time
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout


class RequestProxy:
    agent_file = 'user_agents.txt'

    def __init__(self):
        self.useragents = self.load_user_agents(RequestProxy.agent_file)
        #####
        # Proxy format:
        # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
        #####
        self.proxy_list = []
        self.proxy_list += self.proxyForEU_url_parser('http://proxyfor.eu/geo.php', 100.0)
        self.proxy_list += self.freeProxy_url_parser('http://free-proxy-list.net')
        print("Number of proxies found - " + str(len(self.proxy_list)))

    def load_user_agents(self, useragentsfile):
        """
        useragentfile : string
            path to text file of user agents, one per line
        """
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1-1])
        random.shuffle(useragents)
        return useragents

    def get_random_user_agent(self):
        """
        useragents : string array of different user agents
        :param useragents:
        :return random agent:
        """
        user_agent = random.choice(self.useragents)
        return user_agent

    def generate_random_request_headers(self):
        headers = {
            "User-Agent": self.get_random_user_agent()
        }  # select a random user agent
        return headers

    def proxyForEU_url_parser(self, web_url, speed_in_KBs=100.0):
        curr_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "proxy_list"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            proxy = "http://"
            proxy_straggler  = False
            for field in dataset:
                # Discard slow proxies! Speed is in KB/s
                if field[0] == 'Speed':
                    if float(field[1]) < speed_in_KBs:
                        proxy_straggler = True
                if field[0] == 'IP':
                    proxy = proxy+field[1]+':'
                elif field[0] == 'Port':
                    proxy = proxy+field[1]
            # Avoid Straggler proxies
            if not proxy_straggler:
                curr_proxy_list.append(proxy.__str__())
            #print "{0:<10}: {1}".format(field[0], field[1])
        #print "ALL: ", curr_proxy_list
        return curr_proxy_list


    def freeProxy_url_parser(self, web_url):
        curr_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "display fpltable"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            proxy = "http://"
            for field in dataset:
                if field[0] == 'IP Address':
                    proxy = proxy+field[1]+':'
                elif field[0] == 'Port':
                    proxy = proxy+field[1]
            curr_proxy_list.append(proxy.__str__())
        return curr_proxy_list

    def generate_proxied_request(self, url, req_timeout=30):

        random.shuffle(self.proxy_list)
        req_headers = self.generate_random_request_headers()
        request = None
        try:
            rand_proxy = random.choice(self.proxy_list)
            print('Trying IP', rand_proxy)
            request = requests.get(url, proxies={"https": rand_proxy, "http": rand_proxy},
                                   headers=req_headers, timeout=req_timeout)
        except ConnectionError:
            self.proxy_list.remove(rand_proxy)
            print("Proxy unreachable - Removed Struggling proxy :", rand_proxy, " PL Size = ",len(self.proxy_list))
            pass
        except ReadTimeout:
            self.proxy_list.remove(rand_proxy)
            print("Read timed out - Removed Struggling proxy :", rand_proxy, " PL Size = ", len(self.proxy_list))
            pass
        return request