# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 09:43:57 2019

@author: Galia
"""
import pandas as pn

drugStructure = pn.read_csv("D:\\Galia\\DrugBankStructure\\structure links.csv")
drugStructure = drugStructure.rename(columns={'DrugBank ID':'drug_id'})
fullRepoDB = pn.read_csv("D:\\Galia\\mechanismBased\\full.csv")

fullRepoDB = pn.merge(fullRepoDB,drugStructure[['drug_id','SMILES']],on='drug_id',how='inner')