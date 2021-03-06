# Import this is the directory that has my scripts
from Plotting import SingleSpectraPlotter, YfactorSweepsPlotter, SimpleSweepPlot, YSpectraPlotter2D
from biasSweep3 import BiasSweep
from datapro import SweepDataPro, YdataPro
from profunc import local_copy
from TestSweeper import testsweeps, protestsweeps, plottestsweeps
from profunc import windir

all_Single_Sweeps = False
all_Ydata         = False
all_testsweeps    = False
do_email = True
warning = True

### For Single Sweep ###
do_sweeps              = False
do_SweepDataPro        = False
do_SimpleSweepPlot     = False
do_SingeSpectraPlotter = False
repeat  = 1





####################
### The Programs ###
####################

### For Single Sweeps ###
if all_Single_Sweeps:
    do_SweepDataPro        = True
    do_SimpleSweepPlot     = True
    do_SingeSpectraPlotter = True

# The directory what the data is kept
datadir = windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar04_15/LO_PID_test/')
start_num = 0
if do_sweeps:
    for repeat_num in range(repeat):
        sweep_num = repeat_num+start_num
        BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True,
              testMode=False, warmmode=False,
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=64000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=73000, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=True, SISbiasMeasNum=5,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=1.5, sisVsweep_stop=2.25, sisVsweep_step=0.1,
              sisVsweep_list=[-.1, -0.05, 0.0, 0.05, 0.1, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4],
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=60000, sisPot_feedTrue_stop=49000, sisPot_feedTrue_step=200,
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2],
              spec_sweep_time='AUTO', spec_video_band=30, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=300, aveNum=32,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=0.25,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=False, mag_meas=10,
              magisweep_start=46, magisweep_stop=43,magisweep_step=-2,
              magpotsweep_start=100000, magpotsweep_stop=70000, magpotsweep_step=-1250,
              do_LOuAsearch=True, benchMAGmeasNum=5,benchSISmeasNum=5,
              LOuAsearch_start=14, LOuAsearch_stop=9, LOuAsearch_step=-2,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=do_email, FiveMinEmail=do_email, PeriodicEmail=do_email,
              seconds_per_email=2*3600, chopper_off=True, do_LOuApresearch=False, biasOnlyMode=False,
              warning=warning)


        if do_SweepDataPro:
            SweepDataPro(datadir, verbose=True, search_4Sweeps=True, search_str='Y', Snums=['00003'],
                         mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01,
                         do_conv_mV=False, sigma_mV=0.02, min_cdf_mV=0.95,
                         do_normspectra=True, norm_freq=1.42, norm_band=0.060,
                         do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)

        if do_SimpleSweepPlot:
            SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True,
                            show_standdev=True, std_num=3, display_params=True,
                            show_plot=False, save_plot=True, do_eps=False,
                            find_lin_mVuA=True, linif=0.3,
                            der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                            der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                            plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=True, plot_fastmVtp=True,
                            plot_unpumpmVuA=True, plot_unpumpmVtp=True)

        if do_SingeSpectraPlotter:
            SingleSpectraPlotter(datadir, search_4Snums=True, Snums=[], verbose=False,
                                show_plot=False, save_plot=True, do_eps=False)






###########################
### For Y factor sweeps ###
###########################
### For Y-factor data and Sweeps ###
do_Ysweeps              = False
do_YdataPro             = False
do_YfactotSweepsPlotter = True
do_YSpectra_Plotter     = False

start_num = 1
norm_freq = 2.3  # GHz
norm_band = 0.015 # GHz
use_google_drive=False
do_email = False
warning  = True

# The directory what the data is kept
setnames = []
# setnames.extend(['set4','set5','set6','set7','LOfreq'])
# setnames.extend(['Mar28/LOfreq_wspec','Mar28/LOfreq_wspec2','Mar28/moonshot','Mar28/Mag_sweep','Mar28/LOfreq'])
# setnames.extend(['Mar24_15/LO_power','Mar24_15/Yfactor_test'])
# setnames.extend(['Nov05_14/Y_LOfreqMAGLOuA','Nov05_14/Y_MAG','Nov05_14/Y_MAG2','Nov05_14/Y_MAG3','Nov05_14/Y_standard'])
# setnames.extend(['Oct20_14/LOfreq','Oct20_14/Y_LO_pow','Oct20_14/Y_MAG','Oct20_14/Y_MAG2','Oct20_14'])
# setnames.extend(['Jun08_15/RandS'])
# setnames.extend(['Alice/LOfreq650-655/rerun','Alice/LOfreq655-660/rerun','Alice/LOfreq660-665/rerun','Alice/LOfreq665-670/rerun','Alice/LOfreq670-675/rerun'])
setnames.append('Alice_3p/LOfreq664-666/rerun')
parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'
fullpaths = [windir(parent_folder + setname + '/') for setname in setnames]
for datadir in fullpaths:
    Ynums = []
    if Ynums ==[]:
        search4Ynums = True
    else:
        search4Ynums = False
    if do_Ysweeps:
        sweep_num = start_num
    if do_Ysweeps:
        BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, #careful=False,

              # Parameter sweep behaviour
              Kaxis=0, sisVaxis=1, magaxis=3, LOpowaxis=2, LOfreqaxis=4, IFbandaxis=5,
              testMode=False, testModeWaitTime=1, warmmode=False, turnRFoff=True,
              chopper_off=False, biasOnlyMode=False,
              warning=True,
              sweepShape="rectangular",
              dwellTime_BenchmarkSIS=5,
              dwellTime_BenchmarkMag=5,
              dwellTime_fastSweep=5,
              dwellTime_unpumped=5,
              dwellTime_sisVsweep=1,

              # email options
              FinishedEmail=do_email, FiveMinEmail=do_email, PeriodicEmail=do_email,
              emailGroppi=False,
              seconds_per_email=1200,

              ## Benchmark Tests
              do_benchmarkSIS=True,
              do_benchmarkMag=True,
              # measure the electromagnet and the SIS junction at their standard positions
              benchSISmeasNum=10,benchMAGmeasNum=5,
              # THz computer fast sweeps
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=66100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,

              # mV sweep Parameters
              sisV_feedback=True, do_sisVsweep=False, SISbiasMeasNum=5,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
              sisVsweep_list=None,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_list=[63518,  63140, 62762, 62384,
                                    62006,  61628, 61250, 60872,
                                    60393,  59924, 59461, 59039,
                                    58549,  58111, 57638, 57173,
                                    56775],

              # [65430, 65491, 65037, 64949, 64774, 64697, 64571, 64480,
              #                       61250, 61127, 60872, 60581, 60393, 60125, 59924, 59684,
              #                       59461, 59223, 59039, 58831, 58549, 58345, 58111, 57879, 57638, 57418, 57173, 56987,
              #                       56775, 56525, 56299, 56052, 55826, 55582, 55369, 55123, 54955, 54732, 54471, 54247, 54013]
              sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
              sisPot_feedFalse_list=None,

              # Powermeter read through LabJack
              TPSampleFrequency=100, TPSampleTime=2,

              # spectrum analyzer settings
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[0.0,0.4,1.0,1.6,2.2,2.5,2.8,3.1,3.4,4.0,4.6,5.2,6.4,12.4,24.4],
              spec_sweep_time='AUTO', spec_video_band=300, spec_resol_band=300,
              spec_attenu=0, lin_ref_lev=500, aveNum=64,

              # Chopper temperature list
              K_list=[296,78],

              # Local Ocsillator frequency selector
              LOfreq_start=650, LOfreq_stop=692, LOfreq_step=1,
              LOfreqs_list=None,

              # Intermediate Frequency Band
              IFband_start=norm_freq, IFband_stop=norm_freq, IFband_step=0.10,

              # Electromagnet Options
              do_magisweep=False, mag_meas=10,
              magisweep_start=32, magisweep_stop=32, magisweep_step=1,
              magisweep_list=None,
              magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
              magpotsweep_list=[100000],

              # setting the local ocsilattor pump power
              do_LOuAsearch=False,  do_LOuApresearch=False, LOuA_search_every_sweep=False,
              UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
              UCAsweep_list=[0],
              LOuAsearch_start=14, LOuAsearch_stop=14, LOuAsearch_step=1,
              LOuAsearch_list=[16],

              # stepper motor control options
              stepper_vel = 0.5, stepper_accel = 1, forth_dist = 0.25, back_dist = 0.25)

    if do_YdataPro:
        YdataPro(datadir, verbose=True, search_4Ynums=search4Ynums, removeOldProData=False,
                 search_str='Y', Ynums=Ynums,
                 use_google_drive=use_google_drive,
                 useOFFdata=False, Off_datadir='',
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01,
                 do_conv_mV=True, sigma_mV=0.05, min_cdf_mV=0.95,
                 remove_spikes=True, do_normspectra=True,
                 regrid_mesh_mV_spec=0.2, norm_freq=norm_freq, norm_band=norm_band,
                 do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.05)

    if not use_google_drive:
        datadir = local_copy(datadir)

    if do_YfactotSweepsPlotter:
        YfactorSweepsPlotter(datadir, search_4Ynums=search4Ynums, Ynums=Ynums, verbose=True, mV_min=0, mV_max=5,
                             Y_mV_min=0.4, Y_mV_max=2.5,
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
                             linif=0.2, der1_int=1, do_der1_conv=True, der1_min_cdf=0.60, der1_sigma=0.05,
                             der2_int=1, do_der2_conv=True, der2_min_cdf=0.60, der2_sigma=0.05,
                             do_xkcd=False)

    if do_YSpectra_Plotter:
        YSpectraPlotter2D(datadir, search_4Ynums=search4Ynums, Ynums=Ynums,
                          mV_min=0.5,mV_max=None, freq_vector = [0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2],
                          show_spikes=True, show_spike_label=False,
                          find_best_Yfactors=True,
                          verbose=True,display_params=True,
                          show_plot=False, save_plot=True, do_eps=False)




### TestSweeps ###
do_testsweeps     = False
do_protestsweeps  = False
do_plottestsweeps = False
istester     = False
isdummydewar = False
istestcirc   = False
istestpixel  = False
iscold       = True

do_SISsweep = True
do_MAGsweep = True

if all_testsweeps:
    do_testsweeps     = True
    do_protestsweeps  = True
    do_plottestsweeps = True

datadir='/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Jun08_15/'
if istester:
    datadir += 'test/'
elif isdummydewar:
     datadir += 'dummydewar/'
elif istestcirc:
    datadir += 'testcircuit/'
elif istestpixel:
    datadir += 'testpixel/'
elif iscold:
    datadir += 'coldtest/'
else:
    datadir += 'warmtest/'

datadir = windir(datadir)
if do_testsweeps:
    testsweeps(datadir, do_SISsweep=do_SISsweep, do_MAGsweep=do_MAGsweep, iscold=iscold, verbose=True,
               numofmeas=10)

if do_protestsweeps:
    protestsweeps(datadir,
                  mono_switcher=True, do_regrid=True, do_conv=False,
                  regrid_mesh=0.01, min_cdf=0.9, sigma=0.01,
                  verbose=False)

if do_plottestsweeps:
    plottestsweeps(datadir, plot_SIS=True, plot_MAG=True,
                       show_std=True, std_num=10,
                       show_plot=False, save_plot=True, do_eps=True,
                       find_lin=True, linif=0.3,
                       der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.05,
                       der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.10,
                       verbose=False)