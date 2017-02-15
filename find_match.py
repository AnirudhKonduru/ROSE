import BioMod as BM
from BioMod import Seq

seqs = map(Seq.from_fasta, BM.read_fasta_file("NA.fasta"))
print [x.fasta()+"\n" for x in seqs[0:3]]
print "fasta"
octs = map(Seq.from_fasta, BM.read_fasta_file("octomers.fasta"))
entries = 0
f = open("test.fasta",'w')


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
