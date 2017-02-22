import platform
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import SearchDistribute.Enums
import datetime
import io
from bs4 import BeautifulSoup as BS

from SearchDistribute import Enums
from SearchDistribute.SearchExtractorErrors import *


phantomjs_path = None
if platform.system() == "Windows":
	phantomjs_path = "./PhantomJS/Windows/phantomjs.exe"
elif platform.system() == "Linux":
	phantomjs_path = "/mnt/Data/Workspaces/Python/GoogleExtractor/SearchDistribute/PhantomJS/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
'''

availableBrowsers = Enum([]) #["SPLINTER", "TWILL0_9", "SPLINTER_PHANTOMJS"]
try:
	import splinter
	availableBrowsers.SPLINTER="SPLINTER"
	availableBrowsers.SPLINTER_PHANTOMJS="SPLINTER_PHANTOMJS"
except Exception:
	make_error("ProxyBrowsers.py", "__main__", "Could not import splinter and splinter phantomjs")




class BrowserTemplate(object):
	browser = None
	headless = None

	def __init__(self, printing=False):
		self.startBrowser(printing)


	def isHeadless(self):
		return self.headless

	def startBrowser(self, errorPrinting=True):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def closeBrowser(self, errorPrinting=True):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def resetBrowser(self, errorPrinting=True):
		"""Reset the browser in case it does not seem to be working."""
		if not self.closeBrowser(errorPrinting):
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot close browser.")
			return False
		if not self.startBrowser(errorPrinting):
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot start browser.")
			return False
		return True




	def test(self, printing=True):
		test_url = "https://github.com/"
		performed_full_test = True

		if printing: print("\n\n\n###----------Test for browser: \t\t"+self.getName()+"----------###")
		start_time = time.time()
		if self.startBrowser(printing):
			if printing: print("\tStart time: %s seconds"%(time.time()-start_time))
		else:
			print_fatal_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Could not start browser.")
			performed_full_test = False

		html = None
		try:
			visit_time=time.time()
			self.go(test_url)	## a small test page, around 26 KB
			html = self.getCurrentPageHtml()

			if html is not None and len(html)>20:
				if printing:
					print("\tPage visit time: %s seconds for visiting %s of length %s characters."%(time.time()-visit_time, test_url,len(html)))
			else:
				print_fatal_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Browser could not obtain HTML from the web.")
				performed_full_test = False

			close_time = time.time()
			if not self.closeBrowser(printing):
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "browser used for testing cannot be closed.")
				performed_full_test = False
			else:
				if printing:
					print("\tClose time: %s seconds"%(time.time()-close_time))

		except Exception:
			print_fatal_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Browser could not complete the test.")

		if printing:
			if performed_full_test:
				print("\n###----------Successfully ran test for browser: \t\t"+self.getName()+"----------###")
			else:
				print("\n###----------Failed test for browser: \t\t"+self.getName()+"----------###")


		return performed_full_test




	def isAvailable(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))

	def checkBrowserAvailability(self, errorPrinting=False):
		if self.browser is not None:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name, "Browser is available.")
			return True
		print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name, "Browser is not available.")
		return False

	def getName(self):
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


	## Methods for avoiding IP-blocking
	def clearBrowserData(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))



	@staticmethod
	def _ensureHTTPorHTTPS(url, secure):
		if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
			if secure: url = 'https://'+url
			else: url = 'http://'+url
		elif secure and url.lower().startswith('http://'):
			url = 'https://' + url[len('http://'):]
		elif not secure and url.lower().startswith('https://'):
			url = 'http://' + url[len('https://'):]
		return url


	@staticmethod
	def _waitBeforeTypingQueryIntoSearchBox(self, searchQueryString, errorPrinting=True):

		searchQueryStringLen=len(searchQueryString)
		waitTime = random.uniform(searchQueryStringLen/float(5), searchQueryStringLen/float(3))	## wait a random amount of time. This assumes that the average typing speed is between 3 and 5 characters per second.
		if errorPrinting:
			print("\t\t\tWaiting for %s seconds before entering query into search box."%waitTime)
		time.sleep(waitTime)



'''
''' Note that as of 19 Feb 2017, Firefox and Chrome do not support SOCKS5 authentication [1], but PhantomJS does [2].
[1] https://www.privateinternetaccess.com/forum/discussion/2915/setting-up-the-socks5-proxy-on-chrome-firefox
[2] http://stackoverflow.com/a/16353584/4900327  and  http://stackoverflow.com/a/26931933/4900327
'''

class PhantomJS():
	proxy_browser_type = Enums.ProxyBrowsers.PhantomJS
	headless = True
	proxy_args = {}			## (optional, defaults to None) A hashtable with the following values: proxy_type, hostname, port, username, password.
							##  - proxy_type : a string denoting the type of proxy, e.g. Socks5, HTTP etc. Must be from Enums.ProxyTypes
							##  - hostname : a string of the name or ip address of the proxy server.
							##  - port : a string of the port at the proxy server to which the webdriver must connect.
							##  - username : (optional, defaults to None) a string of the proxy authentication username
							##  - password : (optional, defaults to None) a string of the proxy authentication password
	webdriver = None		## The selenium object. This should not be refreshed.

	def __init__(self, proxy_args):
		'''
		Here, proxy_args may be None. In that case, we instantiate the default browser.

		Example proxy_args with all parameters set:
		{
			"proxy_type" : Enums.ProxyTypes.Socks5,
			"hostname" : "proxy-nl.privateinternetaccess.com",
			"port" : "1080",
			"username" : "x1237029",
			"password" : "3iV3za46xD"
		}
		'''
		self.proxy_args = proxy_args	## Defaults to None
		service_args = ['--load-images=no']
		if proxy_args is not None:
			proxy_type = proxy_args.get('proxy_type')
			if proxy_type not in Enums.ProxyTypes:
				raise InvalidProxyParameterException(self.proxy_browser_type, 'proxy_type', proxy_type, "must be a non-empty string from %s"%Enums.ProxyTypes)

			hostname = proxy_args.get('hostname')
			if type(hostname) != type("") or len(hostname) == 0:
				raise InvalidProxyParameterException(self.proxy_browser_type, 'hostname', hostname, "must be a non-empty string")

			port = proxy_args.get('port')
			if type(port) != type(0) or port<0 or port>65535:
				raise InvalidProxyParameterException(self.proxy_browser_type, 'port', port, "must be an interger between 0 and 65535 (inclusive)")

			username = proxy_args.get('username')	## Can be None
			password = proxy_args.get('password')	## Can be None
			## For PrivateInternetAccess.com : https://www.privateinternetaccess.com/forum/discussion/258/private-internet-access-proxy-now-available-now-open
			## Source: http://stackoverflow.com/a/16353584/4900327
			if proxy_type == Enums.ProxyTypes.Socks5:
				phantomjs_socks5_proxy_service_args = ['--proxy=%s:%s'%(hostname, port), '--proxy-type=socks5']
				if username is not None and password is not None:
					if type(username) != type("") or len(username) == 0:
						raise InvalidProxyParameterException(self.proxy_browser_type, 'username', username, "must be a non-empty string")
					if type(password) != type("") or len(password) == 0:
						raise InvalidProxyParameterException(self.proxy_browser_type, 'password', password, "must be a non-empty string")
					phantomjs_socks5_proxy_service_args += ['--proxy-auth=%s:%s'%(username, password)]
				service_args += phantomjs_socks5_proxy_service_args
		self.webdriver = webdriver.PhantomJS(service_args = service_args, executable_path=phantomjs_path)

	def visit(self, url):
		self.webdriver.get(url)
		self.last_loaded_time = datetime.datetime.now()

	def get_html(self):
		return self.webdriver.page_source

	def get_url(self):
		return self.webdriver.current_url

	def close(self):
		'''This closes the current window. Note: webdriver.quit() kills the phantomjs executable, which means you cannot produce more phantomjs instances.
		The quit() functionality is hence not exposed.
		'''
		self.webdriver.close()
		self.webdriver = None

	def switch_proxy(self):
		self.webdriver.close()
		self.webdriver = webdriver.PhantomJS(service_args = self.service_args)

	## Source: http://stackoverflow.com/questions/24053671/webdriver-wait-for-ajax-request-in-python/24053891#24053891
	## and http://stackoverflow.com/a/26949021/4900327
	def wait_for_element_to_load_ajax(self, timeout, element_css_selector):
		try:
			## Wait for the AJAX to load.
			WebDriverWait(self.webdriver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_css_selector)))
			return True
		except Exception:  ## The WebDriverWait timed out.
			print("Webdriver has timed out.")
			self._log_state()
			return False

	def _log_state(self, timeout):
		now = datetime.datetime.now()
		with io.open("./search_logs/UTC %s-%s-%s %s-%s-%s.html" % (
		now.year, now.month, now.day, now.hour, now.minute, now.second), "w+") as out:
			out.write("<!--Timeout time: %s seconds-->\n\n<!--URL:\n%s-->\n\n<!--HTML:-->\n%s" % (timeout, self.get_url(), BS(self.get_html()).prettify()))



# print("\n\tSplinter is the default headless client of this package as it is more reliable.")
'''


class splinterBrowser(BrowserTemplate):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class splinterBrowser.


	browser = None
	headless = False

	def isAvailable(self):
		if availableBrowsers.SPLINTER is not None:
			return True
		return False

	def startBrowser(self, errorPrinting=True):
		try:
			if self.isAvailable():
				self.browser = splinter.Browser()
				return True
		except Exception:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot start splinter browser.")
		return False

	def closeBrowser(self, printing=False):
		if self.checkBrowserAvailability():
			try:
				self.browser.quit()
				if printing: print("\nSuccessfully closed Splinter browser window.")
				return True
			except Exception:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to close Splinter browser window.")
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
	

















class splinterBrowserPhantomJS(splinterBrowser):

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class splinterBrowser.

	browser = None
	headless = True

	def isAvailable(self):
		if availableBrowsers.SPLINTER_PHANTOMJS is not None:
			return True
		return False


	def startBrowser(self, errorPrinting=True):
		try:
			if self.isAvailable():
				self.browser = splinter.Browser("phantomjs", executable_path=phantomjs_path)
				return True
		except Exception:
			print_error(errorPrinting, self.__class__.__name__, sys._getframe().f_code.co_name,"Cannot create phantomjs process.")
		return False


	def closeBrowser(self, printing=False):
		if self.checkBrowserAvailability():
			try:
				self.browser.quit() 	## Usually quite glitchy.
				if printing:
					print("\nSuccessfully closed Splinter browser window.")
				return True			## this line has been added as code belpw has been commented out.
			except Exception:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to close Splinter phantomjs browser instance.")

		## The following code has become redundant with the inclusion of phantomJS executables in the project itself, which allows self.browser.quit() to work perfectly well:
		# try:
		# 	## see the following: https://github.com/hpcugent/easybuild/wiki/OS_flavor_name_version
		# 	if platform.system() == "Linux" or platform.system() ==  "Darwin": ## Linux or MacOSX
		# 		if os.system("killall phantomjs") == 0:
		# 			return True
		# 	elif platform.system() == "Windows":	## Windows
		# 		if os.system('taskkill /f /im phantomjs.exe') == 0:
		# 			return True
        #
		# except Exception, e:
		# 	print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name,"Unable to kill phantomjs process.",e)

		return False






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


	def closeBrowser(self, errorPrinting=False):
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
			self.closeBrowser(errorPrinting)
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
# sb=splinterBrowser()
# sb.test(printing=True)
# sbJS = splinterBrowserPhantomJS()
# sbJS.test(printing=True)


'''
