from enum import Enum


class SearchEngine(Enum):
    GOOGLE = 'search.google'
    BING = 'search.bing'


class AvailableSearchMediums(Enum):
    SPLINTER = 'medium.splinter'
    PHANTOM = 'medium.phantom'
    HTTP_MODE = 'medium.http_mode'
