'''
create embeddings for terms in repo
If a term is composed of more than one work we add the embeddings
'''
def getEmbedding(term):
    e = np.zeros(150)
    for w in term:
        if w in model.wv.vocab:
            e = e+model.wv.word_vec(w)
        e = e/len(term)
    return e

def isZero(var):
    return var.sum()

model = gensim.models.Word2Vec.load('/mnt/galiasn/word2vec25MNoCUI')

repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")

repo['drug_name_processed'] = repo['drug_name'].apply(gensim.utils.simple_preprocess)
repo['drug_name_processed'] = repo['drug_name_processed'].apply(removeStopWords)
repo['drug_name_processed'] = repo['drug_name_processed'].apply(stem)

repo['drugEmb'] = repo['drug_name_processed'].apply(getEmbedding)

repo['ind_name_processed'] = repo['ind_name'].apply(gensim.utils.simple_preprocess)
repo['ind_name_processed'] = repo['ind_name_processed'].apply(removeStopWords)
repo['ind_name_processed'] = repo['ind_name_processed'].apply(stem)
repo['indEmb'] = repo['ind_name_processed'].apply(getEmbedding)

repo.to_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID_Embedding.csv")



repo['indZero'] = repo['indEmb'].apply(isZero)
repo['drugZero'] = repo['drugEmb'].apply(isZero)
repo = repo[(repo['indZero']!=0)&(repo['drugZero']!=0)]


'''
Create training data for links in repoBefore
'''

cutYear = 1990
repoBefore = repo[repo['pubYear']<cutYear]
repoAfter = repo[repo['pubYear']>=cutYear]


def appendarrays(var1,var2):
    return np.hstack([var1,var2])

def getLinkData(repoTable1):

    repoTable = repoTable1[['drug_name','drugEmb','ind_name','indEmb','pubYear']].copy()
    repoTable['lable'] = [1]*len(repoTable)

    repoNeg = pn.DataFrame()
    repoNeg['drug_name'] = list(repoTable['drug_name'])
    repoNeg['drugEmb'] = list(repoTable['drugEmb'])

    #reorder table to get false pairs
    repoTable = repoTable.sort_values('ind_name',ascending=True)
    repoNeg['ind_name'] = list(repoTable['ind_name'])
    repoNeg['indEmb'] = list(repoTable['indEmb'])

    repoNeg = pn.merge(repoNeg,repoTable[['drug_name','ind_name','pubYear']],on=['drug_name','ind_name'],how='left')
    repoNeg['pubYear'] = repoNeg['pubYear'].fillna(1)
    repoNeg = repoNeg[repoNeg['pubYear']==1] #row that is only in repoNeg
    repoNeg = repoNeg[['drug_name','ind_name','drugEmb','indEmb']]
    repoNeg['lable'] = [0]*len(repoNeg)

    data = repoTable.append(repoNeg)

    data['vecs'] = map(appendarrays,data['drugEmb'],data['indEmb'])

    return np.vstack(data['vecs']),list(data['lable'])


X,y = getLinkData(repoBefore)



XAfter,yAfter = getLinkData(repoAfter)

