import sqliteDefaults
import os
import extraction_text_manip

os.system("reset")

conn = sqliteDefaults.get_conn("article_extract_db.db")
conn.execute('''CREATE TABLE IF NOT EXISTS `articles_clean` (
	`company_or_sector`		TEXT,
	`article_url`			TEXT,
	PRIMARY KEY(company_or_sector, article_url)
	);
	''')
conn.commit()

company_name = 'Infosys'

articles = sqliteDefaults.verified_select_sqlite(conn,
													"SELECT DISTINCT article_url, company_name, article_headline, article_text, article_date \
														FROM articles \
														WHERE company_name='%s' \
															and article_url not in (select article_url from articles_clean)\
														ORDER BY article_url ASC\
															"%(company_name)
												)


conn2 = sqliteDefaults.get_conn("extracted_search_urls.db")
company_dict = {}
temp_table = sqliteDefaults.verified_select_sqlite(conn2,"SELECT DISTINCT ArticleTopic from articleUrls order by ArticleTopic asc")
for i in range(0,len(temp_table)):
	company_dict[i+1]=temp_table[i][0]


company_dict[100]="Financial Services sector"
company_dict[200]="IT sector"
company_dict[300]="Energy sector"
company_dict[400]="Consumer goods sector"
company_dict[500]="Automobiles sector"
company_dict[600]="Pharma sector"
company_dict[700]="Construction sector"
company_dict[800]="Cement products sector"
company_dict[900]="Metals sector"
company_dict[1000]="Telecom sector"
company_dict[1100]="Services sector"
company_dict[1200]="Media and Entertainment sector"
company_dict[1300]="Industrial Manufacturing sector"

# print company_dict

## Print list of comapnies and sectors:
print "\n\nList of companies: \n"
for j in company_dict:
	if j < 100:
		print "%s : %s"%(j, company_dict[j])
print "\n\nList of sectors: \n"
temp_list = list(sorted([j for j in company_dict]))
for j in temp_list:
	if j >= 100:
		print "%s : %s"%(j, company_dict[j])



print "\n\n\nNumber of articles left to go = %s\n"%len(articles)

x = raw_input("\n\n\nPress 'Enter' to start...")





i=0

while i < len(articles):
	os.system("reset")
	
	print "#--------------------------------------INSTRUCTIONS--------------------------------------#"
	print "\n\tENTER THE COMPANY NUMBER FOR THE BODY OF THE ARTICLE."
	print "\tIF THERE ARE MORE THAN ONE, ENTER THE NUMBERS SEPARETED BY SPACES, E.G.:"
	print "\t\t3 4 8"
	print "IF THE ARTICLE IS NOT ABOUT ANY OF THE COMPANIES LISTED, ENTER '0' (ZERO)."
	print "IF THE ARTICLE IS ____ONLY____ ABOUT THE TOPIC FOR WHICH IT IS LISTED, PRESS ENTER."
	print "YOU CAN GO BACK TO THE PREVIOUS ARTICLE WITH 'P', 'p', 'b' OR 'B'. \n\tNote: for every time you go back, you must re-mark the articles.\n"

	print "#----------------------------------END OF INSTRUCTIONS-----------------------------------#"


	print "\n\n\nArticle #%s of this session:\n\n"%(i+1)
	print "Topic:\t\t\t%s\n"%(articles[i][1])
	print "URL:\t\t\t%s\n\n"%(articles[i][0])
	print "Date:\t\t\t%s\n"%(articles[i][4])
	print "Headline:\t\t%s\n\n\n\n"%(articles[i][2])
	print "Body:\n\t\t%s\n"%(articles[i][3])


	## Print list of comapnies and sectors:
	print "\n\nList of companies: \n"
	for j in company_dict:
		if j < 100:
			print "%s : %s"%(j, company_dict[j])
	print "\n\nList of sectors: \n"
	temp_list = list(sorted([j for j in company_dict]))
	for j in temp_list:
		if j >= 100:
			print "%s : %s"%(j, company_dict[j])
	


	while True:
		select = raw_input("\n>")
		if not select:
			ensure_not_double_query = "SELECT * from articles_clean where article_url='%s'"%(articles[i][0])
			if len(sqliteDefaults.verified_select_sqlite(conn,ensure_not_double_query)) == 0:

				sqliteDefaults.insert_table_sqlite(conn, 
					'articles_clean',
					('company_or_sector', 'article_url'),
					[ (articles[i][1], articles[i][0]) ]
				)
				
				i+=1		## Go to next entry
			else:
				print "ERROR #1: pair already exists in table"
				y = raw_input()
				
			break;
	




		elif select.lower() == 'p' or select.lower() == 'b':
			i-=2		## Go to previous entry
			delete_query = "DELETE from articles_clean where article_url='%s'"%(articles[i+1][0])
			print delete_query
			conn.execute(delete_query)	
			conn.commit()
						## Delete listing for previous entry
			break;




		else:
			## Step 1: convert input string to a list of numbers

			nums_str= extraction_text_manip.remove_empty_from_list(select.split(' '))
			try: 
				input_companies_nums=list(set([int(x) for x in nums_str]))
			except Exception:
				print "\n\tERROR #2: please enter an integer."
				continue

			# print input_companies_nums

			if input_companies_nums == [0]:
				try:
					sqliteDefaults.insert_table_sqlite(conn, 
					'articles_clean',
					('company_or_sector', 'article_url'),
					[ ('None', articles[i][0]) ]
					)
					break;
				except Exception:
					print "\tERROR: Duplicate entry for pair: (%s , %s)"%("None", articles[i][0])
					y = raw_input()

			


			## Step 2: make a list of the companies / sectors, insert them into the database.

			try:
				input_companies_and_sectors = [company_dict[j] for j in input_companies_nums]
			except Exception:
				print "\n\tERROR #3: please enter an a number from the list above."
				continue

			# print input_companies_and_sectors

			for company_or_sector in input_companies_and_sectors:
				try:
					sqliteDefaults.insert_table_sqlite(conn, 
					'articles_clean',
					('company_or_sector', 'article_url'),
					[ (company_or_sector, articles[i][0]) ]
					)
				except Exception:
					print "\tDuplicate entry for pair: (%s , %s)"%(company, articles[i][0])
					y = raw_input()

			break;

	i+=1
