import sympy as sm
import pandas as pd

""" 
The functions uses the mathematically determined sigmas to reverse calculate the probabilities
""" 

def calculate_probabilities (StepwiseProbabilityObject, exp_df,CRITICAL_ILLNESSES):
    sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU")
    pZZ=sm.sympify(exp_df.at['pZZ','pZZ'])
    pZZ_calculated=float(pZZ.subs(sigma_R,StepwiseProbabilityObject.sol[0]).subs(sigma_SU,StepwiseProbabilityObject.sol[1]).subs(sigma_MU,StepwiseProbabilityObject.sol[2]))
    #This temporary dateframe object contains only pZZ, here in order to be concatenated into one df holding all calculated probabilities
    pZZ_calculated_df_data=pd.DataFrame(data={"pii":'',"pZi":'',"pZZ":pZZ_calculated}, index=['pZZ']).apply(pd.to_numeric)
    #Using the calculated initial stepwise intensities, build a dataframe object initial_calculated_probabilities; 
    calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
    calculated_probabilities=pd.concat([pZZ_calculated_df_data,calculated_probabilities])
    
    #looping per illness
    for illness in CRITICAL_ILLNESSES:
    #select the probability value from exp_df_initial that mathches the illness at location other than (~) empty (eq(''))
        pZi=sm.sympify(exp_df.at[illness,'pZi'].loc[~exp_df.at[illness,'pZi'].eq('')].at[illness])
        #substitute with calculates sigmas store in sol
        pZi_calculated=float(pZi.subs(sigma_R,StepwiseProbabilityObject.sol[0]).subs(sigma_SU,StepwiseProbabilityObject.sol[1]).subs(sigma_MU,StepwiseProbabilityObject.sol[2]))
        #temporary dataframe to enable concatenation
        pZi_calculated_df_data=pd.DataFrame(data={"pii":'',"pZi":pZi_calculated,"pZZ":''}, index=[illness]).apply(pd.to_numeric)
        calculated_probabilities=pd.concat([pZi_calculated_df_data,calculated_probabilities])
        #pii_initial is indenpented of sigmas, therefore the same as pii_calculated_initial would be
        pii=float(sm.sympify(exp_df.at[illness,'pii'].loc[~exp_df.at[illness,'pii'].eq('')].at[illness]))
        pii_calculated_df_data=pd.DataFrame(data={"pii":pii,"pZi":'',"pZZ":''}, index=[illness]).apply(pd.to_numeric)
        calculated_probabilities=pd.concat([pii_calculated_df_data,calculated_probabilities])
    
    return calculated_probabilities