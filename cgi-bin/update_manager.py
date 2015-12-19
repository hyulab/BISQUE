import glob, subprocess, os.path, shlex
import MySQLdb as mdb
import Graph, User
import pipeFactory, optparse 
from os import system

###COMMAND-LINE PARAMETERS###
parser = optparse.OptionParser()
parser.add_option('-i', '--include', action = 'store_true', help = 'If this option is included, the core graph will be composed only of the inputed arguments.')
parser.add_option('-d','--dump', action='store_true', help='This option causes the update to ONLY perform an sqldump of your current local BISQUE database')

options, args = parser.parse_args()
#############################



system("rm -rf data")
system("rm -rf parsed_files")



# ###########################
# #Downloading and Unzipping#
# ###########################
print "#############################"
print "#Fetching and unzipping data#"
print "#############################"

print "Downloading Uniprot data..."
system("python ftp_downloads/uniprot_DL.py")
print "Finished downloading Uniprot data!"

print "Unzipping Uniprot data"
system("python ftp_downloads/uniprot_unzip.py")
print "Finished unzipping Uniprot data!"

print "Downloading refSeq data..."
system("python ftp_downloads/refSeq_DL.py")
print "Finished downloading refSeq data!"

print "Unzipping refSeq data..."
system("python ftp_downloads/refSeq_unzip.py")
print "Finished unzipping refSeq data!"

print "Downloading Ensembl data..."
system("python ftp_downloads/ensembl_DL.py")

print "Unzipping Ensembl data..."
system("python ftp_downloads/ensembl_unzip.py")

print "Downloading NCBI data..."
system("python ftp_downloads/ncbi_DL.py")

print "Unzipping NCBI data..."
system("python ftp_downloads/ncbi_unzip.py")

###########################################
#Run parser scripts to create parsed files#
###########################################
print "##############"
print "#Parsing data#"
print "##############"

system("mkdir parsed_files")

print "Beginning Uniprot parsing..."
files = glob.glob('parser_scripts/parse_uniprot/*')
for f in files:
	system("python %s" %(f))
print "Finished parsing Uniprot!"

print "Beginning Ensembl parsing..."
files = glob.glob('parser_scripts/parse_ensembl/*')
for f in files:
	system("python %s" %(f))
print "Finished parsing Ensembl!"

print "Beginning refSeq parsing..."
files = glob.glob('parser_scripts/parse_refSeq/*')
for f in files:
	system("python %s" %(f))
print "Finished parsing refSeq"

###########################
#SQL table creation/update#
###########################
print "####################################"
print "#Creating and updating SQL database#"
print "####################################"
con = mdb.connect(User.get_address(),  User.get_username(), User.get_password())
cur = con.cursor()
with con:
	try:cur.execute("create database bisque")
	except: pass 

	cur.execute("use bisque")

sql_files = glob.glob("update_sql/*")
print "Updating sql tables..."
for f in sql_files:
	print "Updating %s..." %(f)
	system("python %s" %(f))
	print "Finished udating %s!" %(f)

#Creating a bisque sqldump
print "Backing up SQL database."
system("mkdir data/sql_dumps")
system('rm data/sql_dumps/bisque.sql')
system("mysqldump -u%s -p%s bisque > data/sql_dumps/bisque.sql" %(User.get_username(), User.get_password())) 
print "SQL database backed up!"

#Storing the core graph in an sql table	
print "Creating custom graph..."
if not options.include:
	try: Graph.destroy(); 
	except: pass
	Graph.create()
	Graph.default()
else:
	try: Graph.destroy();
	except: pass
	Graph.create()
	for key in Graph.default_graph:
		outputs = []
		if key in args:
			for o in Graph.default_graph[key]:
				if o in args: outputs.append(o)
			Graph.add_key(key, outputs)
print "Graph created!"




#######################################
#Creating pipeline from the core graph#
#######################################
print "##############################"
print "#Customized pipeline creation#"
print "##############################"
print "Initializing pipeline..."
if options.include:
	pipeFactory.corePipeline(args)
else:
	pipeFactory.corePipeline(['enst', 'ensg', 'ensp', 'uniprot', 'hg38','reft','refp'])






