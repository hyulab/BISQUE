from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/enst_ensp.txt' %(parentdir), 'r')


with con:
	cur = con.cursor()
	table = 'enst_ensp'
	table_schema = 'enst CHAR(15) PRIMARY KEY NOT NULL, ensp TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	enst_ensp = {}
	for l in file_handle:
		if l.split()[0] not in enst_ensp:
			enst_ensp[l.split()[0]] = []
		enst_ensp[l.split()[0]].append(l.split()[1])

	for enst in enst_ensp:
		cur.execute("insert into %s (enst, ensp) values ('%s', '%s')" %(table, enst, ('\t').join(enst_ensp[enst])))


