#!/usr/bin/env python3 

import pandas as pd
from model_fitting_gompertz import *
import numpy as np
import transitional_probabilities_functions as tpf
import prevalence_rates_equations as pre


#Setting product variables, in next iteration could be repurpused to be used as web interface
# insurable age start
x0=20

#Setting data for modelling
path_death_probabilities='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti.xlsx'
path_initial_Gompertz_parameteres='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Inijalni parametri GM Modela.xlsx'
#Setting paraemeters for transitional_probabilities_expressions
#Number of age groups, agegroupsno
agegroupsno=2
#First age group from 20-64, second age group from 65-105, age list with limit ages
age=[65,105]
t1=age[0]-x0
t2=age[1]-age[0] 



#Setting insured's variable
#age at insurance contract
x=20
# incurance period
n=40
#insured sum, in €
S=20000
#insured critical illnesses - A CONSTANT
CRITICAL_ILLNESSES=['SU','MU','R']
#parameters of a mortality model
mortality_model_parameters_labels=['beta1','beta2']

#calculating a mortality model
#get the number of inured illnesses
no_illnesses=len(CRITICAL_ILLNESSES)
minimizer_results_list=model_fitting_gompertz(path_death_probabilities,path_initial_Gompertz_parameteres)



#mortality model dataframe of parameters
#initialize parameters list, fill it with results based retrieved from the optimisation
mortality_params_list=[]
for res in minimizer_results_list:
    mortality_params_list.append(res.last_internal_values)
    #print(list(res.last_internal_values))

#creating a dataframe object to hold piece-wise contant transitional intensities, data stored in a list, index added based on project assumtions
critical_illnesses=CRITICAL_ILLNESSES.copy()
critical_illnesses.append("ZM") # expend the list adding the row for healthy to dead from other causes probability
mortality_params_df=pd.DataFrame(mortality_params_list,index=critical_illnesses, columns=mortality_model_parameters_labels)

print('Here1')    
transitional_probabilities_expressions_all=tpf.define_transitional_probabilities_functions(mortality_params_df,x0,t1)

#dummy test data
average_prevalance_rates_all_df= pd.DataFrame(data={'65-105':[6.51,1.10,2.63],'20-64':[1.54,0.30,0.37]}, index=CRITICAL_ILLNESSES)
#pass the parameters to define transitional probabilities expressions

print('Here2')    
print(pre.prevalence_rates_equations(transitional_probabilities_expressions_all,average_prevalance_rates_all_df,CRITICAL_ILLNESSES))

pass

#piece-wise contant trans

# call get prevalence data - database, calulate the number of unique age groups, get age boundries
#per prevalance date age group, 
    #call transitional_probabilities_functions function, get equatoins with parameters
    #call prevalence_rates_equations, get equations from prevalnce rates
    #call solve_equations, solve for sigmas
    #write sigmas to dataframe or list

#call calc premium rates 


