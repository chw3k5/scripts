def viewYfactorData(setnum, search_4Ynums, Ynums, verbose, standdev, std_num, do_title, show_plot, save_plot, do_eps, do_Ycut, start_Yplot, end_Yplot, datadir, show_fastIV):

    import sys
    import os
    import matplotlib
    import numpy
    import shutil
    from matplotlib import pyplot as plt
    #matplotlib.rc('text', usetex=True)
    
    # Import this is the directory that has my scripts
    func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)
        
    from profunc import getproparams,  getproYdata, get_fastIV
    
    
    ##############################
    ###### Start the Script ######
    ##############################
    fastprodatahot_found  = False
    fastprodatacold_found = False
    
    prodatadir = datadir + 'prodata/'
    plotdir    = datadir + 'plots/'
    if os.path.isdir(plotdir):
        # remove old processed data
        shutil.rmtree(plotdir)
        # make a folder for new processed data
        os.makedirs(plotdir)
    else:
        # make a folder for new processed data
        os.makedirs(plotdir)
    
    if search_4Ynums:
        # get the Y numbers from the directory names in the datadir directory
        alldirs = []
        for root, dirs, files in os.walk(prodatadir):
            alldirs.append(dirs)
        Ynums = alldirs[0]
    
    for Ynum_index in range(len(Ynums)):
        Ynum = Ynums[Ynum_index]
        
        if verbose:
            print "ploting for Ynum: " + str(Ynum)
	    
        proYdatadir  = prodatadir + Ynum + '/'
        Yfactor, mV, hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean, hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std, cold_TP_std, hot_TP_num, cold_TP_num, hot_TP_freq, cold_TP_freq, hot_time_mean, cold_time_mean, hot_pot, cold_pot, hot_meas_num, cold_meas_num = getproYdata(proYdatadir)
        
        # get fastIV processed data
        if show_fastIV:
            fastprodatahot_filename = proYdatadir + "hotfastIV.csv"
            if os.path.isfile(fastprodatahot_filename):
                mV_fasthot, uA_fasthot, tp_fasthot, pot_fasthot = get_fastIV(fastprodatahot_filename)
                fastprodatahot_found  = True
                
            fastprodatacold_filename = proYdatadir + "coldfastIV.csv"
            if os.path.isfile(fastprodatacold_filename):
                mV_fastcold, uA_fastcold, tp_fastcold, pot_fastcold = get_fastIV(fastprodatacold_filename)
                fastprodatacold_found = True
        # now some calulations needed for plotting
        uA_max = max(hot_uA_mean)
        tp_max = max(max(hot_TP_mean),max(cold_TP_mean))
        if (fastprodatahot_found):
            uA_max = max(uA_max, max(uA_fasthot))
            tp_max = max(tp_max, max(tp_fasthot))
        if (fastprodatacold_found):
            uA_max = max(uA_max, max(uA_fastcold))
            tp_max = max(tp_max, max(tp_fastcold))
        tp_scale=uA_max/tp_max
        
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = 10.0
        fig, ax1 = plt.subplots()
        
        if do_Ycut:
	    ycut_low = numpy.where(mV < start_Yplot)
            ycut_low_ind = ycut_low[0][-1]
            ycut_high = numpy.where(mV > end_Yplot)
            ycut_high_ind = ycut_high[0][0]
        
        
        ax1.plot(mV, Yfactor, color="green", linewidth=3)
        if do_Ycut:
            ax1.plot(mV[:ycut_low_ind], Yfactor[:ycut_low_ind], color="white", linewidth=4)
            ax1.plot(mV[ycut_high_ind:], Yfactor[ycut_high_ind:], color="white", linewidth=4)
        ax1.set_ylabel("Y factor", color="green")
        ax1.set_ylim([-0.5, 2.5])
        for tl in ax1.get_yticklabels():
            tl.set_color("green")
        
        ax2 = ax1.twinx()
        
        if fastprodatahot_found:
            ax2.plot(mV_fasthot, uA_fasthot, color="red", linewidth=1)
            ax2.plot(mV_fasthot, tp_fasthot*tp_scale, color="purple", linewidth=1)
        ax2.plot(mV, hot_uA_mean, color="red", linewidth=3)
        ax2.plot(mV, hot_TP_mean*tp_scale, color="purple", linewidth=3)
        
        if fastprodatacold_found:
            ax2.plot(mV_fastcold, uA_fastcold, color="firebrick", linewidth=1, ls='dashed')
            ax2.plot(mV_fastcold, tp_fastcold*tp_scale, color="blue", linewidth=1)
        ax2.plot(mV, cold_uA_mean, color="firebrick", linewidth=3, ls='dashed')
        ax2.plot(mV, cold_TP_mean*tp_scale, color="blue", linewidth=3)
        
        ax2.set_ylim([-10, 140])
        ax2.set_ylabel('Current ($\mu$A)', color="firebrick")
        for tl in ax2.get_yticklabels():
            tl.set_color('firebrick')
        
        
        if standdev:
            # Positive sigma
            ax2.plot(mV, hot_uA_mean+(hot_uA_std*std_num), color="red", linewidth=3, ls='dotted')
            ax2.plot(mV, cold_uA_mean+(cold_uA_std*std_num), color="firebrick", linewidth=3, ls='dotted')
            ax2.plot(mV, (hot_TP_mean+(hot_TP_std*std_num))*tp_scale, color="purple", linewidth=3, ls='dotted')
            ax2.plot(mV, (cold_TP_mean+(cold_TP_std*std_num))*tp_scale, color="blue", linewidth=3, ls='dotted')
        
            # Negative sigma
            ax2.plot(mV, hot_uA_mean-(hot_uA_std*std_num), color="red", linewidth=3, ls='dotted')
            ax2.plot(mV, cold_uA_mean-(cold_uA_std*std_num), color="firebrick", linewidth=3, ls='dotted')
            ax2.plot(mV, (hot_TP_mean-(hot_TP_std*std_num))*tp_scale, color="purple", linewidth=3, ls='dotted')
            ax2.plot(mV, (cold_TP_mean-(cold_TP_std*std_num))*tp_scale, color="blue", linewidth=3, ls='dotted')
        
 
        line1 = plt.Line2D(range(10), range(10), color="red")
        line2 = plt.Line2D(range(10), range(10),color="green")
        line3 = plt.Line2D(range(10), range(10),color="purple")
        line4 = plt.Line2D(range(10), range(10),color="blue")
        if standdev:
            line5 = plt.Line2D(range(10), range(10),color="black", ls='dotted')
            plt.legend((line1,line2,line3,line4,line5),('IV Sweep','Y factor', '300K Total Power', '77K Total Power',str(std_num) + '$\sigma$'),numpoints=1, loc=2)
        else:
            plt.legend((line1,line2,line3,line4),('IV Sweep','Y factor', '300K Total Power', '77K Total Power'),numpoints=1, loc=2)
        
        Y = max(Yfactor)
        plt.text(1, 127, str('%2.2f' % Y) + " maximum Y-Factor", fontsize=16, color="green")
        Tc = 80.0
        Th = 295.0
        T= (Y*Tc - Th)/(1-Y)
        plt.text(1, 117, str('%3.f' % T) + " lowest Receiver Temperature", fontsize=16, color="green")
        
        if do_title:
            ### get the hot Y factor data
            Ydatadir = prodatadir + Ynum + '/'
            paramsfile = Ydatadir + 'prohotparams.csv' 
            hot_K_val, hot_magisweep, hot_magiset, hot_magpot, hot_meanmag_V, hot_stdmag_V, hot_meanmag_mA, hot_stdmag_mA, hot_sisisweep, hot_sisiset, hot_UCA_volt, hot_meanSIS_mV, hot_stdSIS_mV, hot_meanSIS_uA, hot_stdSIS_uA, hot_meanSIS_tp, hot_stdSIS_tp, hot_SIS_pot, hot_del_time, hot_LOfreq, hot_IFband = getproparams(paramsfile)
            title_str = "Magnet current: " + str('%2.3f' % hot_meanmag_mA) + "mA,  SIS current at " + str('%2.3f' % hot_meanSIS_mV) + "mV (" + str('%2.3f' % hot_stdSIS_mV) +"): " + str('%2.3f' % hot_meanSIS_uA) + "$\mu$A (" + str('%2.3f' % hot_stdSIS_uA) +")"
            plt.title(title_str)
        
        
        
        ax1.set_xlabel('Voltage (mV)')
        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()
        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Ynum+".eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Ynum+".png")  
        
        if verbose:
            print " "
    plt.close("all")
    return

setnum = 2
search_4Ynums = False
Ynums = ['Y0009']
verbose = True
standdev = True
std_num  = 3

do_title  = False
show_plot = False
save_plot = True
do_eps    = True
show_fastIV = True

do_Ycut     = True
start_Yplot = 1.5 # in mV
end_Yplot   = 2.4 # in mV

datadir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set' + str(setnum) + '/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/initialize/'    
viewYfactorData(setnum, search_4Ynums, Ynums, verbose, standdev, std_num, do_title, show_plot, save_plot, do_eps, do_Ycut, start_Yplot, end_Yplot, datadir, show_fastIV)
    