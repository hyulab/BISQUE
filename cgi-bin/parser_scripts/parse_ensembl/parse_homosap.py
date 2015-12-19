from os import system, path
from Bio import SeqIO 

root_directory = path.abspath(__file__ + "/../../../")
file_handle = open('%s/data/ensembl/unzipped/Homo_sapiens.GRCh38.cds.all.fa' %(root_directory), 'r')
output_file = open('%s/parsed_files/enst_seq.txt' %(root_directory), 'w')
output_file1 = open('%s/parsed_files/enst_ensg.txt' %(root_directory), 'w')

for record in SeqIO.parse(file_handle, 'fasta'):

	enst = record.id
	strand = "+" if record.description.split()[2].split(":")[-1] == '1' else "-"
	seq = record.seq 
	ensg = record.description.split()[3].split(":")[1]
	output_file.write("%s\t%s\t%s\n" %(enst, strand, seq))
	output_file1.write("%s\t%s\n" %(enst, ensg))


output_file.close()
file_handle.close()



file_handle = open('%s/data/ensembl/unzipped/Homo_sapiens.GRCh38.pep.all.fa' %(root_directory), 'r')
output_file = open('%s/parsed_files/ensp_aaseq.txt' %(root_directory), 'w')
output_file1 = open('%s/parsed_files/enst_ensp.txt' %(root_directory), 'w')

for record in SeqIO.parse(file_handle, 'fasta'):

	ensp = record.id
	seq = record.seq 
	enst = record.description.split()[4].split(":")[1]

	output_file.write("%s\t%s\n" %(ensp, seq))
	output_file1.write("%s\t%s\n" %(enst, ensp))

output_file.close()
file_handle.close()

