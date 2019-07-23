import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel, GaussianModel
import peakutils
from peakutils.plot import plot as pplot


time=[]

time=np.linspace(0,1000,1000)

def gaussian(xvals,slope,shift,amp1,wid1,cen1,amp2,wid2,cen2,amp3,wid3,cen3,amp4,wid4,cen4):
    return slope*xvals+shift+(amp1*np.exp(-(xvals-cen1)**2/(wid1**2))
    	+amp2*np.exp(-(xvals-cen2)**2/(wid2**2))+amp3*np.exp(-(xvals-cen3)**2/(wid3**2))
    	+amp4*np.exp(-(xvals-cen4)**2/(wid4**2)))

spectra=gaussian(time,0.1,2,-70,50,200,-90,60,550,-150,70,700,-50,40,850)

spectra=[val+2*np.random.rand() for val in spectra]

plt.plot(time,spectra)

def bg_correct(file,show_plot=False):
    num_samp_left = 50
    num_samp_right = 50
    x_bg = np.hstack([time[:num_samp_left],time[-num_samp_right:]])
    y_bg = np.hstack([file[:num_samp_left],file[-num_samp_right:]])
    mod = LinearModel()
    pars = mod.guess(y_bg, x=x_bg)
    out = mod.fit(y_bg, pars, x=x_bg)
    y_fit = out.model.func(time,**out.best_values)
    if show_plot:
        plt.plot(time, spectra)
        plt.plot(x_bg,y_bg,'.')
        plt.plot(time,y_fit,'r--')
        plt.show()
    if show_plot:
        plt.plot(time, spectra-y_fit)
        plt.show()
    data=spectra-y_fit
    return data

y=bg_correct(spectra)

indexes = peakutils.indexes(-y, thres=0.3, min_dist=100)
print(indexes)

pplot(time,y, indexes)
peaks_x = peakutils.interpolate(time, y, ind=indexes)
print(peaks_x)


plt.show()