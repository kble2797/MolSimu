#Purpose: Numerically integrate a rate equation and plot it.

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants import k,pi,N_A
from math import e


N=500000
dt=1


path_width=65
Area=path_width**2
Temp=373.15
V=3000*3000*3000
m_Rb=1.4192261*10e-25


B=(Area/V)*np.sqrt((k*Temp)/(2*pi*m_Rb))

P0=np.exp(5.006+4.312+(-4040)/Temp)

N_1=(P0*V)/(k*Temp)

A=(N_1/V)*np.sqrt((k*Temp)/(2*pi*m_Rb))*Area


x=[0]
y=[0]


for a in range(N):
    x.append(a)
    y.append((y[-1]+B*(A/B-y[-1])*dt))

def exp_func(x,a,b,c):
	return a*(1-np.exp(-b*x))

popt,pcov=curve_fit(exp_func,x,y, p0=(1,1e-6,1))
print(popt)

xx=np.linspace(0,N,N)
yy=exp_func(xx,*popt)


# plt.plot(xx,yy,"x")
plt.plot(x,y)
plt.ylabel('Particles')
plt.xlabel('s')
plt.title('#Rb vs time')

print("Characteristic time:",1/B)

plt.show()