from os import system, path
import sys
import glob 
import MySQLdb as mdb
import pipeline
from pipeline import * 
from build_pipe import *  
#import importlib
import Graph
import re, User 

try: #Handles for if we are dealing with a symlink
	sym_pointer = path.realpath(__file__)
	root_directory = path.abspath(sym_pointer + "/../")
except:
	root_directory = path.abspath(__file__ + "/../")



 #Absolute path to the root project directory
#Helper function. Splits s into capital and lowercase
def split_upper(s):
    return filter(None, re.split("([A-Z][^A-Z]*)", s))

#Fetches the proper custom pipe from the current pipeline
def generatePipe(node, output_type, verbosity,cur=None):
	from_type = node.id_type
	to_type = (output_type).title()
	sys.path.append('%s/pipeline' %(root_directory))
	pipe_module = __import__('%s%s' %(from_type, to_type))
	reload(pipe_module) #THIS IS EXTREMELY IMPORTANT. OTHERWISE PIPE_MODULE.OUTPUT DOES NOT RESET.
	return pipe_module.concretePipe(node, output_type, verbosity,cur) 

#Creates a custom core pipeline of the nodes in nodelist (which must be core-default--nodes)
#I.e, if hg19 and enst are given in the nodelist, the method will create a graph with only
#hg19 and enst, and the pipeline folder
#will only contain pipes relavent to hg19 and enst.
def corePipeline(nodelist): 
	skeleton() 
	for identifier in nodelist:
		if identifier not in Graph.default_graph:
			print "WARNING: %s is not a default identifier and cannot be added to the pipeline." %(identifier)
			nodelist.remove(identifier)
	if len(nodelist) < 2:
		print "ERROR: Must have at least two nodes to make a pipeline."
		return 
	graph = Graph.get_graph()
	pipe_list = []
	for node in nodelist:
		for output in graph[node]:
			if output in nodelist:
				pipe_list.append("%s%s" %(node, output.title()))
	if len(pipe_list) == 0:
		print "ERROR: No connections could be made between your given nodes!"
		return 
	core_class_dictionary = {'enst': 'transcript', 'ensg': 'gene', 'ensp': 'protein', 'uniprot': 'protein', 
	'hg38': 'chromosome', 'hg19':'chromosome', 'reft': 'transcript', 'refp': 'protein', 'dbsnp':'snp','pdb':'pdb', 'pdbc':'pdbc'}
	for pipe in pipe_list:
		# EDGE CASE: NO PDBC TO PDB
		if core_class_dictionary[split_upper(pipe)[0]]=="pdbc" and core_class_dictionary[split_upper(pipe)[1].lower()]=="pdb": continue;

		#Getting pipe from build_pipe and writing it to the pipeline
		inp_file = open("%s/build_pipe/%s_%s.py" %(root_directory, core_class_dictionary[split_upper(pipe)[0]], core_class_dictionary[split_upper(pipe)[1].lower()]))
		out_file = open("%s/pipeline/%s.py" %(root_directory, pipe), 'w')

		for l in inp_file:
			out_file.write(l)
		inp_file.close()
		out_file.close()

#Restores pipeline to ONLY mandatory files. These are package initialization files and main Pipe file
def skeleton():
	files = glob.glob("%s/pipeline/*" %root_directory)
	skeleton_files = ["__init__.py", "Pipe.py"] 
	for f in files:
		if f.split("/")[-1] not in skeleton_files:
			system("rm %s" %(f))


#Adds a new identifier to a graph and creates that new identifiers pipes. The info required for this
#can all be deduced from the new identifiers template. Instructions on how this is done are available
#in the README.txt in the new_node_example directory
def buildPipe(directory_to_template):
	template = open(directory_to_template, 'r')
	template_dict = {}
	for line in template:
		line = line.strip()
		field = line.split()[0][:-1]
		user_input = line.split(None, 1)[1]
		template_dict[field] = user_input

	template.close()

	inp_type = template_dict["input_id_type"]
	out_type = template_dict["output_id_type"]

	if out_type not in Graph.get_graph():
		print "WARNING: Your output identifier (%s) is not in the existing graph!" %(out_type)
		return

	#First, we insert the new identifier into our existing graph (from the bisque module)
	print "Inserting new identifier into graph..."
	if inp_type in Graph.get_graph(): 
		print "Your new identifier is already installed! Try 'python config -r' to reset your graph to default..."; return 
	Graph.add_key(inp_type, [out_type])
	Graph.update(out_type, [inp_type])

	#Next, we will udate the mysql tables from the two tab-delimited files
	print "Creating and updating new MySQL tables!..."
	con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")
	cur = con.cursor()
	
	if template_dict["input_class"] == 'transcript':
		pos_schema = "transcript VARCHAR(50) PRIMARY KEY NOT NULL, cdstart TEXT(100) NOT NULL, cdend TEXT(100) NOT NULL, exonstarts TEXT(1000) NOT NULL, exonends TEXT(1000) NOT NULL"
		seq_schema = "%s VARCHAR(50) PRIMARY KEY NOT NULL, sign CHAR(1) NOT NULL, seq TEXT(1000000) NOT NULL" %(inp_type)
	elif template_dict["input_class"] == 'gene':
		pos_schema = "transcript VARCHAR(50) PRIMARY KEY NOT NULL, gstart TEXT(100) NOT NULL, gend TEXT(100) NOT NULL"
		seq_schema = "%s VARCHAR(50) PRIMARY KEY NOT NULL, seq TEXT(1000000) NOT NULL" %(inp_type)
	else:
		pos_schema = None
		seq_schema = "%s VARCHAR(50) PRIMARY KEY NOT NULL, seq TEXT(1000000) NOT NULL" %(inp_type)
	value_schema = "%s VARCHAR(50) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL" %(inp_type, out_type)
	value_schema2 = "%s VARCHAR(50) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL" %(out_type, inp_type)


	tables = ["%s_%s" %(inp_type, out_type), "%s_seq" %(inp_type), "%s_pos" %(inp_type)]
	schemas = [value_schema, seq_schema, pos_schema]
	files = [template_dict["inputToOutput"], template_dict["inputToSequence"], template_dict["inputToPosition"]]

	for i, f in enumerate(files):
		with con: 
			try: cur.execute("drop table %s" %(tables[i]))
			except: pass
			if schemas[i] == None: continue
			cur.execute("create table %s (%s)" %(tables[i], schemas[i]))
			try: read_file = open(f, 'r') #If user just uses directory relative to root project directory
			except: read_file = open('%s/%s' %(root_directory, f), 'r')  

			
			if tables[i] == "%s_%s" %(inp_type, out_type):
				print "Updating value tables..."
				tab_dictionary1 = {}
				tab_dictionary2 = {}	
				for l in read_file:
					if l.split()[0] not in tab_dictionary1:
						tab_dictionary1[l.split()[0]] = []
					tab_dictionary1[l.split()[0]].append(l.split()[1])

					if l.split()[1] not in tab_dictionary2:
						tab_dictionary2[l.split()[1]] = []
					tab_dictionary2[l.split()[1]].append(l.split()[0])

				for v in tab_dictionary1:
					cur.execute("insert into %s values ('%s', '%s')" %(tables[i], v, ('\t').join(tab_dictionary1[v])))
				try: cur.execute("drop table %s_%s" %(out_type, inp_type))
				except: pass
				cur.execute("create table %s_%s (%s)" %(out_type, inp_type, value_schema2))
				for v in tab_dictionary2:
					cur.execute("insert into %s_%s values ('%s', '%s')" %(out_type,inp_type, v, ('\t').join(tab_dictionary2[v]))) 

				
			if tables[i] == "%s_seq" %(inp_type):
				print "Updating sequence table..."
				if template_dict["input_class"] == "transcript":
					for l in read_file:
						cur.execute("insert into %s (%s, sign, seq) values ('%s', '%s', '%s')" %(tables[i], inp_type, l.split()[0], l.split()[1], l.split()[2]))
				else:
					for l in read_file:
						cur.execute("insert into %s (%s, seq) values ('%s', '%s')" %(tables[i], inp_type, l.split()[0], l.split()[1]))

			elif tables[i] == "%s_pos" %(inp_type) and pos_schema != None:
				print "Updating position table..."
				if template_dict["input_class"] == "transcript":
					for l in read_file:
						values = "'%s', '%s', '%s', '%s', '%s'" %(l.split()[0], l.split()[1], l.split()[2], l.split()[3], l.split()[4])
						cur.execute("insert into %s (transcript, cdstart, cdend, exonstarts, exonends) values (%s)" %(tables[i], values))
				else:
					for l in read_file:
						cur.execute("insert into %s (transcript, gstart, gend) values ('%s', '%s', '%s')" %(tables[i], l.split()[0], l.split()[1], l.split()[2]))

			
	print "Updating pipeline..."

	#Now, we create the input to output pipe
	# system("rm /home/philip/Documents/devToUniProt/pipeline/%s%s.py" %(template_dict["input_id_type"], template_dict["output_id_type"].title()))
	input_file = open("%s/build_pipe/%s_%s.py" %(root_directory, template_dict["input_class"], template_dict["output_class"]), "r")
	output_file = open("%s/pipeline/%s%s.py" %(root_directory, template_dict["input_id_type"], template_dict["output_id_type"].title()), "w")

	for l in input_file:
		output_file.write("%s" %(l))

	#Now we close the connections to the two files 	
	input_file.close()
	output_file.close()

	#Now we create the output to input pipe
	# system("rm /home/philip/Documents/devToUniProt/pipeline/%s%s.py" %(template_dict["output_id_type"], template_dict["input_id_type"].title()))
	input_file = open("%s/build_pipe/%s_%s.py" %(root_directory, template_dict["output_class"], template_dict["input_class"]), "r")
	output_file = open("%s/pipeline/%s%s.py" %(root_directory, template_dict["output_id_type"], template_dict["input_id_type"].title()), "w")

	for l in input_file:
		output_file.write("%s" %(l))

	#Now we close the connections to the two files, and we are done! The new pipes have been sucesfully integrated into the core network!
	input_file.close()
	output_file.close()

#Removes an identifier from the graph and removes its pipes from the pipeline
def removePipe(identifier):
	#First, we remove the identifer from the graph
	Graph.remove_key(identifier)

	#Next, we remove the pipeline files
	pipes = glob.glob("%s/pipeline/*" %(root_directory))
	for p in pipes:
		if identifier in p.split("/")[-1].split(".")[0].lower():
			system("rm %s" %(p)) 

	





























