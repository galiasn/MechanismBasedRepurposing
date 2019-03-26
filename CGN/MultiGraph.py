'''
We build two graphs:
1. using PubMed sentences
2. using Mol2Vec embeddings - here the edge weights are the embedding distances

We train a GCM on both graphs, and combine them. The end task is a true/false classification of a pair (drug,indication)
'''
import keras.backend as K

#X - PubMed graph
#M - Mol2Vec graph

X_in = Input(shape=(X.shape[1],))
H = Dropout(0.5)(X_in)
H = GraphConvolution(16, support, activation='relu', kernel_regularizer=l2(5e-4))([X_in]+G)

M_in = Input(shape=(M.shape[1],))
HM = Dropout(0.5)(M_in)
HM = GraphConvolution(16, supportM, activation='relu', kernel_regularizer=l2(5e-4))([M_in]+GM)


Y = GraphConvolution(y.shape[1], support, activation='softmax')([H]+G,[HM]+GM)

model = Model(inputs=[X_in]+G,[Xm_in]+GM, outputs=Y)
model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.01))



