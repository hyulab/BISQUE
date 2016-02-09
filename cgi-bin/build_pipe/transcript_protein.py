import MySQLdb as mdb
import sys 
import os 
import math
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
sys.path.append('%s/tools' %(root_directory))
import needle_wrapper
import Node
from Pipe import *

stop_codons = ["TAG", "TAA", "TGA"]

class concretePipe(abstractPipe):

    def __init__(self, input_node, out_type, verbosity, cur):
        abstractPipe.__init__(self,input_node, out_type, verbosity, cur)


    def convert_mutation(self, output_value, verbosity):

        cur=self.cur;
        user_wt_base = self.node.mutation[0]
        user_mut_base = self.node.mutation[-1]

        cur.execute("select seq from %s_seq where %s = '%s'" %(self.node.id_type, self.node.id_type, self.node.value))
        rows = cur.fetchall()
        if len(rows) == 1:
            nseq = rows[0][0]
            codon_list = self.split_sequence(nseq)
            try:
                wt_base = nseq[self.node.position-1]
                wt_codon = codon_list[(self.node.position-1)/3]
                mut_codon = ''
            except: return [None];

            for i, ch in enumerate(wt_codon): 
                if i == (self.node.position-1)%3:
                    mut_codon += self.node.mutation[-1]
                else:
                    mut_codon += ch 

            wt_aa = self.codon_dict[wt_codon]
            mut_aa = self.codon_dict[mut_codon]

            cur.execute("select seq from %s_seq where %s = '%s'" %(self.out_type, self.out_type, output_value))
            rows = cur.fetchall()
            try:
                if len(rows) == 1:
                    aaseq = rows[0][0]
                    if aaseq[(self.node.position-1)/3] != wt_aa and len(output_value.split("-"))<2:
                        print "WARNING: Predicted wild type aa does not match protein wild type aa!"
                        return [None]
                else:
                    print "WARNING: Could not deduce aaseq from protein. Continuing without error handling..."

                return ["%s%s"%(wt_aa, mut_aa)]
            except:
                return [None]



        else:
            print "WARNING: Could not derive nucleotide sequence from given tranript! This is a mandatory derivation. Returning None..."
            return [None]

    def convert_position(self, output_value, verbosity):

        aa_position = int(math.ceil(float(self.node.position)/float(3)))
        # ATTEMPT ERROR CHECKING
        self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type,self.out_type,output_value))
        rows=self.cur.fetchall()
        if len(rows)==1:
            seq=rows[0][0]
            if aa_position>len(seq): return [None]
        return [aa_position] 

    def convert_quality(self, output_value, verbosity):
        try:
            #Get Conversion Quality
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value))
            rows=self.cur.fetchall();
            inputSequence=rows[0][0]
            #Remove stop codon from transcript sequence
            if inputSequence[-3:] in stop_codons:
                inputSequence = inputSequence[:-3]
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value))
            rows=self.cur.fetchall();
            outputSequence=rows[0][0]
            #Convert input nucleotide sequence to amino acid sequence
            aa_inputSequence = ""
            for codon in self.split_sequence(inputSequence):
                if codon not in self.codon_dict:
                    aa_inputSequence+="?"
                else:
                    aa_inputSequence+=self.codon_dict[codon]
            alignment = needle_wrapper.run_stretcher(aa_inputSequence, outputSequence, sub_matrix='EBLOSUM62')
            return alignment[2]
        except IndexError:
            return 0.0


