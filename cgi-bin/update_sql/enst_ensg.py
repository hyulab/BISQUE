from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/enst_ensg.txt' %(parentdir), 'r')


with con:
	cur = con.cursor()
	table = 'enst_ensg'
	table_schema = 'enst CHAR(15) PRIMARY KEY NOT NULL, ensg TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	enst_ensg = {}
	for l in file_handle:
		if l.split()[0] not in enst_ensg:
			enst_ensg[l.split()[0]] = []
		enst_ensg[l.split()[0]].append(l.split()[1])

	for enst in enst_ensg:
		cur.execute("insert into %s (enst, ensg) values ('%s', '%s')" %(table, enst, ('\t').join(enst_ensg[enst])))


