#! /usr/bin/env python

import glob, subprocess, shlex
import optparse 
from os import system, path, sys, remove, symlink, unlink
import getpass
import glob 
import Graph



root_directory = path.abspath(__file__ + "/../")

###COMMAND-LINE PARAMETERS###
parser = optparse.OptionParser()
parser.add_option('-i', '--include', action = 'store_true', help = 'If this option is included, the core graph will be composed only of the inputed arguments.')
parser.add_option('-r', '--reset', action = 'store_true', help = 'If this option is included, the installer will only reset your installation to factory settings and will not install the program.')

options, args = parser.parse_args()
#############################


##################
#HELPER FUNCTIONS#
##################
def rm(filename):
	try:
	    remove(filename)
	except OSError:
	    pass

#Returns True if pkg (string) is installed and false otherwise
def is_installed(pkg):
	if pkg == 'mysql': pkg='mysql-client'
	cmd = ['dpkg-query', '-W', '-f', '${Status}', pkg]
	output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
	if output == 'install ok installed': return True 
	return False

def is_installed_non_debian(pkg):
	cmd = ['rpm', '-qa', pkg]
	output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
	if not output: return False;
	else: return True;


########################
#CHECKING OPTIONS.RESET#
########################
if options.reset: 
	rm('%s/user_info/sql_info.txt'%root_directory)
	rm("%s/parsed_files" %root_directory)
	dirs = ['data/ensembl','data/refSeq','data/uniprot']
	for d in dirs:
		files = glob.glob('%s/%s/*' %(root_directory, d))
		for f in files: 
			if f.split("/")[-1] == 'unzipped': system("rm -r %s" %(f))
	sys.exit()


################################
#CLEARING AND INITIALIZING DATA#
################################

rm("%s/user_info/sql_info.txt"%root_directory)
file_handle = open("%s/user_info/sql_info.txt"%root_directory, 'w'); 
file_handle.write("Username:\nPassword:\nAddress:\n")
file_handle.close();



print '		################################'
print "		#WELCOME TO BISQUE INSTALLATION#"
print "		################################"

############################################
#Checking for required package dependencies#
############################################
required_packages = ['mysql', 'mysql-server', 'emboss']

print "\nChecking package dependencies..."
for pkg in required_packages:

	try:
		result = is_installed(pkg)
	except: 
		result = is_installed_non_debian(pkg)
	if result:
		print "%s is installed..." %pkg
	else:
		sys.exit("pkg %s is not installed. Please install this before installing BISQUE!" %pkg)
print "All required packages are installed!\n"

print "Checking module dependencies..."
try: 
	import Bio 
	print "python-biopython is installed..."
except: 
	sys.exit("You do not have the following module dependency installed: python-biopython. Please install this before installing BISQUE!")
try: 
	import MySQLdb as mdb
	print "python-mysqldb is installed..." 
except: 
	sys.exit("You do not have the following module dependency installed: python-mysqldb. Please install this before installing BISQUE!")

print "All module dependencies are installed!\n"
print "**************************************\n"

###############################################
#Getting user MySQL info and creating database#
###############################################
print "Now the installer will require your MySQL username, password and server address in order to build the BISQUE database from the local data files, which is necessary for all calculations and mappings.\n"
permission = raw_input("If this is OK, enter 'y' without quotes. Otherwise, enter 'n' and the installation will be cancelled:  ")
if permission != 'y': sys.exit()

import User

print "###########"
print "#User info#"
print "###########"
print 'Please enter your MySQL username, password, and host (localhost if local)'
username = raw_input('MySQL username: ')
password = getpass.getpass('MySQL password: ')

address = raw_input('MySQL host: ')
User.set_username(username)
User.set_password(password)
User.set_address(address)

con = mdb.connect(User.get_address(), User.get_username(), User.get_password())
cur = con.cursor()
with con:
	try: cur.execute("drop database bisque")
	except: pass
	cur.execute("create database bisque") 



##################
#Unzip data files#
##################
print "################"
print "#Unzipping data#"
print "################"

print "Unzipping Uniprot data"
system("python %s/ftp_downloads/uniprot_unzip.py" %(root_directory))

print "Unzipping refSeq data..."
system("python %s/ftp_downloads/refSeq_unzip.py" %(root_directory))

print "Unzipping Ensembl data..."
system("python %s/ftp_downloads/ensembl_unzip.py" %(root_directory))

print "Unzipping NCBI data..."
system("python %s/ftp_downloads/ncbi_unzip.py" %(root_directory))

###########################################
#Run parser scripts to create parsed files#
###########################################
print "##############"
print "#Parsing data#"
print "##############"
system("mkdir parsed_files")
print "Beginning Uniprot parsing..."
files = glob.glob('%s/parser_scripts/parse_uniprot/*' %(root_directory))
for f in files:
	system("python %s" %(f))
print "Finished parsing Uniprot!"

print "Beginning Ensembl parsing..."
files = glob.glob('%s/parser_scripts/parse_ensembl/*' %(root_directory))
for f in files:
	system("python %s" %(f))
print "Finished parsing Ensembl!"

print "Beginning RefSeq parsing..."
files = glob.glob('%s/parser_scripts/parse_refSeq/*' %(root_directory))
for f in files:
	system("python %s" %(f))
print "Finished parsing RefSeq"



#######################
#Creating SQL database#
#######################
import Graph 
print "#######################"
print "#MySQL database import#"
print "#######################"

#Recreating sql database from backup
print "Building MySQL database... (This will take 1-2 minutes)"
# try:
# 	if is_installed('pv'): system("pv %s/data/sql_dumps/bisque.sql | mysql -u%s -p%s bisque"%(root_directory, User.get_username(), User.get_password()))
# except:
# 	if is_installed_non_debian('pv'): system("pv %s/data/sql_dumps/bisque.sql | mysql -u%s -p%s bisque"%(root_directory, User.get_username(), User.get_password()))
# else:
# 	print "Building database without pv visuals..." 
system("mysql -u%s -p%s bisque < %s/data/sql_dumps/bisque.sql" %(User.get_username(), User.get_password(), root_directory)) 
print "MySQL database created!"


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
import pipeFactory
print "##############################"
print "#Customized pipeline creation#"
print "##############################"
print "Initializing pipeline..."
if options.include:
	pipeFactory.corePipeline(args)
else:
	default_identifiers = [node for node in Graph.default_graph]
	pipeFactory.corePipeline(default_identifiers)

print "Pipeline created!"



########################################################
#Moving bin files into $Path and making them executable#
########################################################



print " "
print "In order for BISQUE to be run and imported from any directory, the installer requires sudo access to add a symlink to the $PATH"
permission = raw_input('Enter "y" without quotations if this is OK. Otherwise, enter "n" to skip this optional step:  ')

if(permission=='y'):
	system("sudo chmod +x bisque.py")
	system("sudo chmod +x config.py")
	print '%s/bisque.py'%root_directory
	try: 
		symlink('%s/bisque.py'%root_directory, '/usr/local/bin/bisque')
	except:
		system('sudo unlink /usr/local/bin/bisque'); symlink('%s/bisque.py'%root_directory, '/usr/local/bin/bisque')

	#Adding cgi-bin symlink to directory in PYTHON PATH for enabling global module import
	PYTHONPATH = sys.path;


	#Giving user option of which python version to use
	pythonOptions = glob.glob('/usr/lib/python2.*')
	if len(pythonOptions)>1: #If multiple versions of python are installed
		print "You have multiple versions of python installed. The following versions are supported:"
		counter = 0
		for x in pythonOptions:
			if int(x.split('/')[-1].split('.')[1]) >=6:
				counter+=1
				print x.split('/')[-1]
		if counter==0: sys.exit("You do not have any valid version of python installed. Please install a valid verison of python (2.6-<3.0) and run the installer again.") 
		pythonVersion = raw_input("Please enter the python version you wish to use (e.g, python2.6): ")

	elif len(pythonOptions)==1:
		pythonVersion = pythonOptions[0].split("/")[-1]
		print "Python version %s detected..." %pythonVersion
	else:
		sys.exit("You do not have python installed. Please install python and run the installer again.") 


	if '/usr/lib/%s/dist-packages'%pythonVersion in sys.path:
		print "Symlink created in %s/dist-packages"%pythonVersion
		system('sudo unlink /usr/lib/%s/dist-packages/bisque_tools'%pythonVersion);
		system('sudo ln -s %s /usr/lib/%s/dist-packages/bisque_tools'%(root_directory, pythonVersion));
	elif '/usr/lib/%s/site-packages'%pythonVersion in sys.path:
		print "Symlink created in %s/site-packages"%pythonVersion
		system('sudo unlink /usr/lib/%s/site-packages/bisque_tools'%pythonVersion);
		system('sudo ln -s %s /usr/lib/%s/dist-packages/bisque_tools'%(root_directory, pythonVersion));
	elif '/usr/lib/%s/' in sys.path:
		print "Symlink created in %s/"%pythonVersion
		system('sudo unlink /usr/lib/%s/bisque_tools'%pythonVersion);
		system('sudo ln -s %s /usr/lib/%s/dist-packages/bisque_tools'%(root_directory,pythonVersion));
	else:
		sys.exit("No folder in python path!")



