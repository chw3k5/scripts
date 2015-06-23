__author__ = 'chwheele'
# Import this is the directory that has my scripts
from Plotting import SingleSpectraPlotter, YfactorSweepsPlotter, SimpleSweepPlot, YSpectraPlotter2D
from BiasSweep2 import BiasSweep
from datapro import SweepDataPro, YdataPro
from profunc import local_copy
from TestSweeper import testsweeps, protestsweeps, plottestsweeps
from profunc import windir


###########################
### For Y factor sweeps ###
###########################
### For Y-factor data and Sweeps ###
do_Ysweeps              = True
do_YdataPro             = True
do_YfactotSweepsPlotter = True
do_YSpectra_Plotter     = False

start_num = 1
norm_freq=2.3  # GHz
norm_band=0.015 # GHz
use_google_drive=False
do_email = False
warning  = False

parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'



            #                                     659,
            # 660,661,    663,664,        667,668,669,
            # 670,671,672,673,674,675,        678,
            # 680,681]
            # ,682,683,684,685,686,687,688,
            # 690]


            # 660,661,662,663,664,665,666,667,668,669,
            # 670,671,672,673,674,675,676,677,678,679,
            # 680,681,682,683,684,685,686,687,688,
            # 690,691,692
LOfreq_list=range(650,693)
for LOfreq in LOfreq_list:
    # The directory what the data is kept
    setnames = []
    # setnames.extend(['set4','set5','set6','set7','LOfreq'])
    # setnames.extend(['Mar28/LOfreq_wspec','Mar28/LOfreq_wspec2','Mar28/moonshot','Mar28/Mag_sweep','Mar28/LOfreq'])
    # setnames.extend(['Mar24_15/LO_power','Mar24_15/Yfactor_test'])
    # setnames.extend(['Nov05_14/Y_LOfreqMAGLOuA','Nov05_14/Y_MAG','Nov05_14/Y_MAG2','Nov05_14/Y_MAG3','Nov05_14/Y_standard'])
    # setnames.extend(['Oct20_14/LOfreq','Oct20_14/Y_LO_pow','Oct20_14/Y_MAG','Oct20_14/Y_MAG2','Oct20_14'])
    thisRun = 'Jun08_15/standingWaveTest6/'+str(int(LOfreq))+'/'
    setnames.extend([thisRun])
    datadir = parent_folder + thisRun


    if do_Ysweeps:
        sweep_num = start_num
        BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, careful=False,
              FinishedEmail=do_email, FiveMinEmail=do_email, PeriodicEmail=do_email,
              seconds_per_email=60*20, chopper_off=False, biastestmode=False,
              turnRFoff=False,
              testmode=False, warmmode=False,sweepShape="rectangular",warning=warning,
              Kaxis=0, sisVaxis=1, magaxis=3, LOpowaxis=2, LOfreqaxis=4, IFbandaxis=5,

              do_fastsweep=True, do_unpumpedsweep=False, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=66100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,

              do_sisVsweep=False, sisV_feedback=True, high_res_meas=5,
              sisVsweep_start=1.5, sisVsweep_stop=2.25, sisVsweep_step=0.1,
              sisVsweep_list=[0.5,0.55,0.6,0.65,0.7,0.75],
              sisPot_feedTrue_start=70000, sisPot_feedTrue_stop=54000, sisPot_feedTrue_step=200,
              sisPot_feedTrue_list=[63518,62006,60393,58549,56775],

              # [63518,  63140, 62762, 62384,
              #                       62006,  61628, 61250, 60872,
              #                       60393,  59924, 59461, 59039,
              #                       58549,  58111, 57638, 57173,
              #                       56775],



              # [65430, 65491, 65037, 64949, 64774, 64697, 64571, 64480,
              #                       61250, 61127, 60872, 60581, 60393, 60125, 59924, 59684,
              #                       59461, 59223, 59039, 58831, 58549, 58345, 58111, 57879, 57638, 57418, 57173, 56987,
              #                       56775, 56525, 56299, 56052, 55826, 55582, 55369, 55123, 54955, 54732, 54471, 54247, 54013]

              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,

              TPSampleFrequency=100, TPSampleTime=1,
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2],
              spec_sweep_time='AUTO', spec_video_band=300, spec_resol_band=300,
              spec_attenu=0, lin_ref_lev=500, aveNum=32,

              LOfreq_start=672 , LOfreq_stop=672, LOfreq_step=1,
              LOfreqs_list=[LOfreq],

              do_magisweep=False, mag_meas=10,
              magisweep_start=50, magisweep_stop=39, magisweep_step=-1,
              magisweep_list=[55],
              magpotsweep_start=110000, magpotsweep_stop=75000-1, magpotsweep_step=-1000,
              magpotsweep_list=[100000],

              do_LOuAsearch=False, do_LOuApresearch=False, LOuA_search_every_sweep=True,
              UCA_meas=40,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              UCAsweep_list=[0],
              LOuAsearch_start=30, LOuAsearch_stop=11, LOuAsearch_step=-1,
              LOuAsearch_list=[16],

              K_list=[296, 77],
              IFband_start=norm_freq, IFband_stop=norm_freq, IFband_step=0.10
              )





    fullpaths = [windir(parent_folder + setname ) for setname in setnames]
    for datadir in fullpaths:
        Ynums = []
        if Ynums ==[]:
            search4Ynums = True
        else:
            search4Ynums = False

        if do_YdataPro:
            YdataPro(datadir, verbose=True, search_4Ynums=search4Ynums, removeOldProData=True,
                     search_str='Y', Ynums=Ynums,
                     use_google_drive=use_google_drive,
                     useOFFdata=False, Off_datadir='',
                     mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01,
                     do_conv_mV=True, sigma_mV=0.03, min_cdf_mV=0.95,
                     remove_spikes=True, do_normspectra=True,
                     regrid_mesh_mV_spec=0.2, norm_freq=norm_freq, norm_band=norm_band,
                     do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)

        if not use_google_drive:
            datadir = local_copy(datadir)

        if do_YfactotSweepsPlotter:
            YfactorSweepsPlotter(datadir, search_4Ynums=search4Ynums, Ynums=Ynums, verbose=True, mV_min=0, mV_max=5,
                                 Y_mV_min=-0.4, Y_mV_max=2.5,
                                 plot_rawhot_mVuA=False, plot_rawhot_mVtp=True,
                                 plot_rawcold_mVuA=False, plot_rawcold_mVtp=True,
                                 show_standdev=False, std_num=1,
                                 display_params=True, show_plot=False, save_plot=True, do_eps=False,
                                 plot_mVuA=True, plot_mVtp=True, plot_Yfactor=True, plot_Ntemp=False,
                                 find_lin_mVuA=False, find_lin_mVtp=False, find_lin_Yf=False,
                                 plot_fastmVuA=True, plot_fastmVtp=False, plot_fastmVpot=False,
                                 hotfast_find_lin_mVuA=True, coldfast_find_lin_mVuA=False,
                                 plot_unpumpmVuA=True, plot_unpumpmVtp=False, plot_unpumpmVpot=False,
                                 hotunpumped_find_lin_mVuA=True, coldunpumped_find_lin_mVuA=False,
                                 linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                                 der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                                 do_xkcd=False)

        if do_YSpectra_Plotter:
            YSpectraPlotter2D(datadir, search_4Ynums=search4Ynums, Ynums=Ynums,
                              mV_min=0.5,mV_max=None, freq_vector = [0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2],
                              show_spikes=True, show_spike_label=False,
                              find_best_Yfactors=True,
                              verbose=True,display_params=True,
                              show_plot=False, save_plot=True, do_eps=False)



