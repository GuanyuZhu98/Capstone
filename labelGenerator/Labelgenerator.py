#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 16:46:44 2022

@author: danielzhu
"""

# Note: pandas tkinter qrcode and barcode library might need importing

## Terminal operations
## pip install qrcode
## pip install python-barcode

import qrcode,barcode,re,os
import pandas as pd
import numpy as np
import tkinter as tk

class Generator:
    def __init__(self):
        return
    
    ## A Simple compress algorithm
    def compress(self,data):
        diction = list(data[0])
        log=[]
        log.append(data[0])
        for i in range(len(data)-1):
            comp = list(data[i+1])
            dum = [';{},{}'.format(j,comp[j]) for j in range(len(comp)) if comp[j]!=diction[j]]
            log.append(''.join(dum))
        return(':'.join(log))
            
    
    ## Sample Name: Vial Label + BioReactor Name + Day (Need to be specific)
    def GUI(self):
        window = tk.Tk()
        window.title('label Generator');window.geometry('450x350')
        
        ## Input textbox for Vial Label
        label1 = tk.Label(window,height = 1, text = 'Vial Label:').place(x = 10,y = 10)
        
        vialLabel = tk.Text(window,height = 1,width = 8)
        vialLabel.place(x = 80,y = 10)
        ##
        
        ## Input textbox for BioReactor Name
        label2 = tk.Label(window,height = 1, text = 'Bioreactor Name:').place(x = 10,y = 40)
        bioReactor = tk.Text(window,height=1,width = 10)
        bioReactor.place(x = 120,y = 40)
        ##
        
        ## Day selector
        daySelector = tk.Listbox(window,selectmode = 'multiple',height = 7,width = 5)
        daySelector.place(x=10,y=110)
        for i in range(31):
            daySelector.insert(i,'D{}'.format(i))
        ##
        
        ## Check box
        label3 = tk.Label(window,height = 2, text = 'Please check the name of sample below \n before generate a label'
                          ).place(x = 160,y = 70)
        
        checkBox = tk.Listbox(window,selectmode='multiple',height = 7,width = 30)
        checkBox.place(x = 160,y=110)
        ##
        
        ## Function for Buttons
        def add():
            
            ## Validation Function (Regular Expression)
            def valid():
                pass
            
            items = daySelector.curselection()
            for item in range(len(items)):
                text = '{}-{}-D{:02d}'.format(vialLabel.get("1.0",'end-1c'),bioReactor.get("1.0",'end-1c'),items[item])
                if not text in checkBox.get(0, "end"):
                    checkBox.insert(item,text)
                
        def remove():
            items = checkBox.curselection()
            for item in items[::-1]:
                checkBox.delete(item)
                
        ##
        
        ## Buttons
        addLabel = tk.Button(window,text = 'add',command = add,width = 5).place(x=70,y=130)
        deleteLabel = tk.Button(window,text = 'remove', command = remove, width = 5).place(x=70,y=170)
        ##
        
        ## QRcode or Barcode generator
        
            ##QRcode Function
        def QRcode():
            label = list(checkBox.get(0,'end'))
            code = self.compress(label)
            img = qrcode.make(code)
            sample_name = '{}_{}'.format(vialLabel.get("1.0",'end-1c'),bioReactor.get("1.0",'end-1c'))
            img.save("{0}QRcode.png".format(sample_name))
            
            ## Notice
            notice()
            
            ##QRcode Button
        qr_code = tk.Button(window,command=QRcode,text='QRcode',width =10).place(x=80,y=290)
            
            ##Barcode Function
        def Barcode():
            label = list(checkBox.get(0,'end'))
            code = label[0]
            img = barcode.get('code39',code)
            sample_name = '{}_{}'.format(vialLabel.get("1.0",'end-1c'),bioReactor.get("1.0",'end-1c'))
            img.save("{0}Barcode".format(sample_name))
            ## Notice
            notice()
            

        def notice():
            path = os.getcwd()

            dum = tk.Label(window,text='Label have been successfully generated on path\n {}'.format(path),height=2).place(x=70,y=250)
            
            ##Barcode Button
        bar_code = tk.Button(window,command=Barcode,text='Barcode',width=10).place(x=250,y=290)
            
        
        ##
        
        tk.mainloop()
        
a = Generator()
a.GUI()




