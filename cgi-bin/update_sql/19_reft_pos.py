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
	table = '19_reft_pos'
	table_scheme = 'transcript CHAR(15) PRIMARY KEY NOT NULL, cdstart TEXT NOT NULL, cdstop TEXT NOT NULL, exonstarts TEXT NOT NULL, exonstops TEXT NOT NULL'
	try: cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_scheme))

	for l in file_handle:
		cdstart = l.split('\t')[3]; cdstop = l.split('\t')[4];
		exonstarts = ('\t').join(l.split('\t')[5].split(',')); exonstops = ('\t').join(l.split('\t')[6].split(','))
		transcript = l.split('\t')[0];

		cur.execute("insert into %s values ('%s','%s','%s','%s','%s')"%(table,transcript,cdstart,cdstop,exonstarts,exonstops))


file_handle.close()
