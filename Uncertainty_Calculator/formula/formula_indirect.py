# -*- coding:utf-8 -*-
'''
@author: frokaikan
'''

import sympy
import numpy as np

_1,_2,_3,_4,_5,_6,_7,_8,_9,_0 = sympy.symbols('_1 _2 _3 _4 _5 _6 _7 _8 _9 _0')

class Indirect_Uncertainty:
    def __init__(self,func,data):
        self.symbols = (_1,_2,_3,_4,_5,_6,_7,_8,_9,_0)
        self.func = func
        self.xi = {}
        self.ansx = []
        self.uxi = []
        k = 0
        for da in data:
            self.xi[self.symbols[k]] = da['Mean']
            self.uxi.append(da['uc'])
            k += 1
        while len(self.uxi) < 10:
            self.uxi.append(0.0)
        
        self.mean = self.func.subs(self.xi)
        
        for var in self.symbols:
            tmp=sympy.diff(self.func,var).subs(self.xi)
            self.ansx.append(tmp*1.0)
        
        ansx_a = np.array(self.ansx,dtype=float)
        uxi_a = np.array(self.uxi,dtype=float)
        self.u = np.sum(ansx_a**2*uxi_a**2)**0.5
        
    def __str__(self):
        txt = 'Ans:\t' + format(self.mean,'0.6f') + '\nu:\t' + format(self.u,'0.6f')
        return txt

