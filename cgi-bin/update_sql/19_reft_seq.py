
import MySQLdb as mdb 
from os import system, path 
from Bio import SeqIO 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User


con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open("%s/parsed_files/19_parsedReft.txt" %(parentdir), 'r')

reft_pos = {}
for l in file_handle:
	reft = l.split('\t')[0];
	if reft[:2]!="NM":continue; #We only want NM transcripts, at the moment
	sign = l.split('\t')[2];
	reft_pos[reft]=sign


with con:
	cur = con.cursor()
	table = '19_reft_seq'
	table_schema = 'reft VARCHAR(20) PRIMARY KEY NOT NULL, sign CHAR(1) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))

        for t in reft_pos:
            cur.execute("insert into %s values ('%s','%s')"%(table,t,reft_pos[t]));
	
	
	
	
	
	

	
	
	
	
	
	
	
