import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses


def prevalence_rates_equations (transitional_probabilities_expressions_initial_all,transitional_probabilities_expressions_second_age_group_all, average_prevalance_rates_all,CRITICAL_ILLNESSES):
#Define as function, add pZZ_initial, pZi_initial list, no list argument as paramters

#Initialisation
    f_i=sm.symbols("f_i")
#Define initial symbols and variables
    pZZ_initial,pZi_initial,pii_initial=sm.symbols("pZZ_initial,pZi_initial,pii_initial")
    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    eq_list_initial=[]
    exp_df_initial=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    pZZ_initial_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
#Define second age group symbols and variables
    pZZ_second_age_group,pZi_second_age_group,pii_second_age_group=sm.symbols("pZZ_second_age_group,pZi_second_age_group,pii_second_age_group")
    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    eq_list_second_age_group=[]
    exp_df_second_age_group=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    pZZ_second_age_group_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])

#Creating an initial expression dataframe
    for illness in CRITICAL_ILLNESSES:
        for row in transitional_probabilities_expressions_initial_all.itertuples():
            if row[0]==illness:
                if row[2]=='pZi':
                    exp_df_initial.loc[len(exp_df_initial.index)]=['',row[1],'',illness]
                elif row[2]=='pii':
                    exp_df_initial.loc[len(exp_df_initial.index)]=[row[1],'','',illness]               
            elif row[2]=='pZZ' and len(pZZ_initial_temp_df.index)<1:
                    pZZ_initial_temp_df.loc[len(exp_df_initial.index)]=['','',row[1],row[2]]
    exp_df_initial=pd.concat([exp_df_initial,pZZ_initial_temp_df], ignore_index=True)
    exp_df_initial=exp_df_initial.set_index('illness')
#Creating a second age group expression dataframe
    for illness in CRITICAL_ILLNESSES:
        for row in transitional_probabilities_expressions_second_age_group_all.itertuples():
            if row[0]==illness:
                if row[2]=='pZi':
                    exp_df_second_age_group.loc[len(exp_df_second_age_group.index)]=['',row[1],'',illness]
                elif row[2]=='pii':
                    exp_df_second_age_group.loc[len(exp_df_second_age_group.index)]=[row[1],'','',illness]               
            elif row[2]=='pZZ' and len(pZZ_second_age_group_temp_df.index)<1:
                    pZZ_second_age_group_temp_df.loc[len(exp_df_second_age_group.index)]=['','',row[1],row[2]]
    exp_df_second_age_group=pd.concat([exp_df_second_age_group,pZZ_second_age_group_temp_df], ignore_index=True)
    exp_df_second_age_group=exp_df_second_age_group.set_index('illness')

#Creates an sympy equation for prevalence rate, with initial age group
    pZZ_initial=sm.sympify(exp_df_initial.at['pZZ','pZZ'])
    #a list to hold all CI pZi_initials for the sum needed in equation
    sum_pZi_initials_list=[]
    for illness in CRITICAL_ILLNESSES:
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        sum_pZi_initials_list.append(pZi_initial)
    sum_pZi_initials=sum(sum_pZi_initials_list)
    #first age group equation definition
    for illness in CRITICAL_ILLNESSES:
        # print("One: ", exp_df_initial.at[illness,'pZi'])
        # print("Two: ", exp_df_initial.at[illness,'pZi'].loc[exp_df_initial.at[illness,'pZi'].eq('')])  
        # print("Three: ", exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')])
        # print("Four: ", exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        #print(average_prevalance_rates_all.at[illness,'20-64'])
        #select the probability value from exp_df_initial that mathches the illness at location other than (~) empty (eq(''))
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        pii_initial=sm.sympify(exp_df_initial.at[illness,'pii'].loc[~exp_df_initial.at[illness,'pii'].eq('')].at[illness])
        new_exp_i=f_i-pZi_initial/(pZZ_initial+sum_pZi_initials)
        new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'20-64'])
        eq_list_initial.append(new_exp_i)
        #Back when sm.nsolve was in play and Equatoins were needed
        #eq_list_initial.append(sm.Eq(new_exp_i,0))
        
    initialStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_initial)
    initialStepwiseProbabilityObject.fsolve_stepwise()

#Using the calculated initial stepwise intensities, calculate the probabilities
    for illness in CRITICAL_ILLNESSES:
        #select the probability value from exp_df_initial that mathches the illness at location other than (~) empty (eq(''))
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        pZi_calculated_initial=pZi_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
        pZZ_calculated_initial=pZZ_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
        #pii_initial is indenpented of sigmas, however hier copied to a pii_calcualted_initial for completness
        pii_calcualted_initial=pii_initial
        pZi_second_age_group=pZi_calculated_initial*pii_calcualted_initial+pZZ_calculated_initial*pZi_calculated_initial
        pZZ_second_age_group=pZZ_calculated_initial
        
        #!!!!!!!!!!! Stala si na sagradnji equations za second_age_group
        #pZi_initial=
        eq_list_initial.append(new_exp_i)
        #Back when sm.nsolve was in play and Equatoins were needed
        #eq_list_initial.append(sm.Eq(new_exp_i,0))
    
    return initialStepwiseProbabilityObject
     
