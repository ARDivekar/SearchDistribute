import sys
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
