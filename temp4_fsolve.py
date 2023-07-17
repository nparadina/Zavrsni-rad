from scipy.optimize import fsolve
import numpy as np
import math
import datetime as dt

def equations(z):
    sigma_SU=z[0]
    sigma_MU=z[1]
    sigma_R=z[2]
    f=np.empty(3)
    f[0] = -0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 1.54
    f[1] = -0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.3
    f[2] =  -0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.37
    return f

myGuess=np.array([0.0000813,0.0000202,0.000384])
z=np.array([0,0,0])
counter=0

ct1 = dt.datetime.now()
print(ct1)

z=fsolve(equations, myGuess)

# while np.any(z<=0):
#     counter+=1
#     #myGuess+=0.0000001
#     myGuess=z
#     z= fsolve(equations, myGuess)

ct2=dt.datetime.now()
print(ct2-ct1)
print(z)
print(counter)
