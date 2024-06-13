from math import log2,ceil
from .df import *


#HDTlog = open("logs/HDT_operations.log","w")

class dynamicGraph:
    '''
    Runs in O(lg n).
    '''
    def __init__(self,n):
        self.n = n
        self.maxLevel = ceil(log2(n))
        self.F = ['']
        self.level = dict()
        for i in range(self.maxLevel):
            Fi = dynamicForest(n)
            self.F.append(Fi)

def printDG(G):
    print("maxLevel  : ",G.maxLevel)
    print("R:")
    for i in range(1,G.maxLevel+1):
        print(i,':',G.R[i])

def addTreeEdge(G, u, v):
    if (u,v) in G.level:
        return

    G.level[(u,v)] = G.maxLevel
    addEdgeDF(G.F[G.maxLevel],u,v)

def addNonTreeEdge(G, u, v):
    if (u,v) in G.level:
        return
    G.level[(u,v)] = G.maxLevel
    uu = G.F[G.maxLevel].H[(u,u)]
    uu.nte.add(v)
    incrementReserveDegree(uu)
    
    vv = G.F[G.maxLevel].H[(v,v)]
    vv.nte.add(u)
    incrementReserveDegree(vv)

def addEdge(G,u,v):
    '''
    It assumes the u < v.

    Runs in O(lg n) expected.
    '''
    if (u,v) in G.level:
        return

    G.level[(u,v)] = G.maxLevel
    if connectedDF(G.F[G.maxLevel],u,v):
        #log(HDTlog,'add','nte', G.maxLevel,u,v)
        
        uu = G.F[G.maxLevel].H[(u,u)]
        uu.nte.add(v)
        incrementReserveDegree(uu)
        
        vv = G.F[G.maxLevel].H[(v,v)]
        vv.nte.add(u)
        incrementReserveDegree(vv)
    else:
        #log(HDTlog,'add',' te', G.maxLevel,u,v)
        addEdgeDF(G.F[G.maxLevel],u,v)

def connected(G,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    return connectedDF(G.F[G.maxLevel],u,v)

def isEdge(G,u,v):
    '''
    It assumes that u < v.
    '''
    return (u,v) in G.level

def isTreeEdge(G,u,v):
    return (u,v) in G.F[G.maxLevel].H

def remTreeEdge(G, u, v):
    level = G.level[(u,v)]
    del(G.level[(u,v)])
    
    #log(HDTlog,'del',' te', level,u,v)
    for i in range(level,G.maxLevel+1):
        remEdgeDF(G.F[i],u,v)
    replace(G,u,v,level)

def remNonTreeEdge(G,u,v):
    #log(HDTlog,'del','nte', level,u,v)
    level = G.level[(u,v)]
    del(G.level[(u,v)])
    
    uu = G.F[level].H[(u,u)]
    uu.nte.remove(v)
    decrementReserveDegree(uu)
    
    vv = G.F[level].H[(v,v)]
    vv.nte.remove(u)
    decrementReserveDegree(vv)


def remEdge(G,u,v):
    '''
    It assumes that u < v.

    Runs in O(lg² n) expected amortized.
    '''
    if (u,v) not in G.level:
        return

    level = G.level[(u,v)]
    del(G.level[(u,v)])
    
    if (u,v) in G.F[G.maxLevel].H:
        #log(HDTlog,'del',' te', level,u,v)
        for i in range(level,G.maxLevel+1):
            remEdgeDF(G.F[i],u,v)
        replace(G,u,v,level)
    else:
        #log(HDTlog,'del','nte', level,u,v)
        uu = G.F[level].H[(u,u)]
        uu.nte.remove(v)
        decrementReserveDegree(uu)
        
        vv = G.F[level].H[(v,v)]
        vv.nte.remove(u)
        decrementReserveDegree(vv)


def replace(G,u,v,level):
    '''
    It assumes that u < v.

    Runs in O(lg² n) expected amortized.
    '''
    substituted = False
    for i in range(level,G.maxLevel+1):
        Tv = getRoot(G.F[i].H[(v,v)])
        Tu = getRoot(G.F[i].H[(u,u)])
        if Tv.size < Tu.size:
            Tu = Tv
        edgeList = getListEdgesOfLevel(Tu)
        #if len(edgeList) == 0:
            #HDTlog.write(f'[rep] {u} edgeList empty\n')
       
        # Downgrading level-i edges in Tu to level i-1
        # We know that x < y.
        for xy in edgeList:
            x = xy.val[0]
            y = xy.val[1]
            G.level[(x,y)] = i-1
            xy.is_level = 0
            decrementLevelCountToRoot(xy)
            addEdgeDF(G.F[i-1],x,y)
            #log(HDTlog,'dec',' te', i-1,x,y)

        # While there is an node incident reserve edges
        while Tu.reserve_degree_count and not substituted:
            #HDTlog.write(f'Tu.c {Tu.reserve_degree_count}\n')
            xx = searchReserveNode(Tu)
            x = xx.val[0]
            toBeRemoved = []
            for y in xx.nte:
                
                # Python3 doesn't allow to modify xx.nte while iteration
                # over it. So we add y to a 'toBeRemoved' list and will
                # remove later.
                toBeRemoved.append(y)

                
                if connectedDF(G.F[i],x,y):
                    if x < y:
                        G.level[(x,y)] = i-1
                    else:
                        G.level[(y,x)] = i-1

                    xx = G.F[i-1].H[(x,x)]
                    xx.nte.add(y)
                    incrementReserveDegree(xx)

                    yy = G.F[i-1].H[(y,y)]
                    yy.nte.add(x)
                    incrementReserveDegree(yy)

                    #log(HDTlog,'dec','nte', i-1,x,y)
                else:
                    if x < y:
                        a = x
                        b = y
                    else:
                        a = y
                        b = x
                    substituted = True
                    #log(HDTlog,'rep',' te', i-1,x,y)
                    addEdgeDF(G.F[i],a,b)
                    for j in range(i+1,G.maxLevel+1):
                        addEdgeDF(G.F[j],a,b,0)
                    break

            # TODO: remove this call to xx
            xx = G.F[i].H[(x,x)]
            for y in toBeRemoved:
                xx.nte.remove(y)
                
                yy = G.F[i].H[(y,y)]
                yy.nte.remove(x)
                decrementReserveDegree(yy)
            
            if len(xx.nte) == 0:
                decrementReserveDegree(xx)

            if substituted:
                return

def log(logfile, is_tree, operation, level, u, v):
    logfile.write(f'{is_tree} {operation} {level} {u} {v}\n')
