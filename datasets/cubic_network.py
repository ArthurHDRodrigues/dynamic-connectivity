import networkx as nwx
import random

#G = nwx.Graph()

#for v in range(100):
#    G.add_node(1)
N = 10

G = nwx.random_regular_graph(3,10)

for e in G.edges:
    uv = random.choice(list(G.edges))
    u, v = uv
    print(u)
    print(v)

