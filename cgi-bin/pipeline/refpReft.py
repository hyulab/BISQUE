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

    output_positions = []

    def __init__(self, input_node, output_type, verbosity,cur):
        abstractPipe.__init__(self,input_node, output_type, verbosity,cur)

    def convert_mutation(self, output_value, verbosity):
        #Converting mutation
        cur=self.cur;
        possible_wt_codons = []
        possible_mut_codons = []
        for codon in self.codon_dict:
            if self.codon_dict[codon] == self.node.mutation[0]: possible_wt_codons.append(codon);
            if self.codon_dict[codon] == self.node.mutation[-1]: possible_mut_codons.append(codon);
        cur.execute("select seq from %s_seq where %s = '%s'" %(self.out_type, self.out_type, output_value))
        rows = cur.fetchall()
        if len(rows) == 0:
            print "WARNING: Could not deduce sequence from %s. Returning None..." %(self.out_type)
            return [None]
        elif len(rows) == 1:
            seq = rows[0][0]
            codon_list = self.split_sequence(seq)
            try: 
                wt_codon = codon_list[self.node.position-1]
            except: 
                print "WARNING: Position %s is out of range! The transcript's codon list is only %s codons long..." %(self.node.position, len(codon_list))
                return [None]
            if wt_codon not in possible_wt_codons:
                print "WARNING: Wild Type codon does not match ANY possible WT codons. Returning None..."
                return [None] 
            valid_mutations = []
            for c in possible_mut_codons:
                if c[0] == wt_codon[0] and c[1] == wt_codon[1]:
                    #if verbosity > 1: print "Succesful output mutation!: %s%s" %(wt_codon[2], c[2])
                    self.output_positions.append((self.node.position * 3) + 0 )
                    valid_mutations.append("%s%s" %(wt_codon[2], c[2]))

                elif c[1] == wt_codon[1] and c[2] == wt_codon[2]:
                    #if verbosity > 1: print "Succesful output mutation!: %s%s" %(wt_codon[0], c[0])
                    self.output_positions.append((self.node.position * 3) - 2 )
                    valid_mutations.append("%s%s" %(wt_codon[0], c[0]))
                elif c[0] == wt_codon[0] and c[2] == wt_codon[2]:
                    #if verbosity > 1: print "Succesful output mutation!: %s%s" %(wt_codon[1], c[1])
                    self.output_positions.append((self.node.position * 3) - 1)
                    valid_mutations.append("%s%s" %(wt_codon[1], c[1]))


                else:
                    self.output_position = None
            #Shows warning so user knows their output mutation is impossible for a single nucleotide mutation 
            if len(valid_mutations) == 0: 
                print "WARNING: WT codon (%s) can't be mutated into any possible mutated codons (%s)" %(wt_codon, possible_mut_codons);
                return [None]

            if len(valid_mutations) > 0:
                return valid_mutations 
            elif len(valid_mutations) == 0: #If it is empty, we return [None], showing that this value has NO valid mutations
                self.output_positions.append(None)
                return [None]

    def convert_position(self, output_value, verbosity):
        cur=self.cur;
        cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type,self.node.id_type,self.node.value))
        rows=cur.fetchall();
        if len(rows)>0:
            seq=rows[0][0];
            if self.node.position>len(seq): return [None];

        if len(self.output_positions) > 0:
            start = (self.node.position-1)*3+1; end=(self.node.position)*3+1;
            return self.output_positions
        elif self.node.position == None:
            return [None]
        else:
            start = (self.node.position-1)*3+1; end=(self.node.position)*3+1;
            return [i for i in range(start, end)]

    def convert_quality(self, output_value, verbosity):
        try:
            #Get Conversion Quality
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.node.id_type, self.node.id_type, self.node.value))
            rows=self.cur.fetchall();
            inputSequence=rows[0][0]
            self.cur.execute("select seq from %s_seq where %s='%s'"%(self.out_type, self.out_type, output_value))
            rows=self.cur.fetchall();
            outputSequence=rows[0][0]
            #Convert input nucleotide sequence to amino acid sequence
            aa_outputSequence = ""
            for codon in self.split_sequence(outputSequence):
                if codon not in self.codon_dict:
                    aa_outputSequence+="?"
                else:
                    aa_outputSequence+=self.codon_dict[codon]
            alignment = needle_wrapper.run_stretcher(inputSequence, aa_outputSequence, sub_matrix='EBLOSUM62')

            return alignment[2]
        except IndexError:
            return 0.0


