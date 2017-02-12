import xlrd as xl
import os

os.listdir(os.curdir)
print "Enter File Name [Only .xlsx supported]"
filename = raw_input()

wb = xl.open_workbook(filename+".xlsx")
print type(wb)
sheet_names = wb.sheet_names()
print str(sheet_names)
select_sheet = raw_input()
sheet = wb.sheet_by_name(select_sheet)
print sheet.nrows
print sheet.ncols

print "Enter Column Number for Gene ID"
gene_col = int(raw_input())-1;
print "Enter Column Number for Sequences"
seq_col = int(raw_input())-1;

print "Enter Output File Name: "
op_file = raw_input()
if op_file == "":
    f = open('result2.fasta', 'w')
else:
    f = open(op_file, 'w')
entries=0
print "Starting at Column Number: "
rows_start = int(raw_input())
print "Upto Column Number: "
rows_end = int(raw_input())
if rows_end > sheet.nrows:
    rows_end = sheet.nrows
for i in range(rows_start-1,  rows_end):
    if sheet.cell(i, gene_col).value!='' and sheet.cell(i, seq_col).value!='':
        if sheet.cell(i, seq_col).value!='NONE':
            line = ">"+sheet.cell(i, gene_col).value.strip(' ')+"\n"
            line += sheet.cell(i, seq_col).value.strip(' ')+"\n"
            ascii_line = line.replace(u'\xa0',u'')
            f.write(ascii_line)
            entries+=1
print str(entries)+" entries addded."
