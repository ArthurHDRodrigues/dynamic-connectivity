class graph:
    def __init__(self,n):
        self.AL = []
        for i in range(n):
            self.AL.append(set())

def addEdgeGLA(G,u,v):
    G.AL[u].add(v)
    G.AL[v].add(u)

def delEdgeGLA(G,u,v):
    G.AL[u].remove(v)
    G.AL[v].remove(u)
