# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:35:16 2019

@author: Galia
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 14:04:55 2019

@author: Galia
"""

from Bio import Entrez

def search(query):
    Entrez.email = 'galiasn"gmal.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='pub+date', 
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'galiasn@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
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
repo = pn.read_csv("D:\\Galia\\mechanismBased\\repo.csv")
repoIndresults=[]
index=0
while index<len(repo):
    term1 = repo.iloc[index]['drug_name']
    term2 = repo.iloc[index]['ind_name']

    term2 = term2.split(',')[0]
    query = term1+'[Title] AND '+term2+'[Title/Abstract]'
    res = search(query)
    if len(res['IdList'])>0:
        repoIndresults.append(res['IdList'][-1]) #last element in list
    else:
        repoIndresults.append('0')
    index+=1
    print(index)
repo['yearRes'] = repoIndresults
repo.to_csv("C:\\Users\\Galia\\Downloads\\repoyear.csv") 
repo = pn.read_csv("C:\\Users\\Galia\\Downloads\\repoyear.csv")
repo['yearRes'] = repo['yearRes'].apply(int)
repo = repo[repo['yearRes']>0].copy()
repo['yearRes'] = repo['yearRes'].apply(str)

count=0
publictionDate={}
papers = fetch_details(list(repo['yearRes']))
for i, paper in enumerate(papers['PubmedArticle']):
    #publictionDate.append(paper['DateCompleted'])
    if 'DateCompleted' in paper['MedlineCitation'].keys():
        publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]=paper['MedlineCitation']['DateCompleted']['Year']
    else:
        if 'DateRevised' in paper['MedlineCitation'].keys():
            publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]=paper['MedlineCitation']['DateRevised']['Year']
        else:
            print("*")
            publictionDate[str(paper['PubmedData']['ArticleIdList'][0])]='0' 
    print(count)
    count+=1        
repo['pubYear'] = repo['yearRes'].apply(getyear)
repo.to_csv("C:\\Users\\Galia\\Downloads\\repoyearWYear.csv") 

repo['count'] = [1]*len(repo)
repogb= repo.groupby(['drug_id'],as_index=False).sum()
repogb = repogb[repogb['count']>1]
repo = repo[repo['drug_id'].isin(repogb['drug_id'])]
repo.to_csv("C:\\Users\\Galia\\Downloads\\repowYear.csv")

