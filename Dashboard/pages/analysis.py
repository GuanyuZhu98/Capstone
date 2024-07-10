#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 12:51:09 2022

@author: danielzhu
"""

from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly,dash
from plotly.subplots import make_subplots
from matplotlib.pyplot import cm

import extractor

file_Names = ['ATF-2L-06',
              'ATF-2L-03,04,05;2L-65,66', #Original: Antifoam Added(Drop)
              'ATF-2L-01,02',
              'ATF-2L-08',
              'Master Datasheet',
              'ATF-2L-01--02; 2L-01--04',
              'ATF-2L-01, 2L-05,06',
              'ATF-2L-03, 2L-07,08'
              ]

## The csv file should be save as CSV(Comma delimited)

data = extractor.extract(file_Names)

'''




file_Names = ['ambrDatasheet']
'''
data = extractor.extract(file_Names)

for i in range(len(file_Names)):
    '''## Feed 3 Added (g) Perfusion Media Added (g) No.30 Column () This line have diff name
    ##
    data[i].drop(data[i].columns[[30]],axis = 1, inplace=True)'''
    data[i]['fileNames'] = file_Names[i]

dt = pd.concat(data)
header = dt.columns.tolist()



dash.register_page(__name__,suppress_callback_exceptions=True)

sampleDataFrame = []

for i in range(len(file_Names)):
    sampleDataFrame.append([])

Start = 0
header[3] = 'VCD-Viab'
dumParameter = header[3]

###== Here's the layout of html ==###
layout = html.Div([
    html.Div(html.H3('Correlation Coefficient Heatmap')),
    html.H1(
        'File'
        ),
    
    dcc.Dropdown(file_Names,file_Names[0],id = 'file'),
    html.Div(children = [dcc.Dropdown(['dum'],id = 'sampleselector-dropdown')]
                         ,id = 'sample-select-box')
    ,
    html.Div([
        dcc.Graph(
    id = 'heatmap'
    )
        ])
    ,
    
    

    ])

@callback(
    Output('sample-select-box','children'),
    Input('file','value')
    )
def children(value1):
    batchData = dt[dt['fileNames']==value1]
    batchName = batchData['SampleID'].drop_duplicates().tolist()
    return [dcc.Dropdown(batchName,batchName[0],id = 'sampleselector-dropdown')]

@callback(
    Output('heatmap','figure'),
    Input('sampleselector-dropdown','value'),
    Input('file','value')
    )

def showHeatmap(value1,value2):
    batchData = dt[dt['fileNames']==value2]
    usefulData = batchData[batchData['SampleID']==value1]

    corr_matrix = []
    fig = go.Figure()
    usefulData.dropna(axis='columns',inplace=True,how='all')
    hd = usefulData.columns.tolist()[3:17]
    try:
        for i in hd:
        
            row = []
            for j in hd:
                a = pd.concat([usefulData[i].interpolate(),usefulData[j].interpolate()],axis=1).dropna(how='all')
                
                try:
                    x1 = np.array(a.iloc[:,0].astype(float).tolist())
                except:
                    x1 = np.array(a.iloc[:,0].str.rstrip('%').astype('float').tolist())
                try:
                    x2 = np.array(a.iloc[:,1].astype(float).tolist())
                except:
                    x2 = np.array(a.iloc[:,1].str.rstrip('%').astype('float').tolist())
                r= np.corrcoef(x1, x2)[0,1]
                if r!=r: ## if correlation coeffecient is nan
                    row.append(0)
                else:
                    row.append(r)
            corr_matrix.append(row)

        fig = px.imshow(corr_matrix, text_auto=True,color_continuous_scale='RdBu_r',
                x=hd,
                y=hd)
        
        return(fig)
    except:
        pass
            
    return(fig)
            
    




    