import re
#File which assists with data parsing + Regex analysis

def parse_identifier(id, cur):
    referenceId = None
    type = None
    if re.match(r'^ENST[0-9]{11,11}', id, re.IGNORECASE):
        type = "enst"
    elif re.match(r'^ENSG[0-9]{11,11}', id, re.IGNORECASE):
        type = "ensg"
    elif re.match(r'^ENSP[0-9]{11,11}', id, re.IGNORECASE):
        type = "ensp"
    elif re.match(r'^chr.+', id, re.IGNORECASE):
        type = "hg38"
        id = id.lower()
    elif re.match(r'^[N,X][M]_[0-9]{5,9}.*[0-9]*', id, re.IGNORECASE):
        type = 'reft'
    elif re.match(r'^NP_[0-9]{1,20}.*[0-9]*', id, re.IGNORECASE):
        type = "refp"
    elif re.match(r'^rs[0-9]*$', id, re.IGNORECASE):
        type = "dbsnp";
    elif re.match(r'^\d$|^([1]\d$)|^([2][0-2]$)|^x$|^y$', id, re.IGNORECASE):
        type="hg38"; id="chr"+id; id=id.lower();
    elif re.match(r'^[0-9][a-z0-9]{3,5}',id,re.IGNORECASE):
        type = 'pdb';
        id=id[0:4].upper()+id[4:];
    elif re.match(r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}', id, re.IGNORECASE):
        type = "uniprot"	
    elif re.match(r'^[A-Z0-9-]+$|^C[0-9XY]+orf[0-9]+$',id, re.IGNORECASE):
        type="uniprot"
        cur.execute("select uniprot from geneName_uniprot where geneName='%s'"%id)
        rows=cur.fetchall();
        try:referenceId=rows[0][0];
        except:type=None;
    else:
        type = "uniprot"
    return {"type": type, "reference": referenceId, "formatted_id": id}
    
def parse_line(inpt, vcf=False):
    abbreviationToCode={
            'ala': 'A',
            'arg': 'R',
            'asn': 'N',
            'asp': 'D',
            'cys': 'C',
            'glu': 'E',
            'gln': 'Q',
            'gly': 'G',
            'his': 'H',
            'ile': 'I',
            'leu': 'L',
            'lys': 'K',
            'met': 'M',
            'phe': 'F',
            'pro': 'P',
            'ser': 'S',
            'thr': 'T',
            'trp': 'W',
            'tyr': 'Y',
            'val': 'V'
            }
    inpt=inpt.strip();
    position=None; mutation=None
	
    if vcf:
        # CASE A: 
        if inpt=="": return 
        # CASE B: BLANK
        elif inpt[0]=="#": return;

        # CASE 1: NO INPUT ID
        if inpt.split()[0]==".": return;
        # CASE 2: NO POSITION:
        elif inpt.split()[1]==".":
            id=inpt.split()[0]
        # CASE 4: MUTATIONS HAVE LENGTH > 1
        elif len(inpt.split()[3])>1 or len(inpt.split()[4])>1:
            id=inpt.split()[0]; position=int(inpt.split()[1]);
        # CASE 3: NO MUTATION:
        elif inpt.split()[3]=="." or inpt.split()[4]==".":
            id=inpt.split()[0]; position=int(inpt.split()[1])
            # CASE 4: ID, MUTATION AND POSITION ARE ALL THERE
        else:
            # If multiple mutations, append to input_array
            mutations=inpt.split()[4].split(",");
            if len(mutations)>1:
                for mut in mutations[1:]:
                    newInpt=inpt.split(); newInpt[4]=mut; input_array.append((" ").join(newInpt))

            id="chr" + inpt.split()[0]; position=int(inpt.split()[1]); mutation="%s%s"%(inpt.split()[3],mutations[0])

    else:
        # STEP 1: SPLIT BY PROPER DELIMETER
        splitInput=re.split('\s|\t|:|,', inpt, re.IGNORECASE)

        # STEP 2: SINGLING OUT ID
        id=splitInput[0];

        # STEP 3: PARSING OUT LOCUS AND MUTATION
        if len(splitInput)==3:
            position=splitInput[1]; mutation=splitInput[2];
        elif len(splitInput)==2:
            # MATCH OBJECTS
            section=splitInput[1]; 
            if len(section.split("."))>1: section=section.split(".")[1];
            case1=re.match(r'^[0-9]+$', section)
            case2=re.match(r'^([0-9]+)([a-z\*][>]?[a-z\*])$',section, re.IGNORECASE)
            case3=re.match(r'^([a-z\*])([0-9]+)([a-z\*])$', section, re.IGNORECASE)
            case4=re.match(r'^([a-z\*]{3,3})([0-9]+)([a-z\*]{3,3})$', section, re.IGNORECASE)

            # CASE 1: SECTION=100, I.E NO MUTATION
            if case1:
                position=section;
            # CASE 2: SECTION=100A>?C
            elif case2:
                position=case2.group(1); mutation=case2.group(2);
                # CASE 3: SECTION=A100C
            elif case3:
                position=case3.group(2); mutation="%s%s"%(case3.group(1), case3.group(3))
            # CASE 4: SECTION=Glu98Val
            elif case4:
                position=case4.group(2); mutation="%s%s"%(abbreviationToCode[case4.group(1).lower()],abbreviationToCode[case4.group(3).lower()])



    # BONUS: REMOVING > FROM MUTATION SO IT DOESN'T APPEAR IN OUTPUT
    try:mutation=mutation.replace(">","")
    except:pass

    # REMOVE MUTATION OF LENGTH GREATER THAN 2 SO IT DOESN'T DISPLAY IN OUTPUT PAGE
    if mutation and len(mutation)>2: mutation=None;
    return (id, position, mutation)
