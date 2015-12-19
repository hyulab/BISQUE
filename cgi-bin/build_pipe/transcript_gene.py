import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
from Pipe import *

class concretePipe(abstractPipe):

	def __init__(self, input_node, output_type, verbosity,cur):
		abstractPipe.__init__(self,input_node, output_type, verbosity,cur)

	def convert_mutation(self, output_value, verbosity):
		
		#Getting transcript sign
		sign = self.get_sign(self.node.id_type, self.node.value, self.cur, verbosity)

		#Converting mutation...
		if sign == "+":
			output_mutation = self.node.mutation
		elif sign == "-":
			try:output_mutation = self.complement(self.node.mutation, verbosity)
			except:output_mutation=None;
		
		return [output_mutation]


	def convert_position(self, output_value, verbosity):

		#Getting Dechunked Transcript position
		dechunked_position = self.dechunk_position(self.node.position, self.node.value, self.cur, verbosity);

		#Calculating dechunked_position relative to the output_value gene: goalPos=dechunked_position-gstart
		self.cur.execute("select gstart from %s_pos where gene='%s'" %(self.out_type, output_value))
		rows = self.cur.fetchall()
		if len(rows)==0: print "WARNING: Could not deduce chromosomal positions from given gene. Returning None for position."; return [None];
		try:
			return [dechunked_position-int(rows[0][0])+1] #+1 is to account for 1-based index
		except:
			return [None]











