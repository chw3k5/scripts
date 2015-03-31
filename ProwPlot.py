# Import this is the directory that has my scripts
from Plotting import SingleSpectraPlotter, YfactorSweepsPlotter, SimpleSweepPlot, YSpectraPlotter2D
from BiasSweep2 import BiasSweep
from datapro import SweepDataPro, YdataPro
from TestSweeper import testsweeps, protestsweeps, plottestsweeps
from profunc import windir

all_Single_Sweeps = False
all_Ydata         = False
all_testsweeps    = False
do_email = False
warning = False

### For Single Sweep ###
do_sweeps              = False
do_SweepDataPro        = False
do_SimpleSweepPlot     = False
do_SingeSpectraPlotter = False
repeat  = 1

### For Y-factor data and Sweeps ###
do_Ysweeps              = False
do_YdataPro             = True
do_YfactotSweepsPlotter = True
do_YSpectra_Plotter     = False





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
        BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, careful=False,
              testmode=False, warmmode=False, do_set_mag_highlow=True,
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=64000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=73000, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=True, high_res_meas=5,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=1.5, sisVsweep_stop=2.25, sisVsweep_step=0.1,
              sisVsweep_list=[-.1, -0.05, 0.0, 0.05, 0.1, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4],
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=60000, sisPot_feedTrue_stop=49000, sisPot_feedTrue_step=200,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=10,
              spec_sweep_time='AUTO', spec_video_band=30, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=500, aveNum=32,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=0.25,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=False, mag_meas=10,
              magisweep_start=46, magisweep_stop=43,magisweep_step=-2,
              magpotsweep_start=100000, magpotsweep_stop=70000, magpotsweep_step=-1250,
              do_LOuAsearch=True, UCA_meas=10,
              LOuAsearch_start=14, LOuAsearch_stop=9, LOuAsearch_step=-2,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=do_email, FiveMinEmail=do_email, PeriodicEmail=do_email,
              seconds_per_email=2*3600, chopper_off=True, do_LOuApresearch=False, biastestmode=False,
              warning=warning)


        if do_SweepDataPro:
            SweepDataPro(datadir, verbose=True, search_4Sweeps=True, search_str='Y', Snums=['00003'],
                         mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=False, sigma_mV=0.02, min_cdf_mV=0.95,
                         do_normspectra=True, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)

        if do_SimpleSweepPlot:
            SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True, show_standdev=True, std_num=3, display_params=True,
                            show_plot=False, save_plot=True, do_eps=False,
                            find_lin_mVuA=True, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                            der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                            plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=True, plot_fastmVtp=True,
                            plot_unpumpmVuA=True, plot_unpumpmVtp=True)

        if do_SingeSpectraPlotter:
            SingleSpectraPlotter(datadir, search_4Snums=True, Snums=[], verbose=False,
                                show_plot=False, save_plot=True, do_eps=False)






###########################
### For Y factor sweeps ###
###########################
if all_Ydata:
    do_YdataPro             = True
    do_YfactotSweepsPlotter = True
    do_YSpectra_Plotter     = True


# The directory what the data is kept
start_num = 0
#datadir   = '/Users/chw3k5/Google Drive/Kappa_preGoogleDrive/NA38/IVsweep/LO_PID_test'
datadir = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar28/LO_opt/'

if do_Ysweeps:
    sweep_num = start_num
    BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, careful=False,
              FinishedEmail=do_email, FiveMinEmail=do_email, PeriodicEmail=do_email,
              seconds_per_email=60*20, chopper_off=False, biastestmode=False,
              testmode=False, warmmode=False,sweepShape="rectangular",warning=warning,
              Kaxis=0, sisVaxis=1, magaxis=3, LOpowaxis=2, LOfreqaxis=4, IFbandaxis=5,

              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=66100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,

              do_sisVsweep=True, sisV_feedback=True, high_res_meas=5,
              sisVsweep_start=1.5, sisVsweep_stop=2.25, sisVsweep_step=0.1,
              sisVsweep_list=[-.100,-0.075 -0.050, -0.025, 0.00, 0.025, 0.05, 0.075, 0.100,
                              1.200, 1.250, 1.300, 1.350, 1.400, 1.450, 1.500, 1.550, 1.600, 1.650, 1.700, 1.750,
                              1.800, 1.850, 1.900, 1.950, 2.000, 2.050, 2.100, 2.150, 2.200, 2.250, 2.300, 2.3500, 2.400],
              sisPot_feedTrue_start=58000, sisPot_feedTrue_stop=54000, sisPot_feedTrue_step=200,
              sisPot_feedTrue_list=[65345,65150,64954,64687,64477,58107,57644,57253,56774,56295,55823,55357,54938,54463,54009],
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,

              TPSampleFrequency=100, TPSampleTime=2,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
              spec_sweep_time='AUTO', spec_video_band=100, spec_resol_band=100,
              spec_attenu=0, lin_ref_lev=500, aveNum=8,

              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=2,

              do_magisweep=False, mag_meas=10,
              magisweep_start=50, magisweep_stop=45, magisweep_step=-2,
              magi,
              magpotsweep_start=100000, magpotsweep_stop=70000-1, magpotsweep_step=-1250,

              do_LOuAsearch=True, do_LOuApresearch=False, UCA_meas=10,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              LOuAsearch_start=14, LOuAsearch_stop=9, LOuAsearch_step=-2,

              K_list=[296, 77],
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10
              )


if do_YdataPro:
    YdataPro(datadir, verbose=True, search_4Ynums=True, search_str='Y', Ynums=['Y0001'], useOFFdata=False, Off_datadir='',
             mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
             do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90,
             sigma_GHz=0.10)

if do_YfactotSweepsPlotter:
    YfactorSweepsPlotter(datadir, search_4Ynums=True, Ynums=[], verbose=True, mV_min=0, mV_max=5,
                         Y_mV_min=1.5, Y_mV_max=2.2,
                         plot_rawhot_mVuA=False, plot_rawhot_mVtp=True,
                         plot_rawcold_mVuA=False, plot_rawcold_mVtp=True,
                         show_standdev=False, std_num=1,
                         display_params=True, show_plot=False, save_plot=True, do_eps=False,
                         plot_mVuA=True, plot_mVtp=True, plot_Yfactor=True, plot_Ntemp=False,
                         find_lin_mVuA=False, find_lin_mVtp=False, find_lin_Yf=False,
                         plot_fastmVuA=True, plot_fastmVtp=False, plot_fastmVpot=False,
                         hotfast_find_lin_mVuA=False, coldfast_find_lin_mVuA=False,
                         plot_unpumpmVuA=True, plot_unpumpmVtp=False, plot_unpumpmVpot=False,
                         hotunpumped_find_lin_mVuA=True, coldunpumped_find_lin_mVuA=False,
                         linif=0.4, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                         do_xkcd=False)

if do_YSpectra_Plotter:
    YSpectraPlotter2D(datadir, search_4Ynums=True, Ynums=[], verbose=True,
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

if all_testsweeps:
    do_testsweeps     = True
    do_protestsweeps  = True
    do_plottestsweeps = True

datadir='/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Mar04_15/'
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
    testsweeps(datadir, do_SISsweep=True, do_MAGsweep=False, iscold=iscold, verbose=True,
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
                       find_lin=True, linif=1.1,
                       der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.05,
                       der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.10,
                       verbose=False)