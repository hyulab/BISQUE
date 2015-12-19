#from os import system, path
#import glob
#import MySQLdb as mdb 
#import sys 
#import os 
#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#os.sys.path.insert(0,parentdir) 
#import User
#import transcriptOperations as tops
#con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
#
#BATCH_LIMIT = 200000
#
#with con:
#    cur = con.cursor()
#    table = '19_pos_reft'
#    table_scheme = 'position VARCHAR(50) PRIMARY KEY NOT NULL, reft TEXT NOT NULL'
#    try: cur.execute("drop table %s" %table)
#    except: pass
#    cur.execute("create table %s (%s)" %(table, table_scheme))
#
#    cur.execute("select * from hg19_reft")
#    rows = cur.fetchall()
#    for row in rows:
#        chr = row[0]
#        pos_table = {}
#        if chr[:3] != "chr": continue
#        print "Processing %s"%chr
#        #Fill table
#        transcripts = row[1].split()
#        for t in transcripts:
#            chunks = tops.get_chunks("19_reft", t, cur)
#            if chunks: 
#                for rng in chunks:
#                    for i in range(rng[0], rng[1] + 1):
#                        if i not in pos_table:
#                            pos_table[i] = []
#                        pos_table[i].append(t)
#        #Write table to temp csv file
#        temp_file = open("/tmp/temp_batch.csv", "w")
#        for position in pos_table:
#            temp_file.write("%s,%s\n"%(str(position) + "+" + chr, ("\t").join(pos_table[position])))
#        #Dump file into mysql table
#        statement = "LOAD DATA INFILE '/tmp/temp_batch.csv' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"%table
#        print "Beginning dump of %s"%chr
#        cur.execute(statement)
#        print "Finished up of %s"%chr

# SLOW TABLE BUILD. EASIER ON DISK SPACE
import os 
import MySQLdb as mdb 
import glob
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User

con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque") 
cur = con.cursor()

file_handle=open('%s/parsed_files/19_parsedReft.txt'%parentdir, 'r')

with con:
    table = '19_pos_reft'
    table_scheme = 'cdstart INT NOT NULL, cdstop INT NOT NULLL, chr VARCHAR(8), reft TEXT NOT NULL, PRIMARY KEY(cdstart,cdstop,chr)'
    try: cur.execute("drop table %s" %(table))
    except: pass
    cur.execute("create table %s import(%s)" %(table, table_scheme))

    cds_reft={}

    for l in file_handle:
        cursordstart = int(l.split('\t')[3]); cdstop = int(l.split('\t')[4]);
        transcriptscript = l.split('\t')[0];
        chrom=l.strip().split('\t')[1];
        unique_id="%s-%s-%s"%(cdstart,cdstop,chrom);
        if unique_id not in cds_reft:
            pathcds_reft[unique_id]=[]
        cds_reft[unique_id].append(transcript);


    for cds in cds_reft:
        data=cds.split("-");
        cdstart=int(data[0]); cdstop=int(data[1]); chrom="chr"+data[2];
        transcript=cds_reft[cds];
        cur.execute("insert into %s values (%i,%i,'%s','%s')"%(table,cdstart,cdstop,chrom,("\t").join(transcript)))


file_handle.close()
