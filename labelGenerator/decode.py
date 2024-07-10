#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 13:35:38 2022

@author: danielzhu
"""

def decode(rawData):
    rows = rawData.split(':')
    result = [rows[0]]
    diction = list(rows[0])
    for row in range(len(rows)-1):
        columns = rows[row+1].split(';')
        columns = columns[1:]
        for column in columns:
            
            [idx,num] = column.split(',')
            diction[int(idx)]=num
        result.append(''.join(diction))
            
    return(result)
    
    
    
''' 
text = '5137-0001L-B01-D00:;17,1:;17,2:;17,3:;17,4:;17,5:;17,6:;17,7:;17,8:;17,9:;16,1;17,0:;17,1:;17,2:;17,3:;17,4'
answer = decode(text)
print(answer)
'''
