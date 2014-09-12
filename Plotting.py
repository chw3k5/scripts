from sys import platform
import os
import numpy
import matplotlib
from matplotlib import pyplot as plt
#if platform == 'darwin':
#    matplotlib.rc('text', usetex=True)
from profunc import getproparams,  getproSweep, get_fastIV, getproYdata # Caleb's Functions
from domath  import linfit # Caleb's Functions


def GetProDirsNames(datadir, search_4nums, nums):
    if platform == 'win32':
        prodatadir = datadir + 'prodata\\'
        plotdir    = datadir + 'plots\\'
    elif platform == 'darwin':
        prodatadir = datadir + 'prodata/'
        plotdir    = datadir + 'plots/'
    if os.path.isdir(plotdir):
        None
        # remove old processed data
        # shutil.rmtree(plotdir)
        # make a folder for new processed data
        # os.makedirs(plotdir)
    else:
        # make a folder for new processed data
        os.makedirs(plotdir)
    if search_4nums:
        # get the Y numbers from the directory names in the datadir directory
        alldirs = []
        for root, dirs, files in os.walk(prodatadir):
            alldirs.append(dirs)
        nums = alldirs[0]
    return nums, prodatadir, plotdir


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

















def YfactorSweepsPlotter(datadir, search_4Ynums=False, Ynums='', verbose=False, show_standdev=True, std_num=1, display_params=True,
                         show_plot=False, save_plot=True, do_eps=True,
                         find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                         plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=False, plot_fastmVtp=False,
                         plot_unpumpmVuA=False, plot_unpumpmVtp=False, plot_Yfactor=True,
                         do_Ycut=False, start_Yplot=0, end_Yplot=3
                         ):
    #####################
    ###### Options ######
    #####################

    ### Plot Options ###
    hotmVuA_color = 'blue'
    hotmVtp_color = 'red'
    hotfast_uA_color = 'green'
    hotfast_tp_color = 'yellow'
    hotunpump_uA_color = 'purple'
    hotunpump_tp_color = 'orange'
    coldmVuA_color = 'blue'
    coldmVtp_color = 'red'
    coldfast_uA_color = 'green'
    coldfast_tp_color = 'yellow'
    coldunpump_uA_color = 'purple'
    coldunpump_tp_color = 'orange'

    Yfactor_color      = 'green'

    astrolinewidth = 2
    fastlinewidth  = 1
    Yfactorlinewidth = 3

    ### Legend ###
    legendsize = 10.0
    legendloc  = 2

    ### Axis Limits ###
    xlimL  =  -1
    xlimR  =   4
    ylimL1 = -10
    ylimR1 = 100
    ylimL2 =   0
    ylimR2 =   10
    # Some Calculations that don't need to be preformed every loop
    xscale = abs(xlimR  - xlimL)
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

        ### Get The Astronomy Quality Processed Sweep Data
        Yfactor, mV, hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean,    \
        hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std,            \
        cold_TP_std, hot_TP_num, cold_TP_num, hot_TP_freq, cold_TP_freq,           \
        hot_time_mean, cold_time_mean, hot_pot, cold_pot,                          \
        hot_meas_num, cold_meas_num \
            = getproYdata(proYdatadir)

        ### Get the Fast Processed Sweep Data
        hotfastprodata_found, hotunpumpedprodata_found, \
        hotmV_fast, hotuA_fast, hottp_fast, hotpot_fast, \
        hotmV_unpumped, hotuA_unpumped, hottp_unpumped, hotpot_unpumped \
            = GetAllTheProFastSweepData(proYdatadir + "hot")
        coldfastprodata_found, coldunpumpedprodata_found, \
        coldmV_fast, colduA_fast, coldtp_fast, coldpot_fast, \
        coldmV_unpumped, colduA_unpumped, coldtp_unpumped, coldpot_unpumped \
            = GetAllTheProFastSweepData(proYdatadir + "cold")

        ### Get the Processed Parameters of the Sweep
        paramsfile = proYdatadir + 'proparams.csv'
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
        Y_max  = 0

        ##############
        ### AXIS 1 ###
        ##############
        fig, ax1 = plt.subplots()

        ### Hot ###
        # AXIS 1 Hot mV versus uA
        if (plot_astromVuA):
            ax1.plot(mV, hot_uA_mean, color=hotmVuA_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotmVuA_color))
            leglabels.append("300K Astro IV")
            uA_max = max(uA_max,max(hot_uA_mean))
            if show_standdev:
               # Positive sigma
                ax1.plot(mV, hot_uA_mean+(hot_uA_std*std_num), color=hotmVuA_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax1.plot(mV, hot_uA_mean-(hot_uA_std*std_num), color=hotmVuA_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=hotmVuA_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")
            if find_lin_mVuA:
                slopes_mVuA, intercepts_mVuA, bestfits_mV, bestfits_uA \
                    =  linfit(mV, hot_uA_mean, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                              do_der2_conv, der2_min_cdf, der2_sigma, verbose)
                for n in range(len(bestfits_mV[0,:])):
                    ax1.plot(bestfits_mV[:,n], bestfits_uA[:, n], color="black", linewidth=2)
                    leglines.append(plt.Line2D(range(10), range(10), color="black"))
                    resist = 1000*(1.0/slopes_mVuA[n])
                    leglabels.append(str('%3.1f' % resist))

        # Axis 1 Hot mV versus uA Fast sweep
        if (hotfastprodata_found and plot_fastmVuA):
            ax1.plot(hotmV_fast, hotuA_fast, color=hotfast_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotfast_uA_color))
            leglabels.append("300K Fast IV")
            uA_max = max(uA_max,max(hotuA_fast))


        # Axis 1 Hot mV versus uA Fast Unpumped Sweep
        if (hotunpumpedprodata_found and plot_unpumpmVuA):
            ax1.plot(hotmV_unpumped, hotuA_unpumped, color=hotunpump_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotunpump_uA_color))
            leglabels.append("300K Unpump IV")
            uA_max = max(uA_max,max(hotuA_unpumped))

        ### COLD ###
        # AXIS 1 Cold mV versus uA
        if plot_astromVuA:
            ax1.plot(mV, cold_uA_mean, color=coldmVuA_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldmVuA_color))
            leglabels.append(" 77K Astro IV")
            uA_max = max(uA_max,max(cold_uA_mean))
            if show_standdev:
               # Positive sigma
                ax1.plot(mV, cold_uA_mean+(cold_uA_std*std_num), color=coldmVuA_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax1.plot(mV, cold_uA_mean-(cold_uA_std*std_num), color=coldmVuA_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=coldmVuA_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")
            if find_lin_mVuA:
                slopes_mVuA, intercepts_mVuA, bestfits_mV, bestfits_uA \
                    =  linfit(mV, cold_uA_mean, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                              do_der2_conv, der2_min_cdf, der2_sigma, verbose)
                for n in range(len(bestfits_mV[0,:])):
                    ax1.plot(bestfits_mV[:,n], bestfits_uA[:, n], color="black", linewidth=2)
                    leglines.append(plt.Line2D(range(10), range(10), color="black"))
                    resist = 1000*(1.0/slopes_mVuA[n])
                    leglabels.append(str('%3.1f' % resist))

        # Axis 1 Cold mV versus uA Fast sweep
        if (coldfastprodata_found and plot_fastmVuA):
            ax1.plot(coldmV_fast, colduA_fast, color=coldfast_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldfast_uA_color))
            leglabels.append(" 77K Fast IV")
            uA_max = max(uA_max,max(colduA_fast))


        # Axis 1 Cold mV versus uA Fast Unpumped Sweep
        if (coldunpumpedprodata_found and plot_unpumpmVuA):
            ax1.plot(coldmV_unpumped, colduA_unpumped, color=coldunpump_uA_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldunpump_uA_color))
            leglabels.append(" 77K Unpump IV")
            uA_max = max(uA_max,max(colduA_unpumped))


        # Calculations for Total Power (tp) Scaling
        if plot_astromVtp:
            tp_max = max(tp_max,max(hot_TP_mean))
            tp_max = max(tp_max,max(cold_TP_mean))
        if (hotfastprodata_found and plot_fastmVtp):
            tp_max = max(tp_max,max(hottp_fast))
        if (coldfastprodata_found and plot_fastmVtp):
            tp_max = max(tp_max,max(coldtp_fast))
        if (hotunpumpedprodata_found and plot_unpumpmVtp):
            tp_max = max(tp_max,max(hottp_unpumped))
        if (coldunpumpedprodata_found and plot_unpumpmVtp):
            tp_max = max(tp_max,max(coldtp_unpumped))
        if not tp_max == 0:
            tp_scale=uA_max/tp_max

        ### Hot ###
        # AXIS 1 Hot mV versus tp Astro Data
        if plot_astromVtp:
            ax1.plot(mV, hot_TP_mean*tp_scale, color=hotmVtp_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotmVtp_color))
            leglabels.append("300K Astro TP")
            if show_standdev:
                # Positive sigma
                ax1.plot(mV, (hot_TP_mean+(hot_TP_std*std_num))*tp_scale, color=hotmVtp_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax1.plot(mV, (hot_TP_mean-(hot_TP_std*std_num))*tp_scale, color=hotmVtp_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=hotmVtp_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")

        # AXIS 1 Hot mV versus tp Fast data
        if (hotfastprodata_found and plot_fastmVtp):
            ax1.plot(hotmV_fast, hottp_fast*tp_scale, color=hotfast_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotfast_tp_color))
            leglabels.append("300K Fast TP")

        # AXIS 1 Hot mV versus to Unpumped Data
        if (hotunpumpedprodata_found and plot_unpumpmVtp):
            ax1.plot(hotmV_unpumped, hottp_unpumped*tp_scale, color=hotunpump_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = hotunpump_tp_color))
            leglabels.append("300K Unpump TP")

        ### Cold ###
        # AXIS 1 Cold mV versus tp Astro Data
        if plot_astromVtp:
            ax1.plot(mV, cold_TP_mean*tp_scale, color=coldmVtp_color, linewidth=astrolinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldmVtp_color))
            leglabels.append(" 77K Astro TP")
            if show_standdev:
                # Positive sigma
                ax1.plot(mV, (cold_TP_mean+(cold_TP_std*std_num))*tp_scale, color=coldmVtp_color, linewidth=1, ls='dotted')
                # Negative sigma
                ax1.plot(mV, (cold_TP_mean-(cold_TP_std*std_num))*tp_scale, color=coldmVtp_color, linewidth=1, ls='dotted')
                leglines.append(plt.Line2D(range(10), range(10), color=coldmVtp_color, ls='dotted'))
                if platform == 'darwin':
                    leglabels.append(str(std_num)+"sigma")
                elif platform == 'win32':
                    leglabels.append(str(std_num)+"sigma")

        # AXIS 1 Cold mV versus tp Fast data
        if (coldfastprodata_found and plot_fastmVtp):
            ax1.plot(coldmV_fast, coldtp_fast*tp_scale, color=coldfast_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldfast_tp_color))
            leglabels.append(" 77K Fast TP")

        # AXIS 1 Cold mV versus to Unpumped Data
        if (coldunpumpedprodata_found and plot_unpumpmVtp):
            ax1.plot(coldmV_unpumped, coldtp_unpumped*tp_scale, color=coldunpump_tp_color, linewidth=fastlinewidth)
            leglines.append(plt.Line2D(range(10), range(10), color = coldunpump_tp_color))
            leglabels.append(" 77K Unpump TP")


        ##############
        ### AXIS 2 ###
        ##############

        ax2 = ax1.twinx()
        if plot_Yfactor:
            Y_max = max(Y_max, max(Yfactor))
            Y_scale = uA_max/Y_max
            ax1.plot(mV, Yfactor*Y_scale, color=Yfactor_color, linewidth=Yfactorlinewidth)
            if do_Ycut:
                ycut_low = numpy.where(mV < start_Yplot)
                ycut_low_ind = ycut_low[0][-1]
                ycut_high = numpy.where(mV > end_Yplot)
                ycut_high_ind = ycut_high[0][0]
                ax1.plot(mV[:ycut_low_ind], Yfactor[:ycut_low_ind], color="white", linewidth=Yfactorlinewidth+1)
                ax1.plot(mV[ycut_high_ind:], Yfactor[ycut_high_ind:], color="white", linewidth=Yfactorlinewidth+1)
            for tl in ax2.get_yticklabels():
                tl.set_color(Yfactor_color)


        ###############################################
        ###### Things to Make the Plot Look Good ######
        ###############################################

        ### Legend ###
        matplotlib.rcParams['legend.fontsize'] = legendsize
        plt.legend(tuple(leglines),tuple(leglabels), numpoints=1, loc=legendloc)

        ### Axis Labels ###
        ax1.set_xlabel('Voltage (mV)')
        ax1.set_ylabel('Current (uA)')
        ax2.set_ylabel('Y-Factor', color=Yfactor_color)

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