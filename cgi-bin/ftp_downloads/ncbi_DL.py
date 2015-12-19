from os import system, path
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/refSeq" %(root_directory))

#REFSEQ X ENSEMBL
ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/'
local_directory = '%s/data/ncbi'%root_directory

sync_files=['gene2ensembl.gz']
ignore_files=[
	'ASN_BINARY/',
	'ASN_BINARY/*',
	'GENE_INFO/',
	'GENE_INFO/*',
	'misc/',
	'misc/*'
]

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error
