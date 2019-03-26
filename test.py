# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 21:38:50 2019

@author: Galia
"""
def getIndications(drug):
    return repoBefore[repoBefore['drug_name']==drug]['ind_name'].unique()

def getAllIndications(drug):
    return repo[repo['drug_name']==drug]['ind_name'].unique()
def getWeight(val):
    return len(list(val))

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
def getIndicationOverlap(indlist1,indlist2):
    print(len(indlist1))
    print(len(indlist2))
    print("*****")
    return len(set(indlist1).intersection(set(indlist2)))
def getPPV(myResults,repoBefore,repurposed_names):
    if len(myResults)==0:
        print("No candidates")
        return pn.DataFrame()
    myResults['indications'] = myResults['dName'].apply(getIndications)

    myResults = myResults.rename(columns={'drug':'drug_name'})
    myResults2 = myResults[myResults['drug_name'].isin(repurposed_names)]

    repoAfterDelta = repoAfter[repoAfter['pubYear']>0]#no delta
    repoRes = pn.merge(myResults2,repoAfterDelta[['drug_name','ind_name']],on='drug_name',how='inner')

    repoRes['Success'] = repoRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
    repoRes2 =  repoRes[repoRes['Success']==True]

    print(len(repoRes2)/(len(myResults)+0.0))

    return repoRes2

def addLablesB(myResults,repoBefore,repurposed_names):
    if len(myResults)==0:
        print("No candidates")
        return pn.DataFrame()


    myResults = myResults.rename(columns={'drug':'drug_name'})
    myResults['indications'] = myResults['drug_name'].apply(getAllIndications)
    repoRes = pn.merge(myResults,repo[['drug_name','ind_name']],on='drug_name',how='inner')

    repoRes['Success'] = repoRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
    repoRes2 =  repoRes[repoRes['Success']==True]

    print(len(repoRes2)/(len(myResults)+0.0))

    return repoRes,myResults

def addLables(myResults,repoBefore,repurposed_names):
    if len(myResults)==0:
        print("No candidates")
        return pn.DataFrame()
    myResults['indications'] = myResults['dName'].apply(getIndications)
    myResults['oldIndication'] = myResults['drug'].apply(getIndications)
    myResults['indOverlap'] = list(map(getIndicationOverlap,myResults['indications'],myResults['oldIndication']))

    myResults = myResults.rename(columns={'drug':'drug_name'})
    myResults2 = myResults[myResults['drug_name'].isin(repurposed_names)].copy()

    repoAfterDelta = repoAfter[repoAfter['pubYear']>0]#no delta
    repoRes = pn.merge(myResults2,repoAfterDelta[['drug_name','ind_name']],on='drug_name',how='inner')

    repoRes['Success'] = repoRes.apply(lambda x: isInCandidates(x.indications, x.ind_name), axis=1)
    repoRes2 =  repoRes[repoRes['Success']==True]

    print(len(repoRes2)/(len(myResults)+0.0))

    return repoRes,myResults

def getPPVAll(myResults,repoBefore,repurposed_names):
    myResults['indications'] = myResults['candidates'].apply(getIndications)

    myResults = myResults.rename(columns={'drug':'drug_name'})
    myResults2 = myResults[myResults['drug_name'].isin(repurposed_names)]

    repoAfterDelta = repo[repo['pubYear']>0]#no delta
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


#ratio mol2vec
print('getResultsMol2Vec')
fullRatiosMol2Vec = getResultsMol2Vec()
fullRatiosMol2VecArr = addLables(fullRatiosMol2Vec,repoBefore,repurposed_names)
#fullRatiosMol2VecArr[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosMol2Vectmp.csv')
#fullRatiosMol2VecArr[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosMol2VectmpRepoResInnovation.csv')

RepoRes = fullRatiosMol2VecArr[0]
RepoRes = RepoRes[RepoRes['ref']<float('inf')]
RepoRes = RepoRes.sort_values('ref',ascending = True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.tail(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))


#ratio mol2vecCUI2vec
print('getResultsMol2VecCUI2Vec')
fullRatiosMol2VecCUI2Vec = getResultsMol2VecCUI2Vec()
fullRatiosMol2VecCUI2VecArr = addLables(fullRatiosMol2VecCUI2Vec,repoBefore,repurposed_names)
#fullRatiosMol2VecArr[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosMol2Vectmp.csv')
#fullRatiosMol2VecArr[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosMol2VectmpRepoResInnovation.csv')

RepoRes = fullRatiosMol2VecCUI2VecArr[0]
RepoRes = RepoRes[RepoRes['ref']<float('inf')]
RepoRes = RepoRes.sort_values('ref',ascending = True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.tail(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))


#ratio SemRep
fullRatiosSemRep = getResultsSemRep()
fullRatiosSemRepArr = addLables(fullRatiosSemRep,repoBefore,repurposed_names)
#fullRatiosSemRepArr[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosSemReptmp.csv')
fullRatiosSemRepArr[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullRatiosSemReptmpRepoRes.csv')

RepoRes = fullRatiosSemRepArr[0]
RepoRes = RepoRes[RepoRes['ref']<float('inf')]
RepoRes = RepoRes.sort_values('ref',ascending = True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.tail(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))




#check only distances in MOA (MolVec)
fullSMol2Vectmp = getResultsSOnlyMol2Vec()
fullSMol2VectmpWlables = addLables(fullSMol2Vectmp,repoBefore,repurposed_names)
RepoRes = fullSMol2VectmpWlables[0]
#fullSMol2VectmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSMol2Vectmp.csv')
#fullSMol2VectmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSMol2VectmpRepoResinnovative.csv')

RepoRes = RepoRes.sort_values('SrelDist',ascending=True)
#RepoRes = RepoRes[RepoRes['indOverlap']<2]

RepoRes['ind1len'] = RepoRes['oldIndication'].apply(len)
RepoRes['ind2len'] = RepoRes['indications'].apply(len)
RepoRes = RepoRes[RepoRes['ind1len']<5]
RepoRes = RepoRes[RepoRes['ind2len']<5]

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))



#check only distances in MOA (SemRep)
print('getResultsSOnlySemRep')
fullStmp = getResultsSOnlySemRep()
fullStmpWlables = addLables(fullStmp,repoBefore,repurposed_names)
RepoRes = fullStmpWlables[0]
#fullStmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullStmp.csv')
#fullStmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullStmpRepoResInnovative.csv')


RepoRes = RepoRes.sort_values('SrelDist',ascending=True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))


#check only distances in CUI2Vec
print('getResultsSOnlyCUI2Vec')
fullSCUI2Vectmp = getResultsSOnlyCUI2Vec()
fullSCUI2VectmpWlables = addLables(fullSCUI2Vectmp,repoBefore,repurposed_names)
RepoRes = fullSCUI2VectmpWlables[0]
#fullSCUI2VectmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSCUI2Vectmp.csv')

#fullSMol2VectmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSMol2VectmpRepoResInnovation.csv')

RepoRes = RepoRes.sort_values('SrelDist',ascending=True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))




#check only distances in word2Vec
fullSWord2Vectmp = getResultsSOnlyWord2Vec()
fullSWord2VectmpWlables = addLables(fullSWord2Vectmp,repoBefore,repurposed_names)
RepoRes = fullSWord2VectmpWlables[0]
#fullSCUI2VectmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSWord2Vectmp.csv')
#fullSWord2VectmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSWord2VectmpRepoRes.csv')

RepoRes = RepoRes.sort_values('SrelDist',ascending=True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))

# check only distances in CGN
#drugNamesrepo = drugNames.intersection(set(repo['drug_name'].unique()))
print('getResultsSOnlyCGN2Vec2')
fullSCGNtmp = getResultsSOnlyCGN2Vec2()
fullSCGNtmpWlables = addLables(fullSCGNtmp, repoBefore, repurposed_names)
RepoRes = fullSCGNtmpWlables[0]
#fullSCGNtmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSCGNtmp.csv')
#fullSCGNtmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSCGNtmpRepoRes.csv')
#fullSCGNtmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullSCGNtmpRepoResinnovative.csv')

RepoRes = RepoRes.sort_values('SrelDist', ascending=True)

for i in [1000, 2000, 3000, 4000, 5000, 10000, 15000]:
    print('precision at ' + str(i) + ' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success'] == True]) / (i + 0.0))
    print(len(tmphead[tmphead['Success'] == True]))


#check only distances in Purpose
print('getResultsTOnly')
fullTtmp = getResultsTOnly()
fullTtmpWlables = addLables(fullTtmp,repoBefore,repurposed_names)
#fullTtmpWlables[1].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullTtmp.csv')
#fullTtmpWlables[0].to_csv('/home/galiasn/DATA/MechanismBasedRepurposing/Data/fullTtmpRepoResInnovation.csv')

RepoRes = fullTtmpWlables[0]

RepoRes = RepoRes.sort_values('TrelDist',ascending=True)

for i in [1000,2000,3000,4000,5000,10000,15000]:
    print('precision at '+str(i)+' : ')
    tmphead = RepoRes.head(i)
    print(len(tmphead[tmphead['Success']==True])/(i+0.0))
    print(len(tmphead[tmphead['Success'] == True]))


for ratio in [(meanRatio-2*stdRatio),(meanRatio-stdRatio),meanRatio,(meanRatio+stdRatio),(meanRatio+2*stdRatio)]:
    print("ratio: "+str(ratio) +' Less:')
    reporesratio = fullTtmp[fullTtmp['SrelDist']<=ratio]
    getPPV(reporesratio,repoBefore,repurposed_names)
print("**********************")
for ratio in [(meanRatio - 2 * stdRatio), (meanRatio - stdRatio), meanRatio, (meanRatio + stdRatio),(meanRatio + 2 * stdRatio)]:
    print("ratio: "+str(ratio) +' More:')
    reporesratio = fullTtmp[fullTtmp['SrelDist'] >= ratio]
    getPPV(reporesratio,repoBefore,repurposed_names)

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


