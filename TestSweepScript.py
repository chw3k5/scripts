import sys
# Import this is the directory that has my scripts

platform = sys.platform
if platform == 'win32':
    func_dir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\scripts'
elif platform == 'darwin':
    func_dir = '/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
else:
    func_dir = 'platform/not/found/'

func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)

if platform == 'win32':
    datadir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\sweep\\warmmag\\'
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test5/'
    
from BiasSweep2 import BiasSweep
BiasSweep(datadir, verbose=False, verboseTop=True, careful=False,
sweepNstart=74, Ynum=0, testmode=False,
do_fastsweep=True, do_unpumpedsweep=True, fastsweep_feedback=False,
SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
SweepStart_feedFalse=65100, SweepStop_feedFalse=57000,
SweepStep_feedFalse=100,
sisV_feedback=True, do_sisVsweep=False, high_res_meas=5,
TPSampleFrequency=100, TPSampleTime=2,
sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000,
sisPot_feedFalse_step=100,
sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=48000,
sisPot_feedTrue_step=200,
getspecs=True, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30, spec_attenu=0,
Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
K_list=[296],
LOfreq_start=660, LOfreq_stop=660, LOfreq_step=1,
IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
do_magisweep=False, mag_meas=10,
magisweep_start=32, magisweep_stop=32, magisweep_step=1,
magpotsweep_start=37000, magpotsweep_stop=65000, magpotsweep_step=-500,
do_sisisweep=False, UCA_set_pot=56800, UCA_meas=10,
sisisweep_start=12, sisisweep_stop=12, sisisweep_step=1,
sisi_magpot=103323, sisi_cheat_num=56666,
UCAsweep_min=0.00, UCAsweep_max=0.00, UCAsweep_step=0.05,
sweepShape="rectangular",
FinishedEmail=True, FiveMinEmail=True, PeriodicEmail=True,
seconds_per_email=10000, chopper_off=True, presearch_LOuA=False)

from datapro    import SweepDataPro    
SweepDataPro(datadir, verbose=True, search_4Sweeps=True, search_str='Y',
Snums=[], mono_switcher=True, do_regrid=True, regrid_mesh=0.01,
do_conv=False, sigma=0.03, min_cdf=0.95)


from SimpleSweepPlot import SimpleSweepPlot
SimpleSweepPlot(datadir, search_4Snums=True, Snums='', verbose=True,
standdev=True, std_num=3, do_title=True, show_plot=False, save_plot=True,
do_eps=False, show_fastIV=True, show_unpumped=True, find_lin_mVuA=False,
linif=0.3,
der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05)
    
print "Test Sweep Script Finished!"