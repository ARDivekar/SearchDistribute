from utils.constants import AvailableSearchMediums
from search_medium.splinter_browser import SplinterBrowser
from search_medium.http_mode import HTTPMode


def get_search_medium(search_medium=AvailableSearchMediums.SPLINTER):
        if search_medium == AvailableSearchMediums.SPLINTER:
            return SplinterBrowser(use_phantom=False)
        if search_medium == AvailableSearchMediums.PHANTOM:
            return SplinterBrowser(use_phantom=True)
        if search_medium == AvailableSearchMediums.HTTP_MODE:
            return HTTPMode()