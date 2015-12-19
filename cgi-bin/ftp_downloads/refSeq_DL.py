from os import system, path
import shlex, subprocess

root_directory = path.abspath(__file__ + "/../../")
system("mkdir %s/data/refSeq" %(root_directory))

#RNA SEQUENCE DATA
ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/RNA/'
local_directory = '%s/data/refSeq'%root_directory

sync_files=['rna.fa.gz']
ignore_files=[]

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error

#PROTEIN SEQUENCE DATA
ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/protein/'
local_directory = '%s/data/refSeq'%root_directory

sync_files=['protein.fa.gz']
ignore_files=[]

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 
 

ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/RNA/'
local_directory = '%s/data/refSeq'%root_directory

sync_files=['rna.fa.gz']
ignore_files=[]

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 

#TRANSCRIPT COORDINATE DATA
ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/GFF/'
sync_files=['ref_GRCh38.p2_top_level.gff3.gz']
ignore_files=[]

includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 

#CROSS MAPPING DATA FILE
ftp_directory = 'ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/protein/'
sync_files=['protein.gbk.gz']
ignore_files=[]
includes = ' '.join(['-i %s' %(f) for f in sync_files])
print includes
ignores = ' '.join(['-X %s' %(f) for f in ignore_files])
cmd = 'lftp -c mirror --verbose=3 %s %s %s %s' %(includes, ignores, ftp_directory, local_directory)
args = shlex.split(cmd)
output,error = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
print output.replace(u"\u0060", "'"), error 
