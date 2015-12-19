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


file_handle = open("%s/data/refSeq/unzipped/protein.gbk"%parentdir,"r");
protein=None;
protein_transcript={}
transcript_protein={}
for l in file_handle:
	l=l.strip().split();
	try:
		if l[0]=="LOCUS":
			protein="%s.1"%l[1]
		if l[0]=="VERSION":
			protein=l[1];
		elif l[0]=="DBSOURCE":
			transcript=l[3]
			if protein[:2]=="NP" and transcript[:2]=="NM":
				#DICT A
				if protein not in protein_transcript: protein_transcript[protein]=[]
				protein_transcript[protein].append(transcript);
				#DICT B
				if transcript not in transcript_protein: transcript_protein[transcript]=[]
				transcript_protein[transcript].append(protein);
				protein=None; transcript=None;
	except:
		pass;

with con:
	cur = con.cursor()
	for typ in ["reft","refp"]:
		out="refp" if typ=="reft" else "reft";
		table="%s_%s"%(typ,out)
		table_schema='%s VARCHAR(20) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL, version INT'%(typ,out);
		try:cur.execute("drop table %s" %(table))
		except: pass
		cur.execute("create table %s (%s)" %(table, table_schema))
		dic=transcript_protein if typ=="reft" else protein_transcript;
		for x in dic:
			cur.execute("insert into %s (%s,%s) values ('%s','%s')"%(table,typ,out,x[0],('\t').join([a[0] for a in dic[x]])));

