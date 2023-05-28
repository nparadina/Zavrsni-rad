from scipy.optimize import fsolve
import numpy as np
import math
import datetime as dt

def equations(z):
    sigma_SU=z[0]
    sigma_MU=z[1]
    sigma_R=z[2]
    f=np.empty(3)
    f[0] = -0.356651831549143*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154)*(0.356651831549143*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.155401054964061*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.719582172729324)) + 1.54
    f[1] = -0.356651831549143*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129)*(0.356651831549143*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.155401054964061*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.719582172729324)) + 0.37
    f[2] = 0.3 - 0.719582172729324/(0.356651831549143*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.155401054964061*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.71958217272932
    return f

myGuess=np.array([0.0000813,0.0000202,0.000384])
z=np.array([0,0,0])
counter=0

ct1 = dt.datetime.now()
print(ct1)

while np.any(z<=0):
    counter+=1
    z= fsolve(equations, myGuess)

ct2=dt.datetime.now()
print(ct2-ct1)
print(z)
print(counter)
