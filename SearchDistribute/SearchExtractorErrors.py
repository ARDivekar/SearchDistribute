import sys
import datetime
from SearchDistribute.Enums import ProxyBrowsers

class SERPParsingException(Exception):
    def __init__(self, search_engine, parsing_stage):
        Exception.__init__(self, "%s parser is unable to obtain the %s."%(search_engine, parsing_stage))
        self.search_engine = search_engine
        self.parsing_stage = parsing_stage


class UnsupportedProxyBrowserException(Exception):
    def __init__(self, proxy_browser_type):
        Exception.__init__(self, "Invalid value %s entered for proxy_browser_type; value must from %s"%(proxy_browser_type, [x for x in ProxyBrowsers]))
        self.proxy_browser_type = proxy_browser_type



class UnsupportedFeatureException(Exception):   ## Source: https://www.codementor.io/sheena/how-to-write-python-custom-exceptions-du107ufv9#subclassing-exceptions-and-other-fancy-things
    def __init__(self, search_engine, param_name):
        error_message = "%s search engine does not support the `%s` feature (%s)"
        feature_description = None
        if param_name == "topics":
            feature_description = "topics which MAY be present in the results, outside of any quotes in the query string."
        elif param_name == "necessary_topics":
            feature_description = "topics which MUST be present in the results. Enclosed by double quotes in query string."
        elif param_name == "excluded_topics":
            feature_description = "topics which MUST be present in the results. Enclosed by double quotes in query string, prefixed by a hyphen."
        elif param_name == "necessary_sites":
            feature_description = "only search on these sites/subdomains."
        elif param_name == "excluded_sites":
            feature_description = "remove these sites from consideration."
        elif param_name == "in_url":
            feature_description = "a single word which must be in all the search result urls."
        elif param_name == "in_title":
            feature_description = "a single word which must be in title of the pages in all search result pages."
        elif param_name == "daterange":
            feature_description = "a range of dates which the search results are restricted to."
        elif param_name == "top_level_domains":
            feature_description = "top-level domains e.g. .net, .edu to which the search urls are restricted."
        elif param_name == "linked_from_page":
            feature_description = "link which must be in the content of the pages in all search result urls. e.g. all the pages with the resulting urls will link to, say, xkcd.com/493. Differs from necessary_topics"
        Exception.__init__(self, error_message = error_message%(search_engine, param_name, feature_description))
        self.param_name = param_name
        self.search_engine = search_engine


class InvalidSearchParameterException(Exception):   ## Source: https://www.codementor.io/sheena/how-to-write-python-custom-exceptions-du107ufv9#subclassing-exceptions-and-other-fancy-things
    def __init__(self, search_engine, param_name, param_value, reason):
        Exception.__init__(self, "Invalid value `%s` encountered while generating %s search query: parameter `%s` %s"%(param_value, search_engine, param_name, reason))
        self.param_name = param_name
        self.param_value = param_value
        self.search_engine = search_engine
        self.reason = reason


## The following functions are used to check arguments passed to `config` in the constructor of *SearchQuery objects,
## They raise InvalidSearchParameterExceptions for inputs which do not match cetain basic criterion.

def check_if_type_none_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type dict, raises an exception if it is not
    if param_value is None:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must not be None.")

def check_if_type_dictionary_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type dict, raises an exception if it is not
    if type(param_value) != type({}):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a dictionary.")

def check_if_type_list_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type list, raises an exception if it is not
    if type(param_value) != type([]):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a list.")

def check_if_type_list_or_tuple_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type list, raises an exception if it is not
    if type(param_value) != type([]) and type(param_value) != type(()):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a list or a tuple.")

def check_if_empty_list_or_tuple_or_dict_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is an empty list, raises an exception if it is not
    if len(param_value) == 0:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must not be an empty.")

def check_if_type_string_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type string, raises an exception if it is not
    if type(param_value) != type(""):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a string.")

def check_if_empty_string_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is an empty string, raises an exception if it is not
    if len(param_value) == 0:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must not be an empty string.")

def check_if_has_spaces_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input has spaces, raises an exception if it does
    if param_value.find(" ") != -1:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="cannot have spaces: only alphabets, numbers, hyphens, underscores and periods are permitted.")

def check_if_has_newlines_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input has newlines, raises an exception if it does
    if param_value.find("\n") != -1:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="cannot have newlines ('\\n'): only alphabets, numbers, hyphens, underscores and periods are permitted.")

def check_if_date_or_datetime_SearchQuery(search_engine, param_name, param_value):
    ## Checks if the input is of type datetime.datetime or datetime.date, raises an exception if it is not
    if type(param_value) != type(datetime.datetime.now()) and type(param_value) != type(datetime.datetime.now().date()):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be of type datetime.datetime or datetime.date.")



def make_error(class_name, function_name, description, exception_obj=None):
    error = "\nERROR in "+class_name+"."+function_name+"(): "+description
    if exception_obj is not None:
        error+= "\n"+str(exception_obj)
    return error


def make_fatal_error(class_name, function_name, description, exception_obj=None):
    error = "\nFATAL ERROR in "+class_name+"."+function_name+"(): "+description
    if exception_obj is not None:
        error+= "\n"+str(exception_obj)
    return error

def make_unimplemented_error(class_name, function_name):
    return make_fatal_error(class_name, function_name, "has not been implemented.")


def print_error(printing, class_name, function_name, description, exception_obj=None):
    error_text = make_error(class_name, function_name, description, exception_obj)
    if printing:
        print(error_text)

def print_fatal_error(printing, class_name, function_name, description, exception_obj=None):
    error_text = make_fatal_error(class_name, function_name, description, exception_obj)
    if printing:
        print(error_text)
