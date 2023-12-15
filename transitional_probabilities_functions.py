import math as sm
import scipy.integrate as integrate
import sympy as sm
import pandas as pd

"""
A define_transitional_probabilities_functions takes the GM parameters,insurers age and the period the function aplies to
We have a first age group running from x0 for a t1 period (equal to age_limit_1 (aka 64)-x0)
A second age group running from x0+t1 up to final insurance age limit(105) or till the end of insurance period given in n
"""

def define_transitional_probabilities_functions (mortality_params_df_values, age, time):
    #defining symbols
    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    
    #the probabilty of staying healthy starting from age x till x+t; equations explained in the paper
    pZZ=sm.exp(-sm.exp(beta_1_Z)/beta_2_Z*(sm.exp(beta_2_Z*(x+t))-sm.exp(beta_2_Z*x))-(sigma_R+sigma_SU+sigma_MU)*t)
    #the probabilty of being ill from sickness i starting from age x till x+t
    pii=sm.exp(-sm.exp(beta_1_Z)/beta_2_Z*(sm.exp(beta_2_Z*(x+t))-sm.exp(beta_2_Z*x))-sm.exp(beta_1_i)/beta_2_i*(sm.exp(beta_2_i*(x+t))-sm.exp(beta_2_i*x)))
    #the probabilty of becomming ill from sickness i starting from age x till x+t when healty
    pZi=sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)*(1-sm.exp(beta_2_Z*t)))*sm.exp(-sm.exp(beta_1_i)/beta_2_i*sm.exp(beta_2_i*(x+t))+sm.exp(beta_1_i)/beta_2_i*sm.exp(beta_2_i*(x+t/2))*(1-beta_2_i*t/2))*sigma_i/(-(sigma_R+sigma_SU+sigma_MU)+sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2)))*sm.exp((sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2))-(sigma_R+sigma_SU+sigma_MU))*t-1)
    
    #helper for debugging
    #pZi_part1=sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)*(1-sm.exp(beta_2_Z*t)))
    #pZi_part2=sm.exp(-sm.exp(beta_1_i)/beta_2_i*sm.exp(beta_2_i*(x+t))+sm.exp(beta_1_i)/beta_2_i*sm.exp(beta_2_i*(x+t/2))*(1-beta_2_i*t/2))
    #pZi_part3=sigma_i/(-(sigma_R+sigma_SU+sigma_MU)+sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2)))
    #pZi_part4=sm.exp((sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2))-(sigma_R+sigma_SU+sigma_MU))*t-1)
    #pZZ_part1=-sm.exp(beta_1_Z)/beta_2_Z*(sm.exp(beta_2_Z*(x+t))-sm.exp(beta_2_Z*x))
    #pZZ_part2=(sigma_R+sigma_SU+sigma_MU)*t

    #helper to pretty print the expressions for debugging 
    #sm.init_printing()
    #print(pii)
    #print(sm.pretty(pZZ))
    #print(pZi)
    #sm.pprint(pZi_part1)
    #sm.pprint(pZi_part2)
    #sm.pprint(pZi_part3)
    #sm.pprint(pZi_part4)

    #temporery Series variable to help in build the dataframe
    transitional_probability_expressions_pii=pd.Series(dtype=str)
    transitional_probability_expressions_pZi=pd.Series(dtype=str)
    transitional_probability_expressions_pZZ=pd.Series(dtype=str)
    
    #building an auxiliary list fo keep the expressiontypes, used later in DataFrame to build a column
    expressiontypes=[]
    
    #supstituting varibales with numerical values
    for row in mortality_params_df_values.itertuples():
        if row[0]!="ZM": #means we are addressing one of the illness states
            #supstituting the values. Pii expression is independat of stepwise constant transitional intensities from; see paper
            transitional_probability_expressions_row_pii=pd.Series(data=pii.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            transitional_probability_expressions_pii=pd.concat([transitional_probability_expressions_pii,transitional_probability_expressions_row_pii], axis=0)
            expressiontypes.append("pii")
            #supstituiting sigma_i with the critical illness corresponding sigmas
            if row[0]=='SU':
                pZi_sigrep=pZi.subs(sigma_i,sigma_SU)
            elif row[0]=='MU':
                pZi_sigrep=pZi.subs(sigma_i,sigma_MU)
            elif row[0]=='R':
                pZi_sigrep=pZi.subs(sigma_i,sigma_R)
            transitional_probability_expressions_row_pZi=pd.Series(data=pZi_sigrep.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            
            #helper for debugging, to be deleted
            #transitional_probability_expressions_row_pZi_part1=pd.Series(data=pZi_part1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            #transitional_probability_expressions_row_pZi_part2=pd.Series(data=pZi_part2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            #transitional_probability_expressions_row_pZi_part3=pd.Series(data=pZi_part3.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            #transitional_probability_expressions_row_pZi_part4=pd.Series(data=pZi_part4.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta2"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])


            transitional_probability_expressions_pZi=pd.concat([transitional_probability_expressions_pZi,transitional_probability_expressions_row_pZi], axis=0)
            expressiontypes.append("pZi")
        else:#probability of stying healthy
            transitional_probability_expressions_pZZ=pd.Series(data=pZZ.subs(beta_2_Z,mortality_params_df_values["beta2"][row[0]]).subs(beta_1_Z,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            
            #helper for debugging
            #transitional_probability_expressions_pZZ_part1=pd.Series(data=pZZ_part1.subs(beta_2_Z,mortality_params_df_values["beta2"][row[0]]).subs(beta_1_Z,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            #transitional_probability_expressions_pZZ_part2=pd.Series(data=pZZ_part2.subs(beta_2_Z,mortality_params_df_values["beta2"][row[0]]).subs(beta_1_Z,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            
            expressiontypes.append("pZZ")

    #creating a series to hold all transitional probabilities expression 
    transitional_probability_expressions_all_series=pd.concat([transitional_probability_expressions_pii,transitional_probability_expressions_pZi,transitional_probability_expressions_pZZ], axis=0)
    #setting up expressiontypes for dataframe index
    expressiontypes.sort(reverse=True)
    #creating a dataframe out of the index
    transitional_probability_expressions_all_df=pd.DataFrame(data={'expression':transitional_probability_expressions_all_series,'expressiontype':expressiontypes},index=transitional_probability_expressions_all_series.index)

    return transitional_probability_expressions_all_df
    
