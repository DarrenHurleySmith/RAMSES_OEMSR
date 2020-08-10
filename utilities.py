# utilities defining assorted functions for econ_model
# D. Hurley-Smith, E. Cartwright, J. Hernandez-Castro, A. Stepannova 2018
import sys
import array
import string
import scipy as sp
import numpy as np
import econ_model_mod as econ
from mal_model import mal
import matplotlib.pyplot as plt
import csv

def output_parser(n,TR,qp,name,r,c,pop,pm,dm,optTR,oqp,opt_r):
    output = []
    score = 0
    optScore = 0

    if pm == 'fixed':
        PR = TR-c
        optPR = optTR-c
        score = (PR/n)*(1-qp)
        optScore = (optPR/n)*(1-oqp)
    elif pm == 'discriminatory':
        PR = sum(TR)-c
        optPR = sum(optTR)-c
        score = (PR/sum(n))*(1-(sum(qp)/len(qp)))
        optScore = (optPR/sum(n))*(1-(sum(oqp)/len(oqp)))

    optimality = PR/optPR
    
    output.append('Malware = ' + name)
    output.append('Population = ' + pop)
    output.append('Pop Size = ' + str(n))
    output.append('Ransom Value = ' + str(r))
    output.append('Ransom Type = ' + pm)
    output.append('Discrimination Type = ' + dm)
    output.append('Cost = ' + str(c))
    output.append('Revenue = ' + str(TR))
    output.append('Total Profit = ' + str('%.2f' % PR))
    output.append('Size of paying pop (proportional) = ' + str(qp))
    output.append('Optimality = ' + str(optimality))
    output.append('Threat-level = ' + str(score))
    output.append('Optimal Revenue = ' + str(optTR))
    output.append('Optimal Profit = ' + str('%.2f' % optPR))
    output.append('Size of optimal paying pop (proportional) = ' + str(oqp))
    output.append('Optimal Ransom(s) = ' + str(opt_r))
    output.append('Threat-level of Optimal Ransom = ' + str(optScore))
    return output
        
# defines function theta which is a monotonically increasing function
# set with appropriate function (defaults until user definition is implemented)
# default = diminishing returns
def theta(e,m,c,a):
    y = (e*a)/(e+m)+c
    return y

def csv_parser(x):
    y = []
    lines = x.decode("utf-8").split('\r\n')
    for i in lines:
        if i != '':
            y.append(int(i))

    return y
        

def to_list(x):
    if len(x) > 0 and x[0] != '':
        y = x.split(",")
        y = [int(i) for i in y]
        return y

def sample_gen(vals,n,props):
    sample = np.random.choice(vals,n,p=props)
    sample = sample.tolist() 
    return sample

def hypothetical_fixed(pop,this_mal,a,lmbd,n,optTR,TR,qp,oqp,opt_r,j,r):
    # hypothetical spread vars
    sqp = []
    sTR = []
    h_axis = []

    x = []
    axis_len = 0

    
    #if max(this_mal.r) > 4000:
        #axis_len = 10000
    if max(this_mal.r) < opt_r:
        axis_len = int(opt_r)+int(opt_r/20)
    else:
        axis_len = max(this_mal.r)+int(max(this_mal.r)/20)
    #else:
        #axis_len = 5000

    for i in range(50,axis_len,50):
        hyp_mal = mal('hypothetical','all','fixed',[],[],[i],this_mal.c,this_mal.hc)
        hTR,hqp = econ.fixed_model(pop,hyp_mal,a,lmbd,n,0)
        sTR.append(hTR)
        if hqp > 1:
            sqp.append(1) #set upper bound of 100% pop pays
        elif hqp < 0:
            sqp.append(0) #set lower bound of 0% of pop pays
        else:
            sqp.append(hqp)
        x.append(i)

    if qp > 1:
        qp = 1 #set upper bound of 100% pop pays
    elif qp < 0:
        qp = 0 #set lower bound of 0% of pop pays

    if oqp > 1:
        oqp = 1 #set upper bound of 100% pop pays
    elif oqp < 0:
        oqp = 0 #set lower bound of 0% of pop pays

    ec = ['k','b','r','c','m','y']
    l = ['-','--','-.',':']
    m = ["o","s","D","h"]
    c = ''
    

    if this_mal.n == 'your mal':
        c = ec[0]
    elif this_mal.n == 'Locky-2017':
        c = ec[1]
    elif this_mal.n == 'zCrypt-2016':
        c = ec[2]
    elif this_mal.n == 'WannaCry-2017':
        c = ec[3]
    elif this_mal.n == 'PowerWare-2016':
        c = ec[4]
    elif this_mal.n == 'Hypothetical-CryptoWall':
        c = ec[5]
        
        
    plt.subplot(211)
    plt.xlabel('Ransom Value ($)')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue of Malware')
    plt.plot(x, sTR, color=c, ls=l[j], label=str(this_mal.n))
    plt.plot(r, TR, marker=m[j], markersize=5, color=c)
    plt.plot(opt_r, optTR, marker=m[j], markersize=5, color=c, markerfacecolor = "None")
    plt.grid(True)    
    plt.legend(fontsize='xx-small')

    plt.subplot(212)
    plt.xlabel('Ransom Value ($)')
    plt.ylabel('Proportion')
    plt.title('Proportion of Paying Population')
    plt.plot(x, sqp, color=c, ls=l[j], label=str(this_mal.n))
    plt.plot(r, qp, marker=m[j], markersize=5, color=c)
    plt.plot(opt_r, oqp, marker=m[j], markersize=5, color=c, markerfacecolor = "None")
    plt.grid(True)
    plt.legend(fontsize='xx-small')

    plt.tight_layout()
