import re
import transcriptOperations as tOp


"""This file contains various helper functions which are performed given identifiers
and any other relevant parameters"""
comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N':'N'}

#Given an identifier, determine if the identifier is canonical or not
def is_canonical(id):
    pure_canonical = len(id.split("-")) == 1
    impure_canonical = len(id.split("-")) > 1 and int(id.split("-")[-1]) == 1
    return pure_canonical or impure_canonical

#Given an identifier, return the identifier's wild type
def get_wild_type(id,type,position,cur,uniprot_pos=None):
    if type=="ensg" or type=="dbsnp" or not position: return None;
    elif "pdb" in type:
        position=uniprot_pos;
        if not position: return None;
        cur.execute("select uniprot from pdb_uniprot where pdb='%s'"%id)
        rows=cur.fetchall()
        if len(rows)==0: return None
        uniprot=rows[0][0];
        cur.execute("select seq from uniprot_seq where uniprot='%s'"%uniprot)
        rows=cur.fetchall()
        if len(rows)==0: return None
        seq=rows[0][0];
        if position>len(seq): return None
        return seq[position-1];
    elif type=="hg19" or type=="hg38":
        rows=None;
        enst_used=True;
        version="19_" if (type=="hg19") else "";
        #cur.execute("select * from %spos_enst where cdstart<=%i and cdstop>=%i and chr='%s'"%(version,position,position,id))
        cur.execute("select * from %spos_enst where position='%s'"%(version,str(position)+"+"+id))
        rows=cur.fetchall();
        if len(rows) == 0: 
            return None;
        transcripts = rows[0][-1].split("\t")
        for t in transcripts:
            transcript_pos=tOp.chunk_position(position, t, version+"enst", cur)
            if not transcript_pos: continue;
            cur.execute("select seq,sign from enst_seq where enst='%s'"%t)
            rows=cur.fetchall()
            if len(rows)==0: continue;
            seq=rows[0][0];
            sign=rows[0][1];
            try:
                if sign=="+":
                    return seq[transcript_pos-1]
                return comp_dict[seq[transcript_pos-1]]
            except:
                pass

        return None;
    # try:
    cur.execute("select seq from %s_seq where %s='%s'"%(type,type,id));
    rows=cur.fetchall();
    if len(rows)==0: return None;
    try:
        seq=rows[0][0];
        return seq[position-1];
    except: return None;

#Given a gene name identifier, return the uniprot associated with the gene name
def geneNameToUniprot(gName, cur):
    if re.match(r'^[A-Z0-9-]+$|^C[0-9XY]+orf[0-9]+$',gName, re.IGNORECASE):
        cur.execute("select uniprot from geneName_uniprot where geneName='%s'"%gName)
        rows = cur.fetchall();
        try:return rows[0][0]
        except: return None;



#Given an identifier, position and mutation, attempt to correct the wild type if it is incorrect
def correctWT(inputId, inputType, position, mutation, cur): #For non-ensg and non-chromosome
    cur.execute("select seq from %s_seq where %s='%s'"%(inputType,inputType,inputId));
    rows=cur.fetchall();
    if len(rows)==0:
        print "WARNING: Could not deduce sequence from given %s. Continuing without WT error handling..." %(inputType);
        return mutation;
    seq=rows[0][0]
    if len(seq)>0 and seq[position-1]!=mutation[0]:
        print "WARNING: WT Mismatch(%s)--User WT base (%s) does not match actual WT base (%s)" %(seq[position-1],mutation[0],seq[position-1]);
        correctedWildType=seq[position-1];
        return "%s%s"%(seq[position-1],mutation[-1])
    return mutation 


#This is only relevant for refSeq identifiers. It returns the correct version number appended to the given id.
def correct_version_number(id,type, cur):
    try:
        if type=="reft":
            cur.execute("select reft from reft_hg38 where reft like '%s.%%'"%(id.split(".")[0]));
            rows=cur.fetchall();
            return rows[0][0];
        elif type=="refp":
            cur.execute("select refp from refp_reft where refp like '%s.%%'"%(id.split(".")[0]));
            rows=cur.fetchall();
            return rows[0][0];
    #No correction found
    except:
        return None
