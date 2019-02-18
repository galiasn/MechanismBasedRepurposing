# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:01:52 2019

@author: Galia
"""

#we create a document for each term by aggregating the sentences the term appears in.
#The document tis created as a bag of words.

import gensim
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

from sklearn.cluster import KMeans
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import NearestCentroid
import pandas as pn

import pickle
def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
def wordCount(docs):
    v = CountVectorizer()
    f = vectorizer.fit_transform(docs)
    wordcount = np.asarray(f.sum(axis=0))
    vectCounDF = pn.DataFrame()
    vectCounDF['word'] = vectorizer.vocabulary_.keys()
    vectCounDF['num'] = wordcount[0]
    vectCounDF = vectCounDF.sort_values('num')
    return vectCounDF

def stem(var):
    newvar =[]
    ps = PorterStemmer()
    for v in var:
        newvar.append(ps.stem(v))
    return newvar

def removeStopWords(var):
    return set(var)-ENGLISH_STOP_WORDS
def removeOrigWord(var,word):
    return set(var)-set(word)

def appendToSentence(var):
    return " ".join(var)
def createDocument(term,sentences):
    doc = ' '
    tmp = sentences[(sentences['SUBJECT_NAME']==term)|(sentences['OBJECT_NAME']==term)][['SENTENCE']]
    tmp = tmp.drop_duplicates()#remove duplicates sentenes
    for s in list(tmp['SENTENCE']):
            doc = doc+' '
            doc = doc + s
    return doc

def createDocumentRepeatSentences(term,sentences):
    doc = ' '
    tmp = sentences[(sentences['SUBJECT_NAME']==term)|(sentences['OBJECT_NAME']==term)]
    for s in list(tmp['SENTENCE']):
            doc = doc+' '
            doc = doc + s
    return doc

def createDocumentFromTerms(term,sentences):
    doc = ' '
    tmp1 = sentences[(sentences['SUBJECT_NAME']==term)]
    tmp2 = sentences[(sentences['OBJECT_NAME']==term)]
    
    for t in tmp1['OBJECT_NAME']:
        doc = doc+' '+t
    for t in tmp2['SUBJECT_NAME']:
        doc = doc+' '+t
    return doc


sentencesT = pn.read_csv("D:\\Galia\\mechanismBased\\sentences_TREATS.csv",sep=',')
sentencesT = sentencesT[sentencesT['PREDICATE']=='TREATS']
sentencesT = sentencesT[sentencesT['PMID'].isin(pmidBefore)]

sentencesT['SENTENCE']= sentencesT['SENTENCE'].apply(gensim.utils.simple_preprocess)
sentencesT['SENTENCE'] = sentencesT['SENTENCE'].apply(removeStopWords)
sentencesT['SENTENCE'] = sentencesT['SENTENCE'].apply(stem)
sentencesT['SENTENCE'] = sentencesT['SENTENCE'].apply(appendToSentence)
drugsT = sentencesT[sentencesT['SUBJECT_SEMTYPE'].isin(['phsu','rcpt'])]['SUBJECT_NAME'].unique()



sentencesS = pn.read_csv('D:\\Galia\\mechanismBased\\sentences_STIMULATES_PLUS.csv',sep=',')
sentencesS = sentencesS[sentencesS['PREDICATE'].isin(['STIMULATES','INHIBITS','PREVENTS'])]
#isa = pn.read_csv('D:\\Galia\\mechanismBased\\sentences_ISA.csv')
#sentencesS = sentencesS.append(isa)
sentencesS = sentencesS[sentencesS['PMID'].isin(pmidBefore)]

sentencesS['SENTENCE']= sentencesS['SENTENCE'].apply(gensim.utils.simple_preprocess)
sentencesS['SENTENCE'] = sentencesS['SENTENCE'].apply(removeStopWords)
sentencesS['SENTENCE'] = sentencesS['SENTENCE'].apply(stem)
sentencesS['SENTENCE'] = sentencesS['SENTENCE'].apply(appendToSentence)
#drugs = sentences[sentences['SUBJECT_SEMTYPE']=='phsu']['SUBJECT_NAME'].unique()
drugsS = sentencesS[sentencesS['SUBJECT_SEMTYPE'].isin(['phsu','rcpt'])]['SUBJECT_NAME'].unique()



#treates
drugDocumentsT={}
count=1
for d in drugsT:
    print(count)
    #doctmp = createDocument(d,sentencesT)
    #if len(doctmp)>100:
    drugDocumentsT[d] = createDocument(d,sentencesT)#createDocument(d,sentencesT)
    count+=1

save_obj(drugDocumentsT,"D:\\Galia\\mechanismBased\\receptorDrugDocuments_Treats_1990")
drugDocumentsT = load_obj("D:\\Galia\\mechanismBased\\receptorDrugDocuments_Treats_1990")

#Bag of words
veryLong ={}
for d in drugDocumentsT.keys():
    if len(drugDocumentsT[d])>300:
        veryLong[d] = drugDocumentsT[d]
drugs_T =list( veryLong.keys())
save_obj(drugs_T,'D:\\Galia\\mechanismBased\\drugsList_Treats_drugreceptors_1990')
drugs_T = load_obj('D:\\Galia\\mechanismBased\\drugsList_Treats_drugreceptors_1990')

'''
vectorizer = CountVectorizer()
XdrugDocuments = vectorizer.fit_transform(veryLong.values())
'''
vectorizerT = TfidfVectorizer()
XdrugDocumentsT = vectorizerT.fit_transform(veryLong.values())

save_obj(XdrugDocumentsT,'D:\\Galia\\mechanismBased\\XdrugDocumentsTreats_drugreceptors_1990')
XdrugDocumentsT = load_obj('D:\\Galia\\mechanismBased\\XdrugDocumentsTreats_drugreceptors_1990')

svd = TruncatedSVD(n_components=300, n_iter=7, random_state=42)
XdrugDocumentsT_SVD = svd.fit_transform(XdrugDocumentsT)

nbrsT = NearestNeighbors(n_neighbors=2).fit(XdrugDocumentsT_SVD)
distancesT, indicesT = nbrsT.kneighbors(XdrugDocumentsT_SVD,n_neighbors=len(drugs_T))




#stimulates
drugDocuments_S={}
count=1
for d in drugsS:
    print(count)
    #doctmp = createDocument(d,sentencesS)
    #if len(doctmp)>100:
    drugDocuments_S[d] = createDocument(d,sentencesS)
    count+=1
#save_obj(drugDocuments_S,"D:\\Galia\\mechanismBased\\receptorDrugDocuments_StimulatesInhibitsPrevents_AllYearFullSent")
#drugDocuments_S = load_obj("D:\\Galia\\mechanismBased\\receptorDrugDocuments_StimulatesANDISA_AllYearFullSent")

save_obj(drugDocuments_S,"D:\\Galia\\mechanismBased\\receptorDrugDocuments_StimulatesInhibitsPrevents_1990")
drugDocuments_S = load_obj("D:\\Galia\\mechanismBased\\receptorDrugDocuments_StimulatesInhibitsPrevents_1990")
#Now we look at the similarities between the drugs

#Bag of words
veryLong_Stimulates ={}
for d in drugDocuments_S.keys():
    if len(drugDocuments_S[d])>300:
        veryLong_Stimulates[d] = drugDocuments_S[d]
drugs_Stimulates = veryLong_Stimulates.keys()

drugs_S = list(veryLong_Stimulates.keys())
save_obj(drugs_S,'D:\\Galia\\mechanismBased\\drugsList_StimulatesInhibitsPrevents_1990')
drugs_S = load_obj('D:\\Galia\\mechanismBased\\drugsList_StimulatesInhibitsPrevents_1990')

vectorizer_S = TfidfVectorizer(max_features = len(drugs_S))
XdrugDocuments_S = vectorizer_S.fit_transform(veryLong_Stimulates.values())

save_obj(XdrugDocuments_S,'D:\\Galia\\mechanismBased\\XdrugDocumentsStimulatesInhibitsPrevents_1990')
XdrugDocuments_S = load_obj('D:\\Galia\\mechanismBased\\XdrugDocumentsStimulatesInhibitsPrevents_1990')

svd = TruncatedSVD(n_components=300, n_iter=7, random_state=42)
XdrugDocumentsS_SVD = svd.fit_transform(XdrugDocuments_S)


nbrs_S = NearestNeighbors(n_neighbors=2).fit(XdrugDocumentsS_SVD)
distances_S, indices_S = nbrs_S.kneighbors(XdrugDocumentsS_SVD,n_neighbors=len(drugs_S))#3000
