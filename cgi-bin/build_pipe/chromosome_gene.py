import MySQLdb as mdb
import Node
from Pipe import *
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))

class concretePipe(abstractPipe):

	def __init__(self, input_node, out_type, verbosity,cur):
		abstractPipe.__init__(self,input_node, out_type, verbosity,cur)
	
	def convert_value(self, verbosity):
		#Convert_value is overriden here. Chromosomes output SO many ENST's, and if the user inputs a specific position,
		#we only want to return the enst at that position.
		if self.node.position != None:
			cur=self.cur;
			if self.node.id_type=='hg19': cur.execute("select %s from %s_%s, 19_%s_pos where %s='%s' and %s=gene and %i>=gstart and %i<=gend"%(self.out_type, self.out_type,self.node.id_type,self.out_type,self.node.id_type,self.node.value,self.out_type,self.node.position,self.node.position))
			else: cur.execute("select %s from %s_%s, %s_pos where %s='%s' and %s=gene and %i>=gstart and %i<=gend"%(self.out_type, self.out_type,self.node.id_type,self.out_type,self.node.id_type,self.node.value,self.out_type,self.node.position,self.node.position))
			rows=cur.fetchall()
			if len(rows)==0:
				print "WARNING: Could not deduce transcripts from given chromosome."
			 	return [None]
			results=[g[0] for g in rows]
			return results if len(results) > 0 else [None]

		else:
			return super(concretePipe, self).convert_value(verbosity)

	def convert_mutation(self, output_value, verbosity):
		return [self.node.mutation]

	def convert_position(self, output_value, verbosity):
		cur=self.cur;
		#Getting gene positions
			#Deprecated hg19 handling
		if self.node.id_type=='hg19': cur.execute("select * from 19_%s_pos where gene = '%s'" %(self.out_type, output_value))
		else: cur.execute("select * from %s_pos where gene = '%s'" %(self.out_type, output_value))
		rows = cur.fetchall()
		if len(rows) == 0:
			print "WARNING: Could not deduce chromosome positions from the output gene. Returning None..."
			return [None]
		elif len(rows) == 1:
			rows = rows[0]
			gstart = int(rows[1])

		output_position = (self.node.position - gstart) + 1 #+1 to make it 1-based
		return [output_position]


