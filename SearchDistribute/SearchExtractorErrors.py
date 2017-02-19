import sys
import datetime

class InvalidSearchParameterException(Exception):   ## Source: https://www.codementor.io/sheena/how-to-write-python-custom-exceptions-du107ufv9#subclassing-exceptions-and-other-fancy-things
    def __init__(self, search_engine, param_name, param_value, reason):
        Exception.__init__(self, "Invalid value `%s` encountered while generating %s search query: parameter `%s` %s"%(param_value, search_engine, param_name, reason))
        self.param_name = param_name
        self.param_value = param_value
        self.search_engine = search_engine
        self.reason = reason

def check_if_type_list(search_engine, param_name, param_value):
    ## Checks if the input is of type list, raises an exception if it is not
    if type(param_value) != type([1]):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a list.")

def check_if_type_list_or_tuple(search_engine, param_name, param_value):
    ## Checks if the input is of type list, raises an exception if it is not
    if type(param_value) != type([1]) and type(param_value) != type((1)):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a list or a tuple.")

def check_if_empty_list(search_engine, param_name, param_value):
    ## Checks if the input is an empty list, raises an exception if it is not
    if len(param_value) == 0:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must not be an empty list.")

def check_if_type_string(search_engine, param_name, param_value):
    ## Checks if the input is of type string, raises an exception if it is not
    if type(param_value) != type(""):
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must be a string.")

def check_if_empty_string(search_engine, param_name, param_value):
    ## Checks if the input is an empty string, raises an exception if it is not
    if len(param_value) == 0:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="must not be an empty string.")

def check_if_has_spaces(search_engine, param_name, param_value):
    ## Checks if the input has spaces, raises an exception if it does
    if param_value.find(" ") != -1:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="cannot have spaces: only alphabets, numbers, hyphens, underscores and periods are permitted.")

def check_if_has_newlines(search_engine, param_name, param_value):
    ## Checks if the input has newlines, raises an exception if it does
    if param_value.find("\n") != -1:
        raise InvalidSearchParameterException(
            search_engine=search_engine,
            param_name=param_name,
            param_value=param_value,
            reason="cannot have newlines ('\\n'): only alphabets, numbers, hyphens, underscores and periods are permitted.")

def check_if_date_or_datetime(search_engine, param_name, param_value):
    ## Checks if the input is of type datetime.datetime or datetime.date, raises an exception if it is not
    if type(param_value) != type(datetime.datetime.now()) and type(param_value) != type(datetime.datetime.now().date):
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
