





print("\n\n\nTesting BrowserHandler:\n")

from BrowserHandler import BrowserHandler
b = BrowserHandler()
print(b.checkBrowser())
print type(b.browser)
y = b.getHtml(url="http://www.facebook.com")
print(y)	
print(len(y))



# import splinter
# browser_js = splinter.Browser("phantomjs")
# browser_js.visit("http://www.google.co.in")
# print(len(browser_js.html))