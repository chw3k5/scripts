__author__ = 'Caleb Wheeler'



# ### Example PID code
#
# (y_set,y_current, y_last, x_last, x_current, error_sum, error_last) = (1,1,1,1,1,1,1)
# (Ki,Kp,Kd)=(1,1,1)
# error = y_set - y_current
# x_diff = float(x_current-x_last)
# int_error = Ki*error*x_diff
# error_sum += int_error
# # only needed for moving setpoints, mA_set
# der_error = (error-error_last)/x_diff
# # below is ideal derivative term for a fixed set point, mA_set
# der_error_simple = y_last - y_current
#
# # the function
# pterm = Kp*error
# iterm = error_sum
# dterm = Kd*der_error_simple
# pid_function_y = pterm + iterm + dterm
# pid_function_x = pid_function_y/der_error





from LabJack_control import LabJackU3_DAQ0
from calibration import magpot_lookup, default_path, fetchoffset
from time import sleep
import numpy as np
from control import mag_channel, measSIS, measmag, setSIS_only, setmag_only, opentelnet, closetelnet, \
    default_magpot, default_sispot, setfeedback






def PID_function(y_set,y_current, y_last, x_last, x_current, error_sum, error_last, Ki, Kp, Kd):
    error = y_set - y_current
    x_diff = float(x_current-x_last)
    int_error = Ki*error*x_diff
    error_sum += int_error
    # only needed for moving setpoints, mA_set
    der_error = (error-error_last)/x_diff
    # below is ideal derivative term for a fixed set point, mA_set
    der_error_simple = y_last - y_current

    # the function
    pterm = Kp*error
    iterm = error_sum
    dterm = Kd*der_error_simple
    # print "pterm:",pterm,'   iterm:',iterm,'   dterm:',dterm
    pid_function_y = pterm + iterm + dterm
    pid_function_x = pid_function_y/der_error
    return pid_function_x, pid_function_y, error, error_sum


def measloop_SIS(feedback,sispot=65100, sleep_per_set=1, meas_number=1, verbose=False):
    setSIS_only(sispot,feedback=feedback)
    sleep(sleep_per_set)
    mV_list = []
    uA_list = []
    for n in range(meas_number):
        mV_temp, uA_temp, pot_temp = measSIS(verbose)
        mV_list.append(mV_temp)
        uA_list.append(uA_temp)
    mV = np.mean(mV_list)
    uA = np.mean(uA_list)
    return mV, uA



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
    pid_function_magpot, pid_function_mA, error, error_sum \
        = PID_function(mA_set, mA_current, mA_last, magpot_last, magpot_current,
                       error_sum, error_last, Ki, Kp, Kd)


    for adjust_attempt in range(max_adjust_attempt):
        mA_last     = mA_current
        magpot_last = magpot_current
        error_last  = error
        magpot_current -= pid_function_magpot
        if adjust_attempt+1 == max_adjust_attempt:
            mA_current, magpot_current = measloop(magpot=magpot_current-pid_function_magpot, meas_number=meas_number)
            error = mA_set - mA_current
        else:
            mA_current, magpot_current = measloop(magpot=magpot_current, meas_number=meas_number)
            pid_function_magpot, pid_function_mA, error, error_sum \
                = PID_function(mA_set, mA_current, mA_last, magpot_last, magpot_current,
                               error_sum, error_last, Ki, Kp, Kd)
        if verbose:
            print str(adjust_attempt+3)+" measurment error:", error, 'mA_set:', mA_set, 'mA_current:', mA_current, 'magpot_current:', magpot_current
        if ((abs(pid_function_magpot) <= min_diff_magpot) and (min_adjust_attempt < adjust_attempt)):
            if verbose:
                print "Set point reached, the change in pot position,"+ str(pid_function_magpot)+", " \
                      "is less than the minimum value of min_diff_magpot: "+str(min_diff_magpot)
            break

    final_deriv = (mA_current-mA_last)/(magpot_current-magpot_last)
    return magpot_current, final_deriv




############################
############################
######## SIS_mV_PID ########
############################
############################


def SIS_mV_PID(mV_set=1.8, mV_set_max=10, mV_set_min=-10,
               feedback=True, max_adjust_attempt=20, min_adjust_attempt=5,
               sleep_per_set=2, meas_number=5,
               min_diff_sispot=3,
               first_pot=65100, second_pot=56800,
               Kp=1.0, Ki=0.0, Kd=0.05, verbose=False):

    if verbose:
        print "The SIS mV PID function"
    if mV_set < mV_set_min:
        mV_set = mV_set_min
    elif mV_set_max < mV_set:
        mV_set = mV_set_max

    status = setfeedback(feedback)
    setmag_only(default_magpot)
    sispot_current = first_pot
    mV_current, uA_current \
        = measloop_SIS(feedback=feedback, sispot=sispot_current, sleep_per_set=sleep_per_set, meas_number=meas_number, verbose=verbose)
    error = mV_set - mV_current
    error_sum = 0
    pid_function_sispot = first_pot - second_pot

    for adjust_attempt in range(max_adjust_attempt):
        error_last  = error
        sispot_last = sispot_current
        mV_last     = mV_current
        sispot_current = sispot_last-pid_function_sispot
        mV_current, uA_current \
            = measloop_SIS(feedback=feedback, sispot=sispot_current, sleep_per_set=sleep_per_set, meas_number=meas_number, verbose=verbose)
        pid_function_sispot, pid_function_mV, error, error_sum \
                    = PID_function(mV_set, mV_current, mV_last, sispot_last, sispot_current,
                                   error_sum, error_last, Ki, Kp, Kd)

        if verbose:
            print str(adjust_attempt+1)+" measurment error:", error, 'mV_set:', mV_set, 'mV_current:', mV_current, 'sispot_current:', sispot_current

        if ((abs(pid_function_sispot) <= min_diff_sispot) and (min_adjust_attempt < adjust_attempt)):
            if verbose:
                print "Set point reached, the change in pot position,"+ str(pid_function_sispot)+", " \
                      "is less than the minimum value of min_diff_magpot: "+str(min_diff_sispot)
            break
    final_deriv = (mV_current-mV_last)/(sispot_current-sispot_last)
    return sispot_current, final_deriv


def LO_PID(uA_set=20.0, uA_set_max=50.0, uA_set_min=5.0,
           feedback=True, max_adjust_attempt=20, min_adjust_attempt=5,
           sleep_per_set=3, meas_number=5,
           uA_search_res = 10,
           min_diff_V=0.001,
           V_min=0,V_max=5,
           Kp=1.0, Ki=0.0, Kd=0.05, verbose=False):
    if verbose:
        print "The SIS uA-LO power PID function"
    if uA_set < uA_set_min:
        uA_set = uA_set_min
    elif uA_set_max < uA_set:
        uA_set = uA_set_max

    # turn on the standard settings
    status = setfeedback(feedback)
    setmag_only(magpot=default_magpot)
    setSIS_only(sispot=default_sispot,feedback=feedback)
    sleep(sleep_per_set)

    # measure the range of LO pump power (uA)
    V_list=[V_min,V_max] # This is the range of the LO UCA Voltage
    status = LabJackU3_DAQ0(UCA_voltage=V_list[0])
    sleep(sleep_per_set)
    mV, uA = measloop_SIS(feedback,sispot=default_sispot, sleep_per_set=sleep_per_set,
                              meas_number=meas_number, verbose=verbose)
    uA_list = [uA]
    if verbose: print "UCA Voltage:", V_list[0], "    SIS current (uA):", uA_list[0]

    status = LabJackU3_DAQ0(UCA_voltage=V_list[-1])
    sleep(sleep_per_set)
    mV, uA = measloop_SIS(feedback,sispot=default_sispot, sleep_per_set=sleep_per_set,
                              meas_number=meas_number, verbose=verbose)
    uA_list.append(uA)
    if verbose: print "UCA Voltage:", V_list[-1], "    SIS current (uA):", uA_list[-1]

    # set range variables
    uA_min = uA_list[-1]
    uA_max = uA_list[0]

    final_deriv = 1
    if uA_set < uA_min:
        print "The LO is set to it max UCA voltage of "+str(V_max) +" Volts (max attenuation)"
        print "giving a minimum uA value:"+str(uA_min)+" which is bigger than the user specified"
        print "uA_set:"+str(uA_set)+ "."
        print " Setting the UCA voltage to max attenuation:"+str(V_max)
        final_V = V_max

    elif uA_max < uA_set:
        print "The LO is set to it min UCA voltage of "+str(V_min) +" Volts (min attenuation)"
        print "giving a maximum uA value:"+str(uA_max)+" which is smaller than the user specified"
        print "uA_set:"+str(uA_set)+ "."
        print " Setting the UCA voltage to min attenuation:"+str(V_min)
        final_V = V_min
    else:
        finished = False
        voltage_index = 0
        # Find the Voltages so that difference in uA power is less than the function variable 'uA_search_res'
        while not finished:
            finished_index = len(V_list)-1
            if finished_index <= voltage_index:
                finished = True
            else:
                uA_high = uA_list[voltage_index]
                uA_low = uA_list[voltage_index+1]
                if uA_search_res < abs(uA_high - uA_low):
                    V_low = V_list[voltage_index]
                    V_high = V_list[voltage_index+1]
                    voltage = (V_low+V_high)/2.0
                    status = LabJackU3_DAQ0(UCA_voltage=voltage)
                    V_list.insert(voltage_index+1, voltage)
                    sleep(sleep_per_set)
                    mV, uA = measloop_SIS(feedback,sispot=default_sispot, sleep_per_set=1,
                                          meas_number=1, verbose=verbose)
                    uA_list.insert(voltage_index+1,uA)

                else:
                    if verbose: print "UCA Voltage:", V_list[voltage_index], "    SIS current (uA):", uA_list[voltage_index]
                    voltage_index += 1



        # first find the uA_list value closest to uA_set
        diff_uA_list = list(abs(np.array(uA_list)-float(uA_set)))
        min_diff_uA_list = min(diff_uA_list)
        min_diff_uA_index = diff_uA_list.index(min_diff_uA_list)
        V_first = V_list[min_diff_uA_index]

        # get the 2nd closest point to deliver to the PID function
        diff_uA_list.pop(min_diff_uA_index)
        min_diff_uA_list = min(diff_uA_list)
        min_diff_uA_index = diff_uA_list.index(min_diff_uA_list)
        V_second = V_list[min_diff_uA_index]

        # Start the PID adjustment sequence
        V_current = V_first
        status = LabJackU3_DAQ0(UCA_voltage=V_current)
        mV_current, uA_current \
            = measloop_SIS(feedback=feedback, sispot=default_sispot, sleep_per_set=sleep_per_set,
                           meas_number=meas_number, verbose=verbose)
        error = uA_set - mV_current
        error_sum = 0
        pid_function_V = V_first - V_second

        for adjust_attempt in range(max_adjust_attempt):
            error_last = error
            V_last     = V_current
            uA_last    = uA_current
            V_current  = V_last-pid_function_V
            status = LabJackU3_DAQ0(UCA_voltage=V_current)

            mV_current, uA_current \
            = measloop_SIS(feedback=feedback, sispot=default_sispot, sleep_per_set=sleep_per_set,
                           meas_number=meas_number, verbose=verbose)

            pid_function_V, pid_function_uA, error, error_sum \
                        = PID_function(uA_set, uA_current, uA_last, V_last, V_current,
                                       error_sum, error_last, Ki, Kp, Kd)

            if verbose:
                print str(adjust_attempt+1)+" measurment error:", error, 'uA_set:', uA_set, 'uA_current:', uA_current, 'V_current:', V_current

            if ((abs(pid_function_V) <= min_diff_V) and (min_adjust_attempt < adjust_attempt)):
                if verbose:
                    print "Set point reached, the change in Voltage ,"+ str(pid_function_V)+", " \
                          "is less than the minimum value of min_diff_V: "+str(min_diff_V)
                break
        final_V = V_current
        final_deriv = (uA_current-uA_last)/(V_current-V_last)
    return final_V, final_deriv



if __name__ == "__main__":
    test_path = 'C:\\Users\\chwheele\\Google Drive\\Kappa\\NA38\\IVsweep\\Mar04_15\\LO_stability_test\\rawdata\\00001\\'
    opentelnet()
    #Emag_PID(local_path=test_path, mA_set=24.0, verbose=True)
    #SIS_mV_PID(mV_set=1.8,
    #           feedback=True, max_adjust_attempt=40, min_adjust_attempt=5,
    #           sleep_per_set=3, meas_number=5,
    #           min_diff_sispot=100,
    #           Kp=1.0, Ki=0.0, Kd=0.05, verbose=True)
    final_V, final_deriv = LO_PID(uA_set=20.0,feedback=True, verbose=True)
    print final_V
    closetelnet()