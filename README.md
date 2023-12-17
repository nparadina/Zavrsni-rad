# Zavrsni-rad: Izračun premije za osiguranje od kritičnih bolesti temeljem Markovljevog modela više stanja
# Final thesis: A multi-state Markov model for premium pricing of critical illness insurance products

## Description
The project presented here introduces a premium pricing model for critical illness insurance products. This is a final thesis project for the Postgraduate Specialist Study In Actuarial Mathematics. 
The first product is a **standalone critical illness insurance** and the second product is **critical illness insurance with term life insurance as raider**. The model is a **Markov model** of the following illnesses: stroke, cancer or heart attack, as well as in case of term insurance an added state of dead from other causes.
The insurance benefits will be payed in case of diagnosis (or sudden death if term insurance included). The model will calculate a one-of premium net value. No added risks factors or expenses are calculated. 
The model is based on Crotian Health Data in part taken directly from Croatian Institute of Public Health and Croatian Bureau of Statistics or mathematically aproximated from exiting data.
Health and populational statistical data in Croatia is sparse and hardly readily availabe in a machine readable format. To that extent the OCR-ed data is now available for further reaearch in a uploaded processed database, as described below. As the quality of data is questionable, sadly so are the model results. The results do not comply with realistic market standards. 

## Instructions on project structure, folders and files
### main.py and main_reruns.py
Both scripts are the main flow of the code. Here the data is loaded, input parameters are set, and results are presented. The difference between is that *main_reruns.py* connects to the database (MS SQLExpress) and executed a while loop recording the calculations through a preset number of iteration. On the other had *main.py* calculates a one of premium from a the set parameters, but will be used as a demo for the thesis delegation. 
Both scripts load the data from the Excel Sheets referenced as apsolute paths. In order to re-use these, the paths need to be adjusted.
### model_fitting_gompertz.py and perform_fitting.py
The script *model_fitting_gompertz.py* takes as input the calculated mortality rates and the initial guess, and calculates the parameters of the Gompertz-Makeham mortality model. These will be used further in calculation. From *model_fitting_gompertz.py* the *perform_fitting.py* script is called which uses the **lmfit Python repository** to find the GM parameters with the least mean squere error.
### transitional_probabilities_functions.py and transitional_probabilities_functions_gamma.py
The underlying functionality of both scripts is the same. Using the fitted GM parameters, starting age and and the period for which the prevalence rates apply, both scripts define the expressions. Theser expression are a tool from sympy repository. With expressions the mathematical calculations can be performed in Python using symbolic variables. The expressions will be used to describe the transitional probabilities of getting sick, dying, staying healthy or staying sick. Transitional probabilities expresssion will be used onwards with the known prevelance rates to determine the stepwise constant transitional intensities (other than mortality rate which are calculated according to GM). If additional mortality factor is included or not, either *transitional_probabilities_functions.define_transitional_probabilities_functions.py* or *transitional_probabilities_functions_gamma.define_transitional_probabilities_functions_gamma.py* is called.
### prevalence_rates_equations.py, class solve_equations_set.StepwiseProbability and calculate_probabilities.py
Function prevalence_rates_equations takes the transitional probability expressions and average prevalance rate (data is calculated as an average rate from 2001 untill 2019 per age group, loaded from Excel).
Combining the expression for transitional probability expressions, which all have step-wise constat transitional probabilities sigmas and known average prevalance rate, we create a nonlinear set of equations.
The numerical solutions to the mentioned nonlinear set of equations is calculated with **scypy's fsolve**. As a seed the fsolve, a random number will be generated within the limits provided from previos similar papers.
As a result *initial_stepwise_intensity* and *second_stepwise_intensity* are objects of a custom defined class StepwiseProbability (these Class incorporated fsolve). 
The function *calculate_probabilities.py* uses the mathematically determined transitional intensities to reverse calculate the probabilities. Only those results from fsolve are accepted that in the end result in positiv not zero transitional probabilities values (the probabilty of getting sick or dying is never negative or zero).
### determine_price_subintervals.py
Combining the information about stepwise transitional intensities and the policy parameters decided upon at the time of policy definition (starting age, duration, benefetis amount) the function determine_price returns the net premium of such a product. In order to keep thing simplerer, the benefit amount for sickness diagnosis or death is equal.
### Inijalni parametri GM Modela.xlsx, Prevalencija_Srednja_vrijednost.xlsx,Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti_gamma_0,25.xlsx, Vjerojatnost smrti populacije od kriticnih bolesti i zdravih od ostalih bolesti_gamma_0.xlsx and Product Prices and Sigmas.xlsx
These are the Excel sheets containing the input data downloaded from Croatian Instititions and adjusted for these paper. The Excel *Product Prices and Sigmas.xlsx* contains results overview of multiple iterations.
### Folder Thesis
Folder *Thesis* holds the PDF for of the thesis in Croatian
### Folder aux data; subfolder Database
Folder *aux data* hold the raw data from the Croatian institution, relevant reference papers (folder Bibliografija) and the database backup (Folder Database).
### Folder pytemp
Holds the test and helper python scripts tested and tryed out as alternatives, here still kept as possible inspiration for some continuing this work.
### Folder __pycache__ 
Is needed to use scripts as modules.
### Folder .vscode 
Automatically generated from Visual Studio Code, irrelevant to the project
### reruns_and_db_entries.py
Script *reruns_and_db_entries.py* itself irrelevant to teh project, kept as a example of database connection possibilities.
