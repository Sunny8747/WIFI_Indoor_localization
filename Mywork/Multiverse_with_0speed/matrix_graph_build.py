# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 23:41:09 2019

@author: tjsdn2560
"""

from PIL import Image
import pandas as pd
import PIL
import os
import sys
import numpy
import copy
import networkx as nx
import matplotlib.pyplot as plt


from scipy.misc import toimage
from scipy.misc import imsave

im = Image.open('Convert_Bf4.bmp')

imWidth,imHeight = im.size

imWidth -= 1 #0 to 750
imHeight -= 1 #0 to 299

imdata_temp = numpy.asarray(im)

node_list = [] #index for node node_list[[node_count, x, y], [node_count2, x, y], ````]
Path_Graph = nx.Graph()
count_node = 0
##image matrix imdata[imHeight][imWidth] = imdata[299][750]
imdata_arr = numpy.zeros((imHeight + 1, imWidth + 1))

def image_processing():
    for i in range(1,imHeight):
        for j in range(1,imWidth):
            if imdata_temp[i][j] == False:
                imdata_arr[i][j] = 0
            else:
                imdata_arr[i][j] = 1

    #toimage(imdata_arr).show()  #showing imdata as image imdata_temp is read only array and true false data

    ##making Grid
    grid_arr = numpy.zeros((imHeight + 1, imWidth + 1))
    grid_arr = copy.copy(imdata_arr)
    for i in range(1, imHeight):
        for j in range(1,imWidth):
            if((imdata_arr[i][j] == 1) and (i%10 == 0) and (j%10 == 0)):
                grid_arr[i][j] = 0

    #toimage(grid_arr).show()  #showing grid as image

    node_arr = numpy.zeros((imHeight + 1, imWidth + 1))
    

    ##making node_arr and adding all node to graph


    for i in range(1,imHeight):
        for j in range(1,imWidth):
            if imdata_arr[i][j] != grid_arr[i][j]: #there is node not same -> gird black part
                node_arr[i][j] = 1
                count_node += 1
                Path_Graph.add_node(count_node, pos=(j,i)) #i,j = y,x pos = (x,y)
                node_list_elem = [count_node, j, i]
                node_list.append(node_list_elem)

    #toimage(node_arr).show()
    #howto connecting blocking nodes?

    ##connecting all node accept blocking

    #connecting with x coordinate
    temp_flag = 1
    for k in range(0, count_node - 2): #o ~ count-1 = 1 ~ count last node is already connect
        if node_list[k][2] == node_list[k+1][2]: #same y coordinate
            if node_list[k+1][1] != (node_list[k][1] + 10): #next node is jump 10 x coordinate need to check k_x + 10 != k+1_x            
                continue
            for i in range(1,10):
                if imdata_arr[node_list[k][2]][node_list[k][1] + i] == 0:
                    temp_flag = 0 #no edge with k and k+1 node
                    break #if no don't need to keep loop
            if temp_flag == 1: #no wall between to node
                Path_Graph.add_edge(node_list[k][0], node_list[k+1][0], weight = 1.013)
            temp_flag = 1 #reset flag

    #conncting with y coordinate
    temp_flag = 1
    for k in range(0, count_node - 2): #o ~ count-1 = 1 ~ count last node is already connect
        if node_list[k][2] == 290: #don't need to calculate last line
            break
        for n in range(k + 1, count_node -1): #if k, then n = k so pointing same node So, k+1
            if node_list[k][1] == node_list[n][1]: #node k and n same x coordinate
                #find same x coordinate
                if (node_list[k][2] + 10) != node_list[n][2]: #k's y+10 = n's y -> aj node with y direction
                    continue
                for i in range(1,10): #check wall
                    if imdata_arr[node_list[k][2] + i][node_list[k][1]] == 0: #there is wall
                        temp_flag = 0 #set flag false
                        break #if no don't needto keep loop
                if temp_flag == 1: #no wall
                    Path_Graph.add_edge(node_list[k][0], node_list[n][0], weight = 1.02) #y direction edge adding
                    break
                temp_flag = 1 #reset


    #connecting with cross?
    #cross weight = 1.438
    temp_flag = 1
    for k in range(0,count_node - 2):
        if node_list[k][2] == 290:
            break
        for n in range(k + 1, count_node - 1):
            if ((node_list[k][1] + 10) == node_list[n][1]) and ((node_list[k][2] + 10) == node_list[n][2]): #find righ donw cross
                for i in range(1,10):
                    for j in range(1,10):
                        if imdata_arr[node_list[k][2] + i][node_list[k][1] + j] == 0: #wall cross check
                            temp_flag = 0
                            break
                if temp_flag == 1:
                    Path_Graph.add_edge(node_list[k][0], node_list[n][0], weight = 1.438)
                    break
            temp_flag = 1

    temp_flag = 1
    for k in range(0,count_node - 2):
        if node_list[k][2] == 290:
            break
        for n in range(k + 1, count_node - 1):
            if ((node_list[k][1] - 10) == node_list[n][1]) and ((node_list[k][2] + 10) == node_list[n][2]): #find righ donw cross
                for i in range(1,10):
                    for j in range(1,10):
                        if imdata_arr[node_list[k][2] + i][node_list[k][1] - j] == 0: #wall cross check
                            temp_flag = 0
                            break
                if temp_flag == 1:
                    Path_Graph.add_edge(node_list[k][0], node_list[n][0], weight = 1.438)
                    break
            temp_flag = 1
                
#connecting all edge with weight finish

#finding position with path data
def node_finder(x,y):
    for i in range(0,count_node - 1):
        [temp_node_num, tempx, tempy] = node_list[i]
        if(x == tempx and (300 - y) == tempy): # image grid is fliped so have to put 300 - realY
            node_num = temp_node_num
            return node_num

#if adding new data then need to adding at off_finger2 not this step 
def making_last_finger():
    dir_name = 'v10'
    fname = 'off_finger2' + '.csv'
    fname = '%s/%s' % (dir_name, fname)
    df = pd.read_csv(fname)
    df.columns
    col = ["-56"]
    ind = ["Eng2_04F-05"]
    last_finger = pd.DataFrame(columns = col, index = ind)
    
    count_row, count_col = df.shape
    count_row -= 1
    ap_list = ["AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI"]
    for i in range(0,count_row):
        tempx = df.loc[i,"x"]
        tempy = df.loc[i,"y"]
        #node_num = node_finder(tempx, tempy)
        for j in ap_list:
            Adata = df.loc[i,j]
            ap_name = Adata.split(':')[0]
            temp_rssi = Adata.split(':')[1]
            last_finger.loc[ap_name, temp_rssi] = ""
            
    for i in range(0,count_row):
       tempx = df.loc[i,"x"]
       tempy = df.loc[i,"y"]
       node_num = node_finder(tempx, tempy)
       if node_num == 0:
           continue
       for j in ap_list:
            Adata = df.loc[i,j]
            ap_name = Adata.split(':')[0]
            temp_rssi = Adata.split(':')[1]
            last_finger.loc[ap_name, temp_rssi] += ",%s" % node_num           
    last_finger.to_csv("v10/off_finger3.csv", mode='w' , index = True ,header = True)
    
#prob_node_list = [] #probable node list
# finding probable location (next node)
def probable_location(ap_name, rssi_value, offset):
    if int(rssi_value) < -86:
        return []
    dir_name = 'v10'
    fname = 'off_finger3' + '.csv'
    fname = '%s/%s' % (dir_name, fname)
    df = pd.read_csv(fname)
    df.set_index('Unnamed: 0', inplace = True)
    prob_node_list = [] #probable node list
    checkbit = 0
    for i in df.index:
        if ap_name == i:
            checkbit = 1
            break
    if checkbit == 0:
        return False
    for i in range(-offset, offset + 1):    
        if df.loc[ap_name,'%s' % (int(rssi_value) + i)] != 'nan' and df.loc[ap_name,'%s' % (int(rssi_value) + i)] != '':
            split_data = str(df.loc[ap_name,'%s' % (int(rssi_value) + i)]).split(',')
            for j in split_data:
                if( j == 'nan' or j == ''):
                    continue
                checkbit = 1
                for k in prob_node_list:
                    if(int(j) == k):
                        checkbit = 0
                if checkbit == 1:
                    prob_node_list.append(int(j))
                for (origin, ajcent) in Path_Graph.edges(int(j)):
                    checkbit = 1
                    #print(origin, ajcent)
                    for k in prob_node_list:
                        if(int(ajcent) == k):
                            checkbit = 0
                            break
                    if checkbit == 1:
                        prob_node_list.append(int(ajcent))
    return prob_node_list
                        
path_list = []
#building path tree
def path_tree_constructor():
    dir_name = 'v10'
    fname = 'walk2' + '.csv'
    fname = '%s/%s' % (dir_name, fname)
    fname2 = 'off_finger1_walk2' + '.csv'
    fname2 = '%s/%s' % (dir_name, fname2)
    df = pd.read_csv(fname)
    count_row, count_col = df.shape
    count_row -= 1
    col = ["x","y"]
    path_divide = pd.DataFrame(columns = col)
    path_col_count = 0
    for i in range(0,count_row-1):
        time_diff = int(df.loc[i + 1,"epochTime"]) - int(df.loc[i,"epochTime"])
        x_diff = df.loc[i+1, "x"] - df.loc[i, "x"]
        y_diff = df.loc[i+1, "y"] - df.loc[i, "y"]
        for j in range(0,time_diff):
            path_divide.loc[path_col_count + j, "x"] = round((df.loc[i, "x"] + j*x_diff)/10 * 0.32511)*10
            path_divide.loc[path_col_count + j, "y"] = round((df.loc[i, "y"] + j*y_diff)/10 * 0.32538)*10
        path_col_count = path_col_count + time_diff
    path_divide.loc[path_col_count, "x"] = round(df.loc[count_row - 1, "x"]/10 * 0.32511)*10
    path_divide.loc[path_col_count, "y"] = round(df.loc[count_row - 1, "y"]/10 * 0.32538)*10
    #path_divide.to_csv("v10/divided_path.csv", mode='w' , index = False ,header = True)
    
    df2 = pd.read_csv(fname2)
    count_row2, count_col2 = df2.shape
    count_row2 -= 1
    startx = path_divide.loc[0,"x"]
    starty = path_divide.loc[0,"y"]
    start_node = node_finder(startx, starty)
    endx = path_divide.loc[path_col_count,"x"]
    endy = path_divide.loc[path_col_count,"y"]
    end_node = node_finder(endx, endy)
    start_time = df2.loc[0, "epochTime"]
    old_time = start_time
    temp_path = [start_node] #level_count == 0
    global path_list
    path_list.append(temp_path)
    level_count = 1
    for i in range(2,path_col_count + 2): #0 is start_node server data period is 2 So, start with 2 Also, last count is end_time
        new_path_list = []
        time_diff = 2#df2.loc[level_count, "epochTime"] - old_time
        #print(time_diff)
        old_time = df2.loc[level_count, "epochTime"]
        if i == df2.loc[level_count, "epochTime"] - start_time:
            probable_node_list = []
            for j in ["AP1:RSSI", "AP2:RSSI", "AP3:RSSI", "AP4:RSSI"]:#ap1 to 4 get probable_node_list
                temp_ap_name = df2.loc[level_count, j].split(":")[0] #ap name
                temp_ap_rssi = df2.loc[level_count, j].split(":")[1] #rssi
                temp_list2 = probable_location(temp_ap_name, temp_ap_rssi, 0)
                if temp_list2 != []:
                    if probable_node_list == []:
                        probable_node_list += temp_list2
                    else :
                        new_temp_list = []
                        for i in temp_list2:
                            for j in probable_node_list:
                                if i == j:
                                    new_temp_list.append(i)
                                    break
                        probable_node_list = new_temp_list
                #probable_node_list += probable_location(temp_ap_name, temp_ap_rssi, 0)
            
            for m in path_list:# all path list
                temp_list = m
                previous_node = m[level_count - 1]
                for k in probable_node_list:
                    path_length = nx.shortest_path_length(Path_Graph, previous_node, k, 'weight')
                    if path_length == 0 or (path_length >= (1*time_diff) and path_length <= (2.6*time_diff)):
                        temp_new_list = temp_list + [k]
                        checkbit = 1
                        for already in new_path_list:
                            if temp_new_list[level_count] == already[level_count]:#prevent double entering 
                                checkbit = 0
                                break;
                        if checkbit == 1:
                            #new_path_list.append(temp_new_list)
                            if len(temp_list) >= 2:
                                if temp_list[level_count - 2] != k or (temp_list[level_count - 2] == k and temp_list[level_count - 1] == k):
                                    new_path_list.append(temp_new_list)#prevent a-b-a case
                            else:
                                if len(temp_list) >= 3:
                                    if temp_list[level_count - 1] != k and temp_list[level_count - 2] == temp_list[level_count - 1] and temp_list[level_count - 2] != temp_list[level_count - 3]:
                                        continue
                                    else:
                                        new_path_list.append(temp_new_list)
                                else :
                                    new_path_list.append(temp_new_list)
            level_count += 1
            path_list = new_path_list
        print(len(path_list))
    #last_path_list = []
    min_node_length = 100
    last_path_with_min = []
    first_check = 1
    min_deviation = 0
    for i in path_list:     #Mean check of each path        
        mean_count = 0
        node_length = 0
        deviation = 0
        for j in range(0,len(i) - 1):   #Mean check of each path        
            if i[j] != i[j+1]:
                node_length += nx.shortest_path_length(Path_Graph, i[j], i[j + 1] , 'weight')
                mean_count += 1
        path_mean = node_length/mean_count
        for j in range(0, len(i) - 1):  #standard deviation check of each path        
            if i[j] != i[j+1]:
                node_length += nx.shortest_path_length(Path_Graph, i[j], i[j + 1] , 'weight')
                deviation += pow((node_length - path_mean),2)
        if first_check == 1:
            last_path_with_min = i
            min_deviation = deviation
        else:
            if min_deviation >= deviation:
                min_deviation = deviation
                last_path_with_min = i
    return last_path_with_min
    #return path_list       

#checking each node's weighted distance for discard impossible speed
def point_diff_check(temp_path_list):
    dir_name = 'v10/'
    fname = 'off_finger2_walk2' + '.csv'
    fname = '%s/%s' % (dir_name, fname)
    df = pd.read_csv(fname)
    count_row, count_col = df.shape
    count_row -= 1
    count = 0
    path_diff_list = []
    for i in temp_path_list:
        real_point = node_finder(df.loc[count, "x"],df.loc[count, "y"])
        path_diff = nx.shortest_path_length(Path_Graph, real_point, i, 'weight')
        path_diff_list.append(path_diff)
        count += 1
        print(path_diff)
        
    return path_diff_list
        
compare_path_list = [1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 1168,
 917,
 677,
 677,
 677,
 677,
 682,
 687,
 692,
 621,
 822,
 822,
 621,
 821,
 1077,
 1184,
 1179,
 1179,
 1184,
 1180,
 1175,
 1170,
 1165,
 1160,
 1155,
 1150,
 1096]


last_path_list = path_tree_constructor()
result = point_diff_check(last_path_list)
#print(result)

  
#making_last_finger()

# temp_list  = []
# temp_list2 = probable_location('Eng2_04F-04','-71',0)
# if temp_list2 != []:
#     if temp_list == []:
#         temp_list += temp_list2
#     else :
#         new_temp_list = []
#         for i in temp_list2:
#             for j in temp_list:
#                 if i == j:
#                     new_temp_list.append(i)
#                     break
#         temp_list = new_temp_list
# temp_list2 = probable_location('Eng2_02F_A03','-77',0)
# if temp_list2 != []:
#     if temp_list == []:
#         temp_list += temp_list2
#     else :
#         new_temp_list = []
#         for i in temp_list2:
#             for j in temp_list:
#                 if i == j:
#                     new_temp_list.append(i)
#                     break
#         temp_list = new_temp_list
# temp_list2 = probable_location('Eng2_03F-08','-85',0)
# if temp_list2 != []:
#     if temp_list == []:
#         temp_list += temp_list2
#     else :
#         new_temp_list = []
#         for i in temp_list2:
#             for j in temp_list:
#                 if i == j:
#                     new_temp_list.append(i)
#                     break
#         temp_list = new_temp_list
# temp_list2 = probable_location('Eng2_06F-06','-71',0)
# if temp_list2 != []:
#     if temp_list == []:
#         temp_list += temp_list2
#     else :
#         new_temp_list = []
#         for i in temp_list2:
#             for j in temp_list:
#                 if i == j:
#                     new_temp_list.append(i)
#                     break
#         temp_list = new_temp_list
# temp_list = []        
# temp_list = new_temp_list               
# temp_list += probable_location('Eng2_04F-04','-71',0)
# temp_list += probable_location('Eng2_02F_A03','-77',0)
# temp_list += probable_location('Eng2_03F-08','-85',0)
# temp_list += probable_location('Eng2_06F-06','-71',0)
#Eng2_04F-04:-71	Eng2_02F_A03:-77	Eng2_03F-08:-85	Eng2_06F-06:-71

#b'Eng2_02F_A03(-77 dBm),Eng2_02F_A04(-77 dBm),Eng2_03F-05(-65 dBm)'

#ng2_02F_A03(-84 dBm),Eng2_02F_A04(-70 dBm),Eng2_01F_A01(-73 dBm)'
#path_list = []
#temp_list = nx.dijkstra_path(Path_Graph, 1, 500, 'weight')
#path_list += temp_list
#temp_list = nx.dijkstra_path(Path_Graph, 500, 1239, 'weight')
#path_list += temp_list
#temp_list = nx.dijkstra_path(Path_Graph, 1239, 500, 'weight')
#path_list += temp_list
#temp_list = nx.dijkstra_path(Path_Graph, 500, 7, 'weight')
#path_list += temp_list
        
#making_last_finger()



# image_count = 0
# test_image = numpy.zeros((imHeight + 1, imWidth + 1))
# test_image = copy.copy(imdata_arr)
# for i in path_list:
#     for j in i:
#         path_x = node_list[j - 1][1] #node index x
#         path_y = node_list[j - 1][2] #node index y
#         test_image[path_y - 1][path_x - 1] = 0
#     toimage(test_image).save('image/'+str(image_count)+'stand2.png')
#     image_count += 1
    
image_count = 0
test_image = numpy.zeros((imHeight + 1, imWidth + 1))
test_image = copy.copy(imdata_arr)
for j in last_path_list:
    path_x = node_list[j - 1][1] #node index x
    path_y = node_list[j - 1][2] #node index y
    test_image[path_y - 1][path_x - 1] = 0
toimage(test_image).save('image/'+str(image_count)+'devi.png')
image_count += 1
#

    
#pos = nx.get_node_attributes(Path_Graph,'pos')
#nx.draw(Path_Graph, pos, node_size=1, with_labels=False)
#plt.savefig("Edge")
        
        
