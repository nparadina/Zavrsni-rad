import pandas as pd
import openpyxl
import numpy as np
from lmfit import Minimizer,Parameters, report_fit
import matplotlib.pylab as plt
import csv
import math

#a function to perform the fitting of beta_1 and beta_2 parameters of the GM model will be called per parameter array
#parameter_array holds the initial guess values, seed
#age contains the ages, will serve as a variable in the fitting
#data contains the mortality rates, will also serve as variable while fitting
#lmfit repository is cructial to fitting


def perform_fitting(parameters,age, data):
    
    #decklare Parameters to be fitted
    params_gompertz=Parameters()
    params_gompertz.add('beta_1', value=parameters[0])
    params_gompertz.add('beta_2', value=parameters[1])

    #Write down the objective function that we want to minimize, i.e., the residuals 
    def residuals_gompertz(params, x, u):
        #Get an ordered dictionary of parameter values
        v = params.valuesdict()
        #Logistic model
        model = np.exp(v['beta_1']+v['beta_2']*x)
        #z ist just a controled value used for debugging if neede
        #z=model - u
        #Return residuals
        return model - u

    # Create a minimizer object
    minner = Minimizer(residuals_gompertz, params_gompertz, fcn_args=(age, data))
    #calling the minimize method defined on the Minimizer object, with fitting done by least mean square error
    #fit_gompertz is an object of a MinimizerResult class, resulting by executing the minimize method on the object of type Minimizer
    fit_gompertz = minner.minimize('leastsq')
    #Get summary of the fit, used for debugging purposes if neede, chi2 value cann be found here
    #report_fit(fit_gompertz)

    return fit_gompertz