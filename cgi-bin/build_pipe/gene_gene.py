import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
from Pipe import *

class concretePipe(abstractPipe):

	def __init__(self, input_node, out_type, verbosity):
		abstractPipe.__init__(self,input_node, output_type, verbosity)
	

	def convert_mutation(self, output_value, verbosity):
		return [self.node.mutation]

	def convert_position(self, output_value, verbosity):
		return [self.node.position]