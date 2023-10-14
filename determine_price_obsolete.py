import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses
from optional import Optional

""" 
Combining the information in about stepwise transitional intensities
and the parameters decided upon at the time of policy definition
the function determine_price returns the net premium of such a product

We are calculated the prices of a stand alone critical illnesses insurance product and
a product that combines critical illnesses insurance and life insurance.

The mathematical beackgroup to the pricing formula is presented in the paper
""" 
def determine_price(age_of_entry,policy_duration,initial_stepwise_intensity,second_stepwise_intensity,age_group_limits,force_of_interest,mortality_params_df_values,comp_ci,comp):
    print("Entering price determination")
    print("Input parameters:")
    print("Age:", age_of_entry,"Duration:", policy_duration,initial_stepwise_intensity,second_stepwise_intensity,"age_group_limits:", age_group_limits,"force_of_interest:", force_of_interest,"mortality_params_df_values:", mortality_params_df_values,"compensations:", comp_ci,comp)
    
    #defining symbols
    x, delta,sci,s,ki,kj=sm.symbols("x,delta,sci,s,ki,kj")
    beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU=sm.symbols("beta_1_Z,beta_2_Z,sigma_R,sigma_SU,sigma_MU")
    #limits to the CI_only_subintegral, determined by the age groups limits,in our case only 65 and 105. Initialize as 0 and 1, accordingly.
    hi=0
    hj=1
  
    #defining equations for price calculation
    #separation in subintegral parts is only in order to make the code easier to read
    #in reality these are not subintegrals, but the solutions to the subintegrals
    #see paper for the pricing formula

    #const is the same with CI stand alone product and a CI + life (risico) product
    #const=sm.exp(beta_1_Z)*sm.exp(beta_2_Z)*(x+(kj-ki)/2)
    const=sm.exp(beta_1_Z)*sm.exp(beta_2_Z)*(x+(kj+ki)/2)
    #CI standalone product
    CI_only_subintegral_part1= ((sm.exp(-ki*(sigma_R+sigma_SU+sigma_MU+const+delta))-sm.exp(-kj*(sigma_R+sigma_SU+sigma_MU+const+delta)))*(sigma_R+sigma_SU+sigma_MU))/(sigma_R+sigma_SU+sigma_MU+const+delta)
    CI_only_subintegral_part1_1=(sm.exp(-ki*(sigma_R+sigma_SU+sigma_MU+const+delta))-sm.exp(-kj*(sigma_R+sigma_SU+sigma_MU+const+delta)))
    CI_only_subintegral_part1_1_1=sm.exp(-ki*(sigma_R+sigma_SU+sigma_MU+const+delta))
    CI_only_subintegral_part1_1_2=sm.exp(-kj*(sigma_R+sigma_SU+sigma_MU+const+delta))
    CI_only_subintegral_part1_2=(sigma_R+sigma_SU+sigma_MU)/(sigma_R+sigma_SU+sigma_MU+const+delta)
    #CI_only_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(kj-ki)/2))
    CI_only_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(kj+ki)/2))
    CI_only_subintegral=sci*CI_only_subintegral_part1*CI_only_subintegral_part2
    
    #CI + life product
    CI_life_subintegral_part1= s*((sm.exp(-ki*(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z))-sm.exp(-kj*(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z)))*(sm.exp(beta_1_Z+beta_2_Z*x)))/(sigma_R+sigma_SU+sigma_MU+const+delta-beta_2_Z)
    #CI_life_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(kj-ki)/2))
    CI_life_subintegral_part2= sm.exp(sm.exp(beta_1_Z)/beta_2_Z*sm.exp(beta_2_Z*x)-const/beta_2_Z*(1-beta_2_Z*(kj+ki)/2))
    CI_life_subintegral=CI_life_subintegral_part1*CI_life_subintegral_part2

    #defining age variable for increment
    current_age=age_of_entry
    price_CI=0
    price_CI_life=0
    iteration=0

    #prints for debugging
    print("Beta2:", mortality_params_df_values["beta2"]["ZM"])
    print("Beta1:",mortality_params_df_values["beta1"]["ZM"])
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



    # determining the price for all products
    while iteration < (policy_duration):
        if current_age<age_group_limits[0]:
            #const
            print("Const: ", const.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(x,current_age).subs(ki,hi).subs(kj,hj))
            #stand alone CI
            print("Price Ci prior the iteration: ",iteration, " is ",price_CI )
            price_CI=price_CI+CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sci,comp_ci).subs(ki,hi).subs(kj,hj)
            print("Price Ci after the iteration: ",iteration, " is ",price_CI )
            #life component of a product combining CI and life
            print("Price Ci_life prior the iteration: ",iteration, " is ",price_CI_life)
            price_CI_life=price_CI_life+CI_life_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(s,comp).subs(ki,hi).subs(kj,hj)
            print("Price Ci_life after the iteration: ",iteration, " is ",price_CI_life)
            #prints for debugging
            # print("const: ", const.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(x,current_age))
            print("CI_only_subintegral_part1: ",CI_only_subintegral_part1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            # print( CI_only_subintegral_part2)
            print("CI_only_subintegral_part2: ",CI_only_subintegral_part2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_whole: ", CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,initial_stepwise_intensity.sol[0]).subs(sigma_SU,initial_stepwise_intensity.sol[1]).subs(sigma_MU,initial_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sci,comp_ci).subs(ki,hi).subs(kj,hj))
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
        """
        To even take into the account the second age group "cost" the insurers age has to be above the second age group limit
        but not higher than the overall last supšport age, her 105
        Also the length of the insurance period and the starting age determine if the second age group probabilities 
        even play a part in the calculation
        When no second age group probabilties were calcualted the second_stepwise_intensity object is empty
        """
        if  current_age<age_group_limits[1] and current_age>=age_group_limits[0] and type(second_stepwise_intensity)!="Optional.empty()":
            #const
            print("I+m in a second loop, number", iteration)

            print("Const: ", const.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(x,current_age).subs(ki,hi).subs(kj,hj))
            print("CI_only_subintegral_part1: ",CI_only_subintegral_part1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_only_subintegral_part1_1: ",CI_only_subintegral_part1_1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_only_subintegral_part1_2: ",CI_only_subintegral_part1_2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_only_subintegral_part1_1_1: ",CI_only_subintegral_part1_1_1.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_only_subintegral_part1_1_2: ",CI_only_subintegral_part1_1_2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            # print( CI_only_subintegral_part2)
            print("CI_only_subintegral_part2: ",CI_only_subintegral_part2.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(ki,hi).subs(kj,hj))
            print("CI_whole+++++++++++++++++: ", CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sci,comp_ci).subs(ki,hi).subs(kj,hj))
            print("Price Ci prior the iteration: ",iteration, " is ",price_CI )
            price_CI=price_CI+CI_only_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(sci,comp_ci).subs(ki,hi).subs(kj,hj)
            print("Price Ci after the iteration: ",iteration, " is ",price_CI )
            print("Price Ci_life prior the iteration: ",iteration, " is ",price_CI_life)
            price_CI_life=price_CI_life+CI_life_subintegral.subs(beta_1_Z,mortality_params_df_values["beta1"]["ZM"]).subs(beta_2_Z,mortality_params_df_values["beta2"]["ZM"]).subs(sigma_R,second_stepwise_intensity.sol[0]).subs(sigma_SU,second_stepwise_intensity.sol[1]).subs(sigma_MU,second_stepwise_intensity.sol[2]).subs(x,current_age).subs(delta,force_of_interest).subs(s,comp).subs(ki,hi).subs(kj,hj)
            print("Price Ci_life after the iteration: ",iteration, " is ",price_CI_life)
            print("current age, hi, hj",current_age,hi,hj)
            hi=hi+1
            hj=hj+1
            current_age=current_age+1
            iteration=iteration+1
    
    #the price of the insurance for CI and life combined is the sum of the both components
    # print(price_CI)
    # print(price_CI_life)
    # print(price_CI+price_CI_life)

    return price_CI, price_CI_life, price_CI+price_CI_life
