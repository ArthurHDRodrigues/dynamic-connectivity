
'''
When describing the time complexity of the follownig
functions, let n be the number of nodes in the treap.
'''

class treapNode:
    def __init__(self, v, priority, is_level=0):
        '''
        Runs in O(1).
        '''
        self.parent = None
        self.left = None
        self.right = None
        self.priority = priority
        self.val = v
        self.size = 1
        self.reserve_degree_count = 0
        self.level_count = is_level
        self.is_level = is_level

def printNode(treap):
    '''
    Runs in O(1).
    '''
    if ( treap ):
        print("parent",treap.parent)
        print("left   ",treap.left)
        print("right   ",treap.right)
        print("priority  ",treap.priority)
        print("val  ",treap.val)
        print("size   ",treap.size)
        return
    print("treap is None")


def printSequence(treap):
    '''
    Runs in O(n).
    '''
    printSequenceRecursive(treap,0)
    print("") #print newline

def printSequenceRecursive(treap,i):
    '''
    Runs in O(n).
    '''
    if(treap):
        printSequenceRecursive(treap.left,i+1)
        print(3*i*' ',treap.val,treap.priority)
        printSequenceRecursive(treap.right,i+1)


def printSequenceHK(treap):
    '''
    Runs in O(n).
    '''
    printSequenceRecursiveHK(treap,0)
    print("") #print newline

def printSequenceRecursiveHK(treap,i):
    '''
    Runs in O(n).
    '''
    if(treap):
        printSequenceRecursiveHK(treap.left,i+1)
        print(3*i*' ',treap.val,treap.priority)
        printSequenceRecursiveHK(treap.right,i+1)

################################
#  Methods get info from treaps
################################

def getSize(treap):
    '''
    Runs in O(1).
    '''
    if (treap != None):
        return treap.size
    return 0

def getListEdgesOfLevel(root):
    '''
    It runs in O(k lg(n)) expected, where k is the number
    of nodes with is_level == 1.

    The funcion dg/replace amortizes k.
    ''' 
    r = []
    getListEdgesOfLevelRecursive(root, r)
    return r

def getListEdgesOfLevelRecursive(root, r):
    '''
    Runs in O(k lg(n)) expected, where k is the number
    of nodes with is_level == 1.

    Assumes that root != None.
    '''
    if root.left != None and root.left.level_count > 0:
        getListEdgesOfLevelRecursive(root.left,r)
    if root.is_level:
        r.append(root)
    if root.right != None and root.right.level_count > 0:
        getListEdgesOfLevelRecursive(root.right,r)

def searchReserveNode(root):
    '''
    Returns a node which has incident reserve edges.

    It assumes that root.reserve_degree_count > 0.

    Runs in O(lg n) expected.
    '''
    if len(root.nte):
        return root

    if(root.left and root.left.reserve_degree_count > 0):
        return searchReserveNode(root.left)
    
    return searchReserveNode(root.right)

##################################
#  Methods update info from treaps
##################################

def incrementReserveDegree(node):
    '''
    Increments the field reserve_degree and, if necessary,
    updates the field reserve_degree_count from the node
    to the root.

    This function is used when adding a new reserve edge
    to the graph.

    Runs in O(lg n) expected.
    '''
    tmp = node
    while tmp != None:
        tmp.reserve_degree_count+=1
        tmp = tmp.parent

def decrementReserveDegree(node):
    '''
    Decrements the field reserve_degree and, if necessary,
    updates the field reserve_degree_count from the node
    to the root.

    This function is used when removing a reserve edge
    from the graph as done in dg/remEdge and dg/replace.
    
    Runs in O(lg n) expected.
    '''
    tmp = node
    while tmp != None:
        tmp.reserve_degree_count-=1
        tmp = tmp.parent

def decrementLevelCountToRoot(node):
    '''
    Decrements the field reserve_degree and, if necessary,
    updates the field reserve_degree_count from the node
    to the root.
    
    Runs in O(lg n) expected.
    '''
    node.level_count -= 1
    if node.level_count == 0:
        tmp = node.parent
        while tmp != None:
            tmp.level_count -= 1
            tmp = tmp.parent

################################
#  Classic methods of treaps
################################


def getRoot(node):
    '''
    Returns the root of the treap that contains the given node.

    Runs in O(lg n) expected.
    '''
    root = node
    while(root.parent):
        root = root.parent
    return root

def order(node):
    '''
    Returns the order of a given node, that is,
    the index of the node in the Euler Tour Tree.

    Runs in O(lg n) expected.
    '''
    order=1+getSize(node.left)
    tmp = node
    while(tmp.parent):
        if(tmp == tmp.parent.right):
            order += 1+getSize(tmp.parent.left)
        tmp = tmp.parent
    return order

def join(treapL,treapR):
    '''
    Joins treapL and treapR in such a way that all nodes
    of treapR are positioned after the nodes of treapL.

    It assumes that treapL and treapR are different.

    Runs in O(lg(L+R)) expected, where L and R are the number of nodes
    of treapL and treapR, respectvely.
    '''
    if(treapL==None): return treapR
    if(treapR==None): return treapL

    if(treapL.priority > treapR.priority):
        treapL.size += treapR.size
        treapL.reserve_degree_count += treapR.reserve_degree_count 
        treapL.level_count += treapR.level_count
        
        treapL.right = join(treapL.right,treapR)
        treapL.right.parent = treapL
        
        
        return treapL
    else:
        treapR.size += treapL.size
        treapR.reserve_degree_count += treapL.reserve_degree_count 
        treapR.level_count += treapL.level_count
        
        treapR.left = join(treapL,treapR.left)
        treapR.left.parent = treapR

        
        return treapR

def split(node):
    '''
    Splits the treap that contains the given node in two treaps.
    The first contains all nodes with keys less than the key of 
    node.
    The second contains all other nodes, including the given node.

    It assumes that node != None.

    This function is only called by df/makeStart.

    Runs in O(lg(n)) expected.
    '''

    R = node
    L = node.left

    if (L != None):
        node.left = None
        node.size -= L.size
        node.reserve_degree_count -= L.reserve_degree_count
        node.level_count -= L.level_count

    tmp = node
    while(tmp.parent != None):
        if(tmp.parent.right == tmp):
            tmp.parent.right = L
         
            tmp.parent.size -= R.size
            tmp.parent.reserve_degree_count -= R.reserve_degree_count
            tmp.parent.level_count -= R.level_count
            

            if (L != None):
                L.parent = tmp.parent

            L = tmp.parent
        else:
            tmp.parent.left = R
            

            if (L != None):
                tmp.parent.size -= L.size
                tmp.parent.reserve_degree_count -= L.reserve_degree_count
                tmp.parent.level_count -= L.level_count
            

            R.parent = tmp.parent

            R = tmp.parent

        tmp = tmp.parent

    if(L != None): L.parent = None
    R.parent = None
    return L,R


def splitByNode(node):
    '''
    Splits the treap that contains the given node in two treaps.
    The first contains all nodes with keys less than the key of 
    node.
    The second contains all other nodes, *excluding* the given node.

    It assumes that node != None.

    This function is only called by df/remEdgeDF.

    Runs in O(lg(n)) expected.
    '''
    if(node==None): return None,None
    R = node.right
    L = node.left


    tmp = node
    while(tmp.parent != None):
        if(tmp.parent.right == tmp):
            tmp.parent.right = L
         
            if (R != None):
                tmp.parent.size -= R.size
                tmp.parent.reserve_degree_count -= R.reserve_degree_count
                tmp.parent.level_count -= R.level_count
            
            if (L != None):
                L.parent = tmp.parent

            L = tmp.parent
        else:
            tmp.parent.left = R
            

            if (L != None):
                tmp.parent.size -= L.size
                tmp.parent.reserve_degree_count -= L.reserve_degree_count
                tmp.parent.level_count -= L.level_count
            

            if (R != None):
                R.parent = tmp.parent

            R = tmp.parent

        tmp = tmp.parent

    if(L != None): L.parent = None
    if (R != None): R.parent = None
    return L,R

def valid_randomized_BST(root):
    if root is None:
        return True

    if root.left is not None and root.priority < root.left.priority:
        return False

    if root.right is not None and root.priority < root.right.priority:
        return False

    return valid_randomized_BST(root.left) & valid_randomized_BST(root.right)
