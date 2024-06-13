from .ETT import *
import sys
import random

class dynamicForest:
    def __init__(self,n):
        '''
        Runs in O(n).
        '''
        self.H = dict()
        for v in range(n):
            self.H[(v,v)] = treapNode(v, random.randint(0,sys.maxsize))


def connectedDF(F,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    uu = F.H[(u,u)]
    vv = F.H[(v,v)]
    return getRoot(uu) == getRoot(vv)


def makeStart(F,v):
    '''
    Moves vv to the front of the sequence
    Return the root of the resulting treap
    
    Runs in O(lg n) expected.
    '''
    vv = F.H[(v,v)]
    A,B = split(vv)

    if A is None:
        # vv is already the first node
        return B

    # We need to get the first and last node in A to
    # update F.H[x,x] and F.H[u,v]
    xxA = A
    while xxA.left not None:
        xxA = xxA.left
    uu = A
    while uu.right not None:
        uu = uu.right
    
    xx = B
    while xx.right not None:
        xx = xx.right
    
    # C is going to be deleted
    B,C = split(xx)
    
    F.H[(x,x)] = xxA

    newvv = treapNode(v, random.randint(0,sys.maxsize))
    F.H[(u,v)] = (uu, newvv)
    return join(join(B,A),newvv)


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

