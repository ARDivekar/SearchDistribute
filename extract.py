# -*- coding: utf-8 -*-
import re
import time
from bs4 import BeautifulSoup
import article_manip
import os
import random
import db_setup
import datetime
import extraction_text_manip

try:
	import google_manip
except Exception:
	1+1

import googlesearch

conn = db_setup.get_conn_sqlite()
	


def build_giant_profile(topic, root_filepath, site_list=None, number_of_months=12, articles_per_month=20, end_date=None, start_date=None, func_type=1):	
	#eg: start_date=2456074, end_date=2456554

	days_per_month=30;

	## If the start and end dates are not specified, we fall back on number_of_months, and vice verca
	if end_date==None:
		now=datetime.datetime.now()
		end_date=extraction_text_manip.to_julian_date_datetime(now)	
		## ^THIS JUILIAN DATE DOES NOT WORK, PLEASE REPLACE!!
	if start_date==None:
		start_date=end_date-number_of_months*days_per_month ##assume for simplicity that each month has 'days_per_month' days
	

	article_urls_list=[]	## A list of ALL the article urls we have extracted in this run. This is useful because sometimes Google searches give the same results, even when the 'daterange' parameter is specified in the Google Search query.
	articleObjs=[]			## A list of ALL objects of class ArticleObjs, with a one-to-one correpsondance to all the URLs in article_urls_list.
	

	## root_filepath is the folder in which we want all our data to be stored. Inside this folder, we will automatically make a new folder with the name of the search query. Inside THAT folder, we will store our articles (in one folder for each time period/month).

	## e.g. query="Infosys", root_filepath="./test_examples/", we will make folder "./test_examples/Infosys/", and start saving articles inside folders inside that.

	root_filepath=extraction_text_manip.make_folder_path(root_filepath)
	base_filepath = extraction_text_manip.make_folder_path(root_filepath+topic)
	if not os.path.exists(base_filepath):	## If the folder does not exist, make it
		os.makedirs(base_filepath)
	total_repeat_count=0
	total_url_count=0


	

	for i in range(0,number_of_months):
		## With each month, we go to a new folder

		if (end_date - i*days_per_month) <= start_date:		## Do not go back beyond the start date
			print "DONE"
			exit(0)

		## Now, we must make the folder names. For simplicity, the folder names are the dateranges (in Julian date) that we use to query the data. 
		## e.g. we might have one folder "./test_example/Infosys/2457215-2457245/", in which we save our 20 article_headline.txt files (the article file names are the article headlines)

		daterange_from=int(max(start_date,end_date-(i+1)*30)) ## to make SURE it does not go beyond the start date
		daterange_to=int(end_date-i*30)
		directory_name = "%s-%s"%(daterange_from,daterange_to)
		folderpath = base_filepath+directory_name
		print "\n>>> Current directory: %s"%folderpath
		if not os.path.exists(folderpath):
			os.makedirs(folderpath)

		## The following is just to throw off Google.
		some_text=None
		if len(articleObjs)>0:
			some_text=articleObjs[random.randrange(0,len(articleObjs))].article_text



		query = extraction_text_manip.make_google_search_query(topic_list=[topic], site_list=site_list, daterange_from=daterange_from, daterange_to=daterange_to)	
		print '>>> Google search Query: \n%s'%query
		print ">>> Getting search results..."


		## Get actual google results (as a list of results)

		if func_type==1:		## <-uses googlesearch.py
			print "\n\n\n\n\n\t\tUSING GOOGLESEARCH.PY"
			result_urls = googlesearch.google_search_results_list(
						query=query, num_results=articles_per_month)
			counter=1

			print ">>> Number of results found: %s"%len(result_urls)
			if len(result_urls)>0:
				print ">>> Results : \n"+ str(result_urls)
			else: 
				print "It seems your IP is getting blocked by Google. Wait some time (at least half an hour) before trying again, or switch to a different internet connection or use a VPN."
				exit(0)
			print "\n\n"
			url_count=1
			repeat_count=1
			


		elif func_type==2:		## <-uses google_manip.py
			print "\n\n\n\n\n\t\tUSING GOOGLE_MANIP.PY"
			results= google_manip.google_search_results(search_query=query, number_of_results=articles_per_month, random_text=some_text)	
		
			counter=1

			result_urls=[]
			print ">>> Number of results found: %s"%len(results)
			if len(results)>0:
				result_urls=[res.url for res in results]
				print ">>> Results : \n"+ str(result_urls)
			else: 
				print "It seems your IP is getting blocked by Google. Wait some time (at least half an hour) before trying again, or switch to a different internet connection."
				exit(0)
			print "\n\n"
			

			url_count=1
			repeat_count=1


		for i in range(0,len(result_urls)):
			result_urls[i]=re.findall('(.*?)(?=&amp)', result_urls[i])[0]


		for res_url in result_urls:
			existing_files = [ f for f in os.listdir(folderpath) if os.path.isfile(folderpath+"/"+f) ]
			## Look in the filesystem to see if that file already exists.

			for existing_file_name in existing_files:
				with open(folderpath+"/"+existing_file_name) as existing_file:
					existing_url=re.findall('(?<=__URL__:).*?(?=\\n)', existing_file.read(), re.I)
					existing_url=existing_url[0]
					article_urls_list.append(existing_url)

			article_urls_list=list(set(article_urls_list))

			if res_url not in article_urls_list:	## if we have not seen this url, we must extract it and write it to file.
				print "\n\n%s. %s"%(url_count,res_url)
				# time.sleep(1)
				htmlObj= article_manip.HTML_page_Obj(res_url)	## Extract the article HTML

				if htmlObj.url!= None:							
					art=article_manip.ArticleObject(HTML_page_Obj=htmlObj, conn=conn)	## Actually extract the article from the HTMLObj object. This will require us to run the extraction code we have saved in the database.


					## Write the article to file (we are already in the appropriate folder)
					print ">>> Writing article to file..."	
					if art.write_to_file(folderpath):	
						print ">>> Write to file status: SUCCESS!"
						articleObjs.append(art)			## Append the article object to the list of article objects we already have. This is done so that we can pickle it for later, if we need it.
					else: print ">>> Write to file status: unsuccessful."

				article_urls_list.append(res_url)	## Append the article url to the list of all urls, to prevent future repeats.
				url_count+=1
				total_url_count+=1
			else: 
				repeat_count+=1			## How many urls we have repeated for this query
				total_repeat_count+=1	## How many urls we have repeated for all the queries

		if func_type==2:
			if len(articleObjs)!=0:
				for x in range(0,random.randrange(1,3)):
					some_text=""
					while some_text == "" or some_text is None:
						some_text=articleObjs[random.randrange(0,len(articleObjs))].article_text
					google_manip.google_search_redirect(some_text)
	print "\n\n>>> Number of urls found: %s"%len(article_urls_list)
	print ">>> Total number of repeat urls: %s out of %s"%(total_repeat_count, total_repeat_count+total_url_count)
	print ">>> Number of articles obtained in this session: %s"%len(articleObjs)







# exec(webextcode[text_manip.extract_website(url)])

# print "\n\nDATELINE:\t"+article_date_and_time
# print "\n\nHEADLINE:\t"+article_headline
# for article_alt_headline in article_alt_headline_list:
# 	print "\n\nALT HEADLINE:\t"+article_alt_headline
# print "\n\n"+article_text

# print "\n\n\n\n\tTotal time taken: "+str(s.stop())+" seconds."





