from os import system, path
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/parsed_files/geneName_uniprot.txt' %(parentdir), 'r')

swissPrimary = {}
swissSynonym = {}
tremblPrimary = {}
tremblSynonym = {}
for l in file_handle:
	geneName = l.split()[0].upper()
	if l.split()[2]=="swiss" and l.split()[3]=="primary":	
		if geneName not in swissPrimary: swissPrimary[geneName]=l.split()[1]
	elif l.split()[2]=="swiss" and l.split()[3]=="synonym":	
		if geneName not in swissSynonym: swissSynonym[geneName]=l.split()[1]
	elif l.split()[2]=="trembl" and l.split()[3]=="primary":		 
		if geneName not in tremblPrimary: tremblPrimary[geneName]=l.split()[1]
	elif l.split()[2]=="trembl" and l.split()[3]=="synonym":
		if geneName not in tremblSynonym: tremblSynonym[geneName]=l.split()[1]

with con:
	cur = con.cursor()
	table = 'geneName_uniprot'
	table_schema = 'geneName VARCHAR(50) PRIMARY KEY NOT NULL, uniprot VARCHAR(10) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass;
	cur.execute("create table %s (%s)" %(table, table_schema))
	cur = con.cursor()
	gn_uniprot = {}
	for gn in swissPrimary:
		cur.execute("insert into %s (geneName, uniprot) values ('%s', '%s')"%(table, gn, swissPrimary[gn]))
	for gn in tremblPrimary:
		if gn not in swissPrimary: 
			gn = gn.replace("'","''")
			try: cur.execute("insert into %s (geneName, uniprot) values ('%s', '%s')"%(table, gn, tremblPrimary[gn]))
			except Exception as e: pass 
	for gn in swissSynonym:
		if gn not in swissPrimary and gn not in tremblPrimary and gn!="X" and gn!="Y": 
			gn = gn.replace("'","''")
			try: cur.execute("insert into %s (geneName, uniprot) values ('%s', '%s')"%(table, gn, swissSynonym[gn]))
			except Exception as e: pass 
	for gn in tremblSynonym:
		if gn not in swissPrimary and gn not in tremblPrimary and gn not in swissSynonym: 
			try: cur.execute("insert into %s (geneName, uniprot) values ('%s', '%s')"%(table, gn, tremblSynonym[gn]))
			except Exception as e: pass

