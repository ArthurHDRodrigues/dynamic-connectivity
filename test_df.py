from ETT import *
from df  import *


def main():
    F = dynamicForrest(100)

    for i in range(1,100):
        addEdgeDF(F,i,i+1)

    for i in [24,64,66,42,92]:
        remEdgeDF(F,i,i+1)

    alreadyPrinted = []
    for i in range(1,101):
        ii = F.H[i,i]
        if ii == None:
            print("Error!!", i, "é None")
        else:
            root = getRoot(ii)
            if root not in alreadyPrinted:
                printSequence(root)
                for i in getListActiveNodes(root):
                    print(i.info)
                alreadyPrinted.append(root)


main()
