import math as sm
import scipy.integrate as integrate
import sympy as sm
import pandas as pd

def define_transitional_probabilities_functions (mortality_params_df_values, age, time):
    #create function, get Gompertz parameters for all diseses, get no of diseses,get X, get t return argument: pZZ and list of pZi
    #x marks the start age
    #t marks the end age

    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    const1,const2=sm.symbols("const1,const2")

    const1=sm.exp(beta_1_Z)/beta_2_Z
    const2=sm.exp(beta_1_i)/beta_2_i

    #the probabilty of staying healthy starting from age x till x+t
    pZZ=sm.exp(-const1*(sm.exp(beta_2_Z*(x+t)))-sm.exp(beta_2_Z*x)-(sigma_R+sigma_SU+sigma_MU)*t)
        #the probabilty of being ill from sickness i starting from age x till x+t - check if at all needed
    pii=sm.exp(-const1*(sm.exp(beta_2_Z*(x+t))-sm.exp(beta_2_Z*x))-const2*(sm.exp(beta_2_i*(x+t))-sm.exp(beta_2_i*x)))
    #iterate over diseses, calulcate pZi ofr each, add to list
    pZi=sm.exp(const1*sm.exp(beta_2_Z*x)*(1-beta_2_Z*t))*sm.exp(-const2*sm.exp(beta_2_i*(x+t))+const2*sm.exp(beta_2_i*(x+t/2))*(1-beta_2_i*t/2))*sigma_i/(-(sigma_R+sigma_SU+sigma_MU)+sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2)))*sm.exp((sm.exp(beta_1_i)*sm.exp(beta_2_i*(x+t/2))-(sigma_R+sigma_SU+sigma_MU))*t-1)
    #set Gomepert values to get the return pZi 
    
    transitional_probability_expressions_pii=pd.Series(dtype=str)
    transitional_probability_expressions_pZi=pd.Series(dtype=str)
    transitional_probability_expressions_pZZ=pd.Series(dtype=str)
    
    #building an auxiliary list fo keep the expressiontypes in DataFrame columns
    expressiontypes=[]
    
   

    #supstituting varibales with numerical values
    for row in mortality_params_df_values.itertuples():
        if row[0]!="ZM":
            transitional_probability_expressions_row_pii=pd.Series(data=pii.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            transitional_probability_expressions_pii=pd.concat([transitional_probability_expressions_pii,transitional_probability_expressions_row_pii], axis=0)
            expressiontypes.append("pii")
            #supstituiting sigma_i with the critical illness corresponding sigma
            if row[0]=='SU':
                pZi_sigrep=pZi.subs(sigma_i,sigma_SU)
            elif row[0]=='MU':
                pZi_sigrep=pZi.subs(sigma_i,sigma_MU)
            elif row[0]=='R':
                pZi_sigrep=pZi.subs(sigma_i,sigma_R)
            transitional_probability_expressions_row_pZi=pd.Series(data=pZi_sigrep.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_1_i,mortality_params_df_values["beta1"][row[0]]).subs(beta_2_i,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            transitional_probability_expressions_pZi=pd.concat([transitional_probability_expressions_pZi,transitional_probability_expressions_row_pZi], axis=0)
            expressiontypes.append("pZi")
        else:
            transitional_probability_expressions_pZZ=pd.Series(data=pZZ.subs(beta_2_Z,mortality_params_df_values["beta2"][row[0]]).subs(beta_1_Z,mortality_params_df_values["beta1"][row[0]]).subs(x,age).subs(t,time), index=[row[0]])
            expressiontypes.append("pZZ")

    transitional_probability_expressions_all_series=pd.concat([transitional_probability_expressions_pii,transitional_probability_expressions_pZi,transitional_probability_expressions_pZZ], axis=0)
    transitional_probability_expressions_all_df=pd.DataFrame(data={'expression':transitional_probability_expressions_all_series,'expressiontype':expressiontypes},index=transitional_probability_expressions_all_series.index)
    
    print('tpf')
    return transitional_probability_expressions_all_df
    
