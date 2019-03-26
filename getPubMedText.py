
from Bio import Entrez
from Bio import Medline
import numpy as np

def search(query):
    Entrez.email = 'galiasn"gmal.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='pub+date',
                            retmode='xml',
                            term=query,
                            retmax=10000)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'galiasn@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids,
                           retmax=10000)
    results = Entrez.read(handle)
    return results


def getyear(pid):
    print(pid)
    if pid not in publictionDate.keys():
        print('00')
        return '00'
    else:
        print(publictionDate[pid])
        return publictionDate[pid]




Abstracts =[]
startDate = '2016/01/01'
endDate = '2017/01/01'

count=0


idresults=[]
query = '('+startDate+'[PDAT]:'+endDate+'[PDAT])'

res = search(query)
if len(res['IdList'])>0:
    idresults+= res['IdList']
else:
    idresults.append('0')



papers = fetch_details(','.join(idresults))
for i, paper in enumerate(papers['PubmedArticle']):
    #Abstracts.append(paper['MedlineCitation']['Article']['ArticleTitle'])
    if 'Abstract' in paper['MedlineCitation']['Article'].keys():
        print("abstract")
        abst = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0].split('.')
        for abs in abst:
            Abstracts.append(abs)
    #publictionDate.append(paper['DateCompleted'])
    '''
    if 'DateCompleted' in paper['MedlineCitation'].keys():
        publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]=paper['MedlineCitation']['DateCompleted']['Year']
    else:
        if 'DateRevised' in paper['MedlineCitation'].keys():
            publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]=paper['MedlineCitation']['DateRevised']['Year']
        else:
            print("*")
            publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]='0'
    '''
    print(count)
    count+=1


