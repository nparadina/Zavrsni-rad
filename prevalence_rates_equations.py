import math as m
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp

#Define as function, add pZZ, pZi list, no list argument as paramters
arg_pZi=0
arg_pZZ=0
arg_pZi=0

f_i=sm.symbols("f_i")


#Creates an sympy equation for prevalence rate 
eq=sm.Eq(f_i-tp.pZi/(tp.pZZ+tp.pZi))

eq_res=eq.subs(tp.pZi,)