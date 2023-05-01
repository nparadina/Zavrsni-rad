import math as m
import scipy.integrate as integrate
import sympy as sm

#create function, get Gompertz parameters for all diseses, get no of diseses,get X, get t return argument: pZZ and list of pZi
#x marks the start age
#t marks the end age

beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i=sm.symbols("beta_1_Z,beta_2_Z,beta_1_i,beta_2_i,x,t,sigma_R,sigma_SU,sigma_MU,sigma_i")
const1,const2=sm.symbols("const1,const2")

const1=m.exp(beta_1_Z)/beta_2_Z
const2=m.exp(beta_1_i)/beta_2_i


#the probabilty of staying healthy starting from age x till x+t
pZZ=m.exp(-const1*(m.exp(beta_2_Z*x))-m.exp(beta_2_Z*x)-(sigma_R+sigma_SU+sigma_MU)*t)
... #set Gomepert values to get the return pZZ

#the probabilty of staying ill from sickness i starting from age x till x+t - check if at all needed
pii=m.exp(-const1*(m.exp(beta_2_Z*(x+t))-m.exp(beta_2_Z*x))-const2*(m.exp(beta_2_i*(x+t))-m.exp(beta_2_i*x)))


#the probabilty of being healthy starting from age x, and being ill from sickness i at x+t

#iterate over diseses, calulcate pZi ofr each, add to list

pZi=m.exp(const1*m.exp(beta_2_Z*x)*(1-beta_2_Z*t))*m.exp(-const2*m.exp(beta_2_i*(x+t))+const2*m.exp(beta_2_i*(x+t/2))*(1-beta_2_i*t/2))*sigma_i/(-(sigma_R+sigma_SU+sigma_MU)+m.exp(beta_1_i)*m.exp(beta_2_i*(x+t/2)))*m.exp((m.exp(beta_1_i)*m.exp(beta_2_i*(x+t/2))-(sigma_R+sigma_SU+sigma_MU))*t-1)
... #set Gomepert values to get the return pZi 

#return list of pZi
