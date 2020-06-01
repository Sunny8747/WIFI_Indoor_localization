# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 03:55:18 2019

@author: tjsdn2560
"""

import pandas as pd
import numpy as npy
import os
import sys
from PIL import Image
import PIL
import numpy
import copy
import networkx as nx
import matplotlib.pyplot as plt

dir_name = 'v30'
fname = 'streaming' + '.csv'
#fname = '%s/%s' % (dir_name, fname)

df = pd.read_csv(fname)
df.columns

ex = df[["Capabilities", "RSSI"]]
count_row, count_col = ex.shape
count_row -= 1
col = ["Capabilities", "RSSI"]
#Score_3 = pd.DataFrame(columns = col)
#Score_100 = pd.DataFrame(columns = col)
#count_3 = 0
#count_100 = 0


#for i in range(0,count_row):
#    if ex.loc[i, "ConnScore"] == 3:
#        Score_3.loc[count_3, "ConnScore"] = 3
#        rssi = ex.loc[i, "RSSI"]
#        Score_3.loc[count_3, "RSSI"] = rssi
#        count_3 +=1
#    if ex.loc[i, "ConnScore"] == 100:
#        Score_100.loc[count_100, "ConnScore"] = 100
#        rssi = ex.loc[i, "RSSI"]
#        Score_100.loc[count_100, "RSSI"] = rssi
#        count_100 +=1

#Score_3.to_csv("Score_3_not.csv", mode='a', index = False)
#Score_100.to_csv("Score_100_not.csv", mode='a', index = False)

#r_3, c = Score_3.shape
#r_100, c = Score_100.shape

#x = []
#y = []
#for i in range(0,count_row):
#    x.append(i)
#    y.append(ex.loc[i, "RSSI"])
#plt.scatter(x,y)
#plt.savefig('Score_all')

#x = []
#y = []
#for i in range(0,r_3):
#    x.append(i)
#    y.append(Score_3.loc[i, "RSSI"]) 
#plt.scatter(x,y)
#plt.savefig('Score_3')

x = []
y = []
for i in range(0, count_row):
    x.append(i)
    y.append(ex.loc[i, "RSSI"])
plt.scatter(x,y)
plt.savefig('scan')

        