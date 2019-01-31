# economic model module for finding optimal ransom based on pre-conditons
# handles fixed price ransoms
# D. Hurley-Smith, E. Cartwright, J. Hernandez-Castro, A. Stepannova 2018
import sys
import array
import string
import scipy as sp
import numpy as np
import random as r
from population import population
from utilities import hypothetical_fixed, theta
import matplotlib.pyplot as plt

def fixed_model(pop,m,a,lmbd,n,i):
    # calculate the Total Revenue and Profit for the criminals
    e = np.exp(-lmbd*m.r[i])
    tqp = (m.r[i]**a)*e # calculate quantity of willing to pay pop
    qp = tqp*(1-pop.b)*(1-pop.d) # of which a proportion are immune    
    TR = m.r[i]*n*qp

    return TR, qp

def fixed_opt_model(pop,m,a,lmbd,n,i):
    # now try for optimal ransom!
    opt_r = (1 + a)/lmbd # calculate the optimal ransom for current curve
    opt_e = np.exp(-lmbd*opt_r)
    toqp = (opt_r**a)*opt_e
    oqp = toqp*(1-pop.b)*(1-pop.d)
    optTR = opt_r*n*oqp

    return optTR,oqp,opt_r

def fixed(this_mal,sample_WTP,i):
    pop = population(sample_WTP,0,0)
    pop.defense_vars(0.6,50,0,0.3,50,0)
    a,lmbd,n = pop.WTP_parser()

    TR,qp = fixed_model(pop,this_mal,a,lmbd,n,i)
    optTR,oqp,opt_r = fixed_opt_model(pop,this_mal,a,lmbd,n,i)

    return n, TR, qp, optTR, oqp, opt_r, pop, a, lmbd
                
def discrim(this_mal,sample_WTP):
    this_WTP = []
    t_TR = []
    t_qp = []
    t_optTR = []
    t_oqp = []
    t_n = []
    t_opt_r = []
    c = 0
    temp_WTP = list(sample_WTP)
    r.shuffle(temp_WTP)
    for i in this_mal.r:
        # manually selected price bands, assumes low sophistication intel
        if this_mal.dm == 'price_bracket':
            this_WTP,temp_WTP = this_mal.bands(temp_WTP,this_mal.bd[c])
        # no sorting method, randomly fires ransoms at targets regardless of WTP    
        elif this_mal.dm == 'no_choice':
            this_WTP = this_mal.no_intel(temp_WTP,sample_WTP,c)
            
        n,TR,qp,optTR,oqp,opt_r,pop,a,lmbd = fixed(this_mal,this_WTP,c)

        t_n.append(n)
        t_TR.append(TR)
        t_qp.append(qp)
        t_optTR.append(optTR)
        t_oqp.append(oqp)
        t_opt_r.append(opt_r)

        hypothetical_fixed(pop,this_mal,a,lmbd,n,optTR,TR,
                               qp,oqp,opt_r,c,i)

        c = c+1

    return t_n,t_TR,t_qp,t_optTR,t_oqp,t_opt_r
    
