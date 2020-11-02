#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 16:36:17 2020

@author: Moe
"""


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')

#%config InlineBackend.figure_format = ‘retina’
#%matplotlib inline



df.head()

df1 = df.iloc[:,2:].values
t = df.iloc[:,2]
w = df.iloc[:,3]
x = df.iloc[:,4]
y = df.iloc[:,5]
z = df.iloc[:,6]

plt.plot(t[0:61325],w[0:61325],x[0:61325],y[0:61325],z[0:61325])
plt.show();
df.isnull().sum()

def graph(df, r, date):

    df2= df.drop('epoc (ms)', axis=1)
    df3= df2.drop('timestamp (+0300)', axis=1)
    
    
    # Initialize the figure
    plt.style.use('seaborn-darkgrid')
     
    # create a color palette
    palette = plt.get_cmap('Set1')
     
    # multiple line plot
    num=0
    for column in df3.drop('elapsed (s)', axis=1):
        num+=1
     
        # Find the right spot on the plot
        plt.subplot(2,2, num)
     
        # plot every groups, but discreet
        for v in df3.drop('elapsed (s)', axis=1):
            plt.plot(df3['elapsed (s)'], df3[v], marker='', color='grey', linewidth=0.6, alpha=0.3)
     
        # Plot the lineplot
        plt.plot(df3['elapsed (s)'], df3[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
     
        # Same limits for everybody!
        plt.xlim(0,r)
        plt.ylim(-2,2)
     
        # Not ticks everywhere
        if num in range(7) :
            plt.tick_params(labelbottom='off')
        if num not in [1,4,7] :
            plt.tick_params(labelleft='off')
     
        # Add title
        plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num) )
        
    
     
    # general title
    plt.suptitle("QUATERNION DATA "+str(date), fontsize=13, fontweight=0, color='black', style='italic', y=1.02)
     
    # Axis title
    plt.text((r+150), -1.9, 'Time', ha='center', va='center')
    plt.text(100, 1.5, 'Angle', ha='center', va='center', rotation='vertical')
 
    
    
    
    
    
    
    
tf0 = "june13.csv"
dtf0 = pd.read_csv(tf0)
graph(dtf0,500,13)

tf1 = "june14.csv"
dtf1 = pd.read_csv(tf1)
graph(dtf1,2000,14)


tf2 = "june19.csv"
dtf2 = pd.read_csv(tf2)
graph(dtf2,1400,19)

test_file = 'MMRtest.csv'
df = pd.read_csv(test_file)
graph(df,2100,22)

tf3 = "june23.csv"
dtf3 = pd.read_csv(tf3)
graph(dtf3,1500, 23)




