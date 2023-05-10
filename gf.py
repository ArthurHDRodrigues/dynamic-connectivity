from df.py import *
from graph import *
from math import log,ceil

class dynamicGraph:
    def __init__(self,n):
        self.n = n
        self.maxLevel = ceil(log(n,2))
        self.F = []
        self.R = []
        for i in range(self.maxLevel):
            F = dynamicForrest(n)
            self.F.append(F)

            R = graph()
            self.R.append(R)
            

