import MySQLdb as mdb
import sys 
import identifierOperations as iops
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
        self.cur.execute("select * from dbSNP_%s where dbSNP='%s'"%(self.out_type,self.node.value));
        rows=self.cur.fetchall();
        if len(rows)==0: return [None];
        rows=rows[0];
        #UPDATE POSITION AND MUTATION FIELDS, WHICH ARE PARSED FROM SNP ID
        self.node.position=int(rows[2]);
        mutation="%s%s"%(rows[3],rows[4])
        self.node.mutation=mutation;
        #Update wild type field as well
        print self.node.position
        self.node.wt_source = iops.get_wild_type("chr" + rows[1], self.out_type, int(rows[2]), self.cur)
        results=["chr"+rows[1]];
        return results;

    def convert_mutation(self,output_value,verbosity):
        return ["%s%s"%(self.node.mutation[0],x) for x in self.node.mutation[1:].split('/')]
    def convert_position(self,output_value,verbosity):
        return [self.node.position for i in range(len(self.node.mutation.split('/')))];


