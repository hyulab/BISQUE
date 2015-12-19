from os import system, path
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/ensembl" %(root_directory))
local_directory = '%s/data/ensembl' %(root_directory) #IMPORTANT: no forward slash after directory name
###################################################################################
ftp_directory = 'ftp://ftp.ensembl.org/pub/current_fasta/homo_sapiens/cds/' #IMPORTANT: no forward slash after directory name

sync_files = []

ignore_files = [
			'CHECKSUMS',
			'README']

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 

###############################################################################
ftp_directory = 'ftp://ftp.ensembl.org/pub/current_fasta/homo_sapiens/pep/'


sync_files = []
ignore_files = ['CHECKSUMS', 'README']

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 

##############################################################################
ftp_directory = 'ftp://ftp.ensembl.org/pub/current_gtf/homo_sapiens/'

sync_files = []
ignore_files = ['CHECKSUMS', 'README']

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error


##############################################################################

#Support for deprecated hg19 database
ftp_directory = 'ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/'

sync_files = []
ignore_files = ['CHECKSUMS', 'README']

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error
