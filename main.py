from treap.treap import *

def main():
    treap = treapNode([1,2])
    treapB = treapNode([3,4])

    treap.dir = treapB
    print(treap.tam)
    printNode(treap)
    print("o último:")
    printNode(getLast(treap))
    printNode(None)   
main()
