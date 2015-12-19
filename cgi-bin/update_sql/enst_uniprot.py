from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/uniprot_enst.txt' %(parentdir), 'r')


with con:
	cur = con.cursor()
	table = 'enst_uniprot'
	table_schema = 'enst CHAR(15) PRIMARY KEY NOT NULL, uniprot TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	enst_uniprot = {}
	for l in file_handle:
		if l.split()[1] not in enst_uniprot:
			enst_uniprot[l.split()[1]] = []
		enst_uniprot[l.split()[1]].append(l.split()[0])

	for enst in enst_uniprot:
		cur.execute("insert into %s (enst, uniprot) values ('%s', '%s')" %(table, enst, ('\t').join(enst_uniprot[enst])))


