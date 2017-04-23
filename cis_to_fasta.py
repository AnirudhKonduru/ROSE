import xlrd as xl



wb = xl.open_workbook("tol sus genes cis elements.xlsx")

s = wb.sheet_by_name("tol gene")

def switcher(s):
    y=''
    m={
    'A':'T','T':'A',
    'C':'G','G':'C',
    'N':'N',
    'R':'Y','Y':'R',
    'W':'W','S':'S',
    'K':'M','M':'K',
    'B':'V','V':'B',
    'D':'H','H':'D',
    }
    for i in range(0,len(s)):
        y+=m[s[i]]
    return y

num=1
k=0
l=[]
for i in range(4,69,7):
    m={}

    for j in range(2,99):
        name=str(s.cell(0,k).value)+'.'+str(num)
        y=str(s.cell(j,i).value)
        if str(s.cell(j,i-2).value)=='(-)':
            y=switcher(y)
        if y!= '' and y not in m:
            m.update({y:name})
            num=num+1
            # print m
    l.append(m)
    k=k+7

f=open('cis_elements_tol.fasta','w')
for i in range (0,len(l)):
    for j in range (0,len(l[i])):
        f.write('>'+l[i].values()[j]+'\n'+l[i].keys()[j]+'\n')
