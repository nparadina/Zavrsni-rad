import math as m
import scipy.integrate as integrate
import sympy as sm

beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x0,t1,sigma_0_R,sigma_0_SU,sigma_0_MU,sigma_0_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x0,t1,sigma_0_R,sigma_0_SU,sigma_0_MU,sigma_0_i")
const1,const2,const3,const4,const5,const6,const7,const8=sm.symbols("const1,const2,const3,const4,const5,const6,const7,const8")

const1=m.exp(beta_1_Z)/beta_2_Z
const2=m.exp(beta_1_i)/beta_2_i
const3=m.exp(beta_1_i)/beta_2_i


#the probabilty of staying healthy starting from age x0 till x0+t1
pZZ=m.exp(-const1*(m.exp(beta_2_Z*(x0+t1))-m.exp(beta_2_Z*x0))-(sigma_0_R+sigma_0_SU+sigma_0_MU)*t1)

#the probabilty of staying ill from sickness i starting from age x0 till x0+t1
pii=m.exp(-const1*(m.exp(beta_2_Z*(x0+t1))-m.exp(beta_2_Z*x0))-m.exp(beta_1_i)/beta_2_i*(m.exp(beta_2_i*(x0+t1))-m.exp(beta_2_i*x0)))

#the probabilty of being healthy starting from age x0, and being ill from sickness i at x0+t1
pZi=m.exp(-const2*m.exp(beta_2_i*(x0+t1))-const1*(m.exp(beta_2_Z*(x0+t1))-m.exp(beta_2_Z*x0))*sigma_0_i*