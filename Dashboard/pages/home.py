#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 15:06:46 2022

@author: danielzhu
"""

import dash
from dash import html, dcc

dash.register_page(__name__,path = '/')

layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),

])