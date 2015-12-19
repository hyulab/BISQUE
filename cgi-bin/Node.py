class Node:
    #Fields
    id_type = ''
    value = ''
    mutation = ''
    position = 0
    quality = -1 #Historical alignment quality. -1 if not applicable
    narrowQueryPosition=None;
    startNode = False; #True if node is the first node in the total traversal
    source = None; #Useful in some cases. For example, it can tell whether a UniProt is from the TrEmbl or Swissprot DB
    version_number = None; #Version number of identifier, if applicable.

    transcripts=None; #For dbSNP purposes
    snp_source=None; #For dbSNP's, should contain the chr#:pos information
    wt_source=None; #For webserver purposes
    chain_source=None; #Webserver purposes (display PDB chain source if no chain supplied)

    #Constructor
    def __init__ (self, input_id_type = None, input_value = None, input_mutation = None, input_position = None, source=None, snp_source=None, wt_source=None,chain_source=None):
        self.id_type = input_id_type
        self.value = input_value
        self.mutation = input_mutation
        self.position = input_position
        self.source=source
        self.snp_source=snp_source
        self.wt_source=wt_source
        self.chain_source=chain_source

    # toString override
    def __str__(self):
        return "ID:%s\tType:%s\tPosition:%s\tMutation:%s"%(self.value,self.id_type,str(self.position),self.mutation);

    def set_version_number(v):
        self.version_number=v;
    def get_version_number():
        return version_number;

