import pandas as pd
import openpyxl
import numpy as np
from lmfit import Minimizer,Parameters, report_fit
import matplotlib.pylab as plt
import csv
import math

def perform_fitting(parameters,age, data):
    
    params_gompertz=Parameters()
    params_gompertz.add('beta_1', value=parameters[0])
    params_gompertz.add('beta_2', value=parameters[1])

    #Write down the objective function that we want to minimize, i.e., the residuals 
    def residuals_gompertz(params, x, u):
        #Get an ordered dictionary of parameter values
        v = params.valuesdict()
        #Logistic model
        model = np.exp(v['beta_1']+v['beta_2']*x)
        z=model - u
        #Return residuals
        return model - u

    # Create a minimizer object
    minner = Minimizer(residuals_gompertz, params_gompertz, fcn_args=(age, data))
    fit_gompertz = minner.minimize('leastsq')
    #Get summary of the fit
    #report_fit(fit_gompertz)

    return fit_gompertz