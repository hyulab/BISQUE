from os import system, path
import MySQLdb as mdb 
import sys 
import os 
import re
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
file_handle = open('%s/data/pdb/pdbresiduemapping.txt' %(parentdir), 'r')
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")

pdb_pos={};
uniprot_pos={};



with con:
	cur=con.cursor();
	table = 'pdb_pos'
	table_schema = 'pdb VARCHAR(30) BINARY PRIMARY KEY NOT NULL, uniprot_pos TEXT(5000) NOT NULL, pdb_pos TEXT(5000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))

	# cur=con.cursor();
	# table1 = 'uniprot_pdb_pos'
	# table_schema1 = 'uniprot VARCHAR(20) PRIMARY KEY NOT NULL, uniprot_pos TEXT(5000) NOT NULL, pdb_pos TEXT(5000) NOT NULL'
	# try:cur.execute("drop table %s" %(table1))
	# except: pass
	# cur.execute("create table %s (%s)" %(table1, table_schema1))

	for l in file_handle:
		l=l.strip().split();
		# l[1]=l[1].split("");
		# if re.match(r'^[a-z]$',l[1]): l[1]="_"+l[1];
		pdb_id=l[0]+l[1]+"-"+l[2];
		uniprot=l[2];
		uniprot_pos=l[3][1:-1];
		pdb_pos=l[4][1:-1];
		try:cur.execute("insert into %s (pdb,uniprot_pos,pdb_pos) values ('%s','%s','%s')"%(table, pdb_id,uniprot_pos,pdb_pos));
		except: print pdb_id;
		