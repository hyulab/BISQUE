from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
import transcriptOperations as tops
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")

with con:
    cur = con.cursor()
    table = 'pos_enst'
    table_scheme = 'position VARCHAR(50) PRIMARY KEY NOT NULL, enst TEXT NOT NULL'
    try: cur.execute("drop table %s" %table)
    except: pass
    cur.execute("create table %s (%s)" %(table, table_scheme))

    cur.execute("select * from hg38_enst")
    rows = cur.fetchall()
    for row in rows:
        chr = row[0]
        pos_table = {}
        if chr[:3] != "chr": continue
        print "Processing %s"%chr
        #Fill table
        transcripts = row[1].split()
        for t in transcripts:
            chunks = tops.get_chunks("enst", t, cur)
            if chunks: 
                for rng in chunks:
                    for i in range(rng[0], rng[1] + 1):
                        if i not in pos_table:
                            pos_table[i] = []
                        pos_table[i].append(t)
        #Write table to temp csv file
        temp_file = open("/tmp/temp_batch.csv", "w")
        for position in pos_table:
            temp_file.write("%s,%s\n"%(str(position) + "+" + chr, ("\t").join(pos_table[position])))
        #Dump file into mysql table
        statement = "LOAD DATA INFILE '/tmp/temp_batch.csv' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"%table
        print "Beginning dump of %s"%chr
        cur.execute(statement)
        print "Finished up of %s"%chr
