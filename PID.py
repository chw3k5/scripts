__author__ = 'chwheele'
from LabJack_control import LabJackU3_DAQ0
from calibration import magpot_lookup
from time import sleep
from control import mag_channel, measSIS, measmag, setSIS_only, setmag_only

def Emag_PID(mA_set=35.0, start_overshoot_mA=1.0, sleep_per_set=2, local_calfile=None,verbose=False):
    mA_set=float(mA_set)

    mA_set_sign = int(mA_set/abs(mA_set))
    mA_to_start = mA_set_sign*start_overshoot_mA+mA_set
    start_magpot = magpot_lookup(mA_to_find=mA_to_start, mag_channel=mag_channel,
                                 lookup_filepath=local_calfile)
    setmag_only(start_magpot)
    sleep(sleep_per_set)



    # Get data for a linear interpolation of the magpot to current relation
    # find max magnet current
    V_high, mA_high, pot_high = setmag(high_pot_pos, verbose)
    # find min magnet current
    V_low, mA_low, pot_high = setmag(low_pot_pos, verbose)

    # make fit a line to the min and max data points (find m,b in Y=mX+b)
    m = (high_pot_pos-low_pot_pos)/(mA_high-mA_low)
    b = low_pot_pos - m*mA_low
    # estimator  the final pot position from the max min line
    est_pot_pos=m*mA_user+b

    # We set the magnet to its rail and come down to the desired current,
    # here we determine which rail (+ or -) to set the magnet pot position
    if mA_user >= 0:
        rail_pos   = max_pot_pos
        multiplier = 1
    elif mA_user < 0:
        rail_pos = min_pot_pos
        multiplier = -1
    else:
        print "mA_user is not set to a number, exiting script."
        print "mA_user = "+ str(mA_user)
        sys.exit()
    mA_rail_list = []
    V_rail_list  = []
    for Q in range(rail_meas):
        V_rail_temp, mA_rail_temp, pot_rail_temp = setmag(rail_pos, verbose)
        mA_rail_list.append(mA_rail_temp)
        V_rail_list.append(V_rail_temp)

    #Get rid of the Outlier in the set rail measurements
    mA_rail_array = numpy.array(mA_rail_list)
    mA_rail_mean  = numpy.mean(mA_rail_array)
    diff_array    = list(abs(mA_rail_array-mA_rail_mean))
    outlier_index = diff_array.index(max(diff_array))
    mA_rail_list.pop(outlier_index)
    V_rail_list.pop(outlier_index)

    mA_rail = numpy.mean(numpy.array(mA_rail_list))
    V_rail  = numpy.mean(numpy.array(V_rail_list))
    ######################
    ####### Loop 1 #######
    ######################
    # Now we step the magnet position toward the estimated pot position.
    # Each step brings the pot position part way between its current position
    # and the estimated position, specified by loop1_frac. This happens until the
    # difference between mA_user and mA_meas becomes less than some threshold
    # value.
    # mA_user = mA_user - multiplier*0.5*loop1_thresh # so the algorithm mean return
    # is the original mA_user value, loop1_thresh is the accepted error

    finished = False
    ebrake   = False
    current_position = rail_pos
    mA_current       = mA_rail
    V_current        = V_rail
    loop1_count      = 0
    loop1_restar     = 0
    pot_diff         = 999999
    diff = multiplier*(mA_current - mA_user)
    loop1_frac        = 0.9

    subloop = False
    if diff < 0:
        print "The use specified magnet current is grater than the rail value"
        print "mA_rail = " + str(mA_rail)
        print "mA_user = " + str(mA_user)
        if careful:
            print "careful is on, killing the script"
            sys.exit()
        else:
            print "careful is off, so script must go on!"

    while not finished:
        if ebrake:
            print "Loop one restarted more than " + str(loop1_restar_max) + " times"
            print "Killing the script"
            sys.exit()
        elif ((diff < 0) and (not abs(pot_diff) < pot_diff_thresh)):
            if careful:
                if verbose:
                    print "Careful is 'ON' "
                    print "The Algorithm overshot the user specified mA setting"
                    print "Restarting the loop"
                    print str(m*(mA_current - mA_user)) + " correction of estimated position"
                est_pot_pos      = current_position + m*(mA_current - mA_user)
                loop1_count      = 0
                current_position = rail_pos
                mA_current       = mA_rail
                V_current        = V_rail
                diff             = 2*loop1_thresh
                pot_diff         = 999999
                loop1_restar = loop1_restar +1
                if loop1_restar_max <= loop1_restar:
                    ebrake = True
            else:
                finished = True
        elif ((abs(diff) <= loop1_thresh) or (abs(pot_diff) < pot_diff_thresh)):
            if verbose:
                print "Loop1 of magnet current finding algorithm completed after "
                print str(loop1_count) + " loops and"
                print str(loop1_restar) + " loop restarts"
            finished = True
        else:
            new_position = current_position*(1-loop1_frac)+est_pot_pos*loop1_frac
            setmag_only(new_position)
            pot_current = new_position
            subfinished = False
            if subloop:
                subloop_count = 0
                mA_list = []
                while not subfinished:
                    subloop_count = subloop_count +1
                    V_temp, mA_temp, pot_temp = measmag(verbose)
                    mA_list.append(mA_temp)

                    if subloop_min <= subloop_count:
                        mA_array = numpy.array(mA_list)
                        mA_ave = numpy.mean(mA_array)
                        mA_STD = numpy.std(mA_array)
                        mA_SEM = mA_STD/numpy.sqrt(subloop_count)
                        mA_current = mA_ave

                        diff   = multiplier*(mA_current - mA_user)
                        if ((mA_SEM < diff) or (subloop_max <= subloop_count)):
                            subfinished = True
                            if verbose:
                                print str(subloop_count) + " is the subloop count  " + str(subloop_max) + " is the maximum allowed subloops"
                                print str(mA_STD)        + " is the standard deviation of the measured current"
                                print str(mA_SEM)        + " is the standard deviation of the mean of the measured current"

            else:
                V_current, mA_current, pot_current = measmag(verbose)
                diff                  = multiplier*(mA_current - mA_user)

            # I didn't get these to work, I instead moved on to other projects
            #m = (current_position-new_position)/(mA_current-((new_position-b)/m))
            #b = current_position - m*mA_current
            current_position      = new_position
            pot_diff              = diff*m
            est_pot_pos           = current_position + m*(mA_user - mA_current)
            loop1_count           = loop1_count + 1

            # this makes the step size finer as we get closer to the user specified currnet (mA)
            # Definition is in mag_config.py
            loop1_frac, subloop, subloop_min  = step_decision(pot_diff, loop1_restar)

            if verbose:
                print str(loop1_count) + " = loop1_cout is "
                print str(loop1_restar) + " = loop1_restar"
                print str(mA_current) + " = mA_current"
                print str(mA_user) + " = mA_user"
                print str(diff) + " = diff"
                print str(pot_diff) + " diff in terms of pot values"
                print " "
                print " "
            if (loop1_count >= loop1_max):
                if careful:
                    print "careful is true and the loop count of the first loop exceeded"
                    print "the maximum allow value of "+str(loop1_max)
                    print "killing the script"
                    sys.exit()
                else:
                    finished = True
                    if verbose:
                        print "Maximum loops reach:" + str(loop1_max)
                        print "ending algorithm and returning variables"
    V_mag   = V_current
    mA_mag  = mA_current
    pot_mag = pot_current
    if verbose:
        print " "
        print " "


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