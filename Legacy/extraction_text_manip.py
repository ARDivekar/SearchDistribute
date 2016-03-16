# -*- coding: utf-8 -*-
import random
import re
import urllib2
import unicodedata
from bs4 import BeautifulSoup
import os
import datetime
from jdcal import gcal2jd


def select_everything(str):
	return re.findall("(\n.*)*?",str)


def strip_http_https_from_url(url):
	return (url.split("https://")[-1]).split("http://")[-1]

def strip_www_from_url(url):
	return (url.split("www.")[-1])



def to_julian_date_datetime(date_time):		## takes as input a datetime object
	jd_tuple = gcal2jd(date_time.year, date_time.month, date_time.day)
	julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
	return int(julian_day)


## Function takes date in string and format, format must be specified like this "%Y.%m.%d" or any other way in which you are passing the string
def to_julian_date_string(date_string, date_format):
	date_time = datetime.datetime.strptime(date_string, date_format)
	jd_tuple = gcal2jd(date_time.year, date_time.month, date_time.day)
	julian_day = jd_tuple[0] + jd_tuple[1] + 0.5
	return int(julian_day)


def get_month_char3(string_year):
	if(string_year == 'Dec'): return 12
	elif(string_year == 'Nov'): return 11
	elif(string_year == 'Oct'): return 10
	elif(string_year == 'Sep'): return 9
	elif(string_year == 'Aug'): return 8
	elif(string_year == 'Jul'): return 7
	elif(string_year == 'Jun'): return 6
	elif(string_year == 'May'): return 5
	elif(string_year == 'Apr'): return 4
	elif(string_year == 'Mar'): return 3
	elif(string_year == 'Feb'): return 2
	elif(string_year == 'Jan'): return 1

def get_month_allchar(string_year):
	if(string_year == 'December'): return 12
	elif(string_year == 'November'): return 11
	elif(string_year == 'October'): return 10
	elif(string_year == 'September'): return 9
	elif(string_year == 'August'): return 8
	elif(string_year == 'July'): return 7
	elif(string_year == 'June'): return 6
	elif(string_year == 'May'): return 5
	elif(string_year == 'April'): return 4
	elif(string_year == 'March'): return 3
	elif(string_year == 'February'): return 2
	elif(string_year == 'January'): return 1



# import nltk #helps with article_supersplit()

def Linux_change_IP(net_interface="wlan0",random_ip=True):	##Note this only changes the private IPs.
##To change the public IPs, use a VPN.
	if random_ip:
		os.system('sudo ifconfig %s down'%net_interface)
		os.system('sudo ifconfig %s 192.168.%s.%s'%(net_interface, random.randrange(1, 255), random.randrange(1, 255)))
		os.system('sudo ifconfig %s up'%net_interface)

def Linux_change_all_IPs():
	Linux_change_IP("eth0")
	Linux_change_IP("wlan0")
	Linux_change_IP("wlan1")
	Linux_change_IP("wlan2")
	Linux_change_IP("vibr0")
	Linux_change_IP("vibr0-nic")


def write_to_file(text, filepath, make_if_not_exists=True, encoding='utf-8'):
	text=text.encode(encoding)
	if make_if_not_exists:
		with open(filepath, 'w+') as some_file:
			some_file.write(text)
	else: 
		with open(filepath) as some_file:
			some_file.write(text)



def make_google_search_query(necessary_topic_list=None, topic_list=None, site_list=None, daterange_from=None, daterange_to=None):
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
	
	return query		
	# '"Infosys" site:financialexpress.com/article/ | site:business-standard.com/article | site:livemint.com/companies | site:timesofindia.indiatimes.com/business/india-business/ '



def make_folder_path(folderpath):
	if folderpath[-1]!= "\\" and folderpath[-1]!= "/":
		folderpath+="/"
	return folderpath


def make_file_path(folderpath, filename, extension):
	if folderpath[-1]!= "\\" and folderpath[-1]!= "/":
		folderpath+="/"

	return folderpath+filename[:255-len(folderpath)-len(extension)]+extension # Windows only allows filepaths upto 260 characters. I'm using 255 to be on the safe side.\

def make_filename(input_line):
	line=re.sub("\:"," -",input_line)
	line=re.sub("\?","",line)
	# line=re.sub("\\\\","-",line)
	line=re.sub("/","-",line)
	line=re.sub('"',"'",line)
	line=re.sub("\|",";",line)
	line=re.sub("<","&lt;",line)
	line=re.sub(">","&gt;",line)
	line=re.sub("\\n","",line)
	return line
	

'''
def to_julian_date(year, month, day): 
	try:
		if(year==int(year)): 
			Y=int(year)
		if(month==int(month)): 
			M=int(month)
		if(day==int(day)): 
			D=int(day)
	except Exception:
		print "Invalid date input."
		return None
	if M<1 or M>12:
		print "Invalid date input."
		return None
	if D<1 or ((M==1 and D>31) or (M==2 and D>29) or (M==3 and D>31) or (M==4and D>30) or (M==5 and D>31) or (M==6 and D>31) or (M==7 and D>31) or (M==8 and D>31) or (M==9 and D>30) or (M==10 and D>31) or (M==11 and D>30) or (M==12 and D>31)):
		print "Invalid date input."
		return None

	C = 2 - (Y/100) + (Y/400)
	E = 365.25*(Y+4716)
	F = 30.6001*(M+1)
	julian_date= int(round(C+D+E+F-1524.5))
	return julian_date
'''


def date_split(input_date): 
	#date must be in YY-MM-DD format
	date=input_date.split('-')
	try:
		Y=int(date[0])
		M=int(date[1])
		D=int(date[2])
	except Exception:
		print "Invalid date input."
		return None
	if M<1 or M>12:
		print "Invalid date input."
		return None
	if D<1 or ((M==1 and D>31) or (M==2 and D>29) or (M==3 and D>31) or (M==4and D>30) or (M==5 and D>31) or (M==6 and D>31) or (M==7 and D>31) or (M==8 and D>31) or (M==9 and D>30) or (M==10 and D>31) or (M==11 and D>30) or (M==12 and D>31)):
		print "Invalid date input."
		return None
	return (Y,M,D)




def num_to_words(num):
	if num>=pow(10,12):
		return str(float(num)/pow(10,12))+" trillion"
	elif num>=pow(10,6):
		return str(float(num)/pow(10,9))+" million"
	elif num>=pow(10,3):
		return str(float(num)/pow(10,3))+" thousand"





def try_dict_index(dictionary, index):
	try: 
		return dictionary[index]
	except Exception: 
		print "ERROR on accessing index '%s': No such dictionary index"%(index)
		return None



def remove_empty_from_list(pylist):
	length=len(pylist)
	if length==0:
		return None
	removed=0
	i=0
	while i < length-removed:
		# print "i=%s, pylist[i]=%s, len(pylist)=%s, removed=%s"%(i,pylist[i],len(pylist),removed)
		if pylist[i]==None or pylist[i]=="" or pylist[i]==[] or pylist[i]=={} or pylist[i]==():
			del pylist[i]
			removed+=1
			i-=1
		i+=1

	
	return pylist
			 	#not necessary...reference pylist is a reference to an object. 
				#Since pylist is a mutable object, changes are saved 
				#but I kept doing list=remove_empty_from_list(list)
				


def remove_empty_from_dict(pydict):
	new_dict={}
	for i in pydict:
		if pydict[i]!=None and pydict[i]!="" and pydict[i]!=[] and pydict[i]!={} and pydict[i]!=():
			new_dict[i]=pydict[i]
	return new_dict



def extract_website(url):
	website=""
	if "http://" in url or "https://" in url:
		website= url.split('/')[2]
	else: website= url.split('/')[0] 

	if "www." in website:
		website = website.split("www.")[1]
	return website


def extract_links(article):
	article_soup=BeautifulSoup(article)
	link_dict={}
	for link_tag in article_soup.find_all('a'):
		link_dict[link_tag.contents[0].strip()]=link_tag.get('href')
		# this makes a dict of the form {'article_heading':'article_hyperlink'}
	return link_dict
	
	

def properly_encode(article, input_encoding="UTF-8"):
	
	article=article.decode(input_encoding)
	article = article.replace(u"\u2022", "*")
	article = article.replace(u"\u2019", "")
	# article = article.replace(u"\u2022", "*")
	# print article.encode('utf-8')
	article=unicodedata.normalize('NFKD', article).encode('ascii','ignore')
	
	# article = article.encode('unicode_escape')
	# article=article.encode('ascii')
	# print article
	return article

def shorten_whitespace(str): 	
	# removes streches of whitespace 
								# appearing before, after and inside a string, 
								# replacing it with two newline characters.
	str=str.strip()
	return re.sub("([ ]*(\\n)+[ ]*)+","\\n\\n",str)

def remove_HTML_tags(str): #removes html tags completely from a string, not their contents
	str=re.sub("<br>","\n", str)
	return re.sub("<(.*?|\n)*?>","", str)
	

def remove_HTML(str, tag, attributes=""): #removed everything inside all occurences of that html tag
	regex='''(<%s[ ]*%s.*?>)(\\n*.*?)*?(</%s>)'''%(tag,attributes,tag)
	# print regex
	return re.sub(regex,"",str)

def remove_HTML_except(str, tag): #removed everything inside all html tags, except a particular HTML tag
	return re.sub('''(<%s.*?>)(\\n.*?)*?(</%s>)'''%(tag,tag),"",str)


def remove_php_from_HTML(str): #removes php code completely from a string
	return re.sub("<?php.*?>","", str)



def get_charset(page_url): #gets encoding of the 
	response=None
	if 'http://'  in page_url.lower():
		response =urllib2.urlopen(page_url)
	elif 'https://' in page_url.lower():
		response=urllib2.urlopen('https://'+page_url.split("https://")[-1])
	else:
		response =urllib2.urlopen('http://'+page_url)
	charset = response.headers.getparam('charset')
	return charset


def get_html(page_url):
	#get_html: because typing a few lines of code is way too hard
	response=None
	if 'http://'  in page_url.lower():
		response =urllib2.urlopen(page_url)
	elif 'https://' in page_url.lower():
		response=urllib2.urlopen('https://'+page_url.split("https://")[-1])
	else:
		response =urllib2.urlopen('http://'+page_url)
	
	html = response.read()
	return html





def bytes_to_other(bytes):
	KB=pow(2,10)
	# print KB
	if bytes < KB:
		return str(bytes)+" Bytes"
	MB = pow(2,20)
	# print MB
	if bytes>KB and bytes<MB:
		return str(bytes/KB)+" KB"
	GB = pow(2,30)
	# print GB
	if bytes>MB and bytes<GB:
		return str(bytes/MB)+" MB"
	if bytes>GB: 
		return str(bytes/GB)+" GB"



def get_file(url, filepath="", block_sz=8192, confirm=False): 
	#does not work on html files
	
	file_name = url.split('/')[-1] #get the last thing seperated by a '/'
	u = urllib2.urlopen(url)
	
	if filepath[-1] !="/" and filepath[-1] != "\\":   
		filepath+="/"
	else:
		filepath[-1] ="/"

	fileout_path=filepath+file_name

	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	if (confirm):
		print "File size is %s , do you want to continue?"%bytes_to_other(file_size)
		y_or_n= raw_input("\nEnter y or n\n\t>")
		if y_or_n.lower() != 'y':
			exit(0)

	print "Downloading: %s\nBytes: %s" % (file_name, file_size)
	print "Writing to: %s"%fileout_path

	f = open(fileout_path, 'wb')
	file_size_dl = 0
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()
	return fileout_path


def properly_format(article):
	
	i=0
	article=article.strip()
	# print article, "\n\n\n\n\n\n\n\n\n\n\n"
	length = len(article)
	output_article = ""#+"\t"
	while i<length:
		if article[i]==";" and article[i+1]=='\n':
			i+=1
			continue
		elif article[i]=='\n':
			if output_article[len(output_article)-1]=='\n':
				i+=1
				continue
			else: output_article+='\n'

		elif article[i]=='\t': #this does not seem to be working
			if output_article[-1]=='\t':
				i+=1; 
				continue
			# elif output_article[-1]=='\n':
				# output_article+='\t'
				# output_article=output_article


		elif article[i]==" ":
			if output_article[len(output_article)-1]=='\n' or output_article[len(output_article)-1]=='\t':
				i+=1
				continue
			else: output_article+=article[i]
		else: output_article+=article[i]

		i+=1
	output_article= re.sub("&amp;","&",output_article)
	output_article= re.sub("&gt;",">",output_article)
	return output_article



def article_supersplit(article):
	article=properly_format(article)
	'''	
	This function splits a "properly_format"ed article, 
	and returns the variable 'text'.

	'text' is structured as:
		a list of paragraphs,
			where each paragraph is a list of sentences,
				where each sentence is a list of words, punctuations as seperate words.
	'''
	text=article.split("\n") #get paragraphs
	text = remove_empty_from_list(text)
	for i in range(0,len(text)):
		text[i]=text[i].split(". ") #get sentences
		text[i]=remove_empty_from_list(text[i])
		for j in range(0,len(text[i])):
			try:
				# print "\ntrying NLTK"
				text[i][j]=nltk.word_tokenize(text[i][j])
				# print "\nNLTK success"
			except Exception:
				# print "\n\nNLTK failed. Going for backup..."
				text[i][j]=text[i][j].split(" ") #get words
				text[i][j]+="."
				for k in range(0,len(text[i][j])):
					text[i][j][k]=re.sub(",", "", text[i][j][k])
					text[i][j][k]=re.sub(";", "", text[i][j][k])
					text[i][j][k]=re.sub("\(", "", text[i][j][k])
					text[i][j][k]=re.sub("\)", "", text[i][j][k])
					text[i][j][k]=re.sub("\[", "", text[i][j][k])
					text[i][j][k]=re.sub("\]", "", text[i][j][k])
					text[i][j][k]=re.sub("\{", "", text[i][j][k])
					text[i][j][k]=re.sub("\}", "", text[i][j][k])

				if text[i][-1][-2][-1] == ".":
					# print text[i][-1]
					text[i][-1][-2]=re.sub(".*", text[i][-1][-2][:-1], text[i][-1][-2])
				# print "\nreplaced: %s\n\n\n"%text[i][-1]
			finally:
				text[i][j]=remove_empty_from_list(text[i][j])

	return text
	
