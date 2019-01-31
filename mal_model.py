# malware generator module for finding optimal ransom based on pre-conditons
# handles fixed price ransoms
# D. Hurley-Smith, E. Cartwright, J. Hernandez-Castro, A. Stepannova 2018
import sys
import array
import string
import scipy as sp
import numpy as np

class mal:
    # defines a person whose machine that may or may not be infected
    def __init__(self, name, target_mode, price_mode, discrim_method, bands, ransom, fixed, handling):
        self.n = name
        # target types: all, target_ind, target_biz
        # all: affects whole population
        # target_ind/biz: affects only targets conforming to pop(biz)...
        # ... or pop(ind)
        self.tm = target_mode
        # price modes: fixed, discriminatory
        self.pm = price_mode
        # discrim_method: none, pop_type or price_banding
        self.dm = discrim_method
        # manually defined price bands (default to zero)
        self.bd = bands
        # ransom value
        self.r = ransom
        #fixed cost estimation
        self.c = fixed
        # handling cost per infected pop member
        self.hc = handling

    def bands(self,temp_WTP,i):
        this_WTP = [a for a in temp_WTP if (a<=i)]
        temp_WTP = [a for a in temp_WTP if (a>i)]
            
        return this_WTP,temp_WTP

    def no_intel(self,temp_WTP,sample_WTP,i):
        this_WTP = temp_WTP[i*int(len(sample_WTP)/len(self.r))
                                    :(i+1)*int(len(sample_WTP)/len(self.r))]

        return this_WTP

            
            
            

    
