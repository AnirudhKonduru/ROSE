import requests as rq
from bs4 import BeautifulSoup as BS
import os
import shutil
from urlparse import urljoin

def downloadMolfile(link, filepath=os.getcwd()):
    r = rq.post(link)
    soup = BS(r.content,"html.parser")
    a_tag = soup.find('a', {"title":"Save Molfile to disk"})
    if a_tag==None:
        print "FAILED: "+link
        return False
    dl_link = urljoin(link,a_tag['href'])
    response = rq.post(dl_link)
    file_name = response.headers["Content-Disposition"]
    file_name = file_name[file_name.find("filename=")+9:]
    print "Downloading: "+file_name
    with open(file_name,'wb') as f:
        f.write(response.content)
    return True



base_url = "http://www.ebi.ac.uk"
OP_FOLDER = "./getLigandsOutput"

#make output folder
if(os.access(OP_FOLDER, os.F_OK)==True):
    shutil.rmtree(OP_FOLDER)
os.mkdir(OP_FOLDER)
os.chdir(OP_FOLDER)

links = {"link1":"http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:27171"}

for link in links:
    os.mkdir(link)
    os.chdir(link)
    r = rq.post(links[link])
    soup = BS(r.content, "html.parser")

    #getting list of links by parsing html, going inwards 1 tag at a time
    #TODO: clean this up
    div = soup.find("div", {"class":"grid_24 clearfix", "id":"content"})
    table = div.find_all("table", recursive=False)[1]
    X = table.tr.td
    t = X.find_all("table",recursive=False)[1]
    tr4 = t.find_all("tr",recursive=False)[3]
    td2 = tr4.find_all("td",recursive=False)[1]
    hrefs=td2.find_all('a', href=True)

    ligand_pages = []
    for i in range(0,len(hrefs),2):
        ligand_pages.append(base_url+hrefs[i]['href'])

    download_count=0
    for link in ligand_pages:
        if(downloadMolfile(link)==True):
            download_count+=1
    print "Total Files Downloaded: "+str(download_count)
    print "Total Files: "+str(len(ligand_pages))

    os.chdir("..")
