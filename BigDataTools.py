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
verbose         = False
show_plots      = False
save_plots      = True
clear_old_plots = True
do_eps          = True


# data processing
process_data  = False
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
min_tp_int = 0 # at least this, None is any
max_tp_int = 60 # at most this, None is any
# the attempted setting of LO pump power in uA
min_LOuAset =  0 # at least this, None is any
max_LOuAset = 40 # at least this, None is any
# The maximum difference between the set and measured LO pump power
maxdiff_LOuA = 2 # None is any


###########################################
###### Intersecting lines Parameters ######
###########################################
do_intersecting_lines    = True
int_lines_plotdir        = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/intersecting_lines/')
int_lines_mV_centers     = list(numpy.arange(0.5,2.5,0.1))
int_lines_mV_plus_minus  = 0.05


###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = ['set4','set5','set6']


parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'
parent_folder = windir(parent_folder)
fullpaths = [parent_folder + setname + '/' for setname in setnames]


### MakeORclear_plotdir ###
def makeORclear_plotdir(plotdir,clear_flag=clear_old_plots):
    # clear out the old plots if you are going to make new ones in an old directory
    if save_plots:
        if os.path.isdir(plotdir):
            # remove old plots
            if clear_flag:
                shutil.rmtree(plotdir)
                # make a folder for new plots
                os.makedirs(plotdir)
        else:
            # make a folder for new plots
            os.makedirs(plotdir)
    return


################################
###### Do data processing ######
################################
if process_data:
    for fullpath in fullpaths:
        YdataPro(fullpath, verbose=verbose, search_4Ynums=search_4Ynums, search_str=search_str,
                 Ynums=Ynums, useOFFdata=False, Off_datadir='',
                 mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, regrid_mesh_mV=regrid_mesh_mV,
                 do_conv_mV=do_conv_mV, sigma_mV=sigma_mV, min_cdf_mV=min_cdf_mV,
                 do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                 do_freq_conv=do_freq_conv, min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz)

##############################
###### Get all the data ######
##############################
Ysweeps = getYsweeps(fullpaths, Ynums=Ynums, verbose=verbose)

##############################################################
###### Cut the data you have based on optional criteria ######
##############################################################

### Total power integration Time ###
if ((min_tp_int is not None) and (max_tp_int is not None)):
    Ysweeps = tp_int_cut(Ysweeps, min_tp_int=min_tp_int, max_tp_int=max_tp_int, verbose=verbose)
### the range of LO powers in uA ###
if ((min_LOuAset is not None) and (max_LOuAset is not None)):
    Ysweeps = LOuAset_cut(Ysweeps, min_LOuAset=min_LOuAset, max_LOuAset=max_LOuAset, verbose=verbose)
### the diffence between the measured LO power in uA and the LO power the was supposed to be set ###
if (maxdiff_LOuA is not None):
    Ysweeps = LOuAdiff_cut(Ysweeps, max_diff=maxdiff_LOuA, verbose=verbose)





################################
###### Intersecting Lines ######
################################
if do_intersecting_lines:
    makeORclear_plotdir(int_lines_plotdir)
    for mV_center in int_lines_mV_centers:
        fig, ax1 = plt.subplots()
        for Ysweep in Ysweeps:
            Ysweep.intersecting_line(mV_center=mV_center,mV_plus_minus=int_lines_mV_plus_minus)
            m = Ysweep.intersectingL_m
            b = Ysweep.intersectingL_b
            temps=[-300,300]
            powers=[]
            for temp in temps:
                powers.append((temp*m)+b)
            ax1.plot(temps,powers)

        plt.title("Bias voltage "+str('%2.2f' % mV_center ) + ' mV')
        plt.xlabel('temperature (K)')
        plt.ylabel('power recorder output (V)')

        #plt.legend(loc=2)
        # temper= -44
        # plt.text(-20, 0.22, "$44 K = T^\prime$", fontsize=16, color="firebrick")
        # ax1.plot([temper, temper],[-0.1, .25], color="firebrick")

        if show_plots:
            plt.show()
            plt.draw()

        plotfilename = int_lines_plotdir+'intersecting_lines_'+str('%2.2f' % mV_center )
        if ((do_eps) and (not platform == 'win32')):
            if verbose:
                print 'saving EPS file'
            plt.savefig(plotfilename+'.eps')
        else:
            if verbose:
                print 'saving PNG file'
            plt.savefig(plotfilename+'.png')
        plt.close("all")
