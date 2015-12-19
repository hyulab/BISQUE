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

	
	def convert_mutation(self,output_value,verbosity):
		return [None]
	def convert_position(self,output_value,verbosity):
		cur=self.cur;
		cur.execute("select * from pdb_pos where pdb='%s'"%(output_value+"-" + self.node.value));
		rows=cur.fetchall();
		if len(rows)==0: return [None];
		rows=rows[0];
		pdb_ranges=rows[2].split(',');
		uniprot_ranges=rows[1].split(',');
		print rows;
		for i,ran in enumerate(uniprot_ranges):
			if len(ran.split("-")) > 1:
				int_ran=[int(x) for x in ran.split("-")];
				if self.node.position in range(int_ran[0],int_ran[1]+1):
					int_pdb_ran=[int(x) for x in pdb_ranges[i].split("-")];
					return [self.node.position-int_ran[0]+int_pdb_ran[0]];
			else:
				if self.node.position == int(ran): return [int(uniprot_ranges[i])];

		return [None];




		
