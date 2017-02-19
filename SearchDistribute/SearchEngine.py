from SearchDistribute.SearchQuery import GoogleSearchQuery

class SearchEngineTemplate(object):
    pass

class Search(SearchEngineTemplate):
    search_engine = ""
    def __init__(self, search_engine):
        self.search_engine = search_engine

    def list_websites_with_top_level_domain(self, top_level_domain):
        query = GoogleSearchQuery(config={"top_level_domains": [top_level_domain], "necessary_topics":[" "]}).generate_query()