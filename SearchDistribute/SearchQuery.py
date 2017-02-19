
from SearchDistribute.SearchExtractorErrors import *

class SearchQueryTemplate:
    search_engine = ""          ## The search engine which we are working on.
    topics = []                 ## topics which May be present in the results.
    necessary_topics = []       ## topics which MUST be present in the results. Enclosed by double quotes in query.
    excluded_topics = []        ## topics which MUST be present in the results. Enclosed by double quotes in query, prefixed by a hyphen.
    necessary_sites = []        ## only search on these sites/subdomains.
    excluded_sites = []         ## remove these sites from consideration.
    in_url = ""                 ## a single word which must be in all the search result url.
    in_title = ""               ## a single word which must be in title of the pages in all search result pages.
    daterange = ()              ## a range of dates in which the search results must lie.

    def check_topics(self):
        check_if_type_list(self.search_engine, "topics", self.topics)
        check_if_empty_list(self.search_engine, "topics", self.topics)
        for topic in self.topics:
            check_if_type_string(self.search_engine, "topics", topic)
            topic = topic.strip()
            check_if_empty_string(self.search_engine, "topics", topic)
            check_if_has_newlines(self.search_engine, "topics", topic)

    def check_necessary_topics(self):
        check_if_type_list(self.search_engine, "necessary_topics", self.necessary_topics)
        check_if_empty_list(self.search_engine, "necessary_topics", self.necessary_topics)
        for necessary_topic in self.necessary_topics:
            check_if_type_string(self.search_engine, "necessary_topics", necessary_topic)
            necessary_topic = necessary_topic.strip()
            check_if_empty_string(self.search_engine, "necessary_topics", necessary_topic)
            check_if_has_newlines(self.search_engine, "necessary_topics", necessary_topic)

    def check_excluded_topics(self):
        check_if_type_list(self.search_engine, "excluded_topics", self.excluded_topics)
        check_if_empty_list(self.search_engine, "excluded_topics", self.excluded_topics)
        for excluded_topic in self.excluded_topics:
            check_if_type_string(self.search_engine, "excluded_topics", excluded_topic)
            excluded_topic = excluded_topic.strip()
            check_if_empty_string(self.search_engine, "excluded_topics", excluded_topic)
            check_if_has_newlines(self.search_engine, "excluded_topics", excluded_topic)

    def check_necessary_sites(self):
        check_if_type_list(self.search_engine, "necessary_sites", self.necessary_sites)
        check_if_empty_list(self.search_engine, "necessary_sites", self.necessary_sites)
        for necessary_site in self.necessary_sites:
            check_if_type_string(self.search_engine, "necessary_sites", necessary_site)
            necessary_site = necessary_site.strip()
            check_if_empty_string(self.search_engine, "necessary_sites", necessary_site)
            check_if_has_newlines(self.search_engine, "necessary_sites", necessary_site)
            check_if_has_spaces(self.search_engine, "necessary_sites", necessary_site)

    def check_excluded_sites(self):
        check_if_type_list(self.search_engine, "excluded_sites", self.excluded_sites)
        check_if_empty_list(self.search_engine, "excluded_sites", self.excluded_sites)
        for excluded_site in self.excluded_sites:
            check_if_type_string(self.search_engine, "excluded_sites", excluded_site)
            excluded_site = excluded_site.strip()
            check_if_empty_string(self.search_engine, "excluded_sites", excluded_site)
            check_if_has_newlines(self.search_engine, "excluded_sites", excluded_site)
            check_if_has_spaces(self.search_engine, "excluded_sites", excluded_site)

    def check_in_url(self):
        in_url = self.in_url
        check_if_type_string(self.search_engine, "in_url", in_url)
        in_url = in_url.strip()
        check_if_empty_string(self.search_engine, "in_url", in_url)
        check_if_has_newlines(self.search_engine, "in_url", in_url)
        check_if_has_spaces(self.search_engine, "in_url", in_url)

    def check_in_title(self):
        in_title = self.in_title
        check_if_type_string(self.search_engine, "in_title", in_title)
        in_title = in_title.strip()
        check_if_empty_string(self.search_engine, "in_title", in_title)
        check_if_has_newlines(self.search_engine, "in_title", in_title)
        check_if_has_spaces(self.search_engine, "in_title", in_title)

    def check_daterange(self):
        daterange = self.daterange
        check_if_type_list_or_tuple(self.search_engine, "daterange", daterange)
        check_if_date_or_datetime(self.search_engine, "daterange[0]", daterange[0])
        check_if_date_or_datetime(self.search_engine, "daterange[1]", daterange[1])
