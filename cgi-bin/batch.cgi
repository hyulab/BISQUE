#!/usr/bin/env python 
print "Content-type: application/json"
print


#########
#MODULES#
#########
import re 
import cgi
import parse
import sys
from os import system, path, devnull 
import bisque, User
import MySQLdb as mdb 
import cgitb
import json
import StringIO
cgitb.enable()

root_directory = path.abspath(__file__ + "/../../")


abbreviationToCode={
        'ala': 'A',
        'arg': 'R',
        'asn': 'N',
        'asp': 'D',
        'cys': 'C',
        'glu': 'E',
        'gln': 'Q',
        'gly': 'G',
        'his': 'H',
        'ile': 'I',
        'leu': 'L',
        'lys': 'K',
        'met': 'M',
        'phe': 'F',
        'pro': 'P',
        'ser': 'S',
        'thr': 'T',
        'trp': 'W',
        'tyr': 'Y',
        'val': 'V'
        }

################
#SQL CONNECTION#
################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur = con.cursor()

###########################
#EXECUTION WITH INPUT DATA#
###########################
data = cgi.FieldStorage();
input_array = data["input"].value.split('\n'); output = data.getvalue('output');
quality = True if data.getvalue("quality") == "true" else False
swissprot = True if data.getvalue("swissprot") == "true" else False
canonical = True if data.getvalue("canonical") == "true" else False
vcf = True if data.getvalue("vcf") == "true" else False
try: input_array.remove("");
except: pass;
results_array = []
processedElements=[] #This prevents the same processing element from being processed more than once
errorNodes=[]

#JSON Output
json_output = []
for inpt in input_array:
    if inpt.strip()[0] == "#": continue
    #Extract id, position and mutation from line
    parsed_line = parse.parse_line(inpt, vcf)
    if parsed_line == None: continue;
    (id, position, mutation) = parsed_line
    #Determine type of identifier
    parsedInput = parse.parse_identifier(id, cur)
    type = parsedInput["type"]
    id = parsedInput["formatted_id"]
    referenceId = parsedInput["reference"]
    hg19_thru=False
    # DEPRECATED HG19 SUPPORT
    if data.getvalue("build")=="old":
        if type=="hg38": type="hg19";
        elif type=="dbsnp" or output=="dbsnp": hg19_thru=True;

    if type!="pdb": id = id.upper();

    #Convert inputs using bisque
    try:
        if type: #If input is valid
            processingElement=str(id).lower()+str(position)+str(mutation).lower();
            if processingElement not in processedElements: #Make sure not to process same element more than once if duplicates are given as input
                source=None;
                if type=="uniprot":
                    cur.execute("select source from uniprot_source where uniprot='%s'"%id.split("-")[0]);
                    rows=cur.fetchall();
                    if len(rows)>0: source=rows[0][0]
                with con:
                    old_stdout = sys.stdout;
                    sys.stdout = mystdout = StringIO.StringIO();
                    results = None
                    my_xcds=None
                    wt_error = None
                    if data.getvalue("xcds")=="y": my_xcds=True;
                    elif data.getvalue("xcds")=="n": my_xcds=False;
                    if position:
                        results = bisque.convert(id=id, type=type, output=output, mutation=mutation, position=int(position), thru=hg19_thru, xcds=my_xcds, quality=quality, swissprot=swissprot, canonical=canonical)
                    else:
                        results = bisque.convert(id=id, type=type, output=output, mutation=mutation, position=None, thru=hg19_thru, xcds=my_xcds, quality=quality, swissprot=swissprot, canonical=canonical)
                    sys.stdout = old_stdout
                    mismatchPos=re.search('WT Mismatch',mystdout.getvalue())
                    if mismatchPos != None: 
                        wt_error = mystdout.getvalue()[mismatchPos.end()+1:mismatchPos.end()+2]
                    if mutation: 
                        mutation=mutation.upper(); #Make output look nicer
                        if len(mutation)==2: mutation="%s>%s"%(mutation[0],mutation[-1])
                    #Add correct version number to input id if reft or refp
                    if type=="reft" or type=="refp" and len(results)>0: id=results[0]["source_version"]; 
                    #Add JSON result entry
                    for result in results:
                        json_result = result
                        if wt_error:
                            json_result["wt_error"] = wt_error
                        if referenceId:
                            json_result["reference_id"] = referenceId
                        json_result["source_id"] = id
                        json_result["source_mutation"] = mutation
                        json_result["source_position"] = position
                        json_result["input_source"] = source
                        json_result["output_type"] = output
                        json_output.append(result)
                processedElements.append(processingElement) #Update elements processed
    except Exception as e: 
        json_output.append({"problem":str(e)})

print(json.JSONEncoder().encode(json_output))





