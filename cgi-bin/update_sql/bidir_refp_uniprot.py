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
files=glob.glob('%s/data/uniprot/unzipped/HUMAN_[0-9]*_idmapping.dat'%(parentdir));
fileHandle = open(files[0], 'r');
# DICTIONARY INSTANTIATIONS
uniprotRefp={}; refpUniprot={};
counter=0;
for l in fileHandle:
	l=l.strip().split('\t');
	if l[1]=="RefSeq" and re.match(r'^NP_.*$',l[2], re.IGNORECASE):
		uniprot=l[0] if (len(l[0].split("-"))>1 and l[0].split("-")[1]!="1") else l[0].split("-")[0];
		refp=l[2]#.split(".")[0];
		if uniprot=="P35609-2": print refp;
		if uniprot not in uniprotRefp: uniprotRefp[uniprot]=[];
		uniprotRefp[uniprot].append(refp);
		if refp not in refpUniprot: refpUniprot[refp]=[];
		refpUniprot[refp].append(uniprot);


with con:
	cur = con.cursor()
	for typ in ["refp","uniprot"]:
		out="uniprot" if typ=="refp" else "refp";
		length="VARCHAR(20)" if typ=="refp" else "CHAR(15)";
		table="%s_%s"%(typ,out)
		table_schema='%s %s PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL'%(typ,length,out);
		try:cur.execute("drop table %s" %(table))
		except: pass
		cur.execute("create table %s (%s)" %(table, table_schema))
		dic=refpUniprot if typ=="refp" else uniprotRefp;
		for x in dic:
			cur.execute("insert into %s (%s,%s) values ('%s','%s')"%(table,typ,out,x,('\t').join(dic[x])));
