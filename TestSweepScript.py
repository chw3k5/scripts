import sys
# Import this is the directory that has my scripts
do_sweeps   = False
do_pro      = True
do_simPlot  = True
do_specPlot = False



platform = sys.platform
if platform == 'win32':
    func_dir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\scripts'
elif platform == 'darwin':
    func_dir = '/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
else:
    func_dir = 'platform/not/found/'

from BiasSweep2 import BiasSweep
from datapro import SweepDataPro
from Plotting import SimpleSweepPlot, SingleSpectraPlotter



func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)

folder = 'DummyDewar'

if platform == 'win32':
    datadir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\sweep\\'+folder+'\\'
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'+folder+'/'
    

if do_sweeps:
    BiasSweep(datadir, verbose=False, verboseTop=True, verboseSet=True, careful=False,
              sweepNstart=0, Ynum=0, testmode=False, warmmode=False,
              do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=False, high_res_meas=5,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=60000, sisPot_feedTrue_stop=54110, sisPot_feedTrue_step=200,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
              spec_sweep_time='AUTO', spec_video_band=100, spec_resol_band=100,
              spec_attenu=0, lin_ref_lev=500, aveNum=8,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],
              LOfreq_start=650, LOfreq_stop=692, LOfreq_step=0.25,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=False, mag_meas=10,
              magisweep_start=40, magisweep_stop=29, magisweep_step=1,
              magpotsweep_start=1000, magpotsweep_stop=1000, magpotsweep_step=-4000,
              do_LOuAsearch=True, UCA_meas=10,
              LOuAsearch_start=12, LOuAsearch_stop=12, LOuAsearch_step=-1,
              LOuA_magpot=1000, LOuA_set_pot=56800,
              UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
              seconds_per_email=1800, chopper_off=False, do_LOuApresearch=False, biastestmode=True)


if do_pro:
    SweepDataPro(datadir, verbose=True, search_4Sweeps=True, search_str='Y', Snums=[],
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=True, sigma_mV=0.08, min_cdf_mV=0.95,
                 do_normspectra=True, norm_freq=1.42, norm_band=0.060, do_freq_conv=True, min_cdf_freq=0.90, sigma_GHz=0.10)


if do_simPlot:
    SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True, show_standdev=True, std_num=3, display_params=True,
                    show_plot=False, save_plot=True, do_eps=False,
                    find_lin_mVuA=True, linif=0.3, der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                    der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                    plot_astromVuA=True, plot_astromVtp=True, plot_fastmVuA=False, plot_fastmVtp=False,
                    plot_unpumpmVuA=False, plot_unpumpmVtp=False)
if do_specPlot:
    SingleSpectraPlotter(datadir, search_4Snums=True, Snums='', verbose=False,
                         show_plot=False, save_plot=True, do_eps=False)


    
print "Test Sweep Script Finished!"