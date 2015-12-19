from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
file_handle = open('%s'%(glob.glob('%s/data/ensembl/unzipped/Homo_sapiens.GRCh38.*.gtf'%parentdir)[0]));



# import os 
# import MySQLdb as mdb 
# import User 
# import glob

# root_directory = os.path.abspath(__file__ + "/../../")

# file_handle = open('%s'%(glob.glob('%s/data/ensembl/unzipped/Homo_sapiens.GRCh38.*.gtf'%root_directory)[0]));
# con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
# cur = con.cursor()

enst_hg38 = {}
ensg_hg38 = {}
hg38_enst = {}
hg38_ensg = {} 



with con:
	cur=con.cursor();
	table1 = 'enst_hg38'
	table2 = 'ensg_hg38'
	table3 = 'hg38_enst'
	table4 = 'hg38_ensg'
	tables=[table1, table2, table3, table4]

	table1_scheme = 'enst CHAR(15) PRIMARY KEY NOT NULL, hg38 TEXT(1000000) NOT NULL'
	table2_scheme = 'ensg CHAR(15) PRIMARY KEY NOT NULL, hg38 TEXT(1000000) NOT NULL'
	table3_scheme = 'hg38 VARCHAR(50) PRIMARY KEY NOT NULL, enst TEXT(1000000) NOT NULL'
	table4_scheme = 'hg38 VARCHAR(50) PRIMARY KEY NOT NULL, ensg TEXT(1000000) NOT NULL'
	schemes = [table1_scheme, table2_scheme, table3_scheme, table4_scheme]

	for l in file_handle:
		try:
			if l.split('\t')[2]=='transcript':
				hg38=l.split('\t')[0]
				transcript = l.split('\t')[8].split(';')[2].split()[1][1:-1]
				if hg38 not in hg38_enst:
					hg38_enst[hg38] = [] 
				hg38_enst[hg38].append(transcript)
				enst_hg38[transcript] = hg38

			elif l.split('\t')[2]=='gene':
				hg38=l.split('\t')[0]
				gene = l.split('\t')[8].split(';')[0].split()[1][1:-1]

				if hg38 not in hg38_ensg:
					hg38_ensg[hg38] = [] 
				hg38_ensg[hg38].append(gene) 
				ensg_hg38[gene] = hg38

		except:
			pass 


	for i,t in enumerate(tables):
		try: cur.execute("drop table %s" %(t))
		except: pass
		cur.execute("create table %s (%s)" %(t, schemes[i]))

	for t in enst_hg38:
		if len(enst_hg38[t])<=2: #Determines whether or not to add 'chr' to beginning
			cur.execute("insert into %s values ('%s','chr%s')" %(table1, t, enst_hg38[t]))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table1, t, enst_hg38[t]))
	for t in ensg_hg38:
		if len(ensg_hg38[t])<=2:
			cur.execute("insert into %s values ('%s','chr%s')" %(table2, t, ensg_hg38[t]))
		else:
			cur.execute("insert into %s values ('%s','chr%s')" %(table2, t, ensg_hg38[t]))
	for c in hg38_enst:
		if len(c)<=2:
			cur.execute("insert into %s values ('chr%s','%s')" %(table3, c, ('\t').join(hg38_enst[c])))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table3, c, ('\t').join(hg38_enst[c])))
	for c in hg38_ensg:
		if len(c)<=2:
			cur.execute("insert into %s values ('chr%s','%s')" %(table4, c, ('\t').join(hg38_ensg[c])))
		else:
			cur.execute("insert into %s values ('%s','%s')" %(table4, c, ('\t').join(hg38_ensg[c])))