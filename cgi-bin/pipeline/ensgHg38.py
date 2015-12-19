import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
from Pipe import *

class concretePipe(abstractPipe):

	def __init__(self, input_node, out_type, verbosity,cur):
		abstractPipe.__init__(self,input_node, out_type, verbosity,cur)
	

	def convert_mutation(self, output_value, verbosity):

		return [self.node.mutation]

	def convert_position(self, output_value, verbosity):

		#Getting gene positions
		
		#Support for deprecated hg19 build
		if (self.out_type)=='hg19': self.cur.execute("select * from 19_%s_pos where gene = '%s'" %(self.node.id_type, self.node.value))
		else: self.cur.execute("select * from %s_pos where gene = '%s'" %(self.node.id_type, self.node.value))
		rows = self.cur.fetchall()
		if len(rows) == 0:
			print "WARNING: Could not deduce chromosome positions from the output gene. Returning None..."
			return [None]
		elif len(rows) == 1:
			rows = rows[0]
			gstart = int(rows[1])

		output_position = self.node.position + gstart - 1; #-1 to take into account that the gene position is 1-indexed

		return [output_position]
