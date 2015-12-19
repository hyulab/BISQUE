from os import system, path
from Bio import SeqIO

root_directory = path.abspath(__file__ + "/../../../")
file_handle = open('%s/data/uniprot/unzipped/uniprot_sprot_human.dat' %(root_directory), 'r')
file_handle2 = open('%s/data/uniprot/unzipped/uniprot_trembl_human.dat' %(root_directory), 'r')
file_handle3 = open('%s/data/uniprot/unzipped/uniprot_sprot_varsplic.fasta' %root_directory, 'r')
output_file = open('%s/parsed_files/uniprot_enst.txt' %(root_directory), 'w')
output_file2=open('%s/parsed_files/uniprot_ensp.txt' %(root_directory), 'w')
sequence_output=open('%s/parsed_files/uniprot_aaseq.txt'%root_directory,'w');

seq_length=None;
seq_start=False
seq_accum="";
currentUniprot = None;
acStart=[False];
for l in file_handle:
		

	if seq_start and seq_length:
		seq_accum+=("").join(l.strip().split());
		if len(seq_accum)==seq_length:
			sequence_output.write("%s\t%s\n"%(currentUniprot,seq_accum));
			seq_start=False;
			seq_accum="";
			seq_length=None;
			continue;
			
	if l.split()[0]!="AC" and acStart[0]: acStart[0]=False;
	elif l.split()[0]=="AC" and len(l.split())>1 and acStart[0]==False:
		currentUniprot=l.split()[1].split(';')[0]
		acStart[0]=True;
	elif l.split()[0]=="DR" and len(l.split())>1:
		acStart[0]=False;
		if l.split()[1]=="Ensembl;": 
			l = l.strip().split(";")[1:]
			enst = l[0].strip();
			ensp = l[1].strip();
			# Look for isoforms
			isoforms = [x.strip() for x in l[-1].strip().split(".")]
			try:isoforms.remove(""); 
			except: pass;
			if len(isoforms)>1: 
				isoform = isoforms[1][1:-1]
				if isoform[-2:]=="-1": isoform = isoform.split("-")[0]
				output_file.write("%s\t%s\n"%(isoform, enst))
			else:
				output_file.write("%s\t%s\n"%(currentUniprot, enst))
			# Write proteins to file 2
			output_file2.write("%s\t%s\n"%(currentUniprot,ensp));

	elif l.split()[0]=="SQ": 
		seq_start=True;
		try:seq_length=int(l.strip().split()[2]);
		except: pass;


seq_length=None;
seq_start=False
seq_accum="";
currentUniprot = None;
acStart=[False];
for l in file_handle2:
	if seq_start and seq_length:
        	seq_accum+=("").join(l.strip().split());
        	if len(seq_accum)==seq_length:
        		sequence_output.write("%s\t%s\n"%(currentUniprot,seq_accum));
        		seq_start=False;
        		seq_accum="";
        		seq_length=None;
        		continue;


	if l.split()[0]!="AC" and acStart[0]: acStart[0]=False;
	elif l.split()[0]=="AC" and len(l.split())>1 and acStart[0]==False:
		currentUniprot=l.split()[1].split(';')[0]
		acStart[0]=True;
	elif l.split()[0]=="DR" and len(l.split())>1:
		# acStart[0]=False;
		if l.split()[1]=="Ensembl;": 
			l = l.strip().split(";")[1:]
			enst = l[0].strip();
			ensp = l[1].strip();
			# Look for isoforms
			isoforms = [x.strip() for x in l[-1].strip().split(".")]
			try:isoforms.remove(""); 
			except: pass;
			if len(isoforms)>1: 
				isoform = isoforms[1][1:-1]
				if isoform[-2:]=="-1": isoform = isoform.split("-")[0]
				output_file.write("%s\t%s\n"%(isoform, enst))
			else:
				output_file.write("%s\t%s\n"%(currentUniprot, enst))
			# Write proteins to file 2
			output_file2.write("%s\t%s\n"%(currentUniprot,ensp));

	
	elif l.split()[0]=="SQ": 
        	seq_start=True;
        	try:seq_length=int(l.strip().split()[2]);
        	except: pass;

#ISOFORM SEQUENCE HANDLING
for record in SeqIO.parse(file_handle3, 'fasta'):
    isoform = record.id.split("|")[1]
    seq = record.seq
    sequence_output.write("%s\t%s\n"%(isoform, seq))



output_file.close(); output_file2.close();
sequence_output.close()


		


