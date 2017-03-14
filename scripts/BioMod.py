import regex as re

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

#converts string with iupac nucleotide codes to regex strings
def seq2regex(seq):
    seq = seq.replace('R','[AG]')
    seq = seq.replace('Y','[CT]')
    seq = seq.replace('S','[GC]')
    seq = seq.replace('W','[AT]')
    seq = seq.replace('K','[GT]')
    seq = seq.replace('M','[AC]')
    seq = seq.replace('B','[CGT]')
    seq = seq.replace('D','[AGT]')
    seq = seq.replace('H','[ACT]')
    seq = seq.replace('V','[ACG]')
    seq = seq.replace('N', '[ATGC]')
    return seq

#finds all occurences of needle in haystack
#returns list of start positions in haystack string
def findSeq(needle, haystack, regex=True):
    if regex==True:
        needle_r = re.compile(seq2regex(needle))
        matches = needle_r.finditer(haystack, overlapped=True)
        return [x.start() for x in matches]
