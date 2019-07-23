import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel, VoigtModel
import peakutils
from peakutils.plot import plot as pplot
import glob



filenames = glob.glob('spectrum*.csv')

def find_peaks(filename,show_plots=False):  #subtract background and find peaks  
    num_samp_left = 200
    num_samp_right = 200

    data = np.genfromtxt(filename)
    x = data[:,0]
    y = data[:,1]
    x_bg = np.hstack([x[:num_samp_left],x[-num_samp_right:]])
    y_bg = np.hstack([y[:num_samp_left],y[-num_samp_right:]])
    model = LinearModel()
    params = model.guess(y_bg,x=x_bg)
    out = model.fit(y_bg,x=x_bg,params=params)
    if show_plots:
        plt.plot(x,y)
        plt.plot(x_bg,y_bg,'.')
    y_fit = out.model.func(x,**out.best_values)
    data=y-y_fit
    if show_plots:
        plt.plot(x,data)
        plt.show()
    indexes = peakutils.indexes(-data, thres=0.25, min_dist=65)
    print(indexes)
    pplot(x,data, indexes)
    peaks_x = peakutils.interpolate(x, data, ind=indexes)
    print(peaks_x)

find_peaks(filenames[5])
plt.show()