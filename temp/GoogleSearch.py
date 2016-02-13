'''
DISCLAIMER: This code document is for personal use only. Any violation of the Google Terms of Service is not the responsibility of the authors of the document and is performed at your own risk. 
	...Just so you know, this sort of thing does violate the Google ToS. We (the authors) personally did not use it in production code, only as an experiment in twill commands. We hope that you do the same.
'''


class GoogleSearch:
	def __init__(self):

		import random

		canRun = True
		try:
			from GoogleSearchQuery import GoogleSearchQuery
		except Exception:
			print("\n\n\n\tFatal ERROR in class GoogleSearch: cannot locate module GoogleSearchQuery.py")
			canRun = False

		try:
			from GoogleWebsiteParser import GoogleWebsiteParser
		except Exception:
			print("\n\n\n\tFatal ERROR in class GoogleSearch: cannot locate module GoogleWebsiteParser.py")
			canRun = False

		try:
			from BrowserHandler import BrowserHandler
		except Exception:
			print("\n\n\n\tFatal ERROR in class GoogleSearch: cannot locate module BrowserHandler.py")
			canRun = False


		self.browser = BrowserHandler()
