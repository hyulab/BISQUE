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
	table = 'ensp_enst'
	table_schema = 'ensp CHAR(15) PRIMARY KEY NOT NULL, enst TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	ensp_enst = {}
	for l in file_handle:
		if l.split()[1] not in ensp_enst:
			ensp_enst[l.split()[1]] = []
		ensp_enst[l.split()[1]].append(l.split()[0])

	for ensp in ensp_enst:
		cur.execute("insert into %s (ensp, enst) values ('%s', '%s')" %(table, ensp, ('\t').join(ensp_enst[ensp])))


