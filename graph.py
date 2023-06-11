class graph:
    def __init__(self,n):
        self.AL = ['']
        for i in range(n):
            self.AL.append(set())

    def __str__(self):
        s = ''
        for u in range(1,len(self.AL)):
            if len(self.AL[u]) > 0:
                s+=str(u)+":"
                l = len(self.AL[u])
                i = 0
                for v in self.AL[u]:
                    s+=str(v)
                    i+=1
                    if i<l:
                        s+=','
                s+='; '
        return s

def addEdgeGLA(G,u,v):
    G.AL[u].add(v)
    G.AL[v].add(u)

def delEdgeGLA(G,u,v):
    G.AL[u].remove(v)
    G.AL[v].remove(u)

