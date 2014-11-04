import sys, time, os, shutil, numpy
import matplotlib
from matplotlib import pyplot as plt
from datapro import windir, BasicDataPro
from control import setSIS_only, measSIS, setmag_only, measmag, setfeedback, zeroSISpot, zeroMAGpot, opentelnet, closetelnet
from profunc import getSnums,getproSweep, getpromagSweep
from BiasSweep2 import makeLists
from Plotting import allstarplotgen

platform = sys.platform

def testsweeps(datadir, do_SISsweep=True, do_MAGsweep=True, iscold=True,
               numofmeas=5, resttimeafterset=1,
               verbose=False, careful=False):
    ### Options
    if iscold:
        SISpot_min  =  65000
        SISpot_max  =  50000
        SISpot_step =    200
        MAGpot_min  =      0
        MAGpot_max  = 129000
        MAGpot_step =  10000
    else:
        SISpot_min  =  65000
        SISpot_max  =  58000
        SISpot_step =    500
        MAGpot_min  =      0
        MAGpot_max  = 129000
        MAGpot_step =  10000

    ### These options below have only been tested with default values
    feedback = True

    ### Set directory information
    rawdatadir = datadir + 'rawdata/'
    if platform == 'win32':
        rawdatadir = windir(rawdatadir)
    if not os.path.isdir(rawdatadir):
        os.makedirs(rawdatadir)

    ### find the other raw data that might be written in this same directory
    Snums = getSnums(rawdatadir)
    # name this new data something different
    Snum = 1
    while True:
        format_Snum = str('%05.f' % Snum)
        if format_Snum in Snums:
            Snum += 1
        else:
            break
    sweepdir = rawdatadir + format_Snum + '/sweep/'
    if not os.path.isdir(sweepdir):
        os.makedirs(sweepdir)

    ### Start the control part of the function
    # Open the connection to the THz bias computer
    opentelnet()

    # set the feedback
    status = setfeedback(feedback)

    # do a bias sweep of the sis junction
    if do_SISsweep:
        step_num = 0
        SISpot_list = makeLists(SISpot_min, SISpot_max, SISpot_step)
        for SISpot in SISpot_list:
            step_num += 1
            setSIS_only(SISpot, feedback, verbose, careful)
            if resttimeafterset is not None:
                time.sleep(resttimeafterset)

            # SIS bias measurements taken with the THz bias computer
            mV_sweep_list         = []
            uA_sweep_list         = []
            pot_sweep_list        = []
            for meas_index in range(numofmeas):
                mV_sweep, uA_sweep, pot_sweep = measSIS(verbose)
                mV_sweep_list.append(mV_sweep)
                uA_sweep_list.append(uA_sweep)
                pot_sweep_list.append(pot_sweep)

            # write the SIS bias data
            SISfilename = sweepdir + 'SIS' + str(step_num) + ".csv"

            if platform == 'win32':
                SISfilename = windir(SISfilename)
            sis_sweepData = open(SISfilename, 'w')
            sis_sweepData.write('mV, uA, pot \n')
            for sweep_index in range(numofmeas):
                mV_sis     = mV_sweep_list[sweep_index]
                uA_sis     = uA_sweep_list[sweep_index]
                pot_sis    = pot_sweep_list[sweep_index]
                meas_line = str(mV_sis) + ',' + str(uA_sis) + ',' + str(pot_sis) +'\n'
                sis_sweepData.write(meas_line)
                if verbose:
                    print meas_line
            sis_sweepData.close()

        # rezero the SIS pot
        status = zeroSISpot(verbose=True)

    if do_MAGsweep:
        step_num = 0
        MAGpot_list = makeLists(MAGpot_min, MAGpot_max, MAGpot_step)
        for MAGpot in MAGpot_list:
            step_num += 1
            setmag_only(MAGpot)
            if resttimeafterset is not None:
                time.sleep(resttimeafterset)

            # Electromagnet bias measurements taken with the THz bias computer
            V_sweep_list   = []
            mA_sweep_list  = []
            pot_sweep_list = []
            for meas_index in range(numofmeas):
                V, mA, pot = measmag(verbose)
                V_sweep_list.append(V)
                mA_sweep_list.append(mA)
                pot_sweep_list.append(pot)

            # write the MAG bias data
            MAGfilename = sweepdir + 'MAG' + str(step_num) + ".csv"

            if platform == 'win32':
                MAGfilename = windir(MAGfilename)
            sis_sweepData = open(MAGfilename, 'w')
            sis_sweepData.write('V, mA, pot \n')
            for sweep_index in range(numofmeas):
                V_mag     = V_sweep_list[sweep_index]
                mA_mag    = mA_sweep_list[sweep_index]
                pot_mag   = pot_sweep_list[sweep_index]
                meas_line = str(V_mag) + ',' + str(mA_mag) + ',' + str(pot_mag) +'\n'
                sis_sweepData.write(meas_line)
                if verbose:
                    print meas_line
            sis_sweepData.close()

        # rezero the MAG pot
        status = zeroMAGpot(verbose=True)

    ### Close the connection to the THz bias computer
    closetelnet()

    return

def protestsweeps(datadir, mono_switcher=True, do_regrid=True, do_conv=False,
                 regrid_mesh=0.01, min_cdf=0.9, sigma=0.05,
                 verbose=False):

    # get the names raw data directories
    rawdatadir = datadir + 'rawdata/'
    Snums = getSnums(rawdatadir)

    # make a new processed data directory or delete the old data
    prodatadir = datadir + "prodata/"
    if platform == 'win32':
        prodatadir = windir(prodatadir)
    if os.path.isdir(prodatadir):
        # remove old processed data
        shutil.rmtree(prodatadir)
        # make a folder for new processed data
        os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)

    for Snum in Snums:
        sweepdir = rawdatadir + Snum + '/sweep/'
        Snumdir = prodatadir + Snum + '/'
        if not os.path.isdir(Snumdir):
            os.makedirs(Snumdir)
        SISprodataname = Snumdir + 'SISdata.csv'
        MAGprodataname = Snumdir + 'MAGdata.csv'
        SISdatafound \
            = BasicDataPro(sweepdir, SISprodataname, is_SIS_data=True,
                           mono_switcher=mono_switcher, do_regrid=do_regrid, do_conv=do_conv,
                           regrid_mesh=regrid_mesh, min_cdf=min_cdf, sigma=sigma,
                           verbose=verbose)

        Magdatafound \
            = BasicDataPro(sweepdir, MAGprodataname, is_SIS_data=False,
                           mono_switcher=mono_switcher, do_regrid=do_regrid, do_conv=do_conv,
                           regrid_mesh=regrid_mesh, min_cdf=min_cdf, sigma=sigma,
                           verbose=verbose)



    return



def plottestsweeps(datadir, plot_SIS=True, plot_MAG=True,
                   show_std=True, std_num=1,
                   show_plot=False, save_plot=True, do_eps=True,
                   find_lin=False, linif=0.3,
                   der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                   der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                   verbose=False):


    ### Legend ###
    legendsize = 8
    legendloc  = 4

    prodatadir = datadir + "prodata/"
    Snums = getSnums(prodatadir)


    plotdir = datadir + "plots/"
    if platform == 'win32':
        plotdir = windir(plotdir)
    if os.path.isdir(plotdir):
        # remove old plots data
        shutil.rmtree(plotdir)
        # make a folder for plots
        os.makedirs(plotdir)
    else:
        # make a folder for new processed data
        os.makedirs(plotdir)


    for Snum in Snums:
        Snumdir = prodatadir + Snum + '/'
        SISdatafile = Snumdir + 'SIS'
        MAGdatafile = Snumdir + 'MAG'

        SIS_mV_mean, SIS_mV_std,  SIS_uA_mean, SIS_uA_std, SIS_TP_mean, SIS_TP_std, SIS_time_mean, SIS_pot, SIS_prodata_found\
            = getproSweep(SISdatafile)\

        MAG_V_mean, MAG_V_std,  MAG_mA_mean, MAG_mA_std, MAG_pot, MAG_prodata_found \
            = getpromagSweep(MAGdatafile)


        #################
        ### SIS Plots ###
        #################
        if((plot_SIS) and (SIS_prodata_found)):
            plot_list, leglines, leglabels \
                = allstarplotgen(SIS_mV_mean, SIS_uA_mean, y_std=SIS_uA_std, std_num=std_num,
                                 plot_list=[], leglines=[], leglabels=[],
                                 show_std=show_std, find_lin=find_lin,
                                 label='IV curve', std_label='sigma', lin_label=' Ohms',
                                 color='Chartreuse', lin_color='black',
                                 linw=5, std_linw=3, lin_linw=2,
                                 ls='-', std_ls='dotted', lin_ls='-',
                                 scale_str='', linif=linif,
                                 der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                                 der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                                 verbose=verbose)
            if (plot_list != []):
                fig, ax1 = plt.subplots()
                for plot_obj in plot_list:
                    (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
                    if verbose:
                        print 'ax1', scale_str, color, linw, ls, numpy.shape(x_vector), numpy.shape(y_vector)
                    scale_x_vector = numpy.array(x_vector)
                    scale_y_vector = numpy.array(y_vector)
                    ax1.plot(scale_x_vector, scale_y_vector, color=color, linewidth=linw, ls=ls)
                ### Axis Labels ###
                ax1.set_xlabel('Voltage (mV)')
                ax1.set_ylabel('Current (uA)')


                ### Legend ###
                final_leglines  = []
                final_leglabels = []
                for indexer in range(len(leglines)):
                    if ((leglines[indexer] != None) and (leglabels[indexer] != None)):
                        final_leglabels.append(leglabels[indexer])
                        legline_data = leglines[indexer]
                        color = legline_data[0]
                        ls    = legline_data[1]
                        linw  = legline_data[2]
                        final_leglines.append(plt.Line2D(range(10), range(10), color=color, ls=ls, linewidth=linw))
                matplotlib.rcParams['legend.fontsize'] = legendsize
                plt.legend(tuple(final_leglines),tuple(final_leglabels), numpoints=1, loc=legendloc)

            ### Save Plots ###
            if save_plot:
                if platform == 'win32':
                    do_eps = False
                if do_eps:
                    filename = plotdir+Snum+"_SIS.eps"
                else:
                    filename = plotdir+Snum+"_SIS.png"
                if verbose:
                    print "saving file:", filename
                plt.savefig(filename)

            ### Show Plots ###
            if show_plot:
                plt.show()
                plt.draw()
            else:
                plt.close("all")
            plt.close("all")
        #################
        ### MAG Plots ###
        #################
        if((plot_MAG) and (MAG_prodata_found)):
            plot_list, leglines, leglabels \
                = allstarplotgen(MAG_V_mean, MAG_mA_mean, y_std=MAG_mA_std, std_num=std_num,
                                 plot_list=[], leglines=[], leglabels=[],
                                 show_std=show_std, find_lin=find_lin,
                                 label='IV curve', std_label='sigma', lin_label=' Ohms',
                                 color='OrangeRed', lin_color='black',
                                 linw=5, std_linw=1, lin_linw=2,
                                 ls='-', std_ls='dotted', lin_ls='-',
                                 scale_str='', linif=linif,
                                 der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                                 der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                                 verbose=verbose)
            if (plot_list != []):
                fig, ax1 = plt.subplots()
                for plot_obj in plot_list:
                    (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
                    if verbose:
                        print 'ax1', scale_str, color, linw, ls, numpy.shape(x_vector), numpy.shape(y_vector)
                    scale_x_vector = numpy.array(x_vector)
                    scale_y_vector = numpy.array(y_vector)
                    ax1.plot(scale_x_vector, scale_y_vector, color=color, linewidth=linw, ls=ls)
                ### Axis Labels ###
                ax1.set_xlabel('Voltage (V)')
                ax1.set_ylabel('Current (mA)')


                ### Legend ###
                final_leglines  = []
                final_leglabels = []
                for indexer in range(len(leglines)):
                    if ((leglines[indexer] != None) and (leglabels[indexer] != None)):
                        final_leglabels.append(leglabels[indexer])
                        legline_data = leglines[indexer]
                        color = legline_data[0]
                        ls    = legline_data[1]
                        linw  = legline_data[2]
                        final_leglines.append(plt.Line2D(range(10), range(10), color=color, ls=ls, linewidth=linw))
                matplotlib.rcParams['legend.fontsize'] = legendsize
                plt.legend(tuple(final_leglines),tuple(final_leglabels), numpoints=1, loc=legendloc)

            ### Save Plots ###
            if save_plot:
                if platform == 'win32':
                    do_eps = False
                if do_eps:
                    filename = plotdir+Snum+"_MAG.eps"
                else:
                    filename = plotdir+Snum+"_MAG.png"
                if verbose:
                    print "saving file:", filename
                plt.savefig(filename)

            ### Show Plots ###
            if show_plot:
                plt.show()
                plt.draw()
            else:
                plt.close("all")
            plt.close("all")
    return




