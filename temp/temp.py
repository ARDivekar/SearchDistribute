


class SplinterBrowserHandler(BrowserHandler):


	def __init__(self):
		self.browser=None
		self.browserHandler = ""
		
		if self.setBrowser(errorPrinting=True) == False:	
			print("\n\n\n\tFatal ERROR in class BrowserHandler: none of the supported browser handling modules have been installed.\n")
		





	def setBrowser(self, headless=True, errorPrinting=False):
		"""This function assigns the class variables 'browser' and 'browserHandler'. It effectively sets a new version of the browser.
		The order of the if-else statements below determines the order in which we try to use the browser libraries."""

		if self._trySplinterImport(errorPrinting=errorPrinting) == True:
			self.browser= self._getSplinterBrowser(headless=headless)
			self.browserHandler = "splinter"
			self.clearBrowserData()
			return True

		elif self._tryTwillImport(errorPrinting=errorPrinting) == True:
			self.browser = self._getTwillBrowser()
			self.browserHandler = "twill0.9"
			self.clearBrowserData()
			return True

		else:
			return False

			

	

	def checkBrowser(self):
		if self.browserHandler!="" and self.browser!=None:
			return True
		else: return False
	



	def clearBrowserData(self):
		if self.browserHandler=="splinter":
			self._splinterBrowserClear()

		elif self.browserHandler=="twill0.9":
			self._twillBrowserClear()
			




	def getHtml(self, url, errorPrinting=False):
		"""	Return the HTML of the passed URL, if possible. If not, return None.
			This function uses bandwidth with each call."""

		if self._go(url):
			html =  self._getCurrentPageHtml()
			print html
			return html
		else:
			if errorPrinting:
		 		print("\n\tERROR in getHTML(): cannot get HTML content of %s"%url)
			return None


		# # if self.BrowserHandler == "splinter":
		# import splinter
		# browser_js = splinter.Browser("phantomjs")
		# browser_js.visit(url)
		# return browser_js.html
		# 		# print self.browser.url
		# 		# return self._getCurrentPageHtml()
				
		# 	# else: 
		# 	# 	if errorPrinting:
		# 	# 		print("\n\tERROR in getHTML(): cannot get HTML content of %s"%url)
		# 	# 	return None
			




	def getInitialGoogleSearchResultsPageHtml(self, searchQuery, googleDomain="http://www.google.com"):

		if self.browser._go(googleDomain):	## tries to visit specified Google domain.
			if self.browserHandler=="splinter":
				return self._splinterPerformInitialGoogleSearch(searchQuery, googleDomain)
				
						
			elif self.browserHandler=="twill0.9":
				return self._twillPerformInitialGoogleSearch(searchQuery, googleDomain)

			else: return None

			# return self._getCurrentPageHtml()

		else: return None
				 


			



	##-----------------------------------PRIVATE METHODS-----------------------------------##

	def _trySplinterImport(self, errorPrinting=True, headless = True):

		try:					## First, try to import splinter
			import splinter
			if headless:
				browser_js = splinter.Browser("phantomjs")
			else:
				browser_js = splinter.Browser()

			return True

		except Exception:
			if errorPrinting:
				print("\n\tERROR: One of the following softwares is not installed:\n> splinter		[install to Python with the command 'sudo pip install splinter'].\n> phantomjs  	[refer to http://phantomjs.org as to how to install it to your machine (on Linux, 'sudo apt-get install phantomjs' worked for me in Jan 2016)]\n> selenium 		[usually packaged with splinter, you might need to update with 'sudo pip install selenium --upgrade']"
					)
				print("\n\tSplinter is the default headless client of this package as it is more reliable.")
			return False

	
	
	def _tryTwillImport(self, errorPrinting=True):
		try:				## If importing splinter fails, try to import twill 0.9
			import twill
			import twill.commands

			if twill.__version__ != "0.9":
				if errorPrinting:
					print("\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch.")
				return False

			return True

		except Exception:
			if errorPrinting:
				print("\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch.")
			
			return False





	def _getSplinterBrowser(self, headless=True):
		import splinter
		if headless:
			try:
				import os; temp=os.system("killall phantomjs")
				return splinter.Browser("phantomjs")	## use the phantomjs headless browser client.
			except Exception:
				print("phantomjs not working, using regular splinter browser...")
				return splinter.Browser()

		else: 
			return splinter.Browser()



	def _getTwillBrowser(self):
		import twill
		import twill.commands
		return twill.commands.get_browser()		## get the default browser





	def _splinterPerformInitialGoogleSearch(self, searchQuery, googleDomain):
		""" Source: http://splinter.readthedocs.org/en/latest/tutorial.html """

		# browser = splinter.Browser('zope.testbrowser', ignore_robots=True)
		
		self.browser.fill('q', query)
		button = self.browser.find_by_name('btnG')	## btnG was found by looking at google.com's HTML code.
		button.click()
		url = self._ensureHTTPorHTTPS(self.browser.url)
		self.browser.visit(url)
		return self.browser.html

		# print "SPLINTER URL:%s"%self.browser.url
		# print "\n\n\nGetting results from ===> %s"%self.browser.url
		# print self.browser.title
		


	def _twillPerformInitialGoogleSearch(self, searchQuery, googleDomain):
		""" Source: http://pymantra.pythonblogs.com/90_pymantra/archive/407_form_submit_using_twill.html """
		
		all_forms = self.browser.get_all_forms()	## returns list of all form objects (corresp. to HTML <form>) on that URL 
		
		## now, you have to choose only that form, which has the POST or GET method
		for each_frm in all_forms:
		    attr = each_frm.attrs			## all attributes of form
		    if each_frm.method == 'GET':	## The button to search is a GET button. Sometimes this may be POST
		        ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
		        for ct in ctrl:
		                if ct.type == 'text':     	## i did it as per my use, you can put your condition here
								ct._value = query 	## The Google query we want to fire.
								self.browser.clicked(each_frm, ct.attrs['name'])	## clicked() takes two parameter: a form object and button name to be clicked.
								self.browser.submit()		## Clicks the submit button on that form
		return self.browser.get_html()





	def _getCurrentPageHtml(self):
		if self.checkBrowser():
			if self.browserHandler=="splinter":
				return self._splinterGetCurrentPageHTML()
						
			elif self.browserHandler=="twill0.9":
				return self._twillGetCurrentPageHTML()

		else: return None



	def _ensureHTTPorHTTPS(self,url, secure=False):
		if url.lower().find('http://')!=0 and url.lower().find('https://')!=0:
			if secure:
				return 'https://'+url
			else: return 'http://'+url

		else: return url
		


	def _go(self, url, secure=True):
		if self.checkBrowser():
			url = self._ensureHTTPorHTTPS(url, secure)
			# try:
			if self.browserHandler=="splinter":
				self._splinterBrowserGo(url)
				return True
				
			elif self.browserHandler=="twill0.9":
				self._twillBrowserGo(url)
				return True
			# except Exception:
			return False

		return False





	def _splinterGetCurrentPageHTML(self):
		return self.browser.html



	def _twillGetCurrentPageHTML(self):
		return self.browser.get_html()





	def _splinterBrowserGo(self, url):
		self.browser.visit(url)



	def _twillBrowserGo(self, url):
		self.browser.go(url)





	def _splinterBrowserClear(self):
		# deletes all cookies
		self.browser.cookies.delete()  

	

	def _twillBrowserClear(self):
		t_com=twill.commands
		t_com.reset_browser; 
		t_com.reset_output; 	
		t_com.clear_cookies;
		self.browser = t_com.get_browser()


		


class ABC:
	var = "abc"
	def __init__(self):
		print(self.var)


		
x = ABC()
