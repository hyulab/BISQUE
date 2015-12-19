import MySQLdb as mdb
import sys 
import os 
import transcriptOperations as tops
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
from Pipe import *



class concretePipe(abstractPipe):

    destroyPipe=False; #Pipe self-destruct for chromosomes. This is only done in a ver special case--if the user gives a position
    #and the position doesn't map properly to a transcript, then drop the position AND value, so as not to get the output of the
    #entire chromosome

    grch38Valid = None;


    def __init__(self, input_node, output_type, verbosity,cur):
        abstractPipe.__init__(self,input_node, output_type, verbosity,cur)

    def convert_value(self, verbosity):
        #Convert_value is overriden here. Chromosomes output SO many ENST's, and if the user inputs a specific position,
        #we only want to return the enst at that position.
        temp=self.node.position;
        if self.node.narrowQueryPosition!=None: self.node.position=self.node.narrowQueryPosition;
        if self.node.position != None:
            results = []
            version="19_" if self.node.id_type=="hg19" else "";
            cur=self.cur;
            try:
                cur.execute("select * from %spos_%s where position = '%s'"%(version, self.out_type, str(self.node.position) + "+" + self.node.value))
                rows = cur.fetchall()
                if len(rows) == 0:
                    return [None]
                results = rows[0][-1].split("\t")
            except: 
                cur.execute("select * from %spos_%s where cdstart <= %d and cdstop >= %d"%(version, self.out_type, self.node.position, self.node.position))
                rows=cur.fetchall();
                if len(rows) == 0: return [None]
                transcripts = []
                for row in rows:
                    data=row[3].split("\t"); transcripts+=data;
                # print transcripts
                for t in transcripts:
                    in_range=False;
                    chunks = self.get_chunks("%s%s"%(version,self.out_type), t, cur)
                    if chunks==None: continue;
                    for rng in chunks:
                        if self.node.position>=rng[0] and self.node.position<=rng[1]:
                            results.append(t)
                            break;



            #Reset narrowQuery changes
            self.node.position=temp; self.node.narrowQueryPosition=None #We are done narrowing query, so to preven it from 
            #passing to further pipes, we reset it back to -1 
            return results if len(results) > 0 else [None]

        else:
            return super(concretePipe, self).convert_value(verbosity)





    def convert_mutation(self, output_value, verbosity):
        cur=self.cur
        sign = self.get_sign(self.out_type, output_value, cur, verbosity)
        #Only perform WT check if this is the inserted node. 
        #This saves time and helps to reduce errors from database inconsistencies
        try:
            chunked_position = self.chunk_position(self.node.position, output_value, cur, verbosity)
            cur.execute("select seq from %s_seq where %s='%s'" %(self.out_type, self.out_type, output_value))
            rows = cur.fetchall()
            if len(rows)==0: print "WARNING: Unable to check for valid WT. Continuing without error handling..."
            else:
                seq = [x.upper() for x in rows[0][0]];
                if len(seq)>0: 
                    wild_type = seq[chunked_position-1];
                    if sign=="-": wild_type = self.complement(wild_type);
                    if self.node.startNode and wild_type!=self.node.mutation[0] and seq[0]!="N": #ATG case to handle bad Ensemlb data...
                        print "WARNING: WT Mismatch(%s)--User WT base (%s) does not match actual WT base (%s)" %(wild_type, self.node.mutation[0], wild_type)
                        self.node.mutation = '%s%s'%(wild_type,self.node.mutation[-1])
                    elif wild_type != self.node.mutation[0] and seq[0] != "N":
                        self.node.mutation = "%s?"%(wild_type)

        except: pass;	


        #Converting mutation
        if sign == "+":
            output_mutation = self.node.mutation
        elif sign == "-":
            output_mutation = self.complement(self.node.mutation, verbosity)

        return [output_mutation]

    def convert_position(self, output_value, verbosity):
        cur=self.cur;

        #Chunking position (also takes sign into account)
        chunked_position = self.chunk_position(self.node.position, output_value, cur, verbosity)
        #chunked_position = None
        #if self.node.id_type == "hg38":
        #    chunked_position = tops.chunk_position(self.node.position, output_value, cur)
        #elif self.node.id_type == "hg19":
        #    chunked_position = tops.chunk_ncds_position(self.node.position, output_value, cur)

        # IF MUTATION IS NONE AND SOURCE WILD TYPE IS NONE, THEN SET SOURCE WILD TYPE (FOR WEB SERVER)
        if chunked_position and not self.node.mutation:
            cur.execute("select seq,sign from %s_seq where %s='%s'"%(self.out_type,self.out_type,output_value));
            rows=cur.fetchall();
            if len(rows)>0:
                seq=rows[0][0];
                sign=rows[0][1];
                try:
                    self.node.wt_source=seq[chunked_position-1];
                except: 
                    return [None]
                if sign=="-": self.node.wt_source=self.complement(seq[chunked_position-1]);

        return [chunked_position]
