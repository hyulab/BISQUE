# This file contains functions which are used for chunking and decuhking transcript positions with respect to their chromosomes
import MySQLdb as mdb 
import User

con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")



codon_dict = {'CTT': 'L', 'ATG': 'M', 'AAG': 'K', 'AAA': 'K', 'ATC': 'I', 'AAC': 'N', 'ATA': 'I', 'AGG': 'R', 'CCT': 'P', 'ACT': 'T', 
'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'CAT': 'H', 'AAT': 'N', 'ATT': 'I', 'CTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CAC': 'H', 
'ACG': 'T', 'CAA': 'Q', 'AGT': 'S', 'CAG': 'Q', 'CCG': 'P', 'CCC': 'P', 'TAT': 'Y', 'GGT': 'G', 'TGT': 'C', 'CGA': 'R', 
'CCA': 'P', 'TCT': 'S', 'GAT': 'D', 'CGG': 'R', 'TTT': 'F', 'TGC': 'C', 'GGG': 'G', 'TAG': '*', 'GGA': 'G', 'TAA': '*', 
'GGC': 'G', 'TAC': 'Y', 'GAG': 'E', 'TCG': 'S', 'TTA': 'L', 'GAC': 'D', 'TCC': 'S', 'GAA': 'E', 'TCA': 'S', 'GCA': 'A', 
'GTA': 'V', 'GCC': 'A', 'GTC': 'V', 'GCG': 'A', 'GTG': 'V', 'TTC': 'F', 'GTT': 'V', 'GCT': 'A', 'ACC': 'T', 'TGA': '*', 
'TTG': 'L', 'CGT': 'R', 'TGG': 'W', 'CGC': 'R'}



def complement(seq, verbosity=0):
    if verbosity > 0: print "Producing Complement..."
    comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N':'N'}
    comp_seq = ''
    for c in seq:
        comp_seq += comp_dict[c]
    return comp_seq




def get_sign(id_type, value, cur): #Takes in an ENST and determines whether	 it is on the minus or the plus strand
    if "19" in id_type: id_type=id_type.split("_")[1];
    cur.execute("select sign from %s_seq where %s = '%s'" %(id_type, id_type, value))
    rows = cur.fetchall()
    if len(rows) == 0:
        return "+"
    elif len(rows) == 1:
        sign = rows[0][0]
        return sign 

def get_chunks(transcript_type, transcript, cur):
    cur.execute("select * from %s_pos where transcript = '%s'" %(transcript_type, transcript))
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    elif len(rows) == 1:
        rows = rows[0]
        cdstart = int(rows[1])
        cdstop = int(rows[2])
        exon_starts = [int(x) for x in rows[3].split()]
        exon_stops = [int(x) for x in rows[4].split()]
        exon_starts.sort(); exon_stops.sort();
        range_list = []
        started = False; stop = False

        for i in range(len(exon_starts)):
            rang = [exon_starts[i], exon_stops[i]] #We wrap in int
            if cdstart >= exon_starts[i] and cdstart <= exon_stops[i]:
                rang[0] = cdstart
                started = True
            if cdstop >= exon_starts[i] and cdstop <= exon_stops[i]:
                rang[1] = cdstop
                stop = True
            if started:
                range_list.append(rang)
            if stop:
                break
        return range_list


def get_ncds_chunks(transcript_type,transcript,cur):
    cur.execute("select exonstarts,exonstops from %s_pos where transcript = '%s'" %(transcript_type, transcript))
    rows=cur.fetchall()
    if len(rows)==0:
        return None
    rows=rows[0];
    exonstarts=[int(x) for x in rows[0].split('\t')]; 
    exonstarts.sort()
    exonstops=[int(x) for x in rows[1].split('\t')];
    exonstops.sort()
    return [[exonstarts[i],exonstops[i]] for i in range(len(exonstarts))];
# result = [[int(rows[0].split('\t')[i]),int(rows[1].split('\t')[i])] for i in range(len(rows[0].split('\t')))]
    # return result;




#Takes in a chromosome position and transcript id, and returns the relative position on the transcript
def chunk_position(chrpos, transcript, transcript_type, cur):
    #Deprecated hg19 support
    ranges=get_chunks(transcript_type, transcript, cur)
    if not ranges: return None 
    counter = 0 
    #Iterate through chunk ranges for +
    if get_sign(transcript_type, transcript, cur) == "+":
        for r in ranges:
            if r[0] <= chrpos and chrpos <= r[1]:
                return (counter + chrpos - r[0]) + 1
            else: counter += r[1] - r[0] + 1
    #Iterate through chunk ranges for -
    else:
        ranges.reverse()
        for r in ranges:
            if r[0] <= chrpos and chrpos <= r[1]:
                return (counter + r[1] - chrpos) + 1
            else: counter+=r[1]-r[0]+1


#Takes in a relative transcript position and a transcript, and returns the absolute position on the chromosome
def dechunk_position(tpos, transcript, transcript_type, cur):
    #Deprecated hg19 support
    ranges=get_chunks(transcript_type,transcript,cur)
    if ranges == None: return None;

    tpos = tpos-1 #0-index the tpos for simpler calculations
    #Iterate through chunks ranges for +
    if get_sign(transcript_type, transcript, cur) == '+':
        for r in ranges:
            if 0 <= tpos and tpos <= (r[1]-r[0]):
                return r[0] + tpos 
            else:
                tpos = tpos - (r[1]-r[0]) - 1

    else:
        ranges.reverse()
        for r in ranges: 
            if 0 <= tpos and tpos <= (r[1]-r[0]):
                return r[1]-tpos
            else:
                tpos = tpos - (r[1]-r[0])-1
    return None


#Chunks chromosome position onto ncds sequence of transcrit
def chunk_ncds_position(chrpos, transcript, transcript_type, cur):
    #Deprecated hg19 support
    ranges=get_ncds_chunks(transcript_type, transcript, cur)
    if not ranges: return None 
    counter = 0 
    #Iterate through chunk ranges for +
    if get_sign(transcript_type, transcript, cur) == "+":
        for r in ranges:
            if r[0] <= chrpos and chrpos <= r[1]:
                return (counter + chrpos - r[0]) + 1
            else: counter += r[1] - r[0] + 1
    #Iterate through chunk ranges for -
    else:
        ranges.reverse()
        for r in ranges:
            if r[0] <= chrpos and chrpos <= r[1]:
                return (counter + r[1] - chrpos) + 1
            else: counter+=r[1]-r[0]+1

def dechunk_ncds_position(tpos, transcript, transcript_type, cur):
    #Deprecated hg19 support
    ranges=get_ncds_chunks(transcript_type,transcript,cur)
    if ranges == None: return None;
    tpos = tpos -1 #0-index the tpos for simpler calculations
    #Iterate through chunks ranges for +
    if get_sign(transcript_type, transcript, cur) == '+':
        for r in ranges:
            if 0 <= tpos and tpos <= (r[1]-r[0]):
                return r[0] + tpos 
            else:
                tpos = tpos - (r[1]-r[0]) - 1

    else:
        ranges.reverse()
        for r in ranges: 
            # print 0,tpos,r[1]-r[0]
            if 0 <= tpos and tpos <= (r[1]-r[0]):
                return r[1]-tpos
            else:
                tpos = tpos - (r[1]-r[0])-1
