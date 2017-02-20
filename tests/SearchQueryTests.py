## Run this file as: go to the command line and type: `py.test SearchQueryTests.py`. You must have the pytest module installed.

import sys
sys.path.append("..")
from SearchDistribute.SearchQuery import GoogleSearchQuery as GSQ

from datetime import date


def test_gsq_topic():
    assert str(GSQ({"topics": 'man'})) == 'man'
    assert str(GSQ({"topics": ['man']})) == 'man'
    assert str(GSQ({"topics": ['man', 'candle']})) == 'man candle'
    assert str(GSQ({"topics": ['man', 'candle lama']})) == 'man candle lama'
    assert str(GSQ({"topics": ['man', ' candle lama']})) == 'man candle lama'
    assert str(GSQ({"topics": ['man', 'candle lama ']})) == 'man candle lama'
    assert str(GSQ({"topics": ['man', 'candle  lama']})) == 'man candle  lama'
    assert str(GSQ({"topics": ['man', ' candle  lama']})) == 'man candle  lama'
    assert str(GSQ({"topics": ['man', 'candle  lama']})) != 'man candle  lama '
    assert str(GSQ({"topics": ['man', 'candle  lama']})) != ' man candle  lama'
    assert str(GSQ({"topics": ['man', 'candle  lama']})) != ' man candle  lama '

def test_gsq_necessary_topics():
    assert str(GSQ({"necessary_topics": "pay the piper"})) == '"pay the piper"'
    assert str(GSQ({"necessary_topics": ["pay the piper"]})) == '"pay the piper"'
    assert str(GSQ({"necessary_topics": ["lama", "pay the piper"]})) == '"lama" "pay the piper"'
    assert str(GSQ({"necessary_topics": ["lama", " pay the piper"]})) == '"lama" "pay the piper"'
    assert str(GSQ({"topics": ['man'], "necessary_topics": ["lama", "pay the piper"]})) == 'man "lama" "pay the piper"'

def test_gsq_top_excluded_topics():
    assert str(GSQ({"excluded_topics": 'man'})) == '-man'
    assert str(GSQ({"excluded_topics": ['man']})) == '-man'
    assert str(GSQ({"excluded_topics": ['man', 'super']})) == '-man -super'
    assert str(GSQ({"excluded_topics": ['super man']})) == '-"super man"'
    assert str(GSQ({"excluded_topics": ['man'], "necessary_topics": ["lama", "pay the piper"]})) == '"lama" "pay the piper" -man'
    assert str(GSQ({"excluded_topics": ['man'], "topics":["sandman"], "necessary_topics": ["lama", "pay the piper"]})) == 'sandman "lama" "pay the piper" -man'

def test_gsq_necessary_sites():
    assert str(GSQ({"necessary_sites": 'www.reddit.com'})) == 'site:www.reddit.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com']})) == 'site:www.reddit.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com'], "topics":['la la land']})) == 'la la land site:www.reddit.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com'], "necessary_topics": ['la la land']})) == '"la la land" site:www.reddit.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com'], "topics":['save'], "necessary_topics": ['la la land']})) == 'save "la la land" site:www.reddit.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com', 'xkcd.com'], "necessary_topics": ['la la land']})) == '"la la land" site:www.reddit.com | site:xkcd.com'
    assert str(GSQ({"necessary_sites": ['www.reddit.com', 'xkcd.com', 'http://google-mountain-view.io'], "necessary_topics": ['la la land']})) == '"la la land" site:www.reddit.com | site:xkcd.com | site:http://google-mountain-view.io'
    assert str(GSQ({"necessary_sites": ['www.reddit.com', 'xkcd.com', 'http://google-mountain-view.io', 'https://www.braveheart.com'], "necessary_topics": ['la la land']})) == '"la la land" site:www.reddit.com | site:xkcd.com | site:http://google-mountain-view.io | site:https://www.braveheart.com'

def test_gsq_excluded_sites():
    assert str(GSQ({"excluded_sites": 'www.reddit.com'})) == '-"www.reddit.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com']})) == '-"www.reddit.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com'], "topics":['la la land']})) == 'la la land -"www.reddit.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com'], "necessary_topics": ['la la land']})) == '"la la land" -"www.reddit.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com'], "topics":['save'], "necessary_topics": ['la la land']})) == 'save "la la land" -"www.reddit.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com', 'xkcd.com'], "necessary_topics": ['la la land']})) == '"la la land" -"www.reddit.com" -"xkcd.com"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com', 'xkcd.com', 'http://google-mountain-view.io'], "necessary_topics": ['la la land']})) == '"la la land" -"www.reddit.com" -"xkcd.com" -"http://google-mountain-view.io"'
    assert str(GSQ({"excluded_sites": ['www.reddit.com', 'xkcd.com', 'http://google-mountain-view.io', 'https://www.braveheart.com/loonies'], "necessary_topics": ['la la land']})) == '"la la land" -"www.reddit.com" -"xkcd.com" -"http://google-mountain-view.io" -"https://www.braveheart.com/loonies"'

def test_gsq_in_url():
    assert str(GSQ({"in_url": 'infosys'})) == 'inurl:infosys'
    assert str(GSQ({"in_url": ['infosys', 'lamport']})) == 'inurl:infosys | inurl:lamport'
    assert str(GSQ({"in_url": ['infosys', 'lamport'], "topics":['salamander']})) == 'salamander inurl:infosys | inurl:lamport'
    assert str(GSQ({"in_url": ['infosys', 'lamport'], "topics": ['salamander'], "necessary_topics": ['zuccini']})) == 'salamander "zuccini" inurl:infosys | inurl:lamport'
    assert str(GSQ({"in_url": ['infosys', 'lamport'], "topics": ['salamander'], "necessary_topics": ['zuccini'], "necessary_sites":["xkcd.com", "www.bestcooks.com/salamander"]})) == 'salamander "zuccini" site:xkcd.com | site:www.bestcooks.com/salamander inurl:infosys | inurl:lamport'

def test_gsq_in_title():
    assert str(GSQ({"in_title": 'infosys'})) == 'intitle:infosys'
    assert str(GSQ({"in_title": ['infosys', 'lamport', 'socrates']})) == 'intitle:infosys | intitle:lamport | intitle:socrates'
    assert str(GSQ({"in_title": ['infosys', 'lamport', 'socrates'], "topics":['salamander']})) == 'salamander intitle:infosys | intitle:lamport | intitle:socrates'
    assert str(GSQ({"in_title": ['infosys', 'lamport', 'socrates'], "topics": ['salamander'], "necessary_topics": ['zuccini']})) == 'salamander "zuccini" intitle:infosys | intitle:lamport | intitle:socrates'
    assert str(GSQ({"in_title": ['infosys', 'lamport', 'socrates'], "topics": ['salamander'], "necessary_topics": ['zuccini'], "necessary_sites":["xkcd.com", "www.bestcooks.com/salamander"]})) == 'salamander "zuccini" site:xkcd.com | site:www.bestcooks.com/salamander intitle:infosys | intitle:lamport | intitle:socrates'


def test_gsq_top_level_domains():
    assert str(GSQ({"top_level_domains": '.com'})) == 'site:.com'
    assert str(GSQ({"top_level_domains": ['.club']})) == 'site:.club'
    assert str(GSQ({"top_level_domains": ['.club', '*.io']})) == 'site:.club | site:*.io'
    assert str(GSQ({"top_level_domains": ['.club', '*.io'], "in_title": 'infosys', "topics":['salamander']})) == 'salamander site:.club | site:*.io intitle:infosys'
    assert str(GSQ({"top_level_domains": ['.club', '*.io', '.com'], "in_title": 'infosys', "topics": ['salamander'], "necessary_topics": ['zuccini']})) == 'salamander "zuccini" site:.club | site:*.io | site:.com intitle:infosys'
    assert str(GSQ({"top_level_domains": ['.club', '*.io', '.com'], "in_title": 'infosys', "topics": ['salamander'], "necessary_topics": ['zuccini'], "necessary_sites":['xkcd.com']})) == 'salamander "zuccini" site:xkcd.com | site:.club | site:*.io | site:.com intitle:infosys'
    assert str(GSQ({"top_level_domains": ['.club', '*.io', '.com'], "in_title": 'infosys', "topics": ['salamander'], "necessary_topics": ['zuccini'], "necessary_sites": ['xkcd.com', "semperfi.net/veterans"]})) == 'salamander "zuccini" site:xkcd.com | site:semperfi.net/veterans | site:.club | site:*.io | site:.com intitle:infosys'
    assert str(GSQ({"top_level_domains": ['.club', '*.io', '.com'], "in_title": 'infosys', "topics": ['salamander'], "necessary_topics": ['zuccini'], "necessary_sites": ['xkcd.com', "semperfi.net/veterans"], "excluded_sites":["dailydeals.com"]})) == 'salamander "zuccini" site:xkcd.com | site:semperfi.net/veterans | site:.club | site:*.io | site:.com -"dailydeals.com" intitle:infosys'

def test_gsq_daterange():
    assert str(GSQ({"daterange": (date(2016, 12, 10), date(2016, 12, 30))})) == 'daterange:2457733-2457753'
    assert str(GSQ({"daterange": (date(2016, 12, 10), date(2016, 12, 30)), "in_title":"infosys"})) == 'intitle:infosys daterange:2457733-2457753'
    assert str(GSQ({"daterange": (date(2016, 12, 10), date(2016, 12, 30)), "in_url": "infosys", "necessary_sites":["http://www.business-standard.com/article/companies/"]})) == 'site:http://www.business-standard.com/article/companies/ inurl:infosys daterange:2457733-2457753'
