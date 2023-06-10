import random 

class treapNode:
    def __init__(self, v, is_level=0):
        self.parent = None
        self.esq = None
        self.dir = None
        self.prio = random.randint(0,2**31)
        self.info = v
        self.tam = 1
        self.reserve_count = 0
        self.has_reserve = 0
        self.level_count = is_level
        self.is_level = is_level

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


def printSequence(treap):
    printSequenceRecursive(treap)
    print("") #print newline
    print(treap.reserve_count)
    print(treap.level_count)

def printSequenceRecursive(treap):
    if(treap):
        if(treap.esq):
            printSequenceRecursive(treap.esq)
        print(treap.info,end='')
        if(treap.dir):
            printSequenceRecursive(treap.dir)

def getSize(treap):
    if (treap != None):
        return treap.tam
    return 0

def getReserveCount(treap):
    if (treap != None):
        return treap.reserve_count
    return 0

def getLevelCount(treap):
    if (treap != None):
        return treap.level_count
    return 0

def updateInfo(treap):
        treap.tam = getSize(treap.dir) + getSize(treap.esq) + 1
        treap.reserve_count = getReserveCount(treap.dir) + getReserveCount(treap.esq) + treap.has_reserve
        treap.level_count = getLevelCount(treap.dir) + getLevelCount(treap.esq) + treap.is_level

def updateReserveToRoot(node):
    tmp = node
    while tmp != None:
        tmp.reserve_count = getReserveCount(tmp.dir) + getReserveCount(tmp.esq) + tmp.has_reserve
        tmp = tmp.parent

def updateLevelToRoot(node):
    tmp = node
    while tmp != None:
        tmp.level_count = getReserveCount(tmp.dir) + getReserveCount(tmp.esq) + tmp.is_level
        tmp = tmp.parent


def getListEdgesOfLevel(root):
    if root == None:
        return []
    r = []
    if root.esq != None and root.esq.level_count > 0:
        r += getListEdgesOfLevel(root.esq)
    if root.is_level:
        r.append(root)
    if root.dir != None and root.dir.level_count > 0:
        r += getListEdgesOfLevel(root.dir)
    return r


def getListReserveNodes(root):
    if root == None:
        return []
    r = []
    if root.esq != None and root.esq.reserve_count > 0:
        r += getListReserveNodes(root.esq)
    if root.has_reserve:
        r.append(root)
    if root.dir != None and root.dir.reserve_count > 0:
        r += getListReserveNodes(root.dir)
    return r



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
    if(getSize(treap.esq) >= key):
        return search(treap.esq,key)
    if(getSize(treap.esq)+1 == key):
        return treap
    return search(treap.dir,key-getSize(treap.esq)-1)

def order(treap):
    if(treap == None): return 0
    order=1+getSize(treap.esq)
    tmp = treap
    while(tmp.parent):
        if(tmp == tmp.parent.dir):
            order += 1+getSize(tmp.parent.esq)
        tmp = tmp.parent
    return order

def join(treapT,treapR):
    if(treapT==None): return treapR
    if(treapR==None): return treapT

    if(treapT.prio > treapR.prio):
        treapT.dir = join(treapT.dir,treapR)
        treapT.dir.parent = treapT
        updateInfo(treapT)
        return treapT
    else:
        treapR.esq = join(treapT,treapR.esq)
        treapR.esq.parent = treapR
        updateInfo(treapR)
        return treapR

def split(node):
    if(node==None): return None,None
    R = node
    L = node.esq

    node.esq = None
    if(R != None):
        updateInfo(R)
    tmp = node
    while(tmp.parent != None):
        if(tmp.parent.dir == tmp):
            tmp.parent.dir = L
            if(L != None): L.parent = tmp.parent
            L = tmp.parent
            updateInfo(L)
        else:
            tmp.parent.esq = R
            if(R != None): R.parent = tmp.parent
            R = tmp.parent
            updateInfo(R)
        tmp = tmp.parent

    if(L != None): L.parent = None
    if(R != None): R.parent = None
    return L,R
