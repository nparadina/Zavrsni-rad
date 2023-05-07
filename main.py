#!/usr/bin/env python3 

import pandas as pd
from model_fitting_gompertz import *
import numpy as np
import transitional_probabilities_functions as tpf


#Setting product variables, in next iteration could be repurpused to be used as web interface
# insurable age start
x0=20

#Setting data for modelling
path_death_probabilities='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti.xlsx'
path_initial_Gompertz_parameteres='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Inijalni parametri GM Modela.xlsx'
#Setting paraemeters for transitional_probabilities_expressions
x1=65
x2=105
t1=x1-x0
t2=x2-x1



#Setting insured's variable
#age at insurance contract
x=20
# incurance period
n=40
#insured sum, in €
S=20000
#insured critical illnesses
critical_illnesses=['SU','MU','R']
#parameters of a mortality model
mortality_model_parameters_labels=['beta1','beta2']

#calculating a mortality model
#get the number of inured illnesses
no_illnesses=len(critical_illnesses)
minimizer_results_list=model_fitting_gompertz(path_death_probabilities,path_initial_Gompertz_parameteres)

#mortality model dataframe of parameters
#initialize parameters list, fill it with results based retrieved from the optimisation
mortality_params_list=[]
for res in minimizer_results_list:
    mortality_params_list.append(res.last_internal_values)
    print(list(res.last_internal_values))

#creating a dataframe object to hold piece-wise contant transitional intensities, data stored in a list, index added based on project assumtions
critical_illnesses.append("ZM") # expend the list adding the row for healthy to dead from other causes probability
mortality_params_df=pd.DataFrame(mortality_params_list,index=critical_illnesses, columns=mortality_model_parameters_labels)

#pass the parameters to define transitional probabilities expressions
transitional_probabilities_expressions=tpf.define_transitional_probabilities_functions(mortality_params_df,x0,t1)


#piece-wise contant transition intensities dateframe
#Build dataframe from the available diseses as index of rows and colums for sigmas
#consider a nxn list as well



# call get prevalence data - database, calulate the number of unique age groups, get age boundries
#per prevalance date age group, 
    #call transitional_probabilities_functions function, get equatoins with parameters
    #call prevalence_rates_equations, get equations from prevalnce rates
    #call solve_equations, solve for sigmas
    #write sigmas to dataframe or list

#call calc premium rates 


