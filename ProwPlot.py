# Import this is the directory that has my scripts
from Plotting import SingleSpectraPlotter, YfactorSweepsPlotter, SimpleSweepPlot, YSpectraPlotter
from BiasSweep2 import BiasSweep
from datapro import SweepDataPro, YdataPro
from TestSweeper import testsweeps, protestsweeps, plottestsweeps

all_Single_Sweeps = False
all_Ydata         = False
all_testsweeps    = False

### For Single Sweep ###
do_sweeps              = False
do_SweepDataPro        = False
do_SimpleSweepPlot     = False
do_SingeSpectraPlotter = False

### For Y-factor data and Sweeps ###
do_Ysweeps              = False
do_YdataPro             = True
do_YfactotSweepsPlotter = True
do_YSpectra_Plotter     = False

### TestSweeps ###
do_testsweeps     = False
do_protestsweeps  = False
do_plottestsweeps = False
iscold = True


####################
### The Programs ###
####################

### For Single Sweeps ###
if all_Single_Sweeps:
    do_SweepDataPro        = True
    do_SimpleSweepPlot     = True
    do_SingeSpectraPlotter = True

# The directory what the data is kept
datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/Oct20_14/LOfreq/'

if do_sweeps:
        BiasSweep(datadir, verbose=False, verboseTop=True, verboseSet=True, careful=False,
              sweepNstart=0, Ynum=0, testmode=False, warmmode=False,
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=64100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=False, high_res_meas=8,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=60000, sisPot_feedTrue_stop=52110, sisPot_feedTrue_step=200,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=10,
              spec_sweep_time='AUTO', spec_video_band=30, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=500, aveNum=32,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],
              LOfreq_start=650, LOfreq_stop=692, LOfreq_step=0.25,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=False, mag_meas=10,
              magisweep_start=40, magisweep_stop=29, magisweep_step=1,
              magpotsweep_start=12000, magpotsweep_stop=12000, magpotsweep_step=200,
              do_LOuAsearch=True, UCA_meas=10,
              LOuAsearch_start=14, LOuAsearch_stop=8, LOuAsearch_step=-1,
              LOuA_magpot=1000, LOuA_set_pot=56800,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=True, FiveMinEmail=True, PeriodicEmail=True,
              seconds_per_email=14400, chopper_off=False, do_LOuApresearch=False, biastestmode=False)


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
    SingleSpectraPlotter(datadir, search_4Snums=True, Snums='', verbose=False,
                        show_plot=False, save_plot=True, do_eps=False)









### For Y factor sweeps ###
if all_Ydata:
    do_YdataPro             = True
    do_YfactotSweepsPlotter = True
    do_YSpectra_Plotter     = True


# The directory what the data is kept
datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/Oct20_14/Y_MAG2/'

if do_Ysweeps:
    BiasSweep(datadir, verbose=False, verboseTop=True, verboseSet=True, careful=False,
              sweepNstart=6, Ynum=6, testmode=False, warmmode=False,
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=False, high_res_meas=8,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=60000, sisPot_feedTrue_stop=52110, sisPot_feedTrue_step=200,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
              spec_sweep_time='AUTO', spec_video_band=100, spec_resol_band=100,
              spec_attenu=0, lin_ref_lev=500, aveNum=8,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296, 77],
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=0.25,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=False, mag_meas=10,
              magisweep_start=40, magisweep_stop=29, magisweep_step=1,
              magpotsweep_start=12400, magpotsweep_stop=50001, magpotsweep_step=400,
              do_LOuAsearch=True, UCA_meas=10,
              LOuAsearch_start=12, LOuAsearch_stop=12, LOuAsearch_step=-1,
              LOuA_magpot=1000, LOuA_set_pot=56800,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=True, FiveMinEmail=False, PeriodicEmail=True,
              seconds_per_email=7200, chopper_off=False, do_LOuApresearch=False, biastestmode=False)


if do_YdataPro:
    YdataPro(datadir, verbose=True, search_4Ynums=True, search_str='Y', Ynums=[], useOFFdata=False, Off_datadir='',
             mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
             do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90,
             sigma_GHz=0.10)

if do_YfactotSweepsPlotter:
    YfactorSweepsPlotter(datadir, search_4Ynums=True, Ynums='', verbose=True, mV_min=-0, mV_max=None,
                         show_standdev=True, std_num=1,
                         display_params=True, show_plot=False, save_plot=True, do_eps=False,
                         plot_mVuA=True, plot_mVtp=True, plot_Yfactor=True, plot_Ntemp=False,
                         find_lin_mVuA=False, find_lin_mVtp=False, find_lin_Yf=False,
                         plot_fastmVuA=True, plot_fastmVtp=False, plot_fastmVpot=False,
                         hotfast_find_lin_mVuA=False, coldfast_find_lin_mVuA=False,
                         plot_unpumpmVuA=True, plot_unpumpmVtp=False, plot_unpumpmVpot=False,
                         hotunpumped_find_lin_mVuA=True, coldunpumped_find_lin_mVuA=False,
                         linif=0.4, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                         der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                         do_Ycut=False, start_Yplot=1, end_Yplot=2)

if do_YSpectra_Plotter:
    YSpectraPlotter(datadir, search_4Ynums=True, Ynums='', verbose=True,
                    show_plot=False, save_plot=True, do_eps=False)





if all_testsweeps:
    do_testsweeps     = True
    do_protestsweeps  = True
    do_plottestsweeps = True

datadir='/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/Oct20_14/'
if iscold:
    datadir += 'coldtest/'
else:
    datadir += 'warmtest/'
if do_testsweeps:
    testsweeps(datadir, do_SISsweep=True, do_MAGsweep=True, iscold=iscold, verbose=True)

if do_protestsweeps:
    protestsweeps(datadir,
                  mono_switcher=True, do_regrid=True, do_conv=False,
                  regrid_mesh=0.01, min_cdf=0.9, sigma=0.01,
                  verbose=False)

if do_plottestsweeps:
    plottestsweeps(datadir, plot_SIS=True, plot_MAG=True,
                       show_std=True, std_num=10,
                       show_plot=False, save_plot=True, do_eps=True,
                       find_lin=True, linif=0.4,
                       der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.05,
                       der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.10,
                       verbose=False)