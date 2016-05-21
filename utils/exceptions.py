class SearchMediumNotAvailable(Exception):

    def __init__(self, medium):
        Exception.__init__(self, 'Splinter not available:', medium)
