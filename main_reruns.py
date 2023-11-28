#!/usr/bin/env python3 

import pandas as pd
from model_fitting_gompertz import *
import numpy as np
import transitional_probabilities_functions as tpf
import transitional_probabilities_functions_gamma as tpfg
import prevalence_rates_equations as pre
import determine_price_obsolete as dp
import determine_price_subintervals as dps
import datetime as dt
import pyodbc
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select,URL
from sqlalchemy.types import Double

ct1 = dt.datetime.now()

#Setting product variables, in next iteration could be repurpused to be used as web interface
# insurable age start
x0=40
#policy duration
n=30
#insurance payments for critical illnesses, in €
sci=25000
#insurance payment in case of death to other causes, in €
s=25000

#flag and value of added mortality if used
include_added_mortality=True
gamma=0.25

#Setting data for modelling, Excel Sheets

if (not include_added_mortality):
    path_death_probabilities='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti_gamma_0.xlsx'
else:
    path_death_probabilities='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti_gamma_0,25.xlsx'

path_initial_Gompertz_parameteres='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Inijalni parametri GM Modela.xlsx'
path_prevalence_rates='C:/Users/nikap/Documents/Edukacija/Aktuarstvo/Zavrsni rad/Code Repository/Zavrsni-rad/Prevalencija_Srednja_vrijednost.xlsx'
#Setting paraemeters for transitional_probabilities_expressions

#First age group from 20-64, second age group from 65-105, age list with limit ages. As per morbidity data collected on the market
#More granular data istn+t being collected
age_group_limits=[65,105]
#t1 is time during which the prevalence rates based on the first age group collected data can be applied
if (x0+n<age_group_limits[0]):
    t1=n
else:
    t1=age_group_limits[0]-x0
#t2 is time during which the prevalence rates based on the second age group collected data can be applied
if (x0+n<age_group_limits[1]):
    if (x0+n<age_group_limits[0]):
        t2=0
    else:
        t2=x0+n-age_group_limits[0]
else:
    t2=age_group_limits[1]-age_group_limits[0]
#Setting parameters for a constant force of interest
delta=0.05
#setting insured critical illnesses - A CONSTANT
CRITICAL_ILLNESSES=['SU','MU','R']

#defining parameters of a mortality model, using 
mortality_model_parameters_labels=['beta1','beta2']
#calculating a mortality model
#get the number of inured illnesses
no_illnesses=len(CRITICAL_ILLNESSES)

#the minimizer_results_list is a list with references to the MinimizerResult Objects
minimizer_results_list=model_fitting_gompertz(path_death_probabilities,path_initial_Gompertz_parameteres)

#******Constructing a mortality model dataframe of parameters, we need to know the indexes*****
#initialize parameters list, fill it with results based retrieved from the optimisation
#mortality_params_list will  hold a list of betas
mortality_params_list=[]
for res in minimizer_results_list:
    mortality_params_list.append(res.last_internal_values)

#Creating a dataframe object to hold GM Model parameters, data stored in a list, illnesses index added based on project assumtions
critical_illnesses=CRITICAL_ILLNESSES.copy()
critical_illnesses.append("ZM") # expend the list adding the row for healthy to dead from other causes probability
mortality_params_df=pd.DataFrame(mortality_params_list,index=critical_illnesses, columns=mortality_model_parameters_labels)

print('*******Defining transitional probablities expression******')    

""" 
-using the fitted GM parameters, starting age and and the period for which the prevalence rates apply, define the expressions
-expressions are mathematically explained in the paper
-expression are a tool from sympy repository can work and perform matehmatical calculations with symbolic variables
-expressions will be used to describe the transitional probabilities of getting sick, dying, staying healthy or staying sick
-transitional probabilities expresssion will be used onwards with the known prevlance rates 
to determine the stepwise constant transitional intensities other than mortality rate calculated according to GM
--depending if additional mortality factor is included or not either tpf.define_transitional_probabilities_functions
or tpfg.define_transitional_probabilities_functions_gamma is called, see flag include_added_mortality
"""

if  not include_added_mortality:
    transitional_probabilities_expressions_initial_all=tpf.define_transitional_probabilities_functions(mortality_params_df,x0,t1)
    if t2>0:#if the insurance continues into the second age group 
        transitional_probabilities_expressions_second_age_group_all=tpf.define_transitional_probabilities_functions(mortality_params_df,x0+t1,t2)
    else:#if the insurance stops before the second age group, create the empty dataframe
        transitional_probabilities_expressions_second_age_group_all=pd.DataFrame()
else:
    transitional_probabilities_expressions_initial_all=tpfg.define_transitional_probabilities_functions_gamma(mortality_params_df,x0,t1,gamma)
    if t2>0:#if the insurance continues into the second age group 
        transitional_probabilities_expressions_second_age_group_all=tpfg.define_transitional_probabilities_functions_gamma(mortality_params_df,x0+t1,t2,gamma)
    else:#if the insurance stops before the second age group, create the empty dataframe
        transitional_probabilities_expressions_second_age_group_all=pd.DataFrame()

""" 
Load calculated data about prevalence rates
Date is calculated as an average rate from 2001 untill 2019 per age group
average_prevalance_rates_all_df= pd.DataFrame(data={'65-105':[6.51,1.10,2.63],'20-64':[1.54,0.30,0.37]}, index=CRITICAL_ILLNESSES)
""" 
average_prevalance_rates_all_df= pd.read_excel(path_prevalence_rates)
average_prevalance_rates_all_df.set_index('illness', inplace=True)

#just a helper to time execution
ct2=dt.datetime.now()
print("Time to set up for step-wise probabilties to begin calculation: ", ct2-ct1)


print('************Solving nonlinear equations***********')

#setting up database connection and counter
#run parameters
number_of_runs=100500
counter=100000

print('This will be rerun', number_of_runs, 'number of time and stored in the database')     

#connect to DB
server = 'LAPTOP-SLDJ2N3Q\SQLEXPRESS'
mydatabase = 'Critical Illness insurance'
#username = 'your_username'
#password = 'your_password'

ALCHEMY_URL = URL.create(
"mssql+pyodbc",
host=server,
database=mydatabase,
query={
    "driver": "ODBC Driver 17 for SQL Server",
},)

# Create an engine and a connection object
engine=create_engine((ALCHEMY_URL))
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database+';Trusted_Connection=yes;')
cnxn=engine.connect()
connection=engine.raw_connection()
runcon=connection.cursor()

while counter<(number_of_runs+1):

    """ 
    -Function prevalence_rates_equations takes the transitional probability expressions and average prevalance rate
    -Combinig the expression for transitional probability expressions which all have step-wise constat transitional probabilities sigmas
    and known average prevalance rate we create a nonlinear set of equations
    -The numerical solutions to the mention nonlinear set of equations is calculated with scypy's fsolve
    -As a seed the fsolve, a random number will be generated within the limits provided from previos similar papers
    -Both initial_stepwise_intensity and second_stepwise_intensity are objects of a custom defined class StepwiseProbabilty
    """ 
    ct1 = dt.datetime.now()

    initial_stepwise_intensity, second_stepwise_intensity, initial_calculated_probabilities, second_age_group_calculated_probabilities=pre.prevalence_rates_equations(transitional_probabilities_expressions_initial_all,transitional_probabilities_expressions_second_age_group_all,average_prevalance_rates_all_df,CRITICAL_ILLNESSES)

    """ 
    Combining the information in about stepwise transitional intensities
    and the parameters decided upon at the time of policy definition
    the function determine_price returns the net premium of such a product

    The mathematical beackgroup to the pricing formula is presented in the paper
    """ 
    product_price_CI, product_price_life, product_price_CI_life =dps.determine_price_subintervals(x0,n,initial_stepwise_intensity,second_stepwise_intensity,age_group_limits,delta,mortality_params_df,sci,s)

    print("Product standalon CI:", product_price_CI)
    print("Product price just life component: ", product_price_life)
    print("Product standalon CI and life component:", product_price_CI_life)

    #inserting prices in the DB
    sql_insert_prices='insert into product_prices values (?,?,?,?)'
    runcon.execute(sql_insert_prices,[float(product_price_CI), float(product_price_life),float(product_price_CI_life), counter])
    runcon.commit()

    print("initial_calculated_probabilities: ", initial_calculated_probabilities)
    print("initial sigmas:",initial_stepwise_intensity.sol)
    print(type(initial_stepwise_intensity.sol))
    
    #list sequence needed for sql execute
    initial_stepwise_intensity_list=initial_stepwise_intensity.sol.tolist()
    

    if second_stepwise_intensity.is_present():
        print("second_age_group_calculated_probabilities: ", second_age_group_calculated_probabilities)
        print("second age group sigmas: ", second_stepwise_intensity.sol)
        #list sequence needed for sql execute
        second_age_group_calculated_probabilities_list=second_stepwise_intensity.sol.tolist()
    else:
        print ("Second age group empty: ",not second_stepwise_intensity.is_present())

    for row in initial_calculated_probabilities.itertuples():
        print(row)
        print(row[0], type(row[0]))
        print(row[1], type(row[1]))
        print(row[2], type(row[2]))
        print(row[3], type(row[3]))


    ct2=dt.datetime.now()
    #timedelta converted to string for DB insert, no timedelta object is support by DB
    total_duration=str((ct2-ct1))
    sql_insert_duration='insert into duration (duration, run) values (?,?)'
    runcon.execute(sql_insert_duration,[total_duration, counter])
    runcon.commit()
    print("Time it took to find the price:", ct2-ct1)
    
    # Convert the DataFrame to a format that can be written to SQL Server. Table names and column names are constants from DB
    #If float in Python, an MS SQL column must also be declared as float
    initial_calculated_probabilities.to_sql('initial_calculated_probabilities', engine, if_exists='append', index=True, index_label='index',dtype={'pii': Double, 'pZi': Double, 'pZZ': Double} )
    sql_update_initial = 'update ' + 'initial_calculated_probabilities' +' set run= (?) WHERE run IS NULL'
    runcon.execute(sql_update_initial,counter)
    runcon.commit()

    sql_sigmas_initial='insert into initial_sigmas (sigma_SU, sigma_MU, sigma_R) values (?,?,?)'
    runcon.execute(sql_sigmas_initial,initial_stepwise_intensity_list)
    runcon.commit()

    sql_update_initial_sigmas = 'update ' + 'initial_sigmas' +' set run= (?) WHERE run IS NULL'
    runcon.execute(sql_update_initial_sigmas,counter)
    runcon.commit()

    if second_stepwise_intensity.is_present():
        second_age_group_calculated_probabilities.to_sql('second_age_group_calculated_probabilities', engine, if_exists='append', index=True, index_label='index')
        sql_update_second = 'update ' + 'second_age_group_calculated_probabilities'+' set run= (?) WHERE run IS NULL'
        runcon.execute(sql_update_second,counter)
        runcon.commit()

        sql_sigmas_second='insert into second_age_group_sigmas (sigma_SU, sigma_MU, sigma_R) values (?,?,?)'
        runcon.execute(sql_sigmas_second,second_age_group_calculated_probabilities_list)
        runcon.commit()

        sql_update_second_age_group_sigmas = 'update ' + 'second_age_group_sigmas' +' set run= (?) WHERE run IS NULL'
        runcon.execute(sql_update_second_age_group_sigmas,counter)
        runcon.commit()

    #increase run counter
    counter+=1

#close DB connection
runcon.close()
pass

