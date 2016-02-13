

# can_compile=True
# try:					## First, try to import splinter
# 	import splinter
# 	browser_js = splinter.Browser("phantomjs")
# 	# browserHandler = "splinter"

# except Exception:
# 	print """\n\tERROR: One of the following softwares is not installed:
# 	> splinter		[install to Python with the command 'sudo pip install splinter'].
# 	> phantomjs  	[refer to http://phantomjs.org as to how to install it to your machine (on Linux, 'sudo apt-get install phantomjs' worked for me in Jan 2016)]
# 	> selenium 		[usually packaged with splinter, you might need to update with 'sudo pip install selenium --upgrade']
# 	"""

# 	try:				## If importing splinter fails, try to import twill 0.9
# 		import twill
# 		import twill.commands
# 		if twill.__version__ != "0.9":
# 			print "\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch."
# 			can_compile = False
# 		# browserHandler = "twill"

# 	except Exception:
# 		print "\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch."
# 		can_compile = False



# if can_compile == False:
# 	exit()



class BrowserHandlerTemplate(object):
	browser = None
	_headless = True

	def resetBrowser(self):
		raise NotImplementedError("BrowserHandlerTemplate.resetBrowser() has not been implemented")

	def checkBrowserAvailability(self, errorPrinting=False):
		# raise NotImplementedError("BrowserHandlerTemplate.checkBrowserAvailability() has not been implemented")
		if self.browser != None:
			if errorPrinting:
				print("\n\tBrowser is available")
			return True

		if errorPrinting:
			print("\n\tBrowser is not available")
		return False


	def clearBrowserData(self):
		raise NotImplementedError("BrowserHandlerTemplate.clearBrowserDate() has not been implemented")

	def getHtml(self, url, secure=False):
		url = self._ensureHTTPorHTTPS(url=url, secure=secure)
		if self.go(url):
			return self.getCurrentPageHtml()
		else: return None

	def go(self, url):
		raise NotImplementedError("BrowserHandlerTemplate.go() has not been implemented")

	def getCurrentPageHtml(self):
		raise NotImplementedError("BrowserHandlerTemplate.getCurrentPageHtml() has not been implemented")

	def getCurrentPageUrl(self):
		raise NotImplementedError("BrowserHandlerTemplate.getCurrentPageUrl() has not been implemented")

	def getInitialGoogleSearchResultsPageHtml(self, searchQuery, googleDomain):
		raise NotImplementedError("BrowserHandlerTemplate.getInitialGoogleSearchResultsPageHtml() has not been implemented")

	def isHeadless(self):
		raise NotImplementedError("BrowserHandlerTemplate.isHeadless() has not been implemented")

	def browserClose(self):
		raise NotImplementedError("BrowserHandlerTemplate.browserClose() has not been implemented")


	def _ensureHTTPorHTTPS(self, url, secure=False):
		if url.lower().find('http://')!= 0 and url.lower().find('https://')!= 0:
			if secure:
				return 'https://'+url
			else: 
				return 'http://'+url

		else: 
			return url


# print("\n\tSplinter is the default headless client of this package as it is more reliable.")



"""RUles for classes:
- All imports 
"""



class splinterBrowserHandler(BrowserHandlerTemplate):

	_splinterErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> splinter		[install to Python with the command 'pip install splinter'].\n\t> selenium 		[usually packaged with splinter, you might need to update with 'pip install selenium --upgrade']"

	_phantomjsErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> phantomjs  	[refer to http://phantomjs.org as to how to install it to your machine (on Linux, 'apt-get install phantomjs' worked for me in Jan 2016)]"


	try:					
		import splinter

	except Exception:
		print(_splinterErrorText)
		browser = None
		_headless = None



	def browserClose(self, printing=False):
		if self._headless==False:
			try:
				self.browser.close()
				if printing:
					print("\n\tSuccessfully closed Splinter browser window.")
				return True
			except Exception:
				if printing:
					print("\n\tUnable to close Splinter browser window.")
				return False
		else:
			try:
				import os
				os.system("killall phantomjs")
				if printing:
					print("\n\tSuccessfully closed Splinter phantomjs headless browser.")
				return True
			except Exception:
				if printing:
					print("\n\tUnable to close Splinter phantomjs headless browser.")
				return False





	def resetBrowser(self, headless=True, errorPrinting=False):

		try:					
			import splinter

		except Exception:
			print(self._splinterErrorText)
			self.browser = None
			self._headless = None
			return False

		if headless:
			try:
				self.browserClose(errorPrinting)
				self.browser = splinter.Browser("phantomjs")
				self._headless = True
				return True
			except Exception:
				if errorPrinting:
					print(self._phantomjsErrorText)
				self.browser = None
				self._headless = None
				return False


		else:
			self.browserClose(errorPrinting)
			try:
				self.browser = splinter.Browser()
				self._headless = False
				return True
			except Exception:
				if errorPrinting:
					print(self._splinterErrorText)
				self.browser = None
				self._headless = None
				return False


	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			self.browser.cookies.delete()  
			return True
		else:
			return False


	def isHeadless(self):
		return self._headless


	def go(self, url):
		url = self._ensureHTTPorHTTPS(url)
		if self.checkBrowserAvailability():
			return self.browser.visit(url)
			return True
		else:
			return False


	def getCurrentPageUrl(self):
		if self.checkBrowserAvailability():
			return self.browser.url
		else:
			return None


	def getCurrentPageHtml(self):
		if self.checkBrowserAvailability():
			return self.browser.html
		else:
			return None


	# def getHtml(self, url, secure=False):
	# 	if self.checkBrowserAvailability():
	# 		self.browser.visit(url)
	# 		return self.browser.html
	# 	else: 
	# 		return None
		

	def getInitialGoogleSearchResultsPageHtml(self, searchQueryString, googleDomain="http://www.google.com", secure=False, errorPrinting=False):
		googleDomain = self._ensureHTTPorHTTPS(url=googleDomain, secure=secure)
		if self.checkBrowserAvailability(errorPrinting):
			self.browser.visit(googleDomain)
			self.browser.fill('q', searchQueryString)
			button = self.browser.find_by_name('btnG')	## btnG was found by looking at google.com's HTML code.
			button.click()
			url = self._ensureHTTPorHTTPS(self.browser.url)
			self.browser.visit(url)
			return self.browser.html
		else:
			return None
	

	def __init__(self, headless=True):
		self.resetBrowser(headless=headless)		










class twillBrowserHandler(BrowserHandlerTemplate):

	_twillErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> 'twill' module version 0.9 [install to Python with 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported."

	try:					
		import twill
		import twill.commands
		if twill.__version__ != "0.9":
			raise IncorrectVersionError(_twillErrorText)

	except Exception:
		print(_twillErrorText)
		browser = None
		_headless = None



	def browserClose(self, errorPrinting=False):
		try:		
			self.browser = None
			self._headless = None
			if errorPrinting:
				print("\n\tSuccessfully closed Twill browser.")
			return True

		except Exception:
			if errorPrinting:
				print("\n\tUnable to closes Twill browser.")
			return False



	def resetBrowser(self, errorPrinting=False):
		try:					
			import twill
			import twill.commands
			if twill.__version__ != "0.9":
				raise IncorrectVersionError(_twillErrorText)

		except Exception:
			print(self._twillErrorText)
			self.browser = None
			self._headless = None
			return False


		try:
			self.browserClose(errorPrinting)
			self.browser = twill.commands.get_browser()
			self._headless = True
			return True
		except Exception:
			if errorPrinting:
				print(self._phantomjsErrorText)
			self.browser = None
			self._headless = None
			return False



	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			twill.commands.reset_browser()
			twill.commands.clear_cookies();
			twill.commands.reset_output(); 	
			return True
		else:
			return False
		



	def isHeadless(self):
		return self._headless


	def go(self, url):
		url = self._ensureHTTPorHTTPS(url)
		if self.checkBrowserAvailability():
			try:
				return self.browser.go(url)
				return True
			except Exception:
				return False
		else:
			return False


	def getCurrentPageUrl(self):
		if self.checkBrowserAvailability():
			return self.browser.get_url()
		else:
			return None


	def getCurrentPageHtml(self):
		if self.checkBrowserAvailability():
			return self.browser.get_html()
		else:
			return None


	def getHtml(self, url, secure=False):
		url = self._ensureHTTPorHTTPS(url=url, secure=secure)
		if self.checkBrowserAvailability():
			try:
				self.browser.go(url)
				return self.browser.get_html()
			except Exception:
				return None
		else: 
			return None
		

	def getInitialGoogleSearchResultsPageHtml(self, searchQueryString, googleDomain="http://www.google.com", secure=False, errorPrinting=False):
		googleDomain = self._ensureHTTPorHTTPS(url=googleDomain, secure=secure)
		if self.checkBrowserAvailability(errorPrinting):

			""" Source: http://pymantra.pythonblogs.com/90_pymantra/archive/407_form_submit_using_twill.html """

			self.go(googleDomain)
			all_forms = self.browser.get_all_forms()	## returns list of all form objects (corresp. to HTML <form>) on that URL 
			
			## now, you have to choose only that form, which has the POST or GET method
			for each_frm in all_forms:
				attr = each_frm.attrs			## all attributes of form
				if each_frm.method == 'GET':	## The button to search is a GET button. Sometimes this may be POST
					ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
					for ct in ctrl:
						if ct.type == 'text':     	## i did it as per my use, you can put your condition here
							ct._value = searchQueryString 	## The Google query we want to fire.
							self.browser.clicked(each_frm, ct.attrs['name'])	## clicked() takes two parameter: a form object and button name to be clicked.
							self.browser.submit()		## Clicks the submit button on that form
			return self.getCurrentPageHtml()
		else:
			return None
	

	def __init__(self):
		self.resetBrowser()	



###-----------------------------TESTS-----------------------------###


# x = splinterBrowserHandler()
x = twillBrowserHandler()
print(x.isHeadless())
html = x.getInitialGoogleSearchResultsPageHtml(searchQueryString="man with cat", errorPrinting=True)
print(len(html))
gone = x.go("www.google.com")
print(gone)
html = x.getCurrentPageHtml()
print(len(html))
html = x.getHtml("www.google.com")
print(len(html))
