import math as m
import scipy.integrate as integrate
import sympy as sm
import prevalence_rates_equations as pre
import datetime as dt


def solve_equations_set(equation_list):
    equation_tuple=tuple(equation_list)
    sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU", real=True)
    #get unknow parameters
    y0=equation_list[0]
    y1=equation_list[1]
    y2=equation_list[2]
    # print(y0)
    # print(y1)
    # print(y2)
    ct = dt.datetime.now()
    print("current time:-", ct)
    try:
        #sol = sm.solve((y0,y1,y2),(sigma_R,sigma_SU,sigma_MU),simplify=False)
        sol = sm.nonlinsolve([y0,y1,y2],[sigma_R,sigma_SU,sigma_MU])
    except Exception as e:
        print(e)
    ct = dt.datetime.now()
    print("current time:-", ct)
    print(sol)
    pass
