__author__ = 'chw3k5'
from sys import platform
import matplotlib
from matplotlib import pyplot as plt
import os, shutil, numpy
from datapro import YdataPro
from profunc import windir
from SetGrab import getYsweeps, tp_int_cut, LOuAset_cut, LOuAdiff_cut, mV_bias_cut_Y

colors = ['BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate','Coral','CornflowerBlue','Crimson','Cyan',
          'DarkBlue','DarkCyan','DarkGoldenRod', 'DarkGreen','DarkMagenta','DarkOliveGreen','DarkOrange',
          'DarkOrchid','DarkRed','DarkSalmon','DarkSeaGreen','DarkSlateBlue','DodgerBlue','FireBrick','ForestGreen',
          'Fuchsia','Gold','GoldenRod','Green','GreenYellow','HotPink','IndianRed','Indigo','LawnGreen',
          'LightCoral','Lime','LimeGreen','Magenta','Maroon', 'MediumAquaMarine','MediumBlue','MediumOrchid',
          'MediumPurple','MediumSeaGreen','MediumSlateBlue','MediumTurquoise','MediumVioletRed','MidnightBlue',
          'Navy','Olive','OliveDrab','Orange','OrangeRed','Orchid','PaleVioletRed','Peru','Pink','Plum','Purple',
          'Red','RoyalBlue','SaddleBrown','Salmon','SandyBrown','Sienna','SkyBlue','SlateBlue','SlateGrey',
          'SpringGreen','SteelBlue','Teal','Tomato','Turquoise','Violet','Yellow','YellowGreen']





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
sigma_mV         = 0.05
min_cdf_mV       = 0.95
remove_spikes    = True
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
min_LOuAset =  None # at least this, None is any
max_LOuAset = None # at least this, None is any
# The maximum difference between the set and measured LO pump power
maxdiff_LOuA = None # None is any

### Will only work for Y factor
# mV bias cuts
mV_bias_min = 0.5 # at least this, None is any
mV_bias_max = 1.8 # at most this, None is any



#########################################
###### Yfactor versus LO frequency ######
#########################################
do_Yfactor_versus_LO_freq = True
min_Y_factor = 1.2
spec_bands = [0,1,2,3,4,5]
Y_LOfreq_colors = ['Crimson','FireBrick','Olive','GoldenRod','RoyalBlue','SaddleBrown','Red','Salmon','SandyBrown','Sienna','SkyBlue','SlateBlue','SlateGrey','BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate','Coral','CornflowerBlue','Crimson','Cyan']
Y_LOfreq_plotdir = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_LOfreq/')


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
do_shot_noise = False
shot_noise_plotdir = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/shot_noise/')


###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = ['set4','set5','set6','set7','LOfreq']

parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'
parent_folder = windir(parent_folder)
fullpaths = [parent_folder + setname + '/' for setname in setnames]
# fullpaths.append('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/LOfreq_wspec/')
# fullpaths.append('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/LOfreq_wspec2/')
# fullpaths.append('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/moonshot/')
# fullpaths.append('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/Mag_sweep/')
# fullpaths.append('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/LOfreq/')
print fullpaths
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
                 remove_spikes=remove_spikes,do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
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


### Yfactor cut
if ((mV_bias_min is not None) and (mV_bias_max is not None)):
    Ysweeps = mV_bias_cut_Y(Ysweeps, mV_min=mV_bias_min, mV_max=mV_bias_max, verbose=verbose)



#########################################
###### Yfactor versus LO frequency ######
#########################################
testmode = True
if do_Yfactor_versus_LO_freq:
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("LO frequency (GHz)")
    ax1.set_ylabel("Y Factor")
    ax1.set_xlim([645, 695])
    ax1.set_ylim([0,3])
    leglines  = []
    leglabels = []

    # get and plot the power meter data
    pm_max_Yfactors        = []
    pm_max_Yfactor_mVs     = []
    pm_max_Yfactor_LOfreqs = []
    for Ysweep in Ysweeps:
        pm_max_Yfactor_mV, pm_max_Yfactor = Ysweep.find_max_yfactor_pm()
        LOfreq = Ysweep.LOfreq
        if min_Y_factor <= pm_max_Yfactor:
            pm_max_Yfactors.append(pm_max_Yfactor)
            pm_max_Yfactor_mVs.append(pm_max_Yfactor_mV)
            pm_max_Yfactor_LOfreqs.append(LOfreq)
        if testmode:
            print  pm_max_Yfactor,':',LOfreq,'GHz :', pm_max_Yfactor_mV,' mV'

    x_vector = pm_max_Yfactor_LOfreqs
    y_vector = pm_max_Yfactors
    ls = "None"
    linw = 1
    color = 'DarkOrchid'
    fmt = 'o'
    markersize = 10
    alpha = 0.5

    ax1.plot(x_vector,y_vector , linestyle=ls, color=color,
                         marker=fmt, markersize=markersize, markerfacecolor=color, alpha=alpha)
    leglines.append(plt.Line2D(range(10), range(10), color=color, ls='', linewidth=linw,
                               marker=fmt, markersize=markersize, markerfacecolor=color, alpha=alpha))
    leglabels.append("PM data 1.42 GHz IF band")



    # get and plot the spectrum analyzer data
    for band_index in range(len(spec_bands)-1):
        low_freq = spec_bands[band_index]
        high_freq = spec_bands[band_index+1]

        sa_max_Yfactors = []
        sa_max_Yfactor_mVs = []
        sa_max_Yfactor_freqs = []
        sa_max_Yfactor_LOfreqs = []
        for (index_Y,Ysweep) in list(enumerate(Ysweeps)):
            if Ysweep.spec_data_found:
                sa_max_Yfactor, sa_max_Yfactor_mV, sa_Yfactor_freq = Ysweep.find_max_yfactor_spec(min_freq=low_freq,max_freq=high_freq)
                LOfreq = Ysweep.LOfreq
                if min_Y_factor <= sa_max_Yfactor:
                    sa_max_Yfactors.append(sa_max_Yfactor)
                    sa_max_Yfactor_mVs.append(sa_max_Yfactor_mV)
                    sa_max_Yfactor_freqs.append(sa_Yfactor_freq)
                    sa_max_Yfactor_LOfreqs.append(LOfreq)
                if testmode:
                    print 'max_Yfactor:',sa_max_Yfactor, '  max_Yfactor_LOfreq:',LOfreq,'  max_Yfactor_mV:',sa_max_Yfactor_mV, '  Yfactor_freq:',sa_Yfactor_freq
                    #print index_Y," Y index", Ysweep.name
                    #print len(Ysweep.spec_freq_list[1]),'length of self.spec_freq_list[1]'

        x_vector = sa_max_Yfactor_LOfreqs
        y_vector = sa_max_Yfactors
        ls = "None"
        linw = 1
        color = Y_LOfreq_colors[band_index]
        fmt = 'o'
        markersize = 10
        alpha = 0.5

        ax1.plot(x_vector,y_vector , linestyle=ls, color=color,
                             marker=fmt, markersize=markersize, markerfacecolor=color, alpha=alpha)
        leglines.append(plt.Line2D(range(10), range(10), color=color, ls='', linewidth=linw,
                                   marker=fmt, markersize=markersize, markerfacecolor=color, alpha=alpha))
        leglabels.append("SA data "+str(low_freq)+"-"+str(high_freq)+" GHz IF band")


    # stuff to make the final plot look good
    matplotlib.rcParams['legend.fontsize'] = 10
    plt.legend(tuple(leglines),tuple(leglabels), numpoints=3, loc=4)

    plt.savefig(Y_LOfreq_plotdir+"Yfactor_versus_LOfreq.png")
    plt.close('all')
















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

        if save_plots:
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
        fig, ax1 = plt.subplots()

        if Ysweep.hot_shotnoise_test:
            gain = Ysweep.hot_shotnoise_gain
            input_noise = Ysweep.hot_shotnoise_input_noise
            unpumped_uA = Ysweep.hot_raw_unpumped_uA
            unpumped_tp = Ysweep.hot_raw_unpumped_tp
            raw_uA = Ysweep.hot_raw_uA_mean
            raw_tp = Ysweep.hot_raw_TP_mean
            uA = Ysweep.hot_uA_mean
            tp = Ysweep.hot_tp_mean
            shot_uA = Ysweep.hot_shotnoise_shot_uA
            shot_tp = Ysweep.hot_shotnoise_shot_tp
            ax1.plot(uA, tp)
            ax1.plot(unpumped_uA,unpumped_tp)
            ax1.plot(raw_uA,raw_tp)
            ax1.plot(shot_uA,shot_tp)
            ax1.plot(shot_uA,(shot_uA+input_noise)*gain)

        if show_plots:
            plt.show()
            plt.draw()

        if save_plots:
            plotfilename = shot_noise_plotdir+'shotnoise_'+Ysweep.Ynum
            if ((do_eps) and (not platform == 'win32')):
                if verbose:
                    print 'saving EPS file'
                plt.savefig(plotfilename+'.eps')
            else:
                if verbose:
                    print 'saving PNG file'
                plt.savefig(plotfilename+'.png')
            plt.close("all")


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