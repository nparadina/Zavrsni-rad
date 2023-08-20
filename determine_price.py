import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses

def determine_price(age_of_entry,policy_duration,initial_stepwise_intensity,second_stepwise_intensity,age_group_limits,force_of_interest,mortality_params_df_values,comp_su,comp_mu,comp_r,comp):
    print("Entering price determination")
    
    #defining symbols
    x, delta,ssu,smu,sr,s=sm.symbols("x,delta,su,smu,sr,s")
    beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU=sm.symbols("beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU")
    #limits to the CI_only_subintegral, determined by the age groups limits,in our case only 65 and 105. Initialize as 0 and 1, accordingly.
    hi=0
    hj=1
  
    #defining equations for price calculation
    #separation in subintegral parts is only in oder to make the code easier to read
    #in reality these are not subintegrals, but the solutions to the subintegrals

    #const is the same with CI stand alone product and a CI + life (risico) product
    const=sm.exp(beta_1_Z)*sm.exp(beta_2_Z)*(x+(hj-hi)/2)
    
    #CI standalone
    CI_only_subintegral_part1= ((sm.exp(-hi*(sigma_R+sigma_SU+sigma_MU+const+delta))-sm.exp(-hj*(sigma_R+sigma_SU+sigma_MU+const+delta)))*(sr*sigma_R+ssu*sigma_SU+smu*sigma_MU))/(sigma_R+sigma_SU+sigma_MU+const+delta)
    CI_only_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(hj-hi)/2))
    CI_only_subintegral=CI_only_subintegral_part1*CI_only_subintegral_part2
    
    #CI + life
    CI_life_subintegral_part1= s*((sm.exp(-hi*(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z))-sm.exp(-hj*(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z)))*(sm.exp(beta_1_Z+beta_2_Z*x)))/(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z)
    CI_life_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(hj-hi)/2))
    CI_life_subintegral=CI_life_subintegral_part1*CI_life_subintegral_part2

    #defining age variable for increment
    current_age=age_of_entry
    price_CI=0
    price_CI_life=0
    iteration=0

    #prints for debugging
    # print("Beta2:", mortality_params_df_values["beta2"]["ZM"])
    # print("Beta1:",mortality_params_df_values["beta1"]["ZM"])
    # print("Sigma1R:", initial_stepwise_intensity.sol[0])
    # print("Sigma1SU:",initial_stepwise_intensity.sol[1])
    # print("Sigma1MU:",initial_stepwise_intensity.sol[2])
    # print("Sigma2R:",second_stepwise_intensity.sol[0])
    # print("Sigma2SU:",second_stepwise_intensity.sol[1])
    # print("Sigma2MU:",second_stepwise_intensity.sol[2])
    # sum_sigmas_init=initial_stepwise_intensity.sol[0]+initial_stepwise_intensity.sol[1]+initial_stepwise_intensity.sol[2]
    # sum_sigmas_second=second_stepwise_intensity.sol[0]+second_stepwise_intensity.sol[1]+second_stepwise_intensity.sol[2]
    # print("sssuuuummmsss")
    # print("Sumsigmas1:", sum_sigmas_init)
    # print("Sumsigmas2:", sum_sigmas_second)


    # determining the price for only CI insurance
    while iteration < (policy_duration):
        if current_age<age_group_limits[0]:
            price_CI=price_CI+CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sr,comp_r).subs(ssu,comp_su).subs(smu,comp_mu)
            price_CI_life=price_CI_life+CI_life_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(s,comp)
            #prints for debugging
            # print("const: ", const.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(x,current_age))
            # print("CI_only_subintegral_part1: ",CI_only_subintegral_part1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest))
            # print( CI_only_subintegral_part2)
            # print("CI_only_subintegral_part2: ",CI_only_subintegral_part2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest))
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
        if  current_age<age_group_limits[1] and current_age>=age_group_limits[0] :
            price_CI=price_CI+CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sr,comp_r).subs(ssu,comp_su).subs(smu,comp_mu)
            price_CI_life=price_CI_life+CI_life_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(s,comp)
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
    #the price of the insurance for CI and life combined is the sum of the both components
    print(price_CI_life)
    price_CI_life=price_CI+price_CI_life
    print(price_CI)
    print(price_CI_life)
    pass