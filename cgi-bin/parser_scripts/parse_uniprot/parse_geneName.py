from os import system, path

root_directory = path.abspath(__file__ + "/../../../")
file_handle = open('%s/data/uniprot/unzipped/uniprot_sprot_human.dat' %(root_directory), 'r')
file_handle2 = open('%s/data/uniprot/unzipped/uniprot_trembl_human.dat' %(root_directory), 'r')
out_file = open('%s/parsed_files/geneName_uniprot.txt' %root_directory, 'w')


start = False
currentUniprot = None;


for l in file_handle:
	if l.split()[0]=='AC' and start == False:
		try:currentUniprot = l.split()[1][:-1];
		except: continue
		start = True;
	elif l.split()[0]=='GN' and start == True:
		try:
			geneName = l.split()[1].split('=')[1].replace(';','');
			out_file.write('%s\t%s\tswiss\tprimary\n'%(geneName, currentUniprot))
			synonyms = [x.replace(";","").strip() for x in l.split(';')[1].split('=')[1].split(',')]
			for s in synonyms:
				out_file.write('%s\t%s\tswiss\tsynonym\n'%(s, currentUniprot))
			start = False;
		except:
			start = False;

start=False
currentUniprot=None
for l in file_handle2:
	if l.split()[0]=='AC' and start == False:
		try:currentUniprot = l.split()[1][:-1];
		except: continue 
		start = True;
	elif l.split()[0]=='GN' and start == True:
		try:
			geneName = l.split()[1].split('=')[1].replace(';','');
			out_file.write('%s\t%s\ttrembl\tprimary\n'%(geneName, currentUniprot))
			synonyms = [x.replace(";","").strip() for x in l.split(';')[1].split('=')[1].split(',')]
			for s in synonyms:
				out_file.write('%s\t%s\ttrembl\tsynonym\n'%(s, currentUniprot))
			start = False;
		except:
			start = False;

file_handle.close();
file_handle2.close();
out_file.close();