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
do_intersecting_lines    = False
int_lines_plotdir        = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/intersecting_lines/')
int_lines_mV_centers     = list(numpy.arange(0.5,2.5,0.1))
int_lines_mV_plus_minus  = 0.05



###################################
###### Shot Noise Parameters ######
###################################
do_shot_noise = True


###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = ['set4']#,'set5','set6']


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




########################
###### Shot Noise ######
########################
if do_shot_noise:
    for Ysweep in Ysweeps:
        Ysweep.shotnoise_test(verbose=True)

            # # do derivatives to find linear regions
            # shot_matrix = numpy.zeros((len(uA_unpumpedhot),3))
            # shot_matrix[:,0] = uA_unpumpedhot
            # shot_matrix[:,1] = mV_unpumpedhot
            # shot_matrix[:,2] = tp_unpumpedhot
            # der1, der2 = do_derivative(shot_matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose)
            # #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
            # #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
            #
            # status, lin_start_uAtp, lin_end_uAtp = findlinear(der2[:,0], der2[:,2], linif, verbose)
            # slopes, intercepts, bestfits_uA, bestfits_tp = resfitter(uA_unpumpedhot, tp_unpumpedhot, lin_start_uAtp, lin_end_uAtp)
            #
            # import matplotlib
            # from matplotlib import pyplot as plt
            # matplotlib.rc('text', usetex=True)
            #
            # plt.clf()
            # matplotlib.rcParams['legend.fontsize'] = 10.0
            # IV_color = 'blue'
            # TP_color = 'red'
            # shot_color = 'green'
            # fig, ax1 = plt.subplots()
            # ax1.plot(uA_unpumpedhot, tp_unpumpedhot, color=TP_color, linewidth=5)
            # ax1.set_xlabel("current ($\mu$$A$)")
            # ax1.set_ylabel('Receiver Power', color=TP_color)
            # for tl in ax1.get_yticklabels():
            #     tl.set_color(TP_color)
            # for n in range(len(bestfits_tp[0,:])):
            #     ax1.plot(bestfits_uA[:,n], bestfits_tp[:, n], color="black", linewidth=2)
            # n = len(bestfits_tp[0,:])-1
            # shot_line_uA = []
            # shot_line_tp = []
            #
            # print
            # dark_current = intercepts[n]/slopes[n]
            # #shot_line_uA.append(-1*dark_current)
            # shot_line_uA.append(bestfits_uA[0,n])
            # shot_line_uA.append(bestfits_uA[1,n])
            #
            # #shot_line_tp.append(0)
            # shot_line_tp.append(bestfits_tp[0,n])
            # shot_line_tp.append(bestfits_tp[1,n])
            #
            # ax1.plot(shot_line_uA,shot_line_tp, color=shot_color, linewidth=3)
            # #ax1.plot([-1*dark_current, -1*dark_current],[0,max(tp_unpumpedhot)], color='firebrick', linewidth = 3)
            # plt.text(30, 0.068, "L$\cdot$$T_{IF} = 51$K", fontsize=16, color=shot_color)
            # plt.text(30, 0.06, "with $T_{IF}$ $=$ $10$K, L$ = 7$dB", fontsize=16, color=shot_color)
            #
            # B = 60.0e6 # MHz
            # e = 1.60217657e-19 # Columbs (electron charge)
            # I = dark_current*1.0e-6
            # P = 2.0*e*I*B
            # fP = P*1.0e15
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.7, str('%2.2f' % fP) + " $fW = 2eI_0$$B = P_0$", fontsize=16, color="firebrick")
            #
            # kb = 1.3806488e-23
            # T = (2.0*e*I)/(kb)
            # mT = T*1.0e3
            # #print T
            #
            #
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.6, str('%2.2f' % T) + " $K = T_0$", fontsize=16, color="firebrick")
            #
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.5, str(slopes[n]) + " = slope, " + str(intercepts[n]) +" = Y(0)", fontsize=16, color="firebrick")
            # ax2 = ax1.twinx()
            # ax2.plot(uA_unpumpedhot, mV_unpumpedhot, color=IV_color, linewidth=5)
            # ax2.set_ylabel('Voltage ($mV$)', color=IV_color)
            # for tl in ax2.get_yticklabels():
            #     tl.set_color(IV_color)
            #
            # plt.savefig("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/shotplots/" + Ynum + ".eps")
            # plt.close('all')