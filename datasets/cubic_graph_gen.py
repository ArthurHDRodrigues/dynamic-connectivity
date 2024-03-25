import random
import networkx as nwx




file = open("cubic","w")
T = 0 # Variable for Time Stamp

N = 200
S = 1000000


# Current set of edges
E = set()

def genCubic( N , T):
    for v in range(N):
        file.write(f"+,{v},{(v+1)%N},{T}\n")
        T+=1
    

    # This set constains all already sampled vertices
    repeated = set()
    for v in range(N):
        if v not in repeated:
            u = random.randrange(v, N)
            while u in repeated:
                u = random.randrange(v, N)
            repeated.add(v)
            repeated.add(u)
            file.write(f"+,{v},{u},{T}\n")
            T+=1
            E.add((u,v))
    return T

        
def crossEdges( G, S, T):
    for t in range(S):
        edges = list(G.edges)

        uv = random.choice(edges)
        xy = random.choice(edges)
        while uv == xy:
            xy = random.choice(edges)
        

        u, v = uv
        G.remove_edge(u,v) 
        x, y = xy
        G.remove_edge(x,y) 
        
        file.write(f"-,{u},{v},{T}\n")
        T+=1
        file.write(f"-,{x},{y},{T}\n")
        T+=1


        file.write(f"+,{u},{x},{T}\n")
        T+=1
        file.write(f"+,{v},{y},{T}\n")
        T+=1
        G.add_edge(u,x)
        G.add_edge(v,y)
 
        
    

# Returns a random cubic graph
G = nwx.random_regular_graph(3, N)
for e in G.edges:
    u, v = e
    file.write(f"+,{u},{v},{T}\n")
    T+=1
    


#T = genCubic(N, T)

crossEdges(G, S, T)

file.close()
