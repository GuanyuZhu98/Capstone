#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 12:51:34 2022

@author: danielzhu
"""

## A data pretreatment process
## 1. Identify the samples name (Seed Train; Batches)
## 2. Pull request from MySQL ## This will be done latter. 
##    Assuming there's already a giant csv file
##    
## 3. Input: Multiple csv file?
##    Output: A giant pandas dataframe:
    #   |File Name| Sample ID |Time|Other Parameters|

import pandas as pd
import os

class extractor:
    def __init__(self,data):
        self.data = data
    
    def extractInfo(self):
        data = self.data.dropna(how='all')
        data = data.dropna(axis=1,how='all')
        data = pd.DataFrame(data.iloc[2:,:].values,columns=data.iloc[1,:].values)
        ## Identify Seed Train SampleID & Time sequence SampleID
        
        self.header = data.columns
        
        ## Seed Train ID 
        ### (For ATF-2L-01,2L-05,06) is called P0D0 Thaw
        self.stID = data[((data['Passage/Day']=='P0 D0') |
                     (data['Passage/Day']=='P0 D0 Thaw'))].index.tolist()
        ## Test ID
        self.tsID = data[(data['Passage/Day']=='D0')].index.tolist()
        
        self.data = data
        
        dt1 = self.sortInfo(self.stID)
        dt2 = self.sortInfo(self.tsID,False)
        result = pd.concat([dt1,dt2])
        
        return(result)
    
    
    
    def sortInfo(self,indexList,isSeedTrain=True):
        ## delete empty samples and Return a concatenate DataFrame 
        ####    |index|Sample Name|Parameters|
        nameList = []
        dumData = []

        try:
            for i in range(len(indexList)):
                col1 = pd.DataFrame(self.data.iloc[indexList[i]:indexList[i+1]-3,3].values)
                col2 = pd.DataFrame(self.data.iloc[indexList[i]:indexList[i+1]-3,4].values)
    
                if (col1.count().values.sum()>1) & (col2.count().values.sum()>1):

                    ## If Dilution Factor column and Viability column both value is greater than 1,
                    ## This sample is valid.
                    ## Keep Processing
                    idx = indexList[i]
                    name = self.getName(idx)
                    nameList.append(name)
                    dt = pd.DataFrame(self.data.iloc[indexList[i]:indexList[i+1]-3,:].values)
                    dt.columns = self.header
                    dt['SampleID'] = name
                    dumData.append(dt)
                    
                
        except:
            ## This is the last number in indexlist
            if isSeedTrain:
                col1 = pd.DataFrame(self.data.iloc[indexList[i]:self.tsID[0]-4,3].values)
                col2 = pd.DataFrame(self.data.iloc[indexList[i]:self.tsID[0]-4,4].values)
                if (col1.count().values.sum()>1) & (col2.count().values.sum()>1):
                    idx = indexList[i]
                    name = self.getName(idx)
                    nameList.append(name)
                    dt = pd.DataFrame(self.data.iloc[indexList[i]:self.tsID[0]-4,:].values)
                    dt.columns = self.header
                    dt['SampleID'] = name
                    dumData.append(dt)

            else:
                col1 = pd.DataFrame(self.data.iloc[indexList[i]:,3].values)
                col2 = pd.DataFrame(self.data.iloc[indexList[i]:,4].values)
                if (col1.count().values.sum()>1) & (col2.count().values.sum()>1):
                    idx = indexList[i]
                    name = self.getName(idx)
                    nameList.append(name)
                    dt = pd.DataFrame(self.data.iloc[indexList[i]:,:].values)
                    dt.columns = self.header
                    dt['SampleID'] = name
                    dumData.append(dt)
            
            pass
            
            
        if len(dumData) == 0:
            return()
        result = pd.concat(dumData)

        return(result)
    
    
    def getName(self,idx):
        ## Sometimes the datasheet got a missing line
        if pd.notna(self.data.iloc[idx-2,2]):
            return(self.data.iloc[idx-2,2])
        else:
            return(self.data.iloc[idx-2,0])



def extract(file_Names):
    path = os.getcwd()
    dum = []

    
    for file_Name in file_Names:
        a = extractor(pd.read_csv('{}/{}.csv'.format(path,file_Name)))
        dum.append(a.extractInfo())
    return(dum)

## Here, dum is what we need
## Useful info: dum
## files should be in the same folder with this py file

