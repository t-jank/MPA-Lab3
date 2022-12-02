# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:26:05 2022

@author: t-jan
"""
import random
import matplotlib.pyplot as plt
import math

def length(A,B):
    return math.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )


def angle(A,B,C):
    if B==C: return -1
    AB=length(A,B)
    BC=length(B,C)
    AC=length(A,C)
    return math.acos( (AB**2 + BC**2 - AC**2) / (2*AB*BC) )


def update_angles(hull,points,angles):
    hull_size=len(hull)
    for i in range(0,len(points)):
        angles[i]=angle(hull[hull_size-2], hull[hull_size-1], points[i])


def Jarvis_march(points):
    hull=[]
    hull.append([0,0])
    hull.append([0,9999])
    for i in range(0,len(points)): # finding first point of hull, the smallest y
        if points[i][1]<hull[1][1]:
            hull[1] = points[i]
    hull[0]=([-9999,hull[1][1]]) # point zero [-inf, y(P1)]
    
    angles=[]
    for i in range(0,len(points)):
        angles.append([0])
    update_angles(hull,points,angles)
    N=([-1,-1])
    while(True):
        N=points[0]
        angle=-1
        for i in range(0,len(points)):
            if angles[i]>angle:
                angle=angles[i]
                N=points[i]    
        if N==hull[1]:
            break
        hull.append(N)
        update_angles(hull,points,angles)

    hull_x=[]
    hull_y=[]
    for i in range(1,len(hull)):
        hull_x.append(hull[i][0])
        hull_y.append(hull[i][1])
    hull_x.append(hull_x[0])
    hull_y.append(hull_y[0])
    return hull_x, hull_y



n = 10
plane = 'c' # square or circle
Points=[]

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
hullxy=Jarvis_march(Points)
plt.plot(hullxy[0],hullxy[1])
plt.show()
