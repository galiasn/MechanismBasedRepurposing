'''
This repository is created based on PubMed citations downloaded from the PubMed search engine
1.We go over each file, extract the title and abstracts and create a list of sentences from them
2. For each sentence we identify entities and change them into their CUIs (UMLS)
'''

from Bio import Entrez
from Bio import Medline

Repository=[]
#################################
with open("/mnt/galiasn/pubmed_result_1960_1970.txt") as handle:
    records = Medline.parse(handle)
    for record in records:
        if 'AB' in record.keys():
            Repository+=record['AB'].split('.')
        if 'OAB' in record.keys():
            Repository+=record['OAB'][0].split('.')
        if 'TI' in record.keys():
            Repository+=record['TI'][0].split('.')
        if 'BTI' in record.keys():
            Repository += record['BTI'][0].split('.')
handle.close()

with open("/mnt/galiasn/pubmed_result_1970_1980.txt") as handle:
    records = Medline.parse(handle)
    for record in records:
        if 'AB' in record.keys():
            Repository+=record['AB'].split('.')
        if 'OAB' in record.keys():
            Repository+=record['OAB'][0].split('.')
        if 'TI' in record.keys():
            Repository+=record['TI'][0].split('.')
        if 'BTI' in record.keys():
            Repository += record['BTI'][0].split('.')
handle.close()

with open("/mnt/galiasn/pubmed_result_1980_1990.txt") as handle:
    records = Medline.parse(handle)
    for record in records:
        if 'AB' in record.keys():
            Repository+=record['AB'].split('.')
        if 'OAB' in record.keys():
            Repository+=record['OAB'][0].split('.')
        if 'TI' in record.keys():
            Repository+=record['TI'][0].split('.')
        if 'BTI' in record.keys():
            Repository += record['BTI'][0].split('.')
handle.close()


#go over all sentences and change entities to cuis.
#At this stage we check only for the entities that we are interested in - the ones in cuiDict

#This will take too long. We will do it as part of the preprocessing

repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")
terms = set(repo['drug_cui'].unique()).union(set(repo['ind_cui'].unique()))


#randomly select 1M sentences from repository
import datetime
import random
RepoSample = random.sample(Repository,50000)

res = map(fn,RepoSample)

def AugmentSentence(sent):
    augmented=[]
    sentTerms = getTermsInSentence(sent, wrapper)
    jointTerms = set(sentTerms).intersection(set(terms))
    if (len(jointTerms) > 0):
        for t in jointTerms:
            augmented.append(ReplacetermInSentence(t, sent, wrapper))
    else:
        augmented.append(sent)
    return augmented

fn = AugmentSentence
a = datetime.datetime.now()


b = datetime.datetime.now()
print((b-a).total_seconds())

count=0
actuallyAugmented=0
augmentedRepository=[]
for sent in Repository:
    sentTerms = getTermsInSentence(sent,wrapper)
    jointTerms = set(sentTerms).intersection(set(terms))
    if(len(jointTerms)>0):
        for t in jointTerms:
            actuallyAugmented+=1
            augmentedRepository.append(ReplacetermInSentence(t, sent, wrapper))
    else:
        augmentedRepository.append(sent)

    count+=1
    print("*"+str(count)+"*"+str(actuallyAugmented))
