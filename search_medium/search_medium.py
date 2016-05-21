from abc import ABCMeta, abstractmethod


class SearchMedium(metaclass=ABCMeta):

    @abstractmethod
    def get_html_from_url(self, url):
        pass

    @abstractmethod
    def get_htmls_from_urls(self, urls):
        pass

    @abstractmethod
    def get_htmls_from_urls_use_proxy(self, urls, proxies, user_agents):
        pass
