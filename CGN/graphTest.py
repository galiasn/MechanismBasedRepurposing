import pandas as pn

from mol2vec import features
from mol2vec import helpers
from mol2vec.features import mol2alt_sentence, mol2sentence, MolSentence, DfVec, sentences2vec
from gensim.models import word2vec
from gensim.models import KeyedVectors
from rdkit import Chem
from rdkit.Chem import AllChem

import scipy.sparse.csr as csr
import pickle as pkl
import random


drugStructure = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/structure links.csv",',')
drugStructureNames =drugStructure['Name'].unique()


drugGraphDF = pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_10.csv')
drugGraphDF =drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_30.csv'))
drugGraphDF =  drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_50.csv'))

drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_70.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_100.csv'))
drugGraphDF = drugGraphDF.append(pn.read_csv('/mnt/galiasn/DrugPredicates/predicate_PSHU_RCPT_DSYN_over100.csv'))

drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_SEMTYPE']=='phsu']
drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_SEMTYPE']=='phsu']

#drugGraphDF = drugGraphDF[drugGraphDF['SUBJECT_NAME'].isin(drugStructureNames)]
#drugGraphDF = drugGraphDF[drugGraphDF['OBJECT_NAME'].isin(drugStructureNames)]

selfLoopDF = pn.DataFrame()
selfLoopDF['SUBJECT_NAME'] = list(drugGraphDF['SUBJECT_NAME'].unique())
selfLoopDF['OBJECT_NAME'] = list(drugGraphDF['SUBJECT_NAME'].unique())




drugGraphDF = selfLoopDF
drugGraphDF['weight'] = [1]*len(drugGraphDF)
drugGraphDFgb = drugGraphDF.groupby(['SUBJECT_NAME','OBJECT_NAME'],as_index=False).sum()


fullGraph = nx.from_pandas_edgelist(drugGraphDFgb,'SUBJECT_NAME','OBJECT_NAME')


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
    #if type(val)==type(1):
    #    return [0]*300
    #else:
    #    return val
    return [0.5]*300
nodecuisnodes = list(fullGraph.nodes())
featureDF = pn.DataFrame()
featureDF['Name'] = nodecuisnodes
featureDF = pn.merge(featureDF,drugStructure[['Name','mol2vec']],on='Name',how='left')
featureDF['mol2vec']=featureDF['mol2vec'].fillna(1)
featureDF['mol2vec'] = featureDF['mol2vec'].apply(translateToVec)

trainidx = np.random.choice(np.arange(0,len(featureDF)),int(np.round(0.7*len(featureDF))))
testidx = set(np.arange(0,len(featureDF)))-set(trainidx)


featuressparse = np.vstack(featureDF['mol2vec'])

with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'ally'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)




featuressparse = np.vstack(featureDF['mol2vec'].loc[trainidx])
with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'y'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)

featuressparse = np.vstack(featureDF['mol2vec'].loc[testidx])
with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'ty'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)

featuressparse = csr.csr_matrix(np.vstack(featureDF['mol2vec']))

with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'allx'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)




featuressparse = csr.csr_matrix(np.vstack(featureDF['mol2vec'].loc[trainidx]))
with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'x'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)

featuressparse = csr.csr_matrix(np.vstack(featureDF['mol2vec'].loc[testidx]))
with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'tx'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(featuressparse,f, encoding='latin1')
    else:
        pkl.dump(featuressparse,f)


with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.test.{}".format('galia', 'index'),'wb') as f:
    for s in testidx:
        f.write(str(s)+'\n')


#create indexes from names
nodenames = list(set(drugGraphDFgb['SUBJECT_NAME'].unique()).union(drugGraphDFgb['OBJECT_NAME'].unique())) #remove duplicates
def changeNodeNameToIndex(name):
    return nodenames.index(name)


drugGraphDFgb['SUBJECT_NAME'] = drugGraphDFgb['SUBJECT_NAME'].apply(changeNodeNameToIndex)
drugGraphDFgb['OBJECT_NAME'] = drugGraphDFgb['OBJECT_NAME'].apply(changeNodeNameToIndex)


fullGraph = nx.from_pandas_edgelist(drugGraphDFgb,'SUBJECT_NAME','OBJECT_NAME')

with open("/home/galiasn/DATA/MechanismBasedRepurposing/CGN/gcn-master/gcn/data/ind.{}.{}".format('galia', 'graph'),'wb') as f:
    if sys.version_info > (3, 0):
        pkl.dump(nx.to_dict_of_lists(fullGraph),f, encoding='latin1')
    else:
        pkl.dump(nx.to_dict_of_lists(fullGraph),f)