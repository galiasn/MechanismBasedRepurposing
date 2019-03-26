from MetaMapWrapper import *
import pandas as pn

wrapper = MetaMapWrapper()
texts = ['Hypertension is a multifactorial disease involving the nervous, renal, ' \
           'and cardiovascular systems. ']
output_list = wrapper.analyze_texts(texts)

running_index = 1
for concept_dict in output_list:
    print (running_index)
    for concept_key in concept_dict:
        print (concept_key + ': ' + str(concept_dict[concept_key]))
    running_index += 1

def getTermsInSentence(text,wrapper):
    terms=[]
    try:
        out = wrapper.analyze_texts([text])
        for o in out:
            terms.append(o['cui'])
    except:
        print('getTermsInSentence exception')
    return terms

def TranslateTerm(text,wrapper):
    out = wrapper.analyze_texts([text])
    for o in out:
        if o['original_name']==text:
            return o['cui']
    #else-return first result
    return out[0]['cui']

def FindTermInSentence(term,text,wrapper):
    out = wrapper.analyze_texts([text])
    for o in out:
        if o['cui']==term:
            return o['mappings']
    #else
    return -1

def ReplacetermInSentence(term,text,wrapper):
    indexes = FindTermInSentence(term,text,wrapper)
    if indexes==-1:
        return -1
    newtext = text
    for i in indexes:
        newtext =  newtext.replace(newtext[i[0]:(i[0]+i[1])],term)
    return newtext

def getCUIFromDict(name):
    if name in cuiDict.keys():
        return cuiDict[name]
    else:
        return 'C0'
repo = pn.read_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")
cuiDict = {}
problemTerms=[]
for d in repo['drug_name'].unique():
    try:
        cuiDict[d] = TranslateTerm(d,wrapper)
    except:
        problemTerms.append(d)
for d in repo['ind_name'].unique():
    try:
        cuiDict[d] = TranslateTerm(d,wrapper)
    except:
        problemTerms.append(d)


cuiDict['Legionella pneumophila pneumonia'] = 'C0857846'
cuiDict['Osteolytic Lesions of Multiple Myeloma'] = 'C3898069'

repo['drug_cui'] = repo['drug_name'].apply(getCUIFromDict)
repo['ind_cui'] = repo['ind_name'].apply(getCUIFromDict)
repo.to_csv("/home/galiasn/DATA/MechanismBasedRepurposing/Data/repoyearWYear_indID.csv")

