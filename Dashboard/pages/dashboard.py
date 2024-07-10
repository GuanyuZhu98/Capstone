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
    html.Div(children = [
        html.H1(
            'Upstream Process Dashboard'
            )
        ],
        style={'text-align':'center'}
        )
    ,
    html.Div(children=[
    html.Div(children = [
        dcc.Dropdown(header[3:len(header)-4],header[4],id = 'parameter-dropdown')
        ],
        style={
               'width': 200, 'height': 50, 'margin-left':10
               }),
    
    html.Div(children=[
        dcc.Dropdown(file_Names,file_Names[0],id = 'fileselector-dropdown')
        ],
        style={
               'width': 200, 'height': 50, 'margin-left':10
               }
        
        ),
    html.Div(id = 'sample-select-checklist',children = [
        dcc.Checklist(
                [''],id = 'samples'
                )
        ## This is a dum checklist, just prevent system from reporting error.
        ],
        style = {
               'width': 200, 'height': 100, 'margin-left':10
               }
        
        )],
        style = {'display': 'inline-block',
            'width': 220, 'height':220, 'margin-left':10
            }
    ),
    html.Div(
        dcc.Graph(
        id = 'graph'
        ),
        style = {'display': 'inline-block',
               'width': 900, 'height': 400
               }
        
        )
    
    
    
    ]
    )

@callback(
    Output('sample-select-checklist','children'),
    Input('fileselector-dropdown','value'),
    Input('parameter-dropdown','value')
    )
def show_samples(value1,parameter):
    global sampleDataFrame, dumParameter
    if parameter != dumParameter:
        sampleDataFrame = []
        for i in range(len(file_Names)):
            sampleDataFrame.append([])
        
        dumParameter = parameter
        pass
    
    batchData = dt[dt['fileNames']==value1]
    batchName = batchData['SampleID'].drop_duplicates().tolist()
    batchValidName = []
    for name in batchName:
        a = batchData[batchData['SampleID']==name]
        if parameter != 'VCD-Viab':
            if a[parameter].count()>2:
                batchValidName.append(name)
            
        else:
            if (a['VCD (Cells/mL)'].count()>2) & (a['Viability (%)'].count()>2):
                batchValidName.append(name)
            
    
    
    return dcc.Checklist(
            batchValidName,id = 'samples'
            ,labelStyle={'display': 'block'},
    style={"height":200, "width":200, "overflow":"auto"}
            )

    
@callback(
    Output('graph','figure'),
    Input('fileselector-dropdown','value'),
    Input('parameter-dropdown','value'),
    Input('samples','value')
    )

def update_figure(file,parameter,samples):
    
    
    
    
    n = file_Names.index(file)
    sampleList = []
    x_name = 'Run Time (days)';y_name = parameter
    batchData = dt[dt['fileNames']==file]
    
    
    
    fig = go.Figure()
    try:
        for sample in samples:
            if parameter != 'VCD-Viab':
                sampleData = batchData[batchData['SampleID']==sample].dropna(subset =(parameter,))
                if parameter =='Viability (%)':
                    sampleData = pd.concat([sampleData[x_name].astype(float),
                                            sampleData[y_name].str.rstrip('%').astype('float')],
                                           axis = 1)
                
                sampleData = pd.concat([sampleData[x_name].astype(float),
                                        sampleData[y_name].astype(float)],axis=1)
                sampleData = sampleData[sampleData[x_name]>=0.0]
                sampleList.append([sampleData,sample])
            else:
                sampleData = batchData[batchData['SampleID']==sample].dropna(subset =('VCD (Cells/mL)','Viability (%)'))
                sampleData = pd.concat([sampleData[x_name].astype(float),
                                        sampleData['VCD (Cells/mL)'].astype(float),
                                        sampleData['Viability (%)'].str.rstrip('%').astype('float')],
                                       axis = 1)
                sampleList.append([sampleData,sample])
                
    except:
        return fig
    sampleDataFrame[n] = sampleList
    


    
    try:
        if y_name == 'VCD-Viab':
            figs = make_subplots(specs=[[{"secondary_y": True}]])
            try:
                color = iter(cm.rainbow(np.linspace(0, 1, 20)))
                for file in sampleDataFrame:
                    
                    for sample in file:
                        c = next(color)
                        figs.add_trace(
                            go.Scatter(
                                x = sample[0].iloc[:,0].tolist(), 
                                y = sample[0].iloc[:,1].tolist(),
                                name=('{}_{}').format(file_Names[sampleDataFrame.index(file)],
                                                      sample[1]),
                                line = dict(color='rgb({},{},{})'.format(c[0],c[1],c[2]))
                                
                                ),
                            secondary_y=False
                            )
                        
                        figs.add_trace(
                            go.Scatter(
                                x = sample[0].iloc[:,0].tolist(), 
                                y = sample[0].iloc[:,2].tolist(),
                                name=('{}_{}').format(file_Names[sampleDataFrame.index(file)],
                                                      sample[1]),
                                line = dict(dash = 'dash',color='rgb({},{},{})'.format(c[0],c[1],c[2]))
                                ),
                            secondary_y=True
                            )
                figs.update_xaxes(title_text=x_name)
                figs.update_yaxes(title_text='VCD (Cells/mL)',secondary_y=False)
                figs.update_yaxes(title_text='Viability (%)',secondary_y = True,range = [50,100])
                return figs
            except:
                return figs
        
        for file in sampleDataFrame:
            for sample in file:
                fig.add_trace(
                    go.Scatter(
                        x = sample[0].iloc[:,0].tolist(), 
                        y = sample[0].iloc[:,1].tolist(),
                        name=('{}_{}').format(file_Names[sampleDataFrame.index(file)],
                                              sample[1]),                        mode="lines"
                        )
                    )
        fig.update_xaxes(title_text=x_name)
        fig.update_yaxes(title_text=y_name)
    except:
        return fig
    return fig



    
    
    