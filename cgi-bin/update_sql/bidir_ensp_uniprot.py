from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import re
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")


file_handle = open('%s/parsed_files/uniprot_ensp.txt' %(parentdir), 'r');
# DICTIONARY INSTANTIATIONS
uniprot_ensp={}; ensp_uniprot={};

for l in file_handle:
	# if re.match(r'^NP_[0-9]*\.[0-9]*',l.strip().split()[5], re.IGNORECASE) and re.match(r'^NM_[0-9]*\.[0-9]*',l.strip().split()[3], re.IGNORECASE):
	uniprot=l.strip().split()[0]; ensp=l.strip().split()[1];
	# Append to dict 1
	if uniprot not in uniprot_ensp:uniprot_ensp[uniprot]=[];
	uniprot_ensp[uniprot].append(ensp);
	# Append to dict 2
	if ensp not in ensp_uniprot:ensp_uniprot[ensp]=[];
	ensp_uniprot[ensp].append(uniprot);

with con:
	cur = con.cursor()
	for typ in ["uniprot","ensp"]:
		out="ensp" if typ=="uniprot" else "uniprot";
		table="%s_%s"%(typ,out)
		table_schema='%s VARCHAR(25) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL'%(typ,out) if typ=="uniprot" else '%s CHAR(15) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL'%(typ,out)
		try:cur.execute("drop table %s" %(table))
		except: pass
		cur.execute("create table %s (%s)" %(table, table_schema))
		dic=uniprot_ensp if typ=="uniprot" else ensp_uniprot;
		for x in dic:
			cur.execute("insert into %s (%s,%s) values ('%s','%s')"%(table,typ,out,x.split('.')[0],('\t').join([a.split('.')[0] for a in dic[x]])));

