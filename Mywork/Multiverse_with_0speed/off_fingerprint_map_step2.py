# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 17:33:50 2019

@author: tjsdn2560
"""

import pandas as pd
import numpy as npy
import os
import sys

dir_name = 'v10'
fname = 'off_finger1_stand2' + '.csv'
fname = '%s/%s' % (dir_name, fname)

df = pd.read_csv(fname)
df.columns

df_modi = df[["x", "y", "AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI", "Capabilities", "epochTime"]]

count_row, count_col = df_modi.shape
count_row -= 1
    
col = ["x", "y", "AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI", "Capabilities", "epochTime"]
off_finger2 = pd.DataFrame(columns = col)

copy_col = ["x","y","AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI", "Capabilities", "epochTime"]

tempCount = 0
tempx = 0
tempy = 0
position = []
for i in range(0,count_row + 1):
    if(df_modi.loc[i,"x"] != 0):
        tempx = df_modi.loc[i,"x"]
        tempy = df_modi.loc[i,"y"]
        position.append([i,tempx,tempy])
    for j in copy_col:    
        off_finger2.loc[i, j] = df_modi.loc[i, j]    
        
for i in range(0,len(position) - 1):
    if(position[i][1] == position[i+1][1]):#x is same with next
        if(position[i + 1][0] - position[i][0] - 1) == 0:
            continue
        frag = (position[i+1][2] - position[i][2])/(position[i + 1][0] - position[i][0])
        for j in range(1, (position[i + 1][0]-position[i][0])):
            off_finger2.loc[(position[i][0] + j),"x"] = position[i][1]
            off_finger2.loc[(position[i][0] + j),"y"] = position[i][2] + (frag*j)
    elif(position[i][2] == position[i+1][2]):#y is same with next
        if(position[i + 1][0] - position[i][0] - 1) == 0:
            continue
        frag = (position[i+1][1] - position[i][1])/(position[i + 1][0] - position[i][0])
        for j in range(1, (position[i + 1][0]-position[i][0])):
            off_finger2.loc[(position[i][0] + j),"x"] = position[i][1] + (frag*j)
            off_finger2.loc[(position[i][0] + j),"y"] = position[i][2]       
            
for i in range(0,count_row + 1):
    off_finger2.loc[i,"x"] = round(off_finger2.loc[i,"x"]/10 * 0.32511)*10
    off_finger2.loc[i,"y"] = round(off_finger2.loc[i,"y"]/10 * 0.32538)*10
    
off_finger2.to_csv("v10/"+"off_finger2_stand2.csv", mode='w' , index = False ,header = True)

    
    
