import extractor
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import pandas as pd

scaler = StandardScaler()
acc = 0.95
pca = PCA(acc)


trainSet = ['Master Datasheet']
testSet = ['ATF-2L-01, 2L-05,06']

def sortData(data):
    data = data.replace('*****',np.nan)
    data['Viability (%)'] = data['Viability (%)'].str.rstrip('%').astype('float')
    for i in range(len(data.columns.tolist())):
        data.iloc[:,i]=data.iloc[:,i].astype(float)
    data = data.interpolate(method='linear')
    data = data.fillna(0)
    return(data)

trainData = extractor.extract(trainSet)[0]
trainDatay = trainData['SampleID']
train_y = trainDatay.drop_duplicates().tolist()
train_dic = {}
for i in range(len(train_y)):
    train_dic[train_y[i]] = i
trainDatay = trainDatay.replace(train_dic)
inverted_train_dic = dict(zip(train_dic.values(),train_dic.keys()))

testData = extractor.extract(testSet)[0]
test_y = testData['SampleID']

trainData = trainData.iloc[:,3:18]
testData = testData.iloc[:,3:18]

trainData = sortData(trainData)
testData = sortData(testData)

scaler.fit(trainData)

trainData = scaler.transform(trainData)
testData = scaler.transform(testData)

pca.fit(trainData)
print('{} principal components are remained based on {}% information loss'.format(pca.n_components_,int((1-acc)*100)))

trainData = pca.transform(trainData)
testData = pca.transform(testData)

## This is the logistic regression try not accurate
logisticRegr = LogisticRegression(solver='lbfgs')
logisticRegr.fit(trainData,trainDatay)

result = pd.Series(logisticRegr.predict(testData))
result = result.replace(inverted_train_dic)
data = [test_y.tolist(),result.tolist()]
data = np.array(data)
result = pd.DataFrame(data.T)

result.to_csv('result',index=False)