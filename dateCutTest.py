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
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearwYear.csv")
full = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/full.csv")

repo = pn.merge(repo,full[['ind_name','ind_id']],on='ind_name',how='inner')
repo = repo[['drug_id','drug_name','ind_name','ind_id','pubYear']]
repo = repo.drop_duplicates()
repo.to_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")


repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")
#repo = pn.read_csv("D:\\Galia\\mechanismBased\\PushpakumT1.csv") 

#add mol2vec to repo
repo = pn.merge(repo,fullRepoDB[['drug_id','mol2vec']],on='drug_id',how='inner')
repo = repo[repo['pubYear']>0]
#remove anything after cutYear


#use innovativeRep
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/innovativeDFSTD1.csv")
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/innovativeDFSTD2.csv")
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/innovativeDFSTD2_5.csv")


cutYear = 1990
repoBefore = repo[repo['pubYear']<cutYear]
repoAfter = repo[repo['pubYear']>=cutYear]


repurposed_names = set(repoBefore['drug_name'].unique()).intersection(set(repoAfter['drug_name'].unique()))


#now look at pubmed publications dates
pmid1 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_1.csv')
pmid2 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_2.csv')
pmid3 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_3.csv')
pmid4 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_4.csv')
pmid5 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_5.csv')
pmid6 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_6.csv')
pmid7 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_7.csv')
pmid8 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_8.csv')
pmid9 = pn.read_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/PMIDYear_9.csv')

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


