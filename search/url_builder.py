from abc import ABCMeta, abstractmethod
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlunsplit


class UrlBuilder(metaclass=ABCMeta):

    def __init__(self, search_config):
        self.search_config = search_config

    @abstractmethod
    def _page_url(self, page_number):
        pass

    @abstractmethod
    def _build_query_string(self, search_config):
        pass

    def url_generator(self):
        for i in range(0, self.search_config.num_pages):
            page_url = self._page_url(i)
            yield page_url


class GoogleUrlBuilder(UrlBuilder):

    def __init__(self, search_config):
        super().__init__(search_config)
        self.scheme = 'https'
        self.netloc = 'www.google.com'
        self.path = '/search'
        self.query_string = self._build_query_string(search_config)
        self.fragment = ''

    def _page_url(self, page_number):
        # page_number starts from 0
        params = parse_qs(self.query_string)
        params['start'] = str(page_number) + '0'
        self.query_string = urlencode(params, doseq=True)

        return urlunsplit((self.scheme, self.netloc, self.path, self.query_string, self.fragment))

    def _build_query_string(self, search_config):
        # TODO implement this properly
        return 'q=hello&gws_rd=ssl'


class BingUrlBuilder(UrlBuilder):

    def __init__(self, search_config):
        super().__init__(search_config)
        self.scheme = 'https'
        self.netloc = 'www.bing.com'
        self.path = '/search'
        self.query_string = self._build_query_string(search_config)
        self.fragment = ''

    def _page_url(self, page_number):
        # page_number starts from 0
        params = parse_qs(self.query_string)
        params['first'] = str(page_number) + '1'
        self.query_string = urlencode(params, doseq=True)

        return urlunsplit((self.scheme, self.netloc, self.path, self.query_string, self.fragment))

    def _build_query_string(self, search_config):
        # TODO implement this properly
        return 'q=hello'


