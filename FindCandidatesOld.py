# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:27:47 2019

@author: Galia
"""
from scipy.spatial import distance

def getMol2VecDist(mol1,mol2):
    return distance.euclidean(mol1,mol2)
def translateToNameS(val):
    return drugs_S[val]
def getSDF(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = pn.DataFrame()
    StestcaseDF['did'] = indices_S[drugs_S.index(testcase)]
    StestcaseDF['dName'] = StestcaseDF['did'].apply(translateToNameS)
    StestcaseDF['Sdist'] = distances_S[drugs_S.index(testcase)]
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))

    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def getSDFMol2Vec(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = fullRepoDB[['drug_name','mol2vec']].copy()
    names = map(translateToNameS,indices_S[drugs_S.index(testcase)])
    StestcaseDF = StestcaseDF[StestcaseDF['drug_name'].isin(names)].copy()

    if testcase not in fullRepoDB['drug_name'].unique():
        return pn.DataFrame()
    testcaseMol2Vec = fullRepoDB[fullRepoDB['drug_name']==testcase]['mol2vec'].iloc[0]
    StestcaseDF['Sdist'] = map(getMol2VecDist,StestcaseDF['mol2vec'],[testcaseMol2Vec]*len(StestcaseDF))
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))
    StestcaseDF = StestcaseDF.rename(columns={'drug_name':'dName'})
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF


def translateToNameT(val):
    return drugs_T[val]
def getTDF(drugs_T,distances_T,indices_T,testcase):
    TtestcaseDF = pn.DataFrame()
    TtestcaseDF['did'] = indices_T[drugs_T.index(testcase)]
    TtestcaseDF['dName'] = TtestcaseDF['did'].apply(translateToNameT)
    TtestcaseDF['Tdist'] = distances_T[drugs_T.index(testcase)]
    TtestcaseDF['TrelDist'] = (TtestcaseDF['Tdist']-([np.min(TtestcaseDF['Tdist'])]*len(TtestcaseDF))) / (np.max(TtestcaseDF['Tdist'])-np.min(TtestcaseDF['Tdist']))

    TtestcaseDF= TtestcaseDF.sort_values('Tdist')
    return TtestcaseDF

def getCandidates(StestcaseDF,TtestcaseDF):
    combDF = pn.merge(StestcaseDF,TtestcaseDF,on='dName',how='inner')
    combDF['ref'] = combDF['TrelDist']/combDF['SrelDist']
    combDF = combDF.sort_values('ref',ascending=False)
    cutoff = np.mean(combDF['ref'])+2*np.std(combDF['ref'])
    print(cutoff)
    return combDF[combDF['ref']>=cutoff].copy(),combDF[combDF['ref']>=cutoff]['dName'].unique()



def getNeighbors(StestcaseDF,TtestcaseDF):
    combDF = pn.merge(StestcaseDF,TtestcaseDF,on='dName',how='inner')
    combDF['ref'] = combDF['TrelDist']/combDF['SrelDist']

    cutoff = np.mean(combDF['ref'])+1*np.std(combDF['ref'])
    print(cutoff)
    return combDF[combDF['ref']<cutoff]['dName'].unique()

def getCandidatesByRatioLess(StestcaseDF,TtestcaseDF,cutoff=1):
    combDF = pn.merge(StestcaseDF, TtestcaseDF, on='dName', how='inner')
    combDF['ref'] = combDF['TrelDist'] / combDF['SrelDist']

    if ratio == 99:
        return combDF,combDF['dName'].unique()
    return combDF[combDF['ref'] <= cutoff].copy(), combDF[combDF['ref'] <= cutoff]['dName'].unique()


def getCandidatesByRatioMore(StestcaseDF,TtestcaseDF,cutoff=1):
    combDF = pn.merge(StestcaseDF, TtestcaseDF, on='dName', how='inner')
    combDF['ref'] = combDF['TrelDist'] / combDF['SrelDist']

    return combDF[combDF['ref'] >= cutoff].copy(), combDF[combDF['ref'] >= cutoff]['dName'].unique()



#mol2vec data
repoBeforeMol2Vec = repoBefore.groupby('drug_id',as_index=False).first()
drugs_T = list(repoBeforeMol2Vec['drug_name'])
nbrsT = NearestNeighbors(n_neighbors=2).fit(list(repoBeforeMol2Vec['mol2vec'] ))
distancesT, indicesT = nbrsT.kneighbors(list(repoBeforeMol2Vec['mol2vec']),n_neighbors=len(drugs_T))


StestcaseDF = getSDF(drugs_S,distances_S,indices_S)
TtestcaseDF = getTDF(drugs_T,distancesT,indicesT)
#create table of propsed candidates
testcases= set(drugs_T).intersection(set(drugs_S))
resultsDict={}
fullTableDF = pn.DataFrame()
for testcase in testcases:
    combDF,resultsDict[testcase] = getCandidates(getSDF(drugs_S,distances_S,indices_S,testcase),getTDF(drugs_T,distancesT,indicesT,testcase))
    combDF = combDF[['dName','ref']]
    combDF['d1Name'] = [testcase]*len(combDF)
    fullTableDF = fullTableDF.append(combDF)
    print(str(len(resultsDict[testcase])))

resultsDF = pn.DataFrame()
resultsDF['drug'] = list(resultsDict.keys())
resultsDF['candidates'] = resultsDict.values()
resultsDFBack = resultsDF.copy()
#resultsDF.to_csv("D:\\Galia\\mechanismBased\\tmpCandidates.csv")

#resultsDF = resultsDFBack.copy()

#fullTableDF.to_csv("D:\\Galia\\mechanismBased\\tmpFullCandidates.csv")

def getResultsLess(ratio=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)

        combDF, resultsDict[testcase] = getCandidatesByRatioLess(Stmp,Ttmp,ratio)
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsMore(ratio=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)

        combDF, resultsDict[testcase] = getCandidatesByRatioMore(Stmp,Ttmp,ratio)
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsLessS(ratio=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)

        combDF, resultsDict[testcase] = getCandidatesByRatioLess(Stmp,Ttmp,ratio)
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsMoreS(ratio=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)

        combDF, resultsDict[testcase] = getCandidatesByRatioMore(Stmp,Ttmp,ratio)
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsSOnlyLess(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp[Stmp['SrelDist'] <= cutoff].copy()
        resultsDict[testcase] = Stmp[Stmp['SrelDist'] <= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF
def getResultsSOnlyMore(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp[Stmp['SrelDist'] >= cutoff].copy()
        resultsDict[testcase] = Stmp[Stmp['SrelDist'] >= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsSOnlySemRepLess(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp[Stmp['SrelDist'] <= cutoff].copy()
        resultsDict[testcase] = Stmp[Stmp['SrelDist'] <= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF

def getResultsSOnlySemRepLessNew(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()
    fullTableDF = pn.DataFrame()
    resultsDF = pn.DataFrame()
    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp[Stmp['SrelDist'] <= cutoff].copy()
        combDF['drug'] = ['testcase']*len(combDF)
        resultsDict[testcase] = Stmp[Stmp['SrelDist'] <= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)


    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF
def getResultsSOnlySemRepMore(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp[Stmp['SrelDist'] >= cutoff].copy()
        resultsDict[testcase] = Stmp[Stmp['SrelDist'] >= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF


def getResultsTOnlyLess(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Ttmp = getTDF(drugs_T, distancesT, indicesT, testcase)
        if len(Ttmp)==0:
            continue
        combDF= Ttmp[Ttmp['TrelDist'] <= cutoff].copy()
        resultsDict[testcase] = Ttmp[Ttmp['TrelDist'] <= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF
def getResultsTOnlyMore(cutoff=1):
    testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDict = {}
    fullTableDF = pn.DataFrame()

    for testcase in testcases:
        Ttmp = getTDF(drugs_T, distancesT, indicesT, testcase)
        if len(Ttmp)==0:
            continue
        combDF= Ttmp[Ttmp['TrelDist'] >= cutoff].copy()
        resultsDict[testcase] = Ttmp[Ttmp['TrelDist'] >= cutoff]['dName'].unique()
        fullTableDF = fullTableDF.append(combDF)

    resultsDF = pn.DataFrame()
    resultsDF['drug'] = list(resultsDict.keys())
    resultsDF['candidates'] = resultsDict.values()
    return resultsDF,fullTableDF
#create table of neighbors
testcases= set(drugs_T).intersection(set(drugs_S))
resultsDict={}
for testcase in testcases:
    Tdf = getTDF(drugs_T,distancesT,indicesT,testcase)
    tdfmean = Tdf['Tdist'].mean()
    tdfstd = Tdf['Tdist'].std()
    resultsDict[testcase] = Tdf[Tdf['Tdist']>=tdfmean+2*tdfstd]['dName'].unique()
resultsNDF = pn.DataFrame()
resultsNDF['drug'] = list(resultsDict.keys())
resultsNDF['neighbors'] =resultsDict.values()

resultsNDF = resultsNDF.rename(columns={'neighbors':'candidates'})

#resultsDF = resultsNDF.copy()
#resultsDF.to_csv("D:\\Galia\\mechanismBased\\tmpsneighbors.csv")