from dg  import *
from ETT  import *
from random import randint


VNUM = 20
def main():
    G = dynamicGraph(VNUM)

    for i in range(1,VNUM):
        addEdge(G,i,i+1)

    for i in range(10):
        r = randint(1,VNUM-1)
        s = randint(r+1,VNUM)
        print(i,":(",r,",",s,")")
        addEdge(G,r,s)
    printDG(G)
    print("===============")
    for i in range(10):
        r = randint(1,VNUM-1)
        s = randint(r+1,VNUM)
        while (r,s) not in G.F[G.maxLevel].H:
            r = randint(1,VNUM-1)
            s = randint(r+1,VNUM)
        print(i,":(",r,",",s,")")
        remEdge(G,r,s)
    printDG(G)
    #printSequence(getRoot(G.F[G.maxLevel].H[(1,1)]))
main()
