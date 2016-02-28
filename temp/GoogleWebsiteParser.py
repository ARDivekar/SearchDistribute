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



	def extractResultUrlsFromGoogleSearchResultsPageHtml(self, htmlString, printingDebug=False):	
		""" This function, given the HTML of a Google Search results page, extracts the urls of the Search Results. """
		if self.checkParser() == False:
			return None

		from bs4 import BeautifulSoup

		bs = BeautifulSoup(htmlString)

		if printingDebug:
			print "\n\nGoogleWebsiteParser.extractResultsFromGoogleSearchResultsPageHtml() output:"


		temp_results_urls=bs.findAll(attrs={"class":"r"}) 	## I have found that this extracts all 10 links per page

		if printingDebug:
			print("\n\ttemp_results_urls:")

		if temp_results_urls==[]:
			if printingDebug:
				print "[]"
			return None
		
		if printingDebug:
			for x in temp_results_urls:
				print "\n\t",x

		if printingDebug:
			print "\n\n\tresults_page_urls:"


		results_page_urls=[]	## all the search result urls from a relevant Google Search results page.
		for temp_url in temp_results_urls:
			# print type(temp_url) 		#<-is a BeautifulSoup object
			# print "\n\n\nCHICKEN",str(temp_url)	#<-yeah this is how i debug stuff.
			
			result_page_url=re.findall('(?<=/url\?q=)(.*?)(?=")', str(temp_url))
			if result_page_url!=[]:
				result_page_url=result_page_url[0]
				result_page_url=re.findall('(.*?)(?=&amp)', result_page_url)
				if result_page_url != []:
						result_page_url=result_page_url[0]
						results_page_urls.append(result_page_url)
			
		if results_page_urls==[]:
			if printingDebug:
				print "[]"
			return None

		if printingDebug:
			for x in results_page_urls:
				print "\n\t",x


		return tuple(results_page_urls)


	


	def extractTotalNumberOfResultsFromQuery(self, htmlString, printingDebug=False):
		""" This function, given the HTML of a Google Search results page, extracts the total number of Search Results the query has. 
		This can technically be extracted from any search result page of that query."""

		if self.checkParser() == False:
			return None

		from bs4 import BeautifulSoup

		bs = BeautifulSoup(htmlString)	

		resultStats_html=bs.findAll(attrs={"id":"resultStats"})	## There should be only one.
		
		if printingDebug:
			print "resultStats_html=%s"%resultStats_html

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
				print "total_num_results = %s is not an integer"%total_num_results
			return None
		return total_num_results
	




	def extractNextGoogleSearchResultsPageLink(self, htmlString, googleDomain, printingDebug=False):	
		"""This function, given the HTML of a Google Search results page, will get a single link, of the next results page.
		This function is an easier version of extract_next_google_search_results_page_links(), which allows us to just keep clicking 'Next' to get more results."""

		if self.checkParser() == False:
			return None

		from bs4 import BeautifulSoup
		
		bs = BeautifulSoup(htmlString)	
		
		if printingDebug:
			print "\n\GoogleWebsiteParser.extractNextGoogleSearchResultsPageLink() output:"

		if printingDebug:
			print "\n\tnav_html:\n"

		nav_html=(bs.findAll(attrs={"id":"nav"}))
		if nav_html==[]:
			if printingDebug:
				print "[]"	
			return None

		nav_html=nav_html[0]	## There should be only one.
		if printingDebug:
			print "%s\n"%nav_html
		

		temp_next_pages=BeautifulSoup(str(nav_html)).findAll(attrs={"class":"fl"})	## This extracts links for further result pages. The 'Next' link is not included in this.

		if printingDebug:
			print "\n\temp_next_pages:"

		if temp_next_pages==[]:		## No 'next' results on this page
			if printingDebug:
				print "[]"	
			return None

		if printingDebug:
			for x in temp_next_pages:
				print "\n\t",x


		next_link_html=temp_next_pages[len(temp_next_pages)-1]	#The 'Next' link is also of class 'fl'
		
		
		next_result_page_url=re.findall('(?<=href=").*?(?=")', str(next_link_html))

		if printingDebug:
			print "\n\nnext_result_page_url:"
		
		if next_result_page_url==[]:
			if printingDebug:
				print "[]"
			return None
		next_result_page_url=next_result_page_url[0]
		next_result_page_url=googleDomain+next_result_page_url	
		
		if printingDebug:
			print "\n\t",next_result_page_url

		next_result_page_url= re.sub("&amp;", "&", next_result_page_url)
		return next_result_page_url







