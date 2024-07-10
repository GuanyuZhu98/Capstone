import cv2
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import pandas as pd
from matplotlib import pyplot as plt
import extractor


testSet = ['ATF-2L-01, 2L-05,06']
trainSet = ['Master Datasheet']

### !!! Notice 
###    1.Create a new folder named 'plot' under the same path with this file.
###    2.The csv file of trainset and testset should be also under the same path with this file.
###    3.file extractor.py should be also under the the same path with this file
### !!!

def sortData(data):
    data = data.replace('*****',np.nan)
    data['Viability (%)'] = data['Viability (%)'].str.rstrip('%').astype('float')
    for i in range(len(data.columns.tolist())):
        data.iloc[:,i]=data.iloc[:,i].astype(float)
    return(data)

def pretreate(Data,dum='trainset'):
    Datay = Data['SampleID']
    train_y = Datay.drop_duplicates().tolist()
    Data = pd.concat([sortData(Data.iloc[:,2:18]),Data['SampleID']],axis = 1)
    params = Data.columns.tolist()[2:16]
    
    for param in params:
        for i in train_y:
            plt.figure()
            sample = Data[Data['SampleID']==i]
            sample.dropna(how='all')
            sample = sample[sample['Run Time (days)']>=0]
            plt.title('{}'.format(i))
            dt = pd.concat([sample.iloc[:,0],sample[param]],axis=1).dropna()
            plt.plot(dt.iloc[:,0],dt.iloc[:,1])[0]
            plt.xlim([0, 20])
            fig = plt.savefig('plot/{}/{}_{}.png'.format(dum,i,param.replace('/','\\')))


    for param in params:
        for i in train_y:
            my_img = cv2.imread('plot/{}/{}_{}.png'.format(dum,i,param.replace('/','\\'))
                                ,cv2.IMREAD_GRAYSCALE)
            img = 255-my_img[43:252,55:387]
            cv2.imwrite('plot/{}/after/{}_{}.png'.format(dum,i,param.replace('/','\\')), img)


trainData = extractor.extract(trainSet)[0]
pretreate(trainData)
testData = extractor.extract(testSet)[0]
pretreate(testData,'testset')
print('Process finished!!')
