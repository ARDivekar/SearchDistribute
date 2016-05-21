import os


class ProxyProvider:

    def __init__(self, proxy_file='proxy/proxies.txt', user_agents_file='proxy/user_agents.txt'):
        self.proxy_file = proxy_file
        self.user_agents_file = user_agents_file

    def get_user_agents(self):
        user_agents = []
        with open(self.user_agents_file, 'r') as f:
            for user_agent in f.readlines():
                user_agents.append(user_agent.rstrip())
        return user_agents

    def get_proxies(self):
        proxies = []
        with open(self.proxy_file, 'r') as f:
            for proxy in f.readlines():
                proxy = proxy.rstrip()
                proxy_ip, proxy_port = proxy.split()
                proxies.append({'ip': proxy_ip, 'port': int(proxy_port)})
        return proxies