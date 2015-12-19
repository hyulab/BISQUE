import MySQLdb as mdb
import User 

#################GRAPH#################
#This program uses a dictionary graph implementation to find the mysql table traversal between types (nodes)

#Narrow Query pass-through nodes are nodes whose queries are narrows by the input node
narrowNodes = ['hg38']

default_graph = { #A constant default graph of core identifiers.
	'enst': ['uniprot','ensp','hg38','ensg','reft','hg19'],
	'ensp': ['enst','refp','uniprot'],
	'ensg': ['enst', 'hg38','hg19'],
	'hg38': ['enst', 'ensg', 'reft','dbsnp'],
	'uniprot': ['enst', 'refp','ensp','pdbc'],
	'hg19': ['enst','ensg','dbsnp','reft'],
	'reft': ['hg38','refp','enst','hg19'],
	'refp':['uniprot','reft','ensp'],
	'dbsnp':['hg38','hg19'],
	'pdb':['pdbc'],
	'pdbc':['uniprot']
}



#get_graph() returns the current identifier graph in dictionary format
def get_graph():
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	graph = {}
	with con: 
		cur.execute("select * from graph")
		rows = cur.fetchall()
		if len(rows) == 0:
			print "WARNING: There are no nodes in the graph!"
		else:
			for row in rows:
				for output in row[1].split(","):
					if row[0] not in graph:
						graph[row[0]] = []
					graph[row[0]].append(output)
		return graph

#A graph which avoids the hg38 node
def get_optimized_graph():
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	graph = {}
	with con: 
		cur.execute("select * from graph")
		rows = cur.fetchall()
		if len(rows) == 0:
			print "WARNING: There are no nodes in the graph!"
		else:
			for row in rows:
				for output in row[1].split(","):
					if output!='hg38' and output!='hg19' and row[0]!='hg38' and row[0]!='hg19':
						if row[0] not in graph:
							graph[row[0]] = []
						graph[row[0]].append(output)
		return graph

#creates an empty sql table representing the identifier graph
def create():
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	with con:
		cur.execute('create table graph (input varchar(50)  primary key not null, outputs text(1000) not null)')

#add_key(key, outputs) adds a key and its outputs to the existing identifier graph
def add_key(key, outputs):
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	with con:
		try:cur.execute("delete from graph where input='%s'"%key)
		except:pass
		try: cur.execute("insert into graph (input, outputs) values ('%s', '%s')" %(key, (",").join(outputs)))
		except: 
			print "WARNING: Couldn't add %s to the graph!" %(key) 
			pass

#remove_key(key) removes the key from the identifier graph, and any outputs which match the key
def remove_key(key):
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	with con:
		cur.execute("select * from graph")
		rows = cur.fetchall()
		for row in rows:
			identifier = row[0]; outputs = row[1].split(",")
			if identifier == key: 
				cur.execute("delete from graph where input='%s'" %identifier)
			else:
				try: 
					outputs.remove(key)
					outputs = (",").join(outputs)
					cur.execute("update graph set outputs='%s' where input='%s'" %(outputs, identifier))
				except: pass 

#similar to remove_key, but instead of removing all traces of the key, only removes the row where the key==primary key
def remove_key_lite(key):
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()
	with con:
		cur.execute("delete from graph where input='%s'" %(key)) 
	
#update(key, outputs) updates the outputs of a specific key
def update(key, outputs):
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()
	with con:
		cur.execute("select outputs from graph where input = '%s'" %(key)) 
		rows = cur.fetchall()
		if len(rows) == 0:
			print "WARNING: The key has no values!"
		elif len(rows) == 1:
			l = rows[0][0].split(",")
			for o in outputs:
				l.append(o)
			remove_key_lite(key);
			add_key(key, l);

#sets the sql identifier graph to default
def default():
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	with con:
		try:cur.execute("drop table graph")
		except: pass
		cur.execute('create table graph (input varchar(50)  primary key not null, outputs text(1000) not null)')
		cur.execute("insert into graph (input, outputs) values ('ensg', 'enst,hg38,hg19')")
		cur.execute("insert into graph (input, outputs) values ('ensp','enst,refp,uniprot')")
		cur.execute("insert into graph (input, outputs) values ('enst','uniprot,ensp,hg38,hg19,ensg,reft')")
		cur.execute("insert into graph (input, outputs) values ('uniprot','enst,refp,ensp,pdbc')")
		cur.execute("insert into graph (input, outputs) values ('hg38','enst,ensg,reft,dbsnp')")
		cur.execute("insert into graph (input, outputs) values ('hg19','enst,ensg,dbsnp,reft')")
		cur.execute("insert into graph (input, outputs) values ('reft','hg38,refp,enst,hg19')")
		cur.execute("insert into graph (input, outputs) values ('refp','reft,uniprot,ensp')")
		cur.execute("insert into graph (input, outputs) values ('dbsnp','hg38,hg19')")
		cur.execute("insert into graph (input, outputs) values ('pdbc','uniprot')")
		cur.execute("insert into graph (input, outputs) values ('pdb','pdbc')")



#destroys the identifier graph 
def destroy():
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()

	with con:
		cur.execute("drop table graph")











