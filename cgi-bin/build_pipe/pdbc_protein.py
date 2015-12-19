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

    def convert_position(self,output_value,verbosity):
        cur=self.cur;
        cur.execute("select * from pdb_pos where pdb='%s'"%(self.node.value+"-" + output_value));
        rows=cur.fetchall();
        if len(rows)==0: return [None];
        rows=rows[0];
        pdb_ranges=rows[2].split(',');
        uniprot_ranges=rows[1].split(',');
        for i,ran in enumerate(pdb_ranges):
            if len(ran.split("-"))>1:
                int_ran=[int(x) for x in ran.split("-")];
                if self.node.position in range(int_ran[0],int_ran[1]+1):
                    int_uniprot_ran=[int(x) for x in uniprot_ranges[i].split("-")];
                    return [self.node.position-int_ran[0]+int_uniprot_ran[0]];
            else:
                if self.node.position == int(ran): return [int(uniprot_ranges[i])];

        return [None];

    def convert_mutation(self,output_value,verbosity):
        mapped_pos=self.convert_position(output_value,verbosity)[0];
        # WT HANDLING
        try:
            cur=self.cur;
            cur.execute("select seq from uniprot_seq where uniprot='%s'"%output_value);
            rows=cur.fetchall();
            if len(rows)>0:
                seq=rows[0][0];
                if seq[mapped_pos-1]!=self.node.mutation[0]: 
                    print "WARNING: WT Mismatch(%s)--User WT base (%s) does not match actual WT base (%s)" %(seq[mapped_pos-1], self.node.mutation[0], seq[mapped_pos-1])
                    self.node.mutation="%s%s"%(seq[mapped_pos-1],self.node.mutation[-1])
        except: pass
        return [self.node.mutation]

    def convert_quality(self, output_value, verbosity):
        #Get PDB/Uniprot residues
        cur = self.cur
        cur.execute("select uniprot_pos from pdb_pos where pdb='%s-%s'"%(self.node.value, output_value))
        rows = cur.fetchall()
        if len(rows) == 0:
            return -1
        uniprot_ranges = []
        for r in rows[0][0].split(","):
            r = r.split("-")
            if len(r) == 2:
                uniprot_ranges.append([int(r[0]), int(r[1])])
            else:
                uniprot_ranges.append([int(r[0])])
        #Get Uniprot Sequence for length
        cur.execute("select seq from uniprot_seq where uniprot='%s'"%output_value)
        rows = cur.fetchall()
        if len(rows) == 0:
            return -1
        seq = rows[0][0]
        #Return fraction of residues compared to entire sequence
        accumulator = 0
        for r in uniprot_ranges:
            if len(r) == 2:
                accumulator += (r[1] - r[0] + 1)
            else:
                accumulator += 1
        return float(accumulator) / float(len(seq))






