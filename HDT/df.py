from .ETT import *
import sys
import random

class dynamicForest:
    def __init__(self,n):
        '''
        Runs in O(n).
        '''
        self.H = dict()
        self.te = []
        self.nte = []
        for i in range(n):
            self.te.append(set())
            self.nte.append(set())


def connectedDF(F,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    if (v,v) not in F.H or (u,u) not in F.H:
        return False
    uu = F.H[(u,u)]
    vv = F.H[(v,v)]
    return getRoot(uu) == getRoot(vv)


def makeStart(F,u):
    '''
    Moves uu to the front of the sequence
    
    Runs in O(lg n) expected.
    '''
    uu = F.H[(u,u)]
    A,B = split(uu)
    return join(B,A)

def addEdgeDF(F,u,v,is_level=1):
    '''
    It assumes that u < v

    Runs in O(lg n) expected.
    '''
    U = makeStart(F,u)
    V = makeStart(F,v)
    uv = treapNode((u,v),random.randint(0,sys.maxsize),is_level)
    vu = treapNode((v,u),random.randint(0,sys.maxsize),0)
    F.H[(u,v)] = uv
    F.H[(v,u)] = vu
    join(join(join(U,uv),V),vu)


def remEdgeDF(F,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    uv = F.H[(u,v)]
    vu = F.H[(v,u)]
    Kuv = order(uv)
    Kvu = order(vu)
    if(Kuv > Kvu):
        uv,vu=vu,uv
    A,B = splitByNode(uv) #Split in S
    B,C = splitByNode(vu) #Split in S
    del(F.H[(u,v)])
    del(F.H[(v,u)])
    join(A,C)

