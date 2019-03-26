


import pandas as pn

def getcui2vecEmbedding(cui):
    if cui in cui2vec['Unnamed: 0'].unique():
        return list(cui2vec[cui2vec['Unnamed: 0']==cui].loc[:,'V1':'V500'].iloc[0])
    else:
        return 500*[0]

cui2vec = pn.read_csv('/mnt/galiasn/cui2vec_pretrained/cui2vec_pretrained.csv')


#add drug cui to data
sentencesT = pn.read_csv("/mnt/galiasn/sentences_TREATS/sentences_TREATS.csv",sep=',')

sentencesDrugs = sentencesT[sentencesT['SUBJECT_SEMTYPE']=='phsu']['SUBJECT_NAME'].unique()
sentencesDrugs = set(sentencesDrugs).union(set(sentencesT[sentencesT['OBJECT_SEMTYPE']=='phsu']['OBJECT_NAME'].unique()))

sentencesDrugsDF = sentencesT[sentencesT['SUBJECT_NAME'].isin(sentencesDrugs)][['SUBJECT_NAME','SUBJECT_CUI']]
sentencesDrugsDF = sentencesDrugsDF.drop_duplicates()
sentencesDrugsDF = sentencesDrugsDF.rename(columns={'SUBJECT_NAME':'drug_name','SUBJECT_CUI':'drug_CUI'})



cuiNames = sentencesDrugsDF['drug_name'].unique()