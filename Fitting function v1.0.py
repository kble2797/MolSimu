import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import wofz
import glob


def Voigt(x, cent, alpha, gamma, amp):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.
    """
    sigma = alpha / np.sqrt(2 * np.log(2))
    a = np.real(wofz((x - cent + 1j*gamma)/sigma/np.sqrt(2)))\
     / sigma/np.sqrt(2*np.pi)
    return a*amp

def fitting_function(x,slope,intercept,ctr1,alpha1,gamma1,amp1,ctr2,alpha2,gamma2,
    amp2,ctr3,alpha3,gamma3,amp3,ctr4,alpha4,gamma4,amp4):
    val = slope*x+intercept + Voigt(x,ctr1,alpha1,gamma1,amp1) + Voigt(x,ctr2,alpha2,gamma2,amp2)\
    +Voigt(x,ctr3,alpha3,gamma3,amp3) + Voigt(x,ctr4,alpha4,gamma4,amp4)
    return val


init_vals=[0.15,1.6, -1.5,0.2,0.2,-0.4, 0,0.1,0.1,-1.0, 0.75,0.3,0.3,-1.4, 1.1,0.1,0.1,-0.45]


filenames = glob.glob('spectrum*.csv')

data = np.genfromtxt(filenames[5])

x = data[:,0]
y = data[:,1]

popt, pcov = curve_fit(fitting_function, x, y,p0=init_vals, maxfev=100000)

print(*popt)

plt.show()