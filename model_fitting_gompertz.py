#!/usr/bin/env python3 

import pandas as pd
import numpy as np
from lmfit import Minimizer,Parameters, report_fit
import matplotlib.pylab as plt
from perform_fitting import perform_fitting

#A function that takes the death probabilities per age and initial Guess to define the GM models beta_1 and beta_2 parameters

def model_fitting_gompertz(path_death_probabilities,path_initial_Gompertz_parameteres):
    #Build Dataframe Object from Excel import
    df = pd.read_excel(path_death_probabilities)
    #get the size of the available source
    mortality_data_size=df.shape
    #print(df)
    #create a 2-D transposed array to hold the data
    mortality_data=np.empty([mortality_data_size[1],mortality_data_size[0]])
    #print(mortality_data)

    #filling in the data in the array
    i=0
    for column in df:
        mortality_data[i]=df[column]
        i+=1
    #print(mortality_data)

    #control data export, to compare if transformation from df to array created any differences
    # df2=pd.DataFrame(mortality_data).T
    # df2.to_excel(excel_writer='C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/Vjerojatnost smrti oboljele populacije2.xlsx')

    #initialize array for all parameters, set initial values from Excel file
    parameters_initial_df = pd.read_excel(path_initial_Gompertz_parameteres)
    #creates a numpy array(to_numpy()) containing only the parameter values, not their indexes
    #that is why iloc[:,1:] was used-> get me all the row values, discard the indexes in column 0
    parameter_array=parameters_initial_df.iloc[:,1:].to_numpy()

    #Perform fitting for all data and all initial parameters, save outputs in results list
    #initialize results list in Minimizer Result objects
    #if betas belog to a specific illness or the general healty state is known implicitly, no index is set, keeping the result as a simple list
    minimizer_results_list=[]

    #a function to perform the fitting of beta_1 and beta_2 parameters of the GM model will be called per parameter_array row each containing the mortality per illness or general
    #mortality_data[0] contains the ages, will serve as a variable in the fitting
    #mortality_data[i+1] contains the mortality rates, will also serve as variable while fitting
    #parameter_array[i] holds the initial guess values, seed
    #the minimizer_results_list is a list with references to the MinimizerResult Objects
    for i in range(0,len(parameter_array)):
        minimizer_results_list.append(perform_fitting(parameter_array[i],mortality_data[0],mortality_data[i+1]))
    return minimizer_results_list




