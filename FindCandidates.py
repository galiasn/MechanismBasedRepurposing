# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:27:47 2019

@author: Galia
"""
from scipy.spatial import distance

def getMol2VecDist(mol1,mol2):
    return distance.euclidean(mol1,mol2)

def getCUI2VecDist(cui1,cui2):
    return distance.euclidean(getcui2vecEmbedding(cui1),getcui2vecEmbedding(cui2))

def getWord2VecDist(cui1,cui2):
    return (1- w2vmodel.similarity(cui1,cui2))

def translateToNameS(val):
    return drugs_S[val]
def getSDF(drugs_S,distances_S,indices_S,testcase):
    if testcase not in drugs_S:
        return pn.DataFrame()
    StestcaseDF = pn.DataFrame()
    StestcaseDF['did'] = indices_S[drugs_S.index(testcase)]
    StestcaseDF['dName'] = StestcaseDF['did'].apply(translateToNameS)
    StestcaseDF['Sdist'] = distances_S[drugs_S.index(testcase)]
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))

    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def getSDFMol2Vec(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = fullRepoDB[['drug_name','mol2vec']].copy()
    StestcaseDF = StestcaseDF[StestcaseDF['drug_name'].isin(repo['drug_name'].unique())]
    #names = map(translateToNameS,indices_S[drugs_S.index(testcase)])
    #StestcaseDF = StestcaseDF[StestcaseDF['drug_name'].isin(names)].copy()

    if testcase not in fullRepoDB['drug_name'].unique():
        return pn.DataFrame()
    testcaseMol2Vec = fullRepoDB[fullRepoDB['drug_name']==testcase]['mol2vec'].iloc[0]
    StestcaseDF['Sdist'] = map(getMol2VecDist,StestcaseDF['mol2vec'],[testcaseMol2Vec]*len(StestcaseDF))
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))
    StestcaseDF = StestcaseDF.rename(columns={'drug_name':'dName'})
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def getSDF_GCN(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = cgnEmbDF[cgnEmbDF['node_name'].isin(testcases)][['node_name','cgnVec']].copy()
    #names = map(translateToNameS,indices_S[drugs_S.index(testcase)])
    #StestcaseDF = StestcaseDF[StestcaseDF['node_name'].isin(names)].copy()

    if testcase not in cgnEmbDF['node_name'].unique():
        return pn.DataFrame()
    testcaseVec = cgnEmbDF[cgnEmbDF['node_name']==testcase]['cgnVec'].iloc[0]
    StestcaseDF['Sdist'] = map(getMol2VecDist,StestcaseDF['cgnVec'],[testcaseVec]*len(StestcaseDF))
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))
    StestcaseDF = StestcaseDF.rename(columns={'node_name':'dName'})
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def getSDFCUI(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = fullRepoDB[['drug_name']].copy()
    StestcaseDF = StestcaseDF.drop_duplicates()
    StestcaseDF = StestcaseDF[StestcaseDF['drug_name'].isin(testcases)]
    StestcaseDF = pn.merge(StestcaseDF,sentencesDrugsDF,on='drug_name',how='inner')


    if testcase not in StestcaseDF['drug_name'].unique():
        return pn.DataFrame()
    testcaseCUI2Vec = StestcaseDF[StestcaseDF['drug_name']==testcase]['drug_CUI'].iloc[0]
    StestcaseDF['Sdist'] = map(getCUI2VecDist,StestcaseDF['drug_CUI'],[testcaseCUI2Vec]*len(StestcaseDF))
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))
    StestcaseDF = StestcaseDF.rename(columns={'drug_name':'dName'})
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def getSDFWord(drugs_S,distances_S,indices_S,testcase):
    StestcaseDF = fullRepoDB[['drug_name']].copy()
    StestcaseDF = StestcaseDF.drop_duplicates()
    StestcaseDF = pn.merge(StestcaseDF,sentencesDrugsDF,on='drug_name',how='inner')
    StestcaseDF = StestcaseDF[StestcaseDF['drug_CUI'].isin(list(w2vmodel.vocab))]

    if testcase not in StestcaseDF['drug_name'].unique():
        return pn.DataFrame()
    testcaseWord2Vec = StestcaseDF[StestcaseDF['drug_name']==testcase]['drug_CUI'].iloc[0]
    StestcaseDF['Sdist'] = map(getWord2VecDist,StestcaseDF['drug_CUI'],[testcaseWord2Vec]*len(StestcaseDF))
    StestcaseDF['SrelDist'] = (StestcaseDF['Sdist']-([np.min(StestcaseDF['Sdist'])]*len(StestcaseDF))) / (np.max(StestcaseDF['Sdist'])-np.min(StestcaseDF['Sdist']))
    StestcaseDF = StestcaseDF.rename(columns={'drug_name':'dName'})
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF


def translateToNameT(val):
    return drugs_T[val]
def getTDF(drugs_T,distances_T,indices_T,testcase):
    if testcase not in drugs_T:
        return pn.DataFrame()
    TtestcaseDF = pn.DataFrame()
    TtestcaseDF['did'] = indices_T[drugs_T.index(testcase)]
    TtestcaseDF['dName'] = TtestcaseDF['did'].apply(translateToNameT)
    TtestcaseDF['Tdist'] = distances_T[drugs_T.index(testcase)]
    TtestcaseDF['TrelDist'] = (TtestcaseDF['Tdist']-([np.min(TtestcaseDF['Tdist'])]*len(TtestcaseDF))) / (np.max(TtestcaseDF['Tdist'])-np.min(TtestcaseDF['Tdist']))

    TtestcaseDF= TtestcaseDF.sort_values('Tdist')
    return TtestcaseDF







def getCandidates(StestcaseDF,TtestcaseDF):
    combDF = pn.merge(StestcaseDF, TtestcaseDF, on='dName', how='inner')
    combDF['ref'] = combDF['TrelDist'] / combDF['SrelDist']
    return combDF

def getCandidates2(StestcaseDF,TtestcaseDF):
    TtestcaseDF = TtestcaseDF.rename(columns={'SrelDist':'TrelDist'})
    combDF = pn.merge(StestcaseDF, TtestcaseDF, on='dName', how='inner')
    combDF['ref'] = combDF['TrelDist'] / combDF['SrelDist']
    return combDF

def getCandidatesDrugName(StestcaseDF,TtestcaseDF):
    combDF = pn.merge(StestcaseDF, TtestcaseDF, on='drug_name', how='inner')
    combDF['ref'] = combDF['TrelDist'] / combDF['SrelDist']
    return combDF


def getResultsSemRep():
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)

        combDF = getCandidates(Stmp,Ttmp)
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)

    return resultsDF

def getResultsMol2Vec():
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getTDF(drugs_T, distancesT, indicesT,testcase)
        if len(Ttmp)==0:
            continue
        combDF = getCandidates(Stmp,Ttmp)
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)

    return resultsDF

def getResultsMol2VecCUI2Vec():
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        Ttmp = getSDFCUI(drugs_S, distances_S, indices_S,testcase)
        if len(Ttmp)==0:
            continue
        combDF = getCandidates2(Stmp,Ttmp)
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)

    return resultsDF

def getResultsSOnlyCGN2Vec(): #only stimulatesMol2Vec
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()


    for testcase in testcases:
        Stmp = getSDF_GCN(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF

def getResultsSOnlyCGN2Vec2(): #only stimulatesMol2Vec
    #testcases = list(drugNamesrepo)
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDF_GCN(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF


def getResultsSOnlyMol2Vec(): #only stimulatesMol2Vec
    #testcases = repo['drug_name'].unique()
    resultsDF = pn.DataFrame()


    for testcase in testcases:
        Stmp = getSDFMol2Vec(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF

def getResultsSOnlySemRep(): #only stimulates SemRep
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()


    for testcase in testcases:
        Stmp = getSDF(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF

def getResultsSOnlyCUI2Vec(): #only cui2vec distance
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFCUI(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF

def getResultsSOnlyWord2Vec(): #only cui2vec distance
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Stmp = getSDFWord(drugs_S, distances_S, indices_S,testcase)
        if len(Stmp)==0:
            continue
        combDF= Stmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF


def getResultsTOnly(): #Indication only
    #testcases = set(drugs_T).intersection(set(drugs_S))
    resultsDF = pn.DataFrame()

    for testcase in testcases:
        Ttmp = getTDF(drugs_T, distancesT, indicesT, testcase)
        if len(Ttmp)==0:
            continue
        combDF = Ttmp.copy()
        combDF['drug'] = [testcase] * len(combDF)
        resultsDF = resultsDF.append(combDF)
    return resultsDF




'''
Select group of drugs to test agains. 
We use the intersection between the drugs at repoDB, the drugs at cui2vec and the drugs at mol2vec so we have a "even playing field"
'''

#testcases = set(repo['drug_name'].unique()).intersection(set(mol2vecNames)).intersection(set(cuiNames))
testcases = set(repo['drug_name'].unique())
