#! /usr/bin/env python
import sys
# try:
import pipeFactory, Graph
import optparse, glob 
from os import system, path, remove 
# except:
# 	sys.exit("BISQUE is not fully installed! Please run the installer.py script completely.")

def rm(filename):
	try:
	    remove(filename)
	except OSError:
		pass;
	    

#try:root_directory = ("/").join(readlink(__file__).split("/")[:-1]) #If config is accessed from /usr/local/bin--symlink
root_directory = path.abspath(__file__ + "/../")

#########################
#COMMAND-LINE PARAMETERS#
#########################
parser = optparse.OptionParser()
parser.add_option("-r", '--reset', action = 'store_true', help = """Resets the identifier graph/pipeline
				 to either default, or--if extra argument are provided--to a customized graph/pipeline""")
parser.add_option("-g", '--graph', action = 'store_true', help = "Display the current graph in dictionary format")
parser.add_option("-a", '--add', help="Add an existing identifier to the graph.")
parser.add_option("-n", '--new', help = "Builds a new pipe and incorporates it into the existing graph. The directory to the template is a required argument.")
parser.add_option("-f", '--factory', action = 'store_true', help = "Restores program to factory settings so it is ready to be distributed. For developers only.")
parser.add_option("-d", "--delete", help = "Removes an idenifier from the identifier graph and removes all pipes connected to the identifier.")
options, args = parser.parse_args()

#########
#FACTORY#
#########
#Restores program to factory settings, so it is ready to be compressed and distributed
if options.factory:
	try:
		rm('%s/user_info/sql_info.txt'%root_directory)
		pipeFactory.skeleton()
		system("rm -r %s/parsed_files/" %root_directory)
		dirs = ['data/ensembl','data/refSeq','data/uniprot','data/ncbi','data/dbSNP', 'data/misc']
		for d in dirs:
			files = glob.glob('%s/%s/*' %(root_directory, d))
			for f in files: 
				if f.split("/")[-1] == 'unzipped': system("rm -r %s" %(f))
		system("rm -r %s/*.pyc" %(root_directory))
		
		print "Done"
		system("find %s -name *.pyc -delete" %root_directory)
	except:
		print "BISQUE is not fully installed!"


#####
#ADD#
#####
if options.add:
	Graph.add_key(options.add.split(":")[0], options.add.split(":")[1].split(","))


#######
#RESET#
#######
#Resets both the identifier graph and the pipeline to default if no arguments are given,
#otherwise, it resets it to a custom graph/pipeline.
if options.reset:
	if len(args) == 0:
		print "Resetting graph and pipeline to default..."
		#First, we reset the graph
		Graph.default()
		#Now, we reset the pipeline
		default_identifiers = [node for node in Graph.default_graph]
		pipeFactory.corePipeline(default_identifiers)
	elif len(args) > 0:
		#We destroy the graph and remake a customized graph
		print "Resetting and customizing graph and pipeline..." 
		Graph.destroy()
		Graph.create()
		for identifier in args:
			try: 
				outputs = [] 
				for x in Graph.default_graph[identifier]:
					if x in args: outputs.append(x)
				Graph.add_key(identifier, outputs) 
			except: print "The identifier %s is not a default identifier!" %(identifier); pass
		#Now we re-create the customized pipeline
		pipeFactory.corePipeline(args)

#######
#GRAPH#
#######
#Returns the current graph as a dictionary representation
if options.graph:
	for node in Graph.get_graph():
		print "%s: %s" %(node, Graph.get_graph()[node])
#####
#NEW#
#####
#Adds a new identifier to the graph/pipeline
if options.new:
	pipeFactory.buildPipe(options.new)

########
#REMOVE#
########
#Removes identifier from graph/pipeline
if options.delete:
	pipeFactory.removePipe(options.delete)






