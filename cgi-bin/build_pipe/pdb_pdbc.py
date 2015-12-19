import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
from Pipe import *

class concretePipe(abstractPipe):
	def __init__(self,input_node,output_type,verbosity,cur):
		abstractPipe.__init__(self,input_node,output_type,verbosity,cur);

	def convert_value(self,verbosity):
		self.cur.execute("select pdb from pdb_uniprot where pdb like '%s"%(self.node.value)+"%'");
		rows=self.cur.fetchall();
		if len(rows)==0: return [None];
		return [x[0] for x in rows if len(x[0])>4];

	def convert_position(self,output_value,verbosity):
		return [self.node.position]

	def convert_mutation(self,output_value,verbosity):
		return [self.node.mutation]
	


		
