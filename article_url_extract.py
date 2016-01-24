import re
import os
import traceback
import signal
from datetime import datetime



can_compile=True
try:
	import sqliteDefaults
except Exception:
	print "\n\tERROR: module sqliteDefaults not found, please add to project to continue.\n\tsqliteDefaults may be found at https://github.com/ARDivekar/googlesearch_article_url/blob/master/sqliteDefaults.py"
	can_compile=False

try: 
	import googlesearch
except Exception:
	print "\n\tERROR: module googlesearch not found, please add to project to continue.\n\tsqliteDefaults may be found at https://github.com/ARDivekar/googlesearch_article_url/blob/master/sqliteDefaults.py"
	can_compile=False


try: 
	import cli_help
except Exception:
	print "\n\tERROR: module cli_help not found, please add to project to continue.\n\tcli_help may be found at https://github.com/ARDivekar/googlesearch_article_url/blob/master/cli_help.py"
	can_compile=False

try:
	from jdcal import gcal2jd
except Exception:
	can_compile=False
	print "\n\tERROR: module jdcal not found, please install to Python [e.g. with the command 'pip install jdcal']."

if can_compile == False:
	exit()




##----------------------MISC FUNCTIONS-----------------------------##
def to_julian_date_datetime(date_time):		## takes as input a datetime object
	jd_tuple = gcal2jd(date_time.year, date_time.month, date_time.day)
	julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
	return int(julian_day)



def make_google_search_query(necessary_topic_list=None, topic_list=None, site_list=None, daterange_from=None, daterange_to=None, inurl=None):
	if necessary_topic_list==None and topic_list==None: 
		return None 

	query=""
	if necessary_topic_list!=None:
		for topic in necessary_topic_list:
			query+='"%s" '%topic

	if topic_list!=None:
		for topic in topic_list:
			query+='%s '%topic
	
	if site_list!=None and site_list!=[]:
		query += " site:"+site_list[0]
		for i in range(1,len(site_list)):
			query+=" | site:"+site_list[i]
			
	if daterange_from!=None and daterange_to!=None and daterange_from<=daterange_to:
		query+=" daterange:%s-%s"%(daterange_from, daterange_to)

	if inurl != None and inurl!="":
		query+=" inurl:%s"%inurl
	
	return query	





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
	  		








##--------------------PARAMETERS-------------------##

google_domain = "http://www.google.co.in"


topic = ""

inurl=""

# site_list=[	'financialexpress.com/article/', 
# 			'business-standard.com/article/', 
# 			'livemint.com/companies', 
# 			'timesofindia.indiatimes.com/business/india-business/', 
# 			'articles.economictimes.indiatimes.com/', 'economictimes.indiatimes.com/markets/stocks/news/',
# 			'thehindubusinessline.com/markets/stock-markets/', 'thehindubusinessline.com/companies/']


site_list=[	
			'business-standard.com/article/', 
			
			
			'articles.economictimes.indiatimes.com/', 'economictimes.indiatimes.com/markets/stocks/news/',
			]





# site_list=[	'financialexpress.com/article/', 
			 
# 			'livemint.com/companies', 
# 			'timesofindia.indiatimes.com/business/india-business/', 
			
# 			'thehindubusinessline.com/markets/stock-markets/', 'thehindubusinessline.com/companies/']


initial_start_date = to_julian_date_datetime(datetime.now().date())



time_period = 30					## time period = 30, is 30 days i.e. roughly 1 month. 
num_time_periods_remaining = 60		## we search over = time_period*num_time_periods_remaining
results_per_time_period = 30
results_per_page = 10

## IMPORTANT NOTE: 
## 'time_period' and 'num_time_periods_remaining' should not be changed after you have started extracting for a particular Topic. 
## Specifically, their product should not be changed. 

## 	e.g. suppose time_period = 30, num_time_periods_remaining=48, and results_per_time_period=20. 
## 		Now, you have found that you are only getting 8 out of 20 results per time_period. By making time_period=60 and num_time_periods_remaining=24, you can get more results per time period, which is less 'suspicious' to Google. But the product of time_period and num_time_periods_remaining should stay the same, or else the total time over which you are collecting URLs will not be the same.


resume_from = -1		## maintains the number of time periods, but allows you to skip periods where zero UNIQUE urls were extracted. resume_from should be set to the start date of the latest period in which no urls were extracted. E.g. last period = 250103-250133 <<<< [ if no urls extracted: stop process, change time period and number of time periods appropriately, pass: "____ -f 250103" in command line ]
						## NOTE: once you find a time period in which you DO get some UNIQUE urls, you should not use resume_from in subsequent runs.
						## resume_from is also useful if you think a particular period's urls were not captured correctly and you'd like to make another pass over the period.




waiting=True
wait_between_pages=150
wait_between_searches=900


sound_command="rhythmbox piano_beep.mp3 &"		## Will be different for Windows and Linux. 
												## e.g.: for Windows, "start piano_beep.mp3 &" works as intended.


db_file_path = "extracted_search_urls.db"
db_table_name = "ArticleUrls"





		##---- We can set these parameters from the command line ----##

from sys import argv
# print argv


## I've used a syntax similar to that of Linux for allowing the api user to set the topic, time_period, num_time_periods_remaining, results_per_time_period, wait_between_pages and wait_between_searches.

## -d = database file path
## -d_t = table name in database
## -g = google domain
## -t = topic
## -i = single keyword in url
## -p = length of time_period (in days)
## -n = number of time periods
## -r = results per time period
## -m = max number of results per page (between 10 and 100)
## -w_p = wait time between pages
## -w_s = wait time between searches
## -f = 'resume_from' date (in julian)

## Example of command line: 
## user@blahblah:/blah/blah/user$ python google_extract.py -t "ajanta pharma" -p 180 -n 6 -a 80


if "--help" in argv:
	cli_help.print_cli_help_message()
	exit()


elif len(argv)==1:
	print "\n\tERROR: no topic entered."
	yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
	if yorn.lower() =='y':
		cli_help.print_cli_help_message()
	exit()


elif len(argv)%2==1 and len(argv)>2:	## if we have an odd number of arguments >2, it means we might have these arguments.
	for i in range(1,len(argv), 2):   
		## Start from 1 because we skip the first element of argv which is the script name.
		## We skip every second element because adjacent elements will be a pair.

		if argv[i]=='-g':
			google_domain = argv[i+1]
			if 'http' not in google_domain:
				google_domain = "http://"+google_domain		##https does not work
		elif argv[i]=='-t':
			topic = argv[i+1]
		elif argv[i]=='-i':
			inurl = argv[i+1]
		elif argv[i]=='-p':
			time_period = int(argv[i+1])
		elif argv[i]=='-n':
			num_time_periods_remaining = int(argv[i+1])
		elif argv[i]=='-r':
				results_per_time_period = int(argv[i+1])
		elif argv[i]=='-m':
			results_per_page = int(argv[i+1])
		elif argv[i]=='-w_p':
			wait_between_pages = int(argv[i+1])
		elif argv[i]=='-w_s':
			wait_between_searches = int(argv[i+1])
		elif argv[i]=='-f':
			if argv[i+1].lower() == 'now':
				resume_from = to_julian_date_datetime(datetime.now().date())
			else:
				resume_from = int(argv[i+1])
		elif argv[i]=='-d':
			db_file_path = argv[i+1]
		elif argv[i]=='-d_t':
			db_table_name = argv[i+1]
		else : 
			print "\n\n\tERROR: INVALID ARGUMENT PAIR ENTERED.\n"
			yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
			if yorn.lower() =='y':
				cli_help.print_cli_help_message()
			exit()

else:
	print "\n\n\tERROR: INVALID ARGUMENT PAIR ENTERED.\n"
	yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
	if yorn.lower() =='y':
		cli_help.print_cli_help_message()
	exit()


if topic=="":
	print "\n\tERROR: no topic entered."
	yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
	if yorn.lower() =='y':
		cli_help.print_cli_help_message()
	exit()


print "db_file_path = %s"%(db_file_path)
print "db_table_name = %s"%(db_table_name)
print "google_domain = %s"%(google_domain)
print "topic = %s"%(topic)
if inurl!="":
	print "inurl = %s"%inurl
print "time_period = %s"%(time_period)
print "num_time_periods_remaining = %s"%(num_time_periods_remaining)
print "results_per_time_period = %s"%(results_per_time_period)
print "results_per_page = %s"%(min(max(results_per_page,10), 100))
print "wait_between_pages = %s"%(wait_between_pages)
print "wait_between_searches = %s"%(wait_between_searches)
print "\n\n"


if results_per_page > 100:
	print "\n\t\tERROR: Cannot get %s results per page, getting the maximum allowed (i.e. 100)."%results_per_page
elif results_per_page < 10:
	print "\n\t\tERROR: Cannot get %s results per page, getting the minimum allowed (i.e. 10)."%results_per_pageresults_per_page
results_per_page = min(max(results_per_page,10), 100)	

print "\n\n\n\n"








##-------CODE FOR GETTING A RESULTS FOR DATE-STAGGERED QUERIES AS AN SQLITE DATABASE-------#



signal.signal(signal.SIGINT, ctrl_c_signal_handler)		## assign ctrl_c_signal_handler to Ctrl+C, i.e. SIGINT


conn=sqliteDefaults.get_conn(db_file_path)
conn.execute('''Create table if not exists %s(
		Topic 				TEXT,
		StartDate 			INTEGER,
		EndDate 			INTEGER,
		ResultPageNumber 	INTEGER,
		URL 				TEXT,
		ResultNumber		INTEGER,
		PRIMARY KEY(Topic, URL)
	);
	'''%db_table_name)
conn.commit()




start_date=0
end_date=0

results_sorted_by_date_query = "Select StartDate, EndDate from %s WHERE Topic='%s' ORDER BY StartDate ASC"%(db_table_name, topic)



Urls_sorted_by_date = sqliteDefaults.verified_select_sqlite(conn, results_sorted_by_date_query, printing=False)

if len(Urls_sorted_by_date) == 0:
	end_date = initial_start_date
	print "\n\tNo results in database on the topic %s\n"%(topic)
else: 	
	last_extracted_date = Urls_sorted_by_date[0][0]	## Gets the StartDate of the last extracted URL
	end_date = last_extracted_date	## We must resume googlesearching from this date

	if resume_from != -1:
		end_date = resume_from		## resume_from should be set to the start date of the latest period in which no urls were extracted. NOTE: once you find a time period in which you DO get some UNIQUE urls, you should not use resume_from in subsequent runs.


	num_time_periods_passed = int(round((initial_start_date - end_date)/time_period))	## WHATEVER YOU DO, THE PRODUCT OF time_period*
	num_time_periods_remaining = num_time_periods_remaining - num_time_periods_passed

	if num_time_periods_remaining==0:
		print "\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic)
		exit()
	else:
		print "\tResuming from date=%s, will get further %s time_period of results."%(end_date, num_time_periods_remaining)





start_date = end_date - time_period

results_link_dict=None

## We now start getting more search results.

for i in range(0,num_time_periods_remaining):	##  This is the reason you should not change 'num_time_periods_remaining'
	query = make_google_search_query(
						necessary_topic_list=[topic], 
						inurl=inurl,
						site_list=site_list,
						daterange_from=start_date, 
						daterange_to=end_date)	

	results_link_dict=None
	print "\n\n\nRUNNING QUERY:\n\t%s\n"%(query)

	try:
		results_link_dict = googlesearch.get_google_search_results(
							query = query, 
							num_results = results_per_time_period, 
							results_per_page = results_per_page,
							google_domain = google_domain,
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
			unique_result_number=1
			for page_num in results_link_dict:
				for res_url in results_link_dict[page_num]: 
						## Insert the url into the database.

						try :
							sqliteDefaults.insert_table_sqlite(conn, 
								db_table_name, 
								('URL',	 	'Topic',	'StartDate',	'EndDate', 	'ResultPageNumber', 'ResultNumber'), 
								[(res_url,	 topic, 		start_date, 	end_date, 	page_num, result_number)]
							)
							unique_result_number+=1
						except Exception:
							print "\t\tCould not insert topic-url pair ( %s  ,  %s ), possible duplicate"%(topic, res_url)
							repeat_count=repeat_count+1

						result_number=result_number+1	## We always increment te result number to show where it would be on the page, even in case of duplicates
			print "\n\n\tNumber of URLs repeated in this search = %s"%(repeat_count)
			print "\tNumber of URLs extracted in this search = %s"%(unique_result_number-1)

		except Exception:
			print "\n\t\tERROR: Cannot insert results extracted so far into database.\n"

		exit()


	if results_link_dict != None:
		## Print the search results for this time period.
		googlesearch.print_result_link_dict(results_link_dict=results_link_dict, query=query)


		## Insert the search results for this time period into the database.
		print "\n\n\n\tInserting results into database:\n"

		repeat_count=0
		result_number=1		## gives priority of results. ResultNumber = 1 means the top result
		unique_result_number=1
		for page_num in results_link_dict:
			for res_url in results_link_dict[page_num]: 

					## Insert the url into the database.
					try :
						sqliteDefaults.insert_table_sqlite(conn, 
							db_table_name, 
							('URL',	 	'Topic',	'StartDate',	'EndDate', 	'ResultPageNumber', 'ResultNumber'), 
							[(res_url,	 topic, 		start_date, 	end_date, 	page_num, result_number)]
						)
						unique_result_number+=1
					except Exception:
						print "\t\tCould not insert topic-url pair ( %s  ,  %s ), possible duplicate"%(topic, res_url)
						repeat_count=repeat_count+1

					result_number=result_number+1

		print "\n\n\tNumber of URLs repeated in this search = %s"%(repeat_count)
		print "\tNumber of URLs extracted in this search = %s"%(unique_result_number-1)

	else: 
		# print "\nERROR: No results obtained for query \n\t%s\n"%query
		print "\n\n...please try again later, possibly with a different IP.\n"
		os.system(sound_command)		## Plays a paino beep when the module exits
		exit()

	end_date = start_date
	start_date = start_date - time_period

	print "\n\tREMAINING: %s time_period of results."%(num_time_periods_remaining-i-1)
	if (num_time_periods_remaining-i-1) == 0:
		print "\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic)
		os.system(sound_command)		## Plays a paino beep when the module exits
		exit()


	print "\n\n\n\n\n\n\tWAITING BEFORE NEXT SEARCH QUERY IS FIRED..."
	googlesearch.do_some_waiting(wait=wait_between_searches)


	

os.system(sound_command)		## Plays a paino beep when the module exits