
try: 
	import sqliteDefaults
except Exception:
	print("\n\n\n\tERROR while importing sqliteDefaults.py: . The module may have syntax errors or may be missing entirely.")



class SearchDBHandler:

	conn = None
	dbFilePath = None
	dbTableName = None

	def setDatabase(self, dbFilePath="GoogleSearchResults.db", dbTableName="SearchResultUrls", printing=True):
		self._SQLiteDBSetup(dbFilePath=dbFilePath, dbTableName=dbTableName, printing=printing)
		if self.conn != None:
			self.dbFilePath = dbFilePath
			self.dbTableName = dbTableName
			return True
		return False



	def _SQLiteDBSetup(self, dbFilePath, dbTableName, printing):
		conn = None
		if self.hasImportedNecessaryModulesSQLite():
			try:
				conn=sqliteDefaults.get_conn(dbFilePath, printing)
			except Exception:
				if printing:
					print("\n\tERROR in GoogleSearch._SQLiteDBSetup(): could not connect to database.")
				return None

			try:
				conn.execute('''CREATE TABLE IF NOT EXISTS `%s`(
					resultNumberInSearch 	INTEGER,
					Topic 					TEXT 	NOT NULL,
					URL 					TEXT 	NOT NULL,
					ResultPageNumber 		INTEGER NOT NULL,
					ResultNumberOnPage		INTEGER NOT NULL,
					StartDate 				INTEGER,
					EndDate 				INTEGER,
					SearchedOnDate 			DATE,
					ObtainedFromQuery 		TEXT 	NOT NULL,
					PRIMARY KEY(Topic, URL)
				);
				'''%dbTableName)
				conn.commit()

			except Exception:
				if printing:
					print("\n\tERROR in GoogleSearch._SQLiteDBSetup(): could not create table in database.")
				return None
		self.conn = conn





		
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

		
