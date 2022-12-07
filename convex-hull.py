# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:26:05 2022

@author: t-jan
"""
import random
import matplotlib.pyplot as plt
import math
import time
import sys

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
    
    hull.remove(hull[0])
    return hull


def prosta(P1,P2):
    a = (P1[1] - P2[1]) / (P1[0] - P2[0])
    b = P1[1] - a*P1[0]
    return a,b

def ifright(P1,P2,P3):
    p=prosta(P1,P2)
    a=p[0]
    b=p[1]
    ynaprostej = a*P3[0] + b
    if P3[1] < ynaprostej:
        return True
    else:
        return False
    

def Graham_scan(points):
    n=len(points)
    Lupper=[]
    points.sort()
    Lupper.append(points[0])
    Lupper.append(points[1])
    for i in range(2,n):
        Lupper.append(points[i])
        lenlupper=len(Lupper)
        while(lenlupper>2 and ifright(Lupper[lenlupper-3],Lupper[lenlupper-2],Lupper[lenlupper-1])==False):
            Lupper.remove(Lupper[lenlupper-2])
            lenlupper=len(Lupper)
    Llower=[]
    Llower.append(points[0])
    Llower.append(points[1])
    for i in range(2,n):
        Llower.append(points[i])
        lenllower=len(Llower)
        while(lenllower>2 and ifright(Llower[lenllower-3],Llower[lenllower-2],Llower[lenllower-1])==True):
            Llower.remove(Llower[lenllower-2])
            lenllower=len(Llower)
    Llower.remove(Llower[0])
    Llower.remove(Llower[len(Llower)-1])
    Llower=Llower[::-1]
    hull = Llower + Lupper
    
    return hull
    

from functools import reduce
def convex_hull_graham(points):
    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)
    def cmp(a, b):
        return (a > b) - (a < b)
    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)
    def _keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull
    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


def draw_hull(hull):
    hull_x=[]
    hull_y=[]
    for i in range(0,len(hull)):
        hull_x.append(hull[i][0])
        hull_y.append(hull[i][1])
    hull_x.append(hull_x[0])
    hull_y.append(hull_y[0])
    plt.plot(hull_x,hull_y)
  #  plt.show()


def Chan_algorithm(points):
    n=len(points)
    m = H = int(n/3)
    Psubsets=[]
    j=0
    for i in range(0,math.ceil(n/m)):
        Psubsets.append([0])
    for i in range(0,len(Psubsets)):
        while j!=n and len(Psubsets[i])<=m:
            Psubsets[i].append(points[j])
            j+=1
        Psubsets[i].remove(Psubsets[i][0])
        
    hulls=Graham_scan(Psubsets[0])
    for i in range(1,len(Psubsets)):
        hulls+=Graham_scan(Psubsets[i])
        #draw_hull(Graham_scan(Psubsets[i]))
    hull=Jarvis_march(hulls)
    return hull



n = 600
plane = 'c' # square or circle
algorithm = 'c' # jarvis, graham_my, graham_fast, chan
time_measurement = True
draw = False

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
else: sys.exit("Plane undefined")

if draw==True:
    for i in range(0,len(Points)):
        plt.scatter(Points[i][0],Points[i][1],color='k')
    plt.axis('square')
    plt.xlim([0,n])
    plt.ylim(0,n)
    
start=time.time()
if algorithm=='jarvis' or algorithm=='j' or algorithm=='Jarvis':
    hull=Jarvis_march(Points)
elif algorithm=='graham_my' or algorithm=='g1' or algorithm=='g' or algorithm=='gm' or algorithm=='Graham_my':
    hull=Graham_scan(Points)
elif algorithm=='graham_fast' or algorithm=='g2' or algorithm=='gf' or algorithm=='Graham_fast':
    hull=convex_hull_graham(Points)
elif algorithm=='c' or algorithm=='ch' or algorithm=='Chan' or algorithm=='chan':
    hull=Chan_algorithm(Points)
end=time.time()






if time_measurement==True:
    print(end-start)
if draw==True:
    draw_hull(hull)
