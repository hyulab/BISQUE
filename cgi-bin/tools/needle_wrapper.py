"""Contains useful tools for interacting with UniProt, PDB, and other biological data sources. """

import os
from subprocess import Popen, PIPE
from tempfile import mkdtemp
from shutil import rmtree, copyfile


def run_clustalo(sequences, seqtype='Protein', CLUSTALO_PATH='clustalo'):
	"""Wrapper to run Clustal Omega. Other seqtypes available: Protein, RNA, DNA.
	Returns alignment in same format as given sequences, match character string, fraction identity, similarity (2-levels)"""
	
	#string (fasta file name)
	if type(sequences) == str:
		input_data = open(sequences).read()
	#list of strings
	elif type(sequences) == list and type(sequences[0]) == str:
		input_data='\n'.join(['>seq%s\n%s' %(i+1, s) for i, s in enumerate(sequences)])
	#list of tuples of (name, sequence) pairings
	elif type(sequences) == list and type(sequences[0]) == tuple and len(sequences[0])==2:
		input_data='\n'.join(['>%s\n%s' %(n, s) for n, s in sequences])
	#dictionary of name->sequence mappings
	elif type(sequences) == dict:
		input_data='\n'.join(['>%s\n%s' %(k, v) for k, v in sequences.items()])
	else:
		raise Exception('Invalid input format for variable <sequences>')
	
	#--------------
	clustalo_params = [CLUSTALO_PATH, '--wrap=999999999', '--outfmt=clu', '--seqtype=%s' %(seqtype), '--infile=-']
	#~ print ' '.join(clustalo_params)
	
	output, error = Popen(clustalo_params, stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate(input=input_data)
	#--------------
	
	output = output.split('\n')
	
	alignment = [tuple(l.split()) for l in output[3:-2]]
	start = output[3].rfind(' ')
	match_chars = output[-2][start+1:].replace('\n', '')
	
	stars = match_chars.count('*')
	colons = match_chars.count(':')
	alignment_length = float(len(match_chars))
	
	identity = stars/alignment_length
	similarity = (stars+colons)/alignment_length
	

	if type(sequences) == dict:
		alignment = dict(alignment)
	elif type(sequences) == list and type(sequences[0]) == str:
		alignment = [a[1] for a in alignment]
	#otherwise will return list of tuples in original order
	
	return alignment, match_chars, identity, similarity






def run_needle(seq1, seq2, sub_matrix='EBLOSUM62', NEEDLE_PATH='needle'):
	"""Wrapper to run EMBOSS Needle. Substitution matrices available: EBLOSUM62 (protein) and EDNAFULL (DNA)"""
	
	scratchDir = mkdtemp()
	
	seq1_file = os.path.join(scratchDir, 'seq1.fasta')
	seq2_file = os.path.join(scratchDir, 'seq2.fasta')
	output_file = os.path.join(scratchDir, 'needle.out')
	
	f = open(seq1_file, 'w')
	f.write('>seq1\n%s' %(seq1))
	f.close()
	
	f = open(seq2_file, 'w')
	f.write('>seq2\n%s' %(seq2))
	f.close()
	
	#--------------
	needle_params = [NEEDLE_PATH, seq1_file, seq2_file, output_file, '-datafile', sub_matrix, '-auto', 'Y', '-awidth3', '999999999']
	#~ print ' '.join(needle_params)
	
	_, _ = Popen(needle_params, stdout=PIPE, stderr=PIPE).communicate()
	#--------------
	
	output = open(output_file).read()
	#~ print output
	
	output = output.split('\n')
	align1 = output[-8].split()[2]
	match_chars = output[-7][21:21+len(align1)]
	align2 = output[-6].split()[2]
	
	pipes = match_chars.count('|')
	colons = match_chars.count(':')
	alignment_length = float(len(match_chars))
	identity = pipes/alignment_length
	similarity = (pipes+colons)/alignment_length
	
	#cleanup temporary files
	rmtree(scratchDir)
	
	return [align1, align2], match_chars, identity, similarity
	


def run_stretcher(seq1, seq2, sub_matrix='EBLOSUM62', STRETCHER_PATH='stretcher'):
	"""Wrapper to run EMBOSS Stretcher (faster needle for longer sequences). Substitution matrices available: EBLOSUM62 (protein) and EDNAFULL (DNA)"""
	
	scratchDir = mkdtemp()
	
	seq1_file = os.path.join(scratchDir, 'seq1.fasta')
	seq2_file = os.path.join(scratchDir, 'seq2.fasta')
	output_file = os.path.join(scratchDir, 'stretcher.out')
	
	f = open(seq1_file, 'w')
	f.write('>seq1\n%s' %(seq1))
	f.close()
	
	f = open(seq2_file, 'w')
	f.write('>seq2\n%s' %(seq2))
	f.close()
	
	#--------------
	stretcher_params = [STRETCHER_PATH, seq1_file, seq2_file, output_file, '-datafile', sub_matrix, '-auto', 'Y', '-awidth3', '999999999']
	#~ print ' '.join(stretcher_params)
	
	_, _ = Popen(stretcher_params, stdout=PIPE, stderr=PIPE).communicate()
	#--------------
	
	output = open(output_file).read()
	#~ print output
	
	output = output.split('\n')
	
	align1 = output[-9].split()[1]
	raw_match_chars = output[-8][7:7+len(align1)]
	align2 = output[-7].split()[1]
	
	#make match chars the same as in needle output
	match_chars = ''
	for i in range(len(align1)):
		if raw_match_chars[i] == ':':
			match_chars += '|'
		elif raw_match_chars[i] == '.':
			match_chars += ':'
		elif align1[i] != '-' and align2[i] != '-':
			match_chars += '.'
		else:
			match_chars += ' '
	
	pipes = match_chars.count('|')
	colons = match_chars.count(':')
	alignment_length = float(len(match_chars))
	identity = pipes/alignment_length
	similarity = (pipes+colons)/alignment_length
	
	#cleanup temporary files
	rmtree(scratchDir)
	#~ 
	return [align1, align2], match_chars, identity, similarity


