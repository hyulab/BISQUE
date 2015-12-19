import os 
import MySQLdb as mdb 
import glob
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User

file_handle = open('%s/parsed_files/19_parsedReft.txt'%parentdir);
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
cur = con.cursor()

reftHg38 = {}
hg19Reft = {}

for l in file_handle:
	reft = l.split('\t')[0]
	if reft[:2]=='NM':
		chromosome = l.split('\t')[1]
		reftHg38[reft]=chromosome
		if chromosome not in hg19Reft:
			hg19Reft[chromosome]=[]
		hg19Reft[chromosome].append(reft)


with con:
	table1 = 'reft_hg19'
	table1_scheme = 'reft CHAR(15) PRIMARY KEY NOT NULL, hg19 TEXT(1000000) NOT NULL'
	table2 = 'hg19_reft'
	table2_scheme = 'hg19 VARCHAR(50) PRIMARY KEY NOT NULL, reft TEXT(1000000) NOT NULL'

	try: cur.execute("drop table %s" %(table1))
	except: pass
	cur.execute("create table %s (%s)" %(table1, table1_scheme))

	try: cur.execute("drop table %s" %(table2))
	except: pass
	cur.execute("create table %s (%s)" %(table2, table2_scheme))

	for t in reftHg38:
		cur.execute("insert into %s values ('%s','chr%s')" %(table1, t, reftHg38[t]))

	for c in hg19Reft:
		cur.execute("insert into %s values ('chr%s','%s')" %(table2, c, ('\t').join(hg19Reft[c])))
