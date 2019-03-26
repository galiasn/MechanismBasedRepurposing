# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 09:43:57 2019

@author: Galia

"""
import sys, os
print(sys.prefix)
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd()))+'/mol2vec')

'''
IMPORTANT NOTE: this code needs to be run under python 2 (2.7) for mol2vec to work!
'''
import pandas as pn

from mol2vec import features
from mol2vec import helpers
from mol2vec.features import mol2alt_sentence, mol2sentence, MolSentence, DfVec, sentences2vec
from gensim.models import word2vec
from gensim.models import KeyedVectors
from rdkit import Chem
from rdkit.Chem import AllChem
#first we add the SMILES for each drug

drugStructure = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/structure links.csv")
drugStructure = drugStructure.rename(columns={'DrugBank ID':'drug_id'})
fullRepoDB = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/full.csv")
fullRepoDB = fullRepoDB.groupby('drug_id',as_index=False).first()
fullRepoDB = pn.merge(fullRepoDB,drugStructure[['drug_id','SMILES']],on='drug_id',how='inner')
fullRepoDB['noSmiles'] = fullRepoDB['SMILES'].isnull()
fullRepoDB = fullRepoDB[fullRepoDB['noSmiles']==False]
#now we get mol2vec vector for each drug

modelMol2Vec = word2vec.Word2Vec.load('/home/galiasn/DATA/MechanismBasedRepurposing/Data/model_300dim.pkl')

#aa_smis = fullRepoDB['mol']
#count =0
#for f in aa_smis:
#    MolSentence(mol2alt_sentence(f, 1))
#    count+=1
#    print(count)
#aas = [Chem.MolFromSmiles(x) for x in aa_smis]




fullRepoDB['mol'] = fullRepoDB['SMILES'].apply(Chem.MolFromSmiles)
fullRepoDB['noSmiles'] = fullRepoDB['mol'].isnull()
fullRepoDB = fullRepoDB[fullRepoDB['noSmiles']==False]
fullRepoDB['mol-sentences'] = fullRepoDB.apply(lambda x: MolSentence(mol2alt_sentence(x['mol'], 1)), axis=1)
fullRepoDB['mol2vec'] = [x for x in sentences2vec(fullRepoDB['mol-sentences'], modelMol2Vec, unseen='UNK')]


mol2vecNames = fullRepoDB['drug_name'].unique()