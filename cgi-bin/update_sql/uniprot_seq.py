from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/uniprot_aaseq.txt' %(parentdir), 'r')


with con:
	cur = con.cursor()
	table = 'uniprot_seq'
	table_schema = 'uniprot CHAR(15) PRIMARY KEY NOT NULL, seq TEXT(100000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	uniprot_seq = {}
	for l in file_handle:
		cur.execute("insert into %s (uniprot, seq) values ('%s', '%s')" %(table, l.split()[0], l.split()[1]))


