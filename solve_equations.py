import math as m
import scipy.integrate as integrate
import sympy as sm
import prevalence_rates_equations as pre

index=3
count=0
equation_list=list()

#get equation per critical illness
while count<index:
    ...#get Expression
    ...#append list

equation_tuple=tuple(equation_list)

#get unknow parameters
sol = sm.solve(equation_tuple,(sm.sigma_0_R,sm.sigma_0_SU,sm.sigma_0_MU))
