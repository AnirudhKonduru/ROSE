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


geneID_list = xl.open_workbook("../regulated_NF.xlsx")
microarray_db = xl.open_workbook("../tol genes.xlsx")

print "opening xlsx"

NA_sheet = geneID_list.sheet_by_name("up regulated tolerance")
microarray_sheet = microarray_db.sheet_by_name("Up")


print NA_sheet.nrows
print NA_sheet.ncols
print microarray_sheet.nrows
print microarray_sheet.ncols

print "Enter Output File Name: "
op_file = raw_input()
if op_file == "":
    f = open('PPDB.out', 'w')
    no_sufficient_data = open("PPDB.no_sufficient_data.out",'w')
    not_found = open("PPDB.not_found.out", 'w')
else:
    f = open(op_file+".fasta", 'w')
    no_sufficient_data = open(op_file+".no_sufficient_data.out",'w')
    not_found = open(op_file+"PPDB.not_found.out", 'w')
x=0

NA_list = []
for i in range(1,NA_sheet.nrows):
    '''seq from not_available col'''
    NA_seq = NA_sheet.cell(i,0).value
    if NA_seq != "":
        if NA_seq not in NA_list:
            NA_list.append(NA_seq)
        else:
            print "repeated: " + NA_seq

print "NA list: "+str(len(NA_list))


for NA_seq in NA_list:
    NA_found_flag = False
    for j in range(1, microarray_sheet.nrows):
        accession = microarray_sheet.cell(j,18).value
        if NA_seq in accession:
            NA_found_flag = True
            chr_no = microarray_sheet.cell(j,21).value
            start_no = microarray_sheet.cell(j,22).value
            if chr_no=="" or start_no=="":
                no_sufficient_data.write(NA_seq+'\n')
                #print "Chromosome No or start No for "+NA_seq+" not available\n"
                break;
            chr_no = int(chr_no[-2:])
            start_no = int(start_no)
            x = x+1
            print x
            fasta = get_seq(chr_no, start_no, -2000)+'\n'
            id_line, seq = fasta.split("\n",1)
            id_line = ">"+NA_seq+" "+str(chr_no)+" "+str(start_no)+"\n"
            #seq = id_line + seq
            new = Seq(NA_seq, seq.strip('\n'), chr_no, start_no)
            f.write(new.fasta())
            break
    if(NA_found_flag == False):
        not_found.write(NA_seq+"\n")
print str(x)+" Entries added\n"
