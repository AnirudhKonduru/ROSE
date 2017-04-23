import csv
import BioMod
import operator

fnames = ["up_sus", "down_sus", "up_tol", "down_tol"]

files = {}
readers = {}
for fname in fnames:
    files[fname] = open("../Results/cis_matches_counts/"+fname+".csv", 'rb')
    readers[fname] = csv.reader(files[fname], delimiter=',')

class motif(object):
    def __init__(self,seq, up_sus=0,down_sus=0,up_tol=0,down_tol=0):
        self.seq = seq
        self.counts = []
        self.up_sus=up_sus;
        self.down_sus=down_sus;
        self.up_tol=up_tol;
        self.down_tol=down_tol;

    def total_count(self):
        return self.up_sus+self.down_sus+self.up_tol+self.down_tol
    def __str__(self):
        return str(self.__repr__())
    def __repr__(self):
        return self.list()
    def list(self):
        return [self.seq, self.up_sus, self.down_sus, self.up_tol, self.down_tol, self.total_count()]

motifs = {}

for f in fnames:
    reader = readers[f]
    for row in reader:
        seq = row[1]
        if seq not in motifs:
            m = motif(seq)
            setattr(m,f,int(row[2]))
            motifs[seq]=m
        else:
            setattr(motifs[seq],f,int(row[2]))

with open("cis_all_counts.csv", 'wb') as cis_all_file:
    writer = csv.writer(cis_all_file, delimiter=',')

    for m in motifs:
        writer.writerow(motifs[m].list())

with open("cis_all_counts.csv", 'rb') as cis_all_file:
    reader_cis_all = csv.reader(cis_all_file, delimiter=',')
    sorted_motifs = sorted(reader_cis_all, key=lambda row: int(row[5]), reverse=True)
    #print sorted_motifs
    writer_cis_sorted = csv.writer(open("cis_all_sorted.csv",'wb'), delimiter=',')
    for m in sorted_motifs:
        print m
        writer_cis_sorted.writerow(m)
