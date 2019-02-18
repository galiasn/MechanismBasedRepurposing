# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:43:51 2019

Cut the data according to dates of approval and see if we can predict repurposing candidates.
"""
import pandas as pn
import matplotlib.pyplot as plt

#repo = pn.read_csv("C:\\Users\\Galia\\Downloads\\repoyearWYear.csv") 
#repo = pn.read_csv("D:\\Galia\\mechanismBased\\PushpakumT1.csv") 

#add indications to repo
repo = pn.read_csv("D:\\Galia\\mechanismBased\\repoyearWYear.csv")
full = pn.read_csv("D:\\Galia\\mechanismBased\\full.csv")

repo = pn.merge(repo,full[['ind_name','ind_id']],on='ind_name',how='inner')
repo = repo[['drug_id','drug_name','ind_name','ind_id','pubYear']]
repo = repo.drop_duplicates()
repo.to_csv("D:\\Galia\\mechanismBased\\repoyearWYear_indID.csv")


repo = pn.read_csv("D:\\Galia\\mechanismBased\\repoyearWYear_indID.csv") 
#repo = pn.read_csv("D:\\Galia\\mechanismBased\\PushpakumT1.csv") 

repo = repo[repo['pubYear']>0]
#remove anything after cutYear

cutYear = 1990
repoBefore = repo[repo['pubYear']<cutYear]
repoAfter = repo[repo['pubYear']>=cutYear]


repurposed_names = set(repoBefore['drug_name'].unique()).intersection(set(repoAfter['drug_name'].unique()))


#now look at pubmed publications dates
pmid1 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_1.csv')
pmid2 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_2.csv')
pmid3 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_3.csv')
pmid4 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_4.csv')
pmid5 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_5.csv')
pmid6 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_6.csv')
pmid7 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_7.csv')
pmid8 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_8.csv')
pmid9 = pn.read_csv('D:\\Galia\\mechanismBased\\PMIDYear_9.csv')

pmid = pmid1.copy()
pmid = pmid.append(pmid2)
pmid = pmid.append(pmid3)
pmid = pmid.append(pmid4)
pmid = pmid.append(pmid5)
pmid = pmid.append(pmid6)
pmid = pmid.append(pmid7)
pmid = pmid.append(pmid8)
pmid = pmid.append(pmid9)

pmid = pmid[['mid','year']]
pmid = pmid.drop_duplicates()

pmidBefore = pmid[pmid['year']<cutYear]['mid'].unique()


