__author__ = 'chw3k5'
from sys import platform
import matplotlib
from matplotlib import pyplot as plt
import os, shutil, numpy
from datapro import YdataPro
from profunc import windir
from SetGrab import getYsweeps, tp_int_cut, LOuAset_cut, LOuAdiff_cut

###############
### Options ###
###############

# general
verbose       = True
show_plots    = False
save_plots    = True
do_eps        = True
plotdir       = '/Users/chw3k5/Documents/Grad_School/Kappa/intersecting_lines/'

# data processing
process_data  = True
Ynums         = None
search_str    = 'Y'
search_4Ynums = True
mono_switcher_mV = True
do_regrid_mV     = True
regrid_mesh_mV   = 0.01
do_conv_mV       = True
sigma_mV         = 0.08
min_cdf_mV       = 0.95
do_normspectra   = False
norm_freq        = 1.42
norm_band        = 0.060
do_freq_conv     = True
min_cdf_freq     = 0.90
sigma_GHz        = 0.10

######################
### Parameter Cuts ###
######################
# total power integration time
min_tp_int = None # at least this, None is any
max_tp_int = None # at most this, None is any
# the attempted setting of LO pump power in uA
min_LOuAset =  2 # at least this, None is any
max_LOuAset = 16 # at least this, None is any
# The maximum diffference between the set and measued LO pump power
maxdiff_LOuA = 2 # None is any


###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = ['set4','set5','set6','set7','LOfreq','LOfreq2']


parent_folder = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'
if platform == 'win32':
    parent_folder = windir(parent_folder)
fullpaths = [parent_folder + setname + '/' for setname in setnames]

Ysweeps = getYsweeps(fullpaths, Ynums=Ynums, verbose=verbose)


















# clear out the old plots if you are going to make new ones in an old directory
if save_plots:
    if os.path.isdir(plotdir):
        # remove old plots
        shutil.rmtree(plotdir)
        # make a folder for new plots
        os.makedirs(plotdir)
    else:
        # make a folder for new plots
        os.makedirs(plotdir)


# Do data processing
if process_data:
    for fullpath in fullpaths:
        YdataPro(fullpath, verbose=verbose, search_4Ynums=search_4Ynums, search_str=search_str,
                 Ynums=Ynums, useOFFdata=False, Off_datadir='',
                 mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, regrid_mesh_mV=regrid_mesh_mV,
                 do_conv_mV=do_conv_mV, sigma_mV=sigma_mV, min_cdf_mV=min_cdf_mV,
                 do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                 do_freq_conv=do_freq_conv, min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz)

if ((min_tp_int is not None) and (max_tp_int is not None)):
    Ysweeps = tp_int_cut(Ysweeps, min_tp_int=min_tp_int, max_tp_int=max_tp_int, verbose=verbose)

if ((min_LOuAset is not None) and (max_LOuAset is not None)):
    Ysweeps = LOuAset_cut(Ysweeps, min_LOuAset=min_LOuAset, max_LOuAset=max_LOuAset, verbose=verbose)

if (maxdiff_LOuA is not None):
    Ysweeps = LOuAdiff_cut(Ysweeps, max_diff=maxdiff_LOuA, verbose=verbose)




# with the mask made above we can plot the data
intlindata2plot = []
m_list          = []
b_list          = []
index_list = numpy.transpose(numpy.where((intlindata2plot_mask == True)))
matplotlib.rcParams['legend.fontsize'] = 12.0
fig, ax1 = plt.subplots()
temperature_axis = numpy.arange(-300, 301,1)
for n in index_list:# range(len(index_list)):
    single_line = intlindata[n]
    intlindata2plot.append(single_line)

intlindata2plot_array = numpy.array(intlindata2plot)
intlindata2plot_array = numpy.asarray(sorted(intlindata2plot_array,  key=itemgetter(4)))
intlindata2plot = list(intlindata2plot_array)
for single_line in intlindata2plot:
    hot_temp  = single_line[0]
    cold_temp = single_line[1]
    hot_pwr   = single_line[2]
    cold_pwr  = single_line[3]
    m = (hot_pwr-cold_pwr)/(hot_temp-cold_temp)
    m_list.append(m)
    b = hot_pwr-m*hot_temp
    b_list.append(b)
    pwr_axis = m*temperature_axis + b
    if (LO_current_min <= single_line[4] and single_line[4] <= LO_current_max and single_line[4] != 7.0):
        ax1.plot(temperature_axis, pwr_axis, label = str(single_line[4]) + ' $\mu$A')


ax1.set_ylim([-0.1, .25])
plt.xlabel('temperature (K)')
plt.ylabel('receiver power')

plt.legend(loc=2)
temper= -44
plt.text(-20, 0.22, "$44 K = T^\prime$", fontsize=16, color="firebrick")
ax1.plot([temper, temper],[-0.1, .25], color="firebrick")

if show_plots:
    plt.ylabel('Current ($\mu$A)')
    plt.show()
    plt.draw()
if save_plots:

    plotfilename = plotdir+'intersecting_lines'
    if ((do_eps) and (not platform == 'win32')):
        if verbose:
            print 'saving EPS file'
        plt.savefig(plotfilename+'.eps')
    else:
        if verbose:
            print 'saving PNG file'
        plt.savefig(plotfilename+'.png')
    plt.close("all")