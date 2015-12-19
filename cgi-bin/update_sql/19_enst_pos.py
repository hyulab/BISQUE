from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s/data/ensembl/unzipped/Homo_sapiens.GRCh37.75.gtf' %(parentdir), 'r')

with con:
    cur=con.cursor();
    table = '19_enst_pos'
    table_scheme = 'transcript CHAR(15) PRIMARY KEY NOT NULL, cdstart TEXT NOT NULL, cdstop TEXT NOT NULL, exonstarts TEXT NOT NULL, exonstops TEXT NOT NULL'
    try: cur.execute("drop table %s" %(table))
    except: pass
    cur.execute("create table %s (%s)" %(table, table_scheme))

    transcript_positions = {}
    for l in file_handle:
        try:
            #if l.split('\t')[1] == 'protein_coding': #If it is a coding transcript
            if l.split('\t')[2] == 'transcript':
                transcript = l.split('\t')[8].split(';')[1].strip().split()[1][1:-1]
                if transcript not in transcript_positions:
                    transcript_positions[transcript]={'exon_starts':[], 'exon_stops':[], 'cds':[]}
            elif l.split('\t')[2] == 'exon':
                transcript = l.split('\t')[8].split(';')[1].strip().split()[1][1:-1]
                exon_start = l.split('\t')[3]
                exon_stop = l.split('\t')[4]
                transcript_positions[transcript]['exon_starts'].append(exon_start)
                transcript_positions[transcript]['exon_stops'].append(exon_stop)
            elif l.split('\t')[2] == 'CDS':
                transcript = l.split('\t')[8].split(';')[1].strip().split()[1][1:-1]
                cds_start = l.split('\t')[3]
                cds_stop = l.split('\t')[4]
                transcript_positions[transcript]['cds'].append(cds_start)
                transcript_positions[transcript]['cds'].append(cds_stop)
        except:
            pass 




    for t in transcript_positions:
        formated_exon_starts = ('\t').join(transcript_positions[t]['exon_starts'])
        formated_exon_stops = ('\t').join(transcript_positions[t]['exon_stops'])
        cds_ranges = transcript_positions[t]['cds'];
        if len(cds_ranges)==0: continue;
        cds_ranges.sort();
        cds_start = cds_ranges[0]
        cds_stop = cds_ranges[-1]
        cur.execute("insert into %s values ('%s','%s','%s','%s','%s')" %(table, t, cds_start, cds_stop, formated_exon_starts, formated_exon_stops))


