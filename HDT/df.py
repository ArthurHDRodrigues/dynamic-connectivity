from .ETT import *
import sys
import random

class dynamicForest:
    def __init__(self,n):
        '''
        Runs in O(n).
        '''
        self.H = dict()
        self.nte = []
        for i in range(n):
            self.nte.append(set())


def connectedDF(F,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    if u == v:
        return True
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

    uv = treapNode((u,v),random.randint(0,sys.maxsize),is_level)
    F.H[(u,v)] = uv
    if (u,u) not in F.H:
        F.H[(u,u)] = uv
        if len(F.nte[u]) > 0:
            incrementReserveDegree(uv)
        U = None
    else:
        U = makeStart(F,u)

    vu = treapNode((v,u),random.randint(0,sys.maxsize),0)
    F.H[(v,u)] = vu
    if (v,v) not in F.H:
        F.H[(v,v)] = vu
        if len(F.nte[v]) > 0:
            incrementReserveDegree(vu)
        V = None
    else:
        V = makeStart(F,v)
    

    join(join(join(U,uv),V),vu)


def remEdgeDF(F,u,v):
    '''
    Runs in O(lg n) expected.
    '''
    uv = F.H[(u,v)]
    vu = F.H[(v,u)]

    # if (F.H[(u,u)] == uv and len(F.nte[u]) > 0) is True
    # then we need to decrement the reserve degree before
    # splitting.
    if F.H[(u,u)] == uv and len(F.nte[u]) > 0:
        decrementReserveDegree(uv)
    if F.H[(v,v)] == vu and len(F.nte[v]) > 0:
        decrementReserveDegree(vu)
    
    # Fix F.H[(v,v)] and F.H[(u,u)]
    # We need to do it before splitting to check if 
    # uv is sucessor of vu or vice versa
    successor_uv = successor(uv)
    if  successor_uv == vu:
        # v is going to be an isolated vertex
        # and we know that F.H[(v,v)] == vu
        del(F.H[(v,v)])
    elif successor_uv is not None:
        F.H[(v,v)] = successor_uv
        if len(F.nte[v]) > 0:
            incrementReserveDegree( successor_uv )
    
    successor_vu = successor(vu)
    if  successor_vu == uv:
        # u is going to be an isolated vertex
        # and we know that F.H[(u,u)] == uv
        del(F.H[(u,u)])
    elif successor_vu is not None:
        F.H[(u,u)] = successor_vu
        if len(F.nte[u]) > 0:
            incrementReserveDegree( successor_vu )
        
    A,B = splitByNode(uv)
    C = join(B,A)
    D,E = splitByNode(vu) 

    del(F.H[(u,v)])
    del(F.H[(v,u)])
    

def searchReserveNode(F, root):
    '''
    Returns a node which has incident reserve edges.

    It assumes that root.reserve_degree_count > 0.

    Runs in O(lg n) expected.
    '''
    u = root.val[0]
    if F.H[(u,u)] == root and len(F.nte[u]):
        return root

    if(root.left and root.left.reserve_degree_count > 0):
        return searchReserveNode(F, root.left)
    
    return searchReserveNode(F, root.right)
