# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 21:38:50 2019

@author: Galia
"""
def getIndications(drugs):
    return repoBefore[repoBefore['drug_name'].isin(drugs)]['ind_name'].unique()


def isInCandidates(val1,val2):
    return val2 in val1

def toLower(val):
    return val.lower()
#check if icd9 codes are different
def isNews(val1,val2):
    try:
        diff = np.abs(float(val1)-float(val2))
        return diff>=1
    except:
        return True
def w2vDistance(val1,val2):
    if (val1 in model.vocab) and (val2 in model.vocab):
        return model.similarity(val1,val2)
    else:
        return 10
def addDistanceBetweenIndications(repoRes,repoBefore):
    repoBeforeX = repoBefore.rename(columns={'ind_name':'ind_name_before'})
    merged = pn.merge(repoRes[['drug_name','ind_name']],repoBeforeX[['drug_name','ind_name_before','pubYear']],on='drug_name',how='right')
    merged = pn.merge(merged,repo[['ind_name','ind_id']],on='ind_name',how='inner')
    repoX= repo.rename(columns={'ind_name':'ind_name_before'})
    merged = pn.merge(merged,repoX[['ind_name_before','ind_id']],on='ind_name_before',how='inner')
    merged = merged.drop_duplicates()
    merged['ind_dist'] = map(w2vDistance,merged['ind_id_x'],merged['ind_id_y'])
    return merged

def getPPV(myResults,repoBefore,repurposed_names):
    myResults['indications'] = myResults['candidates'].apply(getIndications)

    myResults = myResults.rename(columns={'drug':'drug_name'})
    myResults2 = myResults[myResults['drug_name'].isin(repurposed_names)]

    repoAfterDelta = repoAfter[repoAfter['pubYear']>0]#no delta
    repoRes = pn.merge(myResults2,repoAfterDelta[['drug_name','ind_name']],on='drug_name',how='inner')

    repoRes['Success'] = repoRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
    repoRes2 =  repoRes[repoRes['Success']==True]
    print(str(len(repoRes2)/(len(repoAfterDelta)+0.0)))
    return repoRes2
def getDist(repoResCandidates,repoResNeighbors):
    repoResCandidates = repoResCandidates[['drug_name','ind_name']]
    repoResNeighbors = repoResNeighbors[['drug_name','ind_name']]
    
    mergeindicator =pn.merge(repoResCandidates,repoResNeighbors,on=['drug_name','ind_name'],how='outer', indicator=True) 
    inter = mergeindicator[mergeindicator['_merge']=='both']
    onlyCandidates = mergeindicator[mergeindicator['_merge']=='left_only']
    onlyNeighbors = mergeindicator[mergeindicator['_merge']=='right_only']

    MPALG = addDistanceBetweenIndications(repoResCandidates,repoBefore)
    MPALG = MPALG[MPALG['ind_dist']<10]

    MALG  = addDistanceBetweenIndications(repoResNeighbors,repoBefore)
    MALG = MALG[MALG['ind_dist']<10]

    onlyCandidates = pn.merge(onlyCandidates,MPALG[['drug_name','ind_name','ind_name_before','ind_dist']],on=['drug_name','ind_name'],how='inner')
    onlyCandidates = onlyCandidates[onlyCandidates['ind_dist']<10]

    onlyNeighbors = pn.merge(onlyNeighbors,MALG[['drug_name','ind_name','ind_name_before','ind_dist']],on=['drug_name','ind_name'],how='inner')
    onlyNeighbors = onlyNeighbors[onlyNeighbors['ind_dist']<10]
    print("Candidates: "+str(MPALG['ind_dist'].mean()))
    print("Neighbors: "+str(MALG['ind_dist'].mean()))
    print(scipy.stats.ks_2samp(onlyNeighbors['ind_dist'],onlyCandidates['ind_dist']))
    return
import scipy.stats
scipy.stats.ks_2samp(onlyNeighbors['ind_dist'],onlyCandidates['ind_dist'])
#add indications according to candidates

resultsDF['indications'] = resultsDF['candidates'].apply(getIndications)
#res = list(set(resultsDF['drug'].unique()).intersection(set(repoAfter['drug_name'].unique())))

resultsDF = resultsDF.rename(columns={'drug':'drug_name'})
resultsDF2 = resultsDF[resultsDF['drug_name'].isin(repurposed_names)]

#repoAfterDelta = repoAfter[repoAfter['pubYear']>2000]
repoAfterDelta = repoAfter[repoAfter['pubYear']>0]#no delta
repoRes = pn.merge(resultsDF2,repoAfterDelta[['drug_name','ind_name']],on='drug_name',how='inner')

repoRes['Success'] = repoRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
repoRes2 =  repoRes[repoRes['Success']==True]



repoResCandidates  = repoRes2.copy()
repoResNeighbors = repoRes2.copy()

print("Candidates:")
repoResCandidates = getPPV(resultsDF,repoBefore,repurposed_names)
print("Neighbors:")
repoResNeighbors = getPPV(resultsNDF,repoBefore,repurposed_names)

getDist(repoResCandidates,repoResNeighbors)

MPALG = addDistanceBetweenIndications(repoResCandidates,repoBefore)
MPALG = MPALG[MPALG['ind_dist']<10]
MPALG_X = MPALG[['drug_name','ind_dist']].groupby('drug_name',as_index=False).mean()
MALG  = addDistanceBetweenIndications(repoResNeighbors,repoBefore)
MALG = MALG[MALG['ind_dist']<10]
MALG_X = MALG[['drug_name','ind_dist']].groupby('drug_name',as_index=False).mean()
MALG = MALG.sort_values('ind_dist')

tmp = MALG[MALG['ind_dist']<0.2]
repoResCandidates = repoResCandidates[['drug_name','ind_name']]
repoResNeighbors = repoResNeighbors[['drug_name','ind_name']]

inter = pn.merge(repoResCandidates,repoResNeighbors,on=['drug_name','ind_name'],how='inner')
mergeindicator =pn.merge(repoResCandidates,repoResNeighbors,on=['drug_name','ind_name'],how='outer', indicator=True) 
inter = mergeindicator[mergeindicator['_merge']=='both']
onlyCandidates = mergeindicator[mergeindicator['_merge']=='left_only']

onlyNeighbors = mergeindicator[mergeindicator['_merge']=='right_only']

onlyCandidates = pn.merge(onlyCandidates,MPALG[['drug_name','ind_name','ind_name_before','ind_dist']],on=['drug_name','ind_name'],how='inner')
onlyCandidates = onlyCandidates[onlyCandidates['ind_dist']<10]

#onlyNeighbors = addDistanceBetweenIndications(onlyNeighbors,repoBefore)
onlyNeighbors = pn.merge(onlyNeighbors,MALG[['drug_name','ind_name','ind_name_before','ind_dist']],on=['drug_name','ind_name'],how='inner')
onlyNeighbors = onlyNeighbors[onlyNeighbors['ind_dist']<10]
#repoRsCandidatesOnly = repoResCandidates[repoResCandidates['drug_name'].isin(inter['drug_name'].unique())==False]



repoBefore = repoBefore.rename(columns={'ind_name':'ind_name_before'})
merged = pn.merge(repoRes2,repoBefore[['drug_name','ind_name_before']],on='drug_name',how='inner')
merged.to_csv("D:\\Galia\\mechanismBased\\tmp.csv")

icd9 = pn.read_csv("D:\\Galia\\mechanismBased\\CUI_ICD.csv")
full = pn.read_csv("C:\\Users\\Galia\\Downloads\\full.csv")
full = full.rename(columns={'ind_id':'CUI'})
icd9ind = pn.merge(icd9[['CODE','CUI']],full,on=['CUI'],how='inner')

icd9merged = pn.merge(merged,icd9ind[['ind_name','CODE']],on=['ind_name'],how='inner')
icd9ind = icd9ind.rename(columns={'CODE':'CODE_before','ind_name':'ind_name_before'})
icd9merged = pn.merge(icd9merged,icd9ind[['ind_name_before','CODE_before']],on=['ind_name_before'],how='inner')
icd9merged.to_csv("D:\\Galia\\mechanismBased\\tmp.csv")
icd9merged['diff'] = map(isNews,icd9merged['CODE'],icd9merged['CODE_before'])

icd9mergedsmall = icd9merged[['drug_name','CODE','CODE_before']]
icd9mergedsmall = icd9mergedsmall.drop_duplicates()

icd9mergedsmall.to_csv("D:\\Galia\\mechanismBased\\tmp.csv")

resultsNDF['indications'] = resultsNDF['candidates'].apply(getIndications)
#res = list(set(resultsDF['drug'].unique()).intersection(set(repoAfter['drug_name'].unique())))

resultsNDF = resultsNDF.rename(columns={'drug':'drug_name'})
resultsNDF = resultsNDF[resultsNDF['drug_name'].isin(repurposed_names)]

repoAfterDelta = repoAfter[repoAfter['pubYear']>2000]
repoNRes = pn.merge(resultsNDF,repoAfterDelta[['drug_name','ind_name']],on='drug_name',how='inner')

repoNRes['Success'] = repoNRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
repoNRes2 =  repoNRes[repoNRes['Success']==True]

inter = set(repoNRes2['drug_name'].unique()).intersection(set(repoRes2['drug_name'].unique()))


