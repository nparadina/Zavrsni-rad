import sympy as sm

x,y,z=sm.symbols("x,y,z", real=True)
y1=sm.simplify(sm.exp(x+y+z))
y4=sm.Eq(y1,1)
y2=sm.Eq(3+y+z,0)
y3=sm.Eq(x+3*y+z,0)

#y=[y1,y2,y3]
#y=tuple(y1,y2,y3)
print(y1)
print(y4)
#print(y2)

#sol = sm.solve(y,(x,y,z))
sol1 = sm.solve((y4,y2,y3),(x,y,z))
#print(type(y))
#print(type((y1,y2,y3)))
print(sol1)
print(type(sol1))
#print(sol)
#print(type(sol))