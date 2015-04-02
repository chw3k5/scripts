### Test functions in this script ###


# Import this is the directory that has my scripts
import sys
from control import opentelnet, closetelnet, default_sispot, default_magpot

#############################
###### From control.py ######
#############################
do_LabJackU3_DAQ0 = False # True or False
do_LabJackU3_AIN0 = False # True or False
do_LJ_streamTP    = False # True or False

do_measmag          = False # True or False
do_measmag_w_offset = False # True or False
do_setmag           = True # True or False
do_setmag_only      = False # True or False
do_Emag_PID         = False # True or False

do_RFfreqset   = True # True or False
do_RFon        = True # True or False
do_RFoff       = False # True or False

do_measSIS     = False # True or False
do_setfeedback = False # True or False
do_setSIS      = False # True or False
do_setSIS_only = False # True or False
do_setSIS_TP   = False # True or False
do_measSIS_TP  = False # True or False

do_setLOI      = True# True or False

do_setSIS_Volt = True # True or False

do_zeropots    = False # True of False


############################
###### From domath.py ######
############################

do_AllanVar    = False # True or False

####################################
###### From StepperControl.py ######
####################################

do_stepperTest = False
 # True or False

#####################################
###### From LabJack_control.py ######
#####################################

if do_LabJackU3_DAQ0:
    from LabJack_control import LabJackU3_DAQ0
    UCA_voltage = 4.3 # Volts in (0,5)
    status = LabJackU3_DAQ0(UCA_voltage)

if do_LabJackU3_AIN0:
    from LabJack_control import LabJackU3_AIN0
    tp = LabJackU3_AIN0()

if do_LJ_streamTP:
    from LabJack_control import LJ_streamTP
    #filename        = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test/data.txt"
    filename        = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\test\\data.txt"
    SampleFrequency =      100  # samples per second
    SampleTime      = float(10) # in seconds 
    verbose         = True
    LJ_streamTP(filename, SampleFrequency, SampleTime, verbose)


#############################
###### From control.py ######
#############################
opentelnet()
if do_measmag:
    from control import measmag
    verbose = True  # True or False
    V_mag, mA_mag, pot_mag = measmag(verbose)
    print str(V_mag) + "=V_mag, " + str(mA_mag) + "=mA_mag, " + str(pot_mag) + "=pot_mag"

if do_measmag_w_offset:
    from control import measmag_w_offset
    verbose = True
    #offset_mA, magpot = measmag_w_offset(filename='', path='', verbose=verbose)
    offset_mA, magpot = measmag_w_offset(verbose=verbose)
    print "offset_mA:", offset_mA, '  magpot:', magpot


if do_setmag:
    from control import setmag
    magpot = default_magpot # electromagnet potentiometer position
    verbose = True  # True or False
    V_mag, mA_mag, pot_mag = setmag(magpot, verbose)
    print str(V_mag) + "=V_mag, " + str(mA_mag) + "=mA_mag, " + str(pot_mag) + "=pot_mag"

if do_setmag_only:
    from control import setmag_only
    magpot = default_magpot # electromagnet potentiometer position
    setmag_only(magpot)

if do_Emag_PID:
    from PID import Emag_PID
    from control import measmag_w_offset
    mA_user = 45 # mA in [-80,78]
    verbose = True  # True or False
    test_path = 'C:\\Users\\chwheele\\Google Drive\\Kappa\\NA38\\IVsweep\\Mar04_15\\LO_stability_test\\rawdata\\00001\\'
    Emag_PID(local_path=test_path, mA_set=45.0, verbose=verbose)
    offset_mA, magpot = measmag_w_offset(verbose=verbose)
    print "offset_mA:", offset_mA, '  magpot:', magpot

#############################
###### From LOinput.py ######
#############################
if do_RFfreqset:
    from LOinput import  setfreq            
    freq = 672 # in GHz
    setfreq(freq)
    
if do_RFon:
    from LOinput import RFon    
    RFon()
    
if do_RFoff:
    from LOinput import RFoff    
    RFoff()

#############################
###### From control.py ######
#############################
if do_measSIS:
    from control import measSIS
    verbose = True  # True or False
    mV_sis, uA_sis, pot_sis = measSIS(verbose)
    print str(mV_sis) + "=mV_sis, " + str(uA_sis) + "=uA_sis, " + str(pot_sis) + "=pot_sis"
    
if do_setfeedback:
    from control import setfeedback
    feedback = True # True or False
    status   = setfeedback(feedback)

if do_setSIS:
    from control import setSIS
    sispot   = 55500 # potentiometer position for the SIS bias
    feedback = True  # True or False, True (V mode), False (R mode)
    verbose  = True  # True or False
    careful   = False # True or False
    mV_sis, uA_sis, pot_sis = setSIS(sispot, feedback, verbose, careful)
    print str(mV_sis) + "=mV_sis, " + str(uA_sis) + "=uA_sis, " + str(pot_sis) + "=pot_sis"
    
if do_setSIS_only:
    from control import setSIS_only
    sispot   = 64000 # potentiometer position for the SIS bias
    feedback = True  # True or False, True (V mode), False (R mode)
    verbose  = True  # True or False
    careful   = False # True or False
    setSIS_only(sispot, feedback, verbose, careful)

if do_setSIS_TP:
    from control import setSIS_TP
    sispot   = 58253 # potentiometer position for the SIS bias
    feedback = True  # True or False, True (V mode), False (R mode)
    verbose  = True  # True or False
    careful  = False # True or False  
    mV_sis, uA_sis, tp_sis, pot_sis = setSIS_TP(sispot, feedback, verbose, careful)
    print str(mV_sis) + "=mV_sis, " + str(uA_sis) + "=uA_sis, " + str(tp_sis) + "=tp_sis, " + str(pot_sis) + "=pot_sis"

if do_measSIS_TP:
    from control import measSIS_TP
    sispot   = 58253 # potentiometer position for the SIS bias
    feedback = True  # True or False, True (V mode), False (R mode)
    verbose  = True  # True or False
    careful  = False # True or False    
    mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(sispot, feedback, verbose, careful)
    print str(mV_sis) + "=mV_sis, " + str(uA_sis) + "=uA_sis, " + str(tp_sis) + "=tp_sis, " + str(pot_sis) + "=pot_sis, " + str(time_stamp) + "=time_stamp"


if do_setLOI:
    from PID import LO_PID
    final_V, final_deriv = LO_PID(uA_set=16.0,
           feedback=True, max_adjust_attempt=20, min_adjust_attempt=5,
           highres_meas_after_diff=0.2,
           lowres_sleep_per_set=0.5, highres_sleep_per_set=3,
           lowres_measnumber=1, highres_meas_number=5,
           uA_search_res = 10,
           min_diff_V=0.001,
           V_min=0,V_max=5,
           Kp=1.0, Ki=0.0, Kd=0.05, verbose=True)


if do_setSIS_Volt:
    from PID import SIS_mV_PID
    sispot_current, final_deriv = SIS_mV_PID(mV_set=1.2, mV_set_max=10, mV_set_min=-10,
                feedback=True, max_adjust_attempt=20, min_adjust_attempt=5,
                sleep_per_set=2, meas_number=5, high_meas_after_diff=0.2,
                min_diff_sispot=3,
                first_pot=65100, second_pot=56800,
                Kp=1.0, Ki=0.0, Kd=0.05, verbose=True)

if do_zeropots:
    from control import zeropots
    verbose   = True  # True or False
    status = zeropots(verbose)



############################
###### From domath.py ######
############################

if do_AllanVar:
    from domath import AllanVar
    s_time = 60 # in seconds
    M = 2  # number of measuemnets to compare. must be greater than 2
    mesh = 1 # in seconds
    tau = 1  # in seconds
    feedback = True
    do_save_data = True
    mV_list, uA_list, tp_list, time_list, regrid_data, Variance = AllanVar(s_time, M, tau, feedback)
    

####################################
###### From StepperControl.py ######
####################################

if do_stepperTest:
    import StepperControl
    import time
    status = StepperControl.initialize()
    time.sleep(1)
    status = StepperControl.GoForth()
    time.sleep(1)
    status = StepperControl.DisableDrive()



closetelnet()
#from control import restartTelnet
#restartTelnet(1)