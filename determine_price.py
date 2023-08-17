import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses

def determine_price(age_of_entry,policy_duration,initial_stepwise_intensity,second_stepwise_intensity,age_group_limits,force_of_interest,mortality_params_df_values):
    print("Entering price determination")
    
    #defining symbols
    x, delta=sm.symbols("x,delta")
    beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU=sm.symbols("beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU")
    #limits to the subintegral, determined by the age groups limits,in our case only 65 and 105. Initialize as 0 and 1, accordingly.
    hi=0
    hj=1
    #defining age interval subintegral as equation
    const=sm.exp(beta_1_Z)*sm.exp(beta_2_Z)*(x+(hj-hi)/2)
    subintegral_part1= ((sm.exp(-hi*(sigma_R+sigma_SU+sigma_MU))-sm.exp(-hj*(sigma_R+sigma_SU+sigma_MU)))*(sigma_R+sigma_SU+sigma_MU))/(sigma_R+sigma_SU+sigma_MU+const+delta)
    subintegral_part2= sm.exp((sm.exp(beta_1_Z))/beta_2_Z*(sm.exp(beta_2_Z*x))-const/beta_2_Z*(1-beta_2_Z*((hj-hi)/2)))
    subintegral=subintegral_part1*subintegral_part2
    #defining age variable for increment
    current_age=age_of_entry
    price_CI=0
    iteration=0
    print(mortality_params_df_values["beta2"]["ZM"])

    # determining the price for only CI insurance
    while iteration < (policy_duration-1):
        if current_age<age_group_limits[0]:
            price_CI=price_CI+subintegral.subs(beta_1_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest)
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
        if  current_age<age_group_limits[1] and current_age>=age_group_limits[0] :
            price_CI=price_CI+subintegral.subs(beta_1_Z,mortality_params_df_values["beta2"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest)
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
    
    print(price_CI)
    pass