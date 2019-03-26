


import pandas as pn
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors

def getword2vecEmbedding(cui):
    if cui in w2vmodel.vocab:
        return w2vmodel.word_vec(cui)
    else:
        return 300*[0]


w2vmodel = KeyedVectors.load_word2vec_format('/mnt/galiasn/DeVine_etal_200/DeVine_etal_200.txt')




#add drug cui to data
sentencesT = pn.read_csv("/mnt/galiasn/sentences_TREATS/sentences_TREATS.csv",sep=',')

sentencesDrugs = sentencesT[sentencesT['SUBJECT_SEMTYPE']=='phsu']['SUBJECT_NAME'].unique()
sentencesDrugs = set(sentencesDrugs).union(set(sentencesT[sentencesT['OBJECT_SEMTYPE']=='phsu']['OBJECT_NAME'].unique()))

sentencesDrugsDF = sentencesT[sentencesT['SUBJECT_NAME'].isin(sentencesDrugs)][['SUBJECT_NAME','SUBJECT_CUI']]
sentencesDrugsDF = sentencesDrugsDF.drop_duplicates()
sentencesDrugsDF = sentencesDrugsDF.rename(columns={'SUBJECT_NAME':'drug_name','SUBJECT_CUI':'drug_CUI'})



