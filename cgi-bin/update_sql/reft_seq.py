
import MySQLdb as mdb 
from os import system, path 
from Bio import SeqIO 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User


con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/data/refSeq/unzipped/rna.fa' %(parentdir), 'r')
file_handle2 = open("%s/parsed_files/parsedReft.txt" %(parentdir), 'r')

reft_pos = {}
for l in file_handle2:
    reft = l.split('\t')[0];
    if reft[:2]!="NM":continue; #We only want NM transcripts, at the moment
    sign = l.split('\t')[2];
    cdstart = int(l.split('\t')[3]); cdstop = int(l.split('\t')[4]);
    exonstarts = [int(x) for x in l.split('\t')[5].split(',')]
    exonstops = [int(x) for x in l.split('\t')[6].split(',')]
    exonstarts.sort(); exonstops.sort();
    reft_pos[reft]=[sign, cdstart, cdstop, exonstarts, exonstops]

print reft_pos['NM_170734.3']


with con:
    cur = con.cursor()
#    table = 'reft_seq'
#    table_schema = 'reft VARCHAR(20) PRIMARY KEY NOT NULL, sign CHAR(1) NOT NULL, seq TEXT(100000) NOT NULL'
#	try:cur.execute("drop table %s" %(table))
#	except: pass
#	cur.execute("create table %s (%s)" %(table, table_schema))

    for record in SeqIO.parse(file_handle, 'fasta'):
        reft = record.id.split("|")[3]
        if reft in reft_pos:
            start = 0;
            stop = 0;
            accumulator=0;
            exonstarts = reft_pos[reft][3]; exonstops = reft_pos[reft][4]; cdstart = reft_pos[reft][1]; cdstop = reft_pos[reft][2];


            #+ strand logic
            if reft_pos[reft][0]=="+":
                for i,e in enumerate(exonstarts):
                    if cdstart>=e and cdstart<=exonstops[i]: start=accumulator+cdstart-e;
                    if cdstop>=e and cdstop<=exonstops[i]: stop=accumulator+cdstop-e;
                    accumulator+=(exonstops[i]-e+1)


            #- strand logic
            elif reft_pos[reft][0]=="-":
                exonstarts=exonstarts[::-1]; exonstops=exonstops[::-1];
                if reft == "NM_170734.3": print cdstart, cdstop, exonstarts, exonstops 
                for i,e in enumerate(exonstops):
                    if cdstop>=exonstarts[i] and cdstop<=e: start=accumulator+e-cdstop;
                    if cdstart>=exonstarts[i] and cdstart<=e: stop=accumulator+e-cdstart;
                    accumulator+=(e-exonstarts[i]+1)

#			cur.execute("insert into %s (reft, sign, seq) values ('%s','%s','%s')"%(table, reft, reft_pos[reft][0], record.seq[start:stop+1]))




