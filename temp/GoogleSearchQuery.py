import datetime

class GoogleSearchQuery:
	def __init__(self):

		self._canPerformDateTimeConversionToJulian = True
		try:
			from jdcal import gcal2jd
		except Exception:
			print("\n\n\n\tERROR: module jdcal not found, please install to Python [e.g. with the command 'pip install jdcal'].\n")
			self._canPerformDateTimeConversionToJulian = False

		self.daterangeFrom = None
		self.daterangeTo = None
		self.siteList = None
		self.necessaryTopicsList = None	## topics which MUST be present in the results. Enclosed by double quotes in query. 
		self.fuzzyTopicsList = None ## topics which can also be present in the results. Not enclosed by double quotes in query.
		self.inurl = None ## a single word (or possibly multiple words separated by hyphens, underscores or periods) which must be in the search url. It is even more restrictive of results than necessaryTopic e.g. query: "site:facebook.com inurl:james-dean". 


	def canPerformDateTimeConversionToJulian(self):
		return self._canPerformDateTimeConversionToJulian


	def toString(self, randomShuffle=False):

		if (self.necessaryTopicsList==None or self.necessaryTopicsList==[]) and (self.fuzzyTopicsList==None   or   self.fuzzyTopicsList==[]):	## there are no topics in the GoogleSearchQuery object.
			return ""


		queryList=[]

		if self.siteList!=None and self.siteList!=[]:
			siteString = ""
			siteString += 'site:'+self.siteList[0]
			for i in range(1,len(self.siteList)):
				siteString += ' | site:'+self.siteList[i]
			siteString = siteString.strip()
			queryList.append(siteString)


		if self.necessaryTopicsList!=None and self.necessaryTopicsList!=[]:
			necessaryTopicString = ""
			for topic in self.necessaryTopicsList:
				necessaryTopicString+=' "%s"'%topic
			necessaryTopicString = necessaryTopicString.strip()
			queryList.append(necessaryTopicString)


		if self.fuzzyTopicsList!=None and self.fuzzyTopicsList!=[]:
			fuzzyTopicString = ""
			for topic in self.fuzzyTopicsList:
				fuzzyTopicString+=' %s'%topic
			fuzzyTopicString = fuzzyTopicString.strip()
			queryList.append(fuzzyTopicString)


		if self.inurl != None and self.inurl!="":
			queryList.append('inurl:%s'%self.inurl)


		if self.daterangeFrom!=None and self.daterangeTo!=None and self.daterangeFrom<=self.daterangeFrom:
			queryList.append('daterange:%s-%s'%(self.daterangeFrom, self.daterangeTo))

		# print(queryList)
		if randomShuffle:
			import random
			random.shuffle(queryList)

		query = ' '.join(queryList)
		query = query.strip()

		return query


	def setSiteList(self, siteList=None, errorPrinting=False):
		if siteList!=None and siteList!=[]:
			if False in [type(x)==type("") for x in siteList]:	## i.e. if there is any item in the list which is not a string
				if errorPrinting:
					print("\n\tERROR in setSiteList(): the site list cannot contain non-strings.")
				return False

			elif False in [x.find(" ")==-1 for x in siteList]: 
				if errorPrinting:
					print("\n\tERROR in setSiteList(): websites in the site list cannot contain a space in their url.")
				return False

			else: 
				self.siteList = siteList
				return True

		else: 
			if errorPrinting:
				print("\n\tERROR in setSiteList(): the list cannot be empty.")
			return False



	def setNecessaryTopicsList(self, necessaryTopicsList=None, errorPrinting=False):
		if necessaryTopicsList!=None and necessaryTopicsList!=[]:
			if False in [type(x)==type("") for x in necessaryTopicsList]:	## i.e. if there is any item in the list which is not a string
				if errorPrinting:
					print("\n\tERROR in setNecessaryTopicsList(): the list cannot contain non-strings.")
				return False
			self.necessaryTopicsList = necessaryTopicsList
			return True
		else: 
			if errorPrinting:
				print("\n\tERROR in setNecessaryTopicsList(): the list cannot be empty.")
			return False

			

	def setFuzzyTopicsList(self, fuzzyTopicsList=None, errorPrinting=False):
		if fuzzyTopicsList!=None and fuzzyTopicsList!=[]:
			if False in [type(x)==type("") for x in fuzzyTopicsList]:	## i.e. if there is any item in the list which is not a string
				if errorPrinting:
					print("\n\tERROR in setFuzzyTopicsList(): the list cannot contain non-strings.")
				return False
			self.fuzzyTopicsList = fuzzyTopicsList
			return True
		else: 
			if errorPrinting:
				print("\n\tERROR in setFuzzyTopicsList(): the list cannot be empty.")
			return False
			




	def setInUrl(self, inurl=None, errorPrinting=False):
		if inurl!=None:
			if inurl.find(" ")==-1 and inurl.find("\n")==-1:
				self.inurl = inurl
				return True
			else:
				if errorPrinting:
					print("\n\tERROR in setInUrl(): the url cannot have spaces or newlines in the word, only hyphens, underscores and periods.")
				return False
		else:
			if errorPrinting:
				print("\n\tERROR in setInUrl(): please pass a value to the function.")
			return False





	def changeDaterangeFrom(self, daterangeFrom=None, errorPrinting=False):
		newDaterangeFrom = self._convertToValidJulianDate(daterangeFrom, errorPrinting)
		if newDaterangeFrom!=-1:
			if newDaterangeFrom <= self.daterangeTo:
				self.daterangeFrom = newDaterangeFrom
				return True
			else:
				if errorPrinting:
					print("\n\tERROR in setDateRangeFrom(): daterangeFrom cannot be greater than daterangeTo.")
				return False
		else: 
			return False



	def changeDaterangeTo(self, daterangeTo=None, errorPrinting=False):
		newDaterangeTo = self._convertToValidJulianDate(daterangeTo, errorPrinting)
		if newDaterangeTo!=-1:
			if newDaterangeTo >= self.daterangeFrom:
				self.daterangeTo = newDaterangeTo
				return True
			else:
				if errorPrinting:
					print("\n\tERROR in setDaterangeTo(): daterangeTo cannot be less than daterangeFrom.")
				return False
		else: 
			return False
		


	def setDateRange(self, daterangeFrom=None, daterangeTo=None, errorPrinting=False):
		"""This function sets the daterange of the GoogleSearchQuery object. 
		If either of the values is invalid, it does not set the new daterange.""" 
		tempDaterangeFrom = self.daterangeFrom
		tempDaterangeTo = self.daterangeTo


		## for setting initially.
		if self.daterangeFrom == None:
			self.daterangeFrom = 0
		if self.daterangeTo == None:
			self.daterangeTo = 2816788	## 1st Jan 3000....assuming Google will be around that long.

		if self.changeDaterangeFrom(daterangeFrom, errorPrinting) and self.changeDaterangeTo(daterangeTo, errorPrinting):
			return True

		else: 	## rollback values which may be set in self.setDaterangeFrom() or self.setDaterangeTo
			self.daterangeFrom = tempDaterangeFrom 
			self.daterangeTo = tempDaterangeTo 
			return False





	def goToNextDateRange(self, newRange=None, errorPrinting=False):
		if self.daterangeFrom != None and self.daterangeTo!= None:
			if newRange == None:
				newRange = self.daterangeTo - self.daterangeFrom
			self.daterangeFrom = self.daterangeTo
			self.daterangeTo += newRange
			return True
		else: 
			if errorPrinting:
				print("\n\tERROR in goToNextDateRange(): daterangeFrom and daterangeTo are not set.")
			return False



	def goToPreviousDateRange(self, newRange=None, errorPrinting=False):
		if self.daterangeFrom != None and self.daterangeTo!= None:
			if newRange == None:
				newRange = self.daterangeTo - self.daterangeFrom
			self.daterangeTo = self.daterangeFrom
			self.daterangeFrom -= newRange
			return True
		else: 
			if errorPrinting:
				print("\n\tERROR in goToPreviousDateRange(): daterangeFrom and daterangeTo are not set.")
			return False





	##-----------------------------------PRIVATE METHODS-----------------------------------##



	def _convertToValidJulianDate(self, daterangeDate, errorPrinting=False):
		"""This function converts daterange values to the appropriate Julian date integer.
		The dateranges are allowed to be entered as datetime.datetime objects, datetime.date objects, or integers which are assumed to be the julian date (cannot be smaller than start of UNIX time i.e. 1 Jan 1970)."""

		if daterangeDate != None:
			
			if type(daterangeDate)==type(datetime.datetime.now().date()) or type(daterangeDate)==type(datetime.datetime.now()):	## works on both datetime.datetime and datetime.date objects.
				return self._toJulianDateDatetime(daterangeDate, errorPrinting)
				

			elif type(daterangeDate) == type(0): 	## if it is an integer, assumed to be julian date.
				if daterangeDate >= 2440588:  ## start of UNIX time, i.e. 1 Jan 1970. Not 4 Sept 1998 (i.e. date of founding of Google as a company) because Google has pages from before it was created.
					return daterangeDate
				else:
					if errorPrinting:
						print("\n\tERROR in _convertToValidJulianDate(): daterangeDate has invalid value of %s, must not be before start of UNIX time i.e. 1 Jan 1970."%(daterangeDate))
					return -1


			else: 
				if errorPrinting:
					print("\n\tERROR in _convertToValidJulianDate(): daterangeDate has invalid value of '%s'"%(daterangeDate))
				return -1



		else: 
			if errorPrinting:
				print("\n\tERROR in _convertToValidJulianDate(): daterangeDate not set.")
			return -1





	def _toJulianDateDatetime(self, dateTime, errorPrinting=False):		## takes as input a datetime.datetime object  or datetime.date object
		if self.canPerformDateTimeConversionToJulian():
			from jdcal import gcal2jd
			jd_tuple = gcal2jd(dateTime.year, dateTime.month, dateTime.day)
			julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
			return int(julian_day)
		else:
			if errorPrinting:
				print("\n\tERROR in _toJulianDateDatetime(): the julian conversion library jdcal has not been installed.")
			return -1




