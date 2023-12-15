import math as m
import random
import pandas as pd
import scipy.integrate as integrate
import sympy as sm
import numpy as np
import transitional_probabilities_functions as tp
from IPython.display import display
import solve_equations_set as ses
import calculate_probabilities as cp
#repository to return the information that an object doesn't exist
from optional import Optional


def prevalence_rates_equations (transitional_probabilities_expressions_initial_all,transitional_probabilities_expressions_second_age_group_all, average_prevalance_rates_all,CRITICAL_ILLNESSES):
     
    #initilize the symbol for prevalnce rates, will be filled with values from average_prevalance_rates_all
    f_i=sm.symbols("f_i")
    
    #Initialisation - Define initial age group symbols and variables
    pZZ_initial,pZi_initial,pii_initial=sm.symbols("pZZ_initial,pZi_initial,pii_initial")
    sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU")
    
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
    therefore creating a system of three nonlinear equations (expression class in python) with three unknown variables aka sigmas
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
    #Sympy expression is needed to be able to use "subs" method to modify values in symbolic variables
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
        
        #helper prints only for control purposes
        #sm.init_printing()
        #sm.pprint(new_exp_i)
        new_exp_i=new_exp_i.subs(f_i,average_prevalance_rates_all.at[illness,'20-64'])
        #sm.pprint(new_exp_i)
        
        #fill in eq_list_initial with new_exp_i, building the nonlinear equation set
        eq_list_initial.append(new_exp_i)
        
 
    """
    Within the while loop below, the sigmas will be fitted and accordingly the possibilities will be calculated.
    Meanining, once we have the estimated calculated sigmas of the initial age group, we can include this values into the
    equations we started from.
    In reality no negative possibilities can be found, so all fitted sigma solutions which result in negative
    posibilities must be rejected, that is why we remain in the while lop till a realistic solution is found
    
    The values of possibilities will be further used in second group calculation, if this is needed, based on
    insurance period.

    """
    #initialize flag to True, to start the while loop
    flag_NegPos=True
    while flag_NegPos:
        #instantiate the object of a custom class StepwiseProbabilty
        initialStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_initial)
        #sets a value for myGuess for debugging purposes, if commented out, a default random value will be used
        myGuess_initial=np.array([random.uniform(0.000001, 0.001),random.uniform(0.000001, 0.001),random.uniform(0.000001, 0.001)])
        #solve the nonlinear equation set and update the object with the solution
        initialStepwiseProbabilityObject.fsolve_stepwise(myGuess_initial)
        #Use sigmas to (back)calculate the pZZ value
        initial_calculated_probabilities=cp.calculate_probabilities(initialStepwiseProbabilityObject,exp_df_initial,CRITICAL_ILLNESSES)
        #helper print for debugging
        #print ("initial_calculated_probabilities.values: ", initial_calculated_probabilities.values)
        flag_NegPos=False #set the flag to Flase, if no negative values found in the iteration, the flag will remain Flase and the while loop will exit 
        for row in initial_calculated_probabilities.values:
            for elem in row:
                if (not isinstance(elem,str)):
                    fl_elem=float(elem)
                    if fl_elem<=0 and fl_elem>1:
                        flag_NegPos=True


    #helper print for debugging
    #print ("Final posibilities: ",initial_calculated_probabilities )
    
    """
    Calculating nonlinear set of equations for a second age group only makes sense 
    if the value of a input parametre transitional_probabilities_expressions_second_age_group_all isn't empty
    There for the if condition as follows; empty is an attribute, not a method

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
        #pZZ_calculated_initial is needed to get the pZZ_up_to_second_age_group
        pZZ_initial=sm.sympify(initial_calculated_probabilities.at['pZZ','pZZ'])
        pZZ_calculated_initial=pZZ_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
        pZZ_up_to_second_age_group=pZZ_calculated_initial*sm.sympify(exp_df_second_age_group.at['pZZ','pZZ'])
        second_age_group_calculated_probabilities=pd.DataFrame(columns=['pii','pZi','pZZ'])
            
        for illness in CRITICAL_ILLNESSES:
            #substitute with calculates sigmas store in sol
            pZi_calculated_initial=pZi_initial.subs(sigma_R,initialStepwiseProbabilityObject.sol[0]).subs(sigma_SU,initialStepwiseProbabilityObject.sol[1]).subs(sigma_MU,initialStepwiseProbabilityObject.sol[2])
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
        

        

        #initialize flag to True, to start the while loop
        flag_NegPos=True
        while flag_NegPos:
            #instantiate the object of a custom class StepwiseProbabilty
            secondStepwiseProbabilityObject=ses.StepwiseProbabilty(eq_list_second_age_group)
            #defalut value for myGuess for debugging purposes, if commented out, a default random value will be used
            #myGuess_second_age_group=[0.0042238,0.00865309,0.00845263]
            myGuess_second_age_group=np.array([random.uniform(0.0000001, 0.00001),random.uniform(0.0000001, 0.00001),random.uniform(0.0000001, 0.00001)])
            #myGuess_second_age_group=initialStepwiseProbabilityObject.sol
            #solve the nonlinear equation set and update the object with the solution
            secondStepwiseProbabilityObject.fsolve_stepwise(myGuess_second_age_group)
            #calculate second age group probabilties based on the second age group sigmas (aka stepwise transitional intensities) 
            #these are determined in secondStepwiseProbabilityObject
            second_age_group_calculated_probabilities=cp.calculate_probabilities(secondStepwiseProbabilityObject,exp_df_second_age_group,CRITICAL_ILLNESSES)
            #helper print for debugging
            #print ("second_age_group_calculated_probabilities.values: ", second_age_group_calculated_probabilities.values)
            flag_NegPos=False #set the flag to Flase, if no negative values found in the iteration, theflag will remain Flase and the while loop will exit 
            for row in second_age_group_calculated_probabilities.values:
                #print("Second row: ", row)
                for elem in row:
                    #print("Elem in row: ", elem, type(elem))
                    if (not isinstance(elem,str)):
                        fl_elem=float(elem)
                        #print("Elem in row not str: ", fl_elem, type(fl_elem))
                        if fl_elem<0 or fl_elem>1:
                            flag_NegPos=True

        #helper print for debugging
        #print ("Final second posibilities: ",second_age_group_calculated_probabilities )
        #helper print for debugging
        #print("Both object instantiated")
        return initialStepwiseProbabilityObject,secondStepwiseProbabilityObject, initial_calculated_probabilities, second_age_group_calculated_probabilities
    else:#second age group was never taken into consideration so a secondStepwiseProbabilityObject doesn't exist
        return initialStepwiseProbabilityObject,Optional.empty(),initial_calculated_probabilities,Optional.empty()
     
