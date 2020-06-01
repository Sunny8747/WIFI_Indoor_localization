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
fname = 'walk2stand12' + '.csv'
fname = '%s/%s' % (dir_name, fname)
cfname = 'stand2' + '.csv'
cfname = '%s/%s' % (dir_name, cfname)

df = pd.read_csv(fname)
df.columns

df_modi = df[["AP Name", "Capabilities", "Heard By",  "RSSI", "SNR",  "epochTime"]]

#Capability convert
count_row, count_col = df_modi.shape
count_row -= 1
for i in range(0,count_row):
    temp = df_modi.loc[i, "Capabilities"]
    temp1 = temp.split('(')
    temp2 = temp1[1]
    temp3 = temp2.split('G')
    temp4 = temp3[0]
    df_modi.loc[i, "Capabilities"] = temp4
    
col = ["x", "y", "AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI", "Capabilities", "epochTime"]
off_finger = pd.DataFrame(columns = col)

copy_col = ["Capabilities", "epochTime"]

for j in range(0,count_row):
    off_finger.loc[j, "x"] = 0
    off_finger.loc[j, "y"] = 0
    
    ap1_name_b = df_modi.loc[j, "AP Name"].split('\'')
    ap1_name = ap1_name_b[1]
    
    rssi1 = df_modi.loc[j, "RSSI"].split('\'')
    rssi1 = rssi1[1]
    ap1_rssi = '%s:%s' % (ap1_name, rssi1)
    off_finger.loc[j, "AP1:RSSI"] = ap1_rssi
    heard_by_sp_b = df_modi.loc[j, "Heard By"].split('\'')
    heard_by_sp = heard_by_sp_b[1].split(',')                                                      
    
    ap2 = heard_by_sp[0]
    ap2_rssi = '%s:%s' % (ap2.split('(')[0], ap2.split('(' )[1][0:3])
    off_finger.loc[j, "AP2:RSSI"] = ap2_rssi
    ap3 = heard_by_sp[1]
    ap3_rssi = '%s:%s' % (ap3.split('(')[0], ap3.split('(' )[1][0:3])
    off_finger.loc[j, "AP3:RSSI"] = ap3_rssi
    ap4 = heard_by_sp[2]
    ap4_rssi = '%s:%s' % (ap4.split('(')[0], ap4.split('(' )[1][0:3])
    off_finger.loc[j, "AP4:RSSI"] = ap4_rssi
    for i in copy_col:    
        off_finger.loc[j, i] = df_modi.loc[j, i]

df2 = pd.read_csv(cfname)
df2.columns
df2_modi = df2[["x", "y","epochTime"]]
count_row2, count_col2 = df2_modi.shape
count_row2 -= 1

tempCount = 0
for i in range(0,count_row2):
    for j in range(tempCount,count_row):
        if(off_finger.loc[j, "epochTime"] > df2_modi.loc[i,"epochTime"]):
            tempx = df2_modi.loc[i,"x"]
            tempy = df2_modi.loc[i,"y"]
            off_finger.loc[j,"x"] = tempx
            off_finger.loc[j,"y"] = tempy
            break;
        else:
            tempCount += 1
            
off_finger.to_csv("v10/off_finger1_stand2.csv", mode='w' , index = False ,header = True)

    
    
