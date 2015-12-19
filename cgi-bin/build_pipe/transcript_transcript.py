import MySQLdb as mdb
import sys 
import transcriptOperations as tops
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
sys.path.append('%s/tools' %(root_directory))
import needle_wrapper
import Graph
import Node
from Pipe import *

class concretePipe(abstractPipe):
    #Dependency Variables
    outputPosition = -1

    def __init__(self, input_node, out_type, verbosity, cur):
        abstractPipe.__init__(self,input_node, out_type, verbosity, cur)


    def convert_mutation(self, output_value, verbosity):		
        self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value));
        #self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value)); 
        rows = self.cur.fetchall();
        if len(rows)==0:
            output_mutation = [None]
            print "WARNING: Could not deduce sequence from given transcript. Continuing without error handling..."
        else:
            seq=rows[0][0];
            output_mutation = "%s%s"%(seq[self.outputPosition - 1], self.node.mutation[-1])
            if output_mutation[0] != self.node.mutation[0]:
                output_mutation = "%s?"%output_mutation[0]

        return [output_mutation]


    def convert_position(self, output_value, verbosity):
        try:
            inputDechunked=tops.dechunk_position(self.node.position,self.node.value,self.node.id_type,self.cur);
            outputChunked=tops.chunk_position(inputDechunked,output_value,self.out_type,self.cur);
            self.outputPosition = outputChunked
            return [outputChunked];

        except:
            return [None];

    def convert_quality(self, output_value, verbosity):
        #Get Conversion Quality
        try:
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value))
            rows=self.cur.fetchall();
            inputSequence=rows[0][0]
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value))
            rows=self.cur.fetchall();
            outputSequence=rows[0][0]
            alignment = needle_wrapper.run_stretcher(inputSequence, outputSequence, sub_matrix='EDNAFULL')
            return alignment[2]
        except IndexError:
            return 0.0

