from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/uniprot_enst.txt'%(parentdir), 'r')


with con:
	cur = con.cursor()
	table = 'uniprot_enst'
	table_schema = 'uniprot CHAR(15) PRIMARY KEY NOT NULL, enst TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	uniprot_enst = {}
	for l in file_handle:
		if l.split()[0] not in uniprot_enst:
			uniprot_enst[l.split()[0]] = []
		if l.split()[1] not in uniprot_enst[l.split()[0]]: uniprot_enst[l.split()[0]].append(l.split()[1])

	for uniprot in uniprot_enst:
		cur.execute("insert into %s (uniprot, enst) values ('%s', '%s')" %(table, uniprot, ('\t').join(uniprot_enst[uniprot])))


