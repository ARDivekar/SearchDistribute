from SearchDistribute.SearchExtractorErrors import *
from jdcal import gcal2jd
import random

def _convert_to_julian_date(self, d):
    ## takes as input a datetime.datetime or datetime.date object
    jd_tuple = gcal2jd(d.year, d.month, d.day)
    julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
    return int(julian_day)


class SearchQueryTemplate(object):
    search_engine = ""          ## The search engine which we are working on.
    ## SearchQueryTemplate must, at every time, have a complete list of all possible parameters that can be passed to any *SearchQuery object.
    topics = []                 ## topics which MAY be present in the results, outside of any quotes in the query string.
    necessary_topics = []       ## topics which MUST be present in the results. Enclosed by double quotes in query string.
    excluded_topics = []        ## topics which MUST be present in the results. Enclosed by double quotes in query string, prefixed by a hyphen.
    necessary_sites = []        ## only search on these sites/subdomains.
    excluded_sites = []         ## remove these sites from consideration.
    in_url = ""                 ## a single word which must be in all the search result urls.
    in_title = ""               ## a single word which must be in title of the pages in all search result urls.
    daterange = ()              ## a range of dates which the search results are restricted to.
    top_level_domains = []      ## top-level domains which the search urls are restricted to e.g. .net, .edu
    linked_from_page = ""       ## link which must be in the content of the pages in all search result urls. e.g. all the pages with the resulting urls will link to, say, xkcd.com/493. Differs from necessary_topics.

    ## IMPORTANT: When a new field is added to the list above, we must also correspondingly add it to:
    ##  - SearchQuery.py : SearchQueryTemplate.__init__(...)
    ##  - GoogleSearchQuery.generate_query(), BingSearchQuery.generate_query(), etc.
    ##  - (Maybe) GoogleSearchQuery.__init__(), BingSearchQuery.__init__(), etc.
    ##  and
    ##  - SearchExtractorErrors.py : UnsupportedFeatureException.__init__(...)

    def __init__(self, config={}):
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "config", config)
        check_if_type_dictionary(self.search_engine, "config", config)
        check_if_type_none(self.search_engine, "config", config)

        config_chooser = lambda x, y: config.get(x) if config.get(x) is not None else config.get(y)
        ## This function looks for two alternative spellings of a field in the dictionary. It prefers the one with underscores.
        ## If neither exist, the self.* value becomes None, and must be handled.
        self.topics = config_chooser('topics', 'Topics')
        self.necessary_topics = config_chooser('necessary_topics', 'necessaryTopics')
        self.excluded_topics = config_chooser('excluded_topics', 'excludedTopics')
        self.necessary_sites = config_chooser('necessary_sites', 'necessarySites')
        self.excluded_sites = config_chooser('excluded_sites', 'excludedSites')
        self.in_url = config_chooser('in_url', 'inurl')
        self.in_title = config_chooser('in_title', 'intitle')
        self.daterange = config_chooser('date_range', 'daterange')
        self.top_level_domains = config_chooser('top_level_domains', 'topLevelDomains')
        self.linked_from_page = config_chooser('linked_from_page', 'linkedFromPage')


    def check_topics(self):
        '''`topics` must be a non-empty list of strings, each string must not be empty and cannot have newlines.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "topics", self.topics)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "topics", self.topics)
        for topic in self.topics:
            check_if_type_string(self.search_engine, "topics", topic)
            topic = topic.strip()
            check_if_empty_string(self.search_engine, "topics", topic)
            check_if_has_newlines(self.search_engine, "topics", topic)

    def check_necessary_topics(self):
        '''`necessary_topics` must be a non-empty list of strings, each string must not be empty and cannot have newlines.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "necessary_topics", self.necessary_topics)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "necessary_topics", self.necessary_topics)
        for necessary_topic in self.necessary_topics:
            check_if_type_string(self.search_engine, "necessary_topics", necessary_topic)
            necessary_topic = necessary_topic.strip()
            check_if_empty_string(self.search_engine, "necessary_topics", necessary_topic)
            check_if_has_newlines(self.search_engine, "necessary_topics", necessary_topic)

    def check_excluded_topics(self):
        '''`excluded_topics` must be a non-empty list of strings, each string must not be empty and cannot have newlines.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "excluded_topics", self.excluded_topics)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "excluded_topics", self.excluded_topics)
        for excluded_topic in self.excluded_topics:
            check_if_type_string(self.search_engine, "excluded_topics", excluded_topic)
            excluded_topic = excluded_topic.strip()
            check_if_empty_string(self.search_engine, "excluded_topics", excluded_topic)
            check_if_has_newlines(self.search_engine, "excluded_topics", excluded_topic)

    def check_necessary_sites(self):
        '''`necessary_sites` must be a non-empty list of strings, each string must not be empty and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "necessary_sites", self.necessary_sites)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "necessary_sites", self.necessary_sites)
        for necessary_site in self.necessary_sites:
            check_if_type_string(self.search_engine, "necessary_sites", necessary_site)
            necessary_site = necessary_site.strip()
            check_if_empty_string(self.search_engine, "necessary_sites", necessary_site)
            check_if_has_newlines(self.search_engine, "necessary_sites", necessary_site)
            check_if_has_spaces(self.search_engine, "necessary_sites", necessary_site)

    def check_excluded_sites(self):
        '''`excluded_sites` must be a non-empty list of strings, each string must not be empty and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "excluded_sites", self.excluded_sites)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "excluded_sites", self.excluded_sites)
        for excluded_site in self.excluded_sites:
            check_if_type_string(self.search_engine, "excluded_sites", excluded_site)
            excluded_site = excluded_site.strip()
            check_if_empty_string(self.search_engine, "excluded_sites", excluded_site)
            check_if_has_newlines(self.search_engine, "excluded_sites", excluded_site)
            check_if_has_spaces(self.search_engine, "excluded_sites", excluded_site)

    def check_in_url(self):
        '''`in_url` must be a non-empty string and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        in_url = self.in_url
        check_if_type_string(self.search_engine, "in_url", in_url)
        in_url = in_url.strip()
        check_if_empty_string(self.search_engine, "in_url", in_url)
        check_if_has_newlines(self.search_engine, "in_url", in_url)
        check_if_has_spaces(self.search_engine, "in_url", in_url)

    def check_in_title(self):
        '''`in_title` must be a non-empty string and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        in_title = self.in_title
        check_if_type_string(self.search_engine, "in_title", in_title)
        in_title = in_title.strip()
        check_if_empty_string(self.search_engine, "in_title", in_title)
        check_if_has_newlines(self.search_engine, "in_title", in_title)
        check_if_has_spaces(self.search_engine, "in_title", in_title)

    def check_daterange(self):
        '''`daterange` must be a 2-tuple of datetime.datetime or datetime.date objects.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        daterange = self.daterange
        check_if_type_list_or_tuple(self.search_engine, "daterange", daterange)
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "daterange", daterange)
        check_if_date_or_datetime(self.search_engine, "daterange[0]", daterange[0])
        check_if_date_or_datetime(self.search_engine, "daterange[1]", daterange[1])

    def check_top_level_domains(self):
        '''`top_level_domains` must be a non-empty list of strings, each string must not be empty and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "top_level_domains", self.top_level_domains)   ## Must be a list because we may random.shuffle(...) it later.
        check_if_empty_list_or_tuple_or_dict(self.search_engine, "top_level_domains", self.top_level_domains)
        for top_level_domain in self.top_level_domains:
            check_if_empty_string(self.search_engine, "top_level_domains", top_level_domain)
            check_if_has_newlines(self.search_engine, "top_level_domains", top_level_domain)
            check_if_has_spaces(self.search_engine, "top_level_domains", top_level_domain)

    def check_linked_from_page(self):
        '''`in_title` must be a non-empty string and cannot have newlines or spaces; only letters, hyphens, periods and underscores are permitted.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        linked_from_page = self.linked_from_page
        check_if_type_string(self.search_engine, "linked_from_page", linked_from_page)
        in_title = linked_from_page.strip()
        check_if_empty_string(self.search_engine, "linked_from_page", linked_from_page)
        check_if_has_newlines(self.search_engine, "linked_from_page", linked_from_page)
        check_if_has_spaces(self.search_engine, "linked_from_page", linked_from_page)


    def generate_query(self, random_shuffle=True, random_spaces=True):
        ## Each subclass MUST implement this in order to call generate_query()
        raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

    def __str__(self, random_shuffle=True, random_spaces=True):
        return self.generate_query(random_shuffle, random_spaces)





class GoogleSearchQuery(SearchQueryTemplate):
    search_engine = "Google"

    ## this function returns a string from the query object parameters.
    ## This must be implemented separatelty for each search engine as the name of the fields differs between search engines.
    def __init__(self, config={}):
        config_chooser = lambda x, y: config.get(x) if config.get(x) is not None else config.get(y)
        super().__init__(config)


    def generate_query(self, random_shuffle=True, random_spaces = True):
        query_parts = []

        if self.topics is not None:
            if random_shuffle:
                random.shuffle(self.topics)
            self.check_topics()
            query_parts += [topic.strip() for topic in self.topics]

        if self.necessary_topics is not None:
            if random_shuffle:
                random.shuffle(self.necessary_topics)
            self.check_necessary_topics()
            query_parts += ['"%s"'%necessary_topic.strip() for necessary_topic in self.necessary_topics]

        if self.excluded_topics is not None:
            if random_shuffle:
                random.shuffle(self.excluded_topics)
            self.check_excluded_topics()
            query_parts += ['-"%s"'%excluded_topic.strip() for excluded_topic in self.excluded_topics]

        if self.necessary_sites is not None:
            site_str = ""
            if random_shuffle:
                random.shuffle(self.necessary_sites)
            self.check_necessary_sites()
            for i in range(0, len(self.necessary_sites)):
                necessary_site = self.necessary_sites[i].strip()
                if i==0:
                    site_str += "site:%s" % necessary_site
                else:
                    site_str += " | site:%s" % necessary_site
            query_parts.append(site_str.strip())

        if self.top_level_domains is not None:
            domain_str = ""
            if random_shuffle:
                random.shuffle(self.top_level_domains)
            self.check_top_level_domains()
            for i in range(0, len(self.top_level_domains)):
                top_level_domain = self.top_level_domains[i].strip()
                if top_level_domain.startswith('.') == False and top_level_domain.startswith('*.') == False:
                    raise InvalidSearchParameterException(
                        search_engine=self.search_engine,
                        param_name="top_level_domains",
                        param_value=top_level_domain,
                        reason="must be of the format .xyz or *.xyz  e.g. *.edu or .com")
                if i==0:
                    domain_str += "site:%s" % top_level_domain
                else:
                    domain_str += " | site:%s" % top_level_domain
            query_parts.append(domain_str.strip())

        if self.excluded_sites is not None:
            if random_shuffle:
                random.shuffle(self.excluded_sites)
            self.check_excluded_sites()
            query_parts += ['-"%s"'%excluded_site.strip() for excluded_site in self.excluded_sites]

        if self.in_url is not None:
            self.check_in_url()
            query_parts.append("inurl:%s"%self.in_url.strip())

        if self.in_title is not None:
            self.check_in_title()
            query_parts.append("intitle:%s"%self.in_title.strip())

        if self.linked_from_page is not None:
            self.check_linked_from_page()
            query_parts.append("link:%s" % self.linked_from_page.strip())

        if self.daterange is not None:
            self.check_daterange()
            query_parts.append('daterange:%s-%s' % (_convert_to_julian_date(self.daterange[0]), _convert_to_julian_date(self.daterange[0])))


        if random_shuffle:
            random.shuffle(query_parts)

        query = ""
        if random_spaces:
            ## Adds random spaces to the query string with a particular frequency
            for query_part in query_parts:
                r = random.randrange(0, 10)
                if 0<=r and r<=6:   ## 70% of the time, add a normal single space
                    query += " %s"%query_part
                elif 7<=r and r<=8:   ## 20% of the time, add two spaces
                    query += "  %s"%query_part
                elif r==9:   ## 10% of the time, add three spaces
                    query += "   %s"%query_part
                query += " "*random.randrange(0, 2) ## 50% of the time, add a random space at the end.
        else:
            query = ' '.join(query_parts)
        return query






