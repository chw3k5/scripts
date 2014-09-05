import sys

# Import this is the directory that has my scripts
platform = sys.platform
from datapro import SweepDataPro
from SimpleSweepPlot import SimpleSweepPlot
from SingleSpectraPlotter import SingleSpectraPlotter

# The directory what the data is kept
if platform == 'win32':
    datadir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\sweep\\test1\\'
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'

do_SweepDataPro = False
do_SimpleSweepPlot = False
do_SingeSpectraPlotter = True


####################
### The Programs ###
####################

if do_SweepDataPro:
    SweepDataPro(datadir, verbose=True, search_4Sweeps=True, search_str='Y', Snums=[],
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
                 do_normspectra=True, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)

if do_SimpleSweepPlot:
    SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True, standdev=True, std_num=3, do_title=True,
                    show_plot=False, save_plot=True, do_eps=False, show_fastIV=True, show_unpumped=True,
                    find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                    der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05)

if do_SingeSpectraPlotter:
    SingleSpectraPlotter(datadir, search_4Snums=True, Snums='', verbose=False,
                        show_plot=False, save_plot=True, do_eps=False)
