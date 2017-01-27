from BioMod import Seq

def read_fasta_file(file_name):
    with open(file_name, "r") as f:
        fastas = []
        new = "default"
        for line in f:
            if line[0]=='>':
                fastas.append(new)
                new=line
            else:
                new = new+line
        fastas.remove("default")
    return fastas

def get_hamming(str1, str2, max_hamming=-1):
    leng = min(len(str1),len(str2))
    if max_hamming==-1:
        max_hamming=leng;
    err = 0;
    for i in range(0,leng):
        if str1[i] != str2[i]:
            err += 1
            if err>max_hamming:
                return -1
    return err

seqs = map(Seq.from_fasta, read_fasta_file("nodupv4.fasta"))
print [x.fasta()+"\n" for x in seqs[0:3]]
print "fasta"
octs = map(Seq.from_fasta, read_fasta_file("rose.fasta"))
entries = 0
f = open("find_rose_flaking.fasta",'w')


for o in octs:
    for s in seqs:
        for i in range(0,s.len() - o.len() -1):
            sub_seq = s.seq[i:i+o.len()]
            if get_hamming(o.seq, sub_seq, max_hamming=0) != -1:
                print sub_seq+"\n"+o.seq+"\n"

                #extract flanking reqions
                #f.write(str(i))
                new = Seq(o.id+"|"+s.id, s.seq[i-2:i+o.len()+2], s.chr, s.pos-5+i)
                #new = Seq(o.id+"|"+s.id, s.seq[i:i+o.len()], s.chr, s.pos)

                f.write(new.fasta())
                entries += 1
                print "Entry No: " + str(entries)
