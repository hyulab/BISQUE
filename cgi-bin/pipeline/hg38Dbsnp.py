import MySQLdb as mdb
import sys 
import os 
import itertools
root_directory = os.path.abspath(__file__ + "/../../")
sys.path.append(root_directory)
sys.path.append('%s/pipeline' %(root_directory))
import Node
import transcriptOperations as top
from Pipe import *


output_dict={}
BATCH_LIMIT = 100

class concretePipe(abstractPipe):

    def __init__(self,input_node,output_type,verbosity,cur):
        abstractPipe.__init__(self,input_node,output_type,verbosity,cur);


    def convert_value(self,verbosity):
        rows = []
        #MUTATION AND POSITION
        if self.node.mutation and self.node.position:
            unique_id=self.node.value[3:]+","+str(self.node.position)+","+self.node.mutation[0]+","+self.node.mutation[-1];
            if self.node.id_type=="hg19": self.cur.execute("select * from 19_pos_dbSNP where id='%s'"%unique_id);
            else: self.cur.execute("select * from pos_dbSNP where id='%s'"%unique_id);

        #POSITION
        elif self.node.position:
            mutations=["AT","AG","AC","TA","TG","TC","GA","GT","GC","CA","CT","CG"]
            unique_id=[self.node.value[3:]+","+str(self.node.position)+","+x[0]+","+x[-1] for x in mutations];
            query="";
            for i in range(len(unique_id)):
                if i==len(unique_id)-1: query+="id='%s'"%unique_id[i];
                else: query+="id='%s' or "%unique_id[i];

            if self.node.id_type=="hg19": self.cur.execute("select * from 19_pos_dbSNP where %s"%query);
            else: self.cur.execute("select * from pos_dbSNP where %s"%query);
        #NO MUTATION AND NO POSITION
        else:
            mutations=["AT","AG","AC","TA","TG","TC","GA","GT","GC","CA","CT","CG"]
            for t in self.node.transcripts[0]:
                chunks = []
                positions = []
                try:
                    if self.node.id_type=="hg19": chunks+=top.get_chunks("19_" + self.node.transcripts[1], t, self.cur);
                    else: chunks+=top.get_chunks(self.node.transcripts[1], t, self.cur);

                except:
                    pass
            for c in chunks:
                positions+=range(c[0],c[1]+1)
            #Partition positions for manageable SQL queries
            partitioned_positions = []
            current_partition = []
            for i,pos in enumerate(positions):
                current_partition.append(pos)
                if i % BATCH_LIMIT == 0 or i == len(positions) - 1:
                    partitioned_positions.append(current_partition)
                    current_partition = []
            #Produce list of batch queries
            batch_queries = []
            batch_query=""
            for partition in partitioned_positions:
                for i,pos in enumerate(partition):
                    id_list = [self.node.value[3:]+","+str(pos)+","+x[0]+","+x[-1] for x in mutations]
                    for a,id in enumerate(id_list):
                        if i==len(partition)-1 and a==len(id_list)-1: 
                            batch_query+="id='%s'"%id;
                        else: batch_query+="id='%s' or "%id;
                #If at end of partition, push batch query
                batch_queries.append(batch_query)
                batch_query = ""
            #Execute and aggregate batch queries
            for q in batch_queries:
                if self.node.id_type=="hg19": self.cur.execute("select * from 19_pos_dbSNP where %s"%(q));
                else: 
                    self.cur.execute("select * from pos_dbSNP where %s"%q);
                try: 
                    batch_result = self.cur.fetchall()
                    rows += batch_result
                except: pass

        if len(rows) == 0:
            rows=self.cur.fetchall();
        if len(rows)==0: return [None];
        results=[]
        for x in rows:
            dbsnp=x[1]
            if dbsnp not in output_dict: output_dict[dbsnp]={"position":[],"mutation":[]} 
            output_dict[dbsnp]["position"].append("chr%s:%s"%(x[0].split(',')[0],x[0].split(',')[1]))
            output_dict[dbsnp]["mutation"].append("%s%s"%(x[0].split(',')[2],x[0].split(',')[3]))
            results.append(dbsnp);
        return results


    def convert_mutation(self,output_value,verbosity):
        try:return output_dict[output_value]["mutation"]
        except:return [None]

    def convert_position(self,output_value,verbosity):
        try:return output_dict[output_value]["position"]
        except:return [None]

		
