import math as m
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses
#repository to return the information that an object doesn+t exist
from optional import Optional


def prevalence_rates_equations (transitional_probabilities_expressions_initial_all,transitional_probabilities_expressions_second_age_group_all, average_prevalance_rates_all,CRITICAL_ILLNESSES):
    #Define as function, add pZZ_initial, pZi_initial list, no list argument as paramters

    #Initialisation - Define initial age group symbols and variables
    f_i=sm.symbols("f_i")
    pZZ_initial,pZi_initial,pii_initial=sm.symbols("pZZ_initial,pZi_initial,pii_initial")
    beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
    #
    """
    -exp_df_initial is used to build a dataframe object containing the expression of probabilities received as input
    -exp_df_initial will be later used to build the expression per illness with inputted prevalence rates,
    therefore creating a system of three nonlinear equations (expression class in python) with three unknow variables aka sigmas
    -mathematical calcualtion is explained in the paper
    -eq_list_initial is a list used to solve the sigmas in the initial age group by solving the system of three nonlinear equations
    """
    exp_df_initial=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    eq_list_initial=[]
    #A temporary dataframe for pZZ, will be concatenated with exp_df_initial to form the final exp_df_initial
    pZZ_initial_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])

    #Initialisation - Define second age group symbols and variables
    pZZ_calculated_initial,pZi_calculated_initial,pii_calculated_initial=sm.symbols("pZZ_calculated_initial,pZi_calculated_initial,pii_calculated_initial")
    pZZ_up_to_second_age_group,pZi_up_to_second_age_group,pii_up_to_second_age_group=sm.symbols("pZZ_up_to_second_age_group,pZi_up_to_second_age_group,pii_up_to_second_age_group")

    """
    -exp_df_second_age_group is used to build a dataframe object containing the expression received as input
    -eq_list_second_age_group will be later used to build the expression per illness with inputted prevalence rates,
    therefore creating a system of three nonlinear equations (expression class in python) with three unknow variables aka sigmas
    -mathematical calcualtion is explained in the paper
    -eq_list_second_age_group is a list used to solve the sigmas in the initial age group by solving the system of three nonlinear equations
    """   
    exp_df_second_age_group=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
    eq_list_second_age_group=[]
    #A temporary dataframe for pZZ, will be concatenated with exp_df_second_age_group to form the final exp_df_second_age_group
    pZZ_second_age_group_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])

    """
    Creating an initial expression dataframe, this is just a transformation of the input attribute transitional_probabilities_expressions_initial_all
    """

    for illness in CRITICAL_ILLNESSES:
        #itertuples() returns row per row of the dateframe
        for row in transitional_probabilities_expressions_initial_all.itertuples():
            #row[0] containes index values, in this case SU,MU,R
            if row[0]==illness:
                #write a pZi expression for the illness in exp_df_initial, and prepare the illness column to be used for index
                if row[2]=='pZi':
                    exp_df_initial.loc[len(exp_df_initial.index)]=['',row[1],'',illness]
                #write a pii expression for the illness in exp_df_initial, and prepare the illness column to be used for index
                elif row[2]=='pii':
                    exp_df_initial.loc[len(exp_df_initial.index)]=[row[1],'','',illness]               
            #if row[0] doesn't contain an illness, than we are setting the expression for a healty individual to stay healthy"""
            #we only have one such probability
            #there for pZZ_initial_temp_df will have only one row, meaninig len(pZZ_initial_temp_df.index)<1
            elif row[2]=='pZZ' and len(pZZ_initial_temp_df.index)<1:
                #add this to the temporary dataframe pZZ, and set the index based on the size of exp_df_initial
                #assumming the values for pii and PZZ for the first illness were set, this index will be 2
                pZZ_initial_temp_df.loc[len(exp_df_initial.index)]=['','',row[1],row[2]]
                
    #the concatination will ignore existing indices, also the one set in elif branch
    exp_df_initial=pd.concat([exp_df_initial,pZZ_initial_temp_df], ignore_index=True)
    #new index for the complete dataframe will be set to the values in exiting illness column
    exp_df_initial=exp_df_initial.set_index('illness')

    #Creates an sympy expression (with sympy function) for prevalence rate, with initial age group; sympify converts to a Sympy object
    #Sympy expression is needed to be able to use "subs" metjod to modify values in symbolic variables
    pZZ_initial=sm.sympify(exp_df_initial.at['pZZ','pZZ'])
    
    #A sum_pZi_initials_list is a list to hold all CI pZi_initials for the sum needed in later equations in nonlinear equation set
    sum_pZi_initials_list=[]
    for illness in CRITICAL_ILLNESSES:
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        sum_pZi_initials_list.append(pZi_initial)
    #sum of all elements in sum_pZi_initials_list, the sum is a sum of symbolic expressions
    sum_pZi_initials=sum(sum_pZi_initials_list)
    
    #A loop to define the initial age group nonlinear equation set 
    for illness in CRITICAL_ILLNESSES:
        #selects the probability value from exp_df_initial that mathches the illness at location that isn+t (~) empty (eq(''))
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        pii_initial=sm.sympify(exp_df_initial.at[illness,'pii'].loc[~exp_df_initial.at[illness,'pii'].eq('')].at[illness])
        #f_i is a symbolic variable for prevalence ratem will be substituted with input values in average_prevalance_rates_all
        new_exp_i=f_i-pZi_initial/(pZZ_initial+sum_pZi_initials)
        new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'20-64'])
        #fill in eq_list_initial with new_exp_i, building the nonlinear equation set
        eq_list_initial.append(new_exp_i)
        
    #instantiate the object of a custom class StepwiseProbabilty
    initialStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_initial)
    #defalut value for myGuess for debugging purposes, if commented out, a default random value will be used
    myGuess_initial=[0.00076082, 0.00051096, 0.00394945]
    #solve the nonlinear equation set and update the object with the solution
    initialStepwiseProbabilityObject.fsolve_stepwise(myGuess_initial)
   
    """
    Once we have the estimated calculated sigmas of the initial age group, we can inclued this values into the
    equations we started from. The values will be used in second group calculation, if this is needed, based on
    insurance period. Further, the calculated values can be saved for debugging purposes

    """
    #Use sigmas to (back)calculate the pZZ value
    pZZ_calculated_initial=pZZ_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
    #This temporary dateframe object contains only pZZ, here in order to be concatenated into one df holding all calculated probabilities
    pZZ_calculated_initial_df_data=pd.DataFrame(data={"pii":'',"pZi":'',"pZZ":pZZ_calculated_initial}, index=['pZZ'])
    #Using the calculated initial stepwise intensities, build a dataframe object initial_calculated_probabilities; 
    initial_calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
    initial_calculated_probabilities=pd.concat([pZZ_calculated_initial_df_data,initial_calculated_probabilities])
    
    #looping per illness
    #TBD -- what if the values are negative, not realistic, shuld be checked and ran again?
    for illness in CRITICAL_ILLNESSES:
        #select the probability value from exp_df_initial that mathches the illness at location other than (~) empty (eq(''))
        pZi_initial=sm.sympify(exp_df_initial.at[illness,'pZi'].loc[~exp_df_initial.at[illness,'pZi'].eq('')].at[illness])
        #substitute with calculates sigmas store in sol
        pZi_calculated_initial=pZi_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
        #temporary dataframe to enable concatenation
        pZi_calculated_initial_df_data=pd.DataFrame(data={"pii":'',"pZi":pZi_calculated_initial,"pZZ":''}, index=[illness])
        initial_calculated_probabilities=pd.concat([pZi_calculated_initial_df_data,initial_calculated_probabilities])
        #pii_initial is indenpented of sigmas, therefore the same as pii_calculated_initial would be
        pii_initial=sm.sympify(exp_df_initial.at[illness,'pii'].loc[~exp_df_initial.at[illness,'pii'].eq('')].at[illness])
        pii_calculated_initial_df_data=pd.DataFrame(data={"pii":pii_initial,"pZi":'',"pZZ":''}, index=[illness])
        initial_calculated_probabilities=pd.concat([pii_calculated_initial_df_data,initial_calculated_probabilities])

    """
    Calculating nonlinear set of equations for a second age group only makes sense 
    if the value of a input parametre transitional_probabilities_expressions_second_age_group_all isn't empty
    There for the if condition as follows. empty is an attribute, not a method

    """
    #if not empty
    if  not transitional_probabilities_expressions_second_age_group_all.empty:

        """
        -exp_df_second_age_group is used to build a dataframe object containing the expression received as input
        -eq_list_second_age_group will be later used to build the expression per illness with inputted prevalence rates,
        therefore creating a system of three nonlinear equations (expression class in python) with three unknow variables aka sigmas
        -mathematical calcualtion is explained in the paper
        -eq_list_second_age_group is a list used to solve the sigmas in the initial age group by solving the system of three nonlinear equations
        """   
        exp_df_second_age_group=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])
        eq_list_second_age_group=[]
        #A temporary dataframe for pZZ, will be concatenated with exp_df_second_age_group to form the final exp_df_second_age_group
        pZZ_second_age_group_temp_df=pd.DataFrame(columns=['pii','pZi','pZZ','illness'])

        """Creating a second age group expression dataframe, just a transformation 
        of input transitional_probabilities_expressions_second_age_group_all
        needed to form the second nonlinear set of equations
        """
        for illness in CRITICAL_ILLNESSES:
            #itertuples() returns row per row of the dateframe
            for row in transitional_probabilities_expressions_second_age_group_all.itertuples():
                #row[0] containes index values, in this case SU,MU,R
                if row[0]==illness:
                    #write a pZi expression for the illness in exp_df_second_age_group, and prepare the illness column to be used for index
                    if row[2]=='pZi':
                        exp_df_second_age_group.loc[len(exp_df_second_age_group.index)]=['',row[1],'',illness]
                    #write a pii expression for the illness in exp_df_second_age_group, and prepare the illness column to be used for index
                    elif row[2]=='pii':
                        exp_df_second_age_group.loc[len(exp_df_second_age_group.index)]=[row[1],'','',illness]               
                #if row[0] doesn't contain an illness, than we are setting the expression for a healty individual to stay healthy"""
                #we only have one such probability
                #there for pZZ_second_age_group_temp_df will have only one row, meaninig len(pZZ_second_age_group_temp_df.index)<1
                elif row[2]=='pZZ' and len(pZZ_second_age_group_temp_df.index)<1:
                    #add this to the temporary dataframe pZZ, and set the index based on the size of exp_df_initial
                    #assumming the values for pii and PZZ for the first illness were set, this index will be 2
                    pZZ_second_age_group_temp_df.loc[len(exp_df_second_age_group.index)]=['','',row[1],row[2]]
        
        #the concatination will ignore existing indices, also the one set in elif branch
        exp_df_second_age_group=pd.concat([exp_df_second_age_group,pZZ_second_age_group_temp_df], ignore_index=True)
        #new index for the complete dataframe will be set to the values in exiting illness column
        exp_df_second_age_group=exp_df_second_age_group.set_index('illness')

        """
        Setting up initialization to calculate stepwise probabilities for second age group
        The calculated initial stepwise intensities and with the the calculated probabilities of the initial age group
        will be used to calculate the probabilities for the age group x0 to x2.
        The mathematical background is explained in the paper
        """
        sum_pZi_up_to_second_age_group_list=[]
        pZi_up_to_second_age_group_series=pd.Series(dtype=str)
        pZZ_up_to_second_age_group=pZZ_calculated_initial*sm.sympify(exp_df_second_age_group.at['pZZ','pZZ'])
        second_age_group_calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
            
        for illness in CRITICAL_ILLNESSES:
            #the probabilities from x0+t1 up to x0+t2 we have already calculated in exp_df_second_age_group, logic beneath calculates the x0 up to x0+t1+t2 probablity
            #mathematical background to be found in the paper
            pZi_up_to_second_age_group=pZi_calculated_initial*sm.sympify(exp_df_second_age_group.at[illness,'pii'].loc[~exp_df_second_age_group.at[illness,'pii'].eq('')].at[illness])+pZZ_calculated_initial*sm.sympify(exp_df_second_age_group.at[illness,'pZi'].loc[~exp_df_second_age_group.at[illness,'pZi'].eq('')].at[illness])
            #store the pZis in a list to calculate their sum later
            sum_pZi_up_to_second_age_group_list.append(pZi_up_to_second_age_group)
            #store the Pzis in a Series to be able to accesess them to build equations with prevalence reates
            pZi_up_to_second_age_group_series_data=pd.Series(data=pZi_up_to_second_age_group, index=[illness])
            pZi_up_to_second_age_group_series=pZi_up_to_second_age_group_series.append(pZi_up_to_second_age_group_series_data)
        
        sum_pZi_up_to_second_age=sum(sum_pZi_up_to_second_age_group_list)
            
        #second age group nonlinear equation set definition
        for illness in CRITICAL_ILLNESSES:
            new_exp_i=f_i-pZi_up_to_second_age_group_series.loc[illness]/(pZZ_up_to_second_age_group+sum_pZi_up_to_second_age)
            new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'65-105'])
            eq_list_second_age_group.append(new_exp_i)
        
        #defalut value for myGuess for debugging purposes, if commented out, a default random value will be used
        myGuess_second_age_group=[0.0042238,0.00865309,0.00845263]
        
        #instantiate the object of a custom class StepwiseProbabilty
        secondStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_second_age_group)
        #solve the nonlinear equation set and update the object with the solution
        secondStepwiseProbabilityObject.fsolve_stepwise(myGuess_second_age_group)
        
        #calculate second age group probabilties based on the second age groupsigmas (aka stepwise transitional intensities) 
        #these are determined in secondStepwiseProbabilityObject
        pZZ_second_age_group=sm.sympify(exp_df_second_age_group.at['pZZ','pZZ'])
        pZZ_calculated_second_age_group=pZZ_second_age_group.subs(sigma_R,secondStepwiseProbabilityObject.sol[0]).subs(sigma_SU,secondStepwiseProbabilityObject.sol[1]).subs(sigma_MU,secondStepwiseProbabilityObject.sol[2])
        pZZ_calculated__second_age_group_df_data=pd.DataFrame(data={"pii":'',"pZi":'',"pZZ":pZZ_calculated_second_age_group}, index=['pZZ'])
        second_age_group_calculated_probabilities=pd.concat([pZZ_calculated__second_age_group_df_data,second_age_group_calculated_probabilities])
        
        #iterate ove disease to calculate the probablities in the second age group
        for illness in CRITICAL_ILLNESSES:
            #select the probability value from exp_df_second_age_group that mathches the illness at location other than (~) empty (eq(''))
            pZi_second_age_group=sm.sympify(exp_df_second_age_group.at[illness,'pZi'].loc[~exp_df_second_age_group.at[illness,'pZi'].eq('')].at[illness])
            pZi_calculated_second_age_group=pZi_second_age_group.subs(sigma_R,secondStepwiseProbabilityObject.sol[0]).subs(sigma_SU,secondStepwiseProbabilityObject.sol[1]).subs(sigma_MU,secondStepwiseProbabilityObject.sol[2])
            pZi_calculated_second_age_group_df_data=pd.DataFrame(data={"pii":'',"pZi":pZi_calculated_second_age_group,"pZZ":''}, index=[illness])
            second_age_group_calculated_probabilities=pd.concat([pZi_calculated_second_age_group_df_data,second_age_group_calculated_probabilities])
            
            pii_second_age_group=sm.sympify(exp_df_second_age_group.at[illness,'pii'].loc[~exp_df_second_age_group.at[illness,'pii'].eq('')].at[illness])
            pii_calculated_second_age_group_df_data=pd.DataFrame(data={"pii":pii_second_age_group,"pZi":'',"pZZ":''}, index=[illness])
            second_age_group_calculated_probabilities=pd.concat([pii_calculated_second_age_group_df_data,second_age_group_calculated_probabilities])
    
        print("Both object instantiated")
        return initialStepwiseProbabilityObject,secondStepwiseProbabilityObject
    else:#second age group was never taken into consideration so a secondStepwiseProbabilityObject doesn+t exist
        return initialStepwiseProbabilityObject,Optional.empty()
     
