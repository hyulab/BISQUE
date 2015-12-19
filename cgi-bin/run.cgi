#!/usr/bin/env python 
print "Content-type: application/json"
print



#########
#MODULES#
#########
import re 
import cgi
import sys
import parse
from os import system, path, devnull 
import bisque, User
import MySQLdb as mdb 
import cgitb
import json
import StringIO
cgitb.enable()

root_directory = path.abspath(__file__ + "/../../")

################
#SQL CONNECTION#
################
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur = con.cursor()

###########################
#EXECUTION WITH INPUT DATA#
###########################
data = cgi.FieldStorage()
inpt = data.getvalue("id"); mutation = data.getvalue("mutation"); position = data.getvalue("position"); output = data.getvalue("output")
build = data.getvalue("build")
quality = True if (data.getvalue("quality") == "true" or data.getvalue("quality") == "y") else False
swissprot = True if (data.getvalue("swissprot") == "true" or data.getvalue("swissprot") == "y") else False
canonical = True if (data.getvalue("canonical") == "true" or data.getvalue("canonical") == "y") else False

#Extra URL query options#
#-----------------------#
best=False; all=False; specific=False;
if data.getvalue("best")=='y': best = True #Best should either be "y" or "n", otherwise it will not be processed
if data.getvalue("all")=='y': all = True #"y" or "n"-->Denotes whether all graph paths should be traversed
if data.getvalue("specific"): specific=data.getvalue("specific");

# extra = {'best': best, 'all': all, 'specific': specific}

#Condensed input analysis#
#------------------------#
if len(inpt.split("!")) > 1:
    mutation = '%s%s' %(inpt.split("!")[1][0], inpt.split("!")[1][-1])
    position = inpt.split("!")[1][1:-1]
    id = inpt.split("!")[0]
elif len(inpt.split(":")) > 1:
    id=inpt.split(":")[0]; position=inpt.split(":")[1].split(" ")[0]; 
    try: mutation=inpt.split(":")[1].split(" ")[1];
    except: mutation = None;
elif len(inpt.split(" ")) == 3:
    id = inpt.split(" ")[0]; position = inpt.split(" ")[1]; mutation = inpt.split(" ")[2];
elif len(inpt.split(" ")) == 2:
    id = inpt.split(" ")[0]; position = inpt.split(" ")[1]; mutation = None;
else: id = inpt;


try: mutation="%s%s"%(mutation.split("->")[0], mutation.split("->")[1]);
except: pass
try: mutation=mutation.replace(">","")
except:pass


#REGEX INPUT PATTERN MATCHING#
#----------------------------#
parsedInput = parse.parse_identifier(id, cur)
type = parsedInput["type"]
id = parsedInput["formatted_id"]
referenceId = parsedInput["reference"]

# DEPRECATED HG19 SUPPORT
hg19_thru=False
if data.getvalue("build")=="old":
    if type=="hg38": type="hg19";
    elif type=="dbsnp" or output=="dbsnp": hg19_thru=True;

#XCDS Handling
my_xcds=None;
if data.getvalue("xcds")=="y": my_xcds=True
elif data.getvalue("xcds")=="n": my_xcds=False
elif data.getvalue("cdna")=="y": my_xcds=True

if type!="pdb": id = id.upper();

#JSON Output
json_output = []
try:
    if type: #If input is valid
        # Getting source of input
        source=None;
        if type=="uniprot":
            cur.execute("select source from uniprot_source where uniprot='%s'"%id.split("-")[0]);
            rows=cur.fetchall();
            if len(rows)>0: source=rows[0][0]
        with con:
            old_stdout = sys.stdout;
            sys.stdout = mystdout = StringIO.StringIO();
            if position: position = int(position)
            results = bisque.convert(id=id, type=type, output=output, mutation=mutation, position=position, all=all, best=best, path=specific,
                    thru=hg19_thru, xcds=my_xcds, quality=quality, swissprot=swissprot, canonical=canonical)
            sys.stdout = old_stdout
            out = mystdout.getvalue();
            #Look for WT Error
            wt_error = None
            mismatchPos = re.search('WT Mismatch',mystdout.getvalue())
            if mismatchPos != None and data.getvalue("web")=="n":
                wt_error = mystdout.getvalue()[mismatchPos.end()+1:mismatchPos.end()+2]
            if mutation: 
                mutation=mutation.upper();
                if len(mutation)==2: mutation="%s>%s"%(mutation[0],mutation[-1])

            #Add correct version number to input id if reft or refp
            if type=="reft" or type=="refp" and len(results)>0: id=results[0]["source_version"]; 
            #Add results to JSON output for webserver
            for result in results:
                if result["mutation"] and len(result["mutation"])==2:
                    result["mutation"]="%s>%s"%(result["mutation"][0],result["mutation"][-1])
                json_result = result;
                if wt_error: 
                    json_result["wt_error"] = wt_error
                if referenceId:
                    json_result["reference_id"] = referenceId
                json_result["source_id"] = id
                json_result["source_mutation"] = mutation
                json_result["source_position"] = position
                json_result["input_source"] = source
                json_result["output_type"] = output
                json_output.append(json_result)
except Exception as e: 
    json_output.append({"problem":str(e)})
# Regular JSON output
if data.getvalue("web") == "n":
    print(json.JSONEncoder().encode(json_output))
# Format JSON output for web API
else:
    formatted_json_output = []
    for obj in json_output:
        formatted_obj = {
            "input_identifier" : id,
            "input_mutation" : mutation,
            "input_position" : position,
            "output_identifier": obj["value"],
            "output_position": obj["position"], 
            "output_mutation": obj["mutation"]
        }
        #Add additional optional keys
        if quality:
            formatted_obj["alignment_quality"] = obj["quality"]
        formatted_json_output.append(formatted_obj)
    print "["
    for i,obj in enumerate(formatted_json_output):
        if i == len(formatted_json_output) - 1:
            print(json.JSONEncoder().encode(obj))
        else:
            print(json.JSONEncoder().encode(obj)) + ","
    print "]"


















