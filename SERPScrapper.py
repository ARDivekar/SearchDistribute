from search_medium.splinter_browser import SplinterBrowser
from proxy.default_proxy_provider import DefaultProxyProvider
from search.search_engine_provider import SearchEngineProvider
from utils.constants import SearchEngine
from utils.search_config import SearchConfig

# a lot of work is yet to be done, this is just to showcase the structure of the project
# please don't change any of the function calls in this files and expect it to work


def main():

    # building the search config
    search_config = SearchConfig()
    search_config.query = 'hello world'
    search_config.num_pages = 1
    search_config.num_results_per_page = 10

    # search engine provider
    search_engine = SearchEngineProvider(search_config, SearchEngine.BING)

    # proxy provider
    proxy_provider = DefaultProxyProvider()
    proxies = proxy_provider.get_proxies()
    user_agents = proxy_provider.get_user_agents()

    # get your preferred search medium (splinter, phantomjs, http_mode)
    search_medium = SplinterBrowser(use_phantom=False)

    # get html pages of all the urls
    url_generator = search_engine.url_builder.url_generator()
    # result_html_pages = search_medium.get_htmls_from_urls_use_proxy(url_generator, proxies, user_agents)
    result_html_generator = search_medium.get_htmls_from_urls(url_generator)

    # parse the html pages to get the desired links
    links = []
    for html_page in result_html_generator:
        links += search_engine.parser.get_urls_from_result_page(html_page)

    for link in links:
        print(link)


if __name__ == '__main__':
    main()