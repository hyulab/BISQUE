from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/enst_seq.txt' %(parentdir), 'r')

with con:
	cur = con.cursor()
	table = 'enst_seq'
	table_schema = 'enst CHAR(15) PRIMARY KEY NOT NULL, sign CHAR(1) NOT NULL, seq TEXT(100000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	enst_seq = {}
	for l in file_handle:
		enst = l.split()[0]; sign = l.split()[1]; seq = l.split()[2]
		cur.execute("insert into %s (enst, sign, seq) values ('%s','%s','%s')" %(table, enst, sign, seq))


