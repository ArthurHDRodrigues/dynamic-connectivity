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
    #log(HDTlog,'add',' te', G.maxLevel,u,v)

    G.level[(u,v)] = G.maxLevel
    addEdgeDF(G.F[G.maxLevel],u,v)

    #uu = G.F[G.maxLevel].H[(u,u)]
    #sanityCheck(getRoot(uu),G.F[G.maxLevel])


def addNonTreeEdge(G, u, v):
    if (u,v) in G.level:
        return
    #log(HDTlog,'add','nte', G.maxLevel,u,v)
    G.level[(u,v)] = G.maxLevel

    #uu = G.F[G.maxLevel].H[(u,u)]
    #sanityCheck(getRoot(uu),G.F[G.maxLevel])

    #vv = G.F[G.maxLevel].H[(v,v)]
    #sanityCheck(getRoot(vv),G.F[G.maxLevel])

    G.F[G.maxLevel].nte[u].add(v) 
    if len(G.F[G.maxLevel].nte[u]) == 1:
        uu = G.F[G.maxLevel].H[(u,u)]
        incrementReserveDegree(uu)
        #sanityCheck(getRoot(uu),G.F[G.maxLevel])
    
    G.F[G.maxLevel].nte[v].add(u)
    if len(G.F[G.maxLevel].nte[v]) == 1:
        vv = G.F[G.maxLevel].H[(v,v)]
        incrementReserveDegree(vv)
        #sanityCheck(getRoot(vv),G.F[G.maxLevel])

    #uu = G.F[G.maxLevel].H[(u,u)]
    #sanityCheck(getRoot(uu),G.F[G.maxLevel])

    #vv = G.F[G.maxLevel].H[(v,v)]
    #sanityCheck(getRoot(vv),G.F[G.maxLevel])
    

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
    level = G.level[(u,v)]
    del(G.level[(u,v)])
    #log(HDTlog,'del','nte', level,u,v)
    
    G.F[level].nte[u].remove(v)
    if len( G.F[level].nte[u] ) == 0:
        uu = G.F[level].H[(u,u)]
        decrementReserveDegree(uu)

    G.F[level].nte[v].remove(u)
    if len( G.F[level].nte[v] ) == 0:
        vv = G.F[level].H[(v,v)]
        decrementReserveDegree(vv)

    #uu = G.F[level].H[(u,u)]
    #sanityCheck(getRoot(uu),G.F[level])
    #vv = G.F[level].H[(v,v)]
    #sanityCheck(getRoot(vv),G.F[level])

#def remEdge(G,u,v):
    '''
    It assumes that u < v.

    Runs in O(lg² n) expected amortized.
    if (u,v) not in G.level:
        return

    level = G.level[(u,v)]
    del(G.level[(u,v)])
    
    if (u,v) in G.F[G.maxLevel].H:
        log(HDTlog,'del',' te', level,u,v)
        for i in range(level,G.maxLevel+1):
            remEdgeDF(G.F[i],u,v)
        replace(G,u,v,level)
    else:
        log(HDTlog,'del','nte', level,u,v)
        uu = G.F[level].H[(u,u)]
        uu.nte.remove(v)
        decrementReserveDegree(uu)
        
        vv = G.F[level].H[(v,v)]
        vv.nte.remove(u)
        decrementReserveDegree(vv)
 '''


def replace(G,u,v,level):
    '''
    It assumes that u < v.

    Runs in O(lg² n) expected amortized.
    '''
    substituted = False
    for i in range(level,G.maxLevel+1):
        if (u,u) not in G.F[i].H:
            if len(G.F[i].nte[u]) > 0:
                y = G.F[i].nte[u].pop()
                G.F[i].nte[y].remove(u)


                if len( G.F[i].nte[y] ) == 0:
                    yy = G.F[i].H[(y,y)]
                    decrementReserveDegree(yy)

                if u < y:
                    a = u
                    b = y
                else:
                    a = y
                    b = u
                #log(HDTlog,'srp',' te', i,a,b)
                addEdgeDF(G.F[i],a,b)

                #uu = G.F[i].H[(u,u)]
                #sanityCheck(getRoot(uu),G.F[i])

                for j in range(i+1,G.maxLevel+1):
                    addEdgeDF(G.F[j],a,b,0)
                    #uu = G.F[j].H[(u,u)]
                    #sanityCheck(getRoot(uu),G.F[j])
                return
            # if (u,u) not in G.F[i].H and
            # and len(G.F[i].nte[u]) = 0, then
            # there is no substitute for uv in level i
            continue
        if (v,v) not in G.F[i].H:
            if len(G.F[i].nte[v]) > 0:
                y = G.F[i].nte[v].pop()
                G.F[i].nte[y].remove(v)

                if len( G.F[i].nte[y] ) == 0:
                    yy = G.F[i].H[(y,y)]
                    decrementReserveDegree(yy)

                if v < y:
                    a = v
                    b = y
                else:
                    a = y
                    b = v
                #log(HDTlog,'srp',' te', i,a,b)
                addEdgeDF(G.F[i],a,b)

                #vv = G.F[i].H[(v,v)]
                #sanityCheck(getRoot(vv),G.F[i])

                for j in range(i+1,G.maxLevel+1):
                    addEdgeDF(G.F[j],a,b,0)
                return
            continue

        Tv = getRoot(G.F[i].H[(v,v)])
        Tu = getRoot(G.F[i].H[(u,u)])
        if Tv.size < Tu.size:
            Tu = Tv
        edgeList = getListEdgesOfLevel(Tu)
        #if len(edgeList) == 0:
        #    HDTlog.write(f'[rep] {u} edgeList empty\n')
       
        # Downgrading level-i edges in Tu to level i-1
        # We know that x < y.
        for xy in edgeList:
            x,y = xy.val
            G.level[(x,y)] = i-1
            xy.is_level = 0
            decrementLevelCountToRoot(xy)
            addEdgeDF(G.F[i-1],x,y)
            #log(HDTlog,'dec',' te', i-1,x,y)

        # While there is an node incident reserve edges
        while Tu.reserve_degree_count and not substituted:
            #HDTlog.write(f'Tu.c {Tu.reserve_degree_count}\n')
            xx = searchReserveNode(G.F[i],Tu)
            x,_ = xx.val
            #if G.F[i].H[(x,x)] != xx:
            #   print("PERIGO: nó",xx.val,"não é active") 
            toBeRemoved = []
            for y in G.F[i].nte[x]:
                
                # Python3 doesn't allow to modify G.F[i].nte[x] while iteration
                # over it. So we add y to a 'toBeRemoved' list and will
                # remove it later.
                toBeRemoved.append(y)

                if connectedDF(G.F[i],x,y):
                    if x < y:
                        G.level[(x,y)] = i-1
                    else:
                        G.level[(y,x)] = i-1

                    G.F[i-1].nte[x].add(y)
                    if len( G.F[i-1].nte[x] ) == 1:
                        xx2 = G.F[i-1].H[(x,x)]
                        incrementReserveDegree(xx2)


                    G.F[i-1].nte[y].add(x)
                    if len( G.F[i-1].nte[y] ) == 1:
                        yy = G.F[i-1].H[(y,y)]
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
                    #log(HDTlog,'rep',' te', i,x,y)
                    addEdgeDF(G.F[i],a,b)
                    for j in range(i+1,G.maxLevel+1):
                        addEdgeDF(G.F[j],a,b,0)
                    break

            #HDTlog.write(f'{x} {xx.val} {len( G.F[i].nte[x] )} {toBeRemoved}\n')
            for y in toBeRemoved:
                G.F[i].nte[x].remove(y)
                G.F[i].nte[y].remove(x)
                if len(G.F[i].nte[y]) == 0:
                    yy = G.F[i].H[(y,y)]
                    decrementReserveDegree(yy)
            
            if len( G.F[i].nte[x] ) == 0:
                decrementReserveDegree(xx)
            #sanityCheck(getRoot(xx),G.F[i])
            #HDTlog.write(f'Tu.c {Tu.reserve_degree_count}\n')
            if substituted:
                return

def log(logfile, is_tree, operation, level, u, v):
    logfile.write(f'{is_tree} {operation} {level} {u} {v}\n')
