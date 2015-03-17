import telnetlib
import time
import numpy
import sys
from LabJack_control import LabJackU3_DAQ0




sis_channel = '0'
mag_channel = '10'

sleep_list = [0.3, 0.7, 2, 5, 10, 30, 60, 120]


def opentelnet():
    global thzbiascomputer
    thzbiascomputer = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    return

def closetelnet():
    thzbiascomputer.close()
    return

def restartTelnet(sleep_time):
    try:
        thzbiascomputer.close()
    except UnboundLocalError:
        print "The bias computer connection is closed already."
        print "Starting it now"
    time.sleep(sleep_time)
    thzbiascomputer = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    return


# This is used by both the the magnet control and the sisbias control
###########################
###### CommandOutput ######
###########################
def CommandOutput(sleep_time, channel):
    out = []
    if sleep_time < 30:
        thzbiascomputer.write("setbias " + channel + " \n")
        junk = thzbiascomputer.read_until('v = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('i = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('f = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('p = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
    else:
        restartTelnet(sleep_time)
        thzbiascomputer.write("setbias " + channel + " \n")
        junk = thzbiascomputer.read_until('v = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('i = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('f = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('p = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
    return out


# This is used by both the the magnet control and the sisbias control
##########################
###### attempt_meas ######
##########################
def attempt_meas(sleep_time, channel):
    V   = -999999
    A   = -999999
    pot = -999999
    channel = str(channel)
    out = CommandOutput(sleep_time, channel)

    V_temp    = out[0]
    A_temp    = out[1]
    f_temp    = out[2]
    pot_temp  = out[3]

    truth_list1 = []
    truth_list1.append(V_temp   == '')
    truth_list1.append(A_temp   == '')
    truth_list1.append(f_temp   == '')
    truth_list1.append(pot_temp == '')
    redo = False
    if any(truth_list1):
        redo = True
    else:
        try:
            V    = float(V_temp)
            A    = float(A_temp)
            pot  = int(numpy.round(float(pot_temp)))

            truth_list2 = []
            truth_list2.append(    40 <= abs(V))
            truth_list2.append(  1000 <= abs(A))
            truth_list2.append(130000 <= pot)
            if any(truth_list2):
                redo = True
        except ValueError:
            redo = True
    return redo, V, A, pot



####################################
####################################
########## MAGNET CONTROL ##########
####################################
####################################

#####################
###### measmag ######
#####################

def measmag(verbose=False):
    channel = mag_channel
    
    message_list = []
    message_list.append("Had to wait extra time for the measurement to be returned")
    message_list.append("Had to wait extra time for the measurement to be returned again")
    for n in range(2,len(sleep_list)-1):
        message_list.append("Had to wait extra time for the measurement to be returned again x" + str(n))
    message_list.append("The script had to wait to long to read a value of mV and uA")
    
    verbose_list = []
    if verbose:
        verbose_list.append(True)
        verbose_list.append(True)
        verbose_list.append(True)
    else:
        verbose_list.append(False)
        verbose_list.append(False)
        verbose_list.append(False)
    for n in range(3,len(sleep_list)):
        verbose_list.append(True)

        
    for loop_index in range(len(sleep_list)):
        redo, V_mag, mA_mag, pot_mag = attempt_meas(sleep_list[loop_index],\
        channel)
        if not redo:
            break
        if verbose_list[loop_index]:
            print message_list[loop_index]
    if redo:
        print "Killing the script"
        print "mV_mag  = " + str(V_mag)
        print "uA_mag  = " + str(mA_mag)
        print "pot_mag = " + str(pot_mag)
        print " "
        sys.exit()
    
    return V_mag, mA_mag, pot_mag


##############################
###### measmag_w_offset ######
##############################

def measmag_w_offset(filename=str(mag_channel)+'mA_biascom-mA_meas.csv', path='', verbose=False):
    from calibration import fetchoffset
    V_mag, mA_mag, magpot = measmag(verbose=verbose)
    m, b = fetchoffset(filename=filename, mag_channel=mag_channel, path=path)
    offset_mA = (mA_mag*m)+b
    return offset_mA, magpot

####################
###### setmag ######
####################

def setmag(magpot, verbose=False):
    mA_mag  = -999998
    V_mag   = -999998
    pot_mag = -999998 
    
    if (magpot < 0 or magpot > 129797):
        print "magpot value was not in the set [0,129797], try agian"
        print "magpot = " + str(magpot)
        if 129797 < magpot:
            magpot = 129000
            print "setting it to: " + str(magpot)
        elif magpot < 0:
            magpot = 1000
            print "setting it to: " + str(magpot)
        else:
            print "killing script"
            sys.exit()
        
    #set the pot position of the magnet and recound the current and volage
    thzbiascomputer.write("setbias "+mag_channel+" "+str(numpy.round(magpot)) + " \n")
    # time.sleep(SleepPerMes)     

    
    V_mag, mA_mag, pot_mag = measmag(verbose)
    return V_mag, mA_mag, pot_mag
 

#########################
###### setmag_only ######
#########################
             
def setmag_only(magpot):
    import telnetlib
    import numpy
    import sys

    if (magpot < 0 or magpot > 129797):
        print "magpot value was not in the set [0,129797], try agian"
        print "magpot = " + str(magpot)
        if 129797 < magpot:
            magpot = 129000
            print "setting it to: " + str(magpot)
        elif magpot < 0:
            magpot = 1000
            print "setting it to: " + str(magpot)
        else:
            print "killing script"
            sys.exit()
        
    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias "+mag_channel+" "+str(numpy.round(magpot)) + " \n")
    # time.sleep(SleepPerMes)     

    return

############################
###### setmag_highlow ######
############################
             
def setmag_highlow(magpot):
    import telnetlib
    import numpy
    import sys
    from time import sleep

    if (magpot < 0 or magpot > 129797):
        print "magpot value was not in the set [0,129797], try agian"
        print "magpot = " + str(magpot)
        if 129797 < magpot:
            magpot = 129000
            print "setting it to: " + str(magpot)
        elif magpot < 0:
            magpot = 1000
            print "setting it to: " + str(magpot)
        else:
            print "killing script"
            sys.exit()
    elif ((0 <= magpot) and (magpot <65100)):
        thzbiascomputer.write("setbias "+mag_channel+" 1000 \n")

    else:
        thzbiascomputer.write("setbias "+mag_channel+" 129796 \n")

    sleep(0.5)
    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias "+mag_channel+" "+str(numpy.round(magpot)) + " \n")
    # time.sleep(SleepPerMes)     

    return
  
      
######################################
######################################
########## SIS BIAS CONTROL ##########
######################################
######################################

#####################
###### measSIS ######
#####################

def measSIS(verbose=False):
    from sisbias_config import sleep_list
    
    channel = sis_channel
    
    message_list = []
    message_list.append("Had to wait extra time for the measurement to be returned")
    message_list.append("Had to wait extra time for the measurement to be returned again")
    for n in range(2,len(sleep_list)-1):
        message_list.append("Had to wait extra time for the measurement to be returned again x" + str(n))
    message_list.append("The script had to wait to long to read a value of mV and uA")

    verbose_list = []
    if verbose:
        verbose_list.append(True)
        verbose_list.append(True)
        verbose_list.append(True)
    else:
        verbose_list.append(False)
        verbose_list.append(False)
        verbose_list.append(False)
    for n in range(3,len(sleep_list)):
        verbose_list.append(True)
        
    redo = False
    for loop_index in range(len(sleep_list)):
        redo, mV_sis, uA_sis, pot_sis = attempt_meas(sleep_list[loop_index], channel)
        #print redo, mV_sis, uA_sis, pot_sis
        if not redo:
            break
        if verbose_list[loop_index]:
            print message_list[loop_index]
    if redo:
        print "Killing the script"
        print "mV_sis  = " + str(mV_sis)
        print "uA_sis  = " + str(uA_sis)
        print "pot_sis = " + str(pot_sis)
        print " "
        sys.exit()
    #time.sleep(SleepPerMes)
    return mV_sis, uA_sis, pot_sis
    
    
#########################
###### setfeedback ######
#########################

def setfeedback(feedback):
    from sisbias_config import SleepPerMes_feedback
    
    status=False
    if feedback:
        thzbiascomputer.write("feedback 1 \n")
        time.sleep(SleepPerMes_feedback)
    else:
        thzbiascomputer.write("feedback 0 \n")
        time.sleep(SleepPerMes_feedback)
    out1 = thzbiascomputer.read_very_eager()
    if feedback:
        if out1 == 'Enabling SIS feedback loop (V-mode)\n':
            status=True
        else:
            print " The feedback command did not get the expected string <Enabling SIS feedback loop (V-mode)\n>." \
                  " Check the connection to the THz bias computer"
    elif not feedback:
        if out1 == 'Disabling SIS feedback loop (R-mode)\n':
            status=True
        else:
            print " The feedback command did not get the expected string <Disabling SIS feedback loop (R-mode)\n>." \
                  " Check the connection to the THz bias computer"
    else:
        print 'The variable feedback can only be True or False. Returning status=False'    

    
    return status 
  

####################
###### setSIS ######
####################  

def setSIS(sispot, feedback, verbose=False, careful=False):
    from sisbias_config import SleepPerMes, feedon_low, feedon_high, feedoff_low, feedoff_high

    uA_sis  = -999998
    mV_sis  = -999998
    pot_sis = -999998
    
    # turn the feedback on or off
    status = setfeedback(feedback)
    if (not status and careful):
        print "The feedback was not set properly"
        print "Killing script"
        sys.exit()
     
    # safty catches, to keep the SIS bias within nominal ranges   
    if feedback:
        if ((feedon_low < sispot) and (sispot < feedon_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedon_low) + " to " + str(feedon_high) + "]"
            print "~[7.5V to -7.5V] for feedback 'ON', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safety catches"
            print "make sure the SIS switch located on the Dewar is set to 'Thru' (not 'Open')"
            if careful:
                print "killing script"
                sys.exit()
            elif feedon_high < sispot:
                sispot = feedon_high - 1000
            elif sispot < feedon_low:
                sispot = feedon_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)
    else:
        if ((feedoff_low < sispot) and (sispot < feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedoff_low) + " to " + str(feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safety catches"
            print "make sure the SIS switch located on the Dewar is on 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif feedoff_high < sispot:
                sispot = feedoff_high - 1000
            elif sispot < feedoff_low:
                sispot = feedoff_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)

    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias " + sis_channel + " "+str(numpy.round(sispot)) + " \n")
    #time.sleep(SleepPerMes)     

    
    mV_sis, uA_sis, pot_sis = measSIS(verbose)


    return mV_sis, uA_sis, pot_sis


#########################
###### setSIS_only ######
#########################

def setSIS_only(sispot, feedback, verbose=False, careful=False):
    from sisbias_config import SleepPerMes, feedon_low, feedon_high, feedoff_low, feedoff_high    
    
    # safty catches, to keep the SIS bias within nominal ranges   
    if feedback:
        if ((feedon_low < sispot) and (sispot < feedon_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedon_low) + " to " + str(feedon_high) + "]"
            print "~[7.5V to -7.5V] for feedback 'ON', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safety catches"
            print "make sure the SIS switch located on the Dewar set to 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif feedon_high < sispot:
                sispot = feedon_high - 1000
            elif sispot < feedon_low:
                sispot = feedon_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "resetting pot to safe value: " + str(sispot)
                
    else:
        if ((feedoff_low < sispot) and (sispot < feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedoff_low) + " to " + str(feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safety catches"
            print "make sure the SIS switch located on the Dewar is set to 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif feedoff_high < sispot:
                sispot = feedoff_high - 1000
            elif sispot < feedoff_low:
                sispot = feedoff_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)
    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias "+sis_channel+" "+str(numpy.round(sispot)) + " \n")
    time.sleep(SleepPerMes)
    return

##############################
###### CommandOutput_TP ######
##############################
def CommandOutput_TP(sleep_time, sispot, channel):
    out = []
    sweep_cmd =  "sweep " + channel + " " + sispot + " " + sispot + " 1\n"
    if sleep_time < 30:
        thzbiascomputer.write(sweep_cmd)
        junk = thzbiascomputer.read_until('v = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('i = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('t = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('p = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
    else:
        restartTelnet(sleep_time)
        thzbiascomputer.write(sweep_cmd)
        junk = thzbiascomputer.read_until('v = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('i = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('t = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
        junk = thzbiascomputer.read_until('p = ', float(sleep_time))
        line = thzbiascomputer.read_until('\n', float(sleep_time))
        out.append(line)
    return out


############################
###### attempt_measTP ######
############################
def attempt_measTP(sleep_time, sispot, channel):
    mV_sis  = -999999
    uA_sis  = -999999
    tp_sis  = -999999
    pot_sis = -999999
    
    sispot = str(numpy.round(sispot))
    out = CommandOutput_TP(sleep_time, sispot, channel)
    mV_sis_temp  = out[0]
    uA_sis_temp  = out[1]
    tp_sis_temp  = out[2]
    pot_sis_temp = out[3]

    truth_list1 = []
    truth_list1.append(mV_sis_temp  == '')
    truth_list1.append(uA_sis_temp  == '')
    truth_list1.append(tp_sis_temp  == '')
    truth_list1.append(pot_sis_temp == '')
    
    redo = False
    if any(truth_list1):
        redo = True
    else:
        try:
            mV_sis  = float(mV_sis_temp)
            uA_sis  = float(uA_sis_temp)
            tp_sis  = float(tp_sis_temp)
            pot_sis = int(numpy.round(float(pot_sis_temp)))
            truth_list2 = []
            truth_list2.append(    20 <= mV_sis )
            truth_list2.append(   200 <= uA_sis )
            truth_list2.append(     5 <= tp_sis )
            truth_list2.append(130000 <= pot_sis)
            if any(truth_list2):
                redo = True
        except ValueError:
            redo = True
    time_stamp = time.time()
    return redo, mV_sis, uA_sis, tp_sis, pot_sis, time_stamp

#######################
###### setSIS_TP ######
#######################

def setSIS_TP(sispot, feedback, verbose=False, careful=False):
    from sisbias_config import SleepPerMes, sleep_list
    channel = '0'

    message_list = []
    message_list.append("Had to wait extra time for the measurement to be returned")
    message_list.append("Had to wait extra time for the measurement to be returned again")
    for n in range(2,len(sleep_list)-1):
        message_list.append("Had to wait extra time for the measurement to be returned again x" + str(n))
    message_list.append("The script had to wait to long to read a value of mV and uA")

    verbose_list = []
    if verbose:
        verbose_list.append(True)
        verbose_list.append(True)
        verbose_list.append(True)
    else:
        verbose_list.append(False)
        verbose_list.append(False)
        verbose_list.append(False)
    for n in range(3,len(sleep_list)):
        verbose_list.append(True)

    # turn the feedback on or off
    status = setfeedback(feedback)
    if (not status and careful):
        print "The feedback was not set properly"
        print "Killing script"
        sys.exit()
    
    # we need to set the pot before measuring Total Power
    setSIS_only(sispot, feedback, verbose, careful)
    time.sleep(SleepPerMes)
    
    for loop_index in range(len(sleep_list)):
        redo, mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = \
        attempt_measTP(sleep_list[loop_index], sispot, channel)
        if not redo:
            break
        if verbose_list[loop_index]:
            print message_list[loop_index]
    if redo:
        print "Killing the script"
        print "mV_sis  = "  + str(mV_sis)
        print "uA_sis  = "  + str(uA_sis)
        print "tp_sis  = "  + str(tp_sis)
        print "pot_sis = "  + str(pot_sis)
        print "Error Report"
        sys.exit()
    
    return mV_sis, uA_sis, tp_sis, pot_sis


########################
###### measSIS_TP ######
########################
def measSIS_TP(sispot, feedback, verbose=False, careful=False):
    from sisbias_config import SleepPerMes, sleep_list
    channel = '0'
    message_list = []
    message_list.append("Had to wait extra time for the measurment to be returned")
    message_list.append("Had to wait extra time for the measurment to be returned again")
    for n in range(2,len(sleep_list)-1):
        message_list.append("Had to wait extra time for the measurment to be returned again x" + str(n))
    message_list.append("The script had to wait to long to read a value of mV and uA")

    verbose_list = []
    if verbose:
        verbose_list.append(True)
        verbose_list.append(True)
        verbose_list.append(True)
    else:
        verbose_list.append(False)
        verbose_list.append(False)
        verbose_list.append(False)
    for n in range(3,len(sleep_list)):
        verbose_list.append(True)

    for loop_index in range(len(sleep_list)):
        redo, mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = \
        attempt_measTP(sleep_list[loop_index], sispot, channel)
        if not redo:
            break
        if verbose_list[loop_index]:
            print message_list[loop_index]
    if redo:
        print "Killing the script"
        print "mV_sis  = "  + str(mV_sis)
        print "uA_sis  = "  + str(uA_sis)
        print "tp_sis  = "  + str(tp_sis)
        print "pot_sis = "  + str(pot_sis)
        print " "
        sys.exit()
    
    return mV_sis, uA_sis, tp_sis, pot_sis, time_stamp  


#########################
###### setSIS_Volt ######
#########################

def setSIS_Volt(mV_user, verbose, careful, cheat_num):
    from matplotlib import pyplot as plt
    from domath import regrid, conv
    from operator import itemgetter
    from sisbias_config import mV_max, mV_min, loop_thresh, pot_diff_thresh, loop_max, loop_hard_max, SEM_user, subloop_min
    from sisbias_config import subloop_max, subloop_hard_max, SEM_user2, loop3_min, loop3_max, loop3_hard_max, high_pot_pos_defult
    from sisbias_config import low_pot_pos_defult, check_radius, pot_per_check, bound_diff, restart_count_max, show_plot, min_cdf, sigma, intep_meas, unstick_max
    unstick_count = 0
    unstick = True
    while ((unstick_count < unstick_max) and (unstick)):
        if 1 <= unstick_count:
            cheat_num = []
        if ((130000 > cheat_num) and (cheat_num > 65100)):
            high_pot_pos = cheat_num
            low_pot_pos  = cheat_num - 1000
            do_check = False
        elif(( 0 < cheat_num) and (cheat_num <= 65100)):
            high_pot_pos = cheat_num+1000
            low_pot_pos  = cheat_num
            do_check = False
        elif cheat_num == []:
            high_pot_pos = high_pot_pos_defult
            low_pot_pos  = low_pot_pos_defult
            do_check = True
        else:
            if verbose:
                print "Cheat_num not set properly in setSIS_Volt, using defaults for pot sweep"
                print "Cheat_num = " + str(cheat_num)
            high_pot_pos = high_pot_pos_defult 
            low_pot_pos  = 35000
            do_check = False
        
        # check to make sure the user input was within the range of values that won't damage the SIS device
        if ((mV_user > mV_min) and (mV_user < mV_max)):
            if verbose:
                print "Setting SIS bias to "+str(mV_user)+" mV"
        else:
            print "mV_user is not within the range of acceptable parameters "+str(mV_min)+ "mV to "+str(mV_max)+"mV"
            print "mV_user = "+str(mV_user)
            print "killing the script"
            sys.exit()
        
        # feedback needs to be turned on to find a unique and stable voltage
        status = setfeedback(True)
        if not status:
            print "the function setfeedback failed in setSIS_Volt"
            print "killing the script"
            sys.exit()
        if verbose:
            print "SIS feedback is on (V-mode)"
            
        # Get data for a linear interpolation of the magpot to voltage relation
        
        # find 'high' qnd 'low' SIS voltage
        
        if low_pot_pos  == 62000:
            setSIS_only(low_pot_pos, True, verbose, careful)
            mV_list = []
            for n in range(intep_meas):
                mV_temp, uA_temp, low_pot_pos = measSIS(verbose)
                mV_list.append(mV_temp)
            mV_low = numpy.mean(numpy.array(mV_list))
            
            setSIS_only(high_pot_pos, True, verbose, careful) 
            time.sleep(0.5)
            mV_list = []
            for n in range(intep_meas):
                mV_temp, uA_temp, high_pot_pos = measSIS(verbose)
                mV_list.append(mV_temp)
            mV_high = numpy.mean(numpy.array(mV_list))

        #elif high_pot_pos == 68000:
        else:
            setSIS_only(high_pot_pos, True, verbose, careful) 
            mV_list = []
            for n in range(intep_meas):
                mV_temp, uA_temp, high_pot_pos = measSIS(verbose)
                mV_list.append(mV_temp)
            mV_high = numpy.mean(numpy.array(mV_list))
            
            setSIS_only(low_pot_pos, True, verbose, careful)
            time.sleep(0.5)
            mV_list = []
            for n in range(intep_meas):
                mV_temp, uA_temp, low_pot_pos = measSIS(verbose)
                mV_list.append(mV_temp)
            mV_low = numpy.mean(numpy.array(mV_list))
    
        # make fit a line to the min and max data points (find m,b in Y=mX+b)
        m = (high_pot_pos-low_pot_pos)/(mV_high-mV_low)
        b = low_pot_pos - m*mV_low
        
        # estimator  the final pot position from the max min line
        est_pot_pos=m*mV_user+b
        
        ### Start the Voltage adjustment algorithm
        # reset to neutral position
        setSIS_only(est_pot_pos, True, verbose, careful) 
        mV_sis, uA_sis, pot_sis = measSIS(verbose)
        
        finished = False
        ebrake   = False
        subloop  = True
        current_position = pot_sis
        mV_current       = mV_sis
        uA_current       = uA_sis
        # uA_current     = uA_sis 
        loop_count      = 0
        pot_diff         = 999999
        diff = mV_current - mV_user
        loop_frac        = 0.707
        
        while not finished:
            if ebrake:
                print "The SIS voltage finding algorithm looped more than " + str(loop_hard_max) + " times"
                print "restarting algorithm"
                unstick = unstick + 1
                finished = True
            elif ((abs(diff) <= loop_thresh) or (abs(pot_diff) < pot_diff_thresh)):
                if verbose:
                    print " The SIS Voltage finding algorithm completed after "
                    print str(loop_count) + " loops"
                    print str(mV_current) + " = mV_current"
                    print str(mV_user) + " = mV_user"
                    print str(current_position) + " = current pot position"
                    #print " "
                    print str(diff) + " = diff"
                    print str(pot_diff) + " diff in terms of pot values"
                    finished = True
                    unstick = False
            else:
                if subloop:    
                    new_position          = current_position*(1-loop_frac)+est_pot_pos*loop_frac
                    if 100000 < new_position:
                        new_position = 90000
                    elif new_position < 30000:
                        new_position = 40000
                    setSIS_only(new_position, True, verbose, careful)
                    time.sleep(1)
                    subfinished = False
                    SEM         = 999999
                    STD         = 999999
                    subloop_count = 0
                    mV_list       = []
                    uA_list       = []
                    while not subfinished:
                        if (SEM < diff):
                            subfinished = True
                        elif subloop_count >= subloop_hard_max:
                            subfinished = True
                            finished = True
                            unstick = False
                            if verbose:
                                print "careful is off and the number of subloops has exceeded the maximum value."
                                print "The script will continue without having reached the user specified SEM standard error of mean: "+str(SEM_user)
                        elif (careful and subloop_count >= subloop_max):
                            print "careful is on and the sub loop exceeded the allow number of loops: "+str(subloop_max)
                            print "the was not able to reached the user specified SEM standard error of mean: "+str(SEM_user)
                            print "SEM was "+str(SEM)
                            print "killing the script"
                            sys.exit()
                        else:
                            subloop_count = subloop_count +1
                            mV_temp, uA_temp, pot_temp = measSIS(verbose)
                            mV_list.append(mV_temp)
                            uA_list.append(uA_temp)
                            #pot_list.append(pot_temp)
                            
                            if subloop_count >= subloop_min:
                                mV_array = numpy.array(mV_list)
                                STD = numpy.std(mV_array)
                                SEM = STD/numpy.sqrt(subloop_count)
                    mV_current = numpy.mean(mV_array)
                    uA_current            = numpy.mean(numpy.array(uA_list))
                    current_position      = pot_temp
                    diff                  = mV_current - mV_user
                    pot_diff              = diff*m
                    est_pot_pos           = current_position + m*(mV_user - mV_current)
                    
                        
                else:
                    new_position          = current_position*(1-loop_frac)+est_pot_pos*loop_frac            
                    setSIS_only(new_position, True, verbose, careful) 
                    mV_current, uA_current, pot_current = measSIS(verbose)
                    current_position      = pot_current
                    diff                  = mV_current - mV_user
                    pot_diff              = diff*m
                    est_pot_pos           = current_position + m*(mV_user - mV_current)
                
                if verbose:
                    if subloop:
                        print str(subloop_count)+" is the sub loop count"
                        print str(STD) + " is the standard deviation"
                        print str(SEM) + " is the stardard deviation of the mean"
                
                # this makes the step size finer as we get closer to the user specified voltage (mV)
                
                if pot_diff <= 200:
                    loop_frac = 0.25
                    subloop  = True
                elif pot_diff <= 500:
                    loop_frac = 0.35
                    subloop  = True   
                elif pot_diff <= 1000:
                    loop_frac = 0.4
                    subloop  = True
                elif pot_diff <= 2000:
                    loop_frac = 0.5
                    subloop  = False
                
                if verbose:
                    print str(loop_count) + " = loop_count "
                    print str(mV_current) + " = mV_current"
                    print str(mV_user) + " = mV_user"
                    print str(current_position) + " = current pot position"
                    #print " "
                    print str(diff) + " = diff"
                    print str(pot_diff) + " diff in terms of pot values"
                    print " "
                if (careful and loop_count >= loop_max):
                    print "careful is true and the loop count of the first loop exceeded"
                    print "the maximum allow value of "+str(loop_max)
                    print "killing the script"
                    sys.exit()
            
                loop_count = loop_count + 1
                if loop_count >= loop_hard_max:
                    ebrake = True
    
    mV_sis   = mV_current
    uA_sis  = uA_current
    pot_sis = current_position
    #print mV_array
        
    # Now we check the surrounding points to see if the mean value is the same user value at this pot position
    if do_check:
        restart = True
        restart_count = 0
        while restart:
            if verbose:
                print str(restart_count) + " is the restart_count"
                print str(check_radius) + " is the check_radius"     
            check_num = check_radius*2+1    
            
            mV_test   = numpy.zeros(check_num)
            uA_test   = numpy.zeros(check_num)
            pot_test  = numpy.zeros(check_num)
            diff_test = numpy.zeros(check_num)
        
            for n in range(check_num):
                # print str(new_position) + " = new position"
    	       
                new_position = (n - check_radius)*pot_per_check + pot_sis
                setSIS_only(new_position, True, verbose, careful)
                # print str(new_position) + " = new position"
                time.sleep(0.2)
                
                finished3 = False
                SEM         = 999999
                STD         = 999999
                loop3_count = 0
                mV_list       = []
                uA_list       = []
                while not finished3:
                    mV_temp, uA_temp, pot_temp = measSIS(verbose)
                    if SEM < SEM_user2:
                        finished3 = True
                    elif loop3_count >= loop3_hard_max:
                        finished3 = True
                        if verbose:
                            print "loops has exceeded the maximum value for loop3."
                            print "The script will continue without having reached the user specified SEM standard error of mean: "+str(SEM_user2)
                    elif (careful and loop3_count >= loop3_max):
                        print "careful is on and the loop3 exceeded the allow number of loops: "+str(loop3_max)
                        print "the was not able to reached the user specified SEM standard error of mean: "+str(SEM_user2)
                        print "SEM was "+str(SEM)
                        print "killing the script"
                        sys.exit()
                    else:
                        loop3_count = loop3_count +1
                        mV_temp, uA_temp, pot_temp = measSIS(verbose)
                        mV_list.append(mV_temp)
                        uA_list.append(uA_temp)
                        #pot_list.append(pot_temp)
                                
                        if loop3_count >= loop3_min:
                            mV_array = numpy.array(mV_list)
                            STD = numpy.std(mV_array)
                            SEM = STD/numpy.sqrt(loop3_count)
                            mV_current = numpy.mean(mV_array)
                uA_current            = numpy.mean(numpy.array(uA_list))
                current_position      = pot_temp
                diff_current          = mV_current - mV_user
                #pot_diff              = diff*m
                
                if verbose:
                    print " "
                    print "Loop3, check " + str(n+1) + " of " + str(check_num)
                    print "The loop count is " + str(loop3_count)
                    print str(mV_current) + " =  mV"
                    print str(uA_current) + " =  uA"
                    print str(current_position) + " =  pot position"
                    print str(diff_current) + " =  diff in mV"
                    print str(SEM) + " = SEM"
                    
                mV_test[n] = mV_current
                uA_test[n] = uA_current
                pot_test[n] = current_position
                diff_test[n] = diff_current
                
            
            data = numpy.zeros((len(mV_test),2))
            data[:,0] = pot_test
            data[:,1] = abs(diff_test)
            
            regrid_data, status = regrid(data, 1, verbose)
            conv_data, status = conv(regrid_data, 1, min_cdf, sigma, verbose)
            mono_data = numpy.asarray(sorted(conv_data, key=itemgetter(1)))    
            if verbose:
                print str(int(mono_data[0,0])) +" is the pot position."
                print str(mono_data[0,1]) +" is min convolved minimum distance in mV"
            setSIS_only(mono_data[0,0], True, verbose, careful)
            if verbose:
                print "Pot set"
            if show_plot:
                plt.clf()
                plt.plot(pot_test,abs(diff_test))
                plt.plot(conv_data[:,0],conv_data[:,1])
                plt.show()
                plt.draw()
            
            restart = False
            left_bound = abs(diff_test[0])
            right_bound = abs(diff_test[len(diff_test)-1])
            
            
            if ((mono_data[0,1] > bound_diff + left_bound) or (mono_data[0,1] > bound_diff + right_bound ) ):
                if restart_count >= restart_count_max:
                    if careful:
                        print "careful is on and the check loop in the function setSIS has restart more than"
                        print "the allowed number of times: "+ str(restart_count_max)
                        print "killing the script"
                        sys.exit()
                    else: 
                        if verbose:
                            print "careful is off and the check loop in the function setSIS has restart more than"
                            print "the allowed number of times: "+ str(restart_count_max)
                            print "function will be allowed to exit normally using the best value it could find"
                else:
                    restart = True
                    
                if restart:
                    restart_count = restart_count +1
                    check_radius = check_radius + 1
                    if verbose:
                        print "The check part of setSIS_Volt need to be restarted the boundaries of the checking " \
                              "function "
                        print str(mono_data[0,1]) + " mV is the minimum difference value, and need to be " + \
                              str(bound_diff) + " mV"
                        print "above the boundaries values of " + str(left_bound) + " and " + str(right_bound)
    if verbose:
        print " "
        print " "
    return mV_sis, uA_sis, pot_sis
#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, True, 56666)


####################
###### setLOI ######
####################

def setLOI(uA_user, verbose=False, careful=False):
    from setLOI_config import uA_max, uA_min, sleep_time, max_meas_per_loop, scan_count_max, count_min
    
    # check to make sure the user input was within the range of values that can be achieved
    if ((uA_user > uA_min) and (uA_user < uA_max)):
        if verbose:
            print "Setting LO bias current to "+str(uA_user)+" uA"
    else:
        print "uA_user is not within the range of acceptable parameters "+str(uA_min)+ "uA to "+str(uA_max)+"uA"
        print "uA_user = "+str(uA_user)
        print "killing the script"
        sys.exit()
    
    # Fully attenuate the LO
    status = LabJackU3_DAQ0(5)
    if not status:
        print "LabJackU3_DAQ0 failed in setLOI"
        print "killing the script"
        sys.exit()
    
    # set the SIS voltage
    time.sleep(1)
    mV_sis, uA_sis, cheat_mVpot = measSIS(verbose)
    
    # does the uA current measured with full LO attenuation exceeds the user specified value
    if uA_sis > uA_user:
        if careful:
            print "uA current " + str(uA_sis) + " uA measured with full LO attenuation,"
            print " exceeds the user specified value of " + str(uA_user) + " uA."
            print "in the function setLOI"
            print " careful is on, killing the script"
            sys.exit()
        else:
            print "uA current " + str(uA_sis) + " uA measured with full LO attenuation,"
            print " exceeds the user specified value of " + str(uA_user) + " uA."
            print " careful is off, I will allow the script to attempt to set the current anyway"
    time.sleep(sleep_time)
    
    # LO attentuation OFF
    status = LabJackU3_DAQ0(0)
    if not status:
        print "LabJackU3_DAQ0 failed in setLOI"
        print "killing the script"
        sys.exit()
    
    # measure the new settings with the unattenuated LO
    mV_sis, uA_sis, pot_sis = measSIS(verbose)
    
    # does the uA current measured with NO LO attenuation fall under the user specified value
    if uA_sis < uA_user:
        if careful:
            print "uA current " + str(uA_sis) + " uA, measured with No LO attenuation,"
            print "is less than the user specified value of " + str(uA_user) + " uA."
            print "in the function setLOI"
            print " careful is on, killing the script"
            sys.exit()
        else:
            print "uA current " + str(uA_sis) + " uA, measured with No LO attenuation,"
            print "is less than the user specified value of " + str(uA_user) + " uA."
            print " careful is off, I will allow the script to attempt to set the current anyway"

    # here we do a simple binary search to find the region wear the uA_user is near
    Vfrac = 2.5 # Votage range of search (This is the initial range that is cut in half each loop)
    UCA_current = float(2.5) # first guess in sweep
    status = LabJackU3_DAQ0(UCA_current)
    mV_temp, uA_current, pot_temp = measSIS(verbose)
    if uA_current < uA_user:
        sign = -1
    elif uA_current >= uA_user:
           sign = 1
    scan_finished = False
    scan_count = 0
    while not scan_finished:
        scan_count = scan_count + 1
        Vfrac = Vfrac/2
        #UCA_prev = UCA_current
        uA_prev = uA_current 
        UCA_current = UCA_current + sign*Vfrac
        status = LabJackU3_DAQ0(UCA_current)
        time.sleep(sleep_time)
        if verbose:
            print str(scan_count) + " is the scan count"
            print str(UCA_current) + " is the UCA voltage"
            print str(uA_current) + " is the Current in uA"
            print str(Vfrac)    + "  is the voltage change (Vfrac)"
            
            
        # We measure enough times achieve the accuracy needed to make the next step.
        meas_finished = False
        uA_list = []
        count = 0
        while not meas_finished:
            count = count + 1
            mV_temp, uA_temp, pot_temp = measSIS(verbose)
            uA_list.append(uA_temp)
            uA_array = numpy.array(uA_list)
            STD = numpy.std(uA_array)
            SED = STD/numpy.sqrt(count)
            uA_current = numpy.mean(uA_array)
            uA_est_change = abs(uA_current - uA_prev)/2
            
            if verbose:
                print str(uA_est_change) + " is the estimated change in uA for this step in voltage"
                
            if ((SED < uA_est_change) and (count_min <= count)):
                meas_finished = True
            elif max_meas_per_loop <= count:
                scan_finished = True
                meas_finished = True
        uA_current = numpy.mean(uA_array)
        if verbose:
            print str(count) + " is the measurement count"
            print str(SED)   + "  is the standard deviation of the mean"
            print " "
            if scan_finished:
                print "# Scan finished #"
                
        if uA_current < uA_user:
            sign = -1
        elif uA_current >= uA_user:
            sign = 1
        else:
            if careful:
                print "careful is on and uA_sis seems to not be a number"
                print "near binary search in function setLOI"
                print "killing script"
                sys.exit
        if scan_count_max <= scan_count:
            scan_finished = True
            if verbose:
                print "scan_count = scan_count_max = "+str(scan_count_max)
            if careful:
                print " Careful is on scan_count_max exceed, killing script"
                sys.exit() 
    
    UCA_val = UCA_current
    if verbose:
        print " "
        print " "
    return mV_sis, uA_sis, pot_sis, UCA_val
# setSIS_Volt   
#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, False, 56666)
# setLOI
#mV_sis, uA_sis, pot_sis, UCA_val = setLOI(10, True, True, 3.45751953125)
# setSIS_Volt   
#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, True, [])



######################
###### zeropots ######
######################
  
def zeropots(verbose=True):
    from sisbias_config import zeropots_center_pos, zeropots_feedback, zeropots_careful, zeropots_max_count,\
        zeropots_do_mag, zeropots_do_sis, zeropots_do_LO, UCA_voltage
    # from LOinput import RFoff
    status   = False
    finished = False  
    count = 0
    if (zeropots_do_mag and zeropots_do_sis):
        while not finished:
            count = count + 1
            if zeropots_do_mag:
                time.sleep(1)
                V_mag,  mA_mag, pot_mag = setmag(zeropots_center_pos, verbose)
                if verbose:
                    print V_mag,  mA_mag, pot_mag, " Magnet"
            if zeropots_do_sis:
                mV_sis, uA_sis, pot_sis = setSIS(zeropots_center_pos, zeropots_feedback, verbose, zeropots_careful)
                time.sleep(1)
                if verbose:
                    print mV_sis, uA_sis, pot_sis, " SIS bias"

            if ((pot_mag == zeropots_center_pos) and (pot_sis == zeropots_center_pos)):
                status   = True
                finished = True
                if verbose:
                    print "Both the electromagnet and the SIS bias pots have been set to the central pot position: " + str(zeropots_center_pos)
            elif (zeropots_max_count < count):
                print "The max number of tries to zero the pot: " + str(zeropots_max_count)
                print "has been exceeded, returning status = False"
                finished = True
            elif ((pot_mag == zeropots_center_pos) and not (pot_sis == zeropots_center_pos)):
                if verbose:
                    print "The electromagnet was set to the central pot position: " + str(zeropots_center_pos)
                    print "But, the SIS bias pot was not set properly, it value is: " + str(pot_sis)
                zeropots_do_mag = False
            elif (not (pot_mag == zeropots_center_pos) and (pot_sis == zeropots_center_pos)):
                if verbose:
                    print "The SIS bias pot was set to the central pot position: " + str(zeropots_center_pos)
                    print "But, the electromagnet pot was not set properly, it value is: " + str(pot_mag)
                zeropots_do_sis = False
            elif (not (pot_mag == zeropots_center_pos) and not (pot_sis == zeropots_center_pos)):
                if verbose:
                    print "Neither the SIS pot nor the elecromagnet pot were zeroed."
                    print str(pot_mag) + ":pot_mag"
                    print str(pot_sis) + ":pot_sis"
                    print "Trying again: attempt " + str(count + 1) + " of " + str(zeropots_max_count)

    elif zeropots_do_sis:
        while not finished:
            count = count + 1
            mV_sis, uA_sis, pot_sis = setSIS(zeropots_center_pos, zeropots_feedback, verbose, zeropots_careful)
            if (pot_sis == zeropots_center_pos):
                status   = True
                finished = True
                if verbose:
                    print "Both the SIS bias pot has been set to the central pot position: " + str(zeropots_center_pos)
            elif zeropots_max_count < count:
                print "The max number of tries to zero the pot: " + str(zeropots_max_count)
                print "has been exceeded, returning status = False"
            elif not (pot_sis == zeropots_center_pos): 
                if verbose:
                    print "The SIS pot was not zeroed"
                    print "Trying again: attempt " + str(count + 1) + " of " + str(zeropots_max_count)
    
    
    if zeropots_do_LO:
        if (UCA_voltage == 0 or UCA_voltage == 5):
            None
        else:
            UCA_voltage = 0
            if verbose:    
                print "Print the UCA voltage was not properly set, it should be 0 or 5 (Volts)"
                print "the safty feature in this scrip is setting it to: " + str(UCA_voltage) + " Volts"
                
        LO_str = "UCA voltage was set to " + str(UCA_voltage) + " Volts "        
        if UCA_voltage == 0:
            LO_str = LO_str + " (No LO Attenuation)"
        if UCA_voltage == 5:
            LO_str = LO_str + " (Full LO Attenuation)"
            
        finished2 = False
        count2 = 0
        while not finished2:
            count2 = count2 + count2
            status2 = LabJackU3_DAQ0(UCA_voltage)
            if status2:
                finished2 = True
                if verbose:
                    print "The LO has been zeroed"
                    print LO_str
                    
            elif zeropots_max_count < count2:
                status = False
                finished2 = True
                print "The max number of tries to zero the LO has been reached: " + str(zeropots_max_count)
                print "returning status = False"
        
        # turn off the Anritsu signal generator
        # RFoff()
        # print "The Anritsu Signal generator has been sent the command to turn off its RF output."
                
    return status

def zeroSISpot(verbose=True):
    from sisbias_config import zeropots_center_pos, zeropots_feedback, zeropots_careful, zeropots_max_count
    finished = False
    count = 0
    status = False
    while not finished:
        count = count + 1
        mV_sis, uA_sis, pot_sis = setSIS(zeropots_center_pos, zeropots_feedback, verbose, zeropots_careful)
        if (pot_sis == zeropots_center_pos):
            status   = True
            finished = True
            if verbose:
                print "SIS bias pot has been set to the central pot position: " + str(zeropots_center_pos)
        elif zeropots_max_count < count:
            print "The max number of tries to zero the pot: " + str(zeropots_max_count)
            print "has been exceeded, returning status = False"
        elif not (pot_sis == zeropots_center_pos):
            if verbose:
                print "The SIS pot was not zeroed"
                print "Trying again: attempt " + str(count + 1) + " of " + str(zeropots_max_count)

    return status


def zeroMAGpot(verbose=True):
    from sisbias_config import zeropots_center_pos, zeropots_feedback, zeropots_careful, zeropots_max_count
    finished = False
    count = 0
    status = False
    while not finished:
        count = count + 1
        V_mag, mA_mag, pot_mag = setmag(zeropots_center_pos)
        if (pot_mag == zeropots_center_pos):
            status   = True
            finished = True
            if verbose:
                print "mag bias pot has been set to the central pot position: " + str(zeropots_center_pos)
        elif zeropots_max_count < count:
            print "The max number of tries to zero the pot: " + str(zeropots_max_count)
            print "has been exceeded, returning status = False"
        elif not (pot_mag == zeropots_center_pos):
            if verbose:
                print "The mag pot was not zeroed"
                print "Trying again: attempt " + str(count + 1) + " of " + str(zeropots_max_count)

    return status
