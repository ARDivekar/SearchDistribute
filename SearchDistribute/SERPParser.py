import re
from bs4 import BeautifulSoup
from SearchDistribute.SearchExtractorErrors import SERPParsingException
from SearchDistribute.Enums import SearchEngines
import urllib

class GoogleParser:
	current_page_url = ""
	results = []
	total_num_results = -1
	total_num_results_for_query = -1
	query_retrieval_time = -1.0
	link_to_previous_page = ""
	links_to_previous_pages = []
	links_to_next_pages = []
	link_to_next_page = ""

	def __init__(self, html, current_page_url):
		self.current_page_url = current_page_url ## This must not be moved, as self._parse_navigation_links(...) uses it.
		bs = BeautifulSoup(html)
		results = self._parse_result_urls(bs)
		if results == None:
			raise SERPParsingException(search_engine=SearchEngines.Google, parsing_stage="search result urls")
		self.results = results
		self.total_num_results = len(self.results)
		total_num_results_for_query = self._parse_total_number_of_results_for_query(bs)
		if total_num_results_for_query == None:
			raise SERPParsingException(search_engine=SearchEngines.Google, parsing_stage="total number of results for query")
		self.total_num_results_for_query = total_num_results_for_query
		query_retrieval_time = self._parse_query_retrieval_time(bs)
		if query_retrieval_time == None:
			raise SERPParsingException(search_engine=SearchEngines.Google, parsing_stage="query retrieval time")
		self.query_retrieval_time = query_retrieval_time
		nav_links = self._parse_navigation_links(bs)
		if nav_links == None:
			raise SERPParsingException(search_engine=SearchEngines.Google, parsing_stage="navigation links to previous and next pages")
		self.link_to_previous_page, self.links_to_previous_pages, temp, self.links_to_next_pages, self.link_to_next_page = nav_links




	def _parse_result_urls(self, bs):
		""" This function, given the BeautifulSoup of the HTML of a Google Search results page, extracts the urls of the Search Results. """
		temp_results_urls=bs.find_all(attrs={"class":"r"}) 	## I have found that this extracts all 10 links per page
		if temp_results_urls==[]:
			return None

		results_page_urls=[]	## all the search result urls from a relevant Google Search results page.

		for temp_url in temp_results_urls:
				## Method 1:
			result_page_url=re.findall('(?<=/url\?q=)(.*?)(?=")', str(temp_url))
			if result_page_url!=[]:
				result_page_url=result_page_url[0]
				result_page_url=re.findall('(.*?)(?=&amp)', result_page_url)
				if result_page_url != []:
					result_page_url=result_page_url[0]
					results_page_urls.append(result_page_url)
			else:
				## Method 2:
				result_page_url=re.findall('(?<=href=").*?(?=")',str(temp_url))
				if result_page_url!=[]:
					results_page_urls.append(result_page_url[0])

		if results_page_urls==[]:
			return None

		return tuple(results_page_urls)




	def _parse_total_number_of_results_for_query(self, bs):
		""" This function, given the BeautifulSoup of the HTML of a Google Search results page, extracts the total number of Search Results the query has.
		This can technically be extracted from any search result page of that query."""
		resultStats_html = bs.find_all(attrs={"id":"resultStats"})	## There should be only one.
		if resultStats_html==[]:
			return None

		resultStats_html=str(resultStats_html[0])
		resultStats_html=re.sub(",","", resultStats_html)
		total_num_results_for_query=re.findall('(?<=bout )\d+(?= results)', resultStats_html)
		if total_num_results_for_query==[]:
			return None

		total_num_results_for_query=total_num_results_for_query[0]
		try:
			total_num_results_for_query=int(total_num_results_for_query)
		except Exception:
			return None
		return total_num_results_for_query



	def _parse_query_retrieval_time(self, bs):
		try:
			time_text = bs.find_all(id="resultStats")[0].find_all('nobr')[0].text.strip()
			return float(re.findall("\((.*?)( )?seconds\)", time_text)[0][0])
		except Exception:
			return None

	def _parse_navigation_links(self, bs):
		''' This function returns a 4-tuple with the following syntax:
			(link_to_previous_page, list_of_links_to_previous_pages, list_of_links_to_next_pages, link_to_next_page)
			All of the links are absolute links, e.g. 'https://www.google.co.in/search?q=killing+me+softly&biw=482&bih=580&ei=KyGrWOmOEJ6QvQSZ5IiQBA&start=30&sa=N'.
		'''

		try:
			nav_links = bs.find_all(id="nav")[0].find_all('td')
			link_to_previous_page = nav_links[0].find_all('a')[0].get('href')
			link_to_next_page = nav_links[-1].find_all('a')[0].get('href')
			link_to_current_page = None
			list_of_links_to_previous_pages = []
			list_of_links_to_next_pages = []
			base = urllib.parse.urlparse(self.current_page_url).scheme+"://"+urllib.parse.urlparse(self.current_page_url).netloc
			for i in range(1, len(nav_links)-1):
				if nav_links[i].get('class') == ['cur']:
					link_to_current_page = self.current_page_url
				elif link_to_current_page == None:
					list_of_links_to_previous_pages.append(base+nav_links[i].find_all('a')[0].get('href'))
				else:
					list_of_links_to_next_pages.append(base+nav_links[i].find_all('a')[0].get('href'))
			return (link_to_previous_page, list_of_links_to_previous_pages, link_to_current_page, list_of_links_to_next_pages, link_to_next_page)

		except Exception:
			return None



	def extractNextGoogleSearchResultsPageLink(self, htmlString, googleDomain, printing=True, printingDebug=False):	
		"""This function, given the HTML of a Google Search results page, will get a single link, of the next results page.
		This function is an easier version of extract_next_google_search_results_page_links(), which allows us to just keep clicking 'Next' to get more results."""

		nav_html=(bs.find_all(attrs={"id":"nav"}))

		if nav_html==[]:
			if printingDebug:
				print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): nav_html=[]")
			return None

		if printingDebug:
			print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): nav_html=")
			for x in nav_html:
				print("\t%s"%x)

		nav_html=nav_html[0]	## There should be only one.		

		temp_next_pages=BeautifulSoup(str(nav_html)).findAll(attrs={"class":"fl"})	## This extracts links for further result pages. The 'Next' link is not included in this.
			

		if temp_next_pages==[]:		## No 'next' results on this page
			if printingDebug:
				print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): temp_next_pages= []")
			return None

		if printingDebug:
			print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): temp_next_pages=")
			for x in temp_next_pages:
				print("\t%s"%x)


		next_link_html=temp_next_pages[len(temp_next_pages)-1]	#The 'Next' link is also of class 'fl'
		
		
		next_result_page_url=re.findall('(?<=href=").*?(?=")', str(next_link_html))

		if next_result_page_url==[]:
			if printingDebug:
				print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): next_result_page_url= []")
			return None
		next_result_page_url=next_result_page_url[0]
		next_result_page_url=googleDomain+next_result_page_url	
		
		if printingDebug:
			print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): next_result_page_url=%s"%next_result_page_url)

		next_result_page_url= re.sub("&amp;", "&", next_result_page_url)
		return next_result_page_url







