# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:44:24 2019

@author: Galia
"""
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors



model = KeyedVectors.load_word2vec_format('D:\\Galia\\DeVine_etal_200\\DeVine_etal_200.txt')

