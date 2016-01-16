'''
DISCLAIMER: This code document is for personal use only. Any violation of the Google Terms of Service is not the responsibility of the authors of the document and is performed at your own risk. 
	...Just so you know, this sort of thing does violate the Google ToS. We (the authors) personally did not use it in production code, only as an experiment in twill commands. We hope that you do the same.
'''



import math
import time
import random
import re


can_compile=True
try:
	import twill
	import twill.commands
except Exception:
	print "\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch."
	can_compile = False

if twill.__version__ != "0.9":
	print "\n\tERROR: twill version 0.9 not found, please install to Python [e.g. with the command 'pip install -Iv http://darcs.idyll.org/~t/projects/twill-0.9.tar.gz'].\n\tPlease note that as of now, only version 0.9 of twill is supported by googlesearch."
	can_compile = False


try:
	from bs4 import BeautifulSoup
except Exception:
	print "\n\tERROR: module BeautifulSoup not found, please install to Python [e.g. with the command 'pip install beautifulsoup4']."
	can_compile = False

if can_compile == False:
	exit()




##-------------------------MISC FUNCTIONS------------------------##


def write_to_file(text, filepath, make_if_not_exists=True, encoding='utf-8'):
	text=text.encode(encoding)
	if make_if_not_exists:
		with open(filepath, 'w+') as some_file:
			some_file.write(text)
	else: 
		with open(filepath) as some_file:
			some_file.write(text)


##------------------------EXTACTION CODE FOR SINGLE QUERY------------------##




def twill_clear_browser_data():
	t_com=twill.commands
	t_com.reset_browser; 
	t_com.reset_output; 	
	t_com.clear_cookies



def extract_results_from_google_search_results_page(bs, printing_debug=False):	## bs is a BeautifulSoup object.

	## This function, given a BeautifulSoup object with the HTML of a Google Search results page, extracts the urls of the Search Results.
	if printing_debug:
		print "\n\nextract_results_from_google_search_results_page:"


	temp_results_urls=bs.findAll(attrs={"class":"r"}) 	## I have found that this extracts all 10 links per page

	if printing_debug:
		print "\n\ttemp_results_urls:"

	if temp_results_urls==[]:
		if printing_debug:
			print "[]"
		return None
	
	if printing_debug:
		for x in temp_results_urls:
			print "\n\t",x

	if printing_debug:
		print "\n\n\tresults_page_urls:"


	results_page_urls=[]	## all the search result urls from a relevant Google Search results page.
	for temp_url in temp_results_urls:
		# print type(temp_url) 		#<-is a BeautifulSoup object
		# print "\n\n\nCHICKEN",str(temp_url)	#<-yeah this is how i debug stuff.
		result_page_url=re.findall('(?<=/url\?q=)(.*?)(?=")', str(temp_url))
		if result_page_url!=[]:
			result_page_url=result_page_url[0]
			result_page_url=re.findall('(.*?)(?=&amp)', result_page_url)
			if result_page_url != []:
					result_page_url=result_page_url[0]
					results_page_urls.append(result_page_url)

	if results_page_urls==[]:
		if printing_debug:
			print "[]"
		return None

	if printing_debug:
		for x in results_page_urls:
			print "\n\t",x


	return results_page_urls








def extract_next_google_search_results_page_links(bs, google_domain, current_page=1, printing_debug=False):	## bs is a BeautifulSoup object.

	## This function, given a BeautifulSoup object with the HTML of a Google Search results page, will get all the 'next links' from a google search results page, i.e. if we are on page 1, at the bottom we will see, under the Google logo, page 1 2 3 4 5 6 7 8 9 10 Next. Page 1 out of these will be selected because we are currently on that page.
	## This function extracts the urls of all the 'next' pages: 2, 3, 4, 5, 6, 7 etc. (but not the 'Next' link, because that is the same as the link for page 2). 
	## Now we must visit other pages. For that, we extract the links at the bottom of the page.

	if printing_debug:
		print "\n\nextract_next_google_search_results_page_links:"

	nav_html=(bs.findAll(attrs={"id":"nav"}))[0]	## There should be only one.
	if printing_debug:
		print "\n\tnav_html:\n%s\n"%nav_html

	temp_next_pages=(BeautifulSoup(nav_html)).findAll(attrs={"class":"fl"})	## This extracts links for further result pages. The 'Next' link is not included in this.
	
	if printing_debug:
		print "\n\temp_next_pages:"

	if temp_next_pages==[]:		## No 'next' results on this page
		if printing_debug:
			print "[]"
		return None

	temp_next_pages=temp_next_pages[0:len(temp_next_pages)-1]	#The 'Next' link is also of class 'fl'

	for x in temp_next_pages:
		print x,"\n\n"


	next_results_urls=[]
	for temp_next_html in temp_next_pages:
		url=re.findall('(?<=href=")(.*?)(?=">)', str(temp_next_html))[0]
		
		bs_temp=BeautifulSoup(temp_next_html)
		search_result_page_number=int((bs_temp.find('a').contents[2]).strip())

		if search_result_page_number>current_page:		## We don't want to extract previous pages, because we assume they have already been covered.
			url=google_domain+url
			next_results_urls.append(url)

	if printing_debug:
		print "\n\next_results_urls:\n%s\n"%next_results_urls

	return next_results_urls
		
	## Side note: the current page we are on is in {"class":"csb"}








def extract_next_google_search_results_link(bs, google_domain, printing_debug=False):	## bs is a BeautifulSoup object.
	
	## This function, given a BeautifulSoup object with the HTML of a Google Search results page, will get a single link, of the next results page.
	## This function is an easier version of extract_next_google_search_results_page_links(), which allows us to just keep clicking 'Next' to get more results.
	
	if printing_debug:
		print "\n\nextract_next_google_search_results_link:"

	if printing_debug:
		print "\n\tnav_html:\n"

	nav_html=(bs.findAll(attrs={"id":"nav"}))
	if nav_html==[]:
		if printing_debug:
			print "[]"	
		return None

	nav_html=nav_html[0]	## There should be only one.
	if printing_debug:
		print "%s\n"%nav_html
	

	temp_next_pages=BeautifulSoup(str(nav_html)).findAll(attrs={"class":"fl"})	## This extracts links for further result pages. The 'Next' link is not included in this.

	if printing_debug:
		print "\n\temp_next_pages:"

	if temp_next_pages==[]:		## No 'next' results on this page
		if printing_debug:
			print "[]"	
		return None

	if printing_debug:
		for x in temp_next_pages:
			print "\n\t",x


	next_link_html=temp_next_pages[len(temp_next_pages)-1]	#The 'Next' link is also of class 'fl'
	
	
	next_result_page_url=re.findall('(?<=href=").*?(?=")', str(next_link_html))

	if printing_debug:
		print "\n\nnext_result_page_url:"
	
	if next_result_page_url==[]:
		if printing_debug:
			print "[]"
		return None
	next_result_page_url=next_result_page_url[0]
	next_result_page_url=google_domain+next_result_page_url	
	
	if printing_debug:
		print "\n\t",next_result_page_url

	next_result_page_url= re.sub("&amp;", "&", next_result_page_url)
	return next_result_page_url







def perform_initial_google_search(query, google_domain):	## This uses the twill library
	## Source for code: http://pymantra.pythonblogs.com/90_pymantra/archive/407_form_submit_using_twill.html
	## Note: code from above link has been tweaked slightly.

	## Side note: you can get your browser user agent at http://whatsmyuseragent.com/

	t_com = twill.commands
	t_brw = t_com.get_browser()			## get the default browser
	url = google_domain					## e.g. "http://www.google.com"
	t_brw.go(url)						## open the url 
	all_forms = t_brw.get_all_forms()	## returns list of all form objects (corresp. to HTML <form>) on that URL 
	 
	## now, you have to choose only that form, which has the POST or GET method
	 
	for each_frm in all_forms:
	    attr = each_frm.attrs			## all attributes of form
	    if each_frm.method == 'GET':	## The button to search is a GET button. Sometimes this may be POST
	        ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
	        for ct in ctrl:
	                if ct.type == 'text':     	## i did it as per my use, you can put your condition here
							ct._value = query 	## The Google query we want to fire.
							t_brw.clicked(each_frm, ct.attrs['name'])	## clicked() takes two parameter: a form object and button name to be clicked.
							t_brw.submit()		## Clicks the submit button on that form

	return t_brw.get_html()



def do_some_waiting(wait, printing=True):
	wait_time=random.uniform(0.3*wait, 1.5*wait)
	if printing:
		print "\n\n\t\tWAITING %s seconds between searches.\n"%(wait_time)
	time.sleep(wait_time)





def total_number_of_results(bs, printing_debug=False):
	resultStats_html=bs.findAll(attrs={"id":"resultStats"})	## There should be only one.
	
	if printing_debug:
		print "resultStats_html=%s"%resultStats_html

	if resultStats_html==[]:
		return None
	resultStats_html=str(resultStats_html[0])
	resultStats_html=re.sub(",","", resultStats_html)
	total_num_results=re.findall('(?<=bout )\d+(?= results)', resultStats_html)
	if total_num_results==[]:
		return None
	total_num_results=total_num_results[0]
	try:
		total_num_results=int(total_num_results)
	except Exception:
		if printing_debug:
			print "total_num_results = %s is not an integer"%total_num_results
		return None
	return total_num_results
	





def get_google_search_results(query, num_results=10, results_per_page=10, google_domain="http://www.google.com", func_type=1, waiting=True, wait=450, printing=True, printing_debug=False):
	## Returns a dictionary, results_link_dict which contains all the links in an organized manner.


	results_link_dict={}	## A dictionary of lists, containing Google Search results as URLs. 
	## results_link_dict[i] is a dictionary of results of the i'th page. 
	## results_link_dict[i][j] is the url of the j'th result on the i'th page. 

	## For most values of i (i.e. for most pages), there should be 10 results i.e. j=1...10. The last page may not have all the links, so the correct way to index this dict is:
	## for result_page in results_link_dict:
	##     for result_url in result_page:
	##         <code/>


	search_result_count=0;	## keeps track of the TOTAL number of search results. 
	## Normally, 'search_result_count' should be exactly 'num_results' after this function completes. 
	## However, if the query itself has only 'X' results, where 'X' < num_results (we requested 'num_results' results), then 'search_result_count' should be 'X' by the end of this function, i.e. we get all the possible results; we should also print a message warning the caller that it was not possible to get num_results.

	page_count=0;

	required_num_of_pages=int(math.ceil(num_results/10))


	first_results_page_html = perform_initial_google_search(query, google_domain)
	## We have now clicked the button on the www.google.com page. Now it is time to extract the links.


	bs = BeautifulSoup(first_results_page_html)
	if printing_debug:
		write_to_file(bs.prettify(), "./Googletest1.html")

	total_num_results = total_number_of_results(bs, printing_debug)
	if total_num_results!=None:
		print "\n\n\tThis query has about %s results in total. We will try to get the top %s results\n"%(total_num_results, num_results)

	first_page_result_urls = extract_results_from_google_search_results_page(bs, printing_debug)

	
	if first_page_result_urls== None:
		print("\n\n\tget_google_search_results(): your query,\n\t%s\n\t...returned no results."%(query))
		if printing_debug:
			write_to_file(bs.prettify(), "./Googletest2.html")
		return None


	## Now, we know we have returned SOME results:
	page_count=1;
	search_result_count = search_result_count+len(first_page_result_urls);
	results_link_dict[1] = first_page_result_urls


	if num_results <= search_result_count:	## We WANTED < 10 results, i.e. the first 'X' results, where X <= 10
		results_link_dict[1] = results_link_dict[1][0:num_results]
		return results_link_dict
	


	if func_type==1:		## use extract_next_google_search_results_link(), which gets a single next page
		while search_result_count < num_results:

			## We first see if the next page exists, then we do_some_waiting()
			next_page_url = extract_next_google_search_results_link(bs, google_domain, printing_debug)	## 'next_page_url' stores the url of the next page

			if printing_debug:
				print "\n\n\nnext_page_url=",next_page_url
			if next_page_url==None:
				print("\n\n\tget_google_search_results(): your query,\n\t%s\n\t..only had %s results, not %s as you requested."%(query, search_result_count, num_results))
				return results_link_dict


			if results_per_page != 10:
				results_per_page = min(max(results_per_page,10), 100)	## You cannot get more than 100 results per page.
				next_page_url+="&num=%s"%results_per_page


			## Wait period between searches
			if waiting:
					do_some_waiting(wait, printing=printing)
			else:	
				do_some_waiting(wait=20, printing=printing)

			if printing_debug:
				write_to_file(bs.prettify(), "./Googletest3.html")



			##Now, we must 'click' on the link, via the browser. Twill does this for us.
			t_brw = twill.commands.get_browser()	## get the default browser
			t_brw.go(next_page_url)					## open the url 
			results_page_html=t_brw.get_html()

			bs = BeautifulSoup(results_page_html)
			page_result_urls = extract_results_from_google_search_results_page(bs, printing_debug)
			if page_result_urls==None:
				print("\n\n\tget_google_search_results(): your query,\n\t%s\n\t..only had %s results, not %s as you requested."%(query, search_result_count, num_results))
				return results_link_dict
			

			page_count = page_count+1

			## if we have got as many as we need
			if search_result_count + len(page_result_urls) >= num_results:	
				results_link_dict[page_count] = page_result_urls[0:num_results-search_result_count]
				return results_link_dict

			## We have not got enough results, so keep getting:
			else:	
				search_result_count = search_result_count + len(page_result_urls);
				results_link_dict[page_count] = page_result_urls

			twill_clear_browser_data()




	elif func_type==2: #EXPERIMENTAL!	## use extract_next_google_search_results_page_links(), which gets multiple next pages
		
		first_page_next_page_urls = extract_next_google_search_results_page_links(bs, google_domain, printing_debug=printing_debug)	
		## 'first_page_next_page_urls' stores the urls of the next pages 2, 3, 4 etc. while we are currently on page 1.

		if first_page_next_page_urls==None:
			print("\n\n\tget_google_search_results(): your query,\n\t%s\n\t...returned only 1 page with %s results."%(query, search_result_count))
			return results_link_dict


		## Now, we know that we have >1 search result pages, so we get the next ones.

		next_page_urls=first_page_next_page_urls	## Initialization for use in loop

		## Inside this loop, we break & return if we have exhausted all the search results. We print the appropriate error message in that case.
		while search_result_count < num_results:	
			for next_page_url in next_page_urls:

				if waiting:
					do_some_waiting(wait, printing=printing)
				else:
					do_some_waiting(wait=20, printing=printing)

				twill_clear_browser_data()


				t_brw = twill.commands.get_browser()	## get the default browser
				t_brw.go(next_page_url)					## open the url 
				results_page_html=t_brw.get_html()

				bs = BeautifulSoup(results_page_html)
				page_result_urls = extract_results_from_google_search_results_page(bs, printing)
				
				page_count = page_count+1
				
				## if we have got as many as we need
				if search_result_count + len(page_result_urls) >= num_results:	
					results_link_dict[page_count] = page_result_urls[1:num_results-search_result_count]
					return results_link_dict

				## We have not got enough results, so keep getting:
				else:	
					search_result_count = search_result_count + len(page_result_urls);
					results_link_dict[page_count] = page_result_urls

				twill_clear_browser_data()


			## We have now exhausted our list of next_page_urls, but we have still not got enough results.
			## As a result, we must get more next_page_urls

			## The latest BeautifulSoup object, 'bs', contains the HTML of the last page from which we have extracted results. page_count holds the number of this page. 
			## If we pass this 'bs' object to extract_next_google_search_results_page_links(), then we can get the maximum number of next page urls. Of course, we'll have to tell the function what is the number of the page we are currently on, so that it does not extract the links of the previous (already extracted) pages.
			next_page_urls = extract_next_google_search_results_page_links(bs, google_domain, current_page=page_count, printing=printing)

			
	## dont forget to reset the browser and outputs.
	twill_clear_browser_data()

	return results_link_dict




def google_search_results_list(query, num_results=10, google_domain="http://www.google.com", func_type=1, waiting=True, wait=180, printing=False, printing_debug=False):
	## converts get_google_search_results(), but returns a list instead of a dict. 

	results_link_dict=get_google_search_results(query=query, num_results=num_results, google_domain=google_domain, func_type=func_type, waiting=waiting, wait=wait, printing=printing, printing_debug=printing_debug)
	results_link_list=[]
	if results_link_dict=={}:
		return None

	for page_no in results_link_dict:
		results_link_list=results_link_list+results_link_dict[page_no]

	return results_link_list



def print_result_link_dict(results_link_dict, query):
	print "\n\n\tResults for query \n\t\t'%s':\n"%(query)

	if results_link_dict != None:
		for page_num in results_link_dict:
			print("\n\tPAGE NUMBER : %s"%(page_num))
			for res_url in results_link_dict[page_num]:
				print("\t\t%s"%(res_url))
	else:
		print "\n\tThere are no results."



"""
## <----------------------------Example------------------------>

test_query='"Infosys"  site:financialexpress.com/article/ | site:business-standard.com/article/ | site:livemint.com/companies | site:timesofindia.indiatimes.com/business/india-business/ | site:articles.economictimes.indiatimes.com/ | site:economictimes.indiatimes.com/markets/stocks/news/ | site:thehindubusinessline.com/markets/stock-markets/ daterange:2455946-2455976'
link_dict= get_google_search_results(	query=test_query, 
										num_results=18, 
										printing=True, 
										waiting=False)
print_result_link_dict(link_dict, test_query)


'''
you might write the output (submitted page) to any file using:
content = t_brw.get_html()	<- to get the html
or 
t_brw.save_html(filepath)	<- to save the file directly
'''

"""



print("\n\n")

