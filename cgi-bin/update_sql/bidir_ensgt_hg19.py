from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s'%(glob.glob('%s/data/ensembl/unzipped/Homo_sapiens.GRCh37.75.gtf'%parentdir)[0]));

enst_hg19 = {}
ensg_hg19 = {}
hg19_enst = {}
hg19_ensg = {} 



with con:
	cur=con.cursor()
	table1 = 'enst_hg19'
	table2 = 'ensg_hg19'
	table3 = 'hg19_enst'
	table4 = 'hg19_ensg'
	tables=[table1, table2, table3, table4]

	table1_scheme = 'enst CHAR(15) PRIMARY KEY NOT NULL, hg19 TEXT(1000000) NOT NULL'
	table2_scheme = 'ensg CHAR(15) PRIMARY KEY NOT NULL, hg19 TEXT(1000000) NOT NULL'
	table3_scheme = 'hg19 VARCHAR(50) PRIMARY KEY NOT NULL, enst TEXT(1000000) NOT NULL'
	table4_scheme = 'hg19 VARCHAR(50) PRIMARY KEY NOT NULL, ensg TEXT(1000000) NOT NULL'
	schemes = [table1_scheme, table2_scheme, table3_scheme, table4_scheme]

	for l in file_handle:
		try:
			if l.split('\t')[2]=='transcript':
				hg19=l.split('\t')[0]
				transcript = l.split('\t')[8].split(';')[1].split()[1][1:-1]
				if hg19 not in hg19_enst:
					hg19_enst[hg19] = [] 
				hg19_enst[hg19].append(transcript)
				enst_hg19[transcript] = hg19

			elif l.split('\t')[2]=='gene':
				hg19=l.split('\t')[0]
				gene = l.split('\t')[8].split(';')[0].split()[1][1:-1]
				if hg19 not in hg19_ensg:
					hg19_ensg[hg19] = [] 
				hg19_ensg[hg19].append(gene) 
				ensg_hg19[gene] = hg19

		except:
			pass 


	for i,t in enumerate(tables):
		try: cur.execute("drop table %s" %(t))
		except: pass
		cur.execute("create table %s (%s)" %(t, schemes[i]))

	for t in enst_hg19:
		if len(enst_hg19[t])<=2: #Determines whether or not to add 'chr' to beginning
			cur.execute("insert into %s values ('%s','chr%s')" %(table1, t, enst_hg19[t]))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table1, t, enst_hg19[t]))
	for t in ensg_hg19:
		if len(ensg_hg19[t])<=2:
			cur.execute("insert into %s values ('%s','chr%s')" %(table2, t, ensg_hg19[t]))
		else:
			cur.execute("insert into %s values ('%s','chr%s')" %(table2, t, ensg_hg19[t]))
	for c in hg19_enst:
		if len(c)<=2:
			cur.execute("insert into %s values ('chr%s','%s')" %(table3, c, ('\t').join(hg19_enst[c])))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table3, c, ('\t').join(hg19_enst[c])))
	for c in hg19_ensg:
		if len(c)<=2:
			cur.execute("insert into %s values ('chr%s','%s')" %(table4, c, ('\t').join(hg19_ensg[c])))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table4, c, ('\t').join(hg19_ensg[c])))