import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel, GaussianModel


time=[]

time=np.linspace(0,1000,1000)

def gaussian(xvals,slope,shift,amp1,wid1,cen1,amp2,wid2,cen2,amp3,wid3,cen3,amp4,wid4,cen4):
    return slope*xvals+shift+(amp1*np.exp(-(xvals-cen1)**2/(wid1**2))
    	+amp2*np.exp(-(xvals-cen2)**2/(wid2**2))+amp3*np.exp(-(xvals-cen3)**2/(wid3**2))
    	+amp4*np.exp(-(xvals-cen4)**2/(wid4**2)))

spectra=gaussian(time,0.1,2,-70,50,200,-90,60,550,-150,70,700,-50,40,850)
spectra=[val+2*np.random.rand() for val in spectra]

lin_shift = LinearModel(prefix='lin_')
gmod1 = GaussianModel(prefix='g1_')
gmod2 = GaussianModel(prefix='g2_')
gmod3 = GaussianModel(prefix='g3_')
gmod4 = GaussianModel(prefix='g4_')

pars = lin_shift.make_params(intercept=2, slope=0.1)
pars += gmod1.guess(spectra, x=time)
pars += gmod2.guess(spectra, x=time)
pars += gmod3.guess(spectra, x=time)
pars += gmod4.guess(spectra, x=time)

mod = lin_shift + gmod1 + gmod2 + gmod3 + gmod4
out = mod.fit(spectra,pars, x=time)

print(out.fit_report())

plt.plot(time, spectra)
# plt.plot(time, out.init_fit,'k--')
plt.plot(time, out.best_fit,'r--')

plt.show()