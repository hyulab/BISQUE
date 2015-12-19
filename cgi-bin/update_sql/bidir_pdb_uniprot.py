from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
file_handle = open('%s/data/pdb/pdbresiduemapping.txt' %(parentdir), 'r')
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")

pdb_uniprot={};
uniprot_pdb={};

for l in file_handle:
	l=l.strip().split();
	pdb=l[0];
	pdb_struct=(l[0]+l[1]);
	uniprot=l[2];
	if pdb not in pdb_uniprot:
		pdb_uniprot[pdb]=[];
	pdb_uniprot[pdb].append(uniprot);

	if pdb_struct not in pdb_uniprot:
		pdb_uniprot[pdb_struct]=[];
	pdb_uniprot[pdb_struct].append(uniprot);

	if uniprot not in uniprot_pdb:
		uniprot_pdb[uniprot]=[]
	uniprot_pdb[uniprot].append(pdb_struct);

with con:
	cur=con.cursor();
	table = 'pdb_uniprot'
	table_schema = 'pdb VARCHAR(10) BINARY PRIMARY KEY NOT NULL, uniprot TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	for pdb in pdb_uniprot:
		cur.execute("insert into %s (pdb,uniprot) values ('%s','%s')"%(table,pdb,('\t').join(pdb_uniprot[pdb])));

	
	table = 'uniprot_pdb'
	table_schema = 'uniprot VARCHAR(20) PRIMARY KEY NOT NULL, pdb TEXT(1000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))
	for uniprot in uniprot_pdb:
		cur.execute("insert into %s (uniprot,pdb) values ('%s','%s')"%(table,uniprot,('\t').join(uniprot_pdb[uniprot])));		