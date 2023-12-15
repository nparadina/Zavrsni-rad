import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig=plt.figure(1, figsize=(0.00005,0.00005))

sigma_SU = np.linspace(-5, 5)
sigma_MU = np.linspace(-5, 5)
sigma_R= np.linspace(-5, 5)

X, Y, Z = np.meshgrid(sigma_SU,sigma_MU,sigma_R)

f0 = -0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 1.54
f1 = -0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.3
f1 =  -0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/((-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797)*(0.260884896827677*sigma_MU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00170434902663555) + 0.256617389979587*sigma_R*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.00363094118807797) + 0.262617004746481*sigma_SU*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU)/(-sigma_MU - sigma_R - sigma_SU + 0.000931334226877499) + 0.719582172729324*np.exp(-45*sigma_MU - 45*sigma_R - 45*sigma_SU))) + 0.37

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, f0, cmap='viridis')


ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

plt.show()