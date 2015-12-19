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


# import os 
# import MySQLdb as mdb 
# import User 

# root_directory = os.path.abspath(__file__ + "/../../")

# file_handle = open('%s/data/ensembl/unzipped/Homo_sapiens.GRCh37.75.gtf' %(root_directory), 'r')
# con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
# cur = con.cursor()

with con:
	cur=con.cursor();
	table = '19_ensg_pos'
	table_scheme = 'gene CHAR(15) PRIMARY KEY NOT NULL, gstart TEXT NOT NULL, gend TEXT NOT NULL'
	try: cur.execute("drop table %s" %(table))
	except: pass
	cur.execute("create table %s (%s)" %(table, table_scheme))

	ensg_pos_dict = {}

	for l in file_handle:
		try:
			if l.split('\t')[2] == 'gene':
				ensg = l.split('\t')[8].split(';')[0].split()[1][1:-1]
				start = l.split('\t')[3]
				end = l.split('\t')[4]
				if ensg not in ensg_pos_dict:
					ensg_pos_dict[ensg]=[] 
				ensg_pos_dict[ensg].append(start)
				ensg_pos_dict[ensg].append(end)
		except:
			pass 

	for g in ensg_pos_dict:
		positions = ensg_pos_dict[g]
		cur.execute("insert into %s values ('%s','%s','%s')" %(table, g, positions[0],positions[1]))