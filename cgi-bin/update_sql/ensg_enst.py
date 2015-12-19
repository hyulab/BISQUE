from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
file_handle = open('%s/parsed_files/enst_ensg.txt' %(parentdir), 'r')
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")

with con:
	cur = con.cursor()
	table = 'ensg_enst'
	table_schema = 'ensg CHAR(15) PRIMARY KEY NOT NULL, enst TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	ensg_enst = {}
	for l in file_handle:
		if l.split()[1] not in ensg_enst:
			ensg_enst[l.split()[1]] = []
		ensg_enst[l.split()[1]].append(l.split()[0])

	for ensg in ensg_enst:
		cur.execute("insert into %s (ensg, enst) values ('%s', '%s')" %(table, ensg, ('\t').join(ensg_enst[ensg])))


