




class graph:
    def __init__(self,n):
        self.L = []
        for i in range(n):
            self.L.append(set())
        #def __contains__(self,edge):

def addEdgeGAL(graph,u,v):
    graph.L[u].add(v)
    graph.L[v].add(u)

def remEdgeGAL(graph,u,v):
    graph.L[u].remove(v)
    graph.L[v].remove(u)
