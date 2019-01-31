# core module, providing all modes and connecting initial params to...
# ... appropriate model scenarios.
# Expect this to see a lot of expansion, particularly to tolerate user_defined...
# ... population types in the next version. 
# handles fixed price ransoms
# D. Hurley-Smith, E. Cartwright, J. Hernandez-Castro, A. Stepannova 2018
import sys
import array
import matplotlib.pyplot as plt
import math
import string
from scipy import optimize
import numpy as np
import econ_model_mod as econ
from population import population
from utilities import sample_gen, hypothetical_fixed
from mal_model import mal

def ransom_calc(usr_def_ind_WTP,usr_def_biz_WTP,target,price_model,diff_method,
                ransom,price_bands,fixed_costs,handling_costs,example):
    
    if len(usr_def_ind_WTP) > 50:
        # get and set the sample_WTP matrix
        sample_ind_WTP = usr_def_ind_WTP
    else:
        # use defaults to generate an example population
        wtp_vals = [100, 0, 250, 50, 600, 1000]
        wtp_props = [0.3,0.1,0.2,0.1,0.2,0.1]
        pop_size = 1000

        sample_ind_WTP = sample_gen(wtp_vals,pop_size,wtp_props)

    if len(usr_def_biz_WTP) > 50:
        # get and set the sample_WTP matrix
        sample_biz_WTP = usr_def_biz_WTP
    else:
        # use defaults to generate an example population
        wtp_vals = [1000, 100, 2500, 500, 6000, 1000]
        wtp_props = [0.3,0.1,0.2,0.1,0.2,0.1]
        pop_size = 100

        sample_biz_WTP = sample_gen(wtp_vals,pop_size,wtp_props)

    # misc vars
    x = []
    v = []
    v_count = []

    # generate malware (based on user input or defaults)
    # and expand all associated attributes
    if price_bands != None:
        price_bands = sorted(price_bands)
		
    #print(price_bands)
        
    this_mal = mal('your mal',target,price_model,diff_method,price_bands,ransom,fixed_costs,handling_costs)

    # pre-defined malware examples
    example_mal = []
    example_mal.append(mal('Locky-2017','all','fixed','',[''],[7500],[10000],0))
    example_mal.append(mal('zCrypt-2016','all','fixed','',[''],[500],[1000],0))
    example_mal.append(mal('WannaCry-2017','target_biz','fixed','',[''],[600],[10000],0))
    example_mal.append(mal('PowerWare-2016','target_biz','fixed','',[''],[500],[10000],0))
    example_mal.append(mal('Hypothetical-CryptoWall','all','discriminatory','pop_type',[''],[300,1500],[50000],0))
    
    c = 0
    e_n = []
    e_TR = []
    e_qp = []
    e_r = []
    e_c = []
    e_tm = []
    e_pm = []
    e_dm = []
    e_optTR = []
    e_oqp = []
    e_opt_r = []
    
    example_mal_names = []
    
    for i in example:
        if i == 'true':
            example_mal_names.append(example_mal[c].n)
            te_n,te_TR,te_qp,te_optTR,te_oqp,te_opt_r = run_model(example_mal[c],sample_ind_WTP,sample_biz_WTP)
            e_n.append(te_n)
            e_TR.append(te_TR)
            e_qp.append(te_qp)
            e_r.append(example_mal[c].r)
            e_c.append(example_mal[c].c)
            e_tm.append(example_mal[c].tm)
            e_pm.append(example_mal[c].pm)
            e_dm.append(example_mal[c].dm)
            e_optTR.append(te_optTR)
            e_oqp.append(te_oqp)
            e_opt_r.append(te_opt_r)
        c=c+1

    n,TR,qp,optTR,oqp,opt_r = run_model(this_mal,sample_ind_WTP,sample_biz_WTP)

    return n,TR,qp,optTR,oqp,opt_r,e_n,e_TR,e_qp,example_mal_names,this_mal.n,e_r,e_c,e_tm,e_pm,e_dm,e_optTR,e_oqp,e_opt_r

def run_model(this_mal,sample_ind_WTP,sample_biz_WTP):
    # if discriminatory pricing of type 'pop_type': run model with...
    # ... target differentiated params
    if this_mal.pm == "discriminatory" and this_mal.dm == "pop_type":
            
        i_n,i_TR,i_qp,i_optTR,i_oqp,i_opt_r,i_pop,i_a,i_lmbd = econ.fixed(this_mal,sample_ind_WTP,0)
        b_n,b_TR,b_qp,b_optTR,b_oqp,b_opt_r,b_pop,b_a,b_lmbd = econ.fixed(this_mal,sample_biz_WTP,1)
            
        pop = [i_pop,b_pop]
        a = [i_a,b_a]
        lmbd = [i_lmbd,b_lmbd]
        opt_r = [i_opt_r,b_opt_r]
        tqp = [i_qp,b_qp]
        toqp = [i_oqp,b_oqp]
        n = [i_n,b_n]
        
        TR = [i_TR,b_TR]
        qp = ((i_qp*i_n)+(b_qp*b_n))/(i_n+b_n)
        optTR = [i_optTR,b_optTR]
        oqp = ((i_oqp*i_n)+(b_oqp*b_n))/(i_n+b_n)

        c = 0
        for i in this_mal.r:
            hypothetical_fixed(pop[c],this_mal,a[c],lmbd[c],n[c],optTR[c],TR[c],
                           tqp[c],toqp[c],opt_r[c],c,i)
            c=c+1
            
        return n,TR,tqp,optTR,toqp,opt_r

    # if price discrimination enabled: calc price spread (unless user defined)
    elif this_mal.pm == 'discriminatory':
    # run economic model for established target settings   
        if this_mal.tm == "all":
            
            n,TR,qp,optTR,oqp,opt_r = econ.discrim(this_mal,sample_ind_WTP+sample_biz_WTP)
            
            return n,TR,qp,optTR,oqp,opt_r
            
        elif this_mal.tm == "target_ind":
            
            n,TR,qp,optPR,oqp,opt_r = econ.discrim(this_mal,sample_ind_WTP)
			
            return n,PR,qp,optTR,oqp,opt_r
                            
        elif this_mal.tm == "target_biz":
            
            n,TR,qp,optTR,oqp,opt_r = econ.discrim(this_mal,sample_biz_WTP)

            return n,TR,qp,optTR,oqp,opt_r
       
    # if fixed price enabled: immediately run economic model with...
    # ... target-appropriate params
    elif this_mal.pm == "fixed":
        
        if this_mal.tm == "all":

            n,TR,qp,optTR,oqp,opt_r,pop,a,lmbd = econ.fixed(this_mal,sample_biz_WTP+sample_ind_WTP,0)
            
            hypothetical_fixed(pop,this_mal,a,lmbd,n,optTR,TR,
                           qp,oqp,opt_r,0,this_mal.r[0])

            return n,TR,qp,optTR,oqp,opt_r
            
        elif this_mal.tm == "target_ind":
            
            n,TR,qp,optTR,oqp,opt_r,pop,a,lmbd = econ.fixed(this_mal,sample_ind_WTP,0)
            
            hypothetical_fixed(pop,this_mal,a,lmbd,n,optTR,TR,
                           qp,oqp,opt_r,0,this_mal.r[0])

            return n,TR,qp,optTR,oqp,opt_r
            
        elif this_mal.tm == "target_biz":
            
            n,TR,qp,optTR,oqp,opt_r,pop,a,lmbd = econ.fixed(this_mal,sample_biz_WTP,0)
            
            hypothetical_fixed(pop,this_mal,a,lmbd,n,optTR,TR,
                           qp,oqp,opt_r,0,this_mal.r[0])

            return n,TR,qp,optTR,oqp,opt_r
        

