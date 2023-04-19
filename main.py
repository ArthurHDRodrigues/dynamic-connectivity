from ETT import *
from df  import *


def main():


    F = dynamicForrest(100)

    #addEdgeDF(F,4,6)

    for i in range(1,100):
        addEdgeDF(F,i,i+1)
    printSequence(getRoot(F.H[(1,1)]))


main()
