# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:27:47 2019

@author: Galia
"""

def translateToNameS(val):
    return drugs_S[val]
def getSDF(drugs_S,distances_S,indices_S):
    StestcaseDF = pn.DataFrame()
    StestcaseDF['did'] = indices_S[drugs_S.index(testcase)]
    StestcaseDF['dName'] = StestcaseDF['did'].apply(translateToNameS)
    StestcaseDF['Sdist'] = distances_S[drugs_S.index(testcase)]
    StestcaseDF['SrelDist'] = StestcaseDF['Sdist']/np.max(StestcaseDF['Sdist'])
    StestcaseDF= StestcaseDF.sort_values('Sdist')
    return StestcaseDF

def translateToNameT(val):
    return drugs_T[val]
def getTDF(drugs_T,distances_T,indices_T):
    TtestcaseDF = pn.DataFrame()
    TtestcaseDF['did'] = indicesT[drugs_T.index(testcase)]
    TtestcaseDF['dName'] = TtestcaseDF['did'].apply(translateToNameT)
    TtestcaseDF['Tdist'] = distancesT[drugs_T.index(testcase)]
    TtestcaseDF['TrelDist'] = TtestcaseDF['Tdist']/np.max(TtestcaseDF['Tdist'])
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


StestcaseDF = getSDF(drugs_S,distances_S,indices_S)
TtestcaseDF = getTDF(drugs_T,distancesT,indicesT)
#create table of propsed candidates
testcases= set(drugs_T).intersection(set(drugs_S))
resultsDict={}
fullTableDF = pn.DataFrame()
for testcase in testcases:
    combDF,resultsDict[testcase] = getCandidates(getSDF(drugs_S,distances_S,indices_S),getTDF(drugs_T,distancesT,indicesT))
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



#create table of neighbors
testcases= set(drugs_T).intersection(set(drugs_S))
resultsDict={}
for testcase in testcases:
    Tdf = getTDF(drugs_T,distancesT,indicesT)
    resultsDict[testcase] = Tdf.head(20)['dName'].unique()
resultsNDF = pn.DataFrame()
resultsNDF['drug'] = list(resultsDict.keys())
resultsNDF['neighbors'] =resultsDict.values()

resultsNDF = resultsNDF.rename(columns={'neighbors':'candidates'})

#resultsDF = resultsNDF.copy()
#resultsDF.to_csv("D:\\Galia\\mechanismBased\\tmpsneighbors.csv")