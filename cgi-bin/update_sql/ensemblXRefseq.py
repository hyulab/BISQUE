from os import system, path
import glob
import MySQLdb as mdb 
import sys 
import re
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import User
con = mdb.connect(User.get_address(), User.get_username(), User.get_password(), "bisque")


file_handle = open('%s/data/ncbi/unzipped/gene2ensembl' %(parentdir), 'r')
appension_file = open('%s/data/misc/unzipped/ensemblxrefSeqAppension.txt'%parentdir, 'r')
# DICTIONARY INSTANTIATIONS
reftEnst={}; enstReft={};
enspRefp={}; refpEnsp={};

#PRIMARY FILE
for l in file_handle:
    if re.match(r'^ENST[0-9]{11,11}$',l.strip().split()[4], re.IGNORECASE) and re.match(r'^NM_[0-9]*\.[0-9]*',l.strip().split()[3], re.IGNORECASE):
        enst=l.strip().split()[4]; reft=l.strip().split()[3];
        # Append to dict 1
        if reft not in reftEnst: reftEnst[reft]=[];
        reftEnst[reft].append(enst);
        # Append to dict 2
        if enst not in enstReft: enstReft[enst]=[];
        enstReft[enst].append(reft);
    if re.match(r'^ENSP[0-9]{11,11}$',l.strip().split()[6], re.IGNORECASE) and re.match(r'^NP_[0-9]*\.[0-9]*',l.strip().split()[5], re.IGNORECASE):
        ensp=l.strip().split()[6]; refp=l.strip().split()[5];
        #Append to dict 1
        if ensp not in enspRefp: enspRefp[ensp]=[];
        enspRefp[ensp].append(refp);
        #Append to dict 2
        if refp not in refpEnsp: refpEnsp[refp]=[];
        refpEnsp[refp].append(ensp);

#SUPPLEMENTARY FILE
for l in appension_file:
    l = l.strip().split(",")
    try: l.remove('')
    except: pass
    if len(l) < 2: continue
    enst = l[0]
    reft = l[1]
    #Append version number to reft, if possible
    found = False
    for i in range(1,30):
        if reft+"." + str(i) in reftEnst:
            reft = reft+"." + str(i)
            found = True
            break
    #Merge with enstReft
    if enst not in enstReft:
        enstReft[enst] = []
    if reft not in enstReft[enst]:
        enstReft[enst].append(reft)
    #Merge with reftEnst
    if reft not in reftEnst:
        reftEnst[reft] = []
    if enst not in reftEnst[reft]:
        reftEnst[reft].append(enst)


with con:
    cur = con.cursor()
    #ENSEMBL TO REFSEQ
    tables={"enst":"reft","ensp":"refp"}
    for typ in tables:
        table="%s_%s"%(typ,tables[typ])
        table_schema='%s CHAR(15) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL'%(typ,tables[typ]);
        try:cur.execute("drop table %s" %(table))
        except: pass
        cur.execute("create table %s (%s)" %(table, table_schema))
        dic=enstReft if typ=="enst" else enspRefp;
        for x in dic:
            cur.execute("insert into %s (%s,%s) values ('%s','%s')"%(table,typ,tables[typ],x,('\t').join([a for a in dic[x]])));


    #REFSEQ TO ENSEMBL
    tables={"reft":"enst","refp":"ensp"}
    for typ in tables:
        table="%s_%s"%(typ,tables[typ])
        table_schema='%s VARCHAR(40) PRIMARY KEY NOT NULL, %s TEXT(1000) NOT NULL'%(typ,tables[typ]);
        try:cur.execute("drop table %s" %(table))
        except: pass
        cur.execute("create table %s (%s)" %(table, table_schema))
        dic=reftEnst if typ=="reft" else refpEnsp;
        for x in dic:
            cur.execute("insert into %s (%s,%s) values ('%s','%s')"%(table,typ,tables[typ],x,('\t').join(dic[x])));
