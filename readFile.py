from dg import *

def importFromFile(fileName,VERBOSE=0):
    file = open(fileName, 'r')
    lines = file.readlines()
    n = int(lines.pop(0))
    G = dynamicGraph(n)
    for line in lines:
        symbol_list = line.split()
        operation = symbol_list[0]
        u = int(symbol_list[1])
        v = int(symbol_list[2])
        match operation:
            case '+':
                if VERBOSE:
                    print("Adding edge (",u,",",v,")")
                addEdge(G,u,v)
            case '-':
                if VERBOSE:
                    print("Deleting edge (",u,",",v,")")
                remEdge(G,u,v)
            case '?':
                if connected(G,u,v):
                    print("vertices ",u," and ",v," are connected")
                else:
                    print("vertices ",u," and ",v," are NOT connected")
            case default:
                print("Error, unknown operation")



    return G


