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
    pZZ_calculated_initial,pZi_calculated_initial,pii_calculated_initial=sm.symbols("pZZ_calculated_initial,pZi_calculated_initial,pii_calculated_initial")
    pZZ_up_to_second_age_group,pZi_up_to_second_age_group,pii_up_to_second_age_group=sm.symbols("pZZ_up_to_second_age_group,pZi_up_to_second_age_group,pii_up_to_second_age_group")
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

#Creates an sympy equation for prevalence rate, with initial age group; sympify converts to a Sympy object
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
    #defalut value for myGuess for developmnet purposes
    myGuess_initial=[0.00076082, 0.00051096, 0.00394945]
    initialStepwiseProbabilityObject.fsolve_stepwise(myGuess_initial)

#Setting initializsation to calculate stepwise probabilities for second age group
#Using the calculated initial stepwise intensities, calculate the probabilities for the age group x0 to x2. 
    sum_pZi_up_to_second_age_group_list=[]
    pZi_up_to_second_age_group_series=pd.Series(dtype=str)
    pZZ_calculated_initial=pZZ_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
    pZZ_up_to_second_age_group=pZZ_calculated_initial*sm.sympify(exp_df_second_age_group.at['pZZ','pZZ'])
#Using the calculated initial stepwise intensities, build a dataframe object initial_calculated_probabilities; to be used for evaluations of calculation 
    pZZ_calculated_initial_df_data=pd.DataFrame(data={"pii":'',"pZi":'',"pZZ":pZZ_calculated_initial}, index=['pZZ'])
#Creating a dataframe object for all probabilties, initial and second age group; to be used for evaluations of calculation 
    initial_calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
    second_age_group_calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
    initial_calculated_probabilities=pd.concat([pZZ_calculated_initial_df_data,initial_calculated_probabilities])

    for illness in CRITICAL_ILLNESSES:
        #select the probability value from exp_df_initial that mathches the illness at location other than (~) empty (eq(''))
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        pZi_calculated_initial=pZi_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
        pZi_calculated_initial_df_data=pd.DataFrame(data={"pii":'',"pZi":pZi_calculated_initial,"pZZ":''}, index=[illness])
        initial_calculated_probabilities=pd.concat([pZi_calculated_initial_df_data,initial_calculated_probabilities])
        #pii_initial is indenpented of sigmas, therefore the same as pii_calculated_initial would be
        pii_initial=sm.sympify(exp_df_initial.at[illness,'pii'].loc[~exp_df_second_age_group.at[illness,'pii'].eq('')].at[illness])
        pii_calculated_initial_df_data=pd.DataFrame(data={"pii":pii_initial,"pZi":'',"pZZ":''}, index=[illness])
        initial_calculated_probabilities=pd.concat([pii_calculated_initial_df_data,initial_calculated_probabilities])

        #the probabilities from x0+t1 up to x0+t2 we have already calculated in exp_df_second_age_group, logic beneath calculates the x0 up to x0+t1+t2 probablity
        pZi_up_to_second_age_group=pZi_calculated_initial*sm.sympify(exp_df_second_age_group.at[illness,'pii'].loc[~exp_df_second_age_group.at[illness,'pii'].eq('')].at[illness])+pZZ_calculated_initial*sm.sympify(exp_df_second_age_group.at[illness,'pZi'].loc[~exp_df_second_age_group.at[illness,'pZi'].eq('')].at[illness])
        #store the pZis in a list to calculate the sum later
        sum_pZi_up_to_second_age_group_list.append(pZi_up_to_second_age_group)
        #store the Pzis in a Series to be able to accesess them to build equations with prevalence reates
        pZi_up_to_second_age_group_series_data=pd.Series(data=pZi_up_to_second_age_group, index=[illness])
        pZi_up_to_second_age_group_series=pZi_up_to_second_age_group_series.append(pZi_up_to_second_age_group_series_data)
        
    sum_pZi_up_to_second_age=sum(sum_pZi_up_to_second_age_group_list)
        
     #second age group equation definition
    for illness in CRITICAL_ILLNESSES:
        new_exp_i=f_i-pZi_up_to_second_age_group_series.loc[illness]/(pZZ_up_to_second_age_group+sum_pZi_up_to_second_age)
        new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'65-105'])
        eq_list_second_age_group.append(new_exp_i)
    
    #defalut value for myGuess for developmnet purposes
    myGuess_second_age_group=[0.0042238,0.00865309,0.00845263]
    
    secondStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_second_age_group)
    secondStepwiseProbabilityObject.fsolve_stepwise(myGuess_second_age_group)
    
    #calculate second age group probabilties based on the sigmas (aka stepwise transitinal intensities) determined in secondStepwiseProbabilityObject
    pZZ_second_age_group=sm.sympify(exp_df_second_age_group.at['pZZ','pZZ'])
    pZZ_calculated_second_age_group=pZZ_second_age_group.subs(sigma_R,secondStepwiseProbabilityObject.sol[0]).subs(sigma_SU,secondStepwiseProbabilityObject.sol[1]).subs(sigma_MU,secondStepwiseProbabilityObject.sol[2])
    pZZ_calculated__second_age_group_df_data=pd.DataFrame(data={"pii":'',"pZi":'',"pZZ":pZZ_calculated_second_age_group}, index=['pZZ'])
    second_age_group_calculated_probabilities=pd.concat([pZZ_calculated__second_age_group_df_data,second_age_group_calculated_probabilities])
    #iterate ove disease to calculate the probablities in the second age group
    for illness in CRITICAL_ILLNESSES:
        #select the probability value from exp_df_second_age_group that mathches the illness at location other than (~) empty (eq(''))
        pZi_second_age_group=sm.sympify(exp_df_second_age_group.at[illness,'pZi'].loc[~exp_df_second_age_group.at[illness,'pZi'].eq('')].at[illness])
        pZi_calculated_second_age_group=pZi_second_age_group.subs(sigma_R,secondStepwiseProbabilityObject.sol[0]).subs(sigma_SU,secondStepwiseProbabilityObject.sol[1]).subs(sigma_MU,secondStepwiseProbabilityObject.sol[2])
        pZi_calculated_second_age_group_df_data=pd.DataFrame(data={"pii":'',"pZi":pZi_calculated_second_age_group,"pZZ":''}, index=[illness])
        second_age_group_calculated_probabilities=pd.concat([pZi_calculated_second_age_group_df_data,second_age_group_calculated_probabilities])
        pii_second_age_group=sm.sympify(exp_df_second_age_group.at[illness,'pii'].loc[~exp_df_second_age_group.at[illness,'pii'].eq('')].at[illness])
        pii_calculated_second_age_group_df_data=pd.DataFrame(data={"pii":pii_second_age_group,"pZi":'',"pZZ":''}, index=[illness])
        second_age_group_calculated_probabilities=pd.concat([pii_calculated_second_age_group_df_data,second_age_group_calculated_probabilities])
    print("I have calculated")
    return initialStepwiseProbabilityObject,secondStepwiseProbabilityObject
     
