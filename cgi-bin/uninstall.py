#! /usr/bin/env python
import MySQLdb as mdb 
import User
from os import system, path 

###################
#Drop SQL Database#
###################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password())
with con:
	cur = con.cursor() 
	try: cur.execute("drop database bisque")
	except: pass 

#####################
#Remove symlink file#
#####################
system("sudo rm /usr/local/bin/run_tool")

##########################
#Remove project directory#
##########################
root_directory = path.abspath(__file__ + "/../")
system("sudo rm -r %s" %(root_directory))

