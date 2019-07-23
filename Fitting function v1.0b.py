import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel, VoigtModel
import peakutils
from peakutils.plot import plot as pplot
import glob


filenames = glob.glob('spectrum*.csv')

def fitting(filename):
    data = np.genfromtxt(filename)
    x = data[:,0]
    y = data[:,1]
    lin_shift = LinearModel(prefix='lin_')
    pars = lin_shift.guess(y, x=x)

    voight1 = VoigtModel(prefix='v1_')
    pars.update(voight1.make_params())

    pars['v1_center'].set(-0.65)
    pars['v1_sigma'].set(0.1)
    pars['v1_gamma'].set(0.1)
    pars['v1_amplitude'].set(-0.4)

    voight2 = VoigtModel(prefix='v2_')
    pars.update(voight2.make_params())

    pars['v2_center'].set(0)
    pars['v2_sigma'].set(0.1)
    pars['v2_gamma'].set(0.1)
    pars['v2_amplitude'].set(-1.0)

    voight3 = VoigtModel(prefix='v3_')
    pars.update(voight3.make_params())

    pars['v3_center'].set(0.75)
    pars['v3_sigma'].set(0.5)
    pars['v3_gamma'].set(0.5)
    pars['v3_amplitude'].set(-1.4)

    voight4 = VoigtModel(prefix='v4_')
    pars.update(voight4.make_params())

    pars['v4_center'].set(1.1)
    pars['v4_sigma'].set(0.15)
    pars['v4_gamma'].set(0.15)
    pars['v4_amplitude'].set(-0.6)

    mod = lin_shift + voight1 + voight2 +voight3 + voight4
    init = mod.eval(pars, x=x)
    out = mod.fit(y,pars, x=x)
    y_fit = out.model.func(x,**out.best_values)

    # print(out.fit_report())
    out.plot(datafmt='g-',fitfmt='r--')
    plt.show()

fitting(filenames[5])