import MySQLdb as mdb
import Node, User, Graph
import sys

class abstractPipe(object):

    #Static fields
    cur=None;
    codon_dict = {'CTT': 'L', 'ATG': 'M', 'AAG': 'K', 'AAA': 'K', 'ATC': 'I', 'AAC': 'N', 'ATA': 'I', 'AGG': 'R', 'CCT': 'P', 'ACT': 'T', 
            'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'CAT': 'H', 'AAT': 'N', 'ATT': 'I', 'CTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CAC': 'H', 
            'ACG': 'T', 'CAA': 'Q', 'AGT': 'S', 'CAG': 'Q', 'CCG': 'P', 'CCC': 'P', 'TAT': 'Y', 'GGT': 'G', 'TGT': 'C', 'CGA': 'R', 
            'CCA': 'P', 'TCT': 'S', 'GAT': 'D', 'CGG': 'R', 'TTT': 'F', 'TGC': 'C', 'GGG': 'G', 'TAG': '*', 'GGA': 'G', 'TAA': '*', 
            'GGC': 'G', 'TAC': 'Y', 'GAG': 'E', 'TCG': 'S', 'TTA': 'L', 'GAC': 'D', 'TCC': 'S', 'GAA': 'E', 'TCA': 'S', 'GCA': 'A', 
            'GTA': 'V', 'GCC': 'A', 'GTC': 'V', 'GCG': 'A', 'GTG': 'V', 'TTC': 'F', 'GTT': 'V', 'GCT': 'A', 'ACC': 'T', 'TGA': '*', 
            'TTG': 'L', 'CGT': 'R', 'TGG': 'W', 'CGC': 'R'}

    node = None
    out_type = None
    def __init__(self, input_node, out_type, verbosity, cur=None):
        self.node = input_node
        self.out_type = out_type
        self.cur=cur;
        if verbosity > 1:
            print "Source Information: Type: %s, Value: %s, Mutation: %s, Position(1-based): %s\n" %(self.node.id_type, self.node.value, self.node.mutation, self.node.position)




    ###############################################
    ###############HELPER METHODS##################
    ###############################################

    def get_sign(self, id_type, value, cur, verbosity): #Takes in an ENST and determines whether	 it is on the minus or the plus strand
        sign_type=id_type;
        if id_type=="reft" and (self.out_type=="hg19" or self.node.id_type=="hg19"): 
            sign_type="19_"+sign_type;

        cur.execute("select sign from %s_seq where %s = '%s'" %(sign_type, id_type, value))
        rows = cur.fetchall()
        if len(rows) == 0:
            print "WARNING: Could not deduce sign from the given transcript (%s). Assuming it is on (+) strand..." %(value)
            return "+"
        elif len(rows) == 1:
            sign = rows[0][0]
            return sign 

    def complement(self, seq, verbosity=0):
        comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N':'N'}
        comp_seq = ''
        for c in seq:
            comp_seq += comp_dict[c]
        return comp_seq

    def split_sequence(self, seq): 
        result = []
        sub_seq = ''
        i = 0
        while i < len(seq):
            sub_seq+=seq[i]
            if (i + 1) % 3 == 0:
                result += [sub_seq]
                sub_seq = ''
            i+=1
        return result

    #Returns a list containing tuples of the transcript's start/end cds positions (1-based)
    def get_chunks(self, transcript_type, transcript, cur):
        cur.execute("select * from %s_pos where transcript = '%s'" %(transcript_type, transcript))
        rows = cur.fetchall()
        if len(rows) == 0:
            return None
        elif len(rows) == 1:
            rows = rows[0]
            cdstart = int(rows[1])
            cdstop = int(rows[2])
            exon_starts = [int(x) for x in rows[3].split()]
            exon_stops = [int(x) for x in rows[4].split()]
            exon_starts.sort(); exon_stops.sort();
            range_list = []
            started = False; stop = False

            for i in range(len(exon_starts)):
                rang = [exon_starts[i], exon_stops[i]] #We wrap in int
                if cdstart >= exon_starts[i] and cdstart <= exon_stops[i]:
                    rang[0] = cdstart
                    started = True
                if cdstop >= exon_starts[i] and cdstop <= exon_stops[i]:
                    rang[1] = cdstop
                    stop = True
                if started:
                    range_list.append(rang)
                if stop:
                    break
            return range_list

    #Takes in a chromosome position and transcript id, and returns the relative position on the transcript
    def chunk_position(self, chrpos, transcript, cur, verb):
        #Deprecated hg19 support
        if self.node.id_type=='hg19': ranges = self.get_chunks("19_%s"%self.out_type, transcript, cur) 
        else: ranges = self.get_chunks(self.out_type, transcript, cur)

        if not ranges: return None 
        counter = 0 
        #Iterate through chunk ranges for +
        if self.get_sign(self.out_type, transcript, cur, verb) == "+":
            for r in ranges:
                if r[0] <= chrpos and chrpos <= r[1]:
                    return (counter + chrpos - r[0]) + 1
                else: counter += r[1] - r[0] + 1
        #Iterate through chunk ranges for -
        else:
            ranges.reverse()
            for r in ranges:
                if r[0] <= chrpos and chrpos <= r[1]:
                    return (counter + r[1] - chrpos) + 1
                else: counter+=r[1]-r[0]+1
            print "WARNING: Chromosome position %s is not an any of %s's CDS" %(chrpos, transcript)


    #Takes in a relative transcript position and a transcript, and returns the absolute position on the chromosome
    def dechunk_position(self, tpos, transcript, cur, verb):
        #Deprecated hg19 support
        if self.out_type=='hg19': ranges = self.get_chunks("19_%s"%self.node.id_type, transcript, cur)
        else: ranges = self.get_chunks(self.node.id_type, transcript, cur)
        if ranges == None: return None;
        original=tpos;
        tpos = tpos -1 #0-index the tpos for simpler calculations
        #Iterate through chunks ranges for +
        if self.get_sign(self.node.id_type, transcript, cur, verb) == '+':
            for r in ranges:
                if 0 <= tpos and tpos <= (r[1]-r[0]):
                    return r[0] + tpos 
                else:
                    tpos = tpos - (r[1]-r[0]) - 1

        else:
            ranges.reverse()
            for r in ranges: 
                if 0 <= tpos and tpos <= (r[1]-r[0]):
                    return r[1]-tpos
                else:
                    tpos = tpos - (r[1]-r[0])-1
        print "WARNING: Unable to Dechunk %s's position:%s"%(transcript, original)
        return None



    ###############################################
    ###############PRIMARY METHODS#################
    ###############################################

    def convert_quality(self, output_value, verbosity):
        #Override in child function
        return -1

    def convert_value(self, verbosity):
        value = self.node.value
        from_type = self.node.id_type
        to_type = self.out_type


        #PDB EDGE CASE #1: ASSUME CHAIN IS UPPERCASE UNLESS THERE EXISTS A LOWER CASE VERSION OF CHAIN
        if from_type=="pdbc" and value[-1].islower():
            self.cur.execute("select * from pdb_uniprot where pdb='%s'"%value);
            rows=self.cur.fetchall();
            if len(rows)==0: value=value[:-1]+value[-1].upper();
            self.node.value=value;


        if from_type=="pdbc": from_type=from_type.replace("pdbc","pdb")
        if to_type=="pdbc": to_type=to_type.replace("pdbc","pdb");
        table_name="%s_%s"%(from_type,to_type);


        #PDB EDGE CASE #2: NO PDBC TABLE, SO REPLACE PDBC IN TABLE NAME WITH PDB
        if "pdbc" in table_name: table_name=table_name.replace("pdbc","pdb")

        #PDB EDGE CASE #3: CHAIN SOURCE NODE FIELD
        if self.node.id_type=="pdbc" and self.out_type=="uniprot":
            self.node.chain_source=self.node.value[-1];

        #SPECIAL CASE: If None position is given when traversing through THROUGH (not to or from) a chromosomal node
        if self.node.position==None and self.out_type=='hg38':
            self.node.narrowQueryPosition=self.dechunk_position(1, self.node.value, self.cur, 0);
        self.cur.execute("select %s from %s where %s = '%s'" %(to_type, table_name, from_type, self.node.value))
        result = self.cur.fetchall()
        if len(result) == 0: #No results were found
            return [None]
        elif len(result) == 1:
            #DBSNP EDGE HANDLING	
            if self.node.id_type in ['ensp','uniprot','refp'] and self.out_type in ['enst','reft']: self.node.transcripts=[result[0][0].split(),self.out_type]
            elif self.node.id_type in ['enst','reft'] and self.node.transcripts==None: self.node.transcripts=[[self.node.value],self.node.id_type]
            return result[0][0].split()

    def convert_mutation(self, output_value, verbosity):
        #Overriden in subclass. Uses input node and output value to map the input mutation to its output mutation
        return

    def convert_position(self, output_value, verbosity):
        #Overriden in subclass. Uses input node and output value to map the input position to its output position.
        return

    # Gets the source of the output_value, e.g, Trembl vs Swissprot. Currently only supported for uniprot identifiers
    def convert_source(self, output_value):
        # cur=self.con.cursor();
        if self.out_type!="uniprot": return None;
        if output_value==None: return None;
        self.cur.execute("select source from uniprot_source where uniprot='%s'"%(output_value.split("-")[0]))
        rows=self.cur.fetchall()
        if len(rows)==0: return None;
        return rows[0][0]


    def output(self, verbosity):
        if verbosity > 1:
            print "Mapping identifier..."
            print "====================="
        output_value_list = self.convert_value(verbosity)
        if verbosity > 1:
            print "Output identifiers: %s" %output_value_list
        node_list = []
        counter = 0
        for v in output_value_list:
            local_node_list = []
            # Calculate conversion quality
            if self.node.quality != -2:
                quality = self.convert_quality(v, verbosity)
            else:
                quality = -2
            # Calculating Source
            source=self.convert_source(v);
            if verbosity > 1:
                s1 = "\tMapping features onto %s..." %v
                s2 = "\t"
                for i in range(len(s1)): s2 += "="
                if verbosity > 1:
                    print s1
                    print s2
            if v != None:
                # EXPLICIT DBSNP HANDLING
                if self.out_type=="dbsnp":
                    position_list = self.convert_position(v, verbosity);
                    if verbosity > 1:  print "\tOutput Positions: %s" %position_list
                    output_mutations = self.convert_mutation(v, verbosity);
                    if verbosity > 1: print "\tOutput Mutations: %s" %output_mutations
                elif self.node.position==None: #If the user didn't input a position, then position/muation will be none
                    output_mutations = [None]
                    position_list = [None]

                elif self.node.mutation == None:
                    output_mutations=[None]
                    position_list = self.convert_position(v, verbosity)
                    if verbosity > 1: print "\tOutput Positions: %s" %position_list
                else:
                    output_mutations = self.convert_mutation(v, verbosity)
                    position_list = self.convert_position(v, verbosity)
                    if verbosity > 1: print "\tOutput Positions: %s" %position_list
                    if verbosity > 1: print "\tOutput Mutations: %s" %output_mutations

                dbsnp_edge=self.node.id_type=="dbsnp" and (self.out_type=="hg38" or self.out_type=="hg19"); #reqs for dbsnp edge case
                # IF MUTATIONS AND POSITIONS
                if output_mutations[0]:
                    for i, m in enumerate(output_mutations):
                        if position_list[i]==None: m = None;
                        # PDB EDGE CASE: INPUT POSITION BUT NO OUTPUT POSITIONS
                        if ("pdb" in self.node.id_type or "pdb" in self.out_type) and position_list[i]==None and self.node.position:
                            continue; 
                        snp_source= "%s:%s/%s"%(v,position_list[i],m) if dbsnp_edge else self.node.snp_source;
                        newNode=Node.Node(self.out_type, v, m, position_list[i], source,snp_source,wt_source=self.node.wt_source, chain_source=self.node.chain_source);
                        newNode.transcripts=self.node.transcripts;
                        node_list.append(newNode)
                        local_node_list.append(newNode)

                else: #If no output mutations, but there are positions
                    for p in position_list:
                        pos=p; mut=None;
                        # PDB EDGE CASE: INPUT POSITION BUT NO OUTPUT POSITIONS
                        if ("pdb" in self.node.id_type or "pdb" in self.out_type) and pos==None and self.node.position:
                            continue; 
                        newNode=Node.Node(self.out_type, v, mut, pos,source,self.node.snp_source,wt_source=self.node.wt_source,chain_source=self.node.chain_source);
                        newNode.narrowQueryPosition=self.node.narrowQueryPosition;
                        newNode.transcripts=self.node.transcripts;
                        node_list.append(newNode)
                        local_node_list.append(newNode)
                #Average quality of newNode with previous node in traversal
                for n in local_node_list:
                    if self.node.quality == -1 or self.node.quality == -2:
                        n.quality = quality
                    elif n.quality == -1:
                        n.quality = quality
                    else:
                        print self.node.value, n.value, self.node.quality
                        n.quality = (self.node.quality + quality) / 2.0

            counter+=1

        return node_list 
