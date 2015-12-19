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
		

			
		#Conversion
		#Getting transcript sign
		sign = self.get_sign(self.out_type, output_value, self.cur, verbosity)

		#Converting mutation
		if sign == "+":
			output_mutation = self.node.mutation
		elif sign == "-":
			try:output_mutation = self.complement(self.node.mutation, verbosity)
			except:output_mutation=None;

		
		return [output_mutation]

	def convert_position(self, output_value, verbosity):
		# with self.con:
		# 	cur = self.con.cursor()

		#Getting chromosomal position of self.node.position 
		self.cur.execute("select gstart from %s_pos where gene='%s'"%(self.node.id_type,self.node.value))
		rows = self.cur.fetchall()
		if len(rows)==0: print "WARNING: Could not deduce start position from the gene. Returning None as position..."
		chrPos = int(rows[0][0])+(self.node.position-1) #-1 to account for 1-indexing

		#Chunking position on transcript, and returning that position
		chunkedPos = self.chunk_position(chrPos, output_value, self.cur, verbosity)

		return [chunkedPos]
		



