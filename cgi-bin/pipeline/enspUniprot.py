import MySQLdb as mdb
import sys 
import os 
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
sys.path.append('%s/tools' %(root_directory))
import needle_wrapper
import Node
from Pipe import *


class concretePipe(abstractPipe):

    def __init__(self, input_node, out_type, verbosity,cur):
        abstractPipe.__init__(self,input_node, out_type, verbosity,cur)


    def convert_value(self, verbosity): #Override for uniprot isoform
        value=self.node.value;
        from_type = self.node.id_type
        to_type = self.out_type
        self.cur.execute("select %s from %s_%s where %s = '%s'" %(to_type, from_type, to_type, from_type, value))
        result = self.cur.fetchall()
        if len(result) == 0: #No results were found
            print "WARNING Could not map %s: %s to its %s values!" %(self.node.id_type, self.node.value, self.out_type)
            return [None]
        elif len(result) == 1:
            return result[0][0].split()

    def convert_mutation(self, output_value, verbosity):

        return [self.node.mutation]

    def convert_position(self, output_value, verbosity):
        self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value))
        rows=self.cur.fetchall();
        inputSequence=rows[0][0]
        self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value))
        rows=self.cur.fetchall();
        outputSequence=rows[0][0]
        alignment = needle_wrapper.run_stretcher(inputSequence, outputSequence, sub_matrix='EBLOSUM62')
        position = self.node.position - 1 #0-index for easier calculations
        #Position to input segment mapping
        topPointer = 0
        inputPointer = 0
        for i in range(len(alignment[0][0])):
            if alignment[0][0][i] == "-": continue
            elif inputPointer == position:
                topPointer = i
                break
            else:
                inputPointer+=1
        #Input segment position to output segment mapping
        if alignment[0][1][topPointer] == "-": 
            return [None]
        else:
            counter = 0
            for i in range(topPointer):
                if alignment[0][1][i] != "-":
                    counter += 1
            return [counter + 1]

    def convert_quality(self, output_value, verbosity):
        try:
            #Get Conversion Quality
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value))
            rows=self.cur.fetchall();
            inputSequence=rows[0][0]
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value))
            rows=self.cur.fetchall();
            outputSequence=rows[0][0]
            #alignment = needle_wrapper.run_needle(inputSequence, outputSequence, sub_matrix='EBLOSUM62', NEEDLE_PATH='tools/needle')
            alignment = needle_wrapper.run_stretcher(inputSequence, outputSequence, sub_matrix='EBLOSUM62')
            return alignment[2]
        except:
            return -1





