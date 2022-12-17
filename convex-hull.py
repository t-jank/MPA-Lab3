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
    if B==C or A==C or A==B: return -1
    AB=length(A,B)
    BC=length(B,C)
    AC=length(A,C)
    return math.acos( (AB**2 + BC**2 - AC**2) / (2*AB*BC) )

def update_angles(hull,points,angles):
    hull_size=len(hull)
    for i in range(0,len(points)):
        angles[i]=angle(hull[hull_size-2], hull[hull_size-1], points[i])


def Jarvis_march(points):
    n=len(points)
    if n<4: return points
    hull=[]
    hull.append([0,0])
    hull.append([0,9999])
    for i in range(0,n): # finding first point of hull, the smallest y
        if points[i][1]<hull[1][1]:
            hull[1] = points[i]
    hull[0]=([-9999,hull[1][1]]) # point zero [-inf, y(P1)]
    
    angles=[]
    for i in range(0,n):
        angles.append([0])
    update_angles(hull,points,angles)
    N=([-1,-1])
    while(True):
        N=points[0]
        angle=-1
        for i in range(0,n):
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
    if n<4: return points
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


def max_angle(points,p1,p2):
    '''
    returns the point q from points that maximizes angle )<p1p2q
    by using binary search
    '''
    n=len(points)
    if n==1: return points[0]
    def susq(idx):
        if idx==n-1: idxnext=0
        else: idxnext=idx+1
        angleq=angle(p1,p2,points[idx])
        angleqnext=angle(p1,p2,points[idxnext])
        if angleqnext>angleq: return 'next'
        angleqprev=angle(p1,p2,points[idx-1])
        if angleqprev>angleq: return 'prev'
        else: return 'found'
    t=1
    idx=math.ceil(n/2**t)
    while True:
        t+=1
        sq=susq(idx)
        if sq=='found': return points[idx]
        elif sq=='next':
            idx=idx+math.ceil(n/2**t)
            if idx>=n:
                idx=idx-n
        elif sq=='prev': idx=idx-math.ceil(n/2**t)



def Chan_algorithm(points,m,H):
    n=len(points)
    ## step 1 ##
    Psubsets=[]
    j=0
    for i in range(0,math.ceil(n/m)):
        Psubsets.append([0])
    for i in range(0,len(Psubsets)):
        while j!=n and len(Psubsets[i])<=m:
            Psubsets[i].append(points[j])
            j+=1
        Psubsets[i].remove(Psubsets[i][0])
    ## step 2 i 3 ##
    hulls=[]
    for i in range(0,len(Psubsets)):
        hulls.append(Graham_scan(Psubsets[i]))
        hulls[i].reverse() # in order to have ccw order
     #   draw_hull(Graham_scan(Psubsets[i]))
    ## step 4 ##
    hull=[]
    hull.append([0,-9999]) # point zero - [0,-inf]
    ## step 5 ##
    hull.append([0,0])
    for i in range(0,n): # point 1 - the rightmost point of Points
        if points[i][0]>hull[1][0]:
            hull[1]=points[i]
    ## steps 6-8 ##
    q=[]
    qangle=[]
    for k in range(0,H):
        for i in range(0,math.ceil(n/m)):
            q.append([0,0])
            qangle.append(0)
            q[i] = max_angle(hulls[i], hull[len(hull)-2], hull[len(hull)-1])
            qangle[i]=angle(hull[len(hull)-2], hull[len(hull)-1], q[i])
    ## step 9 ##
        ind=qangle.index(max(qangle))
    ## step 10 ##
        if q[ind]==hull[1]:
            hull.remove(hull[0])
            return hull
    ## step 9 ##
        hull.append(q[ind])
        q.clear()
        qangle.clear()
    ## step 11 ##
    return 'incomplete'

def Chan_good(points):
    t=0
    n=len(points)
    while True:
        t+=1
        m=H=min(2**2**t,n)
        L=Chan_algorithm(points, m, H)
        if L!='incomplete':
            return L



plane = 'c' # square or circle
algorithm = 'c' # jarvis, graham_my, graham_fast, chan
time_measurement = True
draw = False
nMin = 1000
nMax = 1001
nStep = 50
nRepeats = 100

for n in range(nMin,nMax,nStep):
    time1=0
    cntinrep=0
    for rep in range(0,nRepeats):
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
        if algorithm=='jarvis' or algorithm=='j':
            hull=Jarvis_march(Points)
        elif algorithm=='graham_my' or algorithm=='g1' or algorithm=='g' or algorithm=='gm':
            hull=Graham_scan(Points)
        elif algorithm=='graham_fast' or algorithm=='g2' or algorithm=='gf':
            hull=convex_hull_graham(Points)
        elif algorithm=='c' or algorithm=='chan':
         #   hull=Chan_good(Points)
            hull=Chan_algorithm(Points,64,64) # szybciej, super! :) ale dziwnie się zachowuje - do n im więcej tym szybciej
        else: sys.exit("Algorithm undefined")
        end=time.time()
        cntinrep += len(hull)
        time1 += (end-start)
    if time_measurement==True:
       # print(end-start)
       print(time1)
    if draw==True:
        draw_hull(hull)
    '''
    plt.scatter(n,cntinrep/nRepeats,color='b')
    
plt.xlim(left=0)
plt.xlabel('n')
plt.ylabel('|CH(A)|')
if plane=='s': plt.title('Płaszczyzna: kwadrat')
elif plane=='c': plt.title('Płaszczyzna: koło')
'''

'''
#### badanie zlozonosci algorytmu Chana ######
    if n==10:
        plt.scatter(n,(end-start)*50000,color='crimson',label='y=50000*time measured')
        plt.scatter(n,n*len(hull)/2,color='orange',label='y=nh/2')
        plt.scatter(n,n*(math.log(len(hull))**2),color='grey',label='y=nlog^2(h)')
        plt.scatter(n,n*10,color='limegreen',label='y=10n')
        plt.scatter(n,n*math.log(n),color='blue',label='y=nlogn')
        plt.scatter(n,n*math.log(len(hull)),color='hotpink',label='y=nlogh')
    else:
        plt.scatter(n,(end-start)*50000,color='crimson')
        plt.scatter(n,n*10,color='limegreen')
        plt.scatter(n,n*math.log(n),color='blue')
        plt.scatter(n,n*len(hull)/2,color='orange')
        plt.scatter(n,n*math.log(len(hull)),color='hotpink')
        plt.scatter(n,n*(math.log(len(hull))**2),color='grey')
plt.xlim(left=0)
plt.ylim(bottom=0)        
plt.xlabel('n')
plt.ylabel('time')
plt.legend()
'''
