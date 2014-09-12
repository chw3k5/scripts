import sys

# Import this is the directory that has my scripts
from Plotting import SingleSpectraPlotter, YfactorSweepsPlotter, SimpleSweepPlot, YSpectraPlotter

platform = sys.platform
from datapro import SweepDataPro, YdataPro



all_Single_Sweeps = False
all_Ydata         = False

### For Single Sweep ###
do_SweepDataPro        = False
do_SimpleSweepPlot     = False
do_SingeSpectraPlotter = False

### For Y-factor data and Sweeps ###
do_YdataPro             = False
do_YfactotSweepsPlotter = False
do_YSpectra_Plotter     = True

####################
### The Programs ###
####################

### For Single Sweeps ###
if all_Single_Sweeps:
    do_SweepDataPro        = True
    do_SimpleSweepPlot     = True
    do_SingeSpectraPlotter = True

# The directory what the data is kept
if platform == 'win32':
    datadir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\sweep\\warmmag\\'
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'

if do_SweepDataPro:
    SweepDataPro(datadir, verbose=True, search_4Sweeps=False, search_str='Y', Snums=['00003'],
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
                 do_normspectra=True, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)

if do_SimpleSweepPlot:
    SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True, show_standdev=True, std_num=3, display_params=True,
                    show_plot=False, save_plot=True, do_eps=False,
                    find_lin_mVuA=True, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                    der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                    plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=True, plot_fastmVtp=True,
                    plot_unpumpmVuA=True, plot_unpumpmVtp=True)

if do_SingeSpectraPlotter:
    SingleSpectraPlotter(datadir, search_4Snums=True, Snums='', verbose=False,
                        show_plot=False, save_plot=True, do_eps=False)




### For Y factor sweeps ###
if all_Ydata:
    do_YdataPro             = True
    do_YfactotSweepsPlotter = True
    do_YSpectra_Plotter     = True

# The directory what the data is kept
if platform == 'win32':
    datadir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\sweep\\LOfreq\\'
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/LOfreq2/'

if do_YdataPro:
    YdataPro(datadir, verbose=True, search_4Ynums=True, search_str='Y', Ynums=[], useOFFdata=False, Off_datadir='',
             mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
             do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90,
             sigma_GHz=0.10)

if do_YfactotSweepsPlotter:
    YfactorSweepsPlotter(datadir, search_4Ynums=True, Ynums='', verbose=True, show_standdev=True, std_num=3,
                         display_params=True, show_plot=False, save_plot=True, do_eps=True,
                         find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                         plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=True, plot_fastmVtp=False,
                         plot_unpumpmVuA=True, plot_unpumpmVtp=False, plot_Yfactor=True,
                         do_Ycut=False, start_Yplot=1, end_Yplot=2)

if do_YSpectra_Plotter:
    YSpectraPlotter(datadir, search_4Ynums=True, Ynums='', verbose=True,
                    show_plot=False, save_plot=True, do_eps=False)