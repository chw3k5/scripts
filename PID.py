__author__ = 'chwheele'
from LabJack_control import LabJackU3_DAQ0
from calibration import magpot_lookup, default_path, fetchoffset
from time import sleep
import numpy as np
from control import mag_channel, measSIS, measmag, setSIS_only, setmag_only, opentelnet, closetelnet, \
    default_magpot, default_sispot, setfeedback


##########################
##########################
######## Emag_PID ########
##########################
##########################

def Emag_PID(local_path=default_path, mA_set=35.0, mA_set_max=78, mA_set_min=-80,
             max_adjust_attempt=20, min_adjust_attempt=5,
             start_overshoot_mA=2.0, sleep_per_set=2, meas_number=5,
             min_diff_magpot=3, Kp=1.0, Ki=0.0, Kd=0.05, verbose=False):
    if verbose:
        print "The electromagnet PID function"
    if mA_set > mA_set_max:
        mA_set = mA_set_max
    elif mA_set_min > mA_set:
        mA_set = mA_set_min


    def measloop(mA_to_find=None, magpot=None, meas_number=1):
        if mA_to_find is not None:
            magpot = magpot_lookup(mA_to_find, mag_channel=mag_channel, local_lookup_filepath=local_path)
        m, b = fetchoffset(filename=str(mag_channel)+'mA_biascom-mA_meas.csv', mag_channel=mag_channel, path=local_path)

        setmag_only(magpot)
        sleep(sleep_per_set)

        mA_list = []
        for n in range(meas_number):
            V_temp, mA_temp, pot_temp = measmag(verbose)
            mA_list.append((mA_temp*m)+b)
        mA = np.mean(mA_list)
        return mA, magpot

    def PID_function(mA_current, mA_last, magpot_last, magpot_current, error_sum, error_last):
        error = mA_set - mA_current
        magpot_diff = float(magpot_current-magpot_last)
        int_error = Ki*error*magpot_diff
        error_sum += int_error
        # only needed for moving setpoints, mA_set
        der_error = (error-error_last)/magpot_diff
        # below is ideal derivative term for a fixed set point, mA_set
        der_error_simple = mA_last - mA_current

        # the function
        pterm = Kp*error
        iterm = error_sum
        dterm = Kd*der_error_simple
        pid_function_mA = pterm + iterm + dterm
        #if verbose:
        #    print "pid_function_mA:", pid_function_mA
        #    print "pterm:", pterm, 'iterm:',iterm,'dterm:',dterm
        # now we convert to the units of pot position
        pid_function_magpot = pid_function_mA/der_error

        return pid_function_magpot, error, error_sum

    # initialize
    mA_set=float(mA_set)
    mA_set_sign = int(mA_set/abs(mA_set))

    # first measurement (full overshoot)
    overshoot_mA = mA_set_sign*start_overshoot_mA+mA_set
    mA_current, magpot_current = measloop(mA_to_find=overshoot_mA, meas_number=meas_number)
    error = mA_set - mA_current
    if verbose:
        print "first measurment error:", error, 'mA_set:', mA_set, 'mA_current:', mA_current, 'magpot_current:', magpot_current

    # second measurement (half overshoot)
    mA_last     = mA_current
    magpot_last = magpot_current
    error_last  = error

    halfovershoot_mA = mA_set_sign*(start_overshoot_mA/2.0)+mA_set
    mA_current, magpot_current = measloop(mA_to_find=halfovershoot_mA, meas_number=meas_number)
    error = mA_set - mA_current
    if verbose:
        print "second measurment error:", error, 'mA_set:', mA_set, 'mA_current:', mA_current, 'magpot_current:', magpot_current

    # initial error function
    error_sum = 0.
    pid_function_magpot, error, error_sum = PID_function(mA_current, mA_last, magpot_last, magpot_current, error_sum, error_last)


    for adjust_attempt in range(max_adjust_attempt):


        if not adjust_attempt+1 == max_adjust_attempt:
            mA_last     = mA_current
            magpot_last = magpot_current
            error_last  = error
            mA_current, magpot_current = measloop(magpot=magpot_current-pid_function_magpot, meas_number=meas_number)
            pid_function_magpot, error, error_sum = PID_function(mA_current, mA_last, magpot_last, magpot_current, error_sum, error_last)

        else:
            mA_current, magpot_current = measloop(magpot=magpot_current-pid_function_magpot, meas_number=meas_number)
            error = mA_set - mA_current
        if verbose:
            print str(adjust_attempt+3)+" measurment error:", error, 'mA_set:', mA_set, 'mA_current:', mA_current, 'magpot_current:', magpot_current
        if ((abs(pid_function_magpot) <= min_diff_magpot) and (min_adjust_attempt < adjust_attempt)):
            if verbose:
                print "Set point reached, the change in pot position,"+ str(pid_function_magpot)+", " \
                      "is less than the minimum value of min_diff_magpot: "+str(min_diff_magpot)
            break


    return




############################
############################
######## SIS_mV_PID ########
############################
############################


def SIS_mV_PID(mV_set=1.8, mV_set_max=10, mV_set_min=-10,
               feedback=True,max_adjust_attempt=20, min_adjust_attempt=5,
               sleep_per_set=2, meas_number=5,
               min_diff_magpot=3, Kp=1.0, Ki=1.0, Kd=1.0, verbose=False):
    def measloop(sispot, magpot=None, meas_number=1):

        setSIS_only(sispot)
        sleep(sleep_per_set)
        mV_list = []
        for n in range(meas_number):
            mV_temp, uA_temp, pot_temp = measSIS(verbose)
            mV_list.append(mV_temp)
        mA = np.mean(mA_list)
        return mA, magpot

    setSIS_only(65100,feedback=feedback,verbose=verbose)
    status = setfeedback(feedback)
    setmag_only(default_magpot)
    sleep(sleep_per_set)



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


if __name__ == "__main__":
    test_path = 'C:\\Users\\chwheele\\Google Drive\\Kappa\\NA38\\IVsweep\\Mar04_15\\LO_stability_test\\rawdata\\00001\\'
    opentelnet()
    Emag_PID(local_path=test_path, mA_set=24.0, verbose=True)
    closetelnet()