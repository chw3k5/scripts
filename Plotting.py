from sys import platform
import os
import matplotlib
from matplotlib import pyplot as plt
#if platform == 'darwin':
#    matplotlib.rc('text', usetex=True)
from profunc import getproparams,  getproSweep, get_fastIV
from domath  import linfit


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


def SimpleSweepPlot(datadir, search_4Snums=False, Snums='', verbose=False, standdev=True, std_num=1, do_title=True,
                    show_plot=False, save_plot=True, do_eps=True, show_fastIV=True, show_unpumped=True,
                    find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                    der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05):
    #####################
    ###### Options ######
    #####################
    legendsize = 10.0
    ax1_color = 'blue'
    ax2_color = 'red'
    fast_uA_color = 'green'
    fast_tp_color = 'yellow'
    unpump_uA_color = 'purple'
    unpump_tp_color = 'orange'
    astrolinewidth = 3
    fastlinewidth  = 1

    ##############################
    ###### Start the Script ######
    ##############################

    # Get the Sweep Directories to be plotted
    Snums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Snums, Snums)
    for Snum in Snums:
        if verbose:
            print "ploting for Snum: " + str(Snum)
        ####################
        ### Get the Data ###
        ####################
        # Get The Astronomy Quality Processed Sweep Data
        if platform == 'win32':
            proSdatadir  = prodatadir + Snum + '\\'
        elif platform == 'darwin':
            proSdatadir  = prodatadir + Snum + '/'
        mV_mean, mV_std,  uA_mean, uA_std, TP_mean, TP_std, TP_num, TP_freq, time_mean, pot, meas_num \
            = getproSweep(proSdatadir)

        # Get the Fast Processed Sweep Data
        fastprodata_found, unpumpedprodata_found, \
        mV_fast, uA_fast, tp_fast, pot_fast, \
        mV_unpumped, uA_unpumped, tp_unpumped, pot_unpumped \
            = GetAllTheProFastSweepData(proSdatadir)

        # Get the Processed Parameters of the Sweep
        paramsfile = proSdatadir + 'proparams.csv'
        K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsweep, LOuAset, UCA_volt,  \
        LOuA_set_pot, LOuA_magpot, meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
        del_time, LOfreq, IFband = getproparams(paramsfile)

        # Now we do some calculations needed for plotting
        uA_max = max(uA_mean)
        tp_max = max(TP_mean)
        if (fastprodata_found):
            uA_max = max(uA_max, max(uA_fast))
            tp_max = max(tp_max, max(tp_fast))
        if (unpumpedprodata_found):
            uA_max = max(uA_max, max(uA_unpumped))
            tp_max = max(tp_max, max(tp_unpumped))
        tp_scale=uA_max/tp_max

        ######################
        ### Start plotting ###
        ######################
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = legendsize
        fig, ax1 = plt.subplots()

        # AXIS 1 mV versus uA
        ax1.plot(mV_mean, uA_mean, color=ax1_color, linewidth=astrolinewidth)
        if fastprodata_found:
            ax1.plot(mV_fast, uA_fast, color=fast_uA_color, linewidth=fastlinewidth)
        if unpumpedprodata_found:
            ax1.plot(mV_unpumped, uA_unpumped, color=unpump_uA_color, linewidth=fastlinewidth)

        #ax1.set_ylabel('Current ($\mu$A)', color="ax1_color")
        for tl in ax1.get_yticklabels():
            tl.set_color(ax1_color)
        ax1.set_ylim([-10, 140])


        #AXIS 2 mV versus tp
        ax2 = ax1.twinx()
        ax2.plot(mV_mean, TP_mean*tp_scale, color=ax2_color, linewidth=astrolinewidth)
        if fastprodata_found:
            ax2.plot(mV_fast, tp_fast*tp_scale, color=fast_tp_color, linewidth=fastlinewidth)
        if unpumpedprodata_found:
            ax2.plot(mV_unpumped, tp_unpumped*tp_scale, color=unpump_tp_color, linewidth=fastlinewidth)

        #ax2.set_ylabel('Total Power', color=ax2_color)
        for tl in ax2.get_yticklabels():
            tl.set_color(ax2_color)

        if standdev:
            ## AXIS 1
            # Positive sigma
            ax1.plot(mV_mean, uA_mean+(uA_std*std_num), color=ax1_color, linewidth=1, ls='dotted')
            # Negative sigma
            ax1.plot(mV_mean, uA_mean-(uA_std*std_num), color=ax1_color, linewidth=1, ls='dotted')
            ## AXIS 2
            # Positive sigma
            ax2.plot(mV_mean, (TP_mean+(TP_std*std_num))*tp_scale, color=ax2_color, linewidth=1, ls='dotted')
            # Negative sigma
            ax2.plot(mV_mean, (TP_mean-(TP_std*std_num))*tp_scale, color=ax2_color, linewidth=1, ls='dotted')

        if find_lin_mVuA:
            slopes_mVuA, intercepts_mVuA, bestfits_mV, bestfits_uA \
                =  linfit(mV_mean, uA_mean, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                          do_der2_conv, der2_min_cdf, der2_sigma, verbose)

        lines  = []
        labels = []

        line1 = plt.Line2D(range(10), range(10), color = ax1_color)
        lines.append(line1)
        labels.append("Astro IV")

        line2 = plt.Line2D(range(10), range(10), color = ax2_color)
        lines.append(line2)
        labels.append("Astro TP")

        if fastprodata_found:
            line3 = plt.Line2D(range(10), range(10), color = fast_uA_color)
            lines.append(line3)
            labels.append("Fast IV")

            line4 = plt.Line2D(range(10), range(10), color = fast_tp_color)
            lines.append(line4)
            labels.append("Fast TP")

        if unpumpedprodata_found:
            line5 = plt.Line2D(range(10), range(10), color = unpump_uA_color)
            lines.append(line5)
            labels.append("Unpump IV")

            line6 = plt.Line2D(range(10), range(10), color = unpump_tp_color)
            lines.append(line6)
            labels.append("Unpump TP")
        if standdev:
            line7 = plt.Line2D(range(10), range(10), color="black", ls='dotted')
            lines.append(line7)
            if platform == 'darwin':
                labels.append(str(std_num)+"sigma")
            elif platform == 'win32':
                labels.append(str(std_num)+"sigma")

        if find_lin_mVuA:
            for n in range(len(bestfits_mV[0,:])):
                ax1.plot(bestfits_mV[:,n], bestfits_uA[:, n], color="black", linewidth=2)
                lines.append(plt.Line2D(range(10), range(10), color="black"))
                resist = 1000*(1.0/slopes_mVuA[n])
                print resist
                labels.append(str('%3.1f' % resist))

        ### Things to make the plot look good
        plt.legend(tuple(lines),tuple(labels), numpoints=1, loc=2)
        ax1.set_xlabel('Voltage (mV)')
        ax1.set_ylabel('Current (uA)')
        ax2.set_ylabel('Total Power (unscaled)')

        xlimL  =  -3
        xlimR  =   6
        ylimL1 = -20
        ylimR1 = 140
        ylimL2 =   0
        ylimR2 = 180

        xscale = abs(xlimR  - xlimL)
        yscale = abs(ylimR2 - ylimL2)

        ax1.set_xlim([xlimL , xlimR ])
        ax1.set_ylim([ylimL1, ylimR1])
        ax2.set_ylim([ylimL2, ylimR2])

        # get parameter data
        if do_title:
            xpos = xlimL + (5.0/18.0)*xscale
            yincrement = yscale/25.0
            ypos = ylimR2 - yincrement
            if not LOuAset == None:
                plt.text(xpos, ypos, str('%2.3f' % LOuAset) + " uA LO", color = 'dodgerblue' )
                ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%1.5f' % UCA_volt) + " V  UCA", color = 'dodgerblue')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%1.3f' % meanSIS_mV) + " (" + str('%1.3f' % stdSIS_mV) + ") mV",
                         color = 'dodgerblue')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%2.2f' % meanSIS_uA) + " (" + str('%2.2f' % stdSIS_uA) + ") uA",
                         color = 'dodgerblue')
            ypos = ypos - yincrement
            if not LOuA_set_pot == None:
                plt.text(xpos, ypos, "@" + str('%06.f' % LOuA_set_pot) + " SIS bias pot", color = 'dodgerblue')
                ypos = ypos - yincrement
            if not LOuA_magpot == None:
                plt.text(xpos, ypos, "@" + str('%06.f' % LOuA_magpot) + "  Magnet pot", color = 'dodgerblue')
                ypos = ypos - yincrement

            xpos = xlimL + (12.0/18.0)*xscale
            ypos = ylimR2 - yincrement

            if not magiset == None:
                plt.text(xpos, ypos,"magnet set value", color = 'coral')
                ypos = ypos - yincrement
                plt.text(xpos, ypos, str('%2.4f' % magiset)  + " mA" , color='coral')
                ypos = ypos - yincrement

            plt.text(xpos, ypos,"magnet meas value", color = 'coral')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%2.4f' % meanmag_mA) +  " (" + str('%2.4f' % stdmag_mA) + ") mA",
                         color = 'coral')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%06.f' % magpot) + " mag pot", color = 'coral')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str( K_val) + " K", color = 'gold')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%3.2f' % LOfreq) + " GHz", color = 'thistle')
            ypos = ypos - yincrement
            plt.text(    xpos, ypos, str('%1.3f' % IFband) + " GHz", color = 'aquamarine')
            ypos = ypos - yincrement


        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()

        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Snum+".eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Snum+".png")

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



def YfactorSweepsPlotter(datadir, search_4Ynums=False, Ynums=[], verbose=False, standdev=True, std_num=1, do_title=True,
                         show_plot=False, save_plot=True, do_eps=True, show_fastIV=True, show_unpumped=True,
                         find_lin_mVuA=False, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05):
    import sys
    import os
    import matplotlib
    from matplotlib import pyplot as plt
    platform = sys.platform
    #if platform == 'darwin':
    #    matplotlib.rc('text', usetex=True)
    from profunc import getproparams,  getproSweep, get_fastIV
    from domath  import linfit

    ##############################
    ###### Start the Script ######
    ##############################
    fastprodata_found     = False
    unpumpedprodata_found = False

    Ynums, prodatadir, plotdir = GetProDirsNames(datadir, search_4Snums, Ynums)

    for Ynum in Ynums:
        None

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


        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()

        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Snum+"_spec.eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Snum+"_spec.png")

        if verbose:
            print " "
    plt.close("all")

    return

#from sys import platform
#if platform == 'win32':
#    datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\warmmag\\"
#elif platform == 'darwin':
#    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'
#SingleSpectraPlotter(datadir, search_4Snums=True, Snums=['00001'])