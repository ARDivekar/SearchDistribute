from search.parser import GoogleParser, BingParser
from search.url_builder import GoogleUrlBuilder, BingUrlBuilder
from utils.constants import SearchEngine


class SearchEngineProvider:

    def __init__(self, search_config, search_engine_name=SearchEngine.GOOGLE):
        self.parser = None
        self.url_builder = None

        if search_engine_name == SearchEngine.GOOGLE:
            self.parser = GoogleParser()
            self.url_builder = GoogleUrlBuilder(search_config)

        elif search_engine_name == SearchEngine.BING:
            self.parser = BingParser()
            self.url_builder = BingUrlBuilder(search_config)