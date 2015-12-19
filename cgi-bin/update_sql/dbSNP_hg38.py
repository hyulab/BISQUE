from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
# file_handle = open('%s/data/dbSNP/dbSNP_missense.txt'%parentdir);

# snp_dict={};
# id_dict={};
# for l in file_handle:
# 	l=l.strip().split('\t');
# 	#UNIQUE ID DICT FOR CONVERTING TO DBSNP QUICKLY
# 	# try:mutations=l[6].split('/');
# 	# except: continue;
# 	# for m in mutations:
# 	# 	unique_id = l[1]+","+l[2]+","+l[5]+","+m;
# 	# 	if unique_id not in id_dict:
# 	# 		id_dict[unique_id]=[]
# 	# 	id_dict[unique_id].append(l[0]);

# 	#DICT FOR CONVERTING FROM DBSNP
# 	try:
# 		if l[0] not in snp_dict:
# 			snp_dict[l[0]]={};
# 		snp_dict[l[0]]["chr"]=l[1]; snp_dict[l[0]]["pos"]=l[2]; snp_dict[l[0]]["wild_type"]=l[5]; snp_dict[l[0]]["mutation"]=l[6];
# 	except: print l;

file_handle = open('%s/data/dbSNP/dbSNP_GRCh37p13_missense.txt'%parentdir);
snp_dict={};
id_dict={};
for l in file_handle:
	l=l.strip().split('\t');
	#UNIQUE ID DICT FOR CONVERTING TO DBSNP QUICKLY
	try:mutations=l[6].split('/');
	except: continue;
	for m in mutations:
		unique_id = l[1]+","+l[2]+","+l[5]+","+m;
		if unique_id not in id_dict:
			id_dict[unique_id]=[]
		id_dict[unique_id].append(l[0]);

	#DICT FOR CONVERTING FROM DBSNP
	try:
		if l[0] not in snp_dict:
			snp_dict[l[0]]={};
		snp_dict[l[0]]["chr"]=l[1]; snp_dict[l[0]]["pos"]=l[2]; snp_dict[l[0]]["wild_type"]=l[5]; snp_dict[l[0]]["mutation"]=l[6];
	except: print l;



with con:
	 cur=con.cursor();
	 table="dbSNP_hg38";
	 table_schema='dbsnp VARCHAR(20) PRIMARY KEY NOT NULL, chr TEXT NOT NULL, pos TEXT NOT NULL, wild_type TEXT(1) NOT NULL, mutation TEXT NOT NULL'
	 try: cur.execute("drop table %s" %(table))
	 except: pass
     table1="pos_dbSNP";
     table_schema1='id VARCHAR(40) PRIMARY KEY NOT NULL, dbsnp TEXT(1000) NOT NULL'
     try: cur.execute("drop table %s" %(table1))
     except: pass
     cur.execute("create table %s (%s)" %(table1, table_schema1));
	 cur.execute("create table %s (%s)" %(table, table_schema));
	 for snp in snp_dict:
	 	fields=snp_dict[snp];
	 	if len(fields)==4:
	 		cur.execute("insert into %s (dbsnp,chr,pos,wild_type,mutation) values ('%s','%s','%s','%s','%s')"%(table,snp,fields["chr"],fields["pos"],fields["wild_type"],fields["mutation"]));

	  for id in id_dict:
	  	cur.execute("insert into %s (id,dbsnp) values ('%s','%s')"%(table1,id,('\t').join(id_dict[id])));


	cur=con.cursor();
	table="dbSNP_hg19";
	table_schema='dbsnp VARCHAR(20) PRIMARY KEY NOT NULL, chr TEXT NOT NULL, pos TEXT NOT NULL, wild_type TEXT(1) NOT NULL, mutation TEXT NOT NULL'
	try: cur.execute("drop table %s" %(table))
	except: pass
	table1="19_pos_dbSNP";
	table_schema1='id VARCHAR(40) PRIMARY KEY NOT NULL, dbsnp TEXT(1000) NOT NULL'
	try: cur.execute("drop table %s" %(table1))
	except: pass
	cur.execute("create table %s (%s)" %(table1, table_schema1));
	cur.execute("create table %s (%s)" %(table, table_schema));
	for snp in snp_dict:
		fields=snp_dict[snp];
		if len(fields)==4:
			cur.execute("insert into %s (dbsnp,chr,pos,wild_type,mutation) values ('%s','%s','%s','%s','%s')"%(table,snp,fields["chr"],fields["pos"],fields["wild_type"],fields["mutation"]));

	for id in id_dict:
		cur.execute("insert into %s (id,dbsnp) values ('%s','%s')"%(table1,id,('\t').join(id_dict[id])));
	

