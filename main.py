from ETT import *
from df  import *


def main():

    treap = treapNode(1)
    for i in range(2,100):
        tmp = treapNode(i)
        treap = join(treap,tmp)
    
    printNode(treap)


    rand = random.randint(10,90)
    print("rand:",rand)
    u = search(treap,rand)
    printNode(u)
    treapA,treapB = split(u)

#######################################3

    F = dynamicForrest(100)

    for i in list(F.H):
        printNode(F.H[i])

    print(connectedDF(F,1,5))

main()
