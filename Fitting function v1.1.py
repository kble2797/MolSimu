import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import PolynomialModel, VoigtModel
import pandas as pd
from scipy.special import wofz,erf
from scipy.optimize import curve_fit
import peakutils
from peakutils.plot import plot as pplot


data=pd.read_csv('data.csv')

x_raw = data.iloc[:,0]
y_raw = data.iloc[:,1]

x = np.hstack([x_raw[:370],x_raw[425:775],x_raw[-250:]])
y = np.hstack([y_raw[:370],y_raw[425:775],y_raw[-250:]])

raw=pd.read_csv('data.csv')

x1 = raw.iloc[:,0]
y1 = raw.iloc[:,1]

shift = PolynomialModel(2,prefix='Poly_')
pars = shift.guess(y, x=x)


voight1 = VoigtModel(prefix='v1_')
pars.update(voight1.make_params())
pars['v1_center'].set(0)
pars['v1_sigma'].set(0.005)
pars['v1_gamma'].set(0.005)
pars['v1_amplitude'].set(-0.3)


voight2 = VoigtModel(prefix='v2_')
pars.update(voight2.make_params())
pars['v2_center'].set(0.02)
pars['v2_sigma'].set(0.005)
pars['v2_gamma'].set(0.005)
pars['v2_amplitude'].set(-0.2)


model = shift + voight1 + voight2
out = model.fit(y,x=x,params=pars)

out.plot(datafmt='g-',fitfmt='r--')
plt.plot(x1,y1)
plt.show()

def Voigt(x,amplitude,center,sigma,gamma):
    z=(x-center+1j*gamma)/(sigma*np.sqrt(2))
    w=wofz(z)
    f = (amplitude*np.real(w))/(sigma*np.sqrt(2*np.pi))
    return f


def Sum_of_Voigts(x,v2_sigma,v2_center,v2_amplitude,v2_gamma,
    v1_sigma,v1_center,v1_amplitude,v1_gamma,Poly_c0,Poly_c1,Poly_c2):
    val = Poly_c0 + Poly_c1*x + Poly_c2*(x**2) + Voigt(x,v1_amplitude,v1_center,v1_sigma,v1_gamma)\
     +Voigt(x,v2_amplitude,v2_center,v2_sigma,v2_gamma)
    return val

# print(out.best_values)

y_fit=Sum_of_Voigts(x_raw,**out.best_values)

plt.plot(x1,y_fit)
plt.plot(x1,y1)
plt.show()

indexes = peakutils.indexes(-y_fit)

print(indexes)
print(x[indexes])
print(y[indexes])
pplot(x1, y_fit, indexes)
plt.show()

#D2: 384.230 484 468 5(62) THz
#D1: 377.107 463 5(4) THz

Rb_peaks=np.array([377.10746354,384.2304844685])
print(Rb_peaks)

def peaks_calibrate(x,c0,c1):
	return c1*x+c0

init_vals=[377.71,286.64]

popt, pcov = curve_fit(peaks_calibrate,x[indexes],Rb_peaks,p0=init_vals)
print(popt)

x_freq=peaks_calibrate(x1,*popt)

plt.plot(x_freq,y1)
plt.plot(x_freq,y_fit)
plt.xlabel('THz')
plt.ylabel('Signal')
plt.show()