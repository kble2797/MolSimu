import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import wofz


data=[]
time=[]

time=np.linspace(0,100,100)

def Voigt(x, cent, alpha, gamma, amp):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.
    """
    sigma = alpha / np.sqrt(2 * np.log(2))
    a = np.real(wofz((x - cent + 1j*gamma)/sigma/np.sqrt(2)))\
     / sigma/np.sqrt(2*np.pi)
    return a*amp

def fitting_function(x,slope, intercept,ctr1,alpha1,gamma1,amp1,ctr2,alpha2,gamma2,
	amp2,ctr3,alpha3,gamma3,amp3,ctr4,alpha4,gamma4,amp4):
	val = slope*x+intercept + Voigt(x,ctr1,alpha1,gamma1,amp1) + Voigt(x,ctr2,alpha2,gamma2,amp2)\
	+Voigt(x,ctr3,alpha3,gamma3,amp3) + Voigt(x,ctr4,alpha4,gamma4,amp4)
	return val

spectra = fitting_function(time,0.1,2, 20,3,3,-70, 45,5,5,-90, 70,2,2,-150, 85,3,3,-50)
spectra=[val+2*np.random.rand() for val in spectra]


init_vals=[0.5,2, 20,3,3,-70, 45,5,5,-90, 70,2,2,-150, 85,3,3,-50]
popt, pcov=curve_fit(fitting_function,time,spectra,p0=init_vals)

spectra_fit=fitting_function(time,*popt)

print(popt)

plt.plot(time,spectra)
plt.plot(time,spectra_fit,'r--')


plt.show()

