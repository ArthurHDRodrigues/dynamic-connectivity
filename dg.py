from math import log2,ceil
from df import *
from ETT import *
from graph import *

class dynamicGraph:
    def __init__(self,n):
        self.n = n
        self.maxLevel = ceil(log2(n))
        self.F = ['']
        self.R = ['']
        self.level = dict()
        for i in range(self.maxLevel):
            Fi = dynamicForrest(n)
            Ri = graph(n)
            self.F.append(Fi)
            self.R.append(Ri)

def printDG(G):
    print("maxLevel  : ",G.maxLevel)
    print("R:")
    for i in range(1,G.maxLevel+1):
        print(i,':',G.R[i])


def addEdge(G,u,v):
    if (u,v) in G.level:
        return
    G.level[(u,v)] = G.maxLevel
    G.level[(v,u)] = G.maxLevel
    if connectedDF(G.F[G.maxLevel],u,v):
        addEdgeGLA(G.R[G.maxLevel],u,v)
        uu = G.F[G.maxLevel].H[(u,u)]
        uu.has_reserve += 1
        updateReserveToRoot(uu)

        vv = G.F[G.maxLevel].H[(v,v)]
        vv.has_reserve += 1
        updateReserveToRoot(vv)

    else:
        addEdgeDF(G.F[G.maxLevel],u,v)

def connected(G,u,v):
    return connectedDF(G.F[G.maxLevel],u,v)

def remEdge(G,u,v):
    level = G.level[(u,v)]
    del(G.level[(u,v)])
    del(G.level[(v,u)])
    if G.F[G.maxLevel].H[(u,v)] != None:
        for i in range(level,G.maxLevel+1):
            remEdgeDF(G.F[i],u,v)
        replace(G,u,v,level)
    else:
        remEdgeGLA(G.R[level],u,v)


def replace(G,u,v,level):
    for i in range(level,G.maxLevel+1):
        Tv = getRoot(G.F[i].H[(v,v)])
        Tu = getRoot(G.F[i].H[(u,u)])
        if Tv.tam < Tu.tam:
            u,v = v,u
            Tu,Tv = Tv,Tu
        edgeList = getListEdgesOfLevel(Tu)
        for xy in edgeList:
            x = xy.info[0]
            y = xy.info[1]
            G.level[(x,y)] = i-1
            G.level[(y,x)] = i-1
            xy.is_level = 0
            updateLevelToRoot(xy)
            addEdgeDF(G.F[i-1],x,y)
        vertexList = getListReserveNodes(Tu)
        for xx in vertexList:
            x = xx.info[0]
            R = G.R[i].AL[x].copy()
            for y in R:
                delEdgeGLA(G.R[i],x,y)
                
                xx.has_reserve-=1
                updateReserveToRoot(xx)
                
                yy = G.F[i].H[(y,y)]
                yy.has_reserve-=1
                updateReserveToRoot(yy)
                
                if connectedDF(G.F[i],x,y):
                    G.level[(x,y)] = i-1
                    addEdgeGLA(G.R[i-1],x,y)
                else:
                    for j in range(i,G.maxLevel+1):
                        addEdgeDF(G.F[j],x,y)
                    return

