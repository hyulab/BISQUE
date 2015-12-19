#! /usr/bin/env python

from os import system, path, devnull
import sys
import parse
import json
import optparse
import shlex, subprocess, glob
import MySQLdb as mdb
import Node, pipeline.Pipe as PHelper
import pipeFactory
import Graph, User
import re
import traceback
import transcriptOperations as tOp
from identifierOperations import *


#####TYPES####
#enst
#ensp
#ensg
#hg19
#uniprot
##############

####COMMAND LINE PARAMETERS#################################################
if __name__ == '__main__' and len(sys.argv) == 1: sys.argv.append("-h"); #Handle no command line arguments
parser =  optparse.OptionParser()
parser.add_option('-i', '--input', help = 'Input identifier value. E.g, O00522.')
parser.add_option('-t', '--type', help = "Reference to input database convention. Valid types include: enst, ensg, ensp, reft, refp, uniprot, hg38, hg37, pdb, dbsnp. (Optional)")
parser.add_option('-o', '--output', default = 'uniprot', help = "Reference to output database convention. Valid types are the same as input types.")
parser.add_option('-m', '--mutation', help = "Point nucleotide mutation or amino acid substitution (depending on input type). Must be in form [WILDTYPE][MUTATION]. E.g., AC or MV.")
parser.add_option('-p', '--position', help = "1-indexed position of a nucleotide or amino acid residue.", type = int)
parser.add_option('-v', '--verbosity', help = 'Show warnings and detailed conversion step output. Input either 1 (less verbose) or 2 (more verbose) Default is verbosity=false.', default = 0, type = int)
parser.add_option('--path', help = 'By default BISQUE will traverse only the optimal path. Choose "all" to traverse all paths or specify a single specific path by separating databases with //. E.g., --path hg38//enst//uniprot')
parser.add_option('--swissprot', action="store_true", help='Only return UniProt identifiers from the Swiss-Prot database and their associated transcripts.')
parser.add_option('--cdna',action="store_true",help='Treat transcript positions as relative to 1-indexed cDNA positions for both input and output. By default, CDS positions are assumed.')
parser.add_option('--quality', action="store_true", help='Display needle alignment scores of identifiers averaged over all steps of the conversion for which alignments are performed. Requires needle to be installed. Returns -1 if no alignments are performed.')
parser.add_option("--canonical", action="store_true", help="Only return canonical UniProt identifiers and their associated transcripts.")
parser.add_option("--batch", help="Denotes the path of a batch input file and triggers batch conversion. The default output behavior is to print to the command line in JSON format.")
parser.add_option("--out", help="Denotes the path to which a batch conversion exports its json result.")

options, args = parser.parse_args()
#############################################################################
#########
#GLOBALS#
#########
uniprot_pos=None;
seen_nodes = [] #optimization for traverse_graph
batch_cache = [] #optimization for batch queries
##################
#MYSQL CONNECTION#
##################

con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), 'bisque')
cur = con.cursor()

#######
#GRAPH#
#######
#This program uses a dictionary graph implementation to find the mysql table traversal between types (nodes)

graph = Graph.get_graph()
optimizedGraph = Graph.get_optimized_graph();

################
#HELPER METHODS#
################

#Recursive function to remove brackets from a list
def unzip(l): 
    result = [] 
    def looper(l):
        if type(l) == list:
            for x in l:
                looper(x)
        else:
            result.append(l)
    looper(l)
    return result 

def remove_list_duplicates(l):
    temp=[];
    for e in l:
        if not e in temp: temp.append(e)
    return temp;

#The following two methods use DFS to find the paths through a graph
def looper(graph, start, end, path, path_list):
    #Error handling to make sure user doesn't attempt to traverse through a node that doesn't exist
    if start not in graph or end not in graph:
        print "ERROR: You are attempting to use a nonexistent node in your traversal!"
        path_list = None; #None, so the main conversion function recognizes that the path is impossible
        return;
    path = path + [start]
    if start == end:
        path_list.append(path)
    for node in graph[start]:
        if node not in path:
            looper(graph, node, end, path, path_list)

def getPath(graph, start, end):
    path_list = []
    path = []
    looper(graph, start, end, path, path_list)
    return path_list


#Turns path list into an SQL table traversal list
def produce_table_list(path, tables = []):
    if len(path) > 1:
        tables.append("%s_%s" %(path[0], path[1]))
        return produce_table_list(path[1:], tables)
    return tables

#Returns the optimal path through a path list--i.e, the shortest path which traverses the 
#smallest number of databases as well as traverses upstream xor downstream
def get_best_path(path_list,multiple_traversals=False):
    db_mapping={'pdb':'NCBI','pdbc':'NCBI',"hg38":"NCBI","dbsnp":"NCBI","hg19":"NCBI","enst":"Ensembl","ensp":"Ensembl","ensg":"Ensembl","reft":"RefSeq","refp":"RefSeq","uniprot":"UniProt"};
    type_mapping={"enst":"transcript","ensp":"protein","ensg":"gene","reft":"transcript","refp":"protein","uniprot":"protein","hg38":"chromosome","hg19":"chromosome","dbsnp":"chromosome",'pdb':'protein','pdbc':'protein'}
    def num_db_traversed(path):
        db_acc=[];
        for n in path: 
            db=db_mapping[n];
            if db not in db_acc: db_acc.append(db);
        return len(db_acc)
    def get_stream_violation(path):
        if len(path)<3 or (path[0] == "ensg" and path[-1] == "dbsnp"): return False;
        stream_order=["chromosome","gene","transcript","protein"];
        path_stream="up" if stream_order.index(type_mapping[path[0]])<=stream_order.index(type_mapping[path[1]]) else "down";
        path_stream="parallel" if stream_order.index(type_mapping[path[0]])==stream_order.index(type_mapping[path[1]]) else path_stream;
        for i in range(len(path)-1):
            current_stream="up" if stream_order.index(type_mapping[path[i]])<=stream_order.index(type_mapping[path[i+1]]) else "down";
            current_stream="parallel" if stream_order.index(type_mapping[path[i]])==stream_order.index(type_mapping[path[i+1]]) else current_stream;
            if path_stream=="parallel": path_stream=current_stream;
            elif current_stream!="parallel": 
                if current_stream!=path_stream: return True;
        return False;

    #Remove traversals through hg38 node
    path_list=[a for a in path_list if not ("hg38" in a and a[0]!="hg38" and a[0]!="dbsnp" and a[-1]!="hg38" and a[-1]!="dbsnp")];
    #Remove traversals which cause a stream violaion
    path_list=[a for a in path_list if not get_stream_violation(a)];
    if not multiple_traversals:
        #Choose shortest path
        min_path=min(len(p) for p in path_list);
        path_list=[a for a in path_list if len(a)==min_path];
        #Break ties by choosing path with smallest number of database traversals
        min_db_traversals=min(num_db_traversed(p) for p in path_list);
        path_list=[a for a in path_list if num_db_traversed(a)==min_db_traversals];
        #Now that all bad paths have been filtered, choose the first path in the list (if there are more than 1)
        return path_list;
    else:
        return path_list;


def traverse_graph(input_node, traversal_list, preserved_pos=None):
    global seen_nodes
    # EDGE CASE: CORRECTLY FETCHING SOURCE FROM UNIPROT->UNIPROT CONVERSION
    if len(traversal_list)==1 and input_node.id_type=="uniprot":
        cur.execute("select source from uniprot_source where uniprot='%s'"%input_node.value.split('-')[0]);
        rows=cur.fetchall();
        if len(rows)>0: input_node.source=rows[0][0]
    # EDGE CASE HANDLING COMPLETE

    if options.verbosity > 1:
        try:
            s1 = "|Converting from %s->%s|" %(traversal_list[0], traversal_list[1])
            s2 = ""
            for i in range(len(s1)): s2+="-"
            print ""
            print s2
            print s1
            print s2
        except: 
            pass
    if input_node.id_type == traversal_list[-1]:
        data = {'type': input_node.id_type, 'value': input_node.value, 'mutation': input_node.mutation,
                'position': input_node.position, 'source': input_node.source,'snp_source':input_node.snp_source,
                'wt_source':input_node.wt_source, 'wt_out':get_wild_type(input_node.value,input_node.id_type,input_node.position,cur,preserved_pos),
                "chain_source":input_node.chain_source, 'quality': input_node.quality}
        return data 
    next_node_list = None;

    reload(pipeFactory);
    next_pipe=pipeFactory.generatePipe(input_node, traversal_list[1], options.verbosity, cur);
    next_node_list = next_pipe.output(options.verbosity)
    for n in next_node_list:
        #Local seen node optimization
        if str(n) in seen_nodes: 
            next_node_list.remove(n);
        else: seen_nodes.append(str(n));

    results = [traverse_graph(n, traversal_list[1:],preserved_pos) for n in next_node_list];
    return results



###########################
#PRIMARY CONVERSION METHOD#
###########################

#Takes in an identifier id, an identifier type type (core types include: hg19,hg38,enst,ensg,ensp,uniprot), optional mutation, optional position,
#optional cursor, and optional extra options and outputs a dictionary list
def convert(id, type, output, mutation=None, position=None, all=False, best=False, path=None, xcds=True, thru=False, swissprot=False, canonical=False, quality=False, cursor=cur, command_line=False):
    try:
        # Reset globals
        global seen_nodes
        seen_nodes = []
        # If user gives "hg37" as an input, allow it, but replace it with "hg19"
        if type == "hg37": type = "hg19"
        if output == "hg37": output = "hg19"
        # If chromosome given without 'chr' prepended, then prepend it
        if (type=="hg38" or type=="hg19") and id[:3].upper()!="CHR":
            id = ("chr" + options.input).lower()
        # Preserved position handling
        preserved_pos=None;
        if output=="pdb" and type == "uniprot": 
            preserved_pos = position;
        modifier="";
        if type=="hg19" or output=="hg19" or thru: 
            modifier="19_";
        # SET GLOBAL INPUT AND OUTPUT TYPE VARIABLES FOR USE IN OTHER FUNCTIONS
        input_type=type; output_type=output;
        # OUTPUT SHOULD NEVER BE PDB, SHOULD BE PDBC BECAUSE WE WANT CHAIN
        if output=="pdb": output="pdbc";
        if type=="pdb" and len(id)>4: type="pdbc"
        #CORRECT VERSION NUMBER
        if type=="reft" or type=="refp": 
            corrected_id = correct_version_number(id, type)
            if corrected_id: id = corrected_id
        #Upper case mutation and accept > format
        if mutation: mutation=mutation.replace(">","").upper();
        # Drop mutation if it contains amino acids yet the identifier is not a protein
        if type!="ensp"and type!="refp" and type!="uniprot" and 'pdb' not in type and mutation:
            if mutation[0] not in "ATGC" or mutation[1] not in "ATGC": mutation=None;
        # Chop the -1 off user input if it is uniprot 
        try:
            if type=="uniprot" and id.split("-")[-1]=="1": id=id.split("-")[0]
        except:pass
        # Quick Check for GeneName to convert the input to uniprot on the fly
        if(geneNameToUniprot(id, cur)):
            id=geneNameToUniprot(id, cur)
            type='uniprot'


        #If XCDS Flag and converting FROM transcript
        if xcds and (type=="reft" or type=="enst") and position:
            chr_pos=tOp.dechunk_ncds_position(position,id,modifier+type,cur);
            position=tOp.chunk_position(chr_pos,id,modifier+type,cur);
            if not position: mutation=None;


        # WT Error Handling
        if(mutation and position and type!='hg38' and type!='hg19' and type!='ensg' and "pdb" not in type): #Chromosome WTcheck is handled in chromsome_transcript.py
            mutation=correctWT(id,type,position,mutation,cur);	

        path_list = getPath(graph, type, output); 
        path_list = [p for p in path_list if not ("hg19" in p and (not thru and type!="hg19" and output!="hg19"))];
        if not path_list: return None 

        # CONSTRUCTING NODE
        input_node = Node.Node(type, id, mutation, position, wt_source = get_wild_type(id,type,position,cur));
        input_node.startNode=True;

        # SET NODE QUALITY FIELD TO -2, IF NOT OPTIONS.QUALITY, IN ORDER TO PREVENT NEEDLESS ALIGNMENT
        if not quality:
            input_node.quality = -2

        # MODIFY PATH IF THRU
        if thru:
            for p in path_list:
                if "hg38" in p: p[p.index("hg38")]="hg19";

            if not thru and type!="hg19" and output!="hg19":
                for p in path_list: 
                    if "hg19" in p: path_list.remove(p);
        # Remove paths which go directly from ENSG->HG38 if the convrsion is ensg->dbsnp and no position is given for the ensg
        if type == "ensg" and output == "dbsnp" and not position:
            path_list = [p for p in path_list if not (p[0] == "ensg" and (p[1] == "hg19" or p[1] == "hg38"))]

        #Allowing traversal through all routes of the graph
        if path == "all": 
            results = []
            all_valid_paths=get_best_path(path_list,True);
            if options.verbosity == 1: print "Taking all valid paths from source to destination: %s" %str(all_valid_paths);
            for path in all_valid_paths:
                input_node.position = position #Because the position is subtracted by 1 every time it does a loop
                results+=traverse_graph(input_node, path,preserved_pos)

        #Allowsing traversal through a specific route of the graph 
        elif path:
            custom_path = path.split('//')
            if options.verbosity == 1: print "Taking your custom path: %s" %str(custom_path);
            results = traverse_graph(input_node, custom_path,preserved_pos);

        #Default is shortest route
        else: 
            best_paths=get_best_path(path_list);
            results=[];
            for p in best_paths:
                results.append(traverse_graph(input_node, p,preserved_pos));
            if options.verbosity == 1: print "The optimal path(s) taken is: %s" %str(best_paths);

        #Cleaning up results. Some parts optional
        try: results.remove([])
        except: pass
        results = [dict(t) for t in set([tuple(d.items()) for d in unzip(results) if d!="SOURCEREMOVAL"])] #Remove duplicates in results
        if best:
            clean_results = []
            for result in unzip(results):
                has_none = False
                for field in result:
                    if result[field] == None and field!='source': has_none = True 
                if has_none: continue
                else: clean_results.append(result) 

            clean_results = [dict(t) for t in set([tuple(d.items()) for d in clean_results])]
        else: clean_results = unzip(results) #Removes nested lists from result

        #Add accessible source version number to result for web server to use without having to fetch version number again
        if type=="reft" or type=="refp":
            for result in clean_results: result["source_version"]=id;

        #If XCDS flag and output is a transcript
        if xcds and (output=="enst" or output=="reft"):
            for r in clean_results:
                if r['position']:
                    chr_pos=tOp.dechunk_position(r['position'],r['value'],"%s%s"%(modifier,output),cur);
                    r['position']=tOp.chunk_ncds_position(chr_pos, r['value'], "%s%s"%(modifier,output), cur);

        #Filter out isoforms, if canonical option is true
        if canonical and output == "uniprot":
            clean_results = [r for r in clean_results if len(r["value"].split("-")) == 1 or int(r["value"].split("-")[1]) == 1]

        #Filter out any identifiers which don't map to swissprot, or don't map to canonical, depending on options
        if (swissprot or canonical) and output != "hg38" and output != "hg19":
            filtered_results = []
            for result in clean_results[::-1]:
                uniprot_results = convert(result["value"], type=output, output="uniprot")
                if result["value"] == "ENST00000504290": print uniprot_results
                swissprot_satisfied = False
                canonical_satisfied = False
                for r in uniprot_results:
                    #Check to see if swissprot
                    if r["source"] == "s": swissprot_satisfied = True
                    #Check to see if canonical
                    if len(r["value"].split("-")) == 1: canonical_satisfied = True
                    elif len(r["value"].split("-")) > 1 and int(r["value"].split("-")[-1]) == 1: canonical_satisfied = True
                if swissprot and canonical:
                    if swissprot_satisfied and canonical_satisfied: filtered_results.append(result)
                elif swissprot:
                    if swissprot_satisfied: filtered_results.append(result)
                elif canonical:
                    if canonical_satisfied: filtered_results.append(result)
                else:
                    filtered_results.append(result)
                #filtered_results.append(result)
            clean_results = filtered_results

        #Trim and Correct quality
        for result in clean_results:
            #Change quality to 1.0 if < 0
            if result['quality'] < 0: result['quality'] = 1.0
            #Round quality to 2 decimal places
            result["quality"] = "{0:.3f}".format(result["quality"])


        #Print results in a way easy for the user to read, but only if executed through command line
        if command_line:
            if options.verbosity > 1: 
                print ""
                print "----------------------"
                print "|Conversion Complete!|"
                print "----------------------"
            for result in clean_results:
                if options.quality:
                    print "%s %s %s %s"%(result['value'],result['position'],result['mutation'],str(result['quality']))
                else:
                    print "%s %s %s"%(result['value'],result['position'],result['mutation'])

        #Final return statement
        return clean_results
    except Exception:
        print "BISQUE has encountered an internal error. Set verbosity to 1 or 2 to view error traceback."
        if options.verbosity > 0:
            e = sys.exc_info()
            print e[0]
            traceback.print_tb(e[2])


if __name__=="__main__":
    
    #####################################
    #DYNAMIC COMMAND LINE INPUT HANDLING#
    #####################################
    #Batch Handling: Interacts with batch.cgi script, originally intended just for webserver
    if options.batch:
        json_results = []
        batch_file_handle = open(options.batch, "r")
        if options.out:
            json_out_file = open(options.out, "w")
        else:
            json_out_file = open("out.json", "w")
        input_lines = batch_file_handle.read().splitlines()
        for line in input_lines:
            parsed_line = parse.parse_line(line)
            if parsed_line == None: continue
            (identifier, position, mutation) = parsed_line
            input_type = parse.parse_identifier(identifier, cur)["type"]
            position = int(position) if position else None
            results = convert(identifier, input_type, options.output, mutation, position, xcds=options.cdna, quality=options.quality, swissprot=options.swissprot, canonical=options.canonical)
            if not results: continue
            for result in results:
                json_obj = {
                    "input_identifier" : identifier,
                    "input_mutation" : mutation,
                    "input_position" : position,
                    "output_identifier": result["value"],
                    "output_position": result["position"], 
                    "output_mutation": result["mutation"]
                }
                json_results.append(json_obj)
        #Write JSON to output file
        json_out_text = ""
        json_out_text += "[\n"
        for i,obj in enumerate(json_results):
            if i == len(json_results) - 1:
                json_out_text += (json.JSONEncoder().encode(obj) + "\n")
            else:
                json_out_text += (json.JSONEncoder().encode(obj) + "," + "\n")
        json_out_text += "]"
        #Print JSON to command line
        if options.out:
            json_out_file.write(json_out_text)
        else:
            print json_out_text
        sys.exit(1)

    #Normal Handling
    # If no type, parse input to determine type
    if options.type == None: options.type = parse.parse_identifier(options.input, cur)["type"]
    if 'pdb' not in options.type:options.input=options.input.upper();

    ###################
    #COMMAND LINE CALL#
    ###################
    xcds_option=options.cdna;
    convert(options.input, options.type, options.output, options.mutation, options.position, False,False,options.path,xcds=xcds_option, quality=options.quality, swissprot=options.swissprot, canonical=options.canonical, command_line = True if options.input else False)
