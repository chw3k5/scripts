from sys import platform
import sys
import os
import numpy
import matplotlib
from matplotlib import pyplot as plt
#if platform == 'darwin':
#    matplotlib.rc('text', usetex=True)
from profunc import getproparams, getmultiParams,  getproSweep, get_fastIV, getproYdata, GetProDirsNames # Caleb's Functions
from domath  import linfit # Caleb's Functions




def GetAllTheProFastSweepData(prodatadir):
    # get fastIV processed data
    fastprodata_filename = prodatadir + "fastIV.csv"
    if os.path.isfile(fastprodata_filename):
        mV_fast, uA_fast, tp_fast, pot_fast = get_fastIV(fastprodata_filename)
        fastprodata_found  = True
    else:
        fastprodata_found = False
        mV_fast  = None
        uA_fast  = None
        tp_fast  = None
        pot_fast = None
    # get unpumped processed data
    unpumpedprodata_filename = prodatadir + "unpumped.csv"
    if os.path.isfile(unpumpedprodata_filename):
        mV_unpumped, uA_unpumped, tp_unpumped, pot_unpumped = get_fastIV(unpumpedprodata_filename)
        unpumpedprodata_found  = True
    else:
        unpumpedprodata_found = False
        mV_unpumped  = None
        uA_unpumped  = None
        tp_unpumped  = None
        pot_unpumped = None
    return fastprodata_found, unpumpedprodata_found, \
    mV_fast, uA_fast, tp_fast, pot_fast, \
    mV_unpumped, uA_unpumped, tp_unpumped, pot_unpumped



def DataTrimmer(min_trim, max_trim, ordered_set, trim_list):
    if min_trim is not None:
        set_max = max(ordered_set)
    else:
        set_max = None
    if max_trim is not None:
        set_min = min(ordered_set)
    else:
        set_min = None

    index_min_trim = 0
    min_trimmed = ordered_set
    min4min_trim = None
    status = True
    trimmed = None
    if not ((max_trim is None) and (min_trim is None)):
        if ((max_trim is not None) and (min_trim is not None) and (max_trim < min_trim)):
            print "max_trim is less than or equal to min_trim, min trim must be strictly less than max_trim"
            print "min_trim:", min_trim
            print "max_trim:", max_trim
            print "returning status=False"
            status = False
        else:
            # Min trim
            if min_trim is not None:
                if min_trim < set_max:
                    for index_min_trim in range(len(ordered_set[:])):
                        if min_trim <= ordered_set[index_min_trim]:
                            min_trimmed = ordered_set[index_min_trim:]
                            min4min_trim = min(min_trimmed)
                            break
            else:
                min4min_trim = set_min

            if max_trim is not None:
                # Max trim
                if min4min_trim < max_trim:
                    for index_max_trim in reversed(range(len(min_trimmed[:]))):
                        if ordered_set[index_max_trim] <= max_trim:
                            trimmed = ordered_set[:index_max_trim]
                            break
                        else:
                            print max_trim, "=max_trim is greater than the minimum of the the ordered set that has been already been trimmed sweep, that is:", min4min_trim
                            print "The min value of the ordered set before trimming was:", set_min
                            print "It is likely that the difference of max_trim and min_trim is greater that the spacing of values in the ordered set"
                            print "min_trim:", min_trim
                            print "max_trim:", max_trim
                            print "ordered_set:", ordered_set
                            print "min_trimmed:", min4min_trim
                            print "returning status=False"
                            status = False
                else:
                    print min_trim, "=mV_min is greater than the max value of mV for a sweep:", set_max
                    print "returning status=False"
                    status = False
            else:
                trimmed = min_trimmed


    # trim the corresponding values in the list dependent variables
    trimmed_list = []
    if ((trim_list != []) and (status)):
        list_length = len(trimmed)
        index_max_trim = index_min_trim + list_length
        for trim in trim_list:
            trimmed_list.append(trim[index_min_trim:index_max_trim])

    return status, trimmed, trimmed_list

def Params_2_str(param_vals, format_str, btype=None):
    if btype == 'sq':
        out_str = "["
    elif btype == 'curl':
        out_str = "{"
    elif btype == 'round':
        out_str = "("
    else:
        out_str = ''
    try:
        out_str += str(format_str % param_vals)
    except TypeError:
        vals_len = len(param_vals)
        if vals_len == 1:
            out_str += str(format_str % param_vals)
        elif 1 < vals_len:
            for n in range(vals_len - 1):
                out_str += str(format_str % param_vals[n]) + ', '
            out_str += str(format_str % param_vals[-1])
    if btype == 'sq':
        out_str += "]"
    elif btype == 'curl':
        out_str += "}"
    elif btype == 'round':
        out_str += ")"

    return out_str



def SimpleSweepPlot(datadir, search_4Snums=False, Snums='', verbose=False, show_standdev=True, std_num=1, display_params=True,
                    show_plot=False, save_plot=True, do_eps=True,
                    find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                    der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                    plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=False, plot_fastmVtp=False,
                    plot_unpumpmVuA=False, plot_unpumpmVtp=False
                    ):
    #####################
    ###### Options ######
    #####################

    ### Plot Options ###
    ax1_color = 'blue'
    ax2_color = 'red'
    fast_uA_color = 'green'
    fast_tp_color = 'yellow'
    unpump_uA_color = 'purple'
    unpump_tp_color = 'orange'
    astrolinewidth = 3
    fastlinewidth  = 1

    ### Legend ###
    legendsize = 10.0
    legendloc  = 2

    ### Axis Limits ###
    xlimL  =  -3
    xlimR  =   6
    ylimL1 = -20
    ylimR1 = 140
    ylimL2 =   0
    ylimR2 = 180
    # Some Calculations that don't need to be preformed every loop
    xscale = abs(xlimR  - xlimL)
    yscale = abs(ylimR2 - ylimL2)

    ### Parameter Colors
    LOpwr_color       = 'dodgerblue'
    mag_color         = 'coral'
    K_color           = 'gold'
    LOfreq_color      = 'thistle'
    IFband_color      = 'aquamarine'
    TP_int_time_color = 'darkgreen'

    ##############################
    ###### Start the Script ######
    ##############################

    ### Get the Sweep Directories to be plotted
    Snums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Snums, Snums)
    for Snum in Snums:
        if verbose:
            print "ploting for Snum: " + str(Snum)

        ####################
        ### Get the Data ###
        ####################
        if platform == 'win32':
            proSdatadir  = prodatadir + Snum + '\\'
        elif platform == 'darwin':
            proSdatadir  = prodatadir + Snum + '/'

        ### Get The Astronomy Quality Processed Sweep Data
        mV_mean, mV_std,  uA_mean, uA_std,TP_mean, TP_std, TP_num, TP_freq, \
        time_mean, pot, meas_num, astroprodata_found \
            = getproSweep(proSdatadir)

        ### Get the Fast Processed Sweep Data
        fastprodata_found, unpumpedprodata_found, \
        mV_fast, uA_fast, tp_fast, pot_fast, \
        mV_unpumped, uA_unpumped, tp_unpumped, pot_unpumped \
            = GetAllTheProFastSweepData(proSdatadir)

        ### Get the Processed Parameters of the Sweep
        paramsfile = proSdatadir + 'proparams.csv'
        K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsweep, LOuAset, UCA_volt,  \
        LOuA_set_pot, LOuA_magpot, meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
        del_time, LOfreq, IFband, TP_int_time \
            = getproparams(paramsfile)


        ############################
        ###### Start plotting ######
        ############################
        plt.clf()
        leglines  = []
        leglabels = []
        uA_max = 0
        tp_max = 0

        ##############
        ### AXIS 1 ###
        ##############
        fig, ax1 = plt.subplots()

        # AXIS 1 mV versus uA
        if (astroprodata_found and plot_astromVuA):
            ax1.plot(mV_mean, uA_mean, color=ax1_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = ax1_color))
            leglabels.append("Astro IV")
            uA_max = max(uA_max,max(uA_mean))
            if show_standdev:
               # Positive sigma
                ax1.plot(mV_mean, uA_mean+(uA_std*std_num), color=ax1_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax1.plot(mV_mean, uA_mean-(uA_std*std_num), color=ax1_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=ax1_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")
            if find_lin_mVuA:
                slopes_mVuA, intercepts_mVuA, bestfits_mV, bestfits_uA \
                    =  linfit(mV_mean, uA_mean, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                              do_der2_conv, der2_min_cdf, der2_sigma, verbose)
                for n in range(len(bestfits_mV[0,:])):
                    ax1.plot(bestfits_mV[:,n], bestfits_uA[:, n], color="black", linewidth=2)
                    leglines.append(plt.Line2D(range(10), range(10), color="black"))
                    resist = 1000*(1.0/slopes_mVuA[n])
                    leglabels.append(str('%3.1f' % resist))

        # Axis 1 mV versus uA Fast sweep
        if (fastprodata_found and plot_fastmVuA):
            ax1.plot(mV_fast, uA_fast, color=fast_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = fast_uA_color))
            leglabels.append("Fast IV")
            uA_max = max(uA_max,max(uA_fast))


        # Axis 1 mV versus uA Fast Unpumped Sweep
        if (unpumpedprodata_found and plot_unpumpmVuA):
            ax1.plot(mV_unpumped, uA_unpumped, color=unpump_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = unpump_uA_color))
            leglabels.append("Unpump IV")
            uA_max = max(uA_max,max(uA_unpumped))


        ##############
        ### AXIS 2 ###
        ##############

        ax2 = ax1.twinx()
        # Calculations for Axis 2 Scaling
        if (astroprodata_found and plot_astromVtp):
            tp_max = max(tp_max,max(TP_mean))
        if (fastprodata_found and plot_fastmVtp):
            tp_max = max(tp_max,max(tp_fast))
        if (unpumpedprodata_found and plot_unpumpmVtp):
            tp_max = max(tp_max,max(tp_unpumped))
        if not tp_max == 0:
            tp_scale=uA_max/tp_max

        # AXIS 2 mV versus tp Astro Data
        if (astroprodata_found and plot_astromVtp):
            ax2.plot(mV_mean, TP_mean*tp_scale, color=ax2_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = ax2_color))
            leglabels.append("Astro TP")
            if show_standdev:
                # Positive sigma
                ax2.plot(mV_mean, (TP_mean+(TP_std*std_num))*tp_scale, color=ax2_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax2.plot(mV_mean, (TP_mean-(TP_std*std_num))*tp_scale, color=ax2_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=ax2_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")

        # AXIS 2 mV versus tp Fast data
        if (fastprodata_found and plot_fastmVtp):
            ax2.plot(mV_fast, tp_fast*tp_scale, color=fast_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = fast_tp_color))
            leglabels.append("Fast TP")

        # AXIS 2 mV versus to Unpumped Data
        if (unpumpedprodata_found and plot_unpumpmVtp):
            ax2.plot(mV_unpumped, tp_unpumped*tp_scale, color=unpump_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = unpump_tp_color))
            leglabels.append("Unpump TP")


        ###############################################
        ###### Things to Make the Plot Look Good ######
        ###############################################

        ### Legend ###
        matplotlib.rcParams['legend.fontsize'] = legendsize
        plt.legend(tuple(leglines),tuple(leglabels), numpoints=1, loc=legendloc)

        ### Axis Labels ###
        ax1.set_xlabel('Voltage (mV)')
        ax1.set_ylabel('Current (uA)', color=ax1_color)
        ax2.set_ylabel('Total Power (unscaled)', color=ax2_color)

        ### Axis Ticks ###
        #for tl in ax1.get_yticklabels():
        #    tl.set_color(ax1_color)
        #for tl in ax2.get_yticklabel():
        #    tl.set_color(ax2_color)

        ### Axis Limits ###
        ax1.set_xlim([xlimL , xlimR ])
        ax1.set_ylim([ylimL1, ylimR1])
        ax2.set_ylim([ylimL2, ylimR2])


        ######################################################
        ###### Put Sweep ParameterS on the Plot as Text ######
        ######################################################
        if display_params:
            ################
            ### Column 1 ###
            ################
            xpos = xlimL + (5.0/18.0)*xscale
            yincrement = yscale/25.0
            ypos = ylimR2 - yincrement

            if LOuAset is not None:
                plt.text(xpos, ypos, str('%2.3f' % LOuAset) + " uA LO", color = LOpwr_color)
                ypos -= yincrement
            if UCA_volt is not None:
                plt.text(    xpos, ypos, str('%1.5f' % UCA_volt) + " V  UCA", color = LOpwr_color)
                ypos -= yincrement
            if meanSIS_mV is not None:
                if stdSIS_mV is not None:
                    plt.text(xpos, ypos, str('%1.3f' % meanSIS_mV) + " (" + str('%1.3f' % stdSIS_mV) + ") mV", color = LOpwr_color)
                else:
                    plt.text(xpos, ypos, str('%1.3f' % meanSIS_mV) + " mV", color = LOpwr_color)
                ypos -= yincrement
            if meanSIS_uA is not None:
                if stdSIS_uA is not None:
                    plt.text(xpos, ypos, str('%2.2f' % meanSIS_uA) + " (" + str('%2.2f' % stdSIS_uA) + ") uA", color = LOpwr_color)
                else:
                    plt.text(xpos, ypos, str('%2.2f' % meanSIS_uA) + " uA", color = LOpwr_color)
                ypos -= yincrement
            if LOuA_set_pot is not None:
                plt.text(xpos, ypos, "@" + str('%06.f' % LOuA_set_pot) + " SIS bias pot", color = LOpwr_color)
                ypos -= yincrement
            if LOuA_magpot is not None:
                plt.text(xpos, ypos, "@" + str('%06.f' % LOuA_magpot) + "  Magnet pot", color = LOpwr_color)
                ypos -= yincrement


            ################
            ### Column 2 ###
            ################
            xpos = xlimL + (12.0/18.0)*xscale
            ypos = ylimR2 - yincrement

            if magiset is not None:
                plt.text(xpos, ypos,"magnet set value", color = mag_color)
                ypos -= yincrement
                plt.text(xpos, ypos, str('%2.4f' % magiset)  + " mA" , color=mag_color)
                ypos -= yincrement
            if meanmag_mA is not None:
                plt.text(xpos, ypos,"magnet meas value", color = mag_color)
                ypos -= yincrement
                plt.text(xpos, ypos, str('%2.4f' % meanmag_mA) +  " (" + str('%2.4f' % stdmag_mA) + ") mA", color = mag_color)
                ypos -= yincrement
            if magpot is not None:
                plt.text(xpos, ypos, str('%06.f' % magpot) + " mag pot", color = mag_color)
                ypos -= yincrement
            if K_val is not None:
                plt.text(xpos, ypos, str( K_val) + " K", color = K_color)
                ypos -= yincrement
            if LOfreq is not None:
                plt.text(xpos, ypos, str('%3.2f' % LOfreq) + " GHz", color = LOfreq_color)
                ypos -= yincrement
            if IFband is not None:
                plt.text(xpos, ypos, str('%1.3f' % IFband) + " GHz", color = IFband_color)
                ypos -= yincrement
            if TP_int_time is not None:
                plt.text(xpos, ypos, str('%1.3f' % TP_int_time) + " secs", color = TP_int_time_color)
                ypos -= yincrement


        ##################
        ### Save Plots ###
        ##################
        if save_plot:
            if do_eps:
                filename = plotdir+Snum+".eps"
                if verbose:
                    print "saving EPS file: ", filename
                plt.savefig(filename)
            else:
                filename = plotdir+Snum+".png"
                if verbose:
                    print "saving PNG file: ", filename
                plt.savefig(filename)


        ##################
        ### Show Plots ###
        ##################
        if show_plot:
            plt.show()
            plt.draw()
        else:
            plt.close("all")

        if verbose:
            print " "
    plt.close("all")
    return
#
#setnum = 2
#search_4Snums = False     # default is True
#Snums         = ['00001'] # default is empty string ''
#verbose       = True      # default is False
#standdev      = True      # plot the standard deviation of the plotted curves, default is True
#std_num       = 3         # number of standard deviations to plot, default is '1'
#
#do_title      = True      # show plot title, default is True
#show_plot     = True     # display the plot on screen (not a good idea for 100's of plots), default is false
#save_plot     = True      # save the plot to a file, default is True
#do_eps        = True      # True save the plot as an .eps file, False saves the plot as a .png file, default is True
#show_fastIV   = True      # Show the fast IV curve if it is found, default is True
#show_unpumped = True      # Show the unpumped (LO off) IV curve if it is found, default is True
#
#datadir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test4/'
##datadir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set' + str(setnum) + '/'
##datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'
##datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/initialize/'
#SimpleSweepPlot(datadir, search_4Snums=search_4Snums, Snums=Snums,             \
#verbose=verbose, standdev=standdev, std_num=std_num, do_title=std_num,         \
#show_plot=show_plot, save_plot=save_plot, do_eps=do_eps,                       \
#show_fastIV=show_fastIV, show_unpumped=show_unpumped)

#datadir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'
#SimpleSweepPlot(datadir, search_4Snums=True, std_num=3, do_eps=False, Snums=['00002'])



def xyplotgen(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[], color='black', linw=1, ls='-', scale_str='' ):
    plot_list.append((x_vector, y_vector, color, linw, ls, scale_str))
    leglines.append((color,ls))
    leglabels.append(label)
    return plot_list, leglines, leglabels

def stdaxplotgen(x_vector, y_vector, y_std, std_num=1, label='',
                 plot_list=[], leglines=[], leglabels=[],
                 color='black', linw=1, ls='-', scale_str=''):
    # Positive sigma
    plot_list.append((x_vector, y_vector+(y_std*std_num), color, linw, ls, scale_str))
    leglines.append(None)
    leglabels.append(None)
    # Negative sigma
    plot_list.append((x_vector, y_vector-(y_std*std_num), color, linw, ls, scale_str))
    leglines.append((color, ls))

    leglabels.append(label)
    return plot_list, leglines, leglabels

def linifxyplotgen(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[],
                   color='black', linw=1, ls='-', scale_str='', linif=0.3,
                   der1_int=1, do_der1_conv=False, der1_min_cdf=0.90, der1_sigma=0.05, der2_int=1,
                   do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):
    slopes, intercepts, bestfits_x, bestfits_y \
                =  linfit(x_vector, y_vector, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                          do_der2_conv, der2_min_cdf, der2_sigma, verbose)
    for n in range(len(bestfits_x[0,:])):
        plot_list.append((bestfits_x[:,n], bestfits_y[:, n], color, linw, ls, scale_str))
        leglines.append((color, ls))
        resist = 1000*(1.0/slopes[n])
        if label is None:
            leglabels.append(None)
        else:
            leglabels.append(str('%3.1f' % resist)+label)
    return plot_list, leglines, leglabels




def allstarplotgen(x_vector, y_vector, y_std=None, std_num=1, plot_list=[], leglines=[], leglabels=[],
                   show_std=False, find_lin=False,
                   label='', std_label='', lin_label='',
                   color='red', lin_color='black',
                   linw=1, std_linw=1, lin_linw=1,
                   ls='-', std_ls='dotted', lin_ls='-',
                   scale_str='', linif=0.3,
                   der1_int=1, do_der1_conv=False, der1_min_cdf=0.9, der1_sigma=0.05,
                   der2_int=1, do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):
    plot_list, leglines, leglabels = xyplotgen(x_vector=x_vector, y_vector=y_vector, label=label,
                                               plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                                               color=color, linw=linw, ls=ls, scale_str=scale_str )
    if (show_std and (y_std is not None)):
        std_label = str(std_num)+" sigma"
        plot_list, leglines, leglabels \
        = stdaxplotgen(x_vector, y_vector, y_std, std_num=std_num, label=std_label,
                       plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                       color=color, linw=std_linw, ls=std_ls, scale_str=scale_str)
    if find_lin:
        plot_list, leglines, leglabels \
            = linifxyplotgen(x_vector, y_vector, label=lin_label, plot_list=plot_list, leglines=leglines, leglabels=leglabels,
               color=lin_color, linw=lin_linw, ls=lin_ls, scale_str=scale_str, linif=linif,
               der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
               der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
               verbose=verbose)
    return plot_list, leglines, leglabels

def astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                     mV_min, mV_max,
                     plot_list=[], leglines=[], leglabels=[],
                     yscale_info=[],
                     plot_mVuA=False, plot_mVtp=False,
                     show_standdev=False, std_num=1,
                     find_lin_mVuA=False, find_lin_mVtp=False, find_lin_uAtp=False,
                     mVuA_color='blue', mVtp_color='red', uAtp_color='purple', lin_color='black',
                     mVuA_linw=1, mVtp_linw=1, uAtp_linw=1, std_linw=1, lin_linw=1,
                     mVuA_ls = '-', mVtp_ls='-', uAtp_ls='-', std_ls='dotted', lin_ls='-',
                     labelPrefix='',
                     linif=0.3, der1_int=1, do_der1_conv=False, der1_min_cdf=0.9, der1_sigma=0.05,
                     der2_int=1,do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):

    trim_list = [mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx]
    # The trimming part of the script for mV values on the X-axis
    if ((mV_min is None) and (mV_max is None)):
        if verbose:
            print "Data trimming is not selected"
            print "the plot X-axis min and max will depend on the lines being plotted"
    else:
        status, mV, trimmed_list = DataTrimmer(mV_min, mV_max, mV, trim_list)
        if not status:
            print "The program failed the Data trimming"
            print "killing the script"
            sys.exit()

        [mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx] = trimmed_list


    # (Xdata, Y_data, color, linewidth, linestyle, scales-like-'TP'or'uA'or'')
    if plot_mVuA:
        label       = labelPrefix+'Astro IV'
        std_label   = ' sigma'
        lin_label   = ' Ohms'
        x_vector    = mV
        y_vector    = uA
        y_std       = uA_std
        scale_str   = 'uA'
        find_lin    = find_lin_mVuA
        color       = mVuA_color
        linw        = mVuA_linw
        ls          = mVuA_ls
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))
        plot_list, leglines, leglabels \
            = allstarplotgen(x_vector, y_vector, y_std=y_std, std_num=std_num,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=show_standdev, find_lin=find_lin,
                             label=label, std_label=std_label, lin_label=lin_label,
                             color=color, lin_color=lin_color,
                             linw=linw, std_linw=std_linw, lin_linw=lin_linw,
                             ls=ls, std_ls=std_ls, lin_ls=lin_ls,
                             scale_str=scale_str, linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)

    if plot_mVtp:
        label     = labelPrefix+'Astro TP'
        std_label = ' sigma'
        lin_label = ''
        x_vector  = mV
        y_vector  = TP
        y_std     = TP_std
        scale_str = 'tp'
        find_lin  = find_lin_mVtp
        color     = mVtp_color
        linw      = mVtp_linw
        ls        = mVtp_ls
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))
        plot_list, leglines, leglabels \
            = allstarplotgen(x_vector, y_vector, y_std=y_std, std_num=std_num,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=show_standdev, find_lin=find_lin,
                             label=label, std_label=std_label, lin_label=lin_label,
                             color=color, lin_color=lin_color,
                             linw=linw, std_linw=std_linw, lin_linw=lin_linw,
                             ls=ls, std_ls=std_ls, lin_ls=lin_ls,
                             scale_str=scale_str, linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)

    return plot_list, leglines, leglabels, yscale_info


def finddatalims(scale_info):
    min_val =  999999
    max_val = -999999
    overall_scale = []
    scale_types   = []
    for scale in scale_info:
        test1_scale_str = scale[0]
        test1_min_val   = scale[1]
        test1_max_val   = scale[2]
        try:
            # test to see if the reference exists
            scale_types_index = scale_types.index(test1_scale_str)
            # if it it exists, then we figure out whos maxes and mins are bigger
            oscale = overall_scale[scale_types_index]
            test2_scale_str = oscale[0]
            test2_min_val   = oscale[1]
            test2_max_val   = oscale[2]
            min_val = min(test1_min_val, test2_min_val)
            max_val = max(test1_max_val, test2_max_val)
            # get rid of the old reference
            scale_types.pop(scale_types_index)
            overall_scale.pop(scale_types_index)
            # append the new reference
            overall_scale.append((test1_scale_str,min_val,max_val))
            scale_types.append(test1_scale_str)
        except ValueError:
            # append the new reference
            overall_scale.append((test1_scale_str,test1_min_val,test1_max_val))
            scale_types.append(test1_scale_str)

    return overall_scale

def determine_scales(scale_str, scale_maxmins):
    scales = []
    for scale_maxmin in scale_maxmins:
        test_scale_str = scale_maxmin[0]
        if test_scale_str == scale_str:
            prime_scale_min = scale_maxmin[1]
            prime_scale_max = scale_maxmin[2]
            scales.append((scale_str, 1))
    for scale_maxmin in scale_maxmins:
        test_scale_str = scale_maxmin[0]
        if test_scale_str == scale_str:
            None
        else:
            divisor_scale_min = scale_maxmin[1]
            divisor_scale_max = scale_maxmin[2]

            scale_factor = min(float(prime_scale_min)/float(divisor_scale_min),float(prime_scale_max)/float(divisor_scale_max))
            scales.append((test_scale_str, scale_factor))
    return scales

def findscaling(scale_str,scales):
    scale_factor = None
    for scale in scales:
        test_str = scale[0]
        if test_str == scale_str:
            scale_factor = scale[1]
            break
    return scale_factor

def findscalemaxmin(scale_str,scales):
    scale_min = None
    scale_max = None
    for scale in scales:
        test_str = scale[0]
        if test_str == scale_str:
            scale_min = scale[1]
            scale_max = scale[2]
            break
    return scale_min, scale_max

def YfactorSweepsPlotter(datadir, search_4Ynums=False, Ynums='', verbose=False, mV_min=None, mV_max=None,
                         show_standdev=True, std_num=1, display_params=True,
                         show_plot=False, save_plot=True, do_eps=True,
                         plot_mVuA=True, plot_mVtp=True,
                         find_lin_mVuA=False, find_lin_mVtp=False,
                         do_receivertemp=True, linif=0.3,
                         der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                         plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=False, plot_fastmVtp=False,
                         plot_unpumpmVuA=False, plot_unpumpmVtp=False, plot_Yfactor=True,
                         do_Ycut=False, start_Yplot=0, end_Yplot=3
                         ):
    #####################
    ###### Options ######
    #####################

    ax1_scaling = ('mV','uA')
    ax2_scaling = ('mV','Yf')

    hot_labelPrefix  = '300K'
    cold_labelPrefix = ' 77K'

    ### Plot Options ###
    hotmVuA_color = 'blue'
    hotmVuA_linw  = 2
    hotmVuA_ls    = '-'

    hotmVtp_color = 'red'
    hotmVtp_linw  = 2
    hotmVtp_ls    = '-'

    coldmVuA_color = 'blue'
    coldmVuA_linw  = 2
    coldmVuA_ls    = '-'

    coldmVtp_color = 'firebrick'
    coldmVtp_linw  = 2
    coldmVtp_ls    = '-'



    hotfast_uA_color = 'green'

    hotfast_tp_color = 'yellow'
    hotunpump_uA_color = 'purple'
    hotunpump_tp_color = 'orange'

    coldfast_uA_color = 'green'
    coldfast_tp_color = 'yellow'
    coldunpump_uA_color = 'purple'
    coldunpump_tp_color = 'orange'

    Yfactor_color = 'green'
    Yfactor_linw  = 3
    Yfactor_ls    = '-'

    std_ls    = 'dotted'
    std_linw  = 1

    lin_color = 'black'
    lin_linw  = 1
    lin_ls    = '-'

    ### Labels ###
    hot_labelPrefix  = '300K'
    cold_labelPrefix = ' 77K'
    ax1_xlabel = 'Voltage (' + str(ax1_scaling[0]) + ')'
    ax1_ylabel = 'Current (' + str(ax1_scaling[1]) + ')'
    ax2_ylabel = 'Y-Factor'

    ### Legend ###
    legendsize = 20
    legendloc  = 2

    ### Axis Limits ###
    # X-axis
    if mV_min is not None:
        xlimL = mV_min
    else:
        xlimL = 999999.
    if mV_max is not None:
        xlimR = mV_max
    else:
        xlimR = -999999.


    # Y-axis
    ylimL1 =   0
    ylimR1 = 100
    ylimL2 =   0
    ylimR2 =  10
    yscale = abs(ylimR2 - ylimL2)

    ### Parameter Colors
    LOpwr_color       = 'dodgerblue'
    mag_color         = 'coral'
    LOfreq_color      = 'thistle'
    IFband_color      = 'aquamarine'
    TP_int_time_color = 'darkgreen'

    ##############################
    ###### Start the Script ######
    ##############################

    ### Get the Sweep Directories to be plotted
    Ynums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Ynums, Ynums)

    for Ynum in Ynums:
        if verbose:
            print "ploting for Ynum: " + str(Ynum)

        ####################
        ### Get the Data ###
        ####################
        if platform == 'win32':
            proYdatadir  = prodatadir + Ynum + '\\'
        elif platform == 'darwin':
            proYdatadir  = prodatadir + Ynum + '/'

        ######################################
        ###### Astronomy Bias Mode Data ######
        ######################################

        ### Get The Astronomy Quality Processed Sweep Data
        Yfactor, mV_Yfactor, hot_mV_mean, cold_mV_mean, mV, \
        hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean, \
        hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean,\
        hot_TP_std, cold_TP_std,\
        hot_time_mean, cold_time_mean, hot_pot, cold_pot,\
        hotdatafound, colddatafound, Ydatafound\
            = getproYdata(proYdatadir)


        ax1_plot_list   = []
        ax2_plot_list   = []
        leglines        = []
        leglabels       = []
        xscale_info     = []
        ax1_yscale_info = []
        ax2_yscale_info = []
        if hotdatafound:
            labelPrefix = hot_labelPrefix
            mV       = hot_mV_mean
            mV_std   = hot_mV_std
            uA       = hot_uA_mean
            uA_std   = hot_uA_std
            TP       = hot_TP_mean
            TP_std   = hot_TP_std
            time_apx = hot_time_mean
            pot_apx  = hot_pot
            xscale_str = 'mV'
            mVuA_color = hotmVuA_color
            mVtp_color = hotmVtp_color
            mVuA_linw  = hotmVuA_linw
            mVtp_linw  = hotmVtp_linw
            mVuA_ls    = hotmVuA_ls
            mVtp_ls    = hotmVtp_ls

            xscale_info.append((xscale_str,min(mV),max(mV)))
            ax1_plot_list, leglines, leglabels, yax1_scale_info \
                = astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                                  mV_min, mV_max,
                                  plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                                  yscale_info=ax1_yscale_info,
                                  plot_mVuA=plot_mVuA, plot_mVtp=plot_mVtp,
                                  show_standdev=show_standdev, std_num=std_num,
                                  find_lin_mVuA=find_lin_mVuA, find_lin_mVtp=find_lin_mVtp,
                                  mVuA_color=mVuA_color, mVtp_color=mVtp_color, lin_color=lin_color,
                                  mVuA_linw=mVuA_linw, mVtp_linw=mVtp_linw, std_linw=std_linw, lin_linw=lin_linw,
                                  mVuA_ls=mVuA_ls, mVtp_ls=mVtp_ls, std_ls=std_ls, lin_ls=lin_ls,
                                  labelPrefix=labelPrefix,
                                  linif=linif,
                                  der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                                  der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                                  verbose=verbose)


        if colddatafound:
            labelPrefix = cold_labelPrefix
            mV       = cold_mV_mean
            mV_std   = cold_mV_std
            uA       = cold_uA_mean
            uA_std   = cold_uA_std
            TP       = cold_TP_mean
            TP_std   = cold_TP_std
            time_apx = cold_time_mean
            pot_apx  = cold_pot
            xscale_str = 'mV'
            mVuA_color = coldmVuA_color
            mVtp_color = coldmVtp_color
            mVuA_linw  = coldmVuA_linw
            mVtp_linw  = coldmVtp_linw
            mVuA_ls    = coldmVuA_ls
            mVtp_ls    = coldmVtp_ls

            xscale_info.append((xscale_str,min(mV),max(mV)))
            ax1_plot_list, leglines, leglabels, ax1_yscale_info \
                = astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                                  mV_min, mV_max,
                                  plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                                  yscale_info=ax1_yscale_info,
                                  plot_mVuA=plot_mVuA, plot_mVtp=plot_mVtp,
                                  show_standdev=show_standdev, std_num=std_num,
                                  find_lin_mVuA=find_lin_mVuA, find_lin_mVtp=find_lin_mVtp,
                                  mVuA_color=mVuA_color, mVtp_color=mVtp_color, lin_color=lin_color,
                                  mVuA_linw=mVuA_linw, mVtp_linw=mVtp_linw, std_linw=std_linw, lin_linw=lin_linw,
                                  mVuA_ls=mVuA_ls, mVtp_ls=mVtp_ls, std_ls=std_ls, lin_ls=lin_ls,
                                  labelPrefix=labelPrefix,
                                  linif=linif,
                                  der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                                  der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                                  verbose=verbose)


        ############################
        ###### Parameter Data ######
        ############################

        ### Get the Processed Parameters of the Sweep
        paramsfile_list = []
        paramsfile_list.append(proYdatadir + 'hotproparams.csv')
        paramsfile_list.append(proYdatadir + 'coldproparams.csv')
        K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,\
        LOuA_set_pot, LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
        del_time, LOfreq, IFband, meas_num, TP_int_time, TP_num, TP_freq \
            = getmultiParams(paramsfile_list)


        #############################################
        ###### Analyze the scaling information ######
        #############################################

        # Unify xscale string lis then compress mins and maxes to a list that size.


        # Axis X scaling
        xscale_str = ax1_scaling[0]
        xscale_maxmin = finddatalims(xscale_info)

        if mV_min is None:
            for xscale_type in xscale_maxmin:
                type_str = xscale_type[0]
                if xscale_str == type_str:
                    xlimL = xscale_type[1]
        else:
            xlimL = mV_min
        if mV_max is None:
            for xscale_type in xscale_maxmin:
                type_str = xscale_type[0]
                if xscale_str == type_str:
                    xlimR = xscale_type[2]
        else:
            xlimR = mV_max

        xscales = determine_scales(xscale_str, xscale_maxmin)

        # Y Axis 1 scaling
        ax1_yscale_str    = ax1_scaling[1]
        ax1_yscale_maxmin = finddatalims(ax1_yscale_info)
        ax1_yscales       = determine_scales(ax1_yscale_str, ax1_yscale_maxmin)
        ylimL1, ylimR1    = findscalemaxmin(ax1_yscale_str,ax1_yscale_maxmin)

        # Y Axis 2 scaling
        ax2_yscale_str    = ax2_scaling[1]
        ax2_yscale_maxmin = finddatalims(ax2_yscale_info)
        ax2_yscales       = determine_scales(ax2_yscale_str, ax2_yscale_maxmin)
        ylimL2, ylimR2    = findscalemaxmin(ax2_yscale_str,ax2_yscale_maxmin)

        #####################################
        ###### Plot the Collected Data ######
        #####################################
        plt.clf()

        ##############
        ### AXIS 1 ###
        ##############
        if (ax1_plot_list != []):
            fig, ax1 = plt.subplots()
            for plot_obj in ax1_plot_list:
                (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
                scale_factor = findscaling(scale_str,ax1_yscales)
                ax1.plot(x_vector, y_vector*scale_factor, color=color, linewidth=linw, ls=ls)
            ### Axis Labels ###
            ax1.set_xlabel(ax1_xlabel)
            ax1.set_ylabel(ax1_ylabel)
            ### Axis Limits
            ax1.set_xlim([xlimL , xlimR ])
            ax1.set_ylim([ylimL1, ylimR1])
        ##############
        ### AXIS 2 ###
        ##############
        if (ax2_plot_list != []):
            ax2 = ax1.twinx()
            for plot_obj in ax2_plot_list:
                (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
                scale_factor = findscaling(scale_str,ax2_yscales)
                ax2.plot(x_vector, y_vector*scale_factor, color=color, linewidth=linw, ls=ls)
            #for tl in ax2.get_yticklabels():
            #    tl.set_color(Yfactor_color)
            ### Axis Labels ###
            ax2.set_ylabel(ax2_ylabel, color=Yfactor_color)
            ### Axis Limits
            ax2.set_ylim([ylimL2, ylimR2])
        ###############################################
        ###### Things to Make the Plot Look Good ######
        ###############################################

        ### Legend ###
        final_leglines  = []
        final_leglabels = []
        for indexer in range(len(leglines)):
            if ((leglines[indexer] != None) and (leglabels[indexer] != None)):
                final_leglabels.append(leglabels[indexer])
                legline_data = leglabels[indexer]
                color = legline_data[0]
                ls    = legline_data[1]
                final_leglines.append(plt.Line2D(range(10), range(10), color=color, ls=ls))
        matplotlib.rcParams['legend.fontsize'] = legendsize
        plt.legend(tuple(final_leglines),tuple(final_leglabels), numpoints=1, loc=legendloc)

        xsize = abs(xlimL-xlimR)


        ######################################################
        ###### Put Sweep ParameterS on the Plot as Text ######
        ######################################################
        if display_params:
            ################
            ### Column 1 ###
            ################
            xpos = xlimL + (5.0/18.0)*xsize
            yincrement = yscale/25.0
            if ax2_plot_list != []:
                ypos = ylimR2 - yincrement
            else:
                ypos = ylimR1 - yincrement
            if LOuAset is not None:
                LOuAset_str = Params_2_str(LOuAset, '%2.3f')
                plt.text(xpos, ypos, LOuAset_str + " uA LO", color = LOpwr_color)
                ypos -= yincrement
            if UCA_volt is not None:
                UCA_volt_str = Params_2_str(UCA_volt, '%1.5f')
                plt.text(xpos, ypos, UCA_volt_str + " V  UCA", color = LOpwr_color)
                ypos -= yincrement
            if meanSIS_mV is not None:
                meanSIS_mV_str = Params_2_str(meanSIS_mV, '%2.2f')
                if stdSIS_mV is not None:
                    stdSIS_mV_str = Params_2_str(stdSIS_mV, '%2.2f', 'round')
                    plt.text(xpos, ypos, meanSIS_mV_str + " " + stdSIS_mV_str + " mV", color = LOpwr_color)
                else:
                    plt.text(xpos, ypos, str('%1.3f' % meanSIS_mV) + " mV", color = LOpwr_color)
                ypos -= yincrement
            if meanSIS_uA is not None:
                meanSIS_uA_str = Params_2_str(meanSIS_uA, '%2.2f')
                if stdSIS_uA is not None:
                    stdSIS_uA_str = Params_2_str(stdSIS_uA, '%2.2f', 'round')
                    plt.text(xpos, ypos, meanSIS_uA_str + " " + stdSIS_uA_str+ " uA", color = LOpwr_color)
                else:
                    plt.text(xpos, ypos, str('%2.2f' % meanSIS_uA) + " uA", color = LOpwr_color)
                ypos -= yincrement
            if LOuA_set_pot is not None:
                LOuA_set_pot_str = Params_2_str(LOuA_set_pot, '%06.f')
                plt.text(xpos, ypos, "@" + LOuA_set_pot_str + " SIS bias pot", color = LOpwr_color)
                ypos -= yincrement
            if LOuA_magpot is not None:
                LOuA_magpot_str = Params_2_str(LOuA_magpot, '%06f')
                plt.text(xpos, ypos, "@" + LOuA_magpot_str + "  Magnet pot", color = LOpwr_color)
                ypos -= yincrement


            ################
            ### Column 2 ###
            ################
            xpos = xlimL + (12.0/18.0)*xsize
            if ax2_plot_list != []:
                ypos = ylimR2 - yincrement
            else:
                ypos = ylimR1 - yincrement

            if magiset is not None:
                plt.text(xpos, ypos,"magnet set value", color = mag_color)
                ypos -= yincrement
                magiset_str = Params_2_str(magiset, '%2.4f')
                plt.text(xpos, ypos, magiset_str + " mA" , color=mag_color)
                ypos -= yincrement
            if meanmag_mA is not None:
                plt.text(xpos, ypos,"magnet meas value", color = mag_color)
                ypos -= yincrement
                meanmag_mA_str = Params_2_str(meanmag_mA, '%2.4f')
                stdmag_mA_str = Params_2_str(stdmag_mA, '%2.4f', 'round')
                plt.text(xpos, ypos, meanmag_mA_str +  " " + stdmag_mA_str + " mA", color = mag_color)
                ypos -= yincrement
            if magpot is not None:
                magpot_str = Params_2_str(magpot, '%06.f')
                plt.text(xpos, ypos, magpot_str + " mag pot", color = mag_color)
                ypos -= yincrement
            if LOfreq is not None:
                LOfreq_str = Params_2_str(LOfreq, '%3.2f')
                plt.text(xpos, ypos, LOfreq_str + " GHz", color = LOfreq_color)
                ypos -= yincrement
            if IFband is not None:
                IFband_str = Params_2_str(IFband, '%1.3f')
                plt.text(xpos, ypos, IFband_str + " GHz", color = IFband_color)
                ypos -= yincrement
            if TP_int_time is not None:
                TP_int_time_str = Params_2_str(TP_int_time, '%1.3f')
                plt.text(xpos, ypos, TP_int_time_str + " secs", color = TP_int_time_color)
                ypos -= yincrement

        ##################
        ### Save Plots ###
        ##################
        if save_plot:
            if do_eps:
                filename = plotdir+Ynum+".eps"
                if verbose:
                    print "saving EPS file: ", filename
                plt.savefig(filename)
            else:
                filename = plotdir+Ynum+".png"
                if verbose:
                    print "saving PNG file: ", filename
                plt.savefig(filename)


        ##################
        ### Show Plots ###
        ##################
        if show_plot:
            plt.show()
            plt.draw()
        else:
            plt.close("all")

        if verbose:
            print " "
    plt.close("all")
    return








def SingleSpectraPlotter(datadir, search_4Snums=False, Snums='', verbose=False,
                    show_plot=False, save_plot=True, do_eps=False):
    import sys
    import numpy
    from mpl_toolkits.mplot3d import axes3d
    from matplotlib import pyplot as plt
    from matplotlib import cm
    platform = sys.platform
    #if platform == 'darwin':
    #    matplotlib.rc('text', usetex=True)

    Snums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Snums, Snums)

    for Snum in Snums:

        if verbose:
            print "ploting Spectra for Snum: " + str(Snum)

        if platform == 'win32':
            proSdatadir  = prodatadir + Snum + '\\'
        elif platform == 'darwin':
            proSdatadir  = prodatadir + Snum + '/'

        X_file = proSdatadir + "specdata_freq.npy"
        Y_file = proSdatadir + "specdata_mV.npy"
        Z_file = proSdatadir + "specdata_pwr.npy"

        fig = plt.figure()
        ax = fig.gca(projection='3d')


        X = numpy.load(X_file)
        Y = numpy.load(Y_file)
        Z = numpy.load(Z_file)

        X_max = numpy.max(X)
        Y_max = numpy.max(Y)
        Z_max = numpy.max(Z)

        X_min = numpy.min(X)
        Y_min = numpy.min(Y)
        Z_min = numpy.min(Z)

        X_ran = X_max-X_min
        Y_ran = Y_max-Y_min
        Z_ran = Z_max-Z_min

        offset_scale = 0.1

        X_offset = X_min - X_ran*offset_scale
        Y_offset = Y_min - Y_ran*offset_scale
        Z_offset = Z_min - Z_ran*0.4

        num_of_lines = 20.0

        cs = int(numpy.round(len(X[:,0])/num_of_lines))
        rs = int(numpy.round(len(X[0,:])/num_of_lines))

        ax.plot_surface(X, Y, Z, rstride=rs, cstride=cs, alpha=0.3)
        cset = ax.contour(X, Y, Z, zdir='z', offset=Z_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='x', offset=X_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='y', offset=Y_offset, cmap=cm.coolwarm)


        ax.set_xlabel('IF Frequency (GHz)')
        ax.set_xlim(X_min, X_max)
        ax.set_ylabel('Bias Voltage (mV)')
        ax.set_ylim(Y_max, Y_min)
        ax.set_zlabel('Recieved Power')
        ax.set_zlim(Z_min, Z_max)

        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Snum+"_spec.eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Snum+"_spec.png")

        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()
        else:
            plt.close("all")

        if verbose:
            print " "
    plt.close("all")

    return


def YSpectraPlotter(datadir, search_4Ynums=False, Ynums='', verbose=False,
                    show_plot=False, save_plot=True, do_eps=False):
    import sys
    import numpy
    from mpl_toolkits.mplot3d import axes3d
    from matplotlib import pyplot as plt
    from matplotlib import cm
    platform = sys.platform
    #if platform == 'darwin':
    #    matplotlib.rc('text', usetex=True)

    Ynums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Ynums, Ynums)

    for Ynum in Ynums:

        if verbose:
            print "ploting Spectra for Ynum: " + str(Ynum)

        if platform == 'win32':
            proSdatadir  = prodatadir + Ynum + '\\'
        elif platform == 'darwin':
            proSdatadir  = prodatadir + Ynum + '/'

        X_file = proSdatadir + "Y_freq.npy"
        Y_file = proSdatadir + "Y_mV.npy"
        Z_file = proSdatadir + "Y.npy"

        fig = plt.figure()
        ax = fig.gca(projection='3d')


        X = numpy.load(X_file)
        Y = numpy.load(Y_file)
        Z = numpy.load(Z_file)

        X_max = numpy.max(X)
        Y_max = numpy.max(Y)
        Z_max = numpy.max(Z)

        X_min = numpy.min(X)
        Y_min = numpy.min(Y)
        Z_min = numpy.min(Z)

        X_ran = X_max-X_min
        Y_ran = Y_max-Y_min
        Z_ran = Z_max-Z_min

        offset_scale = 0.1

        X_offset = X_min - X_ran*offset_scale
        Y_offset = Y_min - Y_ran*offset_scale
        Z_offset = Z_min - Z_ran*0.4

        num_of_lines = 20.0

        cs = int(numpy.round(len(X[:,0])/num_of_lines))
        rs = int(numpy.round(len(X[0,:])/num_of_lines))

        ax.plot_surface(X, Y, Z, rstride=rs, cstride=cs, alpha=0.3)
        cset = ax.contour(X, Y, Z, zdir='z', offset=Z_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='x', offset=X_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='y', offset=Y_offset, cmap=cm.coolwarm)


        ax.set_xlabel('IF Frequency (GHz)')
        ax.set_xlim(X_min, X_max)
        ax.set_ylabel('Bias Voltage (mV)')
        ax.set_ylim(Y_max, Y_min)
        ax.set_zlabel('Y-factor')
        ax.set_zlim(Z_min, 3)


        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Ynum+"_spec.eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Ynum+"_spec.png")

        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()
        else:
            plt.close("all")

        if verbose:
            print " "
    plt.close("all")

    return