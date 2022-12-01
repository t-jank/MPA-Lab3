# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:26:05 2022

@author: t-jan
"""
import random
import matplotlib.pyplot as plt

n = 100

Points=[]

for i in range(0,n):
    x = random.random()*n
    y = random.random()*n
    Points.append([x,y])

for i in range(0,len(Points)):
    plt.scatter(Points[i][0],Points[i][1],color='k')
    
plt.axis('square')
plt.xlim([0,n])
plt.ylim(0,n)
plt.show()
