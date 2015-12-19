from os import system, path

root_directory = path.abspath(__file__ + "/../../../")
file_handle = open('%s/data/uniprot/unzipped/HUMAN_9606_idmapping_selected.tab' %(root_directory), 'r')
file_output = open('%s/parsed_files/uniprot_refp.txt' %(root_directory), 'w')

for l in file_handle:
	l = l.strip()
	if len(l.split("\t")[3]) > 0:
		if l.split("\t")[3][:2]=='NP':file_output.write("%s\t%s\n" %(l.split("\t")[0], l.split("\t")[3].split('.')[0]))

file_handle.close()
file_output.close()

file_handle = open('%s/parsed_files/uniprot_refp.txt' %(root_directory), 'r')
file_output = open('%s/parsed_files/refp_uniprot.txt' %(root_directory), 'w')

refp_uniprot_dict = {}
for l in file_handle:
	uniprot = l.split("\t")[0]
	refp_list = [x.strip() for x in l.split("\t")[1].split(";")]
	for refp in refp_list:
		if refp not in refp_uniprot_dict:
			refp_uniprot_dict[refp] = []
		refp_uniprot_dict[refp].append(uniprot)

for refp in refp_uniprot_dict:
	for uniprot in refp_uniprot_dict[refp]:
		file_output.write("%s\t%s\n" %(refp, uniprot))

file_handle.close()
file_output.close()
