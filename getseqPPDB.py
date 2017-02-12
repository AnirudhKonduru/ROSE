'''
Gets 2kb upstream of given seq from plantGDB.org

'''
import requests as rq
from BeautifulSoup import BeautifulSoup as BSHTML
import xlrd as xl
import os
from BioMod import Seq

def get_seq(chr_no, start, size):
    #hits' is of the form "3:3676292:3678292"
    if(size<0):
        size = -size
        #excludes the base at reg_seq_start
        hits = str(chr_no)+":"+str(start-size)+":"+str(start-1)
    else:
        #includes the base at reg_seq_start
        hits = str(chr_no)+":"+str(start)+":"+str(start+size-1)
    print "hits: "+hits
    params = {'program':'returnFASTA',
    'db':'GENOME',
    'dbid':'4',
    "hits":hits,
    "DBpath":"/DATA/PlantGDB/Index/Blast/OsGDB/OSgenome",
    "xGDB":"OsGDB"}

    r = rq.post('http://www.plantgdb.org/OsGDB/cgi-bin/formatReader.pl',
                data = params)
    html_resp = r.content

    bs = BSHTML(html_resp)
    fasta_string = bs.pre.contents[0].strip()
    return fasta_string


promoter_db = xl.open_workbook("pd.xlsx")
segregated_db = xl.open_workbook("segregated_genes.xlsx")

print "opening xlsx"

NA_u2_sheet = promoter_db.sheet_by_name("up>2")
fold_up2_sheet = segregated_db.sheet_by_name("fold change_up>2")


print NA_u2_sheet.nrows
print NA_u2_sheet.ncols
print fold_up2_sheet.nrows
print fold_up2_sheet.ncols

print "Enter Output File Name: "
op_file = raw_input()
if op_file == "":
    f = open('NA.fasta', 'w')
else:
    f = open(op_file, 'w')
x=0

NA_list = []
for i in range(1,NA_u2_sheet.nrows):
    '''seq from not_available col'''
    NA_seq = NA_u2_sheet.cell(i,8).value
    if NA_seq != "":
        if NA_seq not in NA_list:
            NA_list.append(NA_seq)
        else:
            print "repeated: " + NA_seq

print "NA list: "+str(len(NA_list))

for NA_seq in NA_list:
    for j in range(1, fold_up2_sheet.nrows):
        accession = fold_up2_sheet.cell(j,18).value
        if NA_seq in accession:
            chr_no = fold_up2_sheet.cell(j,21).value
            start_no = fold_up2_sheet.cell(j,22).value
            if chr_no=="" or start_no=="":
                print "Chromosome No or start No for "+NA_seq+" not available\n"
                break;
            chr_no = int(chr_no[-2:])
            start_no = int(start_no)
            print NA_seq
            x = x+1
            fasta = get_seq(chr_no, start_no, -2000)+'\n'
            #new = Seq.from_fasta(fasta)
            #new.id = NA_seq
            #new.chr = chr_no
            #new.pos = start_no
            id_line, seq = fasta.split("\n",1)
            id_line = ">"+NA_seq+" "+str(chr_no)+" "+str(start_no)+"\n"
            #seq = id_line + seq
            new = Seq(NA_seq, seq.strip('\n'), chr_no, start_no)
            f.write(new.fasta())
            '''print get_seq(chr_no, start_no, 2000)'''
            print "Done: "+str(x)
            break

print str(x)+" Entries added\n"
