import sqliteDefaults
import sys
import datetime
import traceback
import Enums
from SearchExtractorErrors import make_unimplemented_error
from SearchExtractorErrors import print_error


class SearchDBHandler:
	conn = None

	def __init__(self):
		pass

	def isConnected(self):
		if self.conn is None:
			return False
		return True

	def connectToMySQLDB(self):
		raise NotImplementedError(make_unimplemented_error(self.__class__.__name__, sys._getframe().f_code.co_name))


	def connectToSQLiteDB(self, dbFilePath="GoogleSearchResults.db", dbTableName="SearchResultURLs", printing=True):
		"""
		Args:
		    dbFilePath: the file path of the SQLite database file. If not a .db file, it is corrected.
		    	e.g. "xxx/xxx/xxx.db" stays the same, whereas "xxx/xxx/xxx" becomes the former, and "xxx/xxx/" (i.e. a directory) bedomes "xxx/xxx/GoogleSearchResults.db"
		    dbTableName: the SQLite table name to be referred to henceforth.
		    printing: if we should print to terminal or not.

		Returns: True or False, depending on whether we have successfully connected to SQLite and created a usable table, or not.
		"""

		## Correct common errors:
		if dbFilePath.endswith("/") or dbFilePath.endswith("\\"):
			dbFilePath+="GoogleSearchResults.db"
		if not dbFilePath.endswith(".db"):
			dbFilePath+=".db"

		try:
			self.conn=sqliteDefaults.get_conn(dbFilePath, printing)
		except Exception, e:
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "could not connect to SQLite database.", e)
			self.conn = None
			return False

		if not self.DBSetup(dbTableName=dbTableName, printing=printing):
			self.conn = None
			return False

		return True


	def DBSetup(self, dbTableName, printing):
		"""
		Ensures a table with the required name exists in the database.
		Args:
		    dbTableName: the table name to be used in the database.
		    printing: if we should print to terminal or not.

		Returns: True or False.
		"""


		## Assumes self.conn is not None, throws an Exception if it is.
		try:
			self.conn.execute('''CREATE TABLE IF NOT EXISTS `%s`(
				resultNumberInSearch 	INTEGER,
				SearchEngine			TEXT,
				Topic 					TEXT 	NOT NULL,
				URL 					TEXT 	NOT NULL,
				ResultPageNumber 		INTEGER NOT NULL,
				ResultNumberOnPage		INTEGER NOT NULL,
				StartDate 				INTEGER,
				EndDate 				INTEGER,
				SearchedOnDate 			DATE,
				ObtainedFromQuery 		TEXT 	NOT NULL,
				QueryPageURL			TEXT,
				PRIMARY KEY(SearchEngine, Topic, URL)
			);
			'''%dbTableName)
			self.conn.commit()
			return True

		except Exception, e:
			print_error(printing, self.__class__.__name__, sys._getframe().f_code.co_name, "could not create table '"+dbTableName+"' in database.", e)
			return False







	def insertResultsLinkDictIntoDB(self, resultsLinkDict, googleSearchQueryObj, printing, printingDebug):

		if self.conn!=None and type(self.dbTableName)==type(""):
			if printing:
				print("\n\t\t\tTrying to insert results obtained...")
			try:
				resultCount = 0		## gives priority of results. ResultNumber = 1 means the top result
				repeatCount = 0
				uniqueResultNumber=0

				if printingDebug:
					print("\n\n\nresultsLinkDict=\n%s\n\n"%resultsLinkDict)
					print("sorted(resultsLinkDict.keys()) = %s\n\n\n"%sorted(resultsLinkDict.keys()))

				for pageNum in sorted(resultsLinkDict.keys()):
					for resultNumberOnPage in range(1, len(resultsLinkDict[pageNum])+1):
						## Insert the url into the database.
						resUrl = resultsLinkDict[pageNum][resultNumberOnPage-1]	## We always increment the result number to show where it would be on the page, even in case of duplicates
						resultCount += 1
						try:
							topic = googleSearchQueryObj.getTopicStringForDB()
							startDate = googleSearchQueryObj.getDaterangeFrom()
							endDate = googleSearchQueryObj.getDaterangeTO()

							sqliteDefaults.insert_table_sqlite(self.conn, self.dbTableName,
															   ('resultNumberInSearch','URL', 'Topic','ResultPageNumber', 'ResultNumberOnPage','StartDate',	'EndDate', 	'SearchedOnDate', 				'ObtainedFromQuery'),
															   [(resultCount, 			resUrl,	topic,	pageNum, 			resultNumberOnPage,	 startDate, 	endDate, 	datetime.datetime.now().date(),	googleSearchQueryObj.toString() )
																],
															   printing_debug = printingDebug

															   )

							uniqueResultNumber += 1


						except Exception, e:
							errorString = str(e).lower()
							if errorString.find('syntax error')==-1:
								repeatCount += 1
							if printing:
								print("\n\t\t\t\tCould not insert topic-url pair ( %s  ,  %s )"%(topic, resUrl))
								print("\t\t\t\tError description: %s\n"%e)
							if printingDebug:
								traceback.print_stack()


				if printing:
					print("\n\t\t\t\tNumber of URLs repeated: (%s/%s)"%(repeatCount,resultCount))
					print("\t\t\t\tNumber of unique URLs inserted: (%s/%s)\n"%(uniqueResultNumber, resultCount))

			except Exception, e:
				if printing:
					print("\t\t\tERROR in GoogleSearch._insertResultsLinkDictIntoDB(): Cannot insert results extracted so far into database.\n")
					print("\n\t\t\tERROR description: %s"%e)
				if printingDebug:
					print("\n\t\t\tPrinting stack traceback:\n")
					traceback.print_stack()
					print("\n\n\n")

		else:
			if printing:
				print("\n\tERROR in GoogleSearch._insertResultsLinkDictIntoDB(): trying to insert into database, but conn or dbTableName passed is invalid.\n")

		
