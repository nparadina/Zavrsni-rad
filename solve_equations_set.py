
from scipy.optimize import fsolve
import sympy as sm
import prevalence_rates_equations as pre
import datetime as dt
import numpy as np
from  numpy import exp
import random

class StepwiseProbabilty:
    def __init__(self, eq_list):
        self.sigma_SU,self.sigma_MU,self.sigma_R=sm.symbols("sigma_SU,sigma_MU,sigma_R")
        self.equation_list=eq_list
        #for index in range(len(self.equation_list)):
           #self.equation_list[index]=str(self.equation_list[index])
           #self.equation_list[index]=sm.lambdify(((sigma_SU,sigma_MU,sigma_R),),self.equation_list[index])
    def equations(self,z):
        sigma_SU_lokal=z[0]
        sigma_MU_lokal=z[1]
        sigma_R_lokal=z[2]
        f=np.empty(3)
        f[0]=self.equation_list[0].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        f[1]=self.equation_list[1].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        f[2]=self.equation_list[2].subs(self.sigma_SU,sigma_SU_lokal).subs(self.sigma_MU,sigma_MU_lokal).subs(self.sigma_R,sigma_R_lokal)
        return f    
    def fsolve_stepwise(self):
        #self.myGuess=np.array([random.uniform(0, 0.01),random.uniform(0, 0.01),random.uniform(0, 0.01)])
        self.myGuess=[0.00076082, 0.00051096, 0.00394945]
        #self.myGuess=[0.00320263, 0.00210728, 0.0074981]
        #self.myGuess=[random.uniform(0, 0.01),random.uniform(0, 0.01),random.uniform(0, 0.01)]
        self.sol=np.array([0,0,0])
        self.counter=0
        #measure time to find solution
        #ct1 = dt.datetime.now()
        #print(ct1)
        self.sol=fsolve(self.equations, self.myGuess)

        while np.any(self.sol<=0):
            self.counter+=1
            self.myGuess=np.array([random.uniform(0, 0.01),random.uniform(0, 0.01),random.uniform(0, 0.01)])
            #self.myGuess=[random.uniform(0, 0.01),random.uniform(0, 0.01),random.uniform(0, 0.01)]
            self.sol= fsolve(self.equations, self.myGuess)
        #measure time to find solution
        #ct2=dt.datetime.now()
        #print(ct2-ct1)
                
        #print(self.myGuess)
        #print(self.sol)
        #print(self.counter)
       

#OLD SOLUTION WITH NSOLVE AND FUNCTION, DELETE IF FSOLVE AND CLASS WORK
# def solve_equations_set(equation_list):
#     equation_tuple=tuple(equation_list)
#     sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU", real=True)
#     #get unknow parameters
#     y0=equation_list[0]
#     y1=equation_list[1]
#     y2=equation_list[2]
#     # print(y0)
#     # print(y1)
#     # print(y2)
#     ct = dt.datetime.now()
#     print("current time:-", ct)
#     try:
#         #sol = sm.solve((y0,y1,y2),(sigma_R,sigma_SU,sigma_MU),simplify=False)
#         sol = sm.nonlinsolve([y0,y1,y2],[sigma_R,sigma_SU,sigma_MU])
#     except Exception as e:
#         print("An error in  trying to calculate teh stepwise probability")
#         print(e)
#     ct = dt.datetime.now()
#     print("current time:-", ct)
#     print(sol)
#     pass
