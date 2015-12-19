from os import system, path
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/uniprot" %(root_directory))

ftp_directory = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase' #IMPORTANT: no forward slash after directory name
local_directory = '%s/data/uniprot' %(root_directory) #IMPORTANT: no forward slash after directory name

sync_files = [
		'taxonomic_divisions/uniprot_sprot_human.dat.gz',
		'taxonomic_divisions/uniprot_trembl_human.dat.gz',
		'idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz',
		'idmapping/by_organism/HUMAN_9606_idmapping.dat.gz',
		'proteomes/HUMAN.fasta.gz'
		]

ignore_files = [
		'complete/',
		'complete/*',
		'variants/',
		'variants/*',
		'proteomics_mapping/',
		'proteomics_mapping/*',
		'reference_proteomes/',
		'reference_proteomes/*'
		]




includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error
