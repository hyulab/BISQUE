import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Graph 
import Node
import random
import pipeFactory
from Pipe import *

class concretePipe(abstractPipe):

	def __init__(self, input_node, output_type, verbosity, cur):
		abstractPipe.__init__(self,input_node, output_type, verbosity, cur)

	def convert_mutation(self, output_value, verbosity):
		#Getting transcript sign
		sign = self.get_sign(self.node.id_type, self.node.value, self.cur, verbosity)
	
		#Converting mutation
		if sign == "+":
			output_mutation = self.node.mutation
		elif sign == "-":
			try:output_mutation = self.complement(self.node.mutation, verbosity)
			except:output_mutation=None;

		
		return [output_mutation]

	def convert_position(self, output_value, verbosity):
		chrpos = self.dechunk_position(self.node.position, self.node.value,self.cur,verbosity);
		return [chrpos]
