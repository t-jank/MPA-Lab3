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
    
def sortbyx(points): # points mergesort by x
    if len(points)==1:return points
    s=int(len(points)/2)
    a=sortbyx(points[:s])
    b=sortbyx(points[s:])
    a=a[::-1]
    b=b[::-1]
    i=a.pop()
    e=b.pop()
    c=[]
    for x in range(len(points)):
        if(i[0]<e[0]):
            c.append(i)
            if not len(a)==0:
                i=a.pop()
            else:
                c.append(e)
                for q in b:
                    c.append(q)
                break    
        else:
            c.append(e)
            if not len(b)==0:
                e=b.pop()
            else:
                c.append(i)
                for q in a:
                    c.append(q)
                break
    return c
    

def Graham_scan(points):
    n=len(points)
    Lupper=[]
    points = sortbyx(points)
    
    Lupper.append(points[0])
    Lupper.append(points[1])
    for i in range(2,n):
        Lupper.append(points[i])
        lenlupper=len(Lupper)
        while(lenlupper>2 and ifright(Lupper[lenlupper-3],Lupper[lenlupper-2],Lupper[lenlupper-1])==False):
            Lupper.remove(Lupper[lenlupper-2])
            lenlupper=len(Lupper)
            
    Llower=[]
    Llower.append(points[n-1])
    Llower.append(points[n-2])
    
    for i in range(n-3,0,-1):
        Llower.append(points[i])
        lenllower=len(Llower)
        while(lenllower>2 and ifright(Llower[lenllower-3],Llower[lenllower-2],Llower[lenllower-1])==False):
            Llower.remove(Llower[lenllower-2])
            lenllower=len(Llower)
    '''
    Llower.remove(Llower[0])
    Llower.remove(Llower[len(Llower)-1])
    hull = Llower + Lupper
    '''
    return Llower

'''
from functools import reduce
def convex_hull_graham(points):
    ''
    Returns points on convex hull in CCW order according to Graham's scan algorithm. 
    By Tom Switzer <thomas.switzer@gmail.com>.
    ''
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
'''


def draw_hull(hull):
    hull_x=[]
    hull_y=[]
    for i in range(0,len(hull)):
        hull_x.append(hull[i][0])
        hull_y.append(hull[i][1])
    hull_x.append(hull_x[0])
    hull_y.append(hull_y[0])
    plt.plot(hull_x,hull_y)
    plt.show()


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

#######  Jarvis  ########
#hull=Jarvis_march(Points)


#######  Graham  ########
hull=Graham_scan(Points)


draw_hull(hull)

'''
hullxg=[]
hullyg=[]
grahamhull=convex_hull_graham(Points)
for i in range(0,len(grahamhull)):
    hullxg.append(grahamhull[i][0])
    hullyg.append(grahamhull[i][1])
hullxg.append(hullxg[0])
hullyg.append(hullyg[0])
plt.plot(hullxg,hullyg)
plt.show()
'''