
import MySQLdb as mdb 
from os import system, path 
from Bio import SeqIO 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User


con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/data/refSeq/unzipped/protein.fa' %(parentdir), 'r');


with con:
	cur = con.cursor()
	table = 'refp_seq'
	table_schema = 'refp VARCHAR(25) PRIMARY KEY NOT NULL, seq TEXT(100000) NOT NULL'
	try:cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_schema))

	for record in SeqIO.parse(file_handle, 'fasta'):
		refp = record.id.split("|")[3]#.split(".")[0];
		seq = record.seq;
		if refp[0:2]=="NP":
			cur.execute("insert into %s (refp, seq) values ('%s','%s')"%(table, refp,seq))
			



