__author__ = 'chw3k5'
from sys import platform
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import cm
import os, shutil, numpy
from datapro import YdataPro
from profunc import windir
from SetGrab import getYsweeps, tp_int_cut, LOuAset_cut, LOuAdiff_cut, mV_bias_cut_Y, LOfreq_cut
from domath import make_monotonic, filter_on_occurrences
from Plotting import xyplotgen2

colors = ['BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate','Coral','CornflowerBlue','Crimson','Cyan',
          'DarkBlue','DarkCyan','DarkGoldenRod', 'DarkGreen','DarkMagenta','DarkOliveGreen','DarkOrange',
          'DarkOrchid','DarkRed','DarkSalmon','DarkSeaGreen','DarkSlateBlue','DodgerBlue','FireBrick','ForestGreen',
          'Fuchsia','Gold','GoldenRod','Green','GreenYellow','HotPink','IndianRed','Indigo','LawnGreen',
          'LightCoral','Lime','LimeGreen','Magenta','Maroon', 'MediumAquaMarine','MediumBlue','MediumOrchid',
          'MediumPurple','MediumSeaGreen','MediumSlateBlue','MediumTurquoise','MediumVioletRed','MidnightBlue',
          'Navy','Olive','OliveDrab','Orange','OrangeRed','Orchid','PaleVioletRed','Peru','Pink','Plum','Purple',
          'Red','RoyalBlue','SaddleBrown','Salmon','SandyBrown','Sienna','SkyBlue','SlateBlue','SlateGrey',
          'SpringGreen','SteelBlue','Teal','Tomato','Turquoise','Violet','Yellow','YellowGreen']

color_len = len(colors)



###############
### Options ###
###############

# general
verbose         = True
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
do_normspectra   = True
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
maxdiff_LOuA = 1 # None is any
# select an LO freqency to look at
LOfreq_to_get = None # this number is rounded to the near integer, None is any
# reorder the Ysweeps list in terms of lowest to highest LOuA (meanSIS_uA)
sort_LOuA = False


### Will only work for Y factor
# mV bias cuts
mV_bias_min = 0.7 # at least this, None is any
mV_bias_max = 1.9 # at most this, None is any



#########################################
###### Yfactor versus LO frequency ######
#########################################
do_Yfactor_versus_LO_freq = True
do_max_Yfactor = True # False uses the average value for a bandwidth, True uses the maximum
min_Y_factor = 0.9
spec_bands = [1.39,1.45]#1.39,1.45]#,4,5]
Y_LOfreq_colors = ['Crimson','Olive','GoldenRod','RoyalBlue','SaddleBrown','Red','Salmon','SandyBrown','Sienna',
                   'SkyBlue','SlateBlue','SlateGrey','BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate',
                   'Coral','CornflowerBlue','Crimson','Cyan']

Y_LOfreq_plotdir = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_LOfreq/')

Y_LOfreq_ls = "-"
Y_LOfreq_linw = 3
Y_LOfreq_fmt = 'o'
Y_LOfreq_markersize = 5
Y_LOfreq_alpha = 1

Y_LOfreq_legend_size = 10
Y_LOfreq_legend_num_of_points = 3
Y_LOfreq_legend_loc = 3




###########################################
###### Intersecting lines Parameters ######
###########################################
do_intersecting_lines    = False
int_lines_plotdir        = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/intersecting_lines/')

intersecting_lines_behavior = 'Y_max' #'Y_max','Y_mV_band_ave'
int_lines_mV_centers     = [0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8]#list(numpy.arange(0.5,2.0,0.1))
int_lines_mV_plus_minus  = 0.05

# include_spec_data        = True
# IFband_vector            = [1,2,3,4,5]

show_popular_LOfreqs     = True
popular_LOfreqs_min_occurrences = 5 # integer or None for any
popular_LOfreqs_max_occurrences = None # integer or None for any

show_popular_meanmag_mA     = False
popular_meanmag_mA_min_occurrences = 5 # integer or None for any
popular_meanmag_mA_max_occurrences = None # integer or None for any

int_lines_sort_LOuA = True # True or False, sort by LO pump power (LOuA) just before making the plot


inter_lines_leg_on       = True
int_line_alpha = 1.0
int_line_linw  = 1
int_line_ls    = '-'




###################################
###### Shot Noise Parameters ######
###################################
do_shot_noise = False
shot_noise_plotdir = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/shot_noise/')


###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = []
#setnames.extend(['set4','set5','set6','set7','LOfreq'])
setnames.extend(['Mar28/LOfreq_wspec','Mar28/LOfreq_wspec2','Mar28/moonshot','Mar28/Mag_sweep','Mar28/LOfreq'])
#setnames.extend(['Mar24_15/LO_power','Mar24_15/Yfactor_test'])
#setnames.extend(['Nov05_14/Y_LOfreqMAGLOuA','Nov05_14/Y_MAG','Nov05_14/Y_MAG2','Nov05_14/Y_MAG3','Nov05_14/Y_standard'])
#setnames.extend(['Oct20_14/LOfreq','Oct20_14/Y_LO_pow','Oct20_14/Y_MAG','Oct20_14/Y_MAG2','Oct20_14'])

parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'
fullpaths = [windir(parent_folder + setname + '/') for setname in setnames]


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
                 Ynums=Ynums, use_google_drive=False,
                 useOFFdata=False, Off_datadir='',
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
### select a singel LO frequency
if LOfreq_to_get is not None:
    Ysweeps = LOfreq_cut(Ysweeps,LOfreq_to_get)
### reorder the Y sweeps for lowest to higher LO power (meanSIS_uA)
if sort_LOuA:
    LOuA_Ysweep_sort_list = []
    for Ysweep in Ysweeps:
         LOuA_Ysweep_sort_list.append(numpy.mean(Ysweep.meanSIS_uA))
    [new_LOuA_order,Ysweeps] = make_monotonic([LOuA_Ysweep_sort_list,Ysweeps])

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
    ax1.set_ylim([0.5, 2.5])
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

    # Sort all the data to make monotonic lines in the domain of LO frequency
    list_of_lists = [pm_max_Yfactor_LOfreqs,pm_max_Yfactors,pm_max_Yfactor_mVs]
    sorted_list_of_lists = make_monotonic(list_of_lists,reverse=False)
    [pm_max_Yfactor_LOfreqs,pm_max_Yfactors,pm_max_Yfactor_mVs] = sorted_list_of_lists

    x_vector = pm_max_Yfactor_LOfreqs
    y_vector = pm_max_Yfactors
    color = 'DarkOrchid'


    ax1.plot(x_vector,y_vector , linestyle=Y_LOfreq_ls, color=color, linewidth=Y_LOfreq_linw,
                         marker=Y_LOfreq_fmt, markersize=Y_LOfreq_markersize, markerfacecolor=color, alpha=Y_LOfreq_alpha)
    leglines.append(plt.Line2D(range(10), range(10), color=color, ls=Y_LOfreq_ls, linewidth=Y_LOfreq_linw,
                               marker=Y_LOfreq_fmt, markersize=Y_LOfreq_markersize, markerfacecolor=color, alpha=Y_LOfreq_alpha))
    leglabels.append("PM data 1.42 GHz IF band")



    # get and plot the spectrum analyzer data
    for band_index in range(len(spec_bands)-1):
        low_freq = spec_bands[band_index]
        high_freq = spec_bands[band_index+1]

        sa_Yfactors = []
        sa_Yfactor_mVs = []
        sa_Yfactor_freqs = []
        sa_Yfactor_LOfreqs = []
        for (index_Y,Ysweep) in list(enumerate(Ysweeps)):
            if Ysweep.spec_data_found:
                sa_max_Yfactor, sa_max_Yfactor_mV, sa_Yfactor_freq, sa_ave_Yfactor = Ysweep.find_max_yfactor_spec(min_freq=low_freq,max_freq=high_freq)
                LOfreq = Ysweep.LOfreq

                if do_max_Yfactor:
                    sa_Yfactor = sa_max_Yfactor
                else:
                    sa_Yfactor = sa_ave_Yfactor
                if ((min_Y_factor <= sa_Yfactor) and (Ysweep.fullpath !=windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/LOfreq/'))):
                    sa_Yfactors.append(sa_Yfactor)
                    sa_Yfactor_mVs.append(sa_max_Yfactor_mV)
                    sa_Yfactor_freqs.append(sa_Yfactor_freq)
                    sa_Yfactor_LOfreqs.append(LOfreq)
                if testmode:
                    print 'sa_Yfactor:',sa_Yfactor, '  max_Yfactor_LOfreq:',LOfreq,'  max_Yfactor_mV:',sa_max_Yfactor_mV, '  Yfactor_freq:',sa_Yfactor_freq
                    print Ysweep.fullpath
                    #print index_Y," Y index", Ysweep.name
                    #print len(Ysweep.spec_freq_list[1]),'length of self.spec_freq_list[1]'

        # Sort all the data to make monotonic lines in the domain of LO frequency
        list_of_lists = [sa_Yfactor_LOfreqs,sa_Yfactors,sa_Yfactor_mVs,sa_Yfactor_freqs]
        sorted_list_of_lists = make_monotonic(list_of_lists,reverse=False)
        [sa_Yfactor_LOfreqs,sa_Yfactors,sa_Yfactor_mVs,sa_Yfactor_freqs] = sorted_list_of_lists



        x_vector = sa_Yfactor_LOfreqs
        y_vector = sa_Yfactors
        color = Y_LOfreq_colors[band_index]

        ax1.plot(x_vector,y_vector , linestyle=Y_LOfreq_ls, color=color, linewidth=Y_LOfreq_linw,
                             marker=Y_LOfreq_fmt, markersize=Y_LOfreq_markersize, markerfacecolor=color, alpha=Y_LOfreq_alpha)
        leglines.append(plt.Line2D(range(10), range(10), color=color, ls=Y_LOfreq_ls, linewidth=Y_LOfreq_linw,
                                   marker=Y_LOfreq_fmt, markersize=Y_LOfreq_markersize, markerfacecolor=color, alpha=Y_LOfreq_alpha))
        leglabels.append("SA data "+str(low_freq)+"-"+str(high_freq)+" GHz IF band")


    # stuff to make the final plot look good
    matplotlib.rcParams['legend.fontsize'] = Y_LOfreq_legend_size
    plt.legend(tuple(leglines),tuple(leglabels), numpoints=Y_LOfreq_legend_num_of_points, loc=Y_LOfreq_legend_loc)

    plt.savefig(Y_LOfreq_plotdir+"Yfactor_versus_LOfreq.png")
    plt.close('all')









################################
###### Intersecting Lines ######
################################
if do_intersecting_lines:
    great_data_list = []

    great_plot_list = []
    great_leglines  = []
    great_leglabels = []
    makeORclear_plotdir(int_lines_plotdir)
    fig, ax1 = plt.subplots()

    if intersecting_lines_behavior == 'Y_max':
        color_count = 0
        plot_title = 'Ymax'

        local_plot_list = []
        local_leglines  = []
        local_leglabels = []
        local_Ysweeps   = []
        for Ysweep in Ysweeps:
            color = colors[color_count % color_len]
            color_count+=1
            Ysweep.intersecting_line_Ymax(mV_plus_minus=int_lines_mV_plus_minus)

            m = Ysweep.intersectingL_m
            b = Ysweep.intersectingL_b
            temps=[-300,400]
            powers=[]
            for temp in temps:
                powers.append((temp*m)+b)
            local_plot_list, local_leglines, local_leglabels \
                = xyplotgen2(temps, powers, label=''+str('%2.2f' % numpy.mean(Ysweep.meanSIS_uA))+' uA',
                             plot_list=local_plot_list, leglines=local_leglines, leglabels=local_leglabels,
                             color=color, linw=int_line_linw,
                             ls= int_line_ls, alpha= int_line_alpha,
                             scale_str='', leg_on=True )
            local_Ysweeps.append(Ysweep)

        great_data_list.append((plot_title, local_Ysweeps, local_plot_list, local_leglines, local_leglabels))

    elif intersecting_lines_behavior == 'Y_mV_band_ave':
        for mV_center in int_lines_mV_centers:
            color_count = 0
            plot_title = str('%2.2f' % mV_center )+'mV'

            local_plot_list = []
            local_leglines  = []
            local_leglabels = []
            local_Ysweeps   = []


            for Ysweep in Ysweeps:
                color = colors[color_count % color_len]
                color_count+=1
                Ysweep.intersecting_line_mV(mV_center=mV_center,mV_plus_minus=int_lines_mV_plus_minus)

                m = Ysweep.intersectingL_m
                b = Ysweep.intersectingL_b
                temps=[-300,400]
                powers=[]
                for temp in temps:
                    powers.append((temp*m)+b)
                local_plot_list, local_leglines, local_leglabels \
                    = xyplotgen2(temps, powers, label=''+str(Ysweep.mV_Yfactor)+' mV',
                                 plot_list=local_plot_list, leglines=local_leglines, leglabels=local_leglabels,
                                 color=color, linw=int_line_linw,
                                 ls= int_line_ls, alpha= int_line_alpha,
                                 scale_str='', leg_on=True )
                local_Ysweeps.append(Ysweep)
            great_data_list.append((plot_title,local_Ysweeps, local_plot_list, local_leglines, local_leglabels))


    ### Now I take the data and subdivide it based on things like LO frequency or whatever I want to look at
    # LO freq
    if show_popular_LOfreqs:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            LOfreq_list = []
            for Ysweep in Ysweeps:
                LOfreq_list.append(Ysweep.LOfreq)

            unique_LOfreq_list \
                = filter_on_occurrences(LOfreq_list,min_occurrences=popular_LOfreqs_min_occurrences,
                                        max_occurrences=popular_LOfreqs_max_occurrences)

            for unique_LOfreq in unique_LOfreq_list:
                local_plot_list = []
                local_leglines  = []
                local_leglabels = []
                local_Ysweeps   = []
                new_plot_title=plot_title+' '+str(unique_LOfreq)+'GHz'
                for (sweep_index,Ysweep) in list(enumerate(Ysweeps)):

                    if unique_LOfreq == Ysweep.LOfreq:
                        local_plot_list.append(plot_list[sweep_index])
                        local_leglines.append(leglines[sweep_index])
                        local_leglabels.append(leglabels[sweep_index])
                        local_Ysweeps.append(Ysweep)

                new_great_data_list.append((new_plot_title,local_Ysweeps, local_plot_list, local_leglines, local_leglabels))
        great_data_list = new_great_data_list

    # meanmag_mA
    if show_popular_meanmag_mA:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            meanmag_mA_list = []
            for Ysweep in Ysweeps:
                ave_meanmag_mA = numpy.mean(Ysweep.meanmag_mA)
                meanmag_mA_list.append(numpy.round(ave_meanmag_mA))

            unique_meanmag_mA_list \
                = filter_on_occurrences(meanmag_mA_list,min_occurrences=popular_meanmag_mA_min_occurrences,
                                        max_occurrences=popular_meanmag_mA_max_occurrences)

            for unique_meanmag_mA in unique_meanmag_mA_list:
                local_plot_list = []
                local_leglines  = []
                local_leglabels = []
                local_Ysweeps   = []
                new_plot_title=plot_title+' '+str(unique_meanmag_mA)+'mA'
                for (sweep_index,Ysweep) in list(enumerate(Ysweeps)):

                    if unique_meanmag_mA == (numpy.round(numpy.mean(Ysweep.meanmag_mA))):
                        local_plot_list.append(plot_list[sweep_index])
                        local_leglines.append(leglines[sweep_index])
                        local_leglabels.append(leglabels[sweep_index])
                        local_Ysweeps.append(Ysweep)

                new_great_data_list.append((new_plot_title,local_Ysweeps,
                                            local_plot_list, local_leglines, local_leglabels))
        great_data_list = new_great_data_list







    if int_lines_sort_LOuA:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            LOuA_Ysweep_sort_list = []
            for Ysweep in Ysweeps:
                 LOuA_Ysweep_sort_list.append(numpy.mean(Ysweep.meanSIS_uA))
            [new_LOuA_order,Ysweeps,plot_list, leglines, leglabels] = make_monotonic([LOuA_Ysweep_sort_list,Ysweeps,plot_list, leglines, leglabels])
            new_great_data_list.append((plot_title, Ysweeps, plot_list, leglines, leglabels))
        great_data_list = new_great_data_list

    for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
        ##############
        ### AXIS 1 ###
        ##############
        if (plot_list != []):
            fig, ax1 = plt.subplots()
            for plot_obj in plot_list:
                (x_vector, y_vector, color, linw, ls, alpha, scale_str) = plot_obj
                ax1.plot(x_vector, y_vector, color=color, linewidth=linw, ls=ls, alpha=alpha)

        plt.title(plot_title)
        plt.xlabel('temperature (K)')
        plt.ylabel('power recorder output (V)')

        leglines_plot_line = []
        for indexer in range(len(leglines)):
            (color,ls,linw,alpha) = leglines[indexer]
            leglines_plot_line.append(plt.Line2D(range(10), range(10), color=color,
                            ls=ls, linewidth=linw, alpha=alpha))
        if inter_lines_leg_on:
            matplotlib.rcParams['legend.fontsize'] = 12
            plt.legend(tuple(leglines_plot_line),tuple(leglabels), numpoints=1, loc=0)

        if show_plots:
            plt.show()
            plt.draw()

        if save_plots:
            plotfilename = int_lines_plotdir+'intersecting_lines_'+plot_title.replace(' ','_')
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