__author__ = 'chwheele'
from LabJack_control import LabJackU3_DAQ0
from calibration import magpot_lookup, default_path
from time import sleep
import numpy as np
from control import mag_channel, measSIS, measmag, setSIS_only, setmag_only

def Emag_PID(local_path=default_path, mA_set=35.0, start_overshoot_mA=2.0, sleep_per_set=2, meas_number=5,
             min_diff=0.01, Kp=1.0, Ki=1.0, Kd=1.0, verbose=False):
    def measloop(mA_to_find, meas_number=1):
        magpot = magpot_lookup(mA_to_find, mag_channel=mag_channel, local_lookup_filepath=local_path)
        setmag_only(magpot_current)
        sleep(sleep_per_set)

        mA_list = []
        for n in range(meas_number):
            V_temp, mA_temp, pot_temp = measmag(verbose)
            mA_list.append(mA_temp)
        mA = np.mean(mA_list)
        return mA, magpot

    # initialize
    mA_set=float(mA_set)
    mA_set_sign = int(mA_set/abs(mA_set))

    # first measurement (full overshoot)
    overshoot_mA = mA_set_sign*start_overshoot_mA+mA_set
    mA_current, magpot_current = measloop(mA_to_find=overshoot_mA, meas_number=meas_number)
    error = mA_set - mA_current

    # second measurement (half overshoot)
    mA_last     = mA_current
    magpot_last = magpot_current
    error_last  = error

    halfovershoot_mA = mA_set_sign*(start_overshoot_mA/2.0)+mA_set
    mA_current, magpot_current = measloop(mA_to_find=halfovershoot_mA, meas_number=meas_number)







    # initial error function
    error_sum = 0.
    error = mA_set - mA_current
    magpot_diff = float(magpot_current-magpot_last)
    int_error = Ki*error*magpot_diff
    error_sum += int_error
    # only needed for moving setpoints, mA_set
    der_error = (error-error_last)/magpot_diff
    # below is ideal derivative term for a fixed set point, mA_set
    der_error = mA_last - mA_current

    # the function
    pid_function_mA     = Kp*error+error_sum+Kd*der_error
    # now we convert to the units of pot position
    pid_function_magpot = pid_function_mA/der_error



    return


def SIS_mV_PID():


    return





def LO_PID(set_SIS_uA=15.0, set_sis_mV=1.8, set_mag_uA=50.0, max_test_number=20,min_diff_uA=0.1,measures_per_test=5,set_sleep_time=2):


    start_UCA = 5.0
    status = LabJackU3_DAQ0(start_UCA)
    sleep(set_sleep_time)
    meas_mV, meas_uA, meas_pot = measSIS()

    for test_number in range(max_test_number):
        None


    test_V = 0




    return