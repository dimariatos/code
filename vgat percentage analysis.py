# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 17:30:11 2021

@author: andre
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter


# =============================================================================
# def percentages(filename):
#     
#     
#     ''' filename: the output file of the cell counter plug in of image j that contains smpling data from different regions (on and off) 
#     
#     
#     returns a list of objects [all the data for vgat cells,all the data for vglut cells, the percentage of vgatcells in the area, the percentage of vglut cells in the area
#                                ,the number of vgat cells in the area,the number of vglut cells in the area ]
#     '''
#     on_ipsi_6599= pd.read_csv(filename)
#     allvgat= on_ipsi_6599.loc[on_ipsi_6599['Type'] == 1]
#     allvglut=on_ipsi_6599.loc[on_ipsi_6599['Type'] == 2]
#     numvgat=len(allvgat)
#     numvglut=len(allvglut)
#     vgat_percentage= len(allvgat)/len (on_ipsi_6599['Type'])
#     vglut_percentage=len(allvglut)/len (on_ipsi_6599['Type'])
#     return[allvgat,allvglut,vgat_percentage,vglut_percentage,numvgat,numvglut]
# 
# 
# on_ipsi_6599=percentages('C:/Users/andre/OneDrive/Desktop/whole retina/6599/area of diference implant/6599 Results 1_POS 2_NEG.csv')
# off_ipsi_6599_medial=percentages('C:/Users/andre/OneDrive/Desktop/whole retina/6599/medial/Results ipsi medial pos neg.csv')
# off_ipsi_6599_lateral=percentages('C:/Users/andre/OneDrive/Desktop/whole retina/6599/latteral/latteral ipsi.csv')
# offGatpercentage_ipsi_6599= abs(off_ipsi_6599_medial[2]+off_ipsi_6599_lateral[2])/2
# offGlutpercentage_ipsi_6599=1-offGatpercentage_ipsi_6599
# onGatpercentage_ipsi_6599=on_ipsi_6599[2]
# =============================================================================


bins=np.linspace(-2000,2000,50)

pointzero=[0,0,0]

point6599ipsi=[2000,-600,32]
point6599contra=[1358,-564,24]

point6601ipsi=[1200,-300,0]
point6601contra=[1700,-400,0]

point6287ipsi=[1500,-430,0]
point6287contra=[1500,-500,0]

point9323ipsi=[1600,-600,0]
point9323contra=[1200,-600,0]



ipsi6599='C:/Users/andre/OneDrive/Desktop/whole retina/6599/6599 statistics for ipsi threshold6.csv'
contra6599='C:/Users/andre/OneDrive/Desktop/whole retina/6599/Statistics for contra .csv'
ipsi6601='C:/Users/andre/OneDrive/Desktop/whole retina/6601/Statistics for ipsi.csv'
contra6601='C:/Users/andre/OneDrive/Desktop/whole retina/6601/Statistics for contra.csv'
ipsi6287='C:/Users/andre/OneDrive/Desktop/whole retina/6287/statistics for ipsi.csv'
contra6287='C:/Users/andre/OneDrive/Desktop/whole retina/6287/Statistics for contra.csv'
ipsi9323='C:/Users/andre/OneDrive/Desktop/whole retina/9323/Statistics for ipsi.csv'
contra9323='C:/Users/andre/OneDrive/Desktop/whole retina/9323/Statistics for contra.csv'







def distance_finder(point,filename):
    '''
    

    Parameters
    ----------
    point : TYPE list or tuple with three numbers  [x,y,z]
        DESCRIPTION. the xyz coordinates of the point from which we want to find the spatial distribution of cells
    filename : TYPE csv file output of the 3d object counter plug in of image j. contains all the cells identified by the algorythm in rows and several attributes of them
    among which the x y z coordinates 
        DESCRIPTION.

    Returns
    -------
    data : TYPE dataframe
        data has all the initial information plus the distances in all axis and in space .

    '''
    #point =[1170.48,311.96,0]
    data=pd.read_csv(filename)
    data['Y']=-data['Y']
    data['X']=data['X']
    distance_x=data['X']-point[0]
    distance_y=data['Y']-point[1]
    distance_z=data['Z']-point[2]
    distance_2d=np.sqrt((distance_x**2)+(distance_y**2))
   
    distance_3d=np.sqrt((distance_x**2)+(distance_y**2)+(distance_z**2))
    data['distance_x']= distance_x
    data['distance_y']=distance_y
    data['distance_z']=distance_z
    data['distance_3d']=distance_3d
    data['distance_2d']=distance_2d
    data.loc[data.distance_x<0,'distance_2d']=-distance_2d
    
    return data


test6599ipsi=distance_finder(point6599ipsi,ipsi6599)
test6599contra=distance_finder(point6599contra,contra6599)

test6287ipsi=distance_finder(point6287ipsi,ipsi6287)
test6287contra=distance_finder(point6287contra,contra6287)
test6287ipsi_superactive=test6287ipsi.loc[test6287ipsi['Mean']>15]
test6287contra_superactive=test6287contra.loc[test6287contra['Mean']>15]
test9323contra=distance_finder(point9323contra,contra9323)
test9323ipsi=distance_finder(point9323ipsi,ipsi9323)
test9323ipsi_superactive=test9323ipsi.loc[test9323ipsi['Mean']>4]#test9323contra['Mean'].mean()]
test9323contra_superactive=test9323contra.loc[test9323contra['Mean']>4]#test9323contra['Mean'].mean()]

test6601ipsi=distance_finder(point6601ipsi,ipsi6601)
test6601contra=distance_finder(point6601contra,contra6601)

ipsi_list=[test6599ipsi,test6287ipsi_superactive,test9323ipsi_superactive,test6601ipsi]
contra_list=[test6599contra,test6287contra_superactive,test9323contra_superactive,test6601contra]

def el_plotador(ipsi,contra):
   # sns.distplot(ipsi['distance_x'],bins=bins,norm_hist=True)
    #sns.distplot(contra['distance_x'],bins=bins,norm_hist=True)
    #sns.kdeplot(ipsi['distance_x'])
    #sns.kdeplot(ipsi['distance_x'],)
    #sns.kdeplot(ipsi,contra)
    plt.hist(ipsi['distance_2d'],color='b',label='ipsi',bins=15)
    plt.hist(-contra['distance_2d'],color='r',label='contra',alpha=0.5,stacked=True,bins=15)
    plt.legend(loc='upper right')
    plt.show()
    
    
    plt.scatter((-ipsi['X']+2700),ipsi['Y'],color='b')
    plt.scatter(contra['X'],contra['Y'],color='r')
    plt.grid()
    plt.show()

def allploter(ipsi_list,contra_list):

    for i,c in zip(ipsi_list, contra_list):
        el_plotador(i,c)

    
    
    
    
    
    
    
    
    
    
    
    

