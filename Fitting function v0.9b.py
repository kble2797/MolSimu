import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel, VoigtModel


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

spectra = fitting_function(time,0.1,2, 20,3,3,-70, 45,2,2,-90, 70,1,1,-150, 85,2,2,-60)
spectra=[val+2*np.random.rand() for val in spectra]

lin_shift = LinearModel(prefix='lin_')
pars = lin_shift.guess(spectra, x=time)

voight1 = VoigtModel(prefix='v1_')
pars.update(voight1.make_params())

pars['v1_center'].set(20)
pars['v1_sigma'].set(3)
pars['v1_gamma'].set(3)
pars['v1_amplitude'].set(-70)

voight2 = VoigtModel(prefix='v2_')
pars.update(voight2.make_params())

pars['v2_center'].set(45)
pars['v2_sigma'].set(2)
pars['v2_gamma'].set(2)
pars['v2_amplitude'].set(-90)

voight3 = VoigtModel(prefix='v3_')
pars.update(voight3.make_params())

pars['v3_center'].set(70)
pars['v3_sigma'].set(1)
pars['v3_gamma'].set(1)
pars['v3_amplitude'].set(-150)

voight4 = VoigtModel(prefix='v4_')
pars.update(voight4.make_params())

pars['v4_center'].set(85)
pars['v4_sigma'].set(2)
pars['v4_gamma'].set(2)
pars['v4_amplitude'].set(-60)

mod = lin_shift + voight1 + voight2 +voight3 + voight4
init = mod.eval(pars, x=time)
out = mod.fit(spectra,pars, x=time)

print(out.fit_report())

plt.plot(time,spectra)
plt.plot(time, out.init_fit,'k-')
plt.plot(time, out.best_fit,'r--')


plt.show()

