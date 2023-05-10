from math import log2
from df import *
from graph import *

class dynamicGraph:
    def __init__(self,n):
        self.n = n
        self.nivel = log2(n)
        self.F = ['']
        self.R = ['']
        for i in range(self.nivel):
            Fi = dynamicForrest(n)
            Ri = graph(n)
            self.F.append(Fi)
            self.R.append(Ri)

def addEdge(G,u,v):
    if connectedDF(G.F[G.nivel],u,v):
        addEdgeGLA(G.R[G.nivel],u,v)
    else:
        addEdgeDF(G.F[G.nivel],u,v)

def connected(G,u,v):
    return connectedDF(G.F[G.nivel],u,v)

def remEdge(G,u,v):
    return

