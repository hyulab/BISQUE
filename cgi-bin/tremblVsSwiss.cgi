#!/usr/bin/env python 
print "Content-type: text/plain\n\n";

import cgi
import MySQLdb as mdb
import User
import cgitb
from os import path 

cgitb.enable()

root_directory = path.abspath(__file__ + "/../../")

################
#SQL CONNECTION#
################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur=con.cursor();

###########################
#EXECUTION WITH INPUT DATA#
###########################
data = cgi.FieldStorage()
uniprot = data.getvalue("uniprot");

with con:
	cur.execute("select source from uniprot_source where uniprot='%s'"%uniprot)
	rows=cur.fetchall();
	try:print rows[0][0]
	except: pass

