import BioMod as BM
from BioMod import Seq
import re

haystack_fname = raw_input("Haystack: ")
needle_fname = raw_input("Needle: ")

seqs = map(Seq.from_fasta, BM.read_fasta_file(haystack_fname))
print [x.fasta()+"\n" for x in seqs[0:3]]
octs = map(Seq.from_fasta, BM.read_fasta_file(needle_fname))
entries = 0

op_fname = raw_input("Output File Name: ")
if op_fname=="":
    f = open("find_match.out",'w')
else:
    f = open(op_fname,'w')

for o in octs:
    for s in seqs:
        for i in range(0,s.len() - o.len() -1):
            sub_seq = s.seq[i:i+o.len()]
            if BM.get_hamming(o.seq, sub_seq, max_hamming=0) != -1:
                print sub_seq+"\n"+o.seq+"\n"

                #extract flanking reqions
                #f.write(str(i))
                new = Seq(o.id+"|"+s.id, s.seq[i-2:i+o.len()+2], s.chr, s.pos-5+i)
                #new = Seq(o.id+"|"+s.id, s.seq[i:i+o.len()], s.chr, s.pos)

                f.write(new.fasta())
                entries += 1
                print "Entry No: " + str(entries)
