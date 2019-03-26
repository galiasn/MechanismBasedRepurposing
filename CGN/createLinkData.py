
import pandas as pn
import numpy as np
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")

cutYear = 1990
repoBefore = repo[repo['pubYear']<cutYear]
repoAfter = repo[repo['pubYear']>=cutYear]

#read all predicate table so we have name to cui mapping
test = pn.read_csv('/mnt/galiasn/test2/test2.txt')
test.columns = [u'PREDICATION_ID', u'SENTENCE_ID', u'PMID', u'PREDICATE',
       u'SUBJECT_CUI', u'SUBJECT_NAME', u'SUBJECT_SEMTYPE', u'SUBJECT_NOVELTY',
       u'OBJECT_CUI', u'OBJECT_NAME', u'OBJECT_SEMTYPE', u'OBJECT_NOVELTY']

test = test[['SUBJECT_NAME','SUBJECT_CUI']]
test = test.rename(columns={'SUBJECT_NAME':'Name','SUBJECT_CUI':'cui'})
test = test.drop_duplicates()

cui2vec = pn.read_csv('/mnt/galiasn/cui2vec_pretrained/cui2vec_pretrained.csv')
cuisnames = cui2vec['Unnamed: 0']
cui2vec = cui2vec.rename(columns={'Unnamed: 0':'cui'})


def appendarrays(var1,var2):
    return np.hstack([var1,var2])

def getLinkData(repoTableO,testcuimap,cui2vec,mol2vec,drugEmbed='cui'):
    repoTable = repoTableO.copy()

    if drugEmbed=='cui':
        #add drugs cui
        repoTable = repoTable.rename(columns={'drug_name': 'Name'})
        repoTable = pn.merge(repoTable,testcuimap,on='Name',how='inner')

        #add drugs cui2vec
        repoTable = pn.merge(repoTable,cui2vec,on='cui',how='inner')
        repoTable = repoTable.drop_duplicates()
        vectors = np.asarray(repoTable.loc[:,'V1':'V500'])
        repoTable = repoTable[['Name','cui','ind_name','ind_id']]
        repoTable['drugVec'] = list(vectors)
    else: #mol2vec
        repoTable = pn.merge(repoTable,mol2vec,on='drug_name',how='inner')
        repoTable= repoTable.rename(columns={'mol2vec':'drugVec','drug_name':'Name'})
        repoTable['cui'] =['C0']*len(repoTable) #dummy

    #add ind cui2vec

    cui2vec = cui2vec.rename(columns={'cui':'ind_id'})
    repoTable = pn.merge(repoTable, cui2vec, on='ind_id', how='inner')
    indvectors = np.asarray(repoTable.loc[:,'V1':'V500'])
    repoTable = repoTable[['Name', 'cui', 'ind_name', 'ind_id','drugVec']]
    cui2vec = cui2vec.rename(columns={'ind_id': 'cui'})

    repoTable['indVec'] = list(indvectors)

    repoTable['lable'] = [1]*len(repoTable)

    repoNeg = pn.DataFrame()
    repoNeg['Name'] = list(repoTable['Name'])
    repoNeg['drugVec'] = list(repoTable['drugVec'])

    #reorder table to get false pairs
    repoTable = repoTable.sort_values('ind_name',ascending=True)
    repoNeg['ind_name'] = list(repoTable['ind_name'])
    repoNeg['indVec'] = list(repoTable['indVec'])

    repoNeg = pn.merge(repoNeg,repoTable[['Name','ind_name','cui']],on=['Name','ind_name'],how='left')
    repoNeg = repoNeg.fillna(1)
    repoNeg = repoNeg[repoNeg['cui']==1]
    repoNeg = repoNeg[['Name','ind_name','drugVec','indVec']]
    repoNeg['lable'] = [0]*len(repoNeg)

    data = repoTable.append(repoNeg)

    data['vecs'] = map(appendarrays,data['drugVec'],data['indVec'])

    return np.vstack(data['vecs']),list(data['lable'])


X,y = getLinkData(repoBefore,test,cui2vec,fullRepoDB[['drug_name','mol2vec']],drugEmbed='mol2vec')

XAfter,yAfter = getLinkData(repoAfter,test,cui2vec,fullRepoDB[['drug_name','mol2vec']],drugEmbed='mol2vec')