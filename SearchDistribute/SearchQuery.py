from SearchDistribute.SearchExtractorErrors import *
from jdcal import gcal2jd
import random

def _convert_to_julian_date(self, d):
    ## takes as input a datetime.datetime or datetime.date object
    jd_tuple = gcal2jd(d.year, d.month, d.day)
    julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
    return int(julian_day)


class SearchQueryTemplate(object):
    ## SearchQueryTemplate must, at every time, have a complete list of all possible parameters that can be passed to any *SearchQuery object.
    search_engine = ""          ## The search engine which we are working on.
    topics = []                 ## topics which May be present in the results.
    necessary_topics = []       ## topics which MUST be present in the results. Enclosed by double quotes in query.
    excluded_topics = []        ## topics which MUST be present in the results. Enclosed by double quotes in query, prefixed by a hyphen.
    necessary_sites = []        ## only search on these sites/subdomains.
    excluded_sites = []         ## remove these sites from consideration.
    in_url = ""                 ## a single word which must be in all the search result url.
    in_title = ""               ## a single word which must be in title of the pages in all search result pages.
    daterange = ()              ## a range of dates in which the search results must lie.

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


    def check_topics(self):
        '''`topics` must be a non-empty list of strings, each string must not be empty and cannot have newlines.
        Throws a InvalidSearchParameterException if these rules are not followed.
        '''
        check_if_type_list(self.search_engine, "topics", self.topics)
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
        check_if_type_list(self.search_engine, "necessary_topics", self.necessary_topics)
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
        check_if_type_list(self.search_engine, "excluded_topics", self.excluded_topics)
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
        check_if_type_list(self.search_engine, "necessary_sites", self.necessary_sites)
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
        check_if_type_list(self.search_engine, "excluded_sites", self.excluded_sites)
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






        if (self.necessaryTopicsList is None or self.necessaryTopicsList == []) and (
                        self.fuzzyTopicsList is None or self.fuzzyTopicsList == []):  ## there are no topics in the GoogleSearchQuery object.
            return ""

        queryList = []

        if self.siteList is not None and self.siteList != []:
            siteString = ""
            siteString += 'site:' + self.siteList[0]
            for i in range(1, len(self.siteList)):
                siteString += ' | site:' + self.siteList[i]
            siteString = siteString.strip()
            queryList.append(siteString)

        topicString = ""
        if self.necessaryTopicsList is not None and self.necessaryTopicsList != []:
            necessaryTopicString = ""
            for topic in self.necessaryTopicsList:
                necessaryTopicString += ' "%s"' % topic
            necessaryTopicString = necessaryTopicString.strip()
            topicString += necessaryTopicString + " "

        if self.fuzzyTopicsList is not None and self.fuzzyTopicsList != []:
            fuzzyTopicString = ""
            for topic in self.fuzzyTopicsList:
                fuzzyTopicString += ' %s' % topic
            fuzzyTopicString = fuzzyTopicString.strip()
            topicString += fuzzyTopicString

        queryList.append(topicString)

        if self.inurl is not None and self.inurl != "":
            queryList.append('inurl:%s' % self.inurl)

        if self.daterangeFrom is not None and self.daterangeTo is not None and type(self.daterangeFrom) == type(
                0) and type(self.daterangeTo) == type(
                0) and self.daterangeFrom != -1 and self.daterangeTo != -1 and self.daterangeFrom <= self.daterangeFrom:
            queryList.append('daterange:%s-%s' % (self.daterangeFrom, self.daterangeTo))

        # print(queryList)
        queryList = [i.strip() for i in queryList]

        if randomShuffle:
            random.shuffle(queryList)

        query = ' '.join(queryList)
        query = query.strip()

        return query



class GoogleSearchQuery(SearchQueryTemplate):
    search_engine = "Google"

    ## this function returns a string from the query object parameters.
    ## This must be implemented separatelty for each search engine as the name of the fields differs between search engines.

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
                    site_str += "site:%s"%necessary_site
                else:
                    site_str += " | site:%s" % necessary_site
            query_parts.append(site_str.strip())

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






