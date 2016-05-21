from abc import ABCMeta, abstractmethod
import bs4


class Parser(metaclass=ABCMeta):

    def __init__(self):
        self.container_attr = None

    def get_urls_from_result_page(self, html):
        bs = bs4.BeautifulSoup(html, 'html.parser')
        url_containers = bs.find_all(attrs={"class": self.container_attr})

        urls = []
        for container in url_containers:
            urls.append(container.find('a')['href'])
        return urls

class BingParser(Parser):

    def __init__(self):
        super().__init__()
        self.container_attr = 'b_algo'


class GoogleParser(Parser):

    def __init__(self):
        super().__init__()
        self.container_attr = 'r'


class DuckDuckGoParser(Parser):

    def __init__(self):
        super().__init__()
        self.container_attr = 'result__title'
