# population generator module for finding optimal ransom based on pre-conditons
# handles fixed price ransoms
# D. Hurley-Smith, E. Cartwright, J. Hernandez-Castro, A. Stepannova 2018
import sys
import array
import string
from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
from utilities import theta

def fitfunc(x, a, b, c):
    return a * np.exp(-b * x) + c

def q_finder(pt,a,lmbd):
    q = 0
    e = np.exp(-lmbd*pt)
    q = (pt**a)*(e)
    return q

def Q_calc(v,WTP,n):
    Q = 0
    p = 0

    for i in WTP:
        if v <= i and i != 0 and v != 0:
            p = p+1

    Q = p/n
    return Q

# finds the value of F as part of an optimization function
def find_F(z,*params):
    x,y = z
    v,WTP,n = params
    Q = []
    q = []
        
    for k in v:
        Q.append(Q_calc(k,WTP,n))
        q.append(q_finder(k,x,y))

    pre_F = []

    for i in range(0,len(q)):
        pre_F.append((q[i]-Q[i])**2)

    F = sum(pre_F)
    return F
        
# finds the values a and lambda 
def var_finder(v,WTP,n):
    td = []
    tb = []
    params = (v,WTP,n)
        
    rranges = (slice(-0.5, 0.5, 0.01), slice(0.0001, 0.01, 0.0001))
    resbrute = optimize.brute(find_F,rranges,args=params,full_output=True)

    a,lmbd = resbrute[0]
    print(resbrute[0])
    print([(i,list(resbrute[2][0]).all(resbrute[0][0])) for i, sublist in enumerate(list(resbrute[2][0])) if resbrute[0][0] in sublist])
    print([(i,list(resbrute[2][1]).all(resbrute[0][1])) for i, sublist in enumerate(list(resbrute[2][1])) if resbrute[0][1] in sublist])
    return a,lmbd

class population:
    # defines a population by proportion of backed up, defended machines
    # and willingness to pay
    def __init__(self, wtp, backup, det):
        self.w = wtp
        self.b = backup
        self.d = det

    def WTP_parser(self):
        WTP_prop = []
        WTP_brackets = list(dict.fromkeys(self.w))

        while 0 in WTP_brackets: WTP_brackets.remove(0)

        a,lmbd = var_finder(WTP_brackets,self.w,len(self.w))
        
        return a,lmbd,len(self.w)

    def defense_vars(self,ad,md,cd,ab,mb,cb):
        td = []
        tb = []
##        print('def_vars: ' + str(self.w))        
        for i in self.w:
            # 'defensive spend' value for whole pop
            td.append(theta(i,md,cd,ad))
            # 'back up spend' value for whole pop
            tb.append(theta(i,mb,cb,ab))
        if self.w!=[]:       
            self.d = sum(td)/len(td)
            self.b = sum(tb)/len(tb)
        else:
            self.d = 0
            self.b = 0
