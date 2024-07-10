import cv2
import numpy as np
import tensorflow as tf
import pandas as pd
import extractor
from matplotlib import pyplot as plt
import pickle

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
    
params1,data1,train_y1 = createData(extractor.extract(trainSet)[0])
#data2,train_y2 = createData(extractor.extract(testSet)[0],'testset')


## model building
#input_ = (11,209,332,14) #14 param(channel), 11 samples
input_=(332,209,14)

model = tf.keras.models.Sequential([
    
    tf.keras.layers.Conv2D(32,(5,5),padding='same',input_shape=input_),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(32,(5,5)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(4,4)),
    tf.keras.layers.Dropout(0.25),
    
    tf.keras.layers.Conv2D(64,(5,5),padding='same',input_shape=input_),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(64,(5,5)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(0.25),
    
    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(train_y1)),
    tf.keras.layers.Activation('softmax') 
    ])

model.summary()




x_train = np.array(data1).reshape(11,332,209,14)
print(np.shape(x_train))
y_train = np.eye(11)


model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

hist = model.fit(x_train,y_train,batch_size = 7,epochs=50)

model.save('cnn_model.h5')

plt.plot(hist.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.show()
    









