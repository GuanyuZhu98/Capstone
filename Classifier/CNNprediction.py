import cv2
import numpy as np
import tensorflow as tf
import pandas as pd
import csv
import keras
import extractor
from matplotlib import pyplot as plt
import pickle
from keras.models import load_model 
classifier = load_model('cnn_model.h5')

trainSet = ['Master Datasheet']
testSet = ['ATF-2L-01, 2L-05,06']

def sortData(data):
    data = data.replace('*****',np.nan)
    data['Viability (%)'] = data['Viability (%)'].str.rstrip('%').astype('float')
    for i in range(len(data.columns.tolist())):
        data.iloc[:,i]=data.iloc[:,i].astype(float)
    return(data)

def createData(Data,sets='trainset'):
    Datay = Data['SampleID']
    train_y = Datay.drop_duplicates().tolist()
    Data = pd.concat([sortData(Data.iloc[:,2:18]),Data['SampleID']],axis = 1)
    params = Data.columns.tolist()[2:16]
    dt = []

    
    for param in params:
        dum = []
        for i in train_y:
            img = cv2.imread('plot/{}/after/{}_{}.png'.format(sets,i,param.replace('/','\\')),0)
            img = (img/255)
            dum.append(np.array(img).T)

        dt.append(np.array(dum).T)
    return(params,np.array(dt).T,train_y)
    
params1,x_test,y_test = createData(extractor.extract(testSet)[0],'testset')
print(np.shape(x_test))

def valid(i):
    x0 = x_test[i]
    x0 =np.expand_dims(x0, axis =0)
    result = classifier.predict(x0)[0]
    clas = ['Seed Train', 'ATF-2L-01', 'ATF-2L-03', 'ATF-2L-04', '2L-65', '2L-66', 'ATF-2L-06', '2L-06 (2015)', '2L-08 (2015)', 'ATF-2L-08', '2L-30']
    
    predic_idx = list(result).index(max(result))
    predic = clas[predic_idx]
    return(predic,max(result))
for i in range(len(y_test)):
    predic,prob = valid(i)
    print('Ground Truth:{}, Prediction:{},Probability:{}'.format(y_test[i],predic,prob))


