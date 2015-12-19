from os import system, path 
import shlex, subprocess
import glob 

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/ensembl/unzipped" %(root_directory))

raw_directory = '%s/data/ensembl/' %(root_directory)
unzip_directory = '%s/data/ensembl/unzipped/' %(root_directory)



gz_files = [x.split("/")[-1] for x in glob.glob('data/ensembl/*.gz')]



for f in gz_files:
	print "Unzipping %s..." %(f)
	gz_file = path.join(raw_directory, f)
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))
