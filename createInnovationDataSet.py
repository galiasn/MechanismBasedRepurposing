
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
def getIndVector(val):
    if val in model.vocab:
        return model.wv.word_vec(val)
    else:
        return np.asarray(200*[0])

model = KeyedVectors.load_word2vec_format('/mnt/galiasn/DeVine_etal_200/DeVine_etal_200.txt')



#We create a repurposing sata set that contains innovative repurposing.
# i.e. the new indications are significantly different than the original indications

repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")  # type: object
tmp = repo.copy()
tmp['sum'] = [1]*len(repo)
tmp = tmp.groupby('drug_id',as_index=False).sum()
tmp = tmp[tmp['sum']>1]
repo = repo[repo['drug_id'].isin(tmp['drug_id'].unique())]
#repo['w2v'] = repo['ind_id'].apply(getIndVector)


#for each drug, we find first indication
repo = repo.sort_values('pubYear',ascending=True)
repoGBFirst = repo.groupby('drug_id',as_index=False).first()

#for each drug, find indications that are far from the original
allInddiff =[]
notInVocab = 0
firstNotInVocab = 0
avgIndDiff = []
for d in repoGBFirst['drug_id'].unique():
    firstIndication=repoGBFirst[repoGBFirst['drug_id']==d]
    newIndications = repo[(repo['drug_id']==d)&(repo['ind_id'].isin(list(firstIndication['ind_id']))==False)]
    newInddict = {}
    if firstIndication['ind_id'].iloc[0] in model.wv.vocab:
        for ni in newIndications['ind_id'].unique():
            niIndDiff = []
            if ni in model.wv.vocab:
                sim = model.similarity(ni,firstIndication['ind_id'].iloc[0])
                newInddict[ni] = sim
                niIndDiff.append(sim)
                allInddiff.append(sim)
            else:
                notInVocab+=1

        if len(niIndDiff)>0:
            avgIndDiff.append(np.mean(niIndDiff))
    else:
        firstNotInVocab+=1

meanmeanSim = np.mean(avgIndDiff)
meanstdSim = np.std(avgIndDiff)
meanSim = np.mean(allInddiff)
stdSim = np.std(allInddiff)

threshold = meanSim-2*stdSim

drugInnovativeIndication={}
for d in repoGBFirst['drug_id'].unique():
    firstIndication=repoGBFirst[repoGBFirst['drug_id']==d]
    newIndications = repo[(repo['drug_id']==d)&(repo['ind_id'].isin(list(firstIndication['ind_id']))==False)]
    innovative=[]
    if firstIndication['ind_id'].iloc[0] in model.wv.vocab:
        for ni in newIndications['ind_id'].unique():
            if ni in model.wv.vocab:
                sim = model.similarity(ni,firstIndication['ind_id'].iloc[0])
                if sim<threshold:
                    innovative.append(ni)
    if len(innovative)>0:
        drugInnovativeIndication[d] = innovative

#leave only innovative indications
innovativeDF = pn.DataFrame()
for d in drugInnovativeIndication.keys():
    indlist = drugInnovativeIndication[d]
    indlist.append(repoGBFirst[repoGBFirst['drug_id']==d]['ind_id'].iloc[0])
    tmp = repo[(repo['drug_id']==d)&repo['ind_id'].isin(indlist)]
    innovativeDF =innovativeDF.append(tmp)

innovativeDF.to_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/innovativeDFMeanSTD2_5.csv")