from Enums import Enum
import traceback
import time
import random
import os


_BrowserHandlerCanRunSplinter = True
_BrowserHandlerCanRunSplinterHeadless = True
_splinterBrowser=None
try:
	import splinter
	try:
		_splinterBrowser = splinter.Browser("phantomjs")
	except Exception:
		_BrowserHandlerCanRunSplinterHeadless = False	
except Exception:
	_BrowserHandlerCanRunSplinter = False
	_BrowserHandlerCanRunSplinterHeadless = False








###-----------------------------SET POSSIBLE BROWSERS BASED ON CLASSES DEFINED IN THIS FILE-----------------------------###

PossibleBrowserHandlers = Enum([]) #["SPLINTER", "TWILL0_9", "SPLINTER_HEADLESS"]





class BrowserHandlerTemplate(object):
	browser = None
	_headless = True

	def resetBrowser(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.resetBrowser() has not been implemented")

	def checkBrowserAvailability(self, errorPrinting=False):
		# raise NotImplementedError("BrowserHandlerTemplate.checkBrowserAvailability() has not been implemented")
		if self.browser != None:
			if errorPrinting:
				print("\n\tBrowser is available.")
			return True

		if errorPrinting:
			print("\n\tBrowser is not available.")
		return False

	def getName(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.getName() has not been implemented")

	def clearBrowserData(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.clearBrowserDate() has not been implemented")

	def getHtml(self, url, secure=False):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.getHtml() has not been implemented")

	def go(self, url):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.go() has not been implemented")

	def getCurrentPageHtml(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.getCurrentPageHtml() has not been implemented")

	def getCurrentPageUrl(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.getCurrentPageUrl() has not been implemented")

	def getInitialGoogleSearchResultsPageHtml(self, searchQuery, googleDomain):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.getInitialGoogleSearchResultsPageHtml() has not been implemented")

	def isHeadless(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.isHeadless() has not been implemented")

	def browserClose(self):
		raise NotImplementedError("\n\tFATAL ERROR: BrowserHandlerTemplate.browserClose() has not been implemented")


	def _ensureHTTPorHTTPS(self, url, secure=False):
		if url.lower().find('http://')!= 0 and url.lower().find('https://')!= 0:
			if secure:
				return 'https://'+url
			else: 
				return 'http://'+url

		else: 
			return url


	def _waitBeforeTypingQueryIntoSearchBox(self, searchQueryString, errorPrinting=True):
		
		searchQueryStringLen=len(searchQueryString)
		waitTime = random.uniform(searchQueryStringLen/float(5), searchQueryStringLen/float(3))	## wait a random amount of time. This assumes that the average typing speed is between 3 and 5 characters per second.
		if errorPrinting:
			print("\t\t\tWaiting for %s seconds before entering query into search box."%waitTime)
		time.sleep(waitTime) 


			


# print("\n\tSplinter is the default headless client of this package as it is more reliable.")



"""RUles for classes:
- All imports 
"""



class splinterBrowserHandler(BrowserHandlerTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class splinterBrowserHandler.

	_splinterErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> splinter		[install to Python with the command 'pip install splinter'].\n\t> selenium 		[usually packaged with splinter, you might need to update with 'pip install selenium --upgrade']"

	_phantomjsErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> phantomjs  	[refer to http://phantomjs.org as to how to install it to your machine (on Linux, 'apt-get install phantomjs' worked for me in Jan 2016)]"

	browser = None
	_headless = None
	


	def __init__(self, headless=True, errorPrinting=True):
		'''We are starting the browser for the first time.'''
		
		self.browser = None
		self._headless = None

		if _BrowserHandlerCanRunSplinter:
			if headless: 
				if _BrowserHandlerCanRunSplinterHeadless: 
					if _splinterBrowser != None: 	## use existing browser object
						self.browser = _splinterBrowser
						self._headless = True
					else:
						self.browser = splinter.Browser("phantomjs")
						self._headless = True
				else:
					if errorPrinting:
						print(self._phantomjsErrorText)
			else:
				self.browser = splinter.Browser()
				self._headless = False
		else:
			if errorPrinting:
				print(self._splinterErrorText)




	def isHeadless(self):
		return self._headless
		



	def resetBrowser(self, headless=None, errorPrinting=True):
		'''Reset the browser in case it does not seem to be working.'''
		self.browser = None
		self._headless = None

		try:
			self.browserClose(errorPrinting)
		except Exception:
			1+1

		if _BrowserHandlerCanRunSplinter:
			if headless: 
				if _BrowserHandlerCanRunSplinterHeadless: 
					self.browser = splinter.Browser("phantomjs")
					self._headless = True
				else:
					if errorPrinting:
						print(self._phantomjsErrorText)
			else:
				self.browser = splinter.Browser()
				self._headless = False
		else:
			if errorPrinting:
				print(self._splinterErrorText)


			
		# except Exception:
		# 	if errorPrinting:
		# 		print(self._splinterErrorText)
		# 	self.browser = None
		# 	self._headless = None
		# 	return False


		# if self.checkBrowserAvailability()==False:		
		# 	if headless:
		# 		try:
		# 			self.browserClose(errorPrinting)
		# 			self.browser = splinter.Browser("phantomjs")
		# 			self._headless = True
		# 			return True
		# 		except Exception:
		# 			if errorPrinting:
		# 				print(self._phantomjsErrorText)
		# 			self.browser = None
		# 			self._headless = None
		# 			return False

		# 	else:
		# 		self.browserClose(errorPrinting)
		# 		try:
		# 			self.browser = splinter.Browser()
		# 			self._headless = False
		# 			return True
		# 		except Exception:
		# 			if errorPrinting:
		# 				print(self._splinterErrorText)
		# 			self.browser = None
		# 			self._headless = None
		# 			return False


		# elif self.isHeadless()==True:
		# 	try:
		# 		self.browserClose(errorPrinting)
		# 		self.browser = splinter.Browser("phantomjs")
		# 		self._headless = True
		# 		return True
		# 	except Exception:
		# 		if errorPrinting:
		# 			print(self._phantomjsErrorText)
		# 		self.browser = None
		# 		self._headless = None
		# 		return False


		# elif self.isHeadless()==False:
		# 	self.browserClose(errorPrinting)
		# 	try:
		# 		self.browser = splinter.Browser()
		# 		self._headless = False
		# 		return True
		# 	except Exception:
		# 		if errorPrinting:
		# 			print(self._splinterErrorText)
		# 		self.browser = None
		# 		self._headless = None
		# 		return False
		



		


	def browserClose(self, printing=False):
		if self.checkBrowserAvailability():
			if self.isHeadless()==True:
				try:
					if self.isHeadless():
						os.kill("phantomjs")
					if printing:
						print("\n\tSuccessfully closed Splinter phantomjs headless browser.")
					return True
				except Exception:
					if printing:
						print("\n\tUnable to close Splinter phantomjs headless browser.")
					return False

			elif self.isHeadless()==False:
				try:
					self.browser.close()
					if printing:
						print("\n\tSuccessfully closed Splinter browser window.")
					return True
				except Exception:
					if printing:
						print("\n\tUnable to close Splinter browser window.")
					return False









	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			self.browser.cookies.delete()  
			return True
		else:
			return False




	def getName(self):
		nameString = "SPLINTER; Version=%s;"%self.splinter.__version__
		if self.isHeadless():
			nameString+=" Headless=yes;"
		else:
			nameString+=" Headless=no;"
		nameString += " Driver:%s;"%self.browser.driver_name
		return nameString


	


	


	def go(self, url, secure=False):
		url = self._ensureHTTPorHTTPS(url, secure)
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
			html = self.browser.html
			if html=="" or html==None:
				return None
			return html
		else:
			return None

		

	def getInitialGoogleSearchResultsPageHtml(self, searchQueryString, googleDomain="http://www.google.com", secure=False, errorPrinting=False):

		googleDomain = self._ensureHTTPorHTTPS(url=googleDomain, secure=secure)
		if self.checkBrowserAvailability(errorPrinting):
			self.browser.visit(googleDomain)

			self._waitBeforeTypingQueryIntoSearchBox(searchQueryString=searchQueryString, errorPrinting=errorPrinting)
			
			self.browser.fill('q', searchQueryString)
			button = self.browser.find_by_name('btnG')	## btnG was found by looking at google.com's HTML code.
			button.click()


			if self.isHeadless()==True:
				url = self._ensureHTTPorHTTPS(self.browser.url, secure=secure)
				self.browser.visit(url)

			if self.isHeadless()==False:
				time.sleep(5)

			return self.browser.html
		else:
			return None
	

	






class twillBrowserHandler(BrowserHandlerTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class twillBrowserHandler.

	_twillErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> 'twill' module version 0.9 [install to Python with 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported."

	try:					
		import twill
		import twill.commands
		if twill.__version__ != "0.9":
			raise IncorrectVersionError(_twillErrorText)

	except Exception:
		browser = None
		_headless = None

	



	def getName(self):
		nameString = "TWILL; Version=%s;"%self.twill.__version__
		if self.isHeadless():
			nameString+=" Headless=yes;"
		else:
			nameString+=" Headless=no;"
		return nameString


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
			if errorPrinting:
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


	def go(self, url, secure=False):
		url = self._ensureHTTPorHTTPS(url, secure)
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
			html = self.browser.html
			if html=="" or html==None:
				return None
			return html
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
							self._waitBeforeTypingQueryIntoSearchBox(searchQueryString=searchQueryString, errorPrinting=errorPrinting)
							
							ct._value = searchQueryString 	## The Google query we want to fire.
							self.browser.clicked(each_frm, ct.attrs['name'])	## clicked() takes two parameter: a form object and button name to be clicked.
							self.browser.submit()		## Clicks the submit button on that form

			return self.getCurrentPageHtml()
		else:
			return None
	

	def __init__(self, errorPrinting=True):
		self.resetBrowser(errorPrinting=errorPrinting)	





###-----------------------------TESTS-----------------------------###


# # x = splinterBrowserHandler()
# x = twillBrowserHandler()
# print(x.isHeadless())
# html = x.getInitialGoogleSearchResultsPageHtml(searchQueryString="man with cat", errorPrinting=True)
# print(len(html))
# gone = x.go("www.google.com")
# print(gone)
# html = x.getCurrentPageHtml()
# print(len(html))
# html = x.getHtml("www.google.com")
# print(len(html))
