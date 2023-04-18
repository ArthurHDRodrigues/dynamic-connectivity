from ETT import *

class dynamicForrest:
    def __init__(self,n):
        self.n = n
        self.H = dict()
        for i in range(1,n):
            self.H[(i,i)] = treapNode((i,i))

def connectedDF(F,u,v):
    uu = F.H[(u,u)]
    vv = F.H[(v,v)]
    return getRoot(uu) == getRoot(vv)


def makeStart(F,u):
    uu = F.H[(u,u)]
    T = getRoot(uu)
    vv = search(T,1)
    if(vv != uu):
        F.H[(v,v)] = vv
        A,B = split(T,uu)
        vv = getLast(B)
        B,C = split(T,vv)
        uu = treapNote((u,u))
        join(join(B,A),uu)


def addEdgeDF(F,u,v):
    makeStart(F,u)
    makeStart(F,v)
    U = getRoot(F.H[(u,u)])
    V = getRoot(F.H[(v,v)])
    uv = treapNote((u,v))
    vu = treapNote((v,u))
    uu = treapNote((u,u))
    F.H[(u,v)] = uv
    F.H[(v,u)] = vu
    join(join(join(join(U,uv),V),vu),uu)


def remEdgeDF(F,u,v):
    Kuv = order(F.H[(u,v)])
    Kvu = order(F.H[(v,u)])
    if(Kuv > Kvu):
        remEdgeDF(F,v,u)
        return
    S = getRoot(uv)
    uu = search(S,Kuv-1)
    vv = search(S,Kuv+1)
    A,B = split(S,uu)
    B,C = split(B,vv)
    C,D = split(C,vu)
    uu = search(D,2)
    D,E = split(D,uu)
    del(F.H[(u,v)])
    del(F.H[(v,u)])
    join(A,E)


