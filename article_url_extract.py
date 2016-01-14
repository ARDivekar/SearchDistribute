import googlesearch
import sqliteDefaults
import extraction_text_manip
from datetime import datetime
import re
import os
import traceback
import signal

def ctrl_c_signal_handler(signal_number, frame):
    print "\n\n"
    option=""
    while option!=1 and option!=2 and option!=3:	## While it is not an integer
		option=raw_input("Program is paused. Enter an option:\n1.Exit\n2.Continue\n>")
		try:
 	 		option=int(option)
 	 	except Exception:
 	 		print "\n\tERROR: Please enter an integer value.\n"
 	 		if type(option)!=type("str"):
 	 			exit()

 	 	if type(option)==type(0):	## if 'option' is an integer
	  		if option==1:	## Exit
	  			exit()
	  		# if option==2:	## paused
	  		# 	yorn=""
	  		# 	while yorn !='n' and yorn !='N' and yorn!='y' and yorn!='Y':
	 	 	# 		yorn=raw_input("\nResume execution? (Y/n):\n>")
	  		# 		if yorn=='y' or yorn=='Y':
	  		# 			break
	  		# 		if yorn=='n' or yorn=='N':
	  		# 			exit()
	  		if option==2:	## Continue
	  			break
	  		
signal.signal(signal.SIGINT, ctrl_c_signal_handler)		## assign ctrl_c_signal_handler to Ctrl+C, i.e. SIGINT



conn=sqliteDefaults.get_conn("extracted_search_urls.db")
conn.execute('''Create table if not exists ArticleUrls(
		ArticleTopic 		TEXT,
		StartDate 			INTEGER,
		EndDate 			INTEGER,
		ResultPageNumber 	INTEGER,
		URL 				TEXT,
		ResultNumber		INTEGER,
		PRIMARY KEY(URL)
	);
	''')
conn.commit()


##--------------------PARAMETERS-------------------##

topic = "HCL"


site_list=[	'financialexpress.com/article/', 
			'business-standard.com/article/', 
			'livemint.com/companies', 
			'timesofindia.indiatimes.com/business/india-business/', 
			'articles.economictimes.indiatimes.com/', 'economictimes.indiatimes.com/markets/stocks/news/',
			'thehindubusinessline.com/markets/stock-markets/', 'thehindubusinessline.com/companies/']


initial_start_date = extraction_text_manip.to_julian_date_datetime(datetime.now().date())



time_period = 30					## time period = 30, is 30 days i.e. roughly 1 month. 
num_time_periods_remaining = 60		## we search over = time_period*num_time_periods_remaining
articles_per_time_period = 40

## IMPORTANT NOTE: 
## 'time_period' and 'num_time_periods_remaining' should not be changed after you have started extracting for a particular ArticleTopic. 
## Specifically, their product should not be changed. 

## 	e.g. suppose time_period = 30, num_time_periods_remaining=48, and articles_per_time_period=20. 
## 		Now, you have found that you are only getting 8 out of 20 articles per time_period. By making time_period=60 and num_time_periods_remaining=24, you can get more articles per time period, which is less 'suspicious' to Google. But the product of time_period and num_time_periods_remaining should stay the same, or else the total time over which you are collecting URLs will not be the same.


resume_from = -1		## maintains the number of time periods, but allows you to skip periods where zero UNIQUE urls were extracted. resume_from should be set to the start date of the latest period in which no urls were extracted. E.g. last period = 250103-250133 <<<< [ if no urls extracted: stop process, change time period and number of time periods appropriately, pass: "____ -r 250103" in command line ]
						## NOTE: once you find a time period in which you DO get some UNIQUE urls, you should not use resume_from in subsequent runs.
						## resume_from is also useful if you think a particular period's urls were not captured correctly and you'd like to make another pass over the period.




waiting=True
wait_between_pages=150
wait_between_searches=900


sound_command="rhythmbox piano_beep.mp3 &"		## Will be different for Windows and Linux. 
												## e.g.: for Windows, "start piano_beep.mp3 &" works as intended.




		##---- We can set these parameters from the command line ----##

from sys import argv
# print argv


## I've used a syntax similar to that of Linux for allowing the api user to set the topic, time_period, num_time_periods_remaining, articles_per_time_period, wait_between_pages and wait_between_searches.
## -t = topic
## -p = length of time_period (in days)
## -n = number of time periods
## -a = articles per time period
## -w_p = wait time between pages
## -w_s = wait time between searches

## Example of command line: 
## user@blahblah:/blah/blah/user$ python google_extract.py -t "ajanta pharma" -p 180 -n 6 -a 80



if len(argv)%2==1 and len(argv)>2:	## if we have an odd number of arguments >2, it means we might have these arguments.
	for i in range(1,len(argv), 2):   
		## Start from 1 because we skip the first element of argv which is the script name.
		## We skip every second element because adjacent elements will be a pair.
		if argv[i]=='-t':
			topic = argv[i+1]
		elif argv[i]=='-p':
			time_period = int(argv[i+1])
		elif argv[i]=='-n':
			num_time_periods_remaining = int(argv[i+1])
		elif argv[i]=='-a':
			articles_per_time_period = int(argv[i+1])
		elif argv[i]=='-w_p':
			wait_between_pages = int(argv[i+1])
		elif argv[i]=='-w_s':
			wait_between_searches = int(argv[i+1])
		elif argv[i]=='-r':
			resume_from = int(argv[i+1])
		else : 
			print "\n\n\tINVALID ARGUMENT PAIR ENTERED, EXITING...\n"
			exit()

elif len(argv)!=1:
	print "\n\n\tINVALID NUMBER OF ARGUMENTS ENTERED, EXITING...\n"
	exit()


print "topic = %s"%(topic)
print "time_period = %s"%(time_period)
print "num_time_periods_remaining = %s"%(num_time_periods_remaining)
print "articles_per_time_period = %s"%(articles_per_time_period)
print "wait_between_pages = %s"%(wait_between_pages)
print "wait_between_searches = %s"%(wait_between_searches)
print "\n\n"







##-----------------------CODE----------------------##

start_date=0
end_date=0

article_sorted_by_date_query = "Select StartDate, EndDate from ArticleUrls WHERE ArticleTopic='%s' ORDER BY StartDate ASC"%(topic)




ArticleUrls_sorted_by_date = sqliteDefaults.verified_select_sqlite(conn, article_sorted_by_date_query, printing=False)

if len(ArticleUrls_sorted_by_date) == 0:
	end_date = initial_start_date
	print "\n\tNo article urls in database on the topic %s\n"%(topic)
else: 	
	last_extracted_date = ArticleUrls_sorted_by_date[0][0]	## Gets the StartDate of the last extracted article URL
	end_date = last_extracted_date	## We must resume googlesearching from this date

	if resume_from != -1:
		end_date = resume_from		## resume_from should be set to the start date of the latest period in which no urls were extracted. NOTE: once you find a time period in which you DO get some UNIQUE urls, you should not use resume_from in subsequent runs.


	num_time_periods_passed = int(round((initial_start_date - end_date)/time_period))	## WHATEVER YOU DO, THE PRODUCT OF time_period*
	num_time_periods_remaining = num_time_periods_remaining - num_time_periods_passed

	if num_time_periods_remaining==0:
		print "\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic)
		exit()
	else:
		print "\tResuming from date=%s, will get further %s time_period of articles."%(end_date, num_time_periods_remaining)





start_date = end_date - time_period

results_link_dict=None

## We now start getting more search results.

for i in range(0,num_time_periods_remaining):	##  This is the reason you should not change 'num_time_periods_remaining'
	article_query = extraction_text_manip.make_google_search_query(
											topic_list=[topic], 
											site_list=site_list,
											daterange_from=start_date, 
											daterange_to=end_date)	

	results_link_dict=None
	print "\n\n\nRUNNING QUERY:\n\t%s\n"%(article_query)

	try:
		results_link_dict = googlesearch.get_google_search_results(
							query = article_query, 
							num_results = articles_per_time_period, 
							google_domain = "http://www.google.co.in",
							waiting=waiting, wait=wait_between_pages)
	except Exception, e:
		print "\n\n\n\tAN ERROR OCCURED WHILE EXTRACTING URLS:\n"
		print e
		os.system(sound_command)		## Plays a paino beep when the module exits
		print "\n\n"
		traceback.print_exc()

		try:
			print "\n\n\n\tTrying to insert results obtained so far into...\n"

			repeat_count=0
			result_number=1		## gives priority of results. ResultNumber = 1 means the top result
			for page_num in results_link_dict:
				for res_url in results_link_dict[page_num]: 
						## Insert the url into the database.
						try :
							sqliteDefaults.insert_table_sqlite(conn, 
								'ArticleUrls', 
								('URL',	 	'ArticleTopic',	'StartDate',	'EndDate', 	'ResultPageNumber', 'ResultNumber'), 
								[(res_url,	 topic, 		start_date, 	end_date, 	page_num, result_number)]
							)
							result_number=result_number+1
						except Exception:
							print "\t\tCould not insert topic-url pair ( %s  ,  %s ), possible duplicate"%(topic, res_url)
							repeat_count=repeat_count+1
			print "\n\n\tNumber of URLs repeated in this search = %s"%(repeat_count)
			print "\tNumber of URLs extracted in this search = %s"%(result_number-1)

		except Exception:
			print "\n\t\tERROR: Cannot insert results extracted so far into database.\n"

		exit()


	if results_link_dict != None:
		## Print the search results for this time period.
		googlesearch.print_result_link_dict(results_link_dict=results_link_dict, query=article_query)


		## Insert the search results for this time period into the database.
		print "\n\n\n\tInserting results into database:\n"

		repeat_count=0
		result_number=1		## gives priority of results. ResultNumber = 1 means the top result
		for page_num in results_link_dict:
			for res_url in results_link_dict[page_num]: 

					## Insert the url into the database.
					try :
						sqliteDefaults.insert_table_sqlite(conn, 
							'ArticleUrls', 
							('URL',	 	'ArticleTopic',	'StartDate',	'EndDate', 	'ResultPageNumber', 'ResultNumber'), 
							[(res_url,	 topic, 		start_date, 	end_date, 	page_num, result_number)]
						)
						result_number=result_number+1
					except Exception:
						print "\t\tCould not insert topic-url pair ( %s  ,  %s ), possible duplicate"%(topic, res_url)
						repeat_count=repeat_count+1

		print "\n\n\tNumber of URLs repeated in this search = %s"%(repeat_count)
		print "\tNumber of URLs extracted in this search = %s"%(result_number-1)

	else: 
		# print "\nERROR: No results obtained for query \n\t%s\n"%article_query
		print "\n\n...please try again later, possibly with a different IP.\n"
		os.system(sound_command)		## Plays a paino beep when the module exits
		exit()

	end_date = start_date
	start_date = start_date - time_period

	print "\n\tREMAINING: %s time_period of articles."%(num_time_periods_remaining-i-1)
	if (num_time_periods_remaining-i-1) == 0:
		print "\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic)
		os.system(sound_command)		## Plays a paino beep when the module exits
		exit()


	print "\n\n\n\n\tWAITING BEFORE NEXT SEARCH QUERY IS FIRED..."
	googlesearch.do_some_waiting(wait=wait_between_searches)


	

os.system(sound_command)		## Plays a paino beep when the module exits