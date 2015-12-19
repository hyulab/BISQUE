from os import system, path
import shlex, subprocess
import glob 

root_directory = path.abspath(__file__ + "/../../")
system("mkdir data/uniprot/unzipped/")

raw_directory = '%s/data/uniprot/idmapping/by_organism' %(root_directory)
raw_directory1 = '%s/data/uniprot/taxonomic_divisions' %(root_directory)
raw_directory2 = '%s/data/uniprot/proteomes' %(root_directory)
unzip_directory = '%s/data/uniprot/unzipped/' %(root_directory)


gz_files = [x.split("/")[-1] for x in glob.glob("%s/*"%raw_directory)]

gz_files1 = ['uniprot_sprot_human.dat.gz', 'uniprot_trembl_human.dat.gz']

gz_files2 = ['HUMAN.fasta.gz']


for f in gz_files:
	print 'unzipping %s ...' %(f)
	gz_file = path.join(raw_directory, f)
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))

for f in gz_files1:
	print 'unzipping %s ...' %(f)
	gz_file = path.join(raw_directory1, f)
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))

for f in gz_files2:
	print 'unzipping %s ...' %(f)
	gz_file = path.join(raw_directory2, f)
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))



