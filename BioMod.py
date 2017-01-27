class Seq(object):
    def __init__(self,id,seq, chr=-1, pos=-1, pos_end=-1):
        self.seq = seq
        self.id = id
        self.chr = chr
        self.pos = pos
        self.pos_end = -1;

    @classmethod
    def from_fasta(cls, fasta):
        lines = fasta.split("\n")
        seq = ""
        for i in range(1,len(lines)):
            seq += lines[i]
        header_items = lines[0].split(' ')
        #remove > at the beginning
        header_items[0] = header_items[0][1:]
        id = header_items[0]
        if len(header_items)==3:
            chr = int(header_items[1])
            pos = int(header_items[2])
            return Seq(id,seq,chr,pos)
        else:
            return Seq(id,seq)

    def fasta(self):
        fasta = ">"+self.id+" "+str(self.chr)+" "+str(self.pos)+"\n"
        seq = '\n'.join(self.seq[i+i/70:i+70+i/70] for i in xrange(0,len(self.seq),70))
        fasta += seq+'\n'
        return fasta

    def len(self):
        return len(self.seq)
