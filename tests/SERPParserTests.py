import sys
sys.path.append("..")
from SearchDistribute.SERPParser import GoogleParser
import io

html = ""
with io.open('google_serp.html', 'r') as inp:
    html = inp.read()
parsed_google_serp = GoogleParser(
    html = html,
    current_url="https://www.google.co.in/search?q=the+ceshire+cat&oq=the+ceshire+cat&aqs=chrome..69i57j0l5.10716j0j1&sourceid=chrome&ie=UTF-8#q=the+cheshire+cat",
    start_offset=0
)

def test_google_parser_result_urls():   ## Note: http://stackoverflow.com/a/35964901/4900327
    assert parsed_google_serp.results == ('https://en.wikipedia.org/wiki/Cheshire_Cat', 'http://aliceinwonderland.wikia.com/wiki/The_Cheshire_Cat', 'http://disney.wikia.com/wiki/Cheshire_Cat', 'http://www.alice-in-wonderland.net/resources/analysis/character-descriptions/cheshire-cat/', 'https://www.youtube.com/watch?v=G4fHre-yRPY', 'https://www.youtube.com/watch?v=TFqjA2aOe_I', 'https://www.pinterest.com/explore/cheshire-cat/', 'https://www.pinterest.com/explore/cheshire-cat-quotes/', 'http://www.imdb.com/character/ch0012248/quotes', 'http://www.shmoop.com/alice-in-wonderland-looking-glass/cheshire-cat.html')

def test_google_parser_domain():
    assert parsed_google_serp.domain == "google.co.in"

def test_google_parser_link_to_previous_page():
    assert parsed_google_serp.link_to_previous_page == None

def test_google_parser_links_to_previous_pages():
    assert parsed_google_serp.links_to_previous_pages == None

def test_google_parser_links_to_next_pages():
    assert parsed_google_serp.links_to_next_pages == ['https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=10&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=20&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=30&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=40&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=50&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=60&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=70&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=80&sa=N', 'https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=90&sa=N']

def test_google_parser_link_to_next_page():
    assert parsed_google_serp.link_to_next_page == "https://www.google.co.in/search?q=the+cheshire+cat&biw=1366&bih=596&ei=T4msWJWqN8LevgSx8qroDg&start=10&sa=N"
