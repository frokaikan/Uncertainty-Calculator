# -*- coding:utf-8 -*-
'''
@author: frokaikan
'''

from scipy.optimize import leastsq
import numpy as np

class fit:
    def __init__(self,datax,datay):
        self.datax = np.array(datax)
        self.datay = np.array(datay)

    def func(self,x,params):
        k,b = params
        return k*x+b
    
    def diff(self,params,datay,datax):
        return datay - self.func(datax,params)
        
    def calc_fit(self,init_value=(1,1)):
        self.ans = leastsq(self.diff,init_value,args=(self.datay,self.datax))
        return self.ans[0]
        
    def __call__(self,init_value=None):
        if not init_value:
            return self.calc_fit()
        else:
            return self.calc_fit(init_value)
            
