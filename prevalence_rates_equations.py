import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses


def prevalence_rates_equations (transitional_probability_expressions_all, average_prevalance_rates_all,CRITICAL_ILLNESSES):
#Define as function, add pZZ, pZi list, no list argument as paramters
    f_i=sm.symbols("f_i")
    pZZ,pZi,pii=sm.symbols("pZZ,pZi,pii")
    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    eq_list=[]
    exp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    pZZ_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    for illness in CRITICAL_ILLNESSES:
        for row in transitional_probability_expressions_all.itertuples():
            if row[0]==illness:
                if row[2]=='pZi':
                    exp_df.loc[len(exp_df.index)]=['',row[1],'',illness]
                elif row[2]=='pii':
                    exp_df.loc[len(exp_df.index)]=[row[1],'','',illness]               
            elif row[2]=='pZZ' and len(pZZ_temp_df.index)<1:
                    pZZ_temp_df.loc[len(exp_df.index)]=['','',row[1],row[2]]
    exp_df=pd.concat([exp_df,pZZ_temp_df], ignore_index=True)
    exp_df=exp_df.set_index('illness')
    

    #Creates an sympy equation for prevalence rate
    pZZ=sm.sympify(exp_df.at['pZZ','pZZ'])
    #a list to hold all CI pZis for the sum needed in equation
    sum_pZis_list=[]
    for illness in CRITICAL_ILLNESSES:
        pZi=sm.sympify(exp_df.at[illness,'pZi'].loc[~exp_df.at[illness,'pZi'].eq('')].at[illness])
        sum_pZis_list.append(pZi)
    sum_Pzis=sum(sum_pZis_list)
    for illness in CRITICAL_ILLNESSES:
        #print(exp_df.at[illness,'pZi'].loc[~exp_df.at[illness,'pZi'].eq('')])
        #print(exp_df.at[illness,'pZi'].loc[~exp_df.at[illness,'pZi'].eq('')].at[illness])
        #print(average_prevalance_rates_all.at[illness,'20-64'])
        pZi=sm.sympify(exp_df.at[illness,'pZi'].loc[~exp_df.at[illness,'pZi'].eq('')].at[illness])
        pii=sm.sympify(exp_df.at[illness,'pii'].loc[~exp_df.at[illness,'pii'].eq('')].at[illness])
        new_exp_i=f_i-pZi/(pZZ+sum_Pzis)
        new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'20-64'])
        eq_list.append(new_exp_i)
        #Back when sm.nsolve was in play and Equatoins were needed
        #eq_list.append(sm.Eq(new_exp_i,0))
    print('pre')
    initialStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list)
    initialStepwiseProbabilityObject.fsolve_stepwise()
    
    return initialStepwiseProbabilityObject
     
