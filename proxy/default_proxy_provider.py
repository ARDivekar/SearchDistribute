from proxy.proxy_provider import ProxyProvider
import os


class DefaultProxyProvider(ProxyProvider):

    def __init__(self):
        self.proxy_file = os.path.abspath('proxy/proxies.txt')
        self.user_agents_file = os.path.abspath('proxy/user_agents.txt')

    def get_user_agents(self):
        user_agents = []
        with open(self.user_agents_file, 'r') as f:
            for user_agent in f.readlines():
                user_agents.append(user_agent.rstrip().replace('"', ''))
        return user_agents

    def get_proxies(self):
        proxies = []
        with open(self.proxy_file, 'r') as f:
            for proxy in f.readlines():
                proxy = proxy.rstrip()
                proxy_ip, proxy_port = proxy.split()
                proxies.append({'ip': proxy_ip, 'port': int(proxy_port)})
        return proxies