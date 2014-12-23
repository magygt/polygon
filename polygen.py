# -*- coding:utf-8 -*-
from random import randint
from math import cos
from math import sin
from math import sqrt
from math import pi
from copy import deepcopy

def poly(size, sub):
    martrix=[[0 for i in range(size+2)] for j in range(size+2)]
    for i in range(1,size+1):
        for j in range(1,size+1):
            martrix[i][j]=1
    randbox=[]
    for i in range(1,size+1):
        randbox.append([1,i])
        randbox.append([i,1])
    randbox.pop(0)
    for i in range(2,size+1):
        randbox.append([size,i])
        randbox.append([i,size])
    randbox.pop()
    cnt=0
    while cnt != sub:
        ranrange=len(randbox)
        delpoint=randint(1,ranrange)-1
        y=randbox[delpoint][1]
        x=randbox[delpoint][0]
        while not delTest(martrix, y, x):
            delpoint=randint(1,ranrange)-1
            y=randbox[delpoint][1]
            x=randbox[delpoint][0]
        martrix[y][x]=0
        randbox.pop(delpoint)
        if martrix[y+1][x] and [x,y+1] not in randbox:
            randbox.append([x,y+1])
        if martrix[y-1][x] and [x,y-1] not in randbox:
            randbox.append([x,y-1])
        if martrix[y][x+1] and [x+1,y] not in randbox:
            randbox.append([x+1,y])
        if martrix[y][x-1] and [x-1,y] not in randbox:
            randbox.append([x-1,y])
        cnt+=1
    return martrix

def getPoint(mar,size):
    status=1#right=1,up=2,left=3,down=4
    i=1;
    j=1;
    while not mar[i][j]:
        i+=1;
        if i==size+1:
            j+=1
            i=1
    x=j
    y=i
    point=[[x,y]]
    while status:
        if status == 1:
            if mar[y-1][x+1]:
                status=4
            elif mar[y][x+1]:
                pass
            else:
                status=2
            x+=1
            if status != 1:
                point.append([x,y])
                # print [y,x]

        elif status == 2:#up
            if mar[y+1][x]:
                status=1
            elif mar[y+1][x-1]:
                pass
            else:
                status=3
            y+=1
            if status != 2:
                point.append([x,y])
                # print [y,x]

        elif status == 3:#left
            if mar[y-1][x-1] and mar[y][x-2]:
                x-=1
                status=2
            elif mar[y-1][x-1]:
                x-=1
            else:
                status=4
            if status != 3:
                point.append([x,y])
                # print [y,x]

        elif status == 4:#down
            if mar[y-1][x] and mar[y-2][x-1]:
                y-=1
                status=3
            elif mar[y-1][x]:   
                y-=1
            else:
                status=1                
            if status != 4:
                point.append([x,y])
                # print [y,x]
        if point.count([x,y]) == 2:
            status=0
    return point

def pointTransTo3D(point):
    for i in range(len(point)):
        point[i].append(0)
    
def length3D(point):
    res=sqrt(point[0]**2+point[1]**2+point[2]**2)
    if abs(res)<1e-6:
        res=0
    return res

def format3D(point):
    res=deepcopy(point)
    l=length3D(point)*1.0
    for i in range(3):
        res[i]/=l
    return res

def XMulti(vec1,vec2):
    res=[]
    res.append(vec1[1]*vec2[2]-vec1[2]*vec2[1])
    res.append(vec1[2]*vec2[0]-vec1[0]*vec2[2])
    res.append(vec1[1]*vec2[2]-vec1[2]*vec2[1])
    for i in range(3):
        if abs(res[i]) < 1e-6:
            res[i]=0
    return res

def dotMulti(vec1,vec2):
    res=0
    for i in range(3):
        res+=vec1[i]*vec2[i]
    if abs(res) < 1e-6:
        res=0
    return res

def numMulti(num,vec):
    res=deepcopy(vec)
    res[0]*=num
    res[1]*=num
    res[2]*=num
    for i in range(3):
        if abs(res[i]) < 1e-6:
            res[i]=0
    return res

def move(point,vec):
    res=deepcopy(point)
    for i in range(3):
        res[i]+=vec[i]
    return res

def rotate(point,vec,theta):
    ang=theta*pi/180
    cosang=cos(ang)
    sinang=sin(ang)
    fthe=format3D(vec)
    res1=numMulti(cosang,point)
    res2=dotMulti(point,fthe)
    res2=numMulti((1-cosang)*res2,fthe)
    res3=numMulti(sinang,XMulti(fthe,point))
    res=move(move(res1,res2),res3)
    return res

def delTest(mar, row, col):
    cnt=mar[row+1][col] + mar[row-1][col] + mar[row][col+1] + mar[row][col-1]
    if cnt == 1:
        return 1
    elif cnt == 2:
        if ( ( mar[row-1][col] and mar[row][col+1] and mar[row-1][col+1] ) or
            ( mar[row][col+1] and mar[row+1][col] and mar[row+1][col+1] ) or
            ( mar[row+1][col] and mar[row][col-1] and mar[row+1][col-1] ) or
            ( mar[row][col-1] and mar[row-1][col] and mar[row-1][col-1] ) ):
            return 1
        else:
            return 0
    else:
        if ( ( not mar[row-1][col] and mar[row+1][col-1] and mar[row+1][col+1] ) or
            ( not mar[row+1][col] and mar[row-1][col-1] and mar[row-1][col+1] ) or
            ( not mar[row][col-1] and mar[row+1][col+1] and mar[row-1][col+1] ) or
            ( not mar[row][col+1] and mar[row+1][col-1] and mar[row-1][col-1] ) ):
            return 1
        else:
            return 0
