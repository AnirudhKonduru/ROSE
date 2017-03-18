import regex as re

class Seq(object):
    def __init__(self,id,seq, chr=-1, pos=-1, pos_end=-1,header_string=""):
        self.seq = seq
        self.id = id
        self.chr = chr
        self.pos = pos
        self.pos_end = -1
        self.header_string = header_string
        if header_string=="":
            self.header_string=str(self.id)+" "+str(self.chr)+" "+str(self.pos)+'\n'

    def __str__(self):
        res = self.header_string+'\n'
        if self.len()<20:
            res+=self.seq
        else:
            res +=self.seq[:10]+"......"+self.seq[-10:]
        return res

    def __repr(self):
        return self.__str__()
#converts singe fasta string to Seq object
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
        if len(header_items)>=3:
            chr = int(header_items[1])
            pos = int(header_items[2])
            return Seq(id,seq,chr,pos, header_string=lines[0])
        else:
            return Seq(id,seq)

    def fasta(self):
        fasta = ">"+self.id+" "+str(self.chr)+" "+str(self.pos)+"\n"
        seq = '\n'.join(self.seq[i+i/70:i+70+i/70] for i in xrange(0,len(self.seq),70))
        fasta += seq+'\n'
        return fasta

    def len(self):
        return len(self.seq)

#converts string with iupac nucleotide codes to regex strings
    def regex(self):
        return seq2regex(self.seq)

def seq2regex(seq):
    regex_seq = regex_seq
    regex_seq = regex_seq.replace('R','[AG]')
    regex_seq = regex_seq.replace('Y','[CT]')
    regex_seq = regex_seq.replace('S','[GC]')
    regex_seq = regex_seq.replace('W','[AT]')
    regex_seq = regex_seq.replace('K','[GT]')
    regex_seq = regex_seq.replace('M','[AC]')
    regex_seq = regex_seq.replace('B','[CGT]')
    regex_seq = regex_seq.replace('D','[AGT]')
    regex_seq = regex_seq.replace('H','[ACT]')
    regex_seq = regex_seq.replace('V','[ACG]')
    regex_seq = regex_seq.replace('N', '[ATGC]')
    return regex_seq

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


#finds all occurences of needle in haystack
#returns list of start positions in haystack string
def findSeq(needle, haystack, regex=True):
    if regex==True:
        needle_r = re.compile(needle.regex())
        matches = needle_r.finditer(haystack.seq, overlapped=True)
        return [x.start() for x in matches]

def read_fasta(fasta_str=""):
    #reads and returns a list of strings,
    #each string is one fasta Entry
    fastas = []
    new = "default"
    lines = [x+'\n' for x in fasta_str.split('\n')]
    for line in lines:
        if line=="\n" or line=="":
            continue
        if line[0]=='>':
            fastas.append(new)
            new=line
        else:
            new = new+line
    fastas.append(new)
    fastas.remove("default")
    #converts each fasta string to Seq object, returhs list
    return [Seq.from_fasta(x) for x in fastas]

def read_fasta_file(fasta_file):
        f = open(fasta_file, 'r')
        file_str = f.read()
        return read_fasta(file_str)
