import re


class GoogleWebsiteParser:

	def __init__(self):
		self._canParse = True
		try:
			from bs4 import BeautifulSoup
		except Exception:
			print("\n\n\n\tERROR in class GoogleWebsiteParser: module BeautifulSoup not found, please install to Python [e.g. with the command 'pip install beautifulsoup4'].\n")
			self._canParse = False



	def checkParser(self):
		return self._canParse



	def extractResultUrlsFromGoogleSearchResultsPageHtml(self, htmlString, printing=True, printingDebug=False):	
		""" This function, given the HTML of a Google Search results page, extracts the urls of the Search Results. """
		if self.checkParser() == False:
			if printing:
				print("\nGoogleWebsiteParser.extractResultUrlsFromGoogleSearchResultsPageHtml(): no parser available.")
			return None

		from bs4 import BeautifulSoup

		bs = BeautifulSoup(htmlString)

		temp_results_urls=bs.find_all(attrs={"class":"r"}) 	## I have found that this extracts all 10 links per page

		if temp_results_urls==[]:
			if printingDebug:
				print("\nGoogleWebsiteParser.extractResultsFromGoogleSearchResultsPageHtml(): temp_results_urls= []")
			return None
		
		if printingDebug:
			print("\nGoogleWebsiteParser.extractResultsFromGoogleSearchResultsPageHtml(): temp_results_urls=")
			for x in temp_results_urls:
				print("\t%s"%x)

		

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
			if printingDebug:
				print("\nGoogleWebsiteParser.extractResultsFromGoogleSearchResultsPageHtml(): results_page_urls= []")
			return None

		if printingDebug:
			print("\nGoogleWebsiteParser.extractResultsFromGoogleSearchResultsPageHtml(): results_page_urls= ")
			for x in results_page_urls:
				print("\t%s"%x)


		return tuple(results_page_urls)


	


	def extractTotalNumberOfResultsFromQuery(self, htmlString, printing=True, printingDebug=False):
		""" This function, given the HTML of a Google Search results page, extracts the total number of Search Results the query has. 
		This can technically be extracted from any search result page of that query."""

		if self.checkParser() == False:
			if printing:
				print("\nGoogleWebsiteParser.extractTotalNumberOfResultsFromQuery(): no parser available.")
			return None

		from bs4 import BeautifulSoup
		bs = BeautifulSoup(htmlString)	
		resultStats_html = bs.find_all(attrs={"id":"resultStats"})	## There should be only one.
		
		if printingDebug:
			print("\nGoogleWebsiteParser.extractTotalNumberOfResultsFromQuery(): length of html string passed = %s"%len(htmlString))
			print("GoogleWebsiteParser.extractTotalNumberOfResultsFromQuery(): 'id=\"resultStats\"' present  at = %s"%htmlString.find('id="resultStats"'))
			print("GoogleWebsiteParser.extractTotalNumberOfResultsFromQuery(): resultStats_html=%s"%resultStats_html)

		if resultStats_html==[]:
			return None

		resultStats_html=str(resultStats_html[0])
		resultStats_html=re.sub(",","", resultStats_html)
		total_num_results=re.findall('(?<=bout )\d+(?= results)', resultStats_html)
		if total_num_results==[]:
			return None

		total_num_results=total_num_results[0]
		try:
			total_num_results=int(total_num_results)
		except Exception:
			if printingDebug:
				print("\nGoogleWebsiteParser.extractTotalNumberOfResultsFromQuery(): total_num_results = %s is not an integer"%total_num_results)
			return None
		return total_num_results
	




	def extractNextGoogleSearchResultsPageLink(self, htmlString, googleDomain, printing=True, printingDebug=False):	
		"""This function, given the HTML of a Google Search results page, will get a single link, of the next results page.
		This function is an easier version of extract_next_google_search_results_page_links(), which allows us to just keep clicking 'Next' to get more results."""

		if self.checkParser() == False:
			if printing:
				print("\nGoogleWebsiteParser.extractNextGoogleSearchResultsPageLink(): no parser available.")
			return None

		from bs4 import BeautifulSoup
		
		bs = BeautifulSoup(htmlString)	

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







