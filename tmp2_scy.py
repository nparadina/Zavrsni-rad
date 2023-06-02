import sympy as sm
from sympy import nsolve
from sympy import solve
import mpmath
mpmath.mp.dps = 15
sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU", real=True)

f1 = -0.356651831549143*sigma_SU*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154)*(0.356651831549143*sigma_R*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.111823828775468*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.719582172729324)) + 1.54
f3 = -0.356651831549143*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129)*(0.356651831549143*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.155401054964061*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.719582172729324)) + 0.37
f2 = 0.3 - 0.719582172729324/(0.356651831549143*sigma_R*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 9.22287914393683e-129) + 0.356651831549143*sigma_SU*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 1.8122035744266e-154) + 0.111823828775468*exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU) + 0.719582172729324

sol=nsolve((f1, f2,f3), (sigma_R,sigma_SU,sigma_MU), (0.0000813,0.0000202,0.000384))
print(sol)