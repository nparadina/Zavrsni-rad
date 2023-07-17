import sympy as sm
from sympy import nsolve
from sympy import solve
import mpmath
mpmath.mp.dps = 15
sigma_R,sigma_SU,sigma_MU=sm.symbols("sigma_R,sigma_SU,sigma_MU", real=True)


f1 = -0.262617004746481*sigma_SU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499)*(0.260884896827677*sigma_MU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 1.54
f3 = -0.260884896827677*sigma_MU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555)*(0.260884896827677*sigma_MU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.3
f2 = -0.256617389979587*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797)*(0.260884896827677*sigma_MU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*sm.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.37

sol=nsolve((f1, f2,f3), (sigma_R,sigma_SU,sigma_MU), (0.0000813,0.0000202,0.000384))

print(sol)