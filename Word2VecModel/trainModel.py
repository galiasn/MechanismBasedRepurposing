import gensim
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer


def stem(var):
    ps = PorterStemmer()
    newvar = []
    for v in var:
        newvar.append(ps.stem(v))
    return newvar

def removeStopWords(var):
    return set(var)-ENGLISH_STOP_WORDS

documents = map(gensim.utils.simple_preprocess,Repository)
documents = map(removeStopWords,documents)
documents = map(stem,documents)


model = gensim.models.Word2Vec (documents, size=150, window=10, min_count=2, workers=10)
model.train(documents,total_examples=len(documents),epochs=10)
model.save('/mnt/galiasn/word2vec25MNoCUI')


