import os
import sys
from GoogleSearch import GoogleSearch
from GoogleSearchQuery import GoogleSearchQuery
import datetime

def print_cli_help_message():
	x = os.system("clear; clear;")
	print("\n<<<<<-------------------------COMMAND-LINE INTERFACE TO THIS MODULE------------------------->>>>>")
	
	args_note="""
	ARGUMENTS LIST:
		The syntax used is similar to that of Linux for allowing the api user to 
		set the topic, time_period, num_time_periods_remaining, results_per_time_period, 
		wait_between_pages, wait_between_searches, etc.

			Binary arguments:

			-d = database file path
			-d_t = table name in database
			-g = google domain [make sure its's http:// and not https://]
			-t_f = fuzzy topic
			-t_n = necessary topic
			-s = site
			-i = single keyword in url
			-p = length of time_period (in days)
			-n = number of time periods
			-r = results per time period
			-m = max number of results per page
			-w_p = wait time between pages
			-w_s = wait time between searches
			-f = 'resume_from' date (in julian)


			Unary arguments:

			--printing  = set printing to True.
			--no_printing = set printing to False.

			--insert_pages = insert pages into the database as soon as they are extracted.
			--no_insert_pages | --dont_insert_pages = do not insert pages into the database as soon as they are extracted.

			--insert_searches = insert into the database as soon as we get all the results for a particular search.
			--no_insert_searches | --dont_insert_searches = do not insert into the database as soon as we get all the results for a particular search.

			--insert_on_error = insert into database if there is an error.
			--no_insert_on_error | --dont_insert_on_error = do not insert into database if there is an error.

			--skip_invalid_searches = if a search results in an error, keep going regardless.
			--no_skip_invalid_searches | --dont_skip_invalid_searches = stop and return if any search generates an error.



		EXAMPLE:
			
			username@server$ python cli.py -d "GoogleSearchResults.db" -d_t "NetworkingCompaniesResearch" -g www.google.com -t_n Cisco -t_f "systems admin" -t_n "job profile" -p 60 -n 2 -r 20 -w_p 180 -w_s 900
	
	"""


	tp_note= """Increasing -p and decreasing -n to get more results:

        Possible problems you may encounter:
            > Your query is rather obscure, and is only returning 8 results out of 
            the 70 you had requested per time_period.  
            > Your query is returning a lot of results, but they are mostly repeats.
            > your query does not return any new results for the latest time_period.
        

        Solution #1: [steps]
            [1] double your time period (-p)
            and
            [2] halve the number of time periods (-n).
            (or any proportion which maintains the product of -n and -p)


        Explanation:

            'time_period' and 'num_time_periods_remaining' (-p and -n respectively) ideally 
            should not be changed after you have started extracting for a particular Topic. 
            Concretely, their product should remain unchanged. 

            e.g. suppose you've used: 
                $ python article_url_extract.py -t "Cisco" -p 30 -n 48 -r 20
            i.e.
                topic = Cisco
                time_period = 30
                num_time_periods_remaining = 48
                results_per_time_period = 70 

            Initially, this is well and good, and you should not have to run anything else 
            (you may need to change your IP occasionally if you find that Google is blocking it). 


            Make the following change to your command line arguments:
                -p 60 -n 24
            i.e. 
                time_period = 60 
                num_time_periods_remaining = 24

            This will cause you to get more results per time_period, and the results will usually 
            be ones you have not seen before.

            However, this trick only works if the product 
                (time_period * num_time_periods_remaining) 
            i.e. 
                (-p * -n) 
            stays the same across runs, as changing the product will change the total time over 
            which you are collecting results.
	"""

	resume_note = """How to use -f (resume function):

        Possible problems you may encounter:
            > your query returns zero new results for the latest time_period, and then the
              program is terminated before the next run. 
            > you think a particular time_period's urls were not captured correctly and you'd 
              like to make another pass over the period.


        Solution #1: [steps]
            [1] use -f (resume_from) functionality to skip over time periods in later runs.
            
            Optionally:
            [1] double your time period (-p) 
            and 
            [2] halve the number of time periods (-n).


        Explanation: 

            -f i.e. resume_from, is a command-line argument you can use to skip periods where 
            zero UNIQUE urls were obtained.


            e.g. suppose you've used: 
                    $ python article_url_extract.py -t "Cisco" -p 30 -n 48 -r 20
                i.e.
                    topic = Cisco
                    time_period = 30
                    num_time_periods_remaining = 48
                    results_per_time_period = 70 
            
            Suppose this query has already been running for some time, and the latest time_period 
            was 250103-250133 (you should be able to find this in the search query printed to the 
            command line). 
            Suppose that for some reason, this returns zero UNIQUE results, e.g. all 70 out of 70 
            results were repeats. 
            If the program exits at this point (which may happen because of some error or because
            you terminated it with Ctrl+C), it will resume from the period 250103-250133 again, 
            which we know will return no unique resuls.

            To save time, we can skip over this period by setting resume_from = 250103
            i.e. 
                $ python article_url_extract.py -t "Cisco" -p 30 -n 48 -r 20 -f 250103
            Now, we will continue getting results from the next period.

            You may also want to change the time period and number of time periods appropriately 
            (See note: "Increasing -p and decreasing -n to get more results").

        IMPORTANT: once you find a time period in which you DO get some UNIQUE urls, you should not 
                   use resume_from in subsequent runs.									
	"""

	lotsa_results_note = """
	Getting LOTS of results in a friendly manner:

        This project was made to get lots of Google Search results in an automated manner. However, 
        the purpose was never to spam or cheat Google Search, and the Google TOS explicitly outlaws 
        screen scraping.
        There's no clear way to get around the fact that scraping violates Google's TOS. However, 
        if you do it in a respectful way, that is not spamming, you should not have any problem
        collecting lots of data really quickly. 
        If you do not heed this warning and spam anyway, you will probably get your IP blocked by 
        Google, either temporarily for a few hours or (in case you don't back off) for a few days. 

        Note: getting "blocked by Google" means your IP gets blocked when you try to run the script. 
        In most cases, you can still use Google normally via your browser (unless you've REALLLY 
        abused the service).

        
        There are certain things you can do to reliably get LOTS of results with this application:

        [1] Set the wait time to reasonalbe limits:
            Personally, I've found a wait period of 180 seconds between pages (-w_p 180) and 900 
            seconds between searches (-w_s 900) NEVER gets my IP blocked, but this might be too slow 
            for you.
            If you have lots of IP addresses at your disposal, you can make the wait time small and 
            switch them quickly (switching IPs automatically is not performed by this module).



        [2] Randomly select the wait time:
            The application does this automatically. 

            Concretely, googlesearch.py uses the function do_some_waiting(), which sets 
                wait_time = random.uniform(0.3*wait, 1.5*wait), 
            i.e. between 1/3rd and 1.5 times the input wait time. 
            This averages to something like 0.9 times the wait time. 

            Once you factor in the time for writing to database, connecting to the browser, etc, your 
            total wait time can between calculated as:

            Total wait time = (number of pages * wait per page) + (number of period * wait per search query)
                [where number of periods = number of queries].

            Which is what you'd expect it to be.



        [3] The -m argument:
            Like most Linux command-line arguments, -m is badly named. It stands for "max number of results
            per page". 
            As you know, a normal Google Search result returns 10 results per page. However, you can change
            this by adding "&num=<some number>" to the end of a search result. This is essentially what -m 
            does. 
            Specifying -m is a great way to get a LOT of results. Like, a huuuuuge number of results. 
            For example suppose your query is kind of obscure and has 1542 results. You realize that ALL of
            the results are important to you. You could either wait for 155 pages of results to load, or
            you could set "-m 100" and get the same in 16 page results.

            The max value of -m is 100. 

            However, setting -m to 100 is a quick way to get your IP noticed, since only developers and 
            hackers do it. 
            If you have a few IP addresses to space, I would recommend it (while keeping the wait times
            to a reasonalbe limit or more).



        [4] Use Virtual machines:
            I personally found virtual machines a big help. 
            
            Concretely, I used VirtualBox on which I initially created a single virtual machine, based on 
            Lubuntu 15.10 (Lubuntu is Ubuntu but with a very light GUI) and about 600 MB of RAM. My host 
            system was running Ubuntu 15.04.
            
            I set up the required Python modules (splinter+phantomjs or twill v0.9, jdcal and 
            BeautifulSoup), and VPNOneClick. 
            
            I then installed guest additions to VirtualBox [this was very annoying, took me almost a full 
            day to get right], so that I could enable shared folders. I placed the entire code for 
            googlesearch inside that single shared folder. 
            
            Then, I turned on VPNOneClick, connected to a new IP, and ran the code. The results started 
            getting saved in a database file inside the shared directory. 
            
            Once I was sure that my Virtual machine was extracting Google Search results, I cloned the 
            Virtual machine (I created linked clones, which meant that all the software is the same, and
            only the changes were saved separately; this meant incredible savings in disk space as compared 
            to full clones). Each linked clone was about 5 MB, whereas the base Virtual machine was ~4 GB.
            All in all, I made 8 linked clones, which consumed 4.8 GB of RAM when they ran together.

            Each linked clone had access to the same shared directory and the same database file where all
            the results were stored, but I opened VPNOneClick on each VM and connected to a different IP.
            Then, I ran the same code files (in the shared folder) on each and every VM. I used two terminal
            windows per VM, all running queries on different topics (I could have run them on the same 
            topic and used "-f" to start at particular locations, but I this would be difficult to keep
            track of).
            The result was that I was running 16 processes in parallel, on 8 different IP addresses, which was
            an 8-fold increase over what I had with no VMs. And none of my IPs got blocked by Google, because
            I was extracting respectfully, i.e. using arguments "-w_p 180 -w_s 900".

            This is the great thing about parallelism; if you plan it correctly, the performance increase
            is spectacular. 




        [5] ***Use different IP addresses****:
            Any website you visit has access to your IP address; that's just how the IP 
            networking protocol works. Google is no different; every query you send is 
            tagged with your IP address, and if you start sending too many queries too fast,
            Google will know what's up and start blocking your IP.
            
            However, there's literally millions of IP addresses available. To tap into these, 
            you need a VPN (Virtual Private Network), which lets you set up a connection to a 
            PROXY SERVER. 

            A proxy server is a server that obtains content-filled IP packets ON YOUR BEHALF,
            and then forwards them to you. Thus, a proxy server acts as a middleman who ensures
            that any website you visit does not have your real IP address, Google included.

            Before:
                (You) <====> (Google)                        | You get blocked if you query too much/too fast.
            Now:
                (You) <====> (proxy server) <====> (Google)  | The proxy server gets blocked instead of you.


            A proxy server is usually remotely located, in odd places like Turkey, Russia, India, 
            USA, UK etc. 

            A problem with proxy servers is that each proxy server has only one IP, just like you
            do at home. So, if you manage to get that IP blocked by Google, you're back to square
            one.

            The solution to this problem is simple: just use lots of proxy servers! This is done 
            most easily via a VPN, which is a software you run on your browser or your computer 
            that has the configuration settings to connect to several proxy servers. 

            VPNs are often paid services, but relatively cheap (like $5-10 a month). Here's a few
            articles about the best VPN services you can use:
            
                > https://www.bestvpn.com/blog/18736/5-best-free-vpn-2/
                > http://www.pcmag.com/article2/0,2817,2390381,00.asp
                > https://www.bestvpn.com/blog/32729/5-best-vpns-for-windows-november-2015/
            
            Most of the above were free with a data cap, or free for a certain time. 
            
            As a poor, broke and lazy college student, I didn't really feel like using any of these 
            if it meant changing my setup, so I used VPNOneClick, which is (as of Jan 2016) free on both
            Windows and Linux FOREVER with no data cap [the downside is that you do need to install 
            an application from their site (www.vpnoneclick.com). This application is pretty annoying 
            because it keeps crashing every once in a while and you have to manually restart it. 
            But hey, free is free].


            IMPORTANT: This application (GoogleSearch), uses your browser to get Google search results. 
            If you have multiple browsers, you should preferably go for a VPN service that provides its 
            own desktop application, since it's not guaranteed that this application will use a 
            particular browser.
            [If you really want, you can hack a few lines in the file BrowserHandler.py, to force it to 
            use a particular user agent (check for your browser at http://whatsmyuseragent.com/)].


            Now, once you've set up your VPN and connected to a new IP, you're good to go. You can check 
            your new IP by manually Googling "what's my ip". 

	"""

	results_per_page_note = """How to use -m (max number of results per page):
        As you know, a normal Google Search result returns 10 results per page. However, you can change
        this by adding "&num=<some number>" to the end of a search result. This is essentially what -m 
        does. 
        Specifying -m is a great way to get a LOT of results.  
        For example suppose your query is kind of obscure and has 1542 results. You realize that ALL of
        the results are important to you. You could either wait for 155 pages of results to load, or
        you could set "-m 100" and get the same in 16 page results.

        The max value of -m is 100. 

        However, setting -m to 100 is a quick way to get your IP noticed, since only developers and 
        hackers do it. 
	"""

	notes_dict = {5: lotsa_results_note, 4:results_per_page_note, 3: resume_note, 2: tp_note, 1:args_note}
	valid_options = sorted(notes_dict.keys()) +[0]

	help_topics_choice = -1
	while help_topics_choice!=0:
		print("\nWhich topic would you like help with? (Enter 0 to exit)")
		print("1. How to use the command line arguments.")
		print("2. Handling time periods lengths & number of time periods.")
		print("3. How to use -f (resume function).")
		print("4. How to increase the number of results per page obtained.")
		print("5. ***Tips to get lots of search results very fast.")
		
		pythonVersionNumber = sys.version_info.major 	##tells us if it is Python 2 or 3.
		try:
			if pythonVersionNumber==2:
				help_topics_choice=int(raw_input(">"))
			elif pythonVersionNumber==3:
				help_topics_choice=int(input(">"))

			if help_topics_choice not in valid_options:
				print("Invalid option entered.")
			elif help_topics_choice == 0:
				exit()	
			else:
				print("\n\n\n     %s\n\n\n\n"%(notes_dict[help_topics_choice]))


		except Exception:
			print("Invalid option entered.")


	# for note_index in notes_dict:
	# 	print("    %s) %s\n\n\n\n"%(note_index, notes_dict[note_index]))



###--------------------Default values--------------------##


db_file_path="GoogleSearchResults.db"
db_table_name="SearchResultUrls"
google_domain="http://www.google.com"
fuzzy_topics_list = []
necessary_topics_list = []
site_list = []
inurl=""
time_period=None
num_time_periods_remaining=1
results_per_page=10
resume_from=None
results_per_time_period=30
wait_between_pages=150
wait_between_searches=180
printing=True
insert_between_pages = True
insert_between_searches = False
insert_on_error = True
skip_invalid_searches = False



##---- We can set these parameters from the command line ----##

from sys import argv
# print argv



if "--help" in argv:
	print_cli_help_message()
	exit()


elif len(argv)==1:
	print("\n\tERROR: no topic entered.")
	yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
	if yorn.lower() =='y':
		print_cli_help_message()
	exit()

else:
	try:
		i = 1   
		while i < len(argv):
			## Start from 1 because we skip the first element of argv which is the script name.
			## We skip every second element because adjacent elements will be a pair.

			if argv[i] == "--printing":
				printing = True
				i += 1
			elif argv[i] == "--no_printing":
				printing = False
				i += 1
			elif argv[i] == "--insert_pages":
				insert_between_pages = True
				i += 1
			elif argv[i] == "--no_insert_pages" or argv[i] == "--dont_insert_pages":
				insert_between_pages = False
				i += 1
			elif argv[i] == "--insert_searches":
				insert_between_searches = True
				i += 1
			elif argv[i] == "--no_insert_searches" or argv[i] == "--dont_insert_searches":
				insert_between_searches = False
				i += 1
			elif argv[i] == "--insert_on_error":
				insert_on_error = True
				i += 1
			elif argv[i] == "--no_insert_on_error" or argv[i] == "--dont_insert_on_error":
				insert_on_error = False
				i += 1
			elif argv[i] == "--skip_invalid_searches":
				skip_invalid_searches = True
				i += 1
			elif argv[i] == "--no_skip_invalid_searches" or argv[i] == "--dont_skip_invalid_searches":
				skip_invalid_searches = False
				i += 1
			elif argv[i]=='-g':
				google_domain = argv[i+1]
				if 'http' not in google_domain:
					google_domain = "http://"+google_domain		##https does not work
				i += 2
			elif argv[i]=='-t_f':
				fuzzy_topics_list.append(argv[i+1])
				i += 2
			elif argv[i]=='-t_n':
				necessary_topics_list.append(argv[i+1])
				i += 2
			elif argv[i]=='-s':
				site_list.append(argv[i+1])
				i += 2
			elif argv[i]=='-i':
				inurl = argv[i+1]
				i += 2
			elif argv[i]=='-p':
				time_period = int(argv[i+1])
				i += 2
			elif argv[i]=='-n':
				num_time_periods_remaining = int(argv[i+1])
				i += 2
			elif argv[i]=='-r':
				results_per_time_period = int(argv[i+1])
				i += 2
			elif argv[i]=='-m':
				results_per_page = int(argv[i+1])
				i += 2
			elif argv[i]=='-w_p':
				wait_between_pages = int(argv[i+1])
				i += 2
			elif argv[i]=='-w_s':
				wait_between_searches = int(argv[i+1])
				i += 2
			elif argv[i]=='-f':
				if argv[i+1].lower() == 'now':
					gsq = GoogleSearchQuery()
					resume_from = gsq._convertToValidJulianDate(datetime.now().date())
				else:
					resume_from = int(argv[i+1])
				i += 2
			elif argv[i]=='-d':
				db_file_path = argv[i+1]
				i += 2
			elif argv[i]=='-d_t':
				db_table_name = argv[i+1]
				i += 2
			else : 
				print("\n\n\tERROR: INVALID ARGUMENT OR ARGUMENT PAIR ENTERED.\n")
				yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
				if yorn.lower() =='y':
					print_cli_help_message()
				exit()
	except Exception:
		print("\n\n\tERROR: INVALID ARGUMENT OR ARGUMENT PAIR ENTERED.\n")
		yorn = raw_input("\t\tWould you like a tutorial on how to use the command line? (Y/n)\n\t\t>")
		if yorn.lower() =='y':
			print_cli_help_message()
		exit()

	


if fuzzy_topics_list==[] and necessary_topics_list==[]:
	print("\n\tERROR: no topics entered.")
	yorn = raw_input("\t\tWould you like a tutorial on how to use the command line interface of this module? (Y/n)\n\t\t>")
	if yorn.lower() =='y':
		print_cli_help_message()
	exit()


if insert_between_searches==False and insert_between_pages==False:
	print("\n\tERROR: you must be inserting into the database either between pages or between searches.")
	exit()



g = GoogleSearch()
if g.canRun()==False:
    exit()

else:

    def formatted_printing(var_name, var_value, max_var_width=50, underscore_printing_factor=100, before_spacing_factor=5):
    	before_spacing_string=" "*before_spacing_factor
    	underscore_string="_"*underscore_printing_factor
    	var_string=str(var_value)
    	width_spacing = " "*(max_var_width-len(var_name))
    	final_string = before_spacing_string + var_name + ':' + width_spacing + var_string + "\n" + before_spacing_string + underscore_string 
    	print(final_string)

    print("\n\n\n\n")

    underscore_printing_factor = 90
    max_var_width = 35
    before_spacing_factor=5		## must be >= 2

    print("="*(before_spacing_factor-2)+"> ARGUMENT VALUES:")
    print(" "*before_spacing_factor + "_"*underscore_printing_factor)

    formatted_printing("db_file_path", db_file_path, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("db_table_name", db_table_name, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("google_domain", google_domain, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("fuzzy_topics_list", fuzzy_topics_list, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("necessary_topics_list", necessary_topics_list, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("site_list", site_list, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("time_period", time_period, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("num_time_periods_remaining", num_time_periods_remaining, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("results_per_time_period", results_per_time_period, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("results_per_page", results_per_page, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("resume_from", resume_from, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("wait_between_pages", wait_between_pages, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("wait_between_searches", wait_between_searches, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("printing", printing, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("insert_between_pages", insert_between_pages, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("insert_between_searches", insert_between_searches, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("insert_on_error", insert_on_error, max_var_width, underscore_printing_factor, before_spacing_factor)
    formatted_printing("skip_invalid_searches", skip_invalid_searches, max_var_width, underscore_printing_factor, before_spacing_factor)

    print("\n\n\n\n")





    allResults = g.saveToSQLiteDatabase(
    	dbFilePath = db_file_path,
    	dbTableName = db_table_name,
    	googleDomain = google_domain,
    	fuzzyTopicsList = fuzzy_topics_list,
    	necessaryTopicsList = necessary_topics_list,
    	siteList = site_list,
    	inurl = inurl,
    	timePeriod = time_period,
    	numTimePeriodsRemaining = num_time_periods_remaining,
    	resultsPerTimePeriod = results_per_time_period,
    	resultsPerPage = results_per_page,
    	resumeFrom = resume_from,
    	waitBetweenPages = wait_between_pages,
    	waitBetweenSearches = wait_between_searches,
    	printing = printing,
    	insertBetweenPages = insert_between_pages,
    	insertBetweenSearches = insert_between_searches,
    	insertOnError = insert_on_error,
    	skipErroneousSearches = skip_invalid_searches
        # printingDebug=True
    )
