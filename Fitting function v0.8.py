import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


data=[]
time=[]

time=np.linspace(0,100,100)

def gaussian(xvals,slope,shift,amp1,wid1,cen1,amp2,wid2,cen2,amp3,wid3,cen3,amp4,wid4,cen4):
    return slope*xvals+shift+(amp1*np.exp(-(xvals-cen1)**2/(wid1**2))
    	+amp2*np.exp(-(xvals-cen2)**2/(wid2**2))+amp3*np.exp(-(xvals-cen3)**2/(wid3**2))
    	+amp4*np.exp(-(xvals-cen4)**2/(wid4**2)))

spectra=gaussian(time,0.1,2,-7,5,20,-9,6,55,-15,7,70,-5,4,85)

spectra=[val+2*np.random.rand() for val in spectra]

init_vals=[0.1,2,-7,5,20,-9,6,55,-15,7,70,-5,4,85]

popt, pcov=curve_fit(gaussian,time,spectra,p0=init_vals)

spectra_fit=gaussian(time,*popt)

print(popt)


plt.plot(time,spectra)
plt.plot(time,spectra_fit,'r--')

plt.show()