import sys
import random
import datetime
from jdcal import gcal2jd
from SearchExtractorErrors import print_error

class GoogleSearchQuery:
	config = {}
	daterangeFrom = None		## Should be a Julian date integer or a datetime object.
	daterangeTo = None			## Should be a Julian date integer or a datetime object.
	siteList = None
	necessaryTopicsList = None	## topics which MUST be present in the results. Enclosed by double quotes in query.
	fuzzyTopicsList = None ## topics which can also be present in the results. Not enclosed by double quotes in query.
	inurl = None ## a single word (or possibly multiple words separated by hyphens, underscores or periods) which must be in the search url. It is even more restrictive of results than necessaryTopic e.g. query: "site:facebook.com inurl:james-dean".
	intitle = None


	def __init__(self, config=None, printing=False):
		if config is not None and type(config) is type({}):
			self.config = config
			config_chooser = lambda x,y: config.get(x) if config.get(x) is not None else config.get(y)

			self.setSiteList(config_chooser('siteList', 'site_list'), printing)
			self.setNecessaryTopicsList(config_chooser('necessaryTopicsList', 'necessary_topics_list'), printing)
			self.setFuzzyTopicsList(config_chooser('fuzzyTopicsList', 'fuzzy_topics_list'), printing)
			self.setDateRangeFrom(config_chooser('daterangeFrom','daterange_from'))
			self.setDateRangeTo(config_chooser('daterangeTo','daterange_to'))
			self.setInUrl(config_chooser('inurl', None), printing)
			self.setInTitle(config_chooser('intitle', None), printing)




	def toString(self, randomShuffle=True):

		if (self.necessaryTopicsList is None or self.necessaryTopicsList==[]) and (
				self.fuzzyTopicsList is None or self.fuzzyTopicsList==[]):	## there are no topics in the GoogleSearchQuery object.
			return ""


		queryList=[]

		if self.siteList is not None and self.siteList!=[]:
			siteString = ""
			siteString += 'site:'+self.siteList[0]
			for i in range(1,len(self.siteList)):
				siteString += ' | site:'+self.siteList[i]
			siteString = siteString.strip()
			queryList.append(siteString)

		topicString = ""
		if self.necessaryTopicsList is not None and self.necessaryTopicsList!=[]:
			necessaryTopicString = ""
			for topic in self.necessaryTopicsList:
				necessaryTopicString+=' "%s"'%topic
			necessaryTopicString = necessaryTopicString.strip()
			topicString+=necessaryTopicString+" "


		if self.fuzzyTopicsList is not None and self.fuzzyTopicsList!=[]:
			fuzzyTopicString = ""
			for topic in self.fuzzyTopicsList:
				fuzzyTopicString+=' %s'%topic
			fuzzyTopicString = fuzzyTopicString.strip()
			topicString+=fuzzyTopicString

		queryList.append(topicString)


		if self.inurl is not None and self.inurl!= "":
			queryList.append('inurl:%s'%self.inurl)


		if self.daterangeFrom is not None and self.daterangeTo is not None and type(self.daterangeFrom)==type(0) and type(self.daterangeTo)==type(0) and self.daterangeFrom!=-1 and self.daterangeTo!=-1 and self.daterangeFrom<=self.daterangeFrom:
			queryList.append('daterange:%s-%s'%(self.daterangeFrom, self.daterangeTo))

		# print(queryList)
		queryList = [i.strip() for i in queryList]

		if randomShuffle:
			random.shuffle(queryList)

		query = ' '.join(queryList)
		query = query.strip()

		return query


	def setSiteList(self, siteList=None, printing=False):
		if siteList is not None:
			if siteList!=[]:
				if False in [type(x)==type("") for x in siteList]:	## i.e. if there is any item in the list which is not a string
					print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the site list cannot contain non-strings.")
					return False

				elif False in [x.find(" ")==-1 for x in siteList]:
					print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "websites in the site list cannot contain a space in their url.")
					return False

				else:
					self.siteList = siteList
					## update config
					self.config['siteList']=siteList
					self.config['site_list']=siteList
					return True
			else:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the list cannot be empty.")
		return False



	def setNecessaryTopicsList(self, necessaryTopicsList=None, printing=False):
		if necessaryTopicsList is not None:
			if necessaryTopicsList!=[]:
				if False in [type(x)==type("") for x in necessaryTopicsList]:	## i.e. if there is any item in the list which is not a string
					print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the list cannot contain non-strings.")
					return False
				self.necessaryTopicsList = necessaryTopicsList
				## update config
				self.config['necessaryTopicsList'] = necessaryTopicsList
				self.config['necessary_topics_list'] = necessaryTopicsList
				return True
			else:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the list cannot be empty.")
		return False

			

	def setFuzzyTopicsList(self, fuzzyTopicsList=None, printing=False):
		if fuzzyTopicsList is not None :
			if fuzzyTopicsList!=[]:
				if False in [type(x)==type("") for x in fuzzyTopicsList]:	## i.e. if there is any item in the list which is not a string
					print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the list cannot contain non-strings.")
					return False
				self.fuzzyTopicsList = fuzzyTopicsList
				## update config
				self.config['fuzzyTopicsList']=fuzzyTopicsList
				self.config['fuzzy_topics_list']=fuzzyTopicsList
				return True
			else:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the list cannot be empty.")
		return False
			




	def setInUrl(self, inurl=None, printing=False):
		if inurl is not None:
			inurl=inurl.strip()
			if inurl.find("\n")==-1:
				if inurl.find(" ")!= -1:		## is there's multiple words, surround them with quotes
					inurl = '"%s"'%inurl
				self.inurl = inurl
				## update config
				self.config['inurl'] = inurl
				return True
			else:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the url cannot have newlines in the word, only spaces, hyphens, underscores and periods.")
		return False


	def setInTitle(self, intitle=None, printing=False):
		if intitle is not None:
			intitle=intitle.strip()
			if intitle.find("\n")==-1:
				if intitle.find(" ")!= -1:		## is there's multiple words, surround them with quotes
					intitle = '"%s"'%intitle
				self.intitle = intitle
				## update config
				self.config['intitle'] = intitle
				return True
			else:
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "the title cannot have newlines in the word, only spaces, hyphens, underscores and periods.")
		return False




	def setDateRangeFrom(self, daterangeFrom=None, printing=False):
		if daterangeFrom is not None:
			newDaterangeFrom = self._convertToValidJulianDate(daterangeFrom, printing)
			if newDaterangeFrom!=-1:
				if self.daterangeTo is not None:
					if newDaterangeFrom <= self.daterangeTo:
						self.daterangeFrom = newDaterangeFrom
						## update config
						self.config['daterangeFrom']=newDaterangeFrom
						self.config['daterange_from']=newDaterangeFrom
						return True
					else:
						print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeFrom cannot be greater than daterangeTo.")
						return False
				else:
					self.daterangeFrom = newDaterangeFrom
					## update config
					self.config['daterangeFrom']=newDaterangeFrom
					self.config['daterange_from']=newDaterangeFrom
					return True

		return False



	def setDateRangeTo(self, daterangeTo=None, printing=False):
		if daterangeTo is not None:
			newDaterangeTo = self._convertToValidJulianDate(daterangeTo, printing)
			if newDaterangeTo!=-1:
				if self.daterangeFrom is not None:
					if newDaterangeTo >= self.daterangeFrom:
						self.daterangeTo = newDaterangeTo
						## update config
						self.config['daterangeTo']=newDaterangeTo
						self.config['daterange_to']=newDaterangeTo
						return True
					else:
						print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeTo cannot be less than daterangeFrom.")
						return False
				else:
					self.daterangeTo = newDaterangeTo
					## update config
					self.config['daterangeTo']=newDaterangeTo
					self.config['daterange_to']=newDaterangeTo
					return True
		return False



	def setDateRange(self, daterangeFrom=None, daterangeTo=None, printing=False):
		"""This function sets the daterange of the GoogleSearchQuery object. 
		If either of the values is invalid, it does not set the new daterange.""" 
		tempDaterangeFrom = self.daterangeFrom
		tempDaterangeTo = self.daterangeTo


		## for setting initially.
		if self.daterangeFrom is None:
			self.daterangeFrom = 0
		if self.daterangeTo is None:
			self.daterangeTo = 2816788	## 1st Jan 3000....assuming Google will be around that long.

		if self.setDateRangeFrom(daterangeFrom, printing) and self.setDateRangeTo(daterangeTo, printing):
			return True

		else: 	## rollback values which may be set in self.setDateRangeFrom() or self.setDateRangeTo
			self.setDateRangeFrom(tempDaterangeFrom)
			self.setDateRangeTo(tempDaterangeTo)
		return False





	def goToNextDateRange(self, newRange=None, printing=False):
		if self.daterangeFrom is not None and self.daterangeTo is not None:
			if newRange is None:
				newRange = self.daterangeTo - self.daterangeFrom
			self.setDateRange(self.daterangeTo, self.daterangeTo + newRange)
			return True
		else: 
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeFrom and daterangeTo are not set.")
		return False



	def goToPreviousDateRange(self, newRange=None, printing=False):
		if self.daterangeFrom is not None and self.daterangeTo is not None:
			if newRange is None:
				newRange = self.daterangeTo - self.daterangeFrom	## the difference = length of time period
			self.setDateRange(self.daterangeFrom - newRange, self.daterangeFrom)
			return True
		else: 
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeFrom and daterangeTo are not set.")
		return False



	def getConfig(self):
		return self.config


	def getTopicStringForDB(self, printingDebug=False):
		"""
		This returns the topic string that we use to index the query in the database. Unline the toString() function, this string should not be randomly shuffled, and should instead always follow the same format. Here, the format is: sorted neccessaryTopicList, sorted fuzzyTopicList
		Args:
		    printingDebug:

		Returns: a string. For all similar configs, it will be the same.
		"""
		topicString = ""
		if self.necessaryTopicsList is not None and self.necessaryTopicsList!=[]:
			necessaryTopicString = ""
			for topic in sorted(self.necessaryTopicsList):
				necessaryTopicString+=' "%s"'%topic 	## Note: it is very important that this remains a double quote.
			necessaryTopicString = necessaryTopicString.strip()
			topicString+=necessaryTopicString+" "


		if self.fuzzyTopicsList is not None and self.fuzzyTopicsList!=[]:
			fuzzyTopicString = ""
			for topic in sorted(self.fuzzyTopicsList):
				fuzzyTopicString+=' %s'%topic
			fuzzyTopicString = fuzzyTopicString.strip()
			topicString+=fuzzyTopicString
		if printingDebug:
			print("\n\n\nTopic string for DB:\n%s\n\n"%topicString)
		return topicString


	def getDaterangeFrom(self):
		if self.daterangeFrom is not None:
			return self.daterangeFrom
		return -1

	def getDaterangeTo(self):
		if self.daterangeTo is not None:
			return self.daterangeTo
		return -1
		

	def getDateRangeTuple(self):
		if self.daterangeFrom is not None and self.daterangeTo is not None:
			return (self.daterangeFrom, self.daterangeTo)	## returns a tuple
		return (-1,-1)



	##-----------------------------------PRIVATE METHODS-----------------------------------##



	def _convertToValidJulianDate(self, daterangeDate, printing=False):
		"""This function converts daterange values to the appropriate Julian date integer.
		The dateranges are allowed to be entered as datetime.datetime objects, datetime.date objects, or integers which are assumed to be the julian date (cannot be smaller than start of UNIX time i.e. 1 Jan 1970)."""

		if daterangeDate is not None:
			
			if type(daterangeDate)==type(datetime.datetime.now().date()) or type(daterangeDate)==type(datetime.datetime.now()):	## works on both datetime.datetime and datetime.date objects.
				return self._toJulianDateDatetime(daterangeDate)
				

			elif type(daterangeDate) == type(0): 	## if it is an integer, assumed to be julian date.
				if daterangeDate >= 2440588:  ## start of UNIX time, i.e. 1 Jan 1970. Not 4 Sept 1998 (i.e. date of founding of Google as a company) because Google has pages from before it was created.
					return daterangeDate
				else:
					print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeDate has invalid value of %s, must not be before start of UNIX time i.e. 1 Jan 1970."%(daterangeDate))

			else: 
				print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeDate has invalid value of '%s'. Should be a Julian date integer or a datetime object."%(daterangeDate))

		else: 
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "daterangeDate not set.")
		return -1





	def _toJulianDateDatetime(self, dateTime):		## takes as input a datetime.datetime object  or datetime.date object
		jd_tuple = gcal2jd(dateTime.year, dateTime.month, dateTime.day)
		julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
		return int(julian_day)






###-----------------------------TESTS-----------------------------###


# print("\n\n\nTesting GoogleSearchQuery:\n")
#
# x = GoogleSearchQuery()
# print(x.toString())
# x.setInUrl("lol")
# print(x.toString())
# x.setFuzzyTopicsList(['Beatles','liverpool'])
# print(x.toString())
# x.setNecessaryTopicsList(['Lennon','Strawberry'])
# print(x.toString())
#
#
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
# # x.changeDaterangeFrom(datetime.date(2010,3,15), printing=True)
# # print(x.toString())
# # x.changeDaterangeTo(datetime.date(2010,3,17), printing=True)
# # print(x.toString())
# x.setSiteList([])
# print(x.toString())
# x.setSiteList(['helloworld.com', 'thisistheend.co.in'])
# print(x.toString())





