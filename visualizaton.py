# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:59:46 2019

@author: Galia
"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

from sklearn.cluster import KMeans
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
import pandas as pn
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.cluster import AffinityPropagation

############################################
#Drug clusters


XdrugDocumentsT = load_obj('D:\\Galia\\mechanismBased\\XdrugDocumentsTreats_drugreceptors_1990')
drugs_T = load_obj('D:\\Galia\\mechanismBased\\drugsList_Treats_drugreceptors_1990')


svd = TruncatedSVD(n_components=500, n_iter=7, random_state=42)
XdrugDocumentsT_SVD = svd.fit_transform(XdrugDocumentsT)
X = XdrugDocumentsT_SVD

tstdrugs = pn.DataFrame()
tstdrugs['drug'] = drugs_T
tstdrugs['vec'] = list(XdrugDocumentsT_SVD)
X = np.asarray(list(tstdrugs['vec']))
pca = PCA(n_components=2, random_state=42)
XX= pca.fit_transform(X)
tstdrugs['PCA'] = list(XX)


n_clusters=4
colors = ['#4EACC5', '#FF9C34', '#4E9A06','#000080','#FF00FF','#CD5C5C','#00FA9A','#4682B4',
          '#1E90FF','#BA55D3']
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
tstdrugs['clust'] = kmeans.fit_predict(X)


for k, col in zip(tstdrugs['clust'].unique(), colors):
    tmp =np.vstack(np.asarray(tstdrugs[tstdrugs['clust']==k]['PCA']))
    if len(tmp)>0:
        plt.scatter(tmp[:,0],tmp[:,1],c=col)



XdrugDocuments_S = load_obj('D:\\Galia\\mechanismBased\\XdrugDocumentsStimulatesInhibitsPrevents_1990')
drugs_S = load_obj('D:\\Galia\\mechanismBased\\drugsList_StimulatesInhibitsPrevents_1990')


svd = TruncatedSVD(n_components=300, n_iter=7, random_state=42)
XdrugDocumentsS_SVD = svd.fit_transform(XdrugDocuments_S)
X = XdrugDocumentsS_SVD

tstdrugs = pn.DataFrame()
tstdrugs['drug'] = drugs_S
tstdrugs['vec'] = list(XdrugDocumentsS_SVD)
X = np.asarray(list(tstdrugs['vec']))
pca = PCA(n_components=2, random_state=42)
XX= pca.fit_transform(X)
tstdrugs['PCA'] = list(XX)


n_clusters=5
colors = ['#4EACC5', '#FF9C34', '#4E9A06','#000080','#FF00FF','#CD5C5C','#00FA9A','#4682B4',
          '#1E90FF','#BA55D3']
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
tstdrugs['clust'] = kmeans.fit_predict(X)


for k, col in zip(tstdrugs['clust'].unique(), colors):
    tmp =np.vstack(np.asarray(tstdrugs[tstdrugs['clust']==k]['PCA']))
    if len(tmp)>0:
        plt.scatter(tmp[:,0],tmp[:,1],c=col)




############################################
#Indication clusters

def getIndVector(val):
    if val in model.vocab:
        return model.get_vector(val)
    else:
        return np.asarray(200*[0])
model = KeyedVectors.load_word2vec_format('D:\\Galia\\DeVine_etal_200\\DeVine_etal_200.txt')


tst = pn.read_csv("D:\\Galia\\mechanismBased\\full.csv")
tstInd = pn.DataFrame()
tstInd['ind_id'] = tst['ind_id'].unique()
tstInd['w2v'] = tstInd['ind_id'].apply(getIndVector)

X = np.asarray(list(tstInd['w2v']))
pca = PCA(n_components=2, random_state=42)
XX= pca.fit_transform(X)
tstInd['PCA'] = list(XX)

n_clusters=4
colors = ['#4EACC5', '#FF9C34', '#4E9A06','#000080','#FF00FF','#CD5C5C','#00FA9A','#4682B4',
          '#1E90FF','#BA55D3']
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
tstInd['clust'] = kmeans.fit_predict(X)


#db = DBSCAN(eps=0.5, min_samples=5).fit(X)
#tstInd['clust'] = db.fit_predict(X)



for k, col in zip(tstInd['clust'].unique(), colors):
    tmp =np.vstack(np.asarray(tstInd[tstInd['clust']==k]['PCA']))
    if len(tmp)>0:
        plt.scatter(tmp[:,0],tmp[:,1],c=col)







##############################
#Plots

candidates = [0.018,0.02,0.018,0.0167]
neighbors = [0.023,0.0369,0.0392,0.0329]
x=[10,50,100,300]
plt.plot(x,candidates,"*-")
plt.plot(x,neighbors,"+-")
plt.legend(['candidates','neighbors'])
plt.xlabel('dimentions')
plt.ylabel('PPV')


candidates = [0.26,0.24,0.24,0.26]
neighbors = [0.36,0.29,0.29,0.315]
x=[10,50,100,300]
plt.plot(x,candidates,"*-")
plt.plot(x,neighbors,"+-")
plt.legend(['candidates','neighbors'])
plt.xlabel('dimentions')
plt.ylabel('mean similarity')