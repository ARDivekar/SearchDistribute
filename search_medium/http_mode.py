from search_medium.search_medium import SearchMedium

class HTTPMode(SearchMedium):

    def get_html_from_url(self, url):
        raise NotImplementedError()

    def get_htmls_from_urls(self, urls):
        raise NotImplementedError()