
from scipy.optimize import fsolve
import sympy as sm
import prevalence_rates_equations as pre
import datetime as dt
import numpy as np
from  numpy import exp
import random

"""
Defines a custom object call StepwiseProbabilty. As a initialization parameter it starts with a list of a symbolic sympy list of equations
A property sol is numpy array to hold the values for the numerically fitted sigmas
Functions is the equation that will be fitted by the fsolve_stepwise function
An fsolve_stepwise function just sets up the parameters and call the fsolve module from the scipy.optimize repository
"""
class StepwiseProbabilty:
    def __init__(self, eq_list):
        self.sigma_SU,self.sigma_MU,self.sigma_R=sm.symbols("sigma_SU,sigma_MU,sigma_R")
        self.equation_list=eq_list
    def equations(self,z):
        sigma_SU_lokal=z[0]
        sigma_MU_lokal=z[1]
        sigma_R_lokal=z[2]
        f=np.empty(3)
        f[0]=self.equation_list[0].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        f[1]=self.equation_list[1].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        f[2]=self.equation_list[2].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        return f    
    def fsolve_stepwise(self, myGuess=np.array([random.uniform(1, 10),random.uniform(1, 10),random.uniform(1, 10)])):
        self.myGuess=myGuess
        print(myGuess)
        #print(self.equation_list)
        self.sol=np.array([0,0,0])
        self.counter=0
        self.sol=fsolve(self.equations, self.myGuess)

        while np.any(self.sol<=0):
            self.counter+=1
            self.myGuess=np.array([random.uniform(0.0000001, 0.00001),random.uniform(0.0000001, 0.00001),random.uniform(0.0000001, 0.00001)])
            self.sol= fsolve(self.equations, self.myGuess)

       

