import sys
# Import this is the directory that has my scripts
func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)

from BiasSweep2 import BiasSweep
###############################
####### General Options #######
###############################

verbose     = True   # default = True
verboseTop  = True   # default = True
careful     = False  # default = False
chooper_off = True

datadir     = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test4/' # no default setting
sweepNstart = 0   # (default = 0) starts on number after this, changes every sweep to be unique for each sweep
Ynum        = 0   # (default = 0) starts on number after this, changes every sweep to be unique for each sweep

testmode = True   # the default is False
#############################
####### Sweep Options #######
#############################
do_fastsweep         = True  # default is False
do_unpumpedsweep     = True  # default is False
fastsweep_feedback   = False # # default is False, this variable also used by unpumpedsweep
SweepStart_feedTrue  = 65000 # default is 65000 for feedback on
SweepStop_feedTrue   = 52000 # default is 52000 for feedback on
SweepStep_feedTrue   = 100   # default is 100

SweepStart_feedFalse = 65100 # default is 65100 for feedback off 
SweepStop_feedFalse  = 57000 # default is 57000 for feedback off
SweepStep_feedFalse  = 100   # default is 100

# Below is the main sweep type with high stablity for atronomical obsevations
sisV_feedback = True # default is True, if False the program will use valuse from fastsweep parameters above
do_sisVsweep  = True # default is True

high_res_meas = 10   # default is 5

TPSampleFrequency = 100 # default is 100 samples per second
TPSampleTime      =   2 # default is 2 seconds  

# do_sisVsweep is True then these three values are used
sisVsweep_start = -0.1 # default is -0.1 mV, -6 mV min
sisVsweep_stop  = 2.3  # default is  2.5 mV,  6 mV max
sisVsweep_step  = 0.05 # default is  0.1 mV

# do_sisVsweep is False then one set of three values from these six are used
sisPot_feedTrue_start  = 65000 # default is 65000 for feedback on
sisPot_feedTrue_stop   = 52000 # default is 52000 for feedback on
sisPot_feedTrue_step   = 100   # default is 100

sisPot_feedFalse_start = 65100 # default is 65100 for feedback off 
sisPot_feedFalse_stop  = 57000 # default is 57000 for feedback off
sisPot_feedFalse_step  = 100   # default is 100

# 0 changes the most often, the higher the axis the less common switching becomes
Kaxis      = 0 # default = 0, however for stability reasons, this should be set to 0 always
sisVaxis   = 1 # default = 1
magaxis    = 2 # default = 2
LOpowaxis  = 3 # default = 3
LOfreqaxis = 4 # default = 4
IFbandaxis = 5 # default = 5

K_list       = [296] # default is 296 Kelvin [296], [77], [300], [77, 300], or [300, 77]

LOfreq_start = 672 # default is 672 GHz
LOfreq_stop  = 672 # default is 672 GHz
LOfreq_step  =   1 # default is   1 GHz

IFband_start = 1.42 # default is 1.42 GHz
IFband_stop  = 1.42 # default is 1.42 GHz
IFband_step  = 0.10 # default is 0.10 GHz

do_magisweep       = False # default is True
mag_meas           = 10 # default is 10 measurements (measure the magnet at the start of a new bias sweep)

magisweep_start    = 25 # default is 32 mA, -42 in min 
magisweep_stop     = 40 # default is 32 mA,  42 is max
magisweep_step     =  2 # default is  2 mA

magpotsweep_start  = 40000 # default is 40000 potentiometer position,       0 is min 
magpotsweep_stop   = 40000 # default is 40000 potentiometer position, 1279797 is max
magpotsweep_step   =  5000 # default is  5000 potentiometer position


do_sisisweep       = False  # default is True
sisi_set_pot        = 56800 # default is 56800 potentiometer position
UCA_meas           =    10 # default is 10 measurements (measure the LO power at the start of a new bias sweep)

sisisweep_start =  4 # default is 12 uA
sisisweep_stop  = 14 # default is 12 uA
sisisweep_step  =  1 # default is  1 uA
sisi_magpot     = 103323 # default is 103323 potentiometer position
sisi_cheat_num  =  56666 # default is  56666 potentiometer position

UCAsweep_min  = 3.45 # default is 3.45 Volts
UCAsweep_max  = 3.45 # default is 3.45 Volts
UCAsweep_step = 0.05 # default is 0.05 Volts

#########################
###### Sweep Shape ######
#########################

sweepShape  = "rectangular" # default is rectangular

#############################
####### Email Options #######
#############################
FinishedEmail     = True # default is False
FiveMinEmail      = True # default is False
PeriodicEmail     = True # default is False
seconds_per_email = 20*60 # default is 20 mins or 20*60=1200 seconds (60 s = 1 min, 3600 s = 1 hour ) 

test = BiasSweep(datadir=datadir, K_list=K_list, testmode=False, Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3,
                 LOfreqaxis=4, IFbandaxis=5, sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=56000,
                 sisPot_feedTrue_step=2000, magpotsweep_start=40000, magpotsweep_stop=30000, magpotsweep_step=5000)
