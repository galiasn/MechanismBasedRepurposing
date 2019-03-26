

from keras.layers import Input, Dropout, Dense
from keras.models import Model,Sequential
from keras.optimizers import Adam
from keras.regularizers import l2
import random

'''
Network for link prediction
'''

inputDim = 300


kmodel = Sequential()
kmodel.add(Dense(300, input_dim=inputDim, kernel_initializer='normal', activation='relu'))
#model.add(Dense(500, kernel_initializer='normal', activation='relu'))
kmodel.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))

kmodel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])





#random.shuffle(y)
kmodel.fit(X,y ,epochs=10,verbose=1)


#MICRO
XAfter,yAfter = getLinkData(repoAfter)
preds = kmodel.predict(XAfter)

correct = 0
ind = 0
while ind<len(preds):
    if ((preds[ind][0]>0.5) & yAfter[ind]==1)|((preds[ind][0]<=0.5) & yAfter[ind]==0):
        correct+=1
    ind+=1


print((correct+0.0)/len(yAfter))



#MACRO
res={}
drugs = repoAfter['drug_name'].unique()
for d in drugs:
    r = repoAfter[repoAfter['drug_name']==d]
    XAfter, yAfter = getLinkData(r)
    preds = kmodel.predict(XAfter)

    correct = 0
    ind = 0
    while ind < len(preds):
        if ((preds[ind][0] > 0.5) and yAfter[ind] == 1) or ((preds[ind][0] <= 0.5) and yAfter[ind] == 0):
            correct += 1
        ind += 1
    res[d] = (correct+0.0)/len(yAfter)

print(np.mean(res.values()))