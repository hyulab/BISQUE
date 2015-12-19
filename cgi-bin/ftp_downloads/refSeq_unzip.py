from os import system, path
import glob
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/refSeq/unzipped" %(root_directory))

raw_directory = '%s/data/refSeq/' %(root_directory)
unzip_directory = '%s/data/refSeq/unzipped/'%(root_directory)

coord_file = [x.split('/')[-1] for x in glob.glob('%s/ref_GRCh38.*'%raw_directory)]
gz_files = (['protein.fa.gz','rna.fa.gz','protein.gbk.gz']+coord_file)


for f in gz_files:
	print "unzipping %s..." %(f)
	gz_file = path.join(raw_directory, f)
	if f in coord_file:f='GRCh38_top_level.gff3';
	output_file = path.join(unzip_directory, f.replace('.gz', ''))
	system('zcat %s > %s' %(gz_file, output_file))

