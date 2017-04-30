import requests as rq
from bs4 import BeautifulSoup as BS
import os
import shutil
from urlparse import urljoin

def downloadMolfile(link, filepath=os.getcwd()):
    #extract molfile html soup
    r = rq.post(link)
    soup = BS(r.content,"html.parser")

    #attempt to find download link to molfile
    a_tag = soup.find('a', {"title":"Save Molfile to disk"})
    #notify of failure of download link doesnt exist
    if a_tag==None:
        print "FAILED: "+link
        return False

    #generate absolute link from relative
    dl_link = urljoin(link,a_tag['href'])
    #get file as html response
    response = rq.post(dl_link)

    #Extract file name from content desposition in response header
    file_name = response.headers["Content-Disposition"]
    file_name = file_name[file_name.find("filename=")+9:]
    print "Downloading: "+file_name

    #write to file on disk
    with open(file_name,'wb') as f:
        f.write(response.content)
    return True



OP_FOLDER = "./getLigandsOutput"
base_url = "http://www.ebi.ac.uk"

#make output folder, delete it first if already exists
if(os.access(OP_FOLDER, os.F_OK)==True):
    shutil.rmtree(OP_FOLDER)
os.mkdir(OP_FOLDER)
os.chdir(OP_FOLDER)

#hash table with all the links as key:value pairs
links = {"link1":"http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:27171"}

#interate over the links
for link in links:
    #make a folder for each link
    os.mkdir(link)
    os.chdir(link)

    #request for html content of link
    r = rq.post(links[link])
    soup = BS(r.content, "html.parser")

    # extracting a list of links to molfile download pages
    # by parsing html, going inwards 1 html tag at a time
    div = soup.find("div", {"class":"grid_24 clearfix", "id":"content"})
    top_lvl_table = div.find_all("table", recursive=False)[1]
    bot_lvl_table = top_lvl_table.tr.td
    table = bot_lvl_table.find_all("table",recursive=False)[1]
    tr4 = table.find_all("tr",recursive=False)[3]   #GOTO 4TH tr
    td2 = tr4.find_all("td",recursive=False)[1]     #GOTO 2ND td
    #get list of relative hrefs
    hrefs=td2.find_all('a', href=True)

    ligand_pages = []
    #generating the absolute page links from relative links
    for i in range(0,len(hrefs),2):
        ligand_pages.append(base_url+hrefs[i]['href'])

    download_count=0
    #for each absolute link, attempt download
    for link in ligand_pages:
        if(downloadMolfile(link)==True):
            download_count+=1
    #print stats
    print "Total Files Downloaded: "+str(download_count)
    print "Total Files: "+str(len(ligand_pages))

    #return to root dir
    os.chdir("..")
