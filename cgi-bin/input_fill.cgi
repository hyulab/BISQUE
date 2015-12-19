#!/usr/bin/env python 
print "Content-type: application/json"
print

import cgi
import sys
import os
import MySQLdb as mdb
import User
import bisque 
import transcriptOperations as top
import json
import StringIO
import cgitb
import re
from os import path 

cgitb.enable()

root_directory = path.abspath(__file__ + "/../../")



codon_dict = {'CTT': 'L', 'ATG': 'M', 'AAG': 'K', 'AAA': 'K', 'ATC': 'I', 'AAC': 'N', 'ATA': 'I', 'AGG': 'R', 'CCT': 'P', 'ACT': 'T', 
        'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'CAT': 'H', 'AAT': 'N', 'ATT': 'I', 'CTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CAC': 'H', 
        'ACG': 'T', 'CAA': 'Q', 'AGT': 'S', 'CAG': 'Q', 'CCG': 'P', 'CCC': 'P', 'TAT': 'Y', 'GGT': 'G', 'TGT': 'C', 'CGA': 'R', 
        'CCA': 'P', 'TCT': 'S', 'GAT': 'D', 'CGG': 'R', 'TTT': 'F', 'TGC': 'C', 'GGG': 'G', 'TAG': '*', 'GGA': 'G', 'TAA': '*', 
        'GGC': 'G', 'TAC': 'Y', 'GAG': 'E', 'TCG': 'S', 'TTA': 'L', 'GAC': 'D', 'TCC': 'S', 'GAA': 'E', 'TCA': 'S', 'GCA': 'A', 
        'GTA': 'V', 'GCC': 'A', 'GTC': 'V', 'GCG': 'A', 'GTG': 'V', 'TTC': 'F', 'GTT': 'V', 'GCT': 'A', 'ACC': 'T', 'TGA': '*', 
        'TTG': 'L', 'CGT': 'R', 'TGG': 'W', 'CGC': 'R'}



################
#SQL CONNECTION#
################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur=con.cursor();

###########################
#EXECUTION WITH INPUT DATA#
###########################
data = cgi.FieldStorage()
output = json.loads(data.getvalue("output"));
batch = data.getvalue("batch");
TRANSCRIPT_THRESHOLD = 6000
PROTEIN_THRESHOLD = 2000

source_seq = None
with con:	
    for o in output:
        try:
            check_id = o["source_id"] if "reference_id" not in o else o["reference_id"]
            output_type=None
            if re.match(r'^ENST[0-9]{11,11}', str(check_id), re.IGNORECASE):
                output_type = "enst"
            elif re.match(r'^ENSP[0-9]{11,11}', str(check_id), re.IGNORECASE):
                output_type = "ensp"
            elif re.match(r'^ENSG[0-9]{11,11}', str(check_id), re.IGNORECASE):
                output_type = "ensg"
            elif re.match(r'^NP_[0-9]{1,20}.*[0-9]*', str(check_id), re.IGNORECASE):
                output_type = "refp"
            elif re.match(r'^[N,X][M]_[0-9]{5,9}.*[0-9]*', str(check_id), re.IGNORECASE):
                output_type = 'reft'
            elif re.match(r'^[A-Z]\w\w\w\w\d(-[0-9])*', str(check_id), re.IGNORECASE):
                output_type = "uniprot"
            else:
                output_type = "pdb"
            #Fetch source ID sequence. If too long, skip to end of program, and do not do reverse mappings
            if not source_seq:
                cur.execute("select seq from %s_seq where %s='%s'"%(output_type, output_type, check_id))
                rows = cur.fetchall()
                source_seq = rows[0][0]
                if output_type in ["ensp", "refp", "uniprot"] and len(source_seq) > PROTEIN_THRESHOLD:
                    break
                elif len(source_seq) >= TRANSCRIPT_THRESHOLD:
                    break

            chrom=o["position"].split(":")[0];
            pos=int(o["position"].split(":")[1]);

            if output_type:
                chrom_type="hg38";
                if data.getvalue("build")=="old":chrom_type="hg19"; 
                reload(bisque)
                old_stdout = sys.stdout;
                f = open(os.devnull, 'w');
                sys.stdout = f;

                results=bisque.convert(id=chrom,type=chrom_type,position=pos,mutation=o["mutation"],output=output_type);
                sys.stdout = old_stdout
                if not o["source_position"] or not o["source_mutation"]:
                    for result in results:
                        o["source_mutation"] = "%s-%s"%(check_id, result["value"])
                        if result["value"]==check_id:
                            o["source_mutation"]=result["mutation"];
                            if len(o["source_mutation"])==2: o["source_mutation"]="%s>%s"%(o["source_mutation"][0],o["source_mutation"][-1]);
                            o["source_position"]=result["position"];
                            break;
        except Exception as e:
            pass;

print(json.JSONEncoder().encode(output))





