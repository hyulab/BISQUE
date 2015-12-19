#! /usr/bin/env python
import urllib2
import optparse

#########################
#COMMAND LINE PARAMETERS#
#########################
parser = optparse.OptionParser()
parser.add_option('-i', '--input', help = 'Input identifier value. E.g, O00522.')
parser.add_option('-m', '--mutation', help = "Point mutation. Must be in form [WILDTYPE][MUTATION]. E.g, AC.")
parser.add_option('-p', '--position', help = "1-indexed position of a nucleotide or amino acid residue", type = int)
parser.add_option('-o', '--output', default = 'uniprot', help = "Reference to output type. UniProt Protein is referenced as 'uniprot'.")
parser.add_option('-b', '--best', action = 'store_true', help = 'Removes results with None fields.')
parser.add_option('-a', '--all', action = 'store_true', help = 'Traverse all routes through graph. Default is false.')
parser.add_option('-s', '--specific', action = 'store_true', help = 'Traverse a specific route through the graph. E.g, -s hg38//enst//uniprot.')

options, args = parser.parse_args()

############################
#COMMAND LINE FUNCTIONALITY#
############################
if options.input: #If user used command line
	#If user attaches a mutation and position
	if options.mutation and options.position:
		#Extra option handling (best, all, specific)
		if options.best: best_boolean = 'y'
		else: best_boolean = 'n'
		if options.all: all_boolean = 'y'
		else: all_boolean = 'n'
		if options.specific: specific_path=(',').join(options.specific)
		else: specific_path='' 

		#Url request, handling every option
		response = urllib2.urlopen('http://bisque.yulab.org/cgi-bin/run.cgi?id=%s&output=%s&mutation=%s&position=%s&best=%s&all=%s&specific=%s' 
			%(options.input, options.output, options.mutation, options.position, best_boolean, all_boolean, specific_path))
	else:
		#Extra option handling (best, all, specific)
		if options.best: best_boolean = 'y'
		else: best_boolean = 'n'
		if options.all: all_boolean = 'y'
		else: all_boolean = 'n'
		if options.specific: specific_path=(',').join(options.specific)
		else: specific_path='' 
		response = urllib2.urlopen('http://bisque.yulab.org/cgi-bin/run.cgi?id=%s&output=%s&best=%s&all=%s&specific=%s' 
			%(options.input, options.output, best_boolean, all_boolean, specific_path));
	html = response.read().split('\n')
	for result in html:
		if len(result.split()) == 6 or len(result.split())==7:
			print "%s\t%s\t%s" %(result.split()[3].strip(), result.split()[4].strip(), result.split()[5].strip()) 
	

########################################
#IMPORTABLE PYTHON MODULE FUNCTIONALITY#
########################################

#Arguments: input is the input identifier, output is the desired output type. mutation is a 
#string  e.g 'AB' which represents a mutation from A to B. Input position is an int designating the position
#of the mutation. Extras is a dictionary telling the program whether or not to execute additional options. 
#Look at the default setting.

#Output: a dictionary list in the form [{ouput_id:X,output_mutation:Y,output:position:Z},...]
#X and Y are strings. Position Z is of type int and is 1-indexed.

def convert(id, output, mutation = None, position = None, all=False,best=False,specific=False):
	# Extra option handling
	if best: best_boolean = 'y'
	else: best_boolean = 'n'
	if all: all_boolean = 'y'
	else: all_boolean = 'n'
	if specific: specific_path=(',').join(options.specific)
	else: specific_path='' 

	#If user attaches a mutation and position
	if mutation and position:	
		#Url request, handling every option
		response = urllib2.urlopen('http://bisque.yulab.org/cgi-bin/run.cgi?id=%s&output=%s&mutation=%s&position=%s&best=%s&all=%s&specific=%s' 
			%(id, output, mutation, position, best_boolean, all_boolean, specific_path))
	else:
		response = urllib2.urlopen('http://bisque.yulab.org/cgi-bin/run.cgi?id=%s&output=%s&best=%s&all=%s&specific=%s' 
			%(id, output, best_boolean, all_boolean, specific_path))
	html = response.read().split('\n')
	result_list = []
	for result in html:
		if (len(result.split()) == 6 or len(result.split())==7):
			result_list.append({'value':result.split()[3], 'mutation':result.split()[4], 'position':result.split()[5]})

	return result_list



