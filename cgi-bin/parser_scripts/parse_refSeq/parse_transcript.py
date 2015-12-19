from os import path 
root_directory = path.abspath(__file__ + "/../../../")

file_handle = open('%s/data/refSeq/unzipped/GRCh38_top_level.gff3'%root_directory,'r')
out_file = open('%s/parsed_files/parsedReft.txt'%root_directory,'w')
transcript_positions={}
id_transcript={}
transcript_id={}

duplicate_count=0;
for l in file_handle:
	l=l.strip().split()
	try:
		if l[2]=="mRNA":
			data=l[8].strip().split(';')
			transcript=data[3].strip().split('=')[1]#.split('.')[0];
			id=data[0].strip().split('=')[1];
			if transcript[:2]=="NM":
				if transcript in transcript_id: 
					duplicate_count+=1;
					continue;
				transcript_id[transcript]=id;
				id_transcript[id]=transcript;
				if transcript not in transcript_positions and l[0][:2]=="NC":
					chrom=l[0].split(".")[0][-1] if l[0].split(".")[0][-2]=="0" else l[0].split(".")[0][-2:];
					if chrom=="23": chrom="X";
					elif chrom=="24": chrom="Y";
					transcript_positions[transcript]={"e_starts":[],"e_stops":[], "cds":[], "chr":chrom, "sign":l[6]}
		elif l[2]=="exon":
			on_cds=False;
			data=l[8].strip().split(';')
			parent_id=data[1].strip().split('=')[1];
			if parent_id in id_transcript:
				parent_transcript=id_transcript[parent_id];
				transcript_positions[parent_transcript]["e_starts"].append(l[3]);
				transcript_positions[parent_transcript]["e_stops"].append(l[4]);
		elif l[2]=="CDS":	
			data=l[8].strip().split(';')
			parent_id=data[1].strip().split('=')[1];
			if parent_id in id_transcript:
				parent_transcript=id_transcript[parent_id];
				transcript_positions[parent_transcript]["cds"]+=[l[3],l[4]]
	except: pass

print duplicate_count;

for t in transcript_positions:
	for x in ["cds","e_starts","e_stops"]:
		transcript_positions[t][x]=[int(a) for a in transcript_positions[t][x]]
	transcript_positions[t]["e_starts"].sort(); 
	transcript_positions[t]["e_stops"].sort(); 
	transcript_positions[t]["cds"].sort();
	for x in ["cds","e_starts","e_stops"]:
		transcript_positions[t][x]=[str(a) for a in transcript_positions[t][x]]
	formatted_starts=(",").join(transcript_positions[t]["e_starts"])
	formatted_stops=(",").join(transcript_positions[t]["e_stops"])
	if len(transcript_positions[t]["cds"])>1:
		out_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(t,transcript_positions[t]["chr"],transcript_positions[t]["sign"],
							transcript_positions[t]["cds"][0], transcript_positions[t]["cds"][-1], formatted_starts,formatted_stops))
