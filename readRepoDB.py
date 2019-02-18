# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:43:15 2019

@author: Galia
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 06 11:21:43 2019

@author: Galia
"""
def toLower(s):
    return s.lower()

import pandas as pn
tst = pn.read_csv("D:\\Galia\\mechanismBased\\full.csv")
tst = tst[tst['status']=='Approved']
tst['count'] = [1]*len(tst)
tstgb = tst.groupby('drug_id',as_index=False).sum()
tstgb = tstgb[tstgb['count']>1]
tstgb = pn.merge(tstgb,tst[['drug_name','drug_id','ind_name']],on='drug_id',how='inner')
tstgb.to_csv("D:\\Galia\\mechanismBased\\repo.csv")

applications = pn.read_csv("D:\\Galia\FDA\\Applications.csv")
submission = pn.read_csv("D:\\Galia\FDA\\Submissions.csv")
submission = submission[submission['SubmissionStatus']=='AP']
submissionNewDrug = submission[submission['SubmissionClassCodeID'].isin([7,8,9,10,11])]
submissionNewIndication = submission[submission['SubmissionClassCodeID'].isin([16,22,24,25])]
products = pn.read_csv("D:\\Galia\FDA\\Products.csv")

submissionNewIndication = pn.merge(submissionNewIndication,products[['ApplNo','DrugName','ActiveIngredient']],on='ApplNo',how='inner')
candidates= pn.read_csv("D:\\Galia\\FDA\\tmpCorrectDF.csv")

submissionNewIndication['DrugName'] = submissionNewIndication['DrugName'].apply(toLower)
submissionNewIndication['ActiveIngredient'] = submissionNewIndication['ActiveIngredient'].apply(toLower)
candidates['d1'] = candidates['d1'].apply(toLower)
candidates['d2'] = candidates['d2'].apply(toLower)

c1 = candidates[candidates['d1'].isin(submissionNewIndication['DrugName'].unique())]
c2 = candidates[candidates['d2'].isin(submissionNewIndication['DrugName'].unique())]
c3 = candidates[candidates['d1'].isin(submissionNewIndication['ActiveIngredient'].unique())]
c4 = candidates[candidates['d2'].isin(submissionNewIndication['ActiveIngredient'].unique())]

fullcandidates = pn.read_csv("D:\\Galia\FDA\\tmpFullCandidatesDrugRepo.csv")
fullcandidates = fullcandidates.sort_values('ref',ascending=False)

#remove duplicate entries
def sortNames(s):
    lst = s.split(',')
    lst.sort()
    return lst
 def getFirst(lst):
     return lst[0]
 def getSecond(lst):
     return lst[1]
 
fullcandidates['pair'] = fullcandidates['dName']+','+fullcandidates['d1Name']
fullcandidates['pair'] = fullcandidates['pair'].apply(sortNames)
fullcandidates['drug1'] = fullcandidates['pair'].apply(getFirst)
fullcandidates['drug2'] = fullcandidates['pair'].apply(getSecond)
fullcandidates = fullcandidates.drop_duplicates(subset=['drug1','drug2'])
fullcandidates = fullcandidates[['drug1','drug2','ref']]
fullcandidates.to_csv("D:\\Galia\FDA\\FullCandidatesForGidi.csv")