#!/usr/bin/env python 
print "Content-type: text/plain\n\n";

import User
import Graph
import random
import MySQLdb as mdb

#This script generates a random identifier for testing purposes

################
#SQL CONNECTION#
################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur=con.cursor();

identifiers=["ensg","enst","ensp","uniprot","refp","reft"];
random_type = identifiers[int(random.random()*len(identifiers))]
graph = Graph.get_graph();
output_types = graph[random_type];
random_out_type=output_types[int(random.random()*len(output_types))]
table="%s_%s"%(random_type,random_out_type)

with con:
	cur.execute("select * from %s order by rand() limit 1"%table)
	rows=cur.fetchall();
	rows=rows[0][0];
	print rows;