def measmag(verbose):
    import telnetlib
    import time
    import sys 
    
    SleepPerMes = 0.5 # in seconds 
    
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    V_mag   = -999999
    mA_mag  = -999999
    pot_mag = -999999
        
    tn.write("setbias 9 \n")
    time.sleep(SleepPerMes)
    out1 = tn.read_very_eager()
    out2 = out1.replace('mag 1 ', '')
    out3 = out2.replace(' = ', ',')
    
    end_position1=out3.find('\n', 0)
    V_string=out3[0:end_position1]
    
    end_position2=out3.find('\n', end_position1+1)
    mA_string=out3[end_position1+1:end_position2]
    
    end_position3=out3.find('\n', end_position2+1)
    f_string=out3[end_position2+1:end_position3]
    
    end_position4=out3.find('\n', end_position3+1)
    pot_string=out3[end_position3+1:end_position4]
    
    V_start   = V_string.find(',',0)
    mA_start  = mA_string.find(',',0)
    pot_start = pot_string.find(',',0) 
    
    V_mag_temp   = V_string[V_start+1:]
    mA_mag_temp  = mA_string[mA_start+1:]
    pot_mag_temp = pot_string[pot_start+1:]
                
    if (V_mag_temp == '' or mA_mag_temp == '' or f_string == '' or pot_mag_temp == ''):
        if verbose:
            print "Had to wait extra time for the measurment to be returned"
        tn.write("setbias 9 \n")
        time.sleep(1)
        out1 = tn.read_very_eager()
        out2 = out1.replace('mag 1 ', '')
        out3 = out2.replace(' = ', ',')
        
        end_position1=out3.find('\n', 0)
        V_string=out3[0:end_position1]
    
        end_position2=out3.find('\n', end_position1+1)
        mA_string=out3[end_position1+1:end_position2]
        
                    
        end_position3=out3.find('\n', end_position2+1)
        f_string=out3[end_position2+1:end_position3]
    
        end_position4=out3.find('\n', end_position3+1)
        pot_string=out3[end_position3+1:end_position4]
    
        V_start   = V_string.find(',',0)
        mA_start  = mA_string.find(',',0)
        pot_start = pot_string.find(',',0) 
        
        V_mag_temp   = V_string[V_start+1:]
        mA_mag_temp  = mA_string[mA_start+1:]
        pot_mag_temp = pot_string[pot_start+1:]
                
        if (V_mag_temp == '' or mA_mag_temp == '' or f_string == '' or pot_mag_temp == ''):
            if verbose:
                print "Had to wait extra time for the measurment to be returned again"
            tn.write("setbias 9 \n")
            time.sleep(5)
            out1 = tn.read_very_eager()
            out2 = out1.replace('mag 1 ', '')
            out3 = out2.replace(' = ', ',')
        
            end_position1=out3.find('\n', 0)
            V_string=out3[0:end_position1]
        
            end_position2=out3.find('\n', end_position1+1)
            mA_string=out3[end_position1+1:end_position2]
                       
            end_position3=out3.find('\n', end_position2+1)
            f_string=out3[end_position2+1:end_position3]
    
            end_position4=out3.find('\n', end_position3+1)
            pot_string=out3[end_position3+1:end_position4]
        
            V_start   = V_string.find(',',0)
            mA_start  = mA_string.find(',',0)
            pot_start = pot_string.find(',',0) 
        
            V_mag_temp   = V_string[V_start+1:]
            mA_mag_temp  = mA_string[mA_start+1:]
            pot_mag_temp = pot_string[pot_start+1:]
                
            if (V_mag_temp == '' or mA_mag_temp == '' or f_string == '' or pot_mag_temp == ''):
                if verbose:
                    print "Had to wait extra time for the measurment to be returned again x2"
                    print out3
                    print "V_mag_temp  ="+V_mag_temp
                    print "mA_mag_temp ="+mA_mag_temp
                    print "t_string    ="+f_string
                    print "pot_string  ="+pot_string
                    print " "
                tn.close()
                time.sleep(5)
                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                time.sleep(5)
                tn.write("setbias 9 \n")
                time.sleep(15)
                out1 = tn.read_very_eager()
                out2 = out1.replace('mag 1 ', '')
                out3 = out2.replace(' = ', ',')
            
                end_position1=out3.find('\n', 0)
                V_string=out3[0:end_position1]
            
                end_position2=out3.find('\n', end_position1+1)
                mA_string=out3[end_position1+1:end_position2]
                           
                end_position3=out3.find('\n', end_position2+1)
                f_string=out3[end_position2+1:end_position3]
    
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
            
                V_start   = V_string.find(',',0)
                mA_start  = mA_string.find(',',0)
                pot_start = pot_string.find(',',0) 
            
                V_mag_temp   = V_string[V_start+1:]
                mA_mag_temp  = mA_string[mA_start+1:]
                pot_mag_temp = pot_string[pot_start+1:]
            
                if (V_mag_temp == '' or mA_mag_temp == '' or f_string == '' or pot_mag_temp == ''):
                    if verbose:
                        print "Had to wait extra time for the measurment to be returned again x3"
                        print out3
                        print "V_mag_temp  ="+V_mag_temp
                        print "mA_mag_temp ="+mA_mag_temp
                        print "t_string    ="+f_string
                        print "pot_string  ="+pot_mag_temp
                        print " "
                    tn.close()
                    time.sleep(5)
                    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                    time.sleep(5)
                    
                    tn.write("setbias 9 \n")
                    time.sleep(30)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('mag 1 ', '')
                    out3 = out2.replace(' = ', ',')
                
                    end_position1=out3.find('\n', 0)
                    V_string=out3[0:end_position1]
                
                    end_position2=out3.find('\n', end_position1+1)
                    mA_string=out3[end_position1+1:end_position2]
                    
                               
                    end_position3=out3.find('\n', end_position2+1)
                    f_string=out3[end_position2+1:end_position3]
        
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                
                    V_start   = V_string.find(',',0)
                    mA_start  = mA_string.find(',',0)
                    pot_start = pot_string.find(',',0) 
                
                    V_mag_temp   = V_string[V_start+1:]
                    mA_mag_temp  = mA_string[mA_start+1:]
                    pot_mag_temp = pot_string[pot_start+1:]
                
                    if (V_mag_temp == '' or mA_mag_temp == '' or f_string == '' or pot_mag_temp == ''):
                        print "The script had to wait to long to read a value of mV and uA"
	                print "Killing the script"
	                print out3
                        print "V_mag_temp  ="+V_mag_temp
                        print "mA_mag_temp ="+mA_mag_temp
                        print "t_string    ="+f_string
                        print "pot_string  ="+pot_mag_temp
                        print " "
        	        sys.exit()
            
    V_mag=float(V_string[V_start+1:])
    mA_mag=float(mA_string[mA_start+1:])
    pot_mag=int(pot_string[pot_start+1:])
    time.sleep(SleepPerMes)
    tn.close()
    return V_mag, mA_mag, pot_mag
    
    
def setmag(magpot, verbose):
    import telnetlib
    import time
    import numpy
    import sys

    SleepPerMes = 0.5 # in seconds 
    
    mA_mag  = -999998
    V_mag   = -999998
    pot_mag = -999998 
    
    if (magpot < 0 or magpot > 129797):
        print "magpot value was not in the set [0,129797], try agian"
        print "magpot = " + str(magpot)
        print "exiting the script"
        sys.exit()
    else:
        #set the pot position of the magnet and recound the current and volage
        tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)    
        tn.write("setbias 9 "+str(numpy.round(magpot)) + " \n")
        time.sleep(SleepPerMes)     
        tn.close()
        
        V_mag, mA_mag, pot_mag = measmag(verbose)
    return V_mag, mA_mag, pot_mag
               
def setmag_only(magpot):
    import telnetlib
    import time
    import numpy
    import sys

    SleepPerMes = 0.5 # in seconds 
    
    if (magpot < 0 or magpot > 129797):
        print "magpot value was not in the set [0,129797], try agian"
        print "magpot = " + str(magpot)
        print "exiting the script"
        sys.exit()
    else:
        #set the pot position of the magnet and recound the current and volage
        tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)    
        tn.write("setbias 9 "+str(numpy.round(magpot)) + " \n")
        time.sleep(SleepPerMes)     
        tn.close()
    return
    
################################
################################
################################    
    

def setmagI(mA_user, verbose, careful):
    import sys
    import numpy
    
    status = True
    
    max_pot_pos = 129797 # found by testing values by hand 
    min_pot_pos = 0
    
    high_pot_pos = 120000 # things can get funky around the rail positions
    low_pot_pos = 10000
    
    loop1_thresh      = 0.005 # in mA estimated current change to user destination, under this value the algorithm is consider finished
    pot_diff_thresh   = 8     # estimated post postion to user destination, under this value the algorithm is consider finished
    # old #loop1_frac        = 0.35 # distance traveled from current position to estimated pot position
    loop1_max         = 35   # number of loops allowed; when carful is set
    loop1_restar_max  = 10 # number of loops restarts for over shots allowed;, always on
    
    subloop_max = 20
    subloop_min = 5
    
    # find max magnet current  
    V_max, mA_max, pot_max = setmag(max_pot_pos, verbose)
    
    # find min magnet current
    V_min, mA_min, pot_min = setmag(min_pot_pos, verbose)
    
    # Error checking: mag currnet should be mA_min<-40 and mA_max >40.
    if (mA_min >= -40 or mA_max <= 40):
        status = False
        if (verbose or careful):
            print "The rail magnet votages were different then expected value mA_min<-40 or mA_max >40"
            print "mA_min = "+str(mA_min)+ "  V_min = "+ str(V_min)
            print "mA_max = "+str(mA_max)+ "  V_min = "+ str(V_max)
        if careful:
            print "careful is set to True, killing script now"
            V_65100, mA_65100 = setmag(65100, verbose)
            sys.exit()
            
    # Get data for a linear intepolation of the magpot to current relation
    
    # find max magnet current  
    V_high, mA_high, pot_high = setmag(high_pot_pos, verbose)
    
    # find min magnet current
    V_low, mA_low, pot_high = setmag(low_pot_pos, verbose)
    
    # make fit a line to the min and max data points (find m,b in Y=mX+b)
    m = (high_pot_pos-low_pot_pos)/(mA_high-mA_low)
    b = low_pot_pos - m*mA_low
    
    # estimater  the final pot position from the max min line
    est_pot_pos=m*mA_user+b
    
    # We set the magnet to its rail and come down to the desired current,
    # here we determin which rail (+ or -) to set the magnet pot position
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
    V_rail, mA_rail, pot_rail = setmag(rail_pos, verbose)
    
    ######################
    ####### Loop 1 #######
    ######################
    # Now we step the magnet position toward the estimated pot position.
    # Each step brings the pot position part way between its current position
    # and the estimated position, secifed by loop1_frac. This happens until the 
    # difference between mA_user and mA_meas becomes less than some threshold 
    # value.
    
    #mA_user = mA_user - multiplier*0.5*loop1_thresh # so the algoritim mean return is the origanal mA_user value, loop1_thresh is the accepted error
    
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
        print "The use specifed magnet current is grater than the rail value"
        print "mA_rail = " + str(mA_rail)
        print "mA_user = " + str(mA_user)
        print "killing the script"
        sys.exit()
    else:    
        while not finished:
            if ebrake:
                print "Loop one restarted more than " + str(loop1_restar_max) + " times"
                print "Killing the stript"
                sys.exit()
            elif ((diff < 0) and (not abs(pot_diff) < pot_diff_thresh)):
                if verbose:
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
            elif ((abs(diff) <= loop1_thresh) or (abs(pot_diff) < pot_diff_thresh)):
                if verbose:
                    print "Loop1 of magnet current finding algorithm completed after "
                    print str(loop1_count) + " loops and"
                    print str(loop1_restar) + " loop restarts"
                finished = True

            else:
                new_position          = current_position*(1-loop1_frac)+est_pot_pos*loop1_frac
                setmag_only(new_position)
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
                if pot_diff <= 30:
                    loop1_frac = 0.3
                    subloop = True
                    subloop_min = 10
                elif pot_diff <= 100:
                    loop1_frac = 0.4
                    subloop = True
                    subloop_min = 5
                elif 1 <= loop1_restar:
                    loop1_frac = 0.4
                    subloop = False
                    subloop_min = 5   
                elif pot_diff <= 500:
                    loop1_frac = 0.6
                    subloop = False
                    subloop_min = 5
                else:
                    loop1_frac = 0.9
                    subloop = False
                    subloop_min = 5
                
                
                if verbose:
                    print str(loop1_count) + " = loop1_cout is "
                    print str(loop1_restar) + " = loop1_restar"
                    print str(mA_current) + " = mA_current"
                    print str(mA_user) + " = mA_user"
                    print str(diff) + " = diff"
                    print str(pot_diff) + " diff in terms of pot values"
                    print " "
                    print " "
                if (careful and loop1_count >= loop1_max):
                    print "careful is true and the loop count of the first loop exceeded"
                    print "the maximum allow value of "+str(loop1_max)
                    print "killing the script"
                    sys.exit()
    V_mag   = V_current
    mA_mag  = mA_current
    pot_mag = pot_current
    return status, V_mag, mA_mag, pot_mag
    
status, V_mag, mA_mag, pot_mag = setmagI(40, True, True)