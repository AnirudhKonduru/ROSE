from BioMod import *
import csv

fnames = ["up sus", "down sus", "up tol", "down tol"]

#read all 2k seq fasta files
HS = {  "up sus":read_fasta_file("../2kseqs/up_sus.fasta"),
        "down sus":read_fasta_file("../2kseqs/down_sus.fasta"),
        "up tol":read_fasta_file("../2kseqs/up_tol.fasta"),
        "down tol":read_fasta_file("../2kseqs/down_tol.fasta")
}

#read cis element fastas corresponding to fastas in HS
NS = {  "up sus":read_fasta_file("../cis_elements_sus.fasta"),
        "down sus":read_fasta_file("../cis_elements_sus.fasta"),
        "up tol":read_fasta_file("../cis_elements_tol.fasta"),
        "down tol":read_fasta_file("../cis_elements_tol.fasta")

}

for fname in fnames:
    hs = HS[fname]
    ns=NS[fname]
    f = open(fname+".csv", 'wb')
    writer = csv.writer(f)
    total_count =0;
    n_count=0

    for n in ns:
        n_count=0
        for h in hs:
            matches = findSeq(n,h,regex=True)
            for x in matches:
                total_count+=1
                n_count+=1
                #modify csv entry and counts as needed
                '''
                #for csv of all matches
                csv_entry = [n.id,n.seq,h.id,h.seq[x:x+len(n.seq)],x]
                writer.writerow(csv_entry)
                '''
        csv_entry=[n.id,n.seq,n_count]
        writer.writerow(csv_entry)

    print fname
    print "matches: "+str(total_count)
    print "total needles: "+str(len(ns))
    print "total haystacks: "+str(len(hs))
