# Author: Abhishek Divekar, Jan 2016. Licence: Creative Commons.

import os
import sqlite3
import datetime

def get_conn(db_file_name, printing=True):
	#makes a new file if it does not exist

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))	#gets direcotry path in which file is stored. 
	db_path = os.path.join(BASE_DIR, db_file_name)

	with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as conn:	
					#souce for		"detect_types=sqlite3.PARSE_DECLTYPES"		is:
					#http://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion
		if printing:
			print("\n\t\tOpened connection successfully to database %s"%db_path)
		return conn
	return None


# def getConn(dbFilePath):
# 	with sqlite3.connect(dbFilePath, detect_types=sqlite3.PARSE_DECLTYPES) as conn:	
# 					#souce for		"detect_types=sqlite3.PARSE_DECLTYPES"		is:
# 					#http://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion
# 		print "\t\tOpened connection successfully"
# 		return conn
# 	return None

class Table:
	def __init__ (self, input_attributes, input_table):
		self.table=input_table
		self.attributes=input_attributes

	def __len__(self):
		return len(self.table)

	def __getitem__(self,i): 
		'''
			works for 2D or 3D or any-D yay!
			works because if a[i][j][k], a[i] returns a tuple, for the ith row. Let, row=a[i]. 
			Then, a[i][j][k] becomes row[j][k]. We start call the function again, to get the column entry.

		'''
		# print type(self)
		if type(i)==int:
			return self.table[i]
		elif type(i)==str:
			#assume that they are searching by column, i.e.
			#table['col_name']
			#this allows access by column and then row
			ind=self.attributes.index(i)
			col=[]
			for row_no in range(0, len(self.table)-1):
				col.append(self.table[row_no][ind])
			return tuple(col)

	


def build_where_clause(where_params_list, where_values_list):
	if where_params_list!=None and where_values_list!=None:
		where_clause=" WHERE "
		where_clause+=" %s='%s' "%(str(where_params_list[0]), str(where_values_list[0]))
		for i in range(1,len(where_values_list)):
			where_clause+=" AND %s='%s' "%(str(where_params_list[i]), str(where_values_list[i]))
	else : 
		where_clause=""
	return where_clause



def build_select_query(tablename, select_params_list, where_params_list=None, where_values_list=None):
	select_query="SELECT "
	select_query+=" %s"%select_params_list[0]
	for i in range(1,len(select_params_list)):
		select_query+=", %s"%select_params_list[i]
	select_query+=" FROM %s "%tablename
	select_query+=build_where_clause(where_params_list=where_params_list, where_values_list=where_values_list)
	select_query+=";"
	return select_query


def build_update_query(tablename, update_params_list, update_values_list, where_params_list=None, where_values_list=None):
	update_query="UPDATE "+tablename+" SET " 
	update_query+=" %s='%s' "%(str(update_params_list[0]), str(update_values_list[0]))
	for i in range(1,len(update_values_list)):
		update_query+=", %s='%s' "%(str(update_params_list[i]), str(update_values_list[i]))	
	update_query+=build_where_clause(where_params_list=where_params_list, where_values_list=where_values_list)
	update_query+=";"		
	return update_query


def build_insert_query(tablename, insert_params_list, tuple_values_list):
	insert_query="INSERT INTO %s(" %tablename+"%s"%insert_params_list[0]
	# print insert_query
	
	for param in insert_params_list:
		if  insert_params_list[0]!= param:
			insert_query+=", %s"%param
	insert_query+=") VALUES "
	#print insert_query
	
	insert_query+="\n('%s'"%tuple_values_list[0][0]
	for j in range(1,len(tuple_values_list[0])):
		insert_query+=" ,'%s'"%tuple_values_list[0][j]
	insert_query+=")"


	for i in range(1,len(tuple_values_list)):
		insert_query+=",\n('%s'"%tuple_values_list[i][0]
		for j in range(1,len(tuple_values_list[i])):
			insert_query+=" ,'%s'"%tuple_values_list[i][j]
	insert_query+=";"
	# print insert_query
	return insert_query


def build_date(d, m, y):
	return datetime.date(y,m,d)


def build_date2(day, month, year):
	return datetime.date(year,month,day)


"""	<---------------THE CORRECT WAY TO HANDLE DATES IN SQLITE3 with sqliteDefaults------------------>

			#Create a random table
conn.execute('''Create table if not exists person(
		ID INTEGER PRIMARY KEY,
		Name TEXT,
		DOB DATE
		);
		''')
conn.commit()

			#Insert values into the table in one of the accepted formats
sqliteDefaults.insert_table_sqlite(conn, 
	'person', 
	('ID', 	'Name',		'DOB'), 

	[
	(1,		'Bob', 		sqliteDefaults.build_date(07,10,1999)				), 
	(2,		'John', 	sqliteDefaults.build_date(y=2005,m=8,d=21) 			), 
	(3,		'Stacy',	sqliteDefaults.build_date2(month=6,day=25,year=2003)),
	(4,		'Emma',		datetime.date(2001, 10, 27) 						)
	]
)

#Source:	http://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion


table=sqliteDefaults.verified_select_sqlite(conn,"select * from person order by DOB desc;")
for row in table:
	print row

#OUTPUT:
#(2, u'John', datetime.date(2005, 8, 21))
#(3, u'Stacy', datetime.date(2003, 6, 25))
#(4, u'Emma', datetime.date(2001, 10, 27))
#(1, u'Bob', datetime.date(1999, 10, 7))


print table[2][2].day 	

#OUTPUT:
#	27


#We can now compare the values as we do normal datetime objects: with > and <, etc
i=1; j=2;
if table[i][2]<table[j][2]:
	print "%s is older than %s"%(table[i][1], table[j][1])
elif table[j][2]<table[i][2]:
	print "%s is older than %s"%(table[j][1], table[i][1])

#OUTPUT:
#	Emma is older than Stacy


"""





def insert_table_sqlite(conn, tablename, insert_params_list, tuple_values_list, commit=True, printing_debug=False):
	
	insert_query= build_insert_query(tablename=tablename, insert_params_list=insert_params_list, tuple_values_list=tuple_values_list)
	if printing_debug:
		print("\n\n\n\tSQLITE INSERTION QUERY:\n%s\n\n"%insert_query)
	cursor=conn.cursor()
	cursor.execute(insert_query)
	if commit:
		conn.commit()
	# database_in_use(conn)





def insert_table_sqlite2(conn, tablename, parameters_tuple=(), tuple_values_list=[], commit=True, print_query=False):
	if tuple_values_list==[]:
		print("\n\tSQLiteDefaults: insert_table_sqlite() ERROR: tuple_value_list cannot be empty")
		return
	query=""
	if parameters_tuple==():
		query="INSERT INTO %s VALUES " %(tablename);
	else:
		query="INSERT INTO %s %s VALUES" %(tablename, parameters_tuple);
	#else:
		#print("\n\tSQLiteDefaults: insert_table_sqlite() ERROR: parameters_tuple must be a tuple")
	
	query=query+"(?" + (",?"*(len(parameters_tuple)-1)) + ")"	#source: https://docs.python.org/2/library/sqlite3.html

	if print_query:
		print query

	conn.executemany(query, tuple_values_list)
	
	if commit:
		conn.commit()



def verified_select_sqlite(conn, select_query, fetch="all", printing=True):
	'''This function verifies that the entered query is a valid select query (to prevent SQL injection). 
	If it is, it executes it and gets the table object. It  returns None if the table is Empty, and prints an ERROR.
	If the table is non-empty, it returns the table object.'''
	if 'select' in select_query.lower():
		temp = select_query.strip()
		if not ';' in temp:
			temp+=';'
		# print temp
		if temp.index(';') == (len(temp)-1):
			cursor=conn.cursor()
			cursor.execute(temp)
			attributes=[]
			for i in cursor.description:
				attributes.append(i[0])
			result_table=()
			if fetch.lower()=="all":
				result_table=cursor.fetchall()
			elif fetch.lower()=="one":
				result_table=cursor.fetchone()
			else:
				if printing: 
					print "verified_select() ERROR: Improper value '%s' passed to argument 'fetch'"%fetch
				return None 

			if result_table is ():
				if printing: 
					print 'verified_select() ERROR: Empty table'
				return None
			return Table(input_table=result_table, input_attributes=attributes)
			
		else:
			if printing: 
				print 'verified_select() ERROR: Only one query can be fired at a time'
	else:
		if printing: 
			print 'verified_select() ERROR: Only select queries can be executed'


def print_table(conn, select_query):
	table = verified_select_sqlite(conn, select_query, printing=False)
	if table is not None:
		print '\n\n----------------------------------------------------------------'
		for row in table:
			print '\n'
			for i in range(0,len(row)):
				print row[i],"\t\t",
		print '\n\n----------------------------------------------------------------\n'


def list_all_tables(db_file_name):
	conn=get_conn(db_file_name)
	print_table(conn,"select name from sqlite_master where type = 'table';")


'''

print("\n\n<------------TEST CODE----------->\n")

def select_table_sqlite(conn, tablename, parameters_tuple=(), where_string="", order_by_string=""):
	query=""
	if parameters_tuple==():
		query="SELECT * FROM %s"%(tablename)
	elif type(parameters_tuple)=="tuple":
		query="SELECT %s FROM %s"%(parameters_tuple, tablename)
	else:
		print("\n\tSQLiteDefaults: select_table_sqlite() ERROR: parameters_tuple must be a tuple")



	if where_string!="":
		query=query+" WHERE "+where_string
	elif where_string.find(";") != -1:
		print("\n\tSQLiteDefaults: select_table_sqlite() ERROR: where_string cannot have a semicolon in it (this is to prevent SQL injection)")
		return

	if order_by_string!="":
		query=query+" ORDER BY "+order_by_string
	elif order_by_string.find(";") != -1:
		print("\n\tSQLiteDefaults: select_table_sqlite() ERROR: order_by_string cannot have a semicolon in it (this is to prevent SQL injection)")
		return

	query=query+";"
	table=conn.execute(query)
	print type(table)
	for row in table:
		print type(row)
		print row
print("\n<---------END OF TEST CODE-------->\n")
	
'''
