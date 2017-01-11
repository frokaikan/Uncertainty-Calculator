# -*- coding:utf-8 -*-
'''
@author: frokaikan
'''

#__all__=['Mean','StandardDeviation','ua','ub','uc','ans']

def Mean(*args):
    return sum(args)/len(args)
    
def StandardDeviation(*args):
    mean = Mean(*args)
    return (sum((x-mean)**2 for x in args)/(len(args)-1))**0.5
    
def ub(delta,*args):
    return delta/3**0.5
    
def ua(delta,*args):
    length = len(args)
    if length == 1:
        return ub(delta)
    n = 1/length**0.5
    return n*StandardDeviation(*args)
    
def uc(delta,*args):
    return (ua(delta,*args)**2+ub(delta)**2)**0.5
    
def ans(delta,*args):
    return Mean(*args),uc(delta,*args)

