#!/usr/bin/env python3 

import pandas as pd
import openpyxl
import numpy as np
from lmfit import Minimizer,Parameters, report_fit
import matplotlib.pylab as plt
import csv
import math
from perform_fitting import perform_fitting

#Build age array
# x=list(np.arange(20,25,1))
# i=x[-1]+1
# while i<105:
#     x.extend(list(np.arange(i,i+5,1)))
#     i=x[-1]+1
# x=np.array(x)

#CSV imports OBSOLETE
#Build age array, import from csv
# with open('C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/age.csv', newline='') as csvfile:
#     data = csv.reader(csvfile,delimiter=';')
#     for row in data:
#         x=row
#     x=np.array(x, dtype='int')

#Build data array, import from csv
# with open('C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/vjerojatnost_smrti_MU.csv', newline='') as csvfile:
#     data = csv.reader(csvfile,delimiter=';')
#     for row in data:
#         u=row
#     u=np.array(u,dtype='float')

# print(u)
# print(x)

#Build Dataframe Object from Excel import
df = pd.read_excel('C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/Vjerojatnost smrti oboljele populacije.xlsx')
# print(df)
# print(df['Dob'])
# print(df['Dob'].to_numpy())

#get the size of the available source
mortality_data_size=df.shape
#create a multidimensional transposed arrayer to hold the data
mortality_data=np.empty([mortality_data_size[1],mortality_data_size[0]])
#print(mortality_data)

#filling in the data in the array
i=0
for column in df:
    mortality_data[i]=df[column]
    i+=1
#print(mortality_data)

#control data export
# df2=pd.DataFrame(mortality_data).T
# df2.to_excel(excel_writer='C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/Vjerojatnost smrti oboljele populacije2.xlsx')

#initialize array for all parameters, set initial values from Excel file
parameters_initial_df = pd.read_excel('C:/Users/nikap/Documents/Edukacija/Phyton/Zavrsni rad/Markov Model for Pricing CI insurance products/Gompertz-Makeham Model fitting/Inijalni parametri GM Modela.xlsx')
parameter_array=parameters_initial_df.iloc[:,1:].to_numpy()
#parameter_array=np.empty([parameters_initial[1],2])
#print(len(parameter_array))

#Perform fitting for all data and all initial parameters, save outputs in results list
#initialize results list if Minimizer Result objects
minimizer_results_list=[]
#print (minimizer_results_array)

for i in range(0,len(parameter_array)):
    minimizer_results_list.append(perform_fitting(parameter_array[i],mortality_data[0],mortality_data[i+1]))
    #report_fit(minimizer_results_list[i])

pass
pass



