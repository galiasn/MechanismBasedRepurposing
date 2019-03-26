
'''
Train convolutional graph netwok with initial features from mol2v3c (1-vectors for non-drug)
Unsupervised - Loss function according to cui2vec distances

Calssification - classification by indication (for limited drugs)

'''
import pandas as pn
import networkx as nx
import numpy as np
#First, read graph and leave only drugs that we have mol2vec embeddings for.


#create lables (cui2vec distances)
cui2vec = pn.read_csv('/mnt/galiasn/cui2vec_pretrained/cui2vec_pretrained.csv')
cuisnames = cui2vec['Unnamed: 0']
cui2vec = cui2vec.rename(columns={'Unnamed: 0':'CUI'})

drugGraphDF = pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_10.csv')
drugGraphDF =drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_30.csv'))
drugGraphDF =  drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_50.csv'))

drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_70.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_100.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_over100.csv'))

#this graph hold all the semrep predicates for drugs, disesaes and receptors

drugGraphDF = drugGraphDF[[u'OBJECT_CUI', u'SUBJECT_CUI',
      u'SUBJECT_NAME', u'SUBJECT_SEMTYPE',
      u'OBJECT_NAME', u'OBJECT_SEMTYPE']]

#create cui mapping


cuimap1 = drugGraphDF[['SUBJECT_NAME','SUBJECT_CUI']]
cuimap2 = drugGraphDF[['OBJECT_NAME','OBJECT_CUI']]
cuimap1 = cuimap1.rename(columns={'SUBJECT_NAME':'NAME','SUBJECT_CUI':'CUI'})
cuimap2 = cuimap2.rename(columns={'OBJECT_NAME':'NAME','OBJECT_CUI':'CUI'})
cuimap1 = cuimap1.append(cuimap2)
cuimap1 = cuimap1.drop_duplicates()
cuimap1 = pn.merge(cuimap1,cui2vec,on='CUI',how='inner')



#Leave only drugs

drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_SEMTYPE']=='phsu']
drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_SEMTYPE']=='phsu']

#leave only cuis that are in cui2vec
#cui2vec = cui2vec.rename(columns={'Unnamed: 0':'SUBJECT_CUI'})
#drugGraphDF = pn.merge(cui2vec[['SUBJECT_CUI']],drugGraphDF,on='SUBJECT_CUI',how='inner')
#cui2vec = cui2vec.rename(columns={'SUBJECT_CUI':'OBJECT_CUI'})
#drugGraphDF = pn.merge(cui2vec[['OBJECT_CUI']],drugGraphDF,on='OBJECT_CUI',how='inner')
drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_CUI'].isin(cui2vec['CUI'].unique())]
drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_CUI'].isin(cui2vec['CUI'].unique())]

tmp = drugGraphDF[drugGraphDF['SUBJECT_SEMTYPE'].isin(['phsu'])]
tmp = tmp[tmp['SUBJECT_SEMTYPE'].isin(['phsu'])]
drugNames = set(tmp['OBJECT_NAME'].unique()).union(set(tmp['SUBJECT_NAME'].unique()))

#add self loops
selfLoopDF = pn.DataFrame()
selfLoopDF['SUBJECT_NAME'] = list(drugGraphDF['SUBJECT_NAME'].unique())
selfLoopDF['OBJECT_NAME'] = list(drugGraphDF['SUBJECT_NAME'].unique())
#dummies
selfLoopDF['OBJECT_CUI'] = 'C0'*len(selfLoopDF)
selfLoopDF['SUBJECT_CUI'] = 'C0'*len(selfLoopDF)
selfLoopDF['SUBJECT_SEMTYPE'] = 'phsu'*len(selfLoopDF)
selfLoopDF['OBJECT_SEMTYPE'] = 'phsu'*len(selfLoopDF)


drugGraphDF = drugGraphDF.append(selfLoopDF)
#drugGraphDF = selfLoopDF
drugGraphDF['weight'] = [1]*len(drugGraphDF)
drugGraphDFgb = drugGraphDF.groupby(['SUBJECT_NAME','OBJECT_NAME'],as_index=False).sum()

fullGraph = nx.from_pandas_edgelist(drugGraphDFgb,'SUBJECT_NAME','OBJECT_NAME')



#adjacency matrix
AdjMat = nx.adjacency_matrix(fullGraph)
#add identity matrix
#Idnt = np.identity(len(fullGraph.nodes))
#AdjMat_Idnt = AdjMat+Idnt
'''
Create features. The features for each node is the ml2vec embedding. 
If the node does not have mol2vec embeddings the features are a vector of ones
'''
#drugStructure holds all the drugs that we have a chemichal structure for. Compute mol2vec for each of them

modelMol2Vec = word2vec.Word2Vec.load('/home/galiasn/DATA/MechanismBasedRepurposing/Data/model_300dim.pkl')

drugStructure = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/structure links.csv",',')

drugStructure['noSmiles'] = drugStructure['SMILES'].isnull()
drugStructure = drugStructure[drugStructure['noSmiles']==False]


#drugStructure['mol'] = drugStructure['SMILES'].apply(Chem.MolFromSmiles)
ind = 0
lst=[]
while ind<len(drugStructure):
    smiles = drugStructure['SMILES'].iloc[0]
    mol = Chem.MolFromSmiles(smiles)
    if type(mol) is Chem.rdchem.Mol:
        lst.append(mol)
    else:
        lst.append(float('Nan'))
    ind+=1
    print(ind)
drugStructure['mol']= lst
drugStructure['noSmiles'] = drugStructure['mol'].isnull()
drugStructure = drugStructure[drugStructure['noSmiles']==False]
drugStructure['mol-sentences'] = drugStructure.apply(lambda x: MolSentence(mol2alt_sentence(x['mol'], 1)), axis=1)
drugStructure['mol2vec'] = [x for x in sentences2vec(drugStructure['mol-sentences'], modelMol2Vec, unseen='UNK')]

def translateToVec(val):
    if type(val)==type(1):
        return [1]*300
    else:
        return val
nodecuisnodes = list(fullGraph.nodes())
featureDF = pn.DataFrame()
featureDF['Name'] = nodecuisnodes
featureDF = pn.merge(featureDF,drugStructure[['Name','mol2vec']],on='Name',how='left')
featureDF['mol2vec']=featureDF['mol2vec'].fillna(1)
featureDF['mol2vec'] = featureDF['mol2vec'].apply(translateToVec)


#lables
lablesDF = pn.DataFrame()
lablesDF['NAME'] = list(fullGraph.nodes())
lablesDF = pn.merge(lablesDF,cuimap1,on='NAME',how='inner')


lables = lablesDF.loc[:,'V1':'V500']


#nodecuis = set(tmpDrugs['OBJECT_CUI'].unique()).union(set(tmpDrugs['SUBJECT_CUI'].unique()))
#lables = cui2vec[cui2vec['OBJECT_CUI'].isin(nodecuis)]

