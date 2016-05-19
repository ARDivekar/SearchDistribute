import sys
from Enums import Enum
import traceback
import time
import random
import os
from SearchExtractorErrors import *
import platform

availableBrowsers = Enum([]) #["SPLINTER", "TWILL0_9", "SPLINTER_PHANTOMJS"]
try:
	import splinter
	availableBrowsers.SPLINTER="SPLINTER"
	try:
		_splinterBrowser = splinter.Browser("phantomjs")
		availableBrowsers.SPLINTER_PHANTOMJS="SPLINTER_PHANTOMJS"
	except Exception, e:
		make_error("Browsers.py", "__main__", "Could not import splinter phantomjs",e)
except Exception, e:
	make_error("Browsers.py", "__main__", "Could not import splinter",e)





class BrowserTemplate(object):
	browser = None
	headless = None

	def isHeadless(self):
		return self.headless

	def resetBrowser(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def checkBrowserAvailability(self, errorPrinting=False):
		if self.browser is not None:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name, "Browser is available.")
			return True
		print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name, "Browser is not available.")
		return False

	def getName(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def clearBrowserData(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def getHtml(self, url, secure=False):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def go(self, url):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def getCurrentPageHtml(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def getCurrentPageUrl(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def getInitialGoogleSearchResultsPageHtml(self, searchQuery, googleDomain):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def browserClose(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def isAvailable(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))


	def _ensureHTTPorHTTPS(self, inputURL, secure):
		url = inputURL
		if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
			if secure: url = 'https://'+url
			else: url = 'http://'+url
		elif secure and url.lower().startswith('http://'):
			url = 'https://' + url[len('http://'):]
		elif not secure and url.lower().startswith('https://'):
			url = 'http://' + url[len('https://'):]
		return url


	def _waitBeforeTypingQueryIntoSearchBox(self, searchQueryString, errorPrinting=True):
		
		searchQueryStringLen=len(searchQueryString)
		waitTime = random.uniform(searchQueryStringLen/float(5), searchQueryStringLen/float(3))	## wait a random amount of time. This assumes that the average typing speed is between 3 and 5 characters per second.
		if errorPrinting:
			print("\t\t\tWaiting for %s seconds before entering query into search box."%waitTime)
		time.sleep(waitTime)


	def test(self, printing=True):
		html = None
		try:
			self.go("https://github.com/")	## a small test page, around 26 KB
			html = self.getCurrentPageHtml()
			if not self.browserClose(printing):
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "browser used for testing cannot be closed.")
			if html is not None and len(html)>20:
				print("Successfully ran test for browser: "+self.getName())
				return True
		except Exception, e:
			print_fatal_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Browser cannot access the web.", e)
		return False






			


# print("\n\tSplinter is the default headless client of this package as it is more reliable.")



class splinterBrowser(BrowserTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class splinterBrowser.

	_splinterErrorText = "One of the following softwares is not installed:\n\t> splinter		[install to Python with the command 'pip install splinter'].\n\t> selenium 		[usually packaged with splinter, you might need to update with 'pip install selenium --upgrade']"


	browser = None
	headless = False

	def __init__(self):
		self.resetBrowser()

	def isAvailable(self):
		if availableBrowsers.SPLINTER is not None:
			return True
		return False


	def resetBrowser(self, errorPrinting=True):
		'''Reset the browser in case it does not seem to be working.'''
		try:
			self.browserClose(errorPrinting)
			if self.isAvailable():
				self.browser = splinter.Browser()
			return True
		except Exception, e:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot reset browser.",e)
		return False



	def browserClose(self, printing=False):
		if self.checkBrowserAvailability():
			try:
				self.browser.quit()
				if printing: print("\nSuccessfully closed Splinter browser window.")
				return True
			except Exception,e:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to close Splinter browser window.",e)
		return False



	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			self.browser.cookies.delete()
			return True
		return False




	def getName(self):
		nameString = "SPLINTER; Version=%s;"%splinter.__version__
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
		return False


	def getCurrentPageUrl(self):
		if self.checkBrowserAvailability():
			return self.browser.url
		return None


	def getCurrentPageHtml(self):
		if self.checkBrowserAvailability():
			html = self.browser.html
			if html=="" or html is None:
				return None
			return html
		return None



	def getInitialGoogleSearchResultsPageHtml(self, searchQueryString, googleDomain="http://www.google.com", secure=False, errorPrinting=False):

		googleDomain = self._ensureHTTPorHTTPS(url=googleDomain, secure=secure)
		if self.checkBrowserAvailability(errorPrinting):
			self.browser.visit(googleDomain)

			self._waitBeforeTypingQueryIntoSearchBox(searchQueryString=searchQueryString, errorPrinting=errorPrinting)

			self.browser.fill('q', searchQueryString)
			button = self.browser.find_by_name('btnG')	## btnG was found by looking at google.com's HTML code.
			button.click()


			if self.isHeadless():
				url = self._ensureHTTPorHTTPS(self.browser.url, secure=secure)
				self.browser.visit(url)

			if not self.isHeadless():
				time.sleep(5)

			return self.browser.html
		else:
			return None
	

















class splinterBrowserPhantomJS(BrowserTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class splinterBrowser.

	_splinterErrorText = "One of the following softwares is not installed:\n\t> splinter		[install to Python with the command 'pip install splinter'].\n\t> selenium 		[usually packaged with splinter, you might need to update with 'pip install selenium --upgrade']"

	_phantomjsErrorText = "One of the following softwares is not installed:\n\t> phantomjs  	[refer to http://phantomjs.org as to how to install it to your machine (on Linux, 'apt-get install phantomjs' worked for me in Jan 2016)]"

	browser = None
	headless = True

	def isAvailable(self):
		if availableBrowsers.SPLINTER_PHANTOMJS is not None:
			return True
		return False



	def resetBrowser(self, errorPrinting=True):
		'''Reset the browser in case it does not seem to be working.'''
		try:
			self.browserClose(errorPrinting)
		except Exception,e :
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot close browser.",e)

		try:
			if self.isAvailable():
				if platform.system() == "Windows":
					self.browser = splinter.Browser("phantomjs", executable_path="./ExternalLibs/PhantomJS/Windows/phantomjs.exe")
				elif platform.system() == "Linux":
					self.browser = splinter.Browser("phantomjs", executable_path="./ExternalLibs/PhantomJS/Linux/phantomjs")
			return True
		except Exception, e:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot reset browser.",e)
		return False




	def browserClose(self, printing=False):
		if self.checkBrowserAvailability():
			try:
				self.browser.quit() 	## Usually quite glitchy.
				if printing: print("\nSuccessfully closed Splinter browser window.")
			except Exception, e:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to close Splinter phantomjs browser instance.",e)

		try:
			## see the following: https://github.com/hpcugent/easybuild/wiki/OS_flavor_name_version
			if platform.system() == "Linux" or platform.system() ==  "Darwin": ## Linux or MacOSX
				if os.system("killall phantomjs") == 0:
					return True
			elif platform.system() == "Windows":	## Windows
				if os.system('taskkill /f /im phantomjs.exe') == 0:
					return True

			# phantomjs_list = subprocess.Popen("ps -el |grep phantomjs", shell=True, stdout=subprocess.PIPE).stdout.read()
			# phantomjs_list = [y.strip().split(" ") for y in phantomjs_list.split("\n") if y.strip() != ""]
			# phantomjs_list = [[z for z in y if z!=""] for y in phantomjs_list]
			# phantomjs_pid_list = [(int(y[3]), y[-1]) for y in phantomjs_list]
			# for row in  phantomjs_list:
			# 	if row[1] == "phantomjs":
			# 		os.kill(row[0], signal.SIGKILL)
		except Exception, e:
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to kill phantomjs process.",e)

		return False





	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			self.browser.cookies.delete()
			return True
		return False




	def getName(self):
		nameString = "SPLINTER; Version=%s;"%splinter.__version__
		if self.isHeadless():
			nameString+=" Headless=yes;"
		else:
			nameString+=" Headless=no;"
		if self.checkBrowserAvailability():
			nameString += " Driver:%s;"%self.browser.driver_name
		return nameString








	def go(self, url, secure=False):
		url = self._ensureHTTPorHTTPS(url, secure)
		if self.checkBrowserAvailability():
			return self.browser.visit(url)
		return False


	def getCurrentPageUrl(self):
		if self.checkBrowserAvailability():
			url = self.browser.url
			if url!="" and url is not None:
				return url
		return None


	def getCurrentPageHtml(self):
		if self.checkBrowserAvailability():
			html = self.browser.html
			if html!="" and html is not None:
				return html
		return None



	def getInitialGoogleSearchResultsPageHtml(self, searchQueryString, googleDomain="http://www.google.com", secure=False, errorPrinting=False):

		googleDomain = self._ensureHTTPorHTTPS(url=googleDomain, secure=secure)
		if self.checkBrowserAvailability(errorPrinting):
			self.browser.visit(googleDomain)

			self._waitBeforeTypingQueryIntoSearchBox(searchQueryString=searchQueryString, errorPrinting=errorPrinting)

			self.browser.fill('q', searchQueryString)
			button = self.browser.find_by_name('btnG')	## btnG was found by looking at google.com's HTML code.
			button.click()


			if self.isHeadless():
				url = self._ensureHTTPorHTTPS(self.browser.url, secure=secure)
				self.browser.visit(url)

			if not self.isHeadless():
				time.sleep(5)

			return self.browser.html
		else:
			return None




class twillBrowser(BrowserTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class twillBrowser.

	_twillErrorText = "\n\n\tERROR: One of the following softwares is not installed:\n\t> 'twill' module version 0.9 [install to Python with 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported."
	
	browser = None
	headless = True
	
	try:
		import twill
		import twill.commands
		if twill.__version__ != "0.9":
			raise ImportError(_twillErrorText)

	except Exception:
		browser = None
		headless = None




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
			self.headless = None
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
				raise ImportError(self._twillErrorText)

		except Exception:
			if errorPrinting:
				print(self._twillErrorText)
			self.browser = None
			self.headless = None
			return False


		try:
			self.browserClose(errorPrinting)
			self.browser = twill.commands.get_browser()
			self.headless = True
			return True
		except Exception:
			if errorPrinting:
				print(self._phantomjsErrorText)
			self.browser = None
			self.headless = None
			return False



	def clearBrowserData(self):
		if self.checkBrowserAvailability():
			self.twill.commands.reset_browser()
			self.twill.commands.clear_cookies();
			self.twill.commands.reset_output();
			return True
		else:
			return False
	

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


# # x = splinterBrowser()
# x = twillBrowser()
# print(x.isHeadless())
# html = x.getInitialGoogleSearchResultsPageHtml(searchQueryString="man with cat", errorPrinting=True)
# print(len(html))
# gone = x.go("www.google.com")
# print(gone)
# html = x.getCurrentPageHtml()
# print(len(html))
# html = x.getHtml("www.google.com")
# print(len(html))
# x = splinterBrowser()
# print(x.test(printing=True))
b = splinter.Browser("phantomjs", executable_path="./ExternalLibs/PhantomJS/Windows/phantomjs.exe")
b.visit("https://github.com")
print len(b.html)