# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:35:47 2019

@author: Galia
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:46:01 2019

@author: Galia
"""

import pandas as pn

pmid = pn.read_csv("D:\\Galia\\mechanismBased\\DistinctPMID.csv")

#find year of publication for each pmid
pmid['PMID'] = pmid['PMID'].apply(str)

allpmidlist = pmid['PMID'].unique()
allpmidlist2 = pmid[pmid['PMID'].isin(existingpmid)==False]['PMID'].unique()
allpmidlist = allpmidlist2
#fetch details 1000 papers at a time
pmidYears = {}
startind = 0
endInd = 1000
while endInd<len(allpmidlist):
    if endInd>=len(allpmidlist):
        endInd=len(allpmidlist)-1
    print(startind)    
    pmidlist=allpmidlist[startind:endInd]
    papers = fetch_details(pmidlist)
    for i, paper in enumerate(papers['PubmedArticle']):
    #publictionDate.append(paper['DateCompleted'])
        if 'DateCompleted' in paper['MedlineCitation'].keys():
            pmidYears[str(paper['PubmedData']['ArticleIdList'][0])]=int(paper['MedlineCitation']['DateCompleted']['Year'])
        else:
            if 'DateRevised' in paper['MedlineCitation'].keys():
               pmidYears[str(paper['PubmedData']['ArticleIdList'][0])]=int(paper['MedlineCitation']['DateRevised']['Year'])
            else:
                pmidYears[str(paper['PubmedData']['ArticleIdList'][0])]=0 
    startind = endInd
    endInd = endInd+1000      

pmidYearsDF = pn.DataFrame()
pmidYearsDF['mid'] = list(pmidYears.keys())
pmidYearsDF['year'] = pmidYears.values()
pmidYearsDF.to_csv('D:\\Galia\\mechanismBased\\PMIDYear_9.csv')

pmid1 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_1.csv')
pmid2 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_2.csv')
pmid3 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_3.csv')
pmid4 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_4.csv')
pmid5 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_5.csv')
pmid6 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_6.csv')
pmid7 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_7.csv')
pmid8 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_8.csv')
pmid9 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_9.csv')

pmid1['mid'] = pmid1['mid'].apply(str)
pmid2['mid'] = pmid2['mid'].apply(str)
pmid3['mid'] = pmid3['mid'].apply(str)
pmid4['mid'] = pmid4['mid'].apply(str)
pmid5['mid'] = pmid5['mid'].apply(str)
pmid6['mid'] = pmid6['mid'].apply(str)
pmid7['mid'] = pmid7['mid'].apply(str)
pmid8['mid'] = pmid8['mid'].apply(str)
existingpmid = set(pmid1['mid'].unique()).union(set(pmid2['mid'].unique())).union(set(pmid3['mid'].unique())).union(set(pmid4['mid'].unique())).union(set(pmid5['mid'].unique())).union(set(pmid6['mid'].unique())).union(set(pmid7['mid'].unique())).union(set(pmid8['mid'].unique()))