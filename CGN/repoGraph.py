
'''
Create graph for drugs in repo before. lables are cui2vec embeddings
Test the graph on repo after.
'''
import pandas as pn
import networkx as nx

'''
RepoBefore
'''
#create lables (cui2vec distances)
cui2vec = pn.read_csv('/mnt/galiasn/cui2vec_pretrained/cui2vec_pretrained.csv')
cuisnames = cui2vec['Unnamed: 0']
cui2vec = cui2vec.rename(columns={'Unnamed: 0':'CUI'})


#read repo
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")

cutYear = 1990
repoBefore = repo[repo['pubYear']<cutYear]
repoAfter = repo[repo['pubYear']>=cutYear]

repodrugs = repoBefore['drug_name'].unique()
repoInds = repoBefore['ind_id'].unique()

drugGraphDF = pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_10.csv')
drugGraphDF =drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_30.csv'))
drugGraphDF =  drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_50.csv'))

drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_70.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_100.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_over100.csv'))

#leave only nodes that are in repoBefore
drugGraphDF = drugGraphDF[(drugGraphDF['SUBJECT_NAME'].isin(repodrugs))|(drugGraphDF['SUBJECT_CUI'].isin(repoInds))]
drugGraphDF = drugGraphDF[(drugGraphDF['OBJECT_NAME'].isin(repodrugs))|(drugGraphDF['OBJECT_CUI'].isin(repoInds))]


#create cui mapping

cuimap1 = drugGraphDF[['SUBJECT_NAME','SUBJECT_CUI']]
cuimap2 = drugGraphDF[['OBJECT_NAME','OBJECT_CUI']]
cuimap1 = cuimap1.rename(columns={'SUBJECT_NAME':'NAME','SUBJECT_CUI':'CUI'})
cuimap2 = cuimap2.rename(columns={'OBJECT_NAME':'NAME','OBJECT_CUI':'CUI'})
cuimap1 = cuimap1.append(cuimap2)
cuimap1 = cuimap1.drop_duplicates()
cuimap1 = pn.merge(cuimap1,cui2vec,on='CUI',how='inner')

#leave only nodes that are in cuimap
drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_NAME'].isin(cuimap1['NAME'].unique())]
drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_NAME'].isin(cuimap1['NAME'].unique())]


drugGraphDF = drugGraphDF[['SUBJECT_NAME','OBJECT_NAME']]
drugGraphDF['weight'] = [1]*len(drugGraphDF)

drugGraphDFgb = drugGraphDF.groupby(['SUBJECT_NAME','OBJECT_NAME'],as_index=False).sum()


fullGraph = nx.from_pandas_edgelist(drugGraphDFgb,'SUBJECT_NAME','OBJECT_NAME')

#adjacency matrix
AdjMat = nx.adjacency_matrix(fullGraph)


'''
Create node features
'''
'''
degreeCentrality = nx.algorithms.centrality.degree_centrality(fullGraph)
betweenessCentrality = nx.algorithms.centrality.betweenness_centrality(fullGraph)
featureDF = pn.DataFrame()
featureDF['node'] = degreeCentrality.keys()
featureDF['dc'] = degreeCentrality.values()
featureDF['bc'] = betweenessCentrality.values()
'''

'''
Create features. The features for each node is the ml2vec embedding. 
If the node does not have mol2vec embeddings the features are a vector of ones
'''
#drugStructure holds all the drugs that we have a chemichal structure for. Compute mol2vec for each of them

modelMol2Vec = word2vec.Word2Vec.load('/home/galiasn/DATA/MechanismBasedRepurposing/Data/model_300dim.pkl')

drugStructure = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/structure links.csv",',')

drugStructure['noSmiles'] = drugStructure['SMILES'].isnull()
#drugStructure = drugStructure[drugStructure['noSmiles']==False]



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
#drugStructure = drugStructure[drugStructure['noSmiles']==False]
drugStructure['noSmiles'] = drugStructure['noSmiles'].fillna(1)
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


'''
RepoAfter
'''
repodrugs = repoAfter['drug_name'].unique()
repoInds = repoAfter['ind_id'].unique()

drugGraphDF = pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_10.csv')
drugGraphDF =drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_30.csv'))
drugGraphDF =  drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_50.csv'))

drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_70.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_100.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_over100.csv'))

#leave only nodes that are in repoBefore
drugGraphDF = drugGraphDF[(drugGraphDF['SUBJECT_NAME'].isin(repodrugs))|(drugGraphDF['SUBJECT_CUI'].isin(repoInds))]
drugGraphDF = drugGraphDF[(drugGraphDF['OBJECT_NAME'].isin(repodrugs))|(drugGraphDF['OBJECT_CUI'].isin(repoInds))]


#create cui mapping

cuimap1 = drugGraphDF[['SUBJECT_NAME','SUBJECT_CUI']]
cuimap2 = drugGraphDF[['OBJECT_NAME','OBJECT_CUI']]
cuimap1 = cuimap1.rename(columns={'SUBJECT_NAME':'NAME','SUBJECT_CUI':'CUI'})
cuimap2 = cuimap2.rename(columns={'OBJECT_NAME':'NAME','OBJECT_CUI':'CUI'})
cuimap1 = cuimap1.append(cuimap2)
cuimap1 = cuimap1.drop_duplicates()
cuimap1 = pn.merge(cuimap1,cui2vec,on='CUI',how='inner')

#leave only nodes that are in cuimap
drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_NAME'].isin(cuimap1['NAME'].unique())]
drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_NAME'].isin(cuimap1['NAME'].unique())]


drugGraphDF = drugGraphDF[['SUBJECT_NAME','OBJECT_NAME']]
drugGraphDF['weight'] = [1]*len(drugGraphDF)

drugGraphDFgb = drugGraphDF.groupby(['SUBJECT_NAME','OBJECT_NAME'],as_index=False).sum()


fullGraph = nx.from_pandas_edgelist(drugGraphDFgb,'SUBJECT_NAME','OBJECT_NAME')

#adjacency matrix
AdjMat = nx.adjacency_matrix(fullGraph)

'''
Create node features
'''
'''
degreeCentrality = nx.algorithms.centrality.degree_centrality(fullGraph)
betweenessCentrality = nx.algorithms.centrality.betweenness_centrality(fullGraph)
featuresDF = pn.DataFrame()
featuresDF['node'] = degreeCentrality.keys()
featuresDF['dc'] = degreeCentrality.values()
featuresDF['bc'] = betweenessCentrality.values()
'''

nodecuisnodes = list(fullGraph.nodes())
featureDF = pn.DataFrame()
featureDF['Name'] = nodecuisnodes
featureDF = pn.merge(featureDF,drugStructure[['Name','mol2vec']],on='Name',how='left')
featureDF['mol2vec']=featureDF['mol2vec'].fillna(1)
featureDF['mol2vec'] = featureDF['mol2vec'].apply(translateToVec)