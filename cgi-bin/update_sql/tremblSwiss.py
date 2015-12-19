from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User


con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle=open('%s/data/uniprot/unzipped/uniprot_sprot_human.dat'%parentdir);
file_handle2=open('%s/data/uniprot/unzipped/uniprot_trembl_human.dat'%parentdir);

uniprotToSource = {}

# Sprot file 
for l in file_handle:
	if l.split()[0]=="AC":
		uniprot = l.split()[1].split(';')[0].replace(";","")
		if uniprot not in uniprotToSource:
			uniprotToSource[uniprot]="s"
		else: print "Overlap!"


# Sprot file 
for l in file_handle2:
	try: 
		if l.split()[0]=="AC":
			uniprot = l.split()[1].split(';')[0].replace(";","")
			if uniprot not in uniprotToSource:
				uniprotToSource[uniprot]="t"
			else: print "Overlap!" 
	except: pass 



with con:
	cur = con.cursor()
	table = 'uniprot_source'
	table_scheme = 'uniprot CHAR(15) PRIMARY KEY NOT NULL, source char(1)'
	try: cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_scheme))

	for u in uniprotToSource:
		cur.execute("insert into %s (uniprot, source) values ('%s','%s')"%(table, u,uniprotToSource[u]))


	