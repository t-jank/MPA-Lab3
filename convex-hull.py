# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:26:05 2022

@author: t-jan
"""
import random
import matplotlib.pyplot as plt
import math


n = 100

Points=[]

plane = 'c' # square or circle

if plane=='s' or plane=='square':
    for i in range(0,n):
        x = random.random()*n
        y = random.random()*n
        Points.append([x,y])
        
elif plane=='c' or plane=='circle':
    while(len(Points) < n):
        x = random.random()*n
        y = random.random()*n
        ray = n/2
        distance_from_centre = math.sqrt( (n/2-x)**2 + (n/2-y)**2 )
        if distance_from_centre <= ray:
            Points.append([x,y])

for i in range(0,len(Points)):
    plt.scatter(Points[i][0],Points[i][1],color='k')
    
plt.axis('square')
plt.xlim([0,n])
plt.ylim(0,n)
plt.show()
