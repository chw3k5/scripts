import telnetlib
import time
import sys

import numpy

from LabJack_control import LabJackU3_DAQ0


sis_channel = '0'
mag_channel = '10'

sleep_list = [0.3, 0.7, 2, 5, 10, 30, 60, 120]
sleep_per_meas          = sleep_list[0]
sleep_per_meas_feedback = 0.5

SIS_feedon_low  = 30000
SIS_feedon_high = 100000
# feedback = False (off)
SIS_feedoff_low = 53000
SIS_feedoff_high = 77000

default_magpot = 100000 # 65 mA ### 89179 # 45 mA
default_sispot = 59100 # 1.3 mV ### 56800 # 1.8 mV ### 59100 # 1.3 mV
default_LOfreq = 672 # GHz
default_UCA    = 0 # V
default_IF     = 2.3 # GHz



zeropots_center_pos=65100
zeropots_feedback=False
zeropots_careful=False
zeropots_max_count=20
zeropots_do_mag=True
zeropots_do_sis=True
zeropots_do_LO=False
UCA_voltage=5



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
    # time.sleep(sleep_per_meas)     

    
    V_mag, mA_mag, pot_mag = measmag(verbose)
    return V_mag, mA_mag, pot_mag
 

#########################
###### setmag_only ######
#########################
             
def setmag_only(magpot):
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
    # time.sleep(sleep_per_meas)     

    return

############################
###### setmag_highlow ######
############################
             
def setmag_highlow(magpot):
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
    # time.sleep(sleep_per_meas)     

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
    #time.sleep(sleep_per_meas)
    return mV_sis, uA_sis, pot_sis
    
    
#########################
###### setfeedback ######
#########################

def setfeedback(feedback):
    status=False
    if feedback:
        thzbiascomputer.write("feedback 1 \n")
        time.sleep(sleep_per_meas_feedback)
    else:
        thzbiascomputer.write("feedback 0 \n")
        time.sleep(sleep_per_meas_feedback)
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
        if ((SIS_feedon_low < sispot) and (sispot < SIS_feedon_high)):
            None
        else:
            print "sispot value was not in the set [" + str(SIS_feedon_low) + " to " + str(SIS_feedon_high) + "]"
            print "~[7.5V to -7.5V] for feedback 'ON', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safety catches"
            print "make sure the SIS switch located on the Dewar is set to 'Thru' (not 'Open')"
            if careful:
                print "killing script"
                sys.exit()
            elif SIS_feedon_high < sispot:
                sispot = SIS_feedon_high - 1000
            elif sispot < SIS_feedon_low:
                sispot = SIS_feedon_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)
    else:
        if ((SIS_feedoff_low < sispot) and (sispot < SIS_feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(SIS_feedoff_low) + " to " + str(SIS_feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safety catches"
            print "make sure the SIS switch located on the Dewar is on 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif SIS_feedoff_high < sispot:
                sispot = SIS_feedoff_high - 1000
            elif sispot < SIS_feedoff_low:
                sispot = SIS_feedoff_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)

    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias " + sis_channel + " "+str(numpy.round(sispot)) + " \n")
    #time.sleep(sleep_per_meas)     

    
    mV_sis, uA_sis, pot_sis = measSIS(verbose=True)


    return mV_sis, uA_sis, pot_sis


#########################
###### setSIS_only ######
#########################

def setSIS_only(sispot, feedback, verbose=False, careful=False):  
    
    # safty catches, to keep the SIS bias within nominal ranges   
    if feedback:
        if ((SIS_feedon_low < sispot) and (sispot < SIS_feedon_high)):
            None
        else:
            print "sispot value was not in the set [" + str(SIS_feedon_low) + " to " + str(SIS_feedon_high) + "]"
            print "~[7.5V to -7.5V] for feedback 'ON', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safety catches"
            print "make sure the SIS switch located on the Dewar set to 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif SIS_feedon_high < sispot:
                sispot = SIS_feedon_high - 1000
            elif sispot < SIS_feedon_low:
                sispot = SIS_feedon_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "resetting pot to safe value: " + str(sispot)
                
    else:
        if ((SIS_feedoff_low < sispot) and (sispot < SIS_feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(SIS_feedoff_low) + " to " + str(SIS_feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try again"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safety catches"
            print "make sure the SIS switch located on the Dewar is set to 'Thru' (not Open)"
            if careful:
                print "killing script"
                sys.exit()
            elif SIS_feedoff_high < sispot:
                sispot = SIS_feedoff_high - 1000
            elif sispot < SIS_feedoff_low:
                sispot = SIS_feedoff_low + 1000
            else:
                sispot = 65100
            print "careful is off, so the show must go on"
            print "reseting pot to safe value: " + str(sispot)
    #set the pot position of the magnet and record the current and voltage
    thzbiascomputer.write("setbias "+sis_channel+" "+str(numpy.round(sispot)) + " \n")
    time.sleep(sleep_per_meas)
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

    # turn the feedback on or off
    status = setfeedback(feedback)
    if (not status and careful):
        print "The feedback was not set properly"
        print "Killing script"
        sys.exit()
    
    # we need to set the pot before measuring Total Power
    setSIS_only(sispot, feedback, verbose, careful)
    time.sleep(sleep_per_meas)
    
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
    channel = sis_channel
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



##########################
###### measloop_SIS ######
##########################

def measloop_SIS(feedback,sispot=65100, sleep_per_set=1, meas_number=1, verbose=False):
    setSIS_only(sispot,feedback=feedback)
    time.sleep(sleep_per_set)
    mV_list = []
    uA_list = []
    for n in range(meas_number):
        mV_temp, uA_temp, pot_temp = measSIS(verbose)
        mV_list.append(mV_temp)
        uA_list.append(uA_temp)
    return mV_list, uA_list


##########################
###### measloop_SIS ######
##########################

def measloop_SIS_TP(feedback,sispot=65100, sleep_per_set=1, meas_number=1, verbose=False):
    setSIS_only(sispot,feedback=feedback)
    time.sleep(sleep_per_set)
    mV_list = []
    uA_list = []
    tp_list = []
    time_stamp_list = {}
    for n in range(meas_number):
        mV_temp, uA_temp, tp_temp, pot_temp, time_stamp_temp = measSIS_TP(sispot=sispot,feedback=feedback,verbose=False)
        mV_list.append(mV_temp)
        uA_list.append(uA_temp)
        tp_list.append(tp_temp)
        time_stamp_list.append(time_stamp_temp)
    return mV_list, uA_list, tp_list, time_stamp_list


######################
###### zeropots ######
######################
  
def zeropots(verbose=True):
    # from LOinput import RFoff
    zeropots_do_mag=True
    zeropots_do_sis=True
    zeropots_do_LO=False
    UCA_voltage=5
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
                print "the saftey feature in this scrip is setting it to: " + str(UCA_voltage) + " Volts"
                
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
