from ETT import *

class dynamicForrest:
    def __init__(self,n):
        self.n = n
        self.H = dict()
        for i in range(1,n+1):
            self.H[(i,i)] = treapNode((i,i))

def connectedDF(F,u,v):
    uu = F.H[(u,u)]
    vv = F.H[(v,v)]
    return getRoot(uu) == getRoot(vv)


def makeStart(F,u):
    uu = F.H[(u,u)]
    T = getRoot(uu)
    vv = search(T,1)
    v = vv.info[0]
    if(vv != uu):
        vv.has_reserve = F.H[(v,v)].has_reserve
        updateReserveToRoot(vv)
        F.H[(v,v)] = vv
        A,B = split(uu)
        vv = getLast(B)
        B,C = split(vv)
        uu = treapNode((u,u))
        join(join(B,A),uu)


def addEdgeDF(F,u,v):
    if (u,v) in F.H:
        return
    makeStart(F,u)
    makeStart(F,v)
    U = getRoot(F.H[(u,u)])
    V = getRoot(F.H[(v,v)])
    uv = treapNode((u,v),is_level=1)
    vu = treapNode((v,u),is_level=1)
    uu = treapNode((u,u))
    F.H[(u,v)] = uv
    F.H[(v,u)] = vu
    join(join(join(join(U,uv),V),vu),uu)


def remEdgeDF(F,u,v):
    uv = F.H[(u,v)]
    vu = F.H[(v,u)]
    Kuv = order(uv)
    Kvu = order(vu)
    if(Kuv > Kvu):
        u,v = v,u
        uv,vu=vu,uv
        Kuv,Kvu = Kvu,Kuv
    S = getRoot(uv)
    uu = search(S,Kuv-1)
    vv = search(S,Kuv+1)
    A,B = split(uu) #Split in S
    B,C = split(vv) #apply split in B
    C,D = split(vu) #split in C
    xx = search(D,2)
    D,E = split(xx) #spli in D
    xx.has_reserve = F.H[(u,u)].has_reserve
    updateReserveToRoot(xx)
    F.H[(u,u)] = xx
    del(F.H[(u,v)])
    del(F.H[(v,u)])
    join(A,E)
