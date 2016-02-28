import datetime

class GoogleSearchQuery:

	## Note: the following imports are made in local scope, i.e. they are only visible inside the class GoogleSearchQuery.

	_canPerformDateTimeConversionToJulian = True
	try:
		from jdcal import gcal2jd
	except Exception:
		print("\n\n\n\tERROR in class GoogleSearchQuery: module jdcal not found, please install to Python [e.g. with the command 'pip install jdcal'].\n")
		_canPerformDateTimeConversionToJulian = False



	def __init__(self):
		self.daterangeFrom = None		## Should be a Julian date integer or a datetime object.
		self.daterangeTo = None			## Should be a Julian date integer or a datetime object.
		self.siteList = []
		self.necessaryTopicsList = []	## topics which MUST be present in the results. Enclosed by double quotes in query. 
		self.fuzzyTopicsList = [] ## topics which can also be present in the results. Not enclosed by double quotes in query.
		self.inurl = None ## a single word (or possibly multiple words separated by hyphens, underscores or periods) which must be in the search url. It is even more restrictive of results than necessaryTopic e.g. query: "site:facebook.com inurl:james-dean". 


	def canPerformDateTimeConversionToJulian(self):
		return self._canPerformDateTimeConversionToJulian


	def toString(self, randomShuffle=True):

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

		topicString = ""
		if self.necessaryTopicsList!=None and self.necessaryTopicsList!=[]:
			necessaryTopicString = ""
			for topic in self.necessaryTopicsList:
				necessaryTopicString+=' "%s"'%topic
			necessaryTopicString = necessaryTopicString.strip()
			topicString+=necessaryTopicString+" "


		if self.fuzzyTopicsList!=None and self.fuzzyTopicsList!=[]:
			fuzzyTopicString = ""
			for topic in self.fuzzyTopicsList:
				fuzzyTopicString+=' %s'%topic
			fuzzyTopicString = fuzzyTopicString.strip()
			topicString+=fuzzyTopicString

		queryList.append(topicString)


		if self.inurl != None and self.inurl!="":
			queryList.append('inurl:%s'%self.inurl)


		if self.daterangeFrom!=None and self.daterangeTo!=None and type(self.daterangeFrom)==type(0) and type(self.daterangeTo)==type(0) and self.daterangeFrom!=-1 and self.daterangeTo!=-1 and self.daterangeFrom<=self.daterangeFrom:
			queryList.append('daterange:%s-%s'%(self.daterangeFrom, self.daterangeTo))

		# print(queryList)
		queryList = [i.strip() for i in queryList]

		if randomShuffle:
			import random
			random.shuffle(queryList)

		query = ' '.join(queryList)
		query = query.strip()

		return query


	def setSiteList(self, siteList=None, printing=False):
		if siteList!=None and siteList!=[]:
			if False in [type(x)==type("") for x in siteList]:	## i.e. if there is any item in the list which is not a string
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setSiteList(): the site list cannot contain non-strings.")
				return False

			elif False in [x.find(" ")==-1 for x in siteList]: 
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setSiteList(): websites in the site list cannot contain a space in their url.")
				return False

			else: 
				self.siteList = siteList
				return True

		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery.setSiteList(): the list cannot be empty.")
			return False



	def setNecessaryTopicsList(self, necessaryTopicsList=None, printing=False):
		if necessaryTopicsList!=None and necessaryTopicsList!=[]:
			if False in [type(x)==type("") for x in necessaryTopicsList]:	## i.e. if there is any item in the list which is not a string
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setNecessaryTopicsList(): the list cannot contain non-strings.")
				return False
			self.necessaryTopicsList = necessaryTopicsList
			return True
		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery.setNecessaryTopicsList(): the list cannot be empty.")
			return False

			

	def setFuzzyTopicsList(self, fuzzyTopicsList=None, printing=False):
		if fuzzyTopicsList!=None and fuzzyTopicsList!=[]:
			if False in [type(x)==type("") for x in fuzzyTopicsList]:	## i.e. if there is any item in the list which is not a string
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setFuzzyTopicsList(): the list cannot contain non-strings.")
				return False
			self.fuzzyTopicsList = fuzzyTopicsList
			return True
		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery.setFuzzyTopicsList(): the list cannot be empty.")
			return False
			




	def setInUrl(self, inurl=None, printing=False):
		if inurl!=None:
			if inurl.find(" ")==-1 and inurl.find("\n")==-1:
				self.inurl = inurl
				return True
			else:
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setInUrl(): the url cannot have spaces or newlines in the word, only hyphens, underscores and periods.")
				return False
		else:
			if printing:
				print("\n\tERROR in GoogleSearchQuery.setInUrl(): please pass a value to the function.")
			return False





	def setDaterangeFrom(self, daterangeFrom=None, printing=False):
		newDaterangeFrom = self._convertToValidJulianDate(daterangeFrom, printing)
		if newDaterangeFrom!=-1:
			if newDaterangeFrom <= self.daterangeTo:
				self.daterangeFrom = newDaterangeFrom
				return True
			else:
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setDateRangeFrom(): daterangeFrom cannot be greater than daterangeTo.")
				return False
		else: 
			return False



	def setDaterangeTo(self, daterangeTo=None, printing=False):
		newDaterangeTo = self._convertToValidJulianDate(daterangeTo, printing)
		if newDaterangeTo!=-1:
			if newDaterangeTo >= self.daterangeFrom:
				self.daterangeTo = newDaterangeTo
				return True
			else:
				if printing:
					print("\n\tERROR in GoogleSearchQuery.setDaterangeTo(): daterangeTo cannot be less than daterangeFrom.")
				return False
		else: 
			return False
		


	def setDateRange(self, daterangeFrom=None, daterangeTo=None, printing=False):
		"""This function sets the daterange of the GoogleSearchQuery object. 
		If either of the values is invalid, it does not set the new daterange.""" 
		tempDaterangeFrom = self.daterangeFrom
		tempDaterangeTo = self.daterangeTo


		## for setting initially.
		if self.daterangeFrom == None:
			self.daterangeFrom = 0
		if self.daterangeTo == None:
			self.daterangeTo = 2816788	## 1st Jan 3000....assuming Google will be around that long.

		if self.setDaterangeFrom(daterangeFrom, printing) and self.setDaterangeTo(daterangeTo, printing):
			return True

		else: 	## rollback values which may be set in self.setDaterangeFrom() or self.setDaterangeTo
			self.daterangeFrom = tempDaterangeFrom 
			self.daterangeTo = tempDaterangeTo 
			return False





	def goToNextDateRange(self, newRange=None, printing=False):
		if self.daterangeFrom != None and self.daterangeTo!= None:
			if newRange == None:
				newRange = self.daterangeTo - self.daterangeFrom
			self.daterangeFrom = self.daterangeTo
			self.daterangeTo += newRange
			return True
		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery.goToNextDateRange(): daterangeFrom and daterangeTo are not set.")
			return False



	def goToPreviousDateRange(self, newRange=None, printing=False):
		if self.daterangeFrom != None and self.daterangeTo!= None:
			if newRange == None:
				newRange = self.daterangeTo - self.daterangeFrom
			self.daterangeTo = self.daterangeFrom
			self.daterangeFrom -= newRange
			return True
		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery.goToPreviousDateRange(): daterangeFrom and daterangeTo are not set.")
			return False


	def getTopicStringForDB(self, printingDebug=False):
		topicString = ""
		if self.necessaryTopicsList!=None and self.necessaryTopicsList!=[]:
			necessaryTopicString = ""
			for topic in self.necessaryTopicsList:
				necessaryTopicString+=' "%s"'%topic 	## Note: it is very important that this remains a double quote.
			necessaryTopicString = necessaryTopicString.strip()
			topicString+=necessaryTopicString+" "


		if self.fuzzyTopicsList!=None and self.fuzzyTopicsList!=[]:
			fuzzyTopicString = ""
			for topic in self.fuzzyTopicsList:
				fuzzyTopicString+=' %s'%topic
			fuzzyTopicString = fuzzyTopicString.strip()
			topicString+=fuzzyTopicString
		if printingDebug:
			print("\n\n\nTopic string for DB:\n%s\n\n"%topicString)
		return topicString


	def getDaterangeFrom(self):
		if self.daterangeFrom!=None:		
			return self.daterangeFrom
		return -1

	def getDaterangeTO(self):
		if self.daterangeTo!=None:	
			return self.daterangeTo
		return -1
		

	def getDateRangeTuple(self):
		if self.daterangeFrom!=None and self.daterangeTo!=None:
			return (self.daterangeFrom, self.daterangeTo)
		return (-1,-1)



	##-----------------------------------PRIVATE METHODS-----------------------------------##



	def _convertToValidJulianDate(self, daterangeDate, printing=False):
		"""This function converts daterange values to the appropriate Julian date integer.
		The dateranges are allowed to be entered as datetime.datetime objects, datetime.date objects, or integers which are assumed to be the julian date (cannot be smaller than start of UNIX time i.e. 1 Jan 1970)."""

		if daterangeDate != None:
			
			if type(daterangeDate)==type(datetime.datetime.now().date()) or type(daterangeDate)==type(datetime.datetime.now()):	## works on both datetime.datetime and datetime.date objects.
				return self._toJulianDateDatetime(daterangeDate, printing)
				

			elif type(daterangeDate) == type(0): 	## if it is an integer, assumed to be julian date.
				if daterangeDate >= 2440588:  ## start of UNIX time, i.e. 1 Jan 1970. Not 4 Sept 1998 (i.e. date of founding of Google as a company) because Google has pages from before it was created.
					return daterangeDate
				else:
					if printing:
						print("\n\tERROR in GoogleSearchQuery._convertToValidJulianDate(): daterangeDate has invalid value of %s, must not be before start of UNIX time i.e. 1 Jan 1970."%(daterangeDate))
					return -1


			else: 
				if printing:
					print("\n\tERROR in GoogleSearchQuery._convertToValidJulianDate(): daterangeDate has invalid value of '%s'. Should be a Julian date integer or a datetime object."%(daterangeDate))
				return -1



		else: 
			if printing:
				print("\n\tERROR in GoogleSearchQuery._convertToValidJulianDate(): daterangeDate not set.")
			return -1





	def _toJulianDateDatetime(self, dateTime, printing=False):		## takes as input a datetime.datetime object  or datetime.date object
		if self.canPerformDateTimeConversionToJulian():
			from jdcal import gcal2jd
			jd_tuple = gcal2jd(dateTime.year, dateTime.month, dateTime.day)
			julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
			return int(julian_day)
		else:
			if printing:
				print("\n\tERROR in GoogleSearchQuery._toJulianDateDatetime(): the julian conversion library jdcal has not been installed.")
			return -1






###-----------------------------TESTS-----------------------------###


# print("\n\n\nTesting GoogleSearchQuery:\n")

# from GoogleSearchQuery import GoogleSearchQuery
# x = GoogleSearchQuery()
# print(x.toString()) 
# x.setInUrl("lol")
# print(x.toString()) 
# x.setFuzzyTopicsList(['Beatles','liverpool'])
# print(x.toString()) 
# x.setNecessaryTopicsList(['Lennon','Strawberry'])
# print(x.toString()) 

# import datetime

# x.setDateRange(datetime.date(2015,3,15), datetime.date(2015,6,23))
# print(x.toString()) 
# x.setDateRange(datetime.date(2016,3,15), datetime.date(2015,6,25))
# print(x.toString()) 
# x.goToNextDateRange()
# print(x.toString()) 
# x.goToPreviousDateRange()
# x.goToPreviousDateRange()
# x.goToPreviousDateRange()
# print(x.toString()) 
# x.goToNextDateRange(30)
# print(x.toString()) 
# x.changeDaterangeFrom(datetime.date(2010,3,15), printing=True)
# print(x.toString()) 
# x.changeDaterangeTo(datetime.date(2010,3,17), printing=True)
# print(x.toString()) 
# x.setSiteList([])
# print(x.toString()) 
# x.setSiteList(['helloworld.com', 'thisistheend.co.in'])
# print(x.toString()) 





