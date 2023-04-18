import random 

class treapNode:
    def __init__(self, v):
        self.parent = None
        self.esq = None
        self.dir = None
        self.prio = random.randint(0,2**31)
        self.info = v
        self.tam = 1

def printNode(treap):
    if ( treap ):
        print("parent",treap.parent)
        print("esq   ",treap.esq)
        print("dir   ",treap.dir)
        print("prio  ",treap.prio)
        print("info  ",treap.info)
        print("tam   ",treap.tam)
        return
    print("treap is None")


def getSize(treap):
    if (treap != None):
        return treap.tam
    return 0


def getLast(treap):
    if (treap):
        tmp = treap
        while tmp.dir:
            tmp = tmp.dir
        return tmp
    return None

def getRoot(treap):
    root = treap
    while(root.parent):
        root = root.parent
    return root

def search(treap,key):
    if(treap == None): return None
    if(treap.esq and treap.esq.tam >= key):
        return search(treap.esq,key)
    if(treap.esq.tam+1 == key):
        return treap
    return search(treap.dir,key-getSize(treap.esq)-1)

def order(treap):
    if(treap == None): return 0
    order=1+getSize(treap.esq)
    tmp = treap
    while(treap.parent):
        if(treap == treap.parent.dir):
            order += 1+getSize(treap.parent.esq)
        tmp = tmp.parent
    return order



def join(treapT,treapR):
    if(treapT==None): return treapR
    if(treapR==None): return treapT

    if(treapT.prio > treapR.prio):
        treapT.dir = join(treapT.dir,treapR)
        treapT.dir.parent = treapT
        treapT.tam = getSize(treapT.dir) + getSize(treapT.esq) + 1
        return treapT
    else:
        treapR.esq = join(treapT,treapR.esq)
        treapR.esq.parent = treapR
        treapR.tam = getSize(treapR.dir) + getSize(treapR.esq) + 1
        return treapR


def split(node):
    if(node==None): return None,None
    R = node
    L = node.esq

    node.esq = None
    if(L != None): L.tam = getSize(L.dir) + getSize(L.esq) + 1
    tmp = node
    while(tmp.parent != None):
        if(tmp.parent.dir == tmp):
            tmp.parent.dir = L
            if(L != None): L.parent = tmp.parent
            L = tmp.parent
            L.tam = getSize(L.dir) + getSize(L.esq) + 1
        else:
            tmp.parent.esq = R
            if(R != None): R.parent = tmp.parent
            R = tmp.parent
            R.tam = getSize(R.dir) + getSize(R.esq) + 1
        tmp = tmp.parent

    if(L != None): L.parent = None
    if(R != None): R.parent = None
    return L,R




