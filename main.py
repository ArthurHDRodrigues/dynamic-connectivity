from dg  import *
from ETT  import *


def main():
    G = dynamicGraph(100)

    for i in range(1,100):
        addEdge(G,i,i+1)

    addEdge(G,5,20)
    addEdge(G,35,50)
    addEdge(G,78,3)
    printDG(G)
    #printSequence(getRoot(G.F[G.maxLevel].H[(1,1)]))
    remEdge(G,10,11)
    printDG(G)
    #printSequence(getRoot(G.F[G.maxLevel].H[(1,1)]))
main()
