from abc import ABCMeta, abstractmethod


class ProxyProvider(metaclass=ABCMeta):

    @abstractmethod
    def get_proxies(self):
        pass

    @abstractmethod
    def get_user_agents(self):
        pass