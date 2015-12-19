from os import system, path
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/ncbi/unzipped" %(root_directory))

raw_directory = '%s/data/ncbi/' %(root_directory)
unzip_directory = '%s/data/ncbi/unzipped/'%(root_directory)

gz_files = ['gene2ensembl.gz']

for f in gz_files:
	print "Unzipping %s..." %(f)
	gz_file = path.join(raw_directory, f)
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))

