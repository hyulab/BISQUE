"""Contains useful tools for interacting with UniProt, PDB, and other biological data sources. """

import os
from subprocess import Popen, PIPE
from tempfile import mkdtemp
from shutil import rmtree, copyfile


def run_needle(seq1, seq2, sub_matrix='EBLOSUM62', NEEDLE_PATH='/usr/local/bin/needle'):
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
	
