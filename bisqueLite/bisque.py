#! /usr/bin/env python
import urllib2
import optparse
import json
import sys

#########################
#COMMAND LINE PARAMETERS#
#########################
parser = optparse.OptionParser()
if __name__ == '__main__' and len(sys.argv) == 1: sys.argv.append("-h"); #Handle no command line arguments
parser.add_option('-i', '--input', help = 'Input identifier value. E.g, O00522.')
parser.add_option('-m', '--mutation', help = "Point nucleotide mutation or amino acid substitution (depending on input type). Must be in form [WILDTYPE][MUTATION]. E.g., AC or MV.")
parser.add_option('-p', '--position', help = "1-indexed position of a nucleotide or amino acid residue.", type = int)
parser.add_option('-o', '--output', default = 'uniprot', help = "Reference to output database convention. Valid types are the same as input types.")
parser.add_option('--swissprot', action="store_true", help='Only return UniProt identifiers from the Swiss-Prot database and their associated transcripts.')
parser.add_option('--cdna',action="store_true",help='Treat transcript positions as relative to 1-indexed cDNA positions for both input and output. By default, CDS positions are assumed.')
parser.add_option('--quality', action="store_true", help='Display needle alignment scores of identifiers averaged over all steps of the conversion for which alignments are performed. Requires needle to be installed. Returns -1 if no alignments are performed.')
parser.add_option("--canonical", action="store_true", help="Only return canonical UniProt identifiers and their associated transcripts.")

options, args = parser.parse_args()

#########################
#CONVERSION FUNCTIONALIY#
#########################
def convert(identifier, output, mutation = None, position = None, cdna = False, swissprot = False, canonical = False, quality = False): 
    #Generate HTTP Request
    url = "http://bisque.yulab.org/cgi-bin/run.cgi?"
    params = "id=%s&output=%s"%(identifier, output)
    if mutation: params += "&mutation=%s"%mutation
    if position: params += "&position=%s"%(str(position))
    if cdna: params += "&cdna=y"
    if swissprot: params += "&swissprot=y"
    if canonical: params += "&canonical=y"
    if quality: params += "&quality=y"
    #Fetch HTTP Response and Decode as JSON
    response = urllib2.urlopen(url + params).read()
    response = json.loads(response)
    #Encode JSON as UTF8
    utf8_response = []
    for entry in response:
        utf8_entry = {}
        for key in entry:
            utf8_value = entry[key]
            if utf8_value: utf8_value = utf8_value.encode("utf8")
            utf8_entry[key.encode("utf8")] = utf8_value
        utf8_response.append(utf8_entry)
    return utf8_response

############################
#COMMAND LINE FUNCTIONALITY#
############################
if options.input:
    print convert(options.input, options.output, options.mutation, options.position, options.cdna, options.swissprot, options.canonical, options.quality)

