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
pars = lin_shift.guess(spectra, x=time)

gauss1 = GaussianModel(prefix='g1_')
pars.update(gauss1.make_params())

pars['g1_center'].set(200, min=175, max=225)
pars['g1_sigma'].set(50, min=30)
pars['g1_amplitude'].set(-70, min=-100)

gauss2 = GaussianModel(prefix='g2_')
pars.update(gauss2.make_params())

pars['g2_center'].set(550, min=525, max=575)
pars['g2_sigma'].set(60, min=30)
pars['g2_amplitude'].set(-90, min=-120)

gauss3 = GaussianModel(prefix='g3_')
pars.update(gauss3.make_params())

pars['g3_center'].set(700, min=475, max=525)
pars['g3_sigma'].set(70, min=40)
pars['g3_amplitude'].set(-150, min=-200)

gauss4 = GaussianModel(prefix='g4_')
pars.update(gauss4.make_params())

pars['g4_center'].set(850, min=825, max=875)
pars['g4_sigma'].set(40, min=20)
pars['g4_amplitude'].set(-50, min=-100)

mod = lin_shift + gauss1 + gauss2 +gauss3 + gauss4
init = mod.eval(pars, x=time)
out = mod.fit(spectra,pars, x=time)

print(out.fit_report())

plt.plot(time, spectra)
# plt.plot(time, out.init_fit,'k--')
plt.plot(time, out.best_fit,'r--')

plt.show()