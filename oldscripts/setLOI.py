def measSIS(verbose):
    import telnetlib
    import time
    import sys 
    
    
    SleepPerMes = 0.5 # in seconds 
    
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    mV_sis  = -999999
    uA_sis  = -999999
    pot_sis = -999999
        
    tn.write("setbias 0 \n")
    time.sleep(SleepPerMes)
    out1 = tn.read_very_eager()
    out2 = out1.replace('sis 0 ', '')
    out3 = out2.replace(' = ', ',')
    
    end_position1=out3.find('\n', 0)
    mV_string=out3[0:end_position1]
    
    end_position2=out3.find('\n', end_position1+1)
    uA_string=out3[end_position1+1:end_position2]
    
    end_position3=out3.find('\n', end_position2+1)
    f_string=out3[end_position2+1:end_position3]
    
    end_position4=out3.find('\n', end_position3+1)
    pot_string=out3[end_position3+1:end_position4]
    
    mV_start  = mV_string.find(',',0)
    uA_start  = uA_string.find(',',0)
    pot_start = pot_string.find(',',0)
    
    mV_sis_temp  = mV_string[mV_start+1:]
    uA_sis_temp  = uA_string[uA_start+1:]
    pot_sis_temp = pot_string[pot_start+1:]
    
    if (mV_sis_temp == '' or uA_sis_temp == '' or f_string == '' or pot_sis_temp == ''):
        if verbose:
            print "Had to wait extra time for the measurment to be returned"
        tn.write("setbias 0 \n")
        time.sleep(1)
        out1 = tn.read_very_eager()
        out2 = out1.replace('sis 0 ', '')
        out3 = out2.replace(' = ', ',')
        
        end_position1=out3.find('\n', 0)
        mV_string=out3[0:end_position1]
    
        end_position2=out3.find('\n', end_position1+1)
        uA_string=out3[end_position1+1:end_position2]
                 
        end_position3=out3.find('\n', end_position2+1)
        f_string=out3[end_position2+1:end_position3]
    
        end_position4=out3.find('\n', end_position3+1)
        pot_string=out3[end_position3+1:end_position4]
    
        mV_start  = mV_string.find(',',0)
        uA_start  = uA_string.find(',',0)
        pot_start = pot_string.find(',',0)
        
        mV_sis_temp  = mV_string[mV_start+1:]
        uA_sis_temp  = uA_string[uA_start+1:]
        pot_sis_temp = pot_string[pot_start+1:]
                
        if (mV_sis_temp == '' or uA_sis_temp == '' or f_string == '' or pot_sis_temp == ''):

            if verbose:
                print "Had to wait extra time for the measurment to be returned again"
            tn.write("setbias 0 \n")
            time.sleep(5)
            out1 = tn.read_very_eager()
            out2 = out1.replace('sis 0 ', '')
            out3 = out2.replace(' = ', ',')
        
            end_position1=out3.find('\n', 0)
            mV_string=out3[0:end_position1]
        
            end_position2=out3.find('\n', end_position1+1)
            uA_string=out3[end_position1+1:end_position2]
                       
            end_position3=out3.find('\n', end_position2+1)
            f_string=out3[end_position2+1:end_position3]
    
            end_position4=out3.find('\n', end_position3+1)
            pot_string=out3[end_position3+1:end_position4]
        
            mV_start  = mV_string.find(',',0)
            uA_start  = uA_string.find(',',0)
            pot_start = pot_string.find(',',0)
            
            mV_sis_temp  = mV_string[mV_start+1:]
            uA_sis_temp  = uA_string[uA_start+1:]
            pot_sis_temp = pot_string[pot_start+1:]
        
            if (mV_sis_temp == '' or uA_sis_temp == '' or f_string == '' or pot_sis_temp == ''):
                if verbose:
                    print "Had to wait extra time for the measurment to be returned again x2"
                tn.close()
                time.sleep(5)
                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                time.sleep(5)
                tn.write("setbias 0 \n")
                time.sleep(15)
                out1 = tn.read_very_eager()
                out2 = out1.replace('sis 0 ', '')
                out3 = out2.replace(' = ', ',')
            
                end_position1=out3.find('\n', 0)
                mV_string=out3[0:end_position1]
            
                end_position2=out3.find('\n', end_position1+1)
                uA_string=out3[end_position1+1:end_position2]
                           
                end_position3=out3.find('\n', end_position2+1)
                f_string=out3[end_position2+1:end_position3]
    
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
            
                mV_start  = mV_string.find(',',0)
                uA_start  = uA_string.find(',',0)
                pot_start = pot_string.find(',',0)
                
                mV_sis_temp  = mV_string[mV_start+1:]
                uA_sis_temp  = uA_string[uA_start+1:]
                pot_sis_temp = pot_string[pot_start+1:]
            
                if (mV_sis_temp == '' or uA_sis_temp == '' or f_string == '' or pot_sis_temp == ''):
                    print "Had to wait extra time for the measurment to be returned again x3"
	            print out3
                    print "mV_sis_temp  = " + mV_sis_temp
                    print "uA_sis_temp = "  + uA_sis_temp
                    print "t_string    = "  + f_string
                    print "pot_sis_temp  = "  + pot_sis_temp
                    print " "
                    tn.close()
                    time.sleep(5)
                    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                    time.sleep(5)
                    
                    tn.write("setbias 0 \n")
                    time.sleep(30)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('sis 0 ', '')
                    out3 = out2.replace(' = ', ',')
                
                    end_position1=out3.find('\n', 0)
                    mV_string=out3[0:end_position1]
                
                    end_position2=out3.find('\n', end_position1+1)
                    uA_string=out3[end_position1+1:end_position2]
                    
                               
                    end_position3=out3.find('\n', end_position2+1)
                    f_string=out3[end_position2+1:end_position3]
        
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                
                    mV_start  = mV_string.find(',',0)
                    uA_start  = uA_string.find(',',0)
                    pot_start = pot_string.find(',',0)
                    
                    mV_sis_temp  = mV_string[mV_start+1:]
                    uA_sis_temp  = uA_string[uA_start+1:]
                    pot_sis_temp = pot_string[pot_start+1:]
                
                    if (mV_sis_temp == '' or uA_sis_temp == '' or f_string == '' or pot_sis_temp == ''):
                        print "The script had to wait to long to read a value of mV and uA"
	                print "Killing the script"
	                print out3
                        print "mV_sis_temp  = " + mV_sis_temp
                        print "uA_sis_temp = "  + uA_sis_temp
                        print "t_string    = "  + f_string
                        print "pot_sis_temp  = "  + pot_sis_temp
                        print " "
        	        sys.exit()
            
    mV_sis  = float(mV_string[mV_start+1:])
    uA_sis  = float(uA_string[uA_start+1:])
    pot_sis = int(float(pot_string[pot_start+1:]))
    time.sleep(SleepPerMes)
    tn.close()
    return mV_sis, uA_sis, pot_sis
    
def setfeedback(feedback):
    import telnetlib
    import time
    
    status=False
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    if feedback:
        tn.write("feedback 1 \n")
        time.sleep(1)
    else:
        tn.write("feedback 0 \n")
        time.sleep(1)
    out1 = tn.read_very_eager()
    if feedback:
        if out1 == 'Enabling SIS feedback loop (V-mode)\n':
            status=True
        else:
            print "the feedback command did not get the expected string <Enabling SIS feedback loop (V-mode)\n>. Check the connection to the THz bias computer"
    elif not feedback:
        if out1 == 'Disabling SIS feedback loop (R-mode)\n':
            status=True
        else:
            print "the feedback command did not get the expected string <Disabling SIS feedback loop (R-mode)\n>. Check the connection to the THz bias computer"
    else:
        print 'The variable feedback can only be True or False. Returning status=False'    
    tn.close()
    
    return status 
    
def setSIS(sispot, feedback, verbose, careful):
    import telnetlib
    import time
    import numpy
    import sys

    SleepPerMes = 0.5 # in seconds 
    feedon_low  = 30000
    feedon_high = 100000
    feedoff_low = 53000
    feedoff_high = 77000
    
    
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
            print "~[7.5V to -7.5V] for feedback 'ON', try agian"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safty catches"
            print "make sure the SIS swich on the Dewar is on Thru (not Open)"
            print "Killing script"
            sys.exit()
    else:
        if ((feedoff_low < sispot) and (sispot < feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedoff_low) + " to " + str(feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try agian"
            print "sispot = " + str(sispot)
            print "in function setSIS, near safty catches"
            print "make sure the SIS swich on the Dewar is on Thru (not Open)"
            print "Killing script"
            sys.exit()

    #set the pot position of the magnet and recound the current and volage
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)    
    tn.write("setbias 0 "+str(numpy.round(sispot)) + " \n")
    time.sleep(SleepPerMes)     
    tn.close()
    
    mV_sis, uA_sis, pot_sis = measSIS(verbose)


    return mV_sis, uA_sis, pot_sis
    
def setSIS_only(sispot, feedback, verbose, careful):
    import telnetlib
    import time
    import numpy
    import sys

    SleepPerMes = 0.5 # in seconds 
    feedon_low  = 30000
    feedon_high = 100000
    feedoff_low = 53000
    feedoff_high = 77000
    
    
    # safty catches, to keep the SIS bias within nominal ranges   
    if feedback:
        if ((feedon_low < sispot) and (sispot < feedon_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedon_low) + " to " + str(feedon_high) + "]"
            print "~[7.5V to -7.5V] for feedback 'ON', try agian"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safty catches"
            print "make sure the SIS swich on the Dewar is on Thru (not Open)"
            print "killing script"
            sys.exit()
    else:
        if ((feedoff_low < sispot) and (sispot < feedoff_high)):
            None
        else:
            print "sispot value was not in the set [" + str(feedoff_low) + " to " + str(feedoff_high) + "]"
            print "~[7.9V to -8.1V] for feedback 'OFF', try agian"
            print "sispot = " + str(sispot)
            print "in function setSIS_only, near safty catches"
            print "make sure the SIS swich on the Dewar is on Thru (not Open)"
            print "killing script"
            sys.exit()

    #set the pot position of the magnet and recound the current and volage
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)    
    tn.write("setbias 0 "+str(numpy.round(sispot)) + " \n")
    time.sleep(SleepPerMes)     
    tn.close()

    return


def setSIS_TP(sispot, feedback, verbose, careful):
    import telnetlib
    import time
    import sys 
    import numpy
    
    SleepPerMes = 0.5 # in seconds 
    
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    mV_sis  = -999999
    uA_sis  = -999999
    tp_sis  = -999999
    pot_sis = -999999
    
    # turn the feedback on or off
    status = setfeedback(feedback)
    if (not status and careful):
        print "The feedback was not set properly"
        print "Killing script"
        sys.exit()
    
    # we need to set the pot before measuring Total Power
    setSIS_only(sispot, feedback, verbose, careful)
        
    tn.write("sweep 0 " + str(numpy.round(sispot)) + " " + str(numpy.round(sispot)) +  " 1  \n")
    time.sleep(SleepPerMes)
    out1 = tn.read_very_eager()
    out2 = out1.replace('sis 0 ', '')
    out3 = out2.replace(' = ', ',')
    
    end_position1=out3.find('\n', 0)
    mV_string=out3[0:end_position1]
    
    end_position2=out3.find('\n', end_position1+1)
    uA_string=out3[end_position1+1:end_position2]
    
    end_position3=out3.find('\n', end_position2+1)
    tp_string=out3[end_position2+1:end_position3]
    
    end_position4=out3.find('\n', end_position3+1)
    pot_string=out3[end_position3+1:end_position4]
    
    mV_start  = mV_string.find(',',0)
    uA_start  = uA_string.find(',',0)
    tp_start  = tp_string.find(',',0)
    pot_start = pot_string.find(',',0)
    
    mV_sis_temp  = mV_string[mV_start+1:]
    uA_sis_temp  = uA_string[uA_start+1:]
    tp_sis_temp  = tp_string[tp_start+1:]
    pot_sis_temp = pot_string[pot_start+1:]
    
    if (mV_sis_temp == '' or uA_sis_temp == '' or tp_sis_temp == '' or pot_sis_temp == ''):
        if verbose:
            print "Had to wait extra time for the measurment to be returned"
        tn.write("sweep 0 " + str(numpy.round(sispot)) + " " + str(numpy.round(sispot)) +  " 1  \n")
        time.sleep(1)
        out1 = tn.read_very_eager()
        out2 = out1.replace('sis 0 ', '')
        out3 = out2.replace(' = ', ',')
        
        end_position1=out3.find('\n', 0)
        mV_string=out3[0:end_position1]
    
        end_position2=out3.find('\n', end_position1+1)
        uA_string=out3[end_position1+1:end_position2]
                 
        end_position3=out3.find('\n', end_position2+1)
        tp_string=out3[end_position2+1:end_position3]
    
        end_position4=out3.find('\n', end_position3+1)
        pot_string=out3[end_position3+1:end_position4]
    
        mV_start  = mV_string.find(',',0)
        uA_start  = uA_string.find(',',0)
        tp_start  = tp_string.find(',',0)
        pot_start = pot_string.find(',',0)
        
        mV_sis_temp  = mV_string[mV_start+1:]
        uA_sis_temp  = uA_string[uA_start+1:]
        tp_sis_temp  = tp_string[tp_start+1:]
        pot_sis_temp = pot_string[pot_start+1:]
        
        if (mV_sis_temp == '' or uA_sis_temp == '' or tp_sis_temp == '' or pot_sis_temp == ''):

            if verbose:
                print "Had to wait extra time for the measurment to be returned again"
            tn.write("sweep 0 " + str(numpy.round(sispot)) + " " + str(numpy.round(sispot)) +  " 1  \n")
            time.sleep(5)
            out1 = tn.read_very_eager()
            out2 = out1.replace('sis 0 ', '')
            out3 = out2.replace(' = ', ',')
        
            end_position1=out3.find('\n', 0)
            mV_string=out3[0:end_position1]
        
            end_position2=out3.find('\n', end_position1+1)
            uA_string=out3[end_position1+1:end_position2]
                       
            end_position3=out3.find('\n', end_position2+1)
            tp_string=out3[end_position2+1:end_position3]
    
            end_position4=out3.find('\n', end_position3+1)
            pot_string=out3[end_position3+1:end_position4]
        
            mV_start  = mV_string.find(',',0)
            uA_start  = uA_string.find(',',0)
            tp_start  = tp_string.find(',',0)
            pot_start = pot_string.find(',',0)
            
            mV_sis_temp  = mV_string[mV_start+1:]
            uA_sis_temp  = uA_string[uA_start+1:]
            tp_sis_temp  = tp_string[tp_start+1:]
            pot_sis_temp = pot_string[pot_start+1:]
            
            if (mV_sis_temp == '' or uA_sis_temp == '' or tp_sis_temp == '' or pot_sis_temp == ''):
                if verbose:
                    print "Had to wait extra time for the measurment to be returned again x2"
                tn.close()
                time.sleep(5)
                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                time.sleep(5)
                tn.write("sweep 0 " + str(numpy.round(sispot)) + " " + str(numpy.round(sispot)) +  " 1  \n")
                time.sleep(15)
                out1 = tn.read_very_eager()
                out2 = out1.replace('sis 0 ', '')
                out3 = out2.replace(' = ', ',')
            
                end_position1=out3.find('\n', 0)
                mV_string=out3[0:end_position1]
            
                end_position2=out3.find('\n', end_position1+1)
                uA_string=out3[end_position1+1:end_position2]
                           
                end_position3=out3.find('\n', end_position2+1)
                tp_string=out3[end_position2+1:end_position3]
    
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
            
                mV_start  = mV_string.find(',',0)
                uA_start  = uA_string.find(',',0)
                tp_start  = tp_string.find(',',0)
                pot_start = pot_string.find(',',0)
                
                mV_sis_temp  = mV_string[mV_start+1:]
                uA_sis_temp  = uA_string[uA_start+1:]
                tp_sis_temp  = tp_string[tp_start+1:]
                pot_sis_temp = pot_string[pot_start+1:]
                
                if (mV_sis_temp == '' or uA_sis_temp == '' or tp_sis_temp == '' or pot_sis_temp == ''):
                    print "Had to wait extra time for the measurment to be returned again x3"
	            print out3
                    print "mV_sis_temp  = "  + mV_sis_temp
                    print "uA_sis_temp  = "  + uA_sis_temp
                    print "tp_sis_temp  = "  + tp_sis_temp
                    print "pot_sis_temp = "  + pot_sis_temp
                    print " "
                    tn.close()
                    time.sleep(5)
                    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                    time.sleep(5)
                    
                    tn.write("sweep 0 " + str(numpy.round(sispot)) + " " + str(numpy.round(sispot)) +  " 1  \n")
                    time.sleep(30)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('sis 0 ', '')
                    out3 = out2.replace(' = ', ',')
                
                    end_position1=out3.find('\n', 0)
                    mV_string=out3[0:end_position1]
                
                    end_position2=out3.find('\n', end_position1+1)
                    uA_string=out3[end_position1+1:end_position2]
                    
                               
                    end_position3=out3.find('\n', end_position2+1)
                    tp_string=out3[end_position2+1:end_position3]
        
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                
                    mV_start  = mV_string.find(',',0)
                    uA_start  = uA_string.find(',',0)
                    tp_start  = tp_string.find(',',0)
                    pot_start = pot_string.find(',',0)
                
                    mV_sis_temp  = mV_string[mV_start+1:]
                    uA_sis_temp  = uA_string[uA_start+1:]
                    tp_sis_temp  = tp_string[tp_start+1:]
                    pot_sis_temp = pot_string[pot_start+1:]
                    
                    if (mV_sis_temp == '' or uA_sis_temp == '' or tp_sis_temp == '' or pot_sis_temp == ''):
                        print "The script had to wait to long to read a value of mV and uA"
	                print "Killing the script"
	                print out3
                        print "mV_sis_temp  = " +  mV_sis_temp
                        print "uA_sis_temp  = "  + uA_sis_temp
                        print "tp_sis_temp  = "  + tp_sis_temp
                        print "pot_sis_temp = "  + pot_sis_temp
                        print " "
        	        sys.exit()
            
    mV_sis  = float(mV_string[mV_start+1:])
    uA_sis  = float(uA_string[uA_start+1:])
    tp_sis  = float(tp_string[tp_start+1:])
    pot_sis = int(pot_string[pot_start+1:])
    time.sleep(SleepPerMes)
    tn.close()
    return mV_sis, uA_sis, tp_sis, pot_sis


#mV_sis, uA_sis, tp_sis, pot_sis = setSIS_TP(65100, False, True, True)

################################
################################
################################

def setSIS_Volt(mV_user, verbose, careful, cheat_num):
    import sys
    import numpy
    import time
    from regrid import regrid
    from conv import conv
    from operator import itemgetter
    
    # this functon will not let the user exceed these values when setting the SIS bias
    mV_max =  7
    mV_min = -7
    
    loop_thresh      = 0.004 # in mV estimated voltage change to user destination, under this value the first loop is consider finished
    pot_diff_thresh   = 5     # estimated post postion to user destination, under this value first loop is consider finished
    loop_max         = 35   # number of loops allowed; when carful is set
    loop_hard_max    = 100  # number of loops allowed; always on
    
    SEM_user         = 0.100 # mV Standard error of the mean. Loop until we know the mean value of the voltage to this percison
    subloop_min      = 5    # the subloop will run at least this many times
    subloop_max      = 12     # number of loops allowed; when carful is set
    subloop_hard_max = 20    # number of loops allowed; always on
    
    SEM_user2      = 0.10 # mV Standard error of the mean. Loop until we know the mean value of the voltage to this persicion
    loop3_min      = 3    # the loop3 will run at least this many times
    loop3_max      = 12     # number of loops allowed; when carful is set
    loop3_hard_max = 20    # number of loops allowed; always on
    
    high_pot_pos_defult = 85000 
    low_pot_pos_defult  = 35000
        
    check_radius  = 5
    pot_per_check = 50
    bound_diff = 0.01 # in mV This is the diffence needed between the boundries valuses in the check loop and the minimum value found
    restart_count_max = 5 # Number of time the check part of the algorithm is allow to restart. if carful is on, the script will exit after this number
    show_plot = True
        
    min_cdf = 0.90 # fractoin of guassian computed
    sigma   = 40    # in pot positions
    
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
            print "Cheat_num not set proberly in setSIS_Volt, using defults for pot sweep"
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
        
    # Get data for a linear intepolation of the magpot to voltage relation
    
    # find 'high' qnd 'low' SIS voltage
    
    if low_pot_pos  == 62000:
        setSIS_only(low_pot_pos, True, verbose, careful) 
        mV_low, uA_low, pot_low = measSIS(verbose)
        time.sleep(0.5)
        setSIS_only(high_pot_pos, True, verbose, careful) 
        mV_high, uA_high, pot_high = measSIS(verbose)
    #elif high_pot_pos == 68000:
    else:
        setSIS_only(high_pot_pos, True, verbose, careful) 
        mV_high, uA_high, pot_high = measSIS(verbose)
        time.sleep(0.5)
        setSIS_only(low_pot_pos, True, verbose, careful) 
        mV_low, uA_low, pot_low = measSIS(verbose)
        
    
    
    # make fit a line to the min and max data points (find m,b in Y=mX+b)
    m = (high_pot_pos-low_pot_pos)/(mV_high-mV_low)
    b = low_pot_pos - m*mV_low
    
    # estimater  the final pot position from the max min line
    est_pot_pos=m*mV_user+b
    
    ### Start the Voltage ajustment algorithm 
    # reset to netrual position
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
            print "Killing the stript"
            sys.exit()
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
        else:
            if subloop:    
                new_position          = current_position*(1-loop_frac)+est_pot_pos*loop_frac
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
                        if verbose:
                            print "careful is off and the number of subloops has exceeded the maximum value."
                            print "The script will continue without having reached the user specifed SEM standard error of mean: "+str(SEM_user)
                    elif (careful and subloop_count >= subloop_max):
                        print "careful is on and the sub loop exceeded the allow number of loops: "+str(subloop_max)
                        print "the was not able to reached the user specifed SEM standard error of mean: "+str(SEM_user)
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
            
            # this makes the step size finer as we get closer to the user specified voltge (mV)
            
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
                            print "careful is off and the number of loops has exceeded the maximum value for loop3."
                            print "The script will continue without having reached the user specifed SEM standard error of mean: "+str(SEM_user2)
                    elif (careful and loop3_count >= loop3_max):
                        print "careful is on and the loop3 exceeded the allow number of loops: "+str(loop3_max)
                        print "the was not able to reached the user specifed SEM standard error of mean: "+str(SEM_user2)
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
                from matplotlib import pyplot as plt
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
                            print "function will be allowed to exit normaly using the best value it could find"
                else:
                    restart = True
                    
                if restart:
                    restart_count = restart_count +1
                    check_radius = check_radius + 1
                    if verbose:
                        print "The check part of setSIS_Volt need to be restarted the boundries of the checking function "
                        print str(mono_data[0,1]) + " mV is the minium differene vaule, and need to be " + str(bound_diff) + " mV"
                        print "above the bondries values of " + str(left_bound) + " and " + str(right_bound)
    return mV_sis, uA_sis, pot_sis


#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, True, 56666)



def setLOI(uA_user, verbose, careful, cheat_LO):
    import sys
    import time
    import numpy
    from LabJackU3_DAQ0 import LabJackU3_DAQ0
    
    uA_max = 40
    uA_min = 1
    
    sweep_radius = 0.1 # in Volts. the distance travel from the cheat_LO value to detirmine the slope near this value
    
    sleep_time = 1 # in seconds (time between measurments)
    
    
    # Options for the slope finding part of the script
    max_meas_per_loop = 12
    scan_count_max    = 20
    count_min         = 3
    
    # check to make sure the user input was within the range of values that can be achived
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
    
    do_meas_slope = True
    if ((5 >= cheat_LO) and (cheat_LO >= 0)):
        UCA_big = cheat_LO + sweep_radius
        if UCA_big >= 5:
            UCA_big = 5
        
        UCA_lit = cheat_LO - sweep_radius
        if UCA_lit <= 0:
            UCA_lit = 0
        
        # measure point need to find the slope near the cheat_LO point
        status = LabJackU3_DAQ0(UCA_big)
        if not status:
            print "LabJackU3_DAQ0 failed in setLOI"
            print "killing the script"
            sys.exit()
        mV_big, uA_big, pot_big = measSIS(verbose)
        time.sleep(sleep_time)
        status = LabJackU3_DAQ0(UCA_lit)
        if not status:
            print "LabJackU3_DAQ0 failed in setLOI"
            print "killing the script"
            sys.exit()
        mV_lit, uA_lit, pot_lit = measSIS(verbose)
        
        
        # is the user value actually between the measured value
        if ((uA_lit < uA_user) and (uA_user < uA_big)) :
            if verbose:
                print "The user value for uA was matched with cheat_LO"
                print "skipping the slope finding algorithm"
                do_meas_slope = False
        else:
            if verbose:
                print "The user value for uA was NOT matched with cheat_LO"
                print "Doing the slope finding algorithm, standby"
        
    else:
        print "cheat_LO is not set properly, it should be between '0' and '5' or '[]' "
        print "in the function setLOI"
        print "killing script"
        sys.exit()

    # here we do a simpy binary search to find the region wear the uA_user is near
    if do_meas_slope:
        
        Vfrac = float(1) # Votage range of search
        UCA_current = float(3.0) # first guess in sweep   
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
            UCA_prev = UCA_current
            uA_prev = uA_current 
            UCA_current = UCA_current + sign*Vfrac
            status = LabJackU3_DAQ0(UCA_current)
            time.sleep(sleep_time)
            if verbose:
                print str(scan_count) + " is the scan count"
                print str(UCA_current) + " is the UCA voltage"
                print str(uA_current) + " is the Current in uA"
                print str(Vfrac)    + "  is the voltage change (Vfrac)"
                
                
            # We measure enough times achieve the acuracy needed to make the next step.
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
                print str(count) + " is the measurment count"
                print str(SED)   + "  is the standard devietion of the mean"
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
                    print " Carful is on scan_count_max exceed, killing script"
                    sys.exit() 
        
        UCA_big = UCA_current 
        UCA_lit = UCA_prev
        uA_big = uA_current
        uA_lit = uA_prev 
            
    #############################################################################################        
    
    # calulate local slope
    #m = (uA_big-uA_lit)/(UCA_big-UCA_lit)
    #b = uA_big - m*UCA_big
    
    # estimater the final pot position from the local slope line
    UCA_val = UCA_current

    return mV_sis, uA_sis, pot_sis, UCA_val
# setSIS_Volt   
#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, False, 56666)
# setLOI
#mV_sis, uA_sis, pot_sis, UCA_val = setLOI(10, True, True, 3.45751953125)
# setSIS_Volt   
#mV_sis, uA_sis, pot_sis = setSIS_Volt(1.8, True, True, [])
  
    