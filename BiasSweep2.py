def MakeSetDirs(datadir):
    # does the datadir exist? If not, we will make it!
    import os
    from sys import platform
    if platform == 'win32':
        if not os.path.isdir(datadir):
            os.makedirs(datadir)
        if not os.path.isdir(datadir+'rawdata/'):
            os.makedirs(datadir+'rawdata/')
    elif platform == 'darwin':
        if not os.path.isdir(datadir):
            os.makedirs(datadir)
        if not os.path.isdir(datadir+'rawdata\\'):
            os.makedirs(datadir+'rawdata\\')
    #LOrefdir = datadir + "rawdata/LOpowerSettings/"
    #if not os.path.isdir(LOrefdir):
    #    os.makedirs(LOrefdir)
    return

def makeLists(start, stop, step):
    from numpy import arange
    step = abs(step)
    newlist = []
    if start < stop:
        if (isinstance(start, int) and isinstance(stop, int) and isinstance(step, int)):
            newlist = range(start, stop, step)
        else:
            newlist = arange(start, stop, step)
    elif stop < start:
        step = step*-1
        if (isinstance(start, int) and isinstance(stop, int) and isinstance(step, int)):
            newlist = range(start, stop, step)
        else:
            newlist = arange(start, stop, step)
    elif start == stop:
        newlist = [start]
    return newlist
    
def orderLists(master_list_input):
    import sys
    axis_list = []
    unordered_lists = []
    num_of_lists = len(master_list_input)
    for n in range(num_of_lists):
        temp_tuple = master_list_input[n]
        axis_num = temp_tuple[0]
        single_list = temp_tuple[1]
        if isinstance(axis_num, int):
            axis_list.append(axis_num)
        else:
            print "The function orderLists needs a list of tuples \
            with each tuple containing (int, list). Something other than an int \
            was found: ", axis_num
            sys.exit()
        if isinstance(single_list, list):
            unordered_lists.append(single_list)
        else:
            print "The function orderLists needs a list of tuples \
            with each tuple containing (int, list). Something other than a list \
            was found: ", single_list
            sys.exit()
    
    for n in range(num_of_lists):
        axis_num_count = axis_list.count(n)
        if axis_num_count == 1:
            None
        elif axis_num_count < 1:
            print "In the function oderLists the axis: ", n, " is not listed."
            print " Axis_nums should start with 0 and increment by one with each \
            axis having a unique number"
            print "see axis_list:", axis_list
            sys.exit()
        elif 1 < axis_num_count:
            print "In the function oderLists the axis: ", n, " appears ", \
            axis_num_count, " times, it should be unique."
            print " Axis_nums should start with 0 and increment by one with each \
            axis having a unique number"
            print "see axis_list:", axis_list
            sys.exit()
    
    ordered_lists = []
    for n in range(num_of_lists):
        index = axis_list.index(n)
        ordered_lists.append(unordered_lists[index])

    return ordered_lists

def makeparamslist_Rec(lists):
    master_lists = []
    listn = lists[0]
    listn_len = len(listn)
    for list_index in range(1, len(lists)):
        listnplusone = lists[list_index]
        listnplusone_len = len(listnplusone)
        if list_index == 1:
            master_lists.append(listn*listnplusone_len)
            new_listnplusone = []
            for i in range(listnplusone_len):
                temp_list = []
                temp_list.append(listnplusone[i])
                temp_list = temp_list*listn_len
                new_listnplusone.extend(temp_list)
            master_lists.append(new_listnplusone)
        else:
            listn_len = len(master_lists[0])
            for masters_index in range(len(master_lists)):
                master_lists[masters_index] = master_lists[masters_index]*listnplusone_len
            new_listnplusone = []
            for i in range(listnplusone_len):
                temp_list = []
                temp_list.append(listnplusone[i])
                temp_list = temp_list*listn_len
                new_listnplusone.extend(temp_list)
            master_lists.append(new_listnplusone)
    return master_lists
    
def fbmsg(feedback):
    print "Feedback has been set to: " + str(feedback)
    return

def Kmsg(Kval):
    print "The chopper should be set for " + str(Kval) + "K"
    return

def magmsg(magpot):
    print "The magnet pot has ben set to: " + str(magpot)
    return

def sismsg(sisPot):
    print "The SIS bias pot has ben set to: " + str(sisPot)
    return

def LOuAmsg(LOuA):
    print "The LO current has been set to " + str('%2.3f' % LOuA) + "uA"
    return

def UCAmsg(UCA):
    print "The UCA Voltage has been set to " + str('%1.4f' % UCA) + "V"
    return

def LOfreqmsg(freq):
    print "The LO frequency has be set to " + str("%3.3f" % freq) + "GHz"
    return

def IFmsg(IFband):
    print "The IF band width has been set to " + str("%1.4f" % IFband) + "GHz"
    return

def BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, careful=False,
              sweepNstart=0, Ynum=0, testmode=False,
              do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=True, high_res_meas=5,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
              getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
              spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30, spec_attenu=0,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=1,
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              do_magisweep=True, mag_meas=10, magisweep_start=32, magisweep_stop=32, magisweep_step=1,
              magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
              do_LOuAsearch=True, UCA_meas=10,
              LOuAsearch_start=12, LOuAsearch_stop=12, LOuAsearch_step=1,
              LOuA_magpot=103323, LOuA_set_pot=56800, LOuA_cheat_num=56666,
              UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
              sweepShape="rectangular",
              FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
              seconds_per_email=1200, chopper_off=False, do_LOuApresearch=True):
    import time
    import numpy
    import sys
    from sys import platform
    import os
    from control import LabJackU3_DAQ0, LJ_streamTP, measmag, setmagI,       \
    setmag_only, setmag_highlow, setfeedback, measSIS, setSIS_only, setSIS_Volt,   \
    setLOI, setSIS_TP, measSIS_TP, zeropots
    from LOinput import RFon, RFoff, setfreq
    if ((not testmode) and (not chopper_off)):
        from StepperControl import initialize, GoForth, GoBack, DisableDrive
    from email_sender   import email_caleb
    from fastSISsweep   import getfastSISsweep
    from getspec import getspecPlusTP

    # initialize some variables
    K_actual   = None
    K_thisloop = None
    sisPot_actual   = None
    sisPot_thisloop = None
    magpot_actual   = None
    magpot_thisloop = None
    UCA_actual   = None
    UCA_thisloop = None
    LOuA_actual   = None
    LOuA_thisloop = None
    LOfreq_actual   = None
    LOfreq_thisloop = None
    IFband_actual   = None
    Ifband_thisloop = None
    feedback_actual = None
    sisuA_actual = None
    sismV_actual = None
    magV_actual  = None
    magmA_actual = None
    EmailTrigger = False
    sweepN = sweepNstart

    ##########################
    ###### START SCRIPT ######
    ##########################
    #### does the datadir exist? If not, we will make it!
    MakeSetDirs(datadir)
    if platform == 'win32':
        rawdir = datadir + "rawdata\\"
    elif platform == 'darwin':
        rawdir = datadir + "rawdata/"
    
    #### make the parameter lists from user specified parameters
    # SIS bias
    # set feedback for the script here
    if testmode:
        do_sisVsweep = False
        do_magisweep = False
        do_LOuAsearch = False
    else:
        status = setfeedback(sisV_feedback)
        feedback_actual = sisV_feedback
        if verboseSet:
            fbmsg(feedback_actual)

    if do_sisVsweep:
        if verboseTop:
            print "Finding SIS pot positions for each magnet Voltage in 'sisV_list'."
        sisV_list = makeLists(sisVsweep_start, sisVsweep_stop, sisVsweep_step)
        sisPot_list = []
        cheat_num_temp = 65100 # center position of the SIS pot
        for sisV in sisV_list:
            if verboseTop:
                print "Finding the potentiometer position for the sis bias voltage of " + str('%1.3f' % sisV) + 'mV'
            sismV_actual, sisuA_actual, sisPot_actual = setSIS_Volt(sisV, verbose, careful, cheat_num_temp)
            sisPot_list.append(sisPot_actual)
            if verboseSet:
                sismsg(sisPot_actual)
            cheat_num_temp = sisPot_actual
    else:
        sisV_list = None
        if sisV_feedback:
            sisPot_list = makeLists(sisPot_feedTrue_start, sisPot_feedTrue_stop, sisPot_feedTrue_step)
        elif sisV_feedback == False:
            sisPot_list = makeLists(sisPot_feedFalse_start, sisPot_feedFalse_stop, sisPot_feedFalse_step)
    # round the sisPot list to integers, this is needed comparisons to triggers later on in the script
    for Pot_index in range(len(sisPot_list)):
        sisPot_list[Pot_index] = int(round(sisPot_list[Pot_index]))
            
    # Electromagnet 
    if do_magisweep:
        if verboseTop:
            print "Finding Elctromagnet pot positions for each magnet current \
            in 'magi_list'."
        magi_list = makeLists(magisweep_start, magisweep_stop, magisweep_step)
        magpot_list = []
        if do_LOuApresearch:
            for magi in magi_list:
                magV_actual, magmA_actual, magpot_actual = setmagI(magi, verbose, careful)
                magpot_list.append(magpot_actual)
                if verboseSet:
                    magmsg(magpot_actual)
            magpot_list.sort
            if magpot_list[-1] < magpot_list[0]:
                magpot_list.reverse()

    else:
        magi_list = None
        magpot_list = makeLists(magpotsweep_start, magpotsweep_stop, magpotsweep_step)

    # LO Frequency
    LOfreq_list = makeLists(LOfreq_start, LOfreq_stop, LOfreq_step)
    # this a catch for if the value of presearch needed to be changed
    # presearch is not an effective tool if both the LO frequency and LO power are being changed in single run
    if ((1 < len(LOfreq_list)) and do_LOuApresearch):
        do_LOuApresearch = False
        print "do_LOuApresearch was changes to be False since the list of frequencies for this data run is greater than 1"

    # LO power
    if (do_LOuAsearch and do_LOuApresearch):
        if verboseTop:
            print "Finding SIS pot positions for each SIS current in 'LOuA_list'."
            print "This option is found when do_LOuAsearch and do_LOuApresearch are both True."
            print "This list is discarded if both LO power (LOuA) and LO frequency are both changing in a single run"
        LOuA_list = makeLists(LOuAsearch_start, LOuAsearch_stop, LOuAsearch_step)

        setmag_highlow(LOuA_magpot) # set the Electromagnet to a known position
        magpot_actual = LOuA_magpot
        if verboseSet:
            magmsg(magpot_actual)

        setSIS_only(LOuA_set_pot, sisV_feedback, verbose, careful) # set the SIS bias to a known position
        sisPot_actual = LOuA_set_pot
        if verboseSet:
            sismsg(sisPot_actual)

        UCA_list = []
        for LOuA in LOuA_list:
            sismV_actual, sisuA_actual, sisPot_actual, UCA_actual = setLOI(LOuA, verbose, careful)
            UCA_list.append(UCA_actual)
            if verboseTop:
                print "UCA = " + str(UCA_actual) + " V  for LOuA = " + str(LOuA) + " uA"
            elif verboseSet:
                LOuAmsg(LOuA)
                UCAmsg(UCA_actual)

    elif (do_LOuAsearch and (do_LOuApresearch == False)):
        LOuA_list = makeLists(LOuAsearch_start, LOuAsearch_stop, LOuAsearch_step)
        UCA_list  = None
    else:
        LOuA_list = None
        UCA_list  = makeLists(UCAsweep_min, UCAsweep_max, UCAsweep_step)

    if ((1 < len(LOfreq_list)) and (do_LOuAsearch == False) and (1 < len(UCA_list))):
        print "It is not recommended to step LO frequency and UCA voltage with in the same run."
        print "LO power can change as a function of frequency"
        raw_input("Press Enter to continue, you have been warned")

    # IF bandwidth Center
    IFband_list = makeLists(IFband_start, IFband_stop, IFband_step)
    
    # fast and unpumped sweep settings
    if fastsweep_feedback:
        fSweepStart = SweepStart_feedTrue
        fSweepStop  = SweepStop_feedTrue
        fSweepStep  = SweepStep_feedTrue
    elif not fastsweep_feedback:
        fSweepStart = SweepStart_feedFalse
        fSweepStop  = SweepStop_feedFalse
        fSweepStep  = SweepStep_feedFalse
    else:
        print "fastsweep_feedback is not set to 'True' or 'False', check BiasSweep_config.py search for " \
              "do_unpumpedsweep and try again"
        print "killing the script"
        sys.exit()
    
    #########################################################################################################
    ####### From each unique list of parameters, make the master list of every parameter set to be run ######
    #########################################################################################################
    doing_UCA_list = (do_LOuApresearch or (do_LOuAsearch == False))
    master_list_input = []
    master_list_input.append((Kaxis,K_list))
    master_list_input.append((sisVaxis,sisPot_list))
    master_list_input.append((magaxis,magpot_list))
    if doing_UCA_list:
        master_list_input.append((LOpowaxis,UCA_list))
    else:
        master_list_input.append((LOpowaxis,LOuA_list))
    master_list_input.append((LOfreqaxis,LOfreq_list))
    master_list_input.append((IFbandaxis,IFband_list))
    if verboseTop:
        print (Kaxis,K_list), " K axis list"
        print (sisVaxis,sisPot_list), " SIS Voltage axis list"
        print (magaxis,magpot_list), " Electromagnet axis list"
        if doing_UCA_list:
            print (LOpowaxis,UCA_list), " LO power (UCA) axis list"
        else:
            print (LOpowaxis,LOuA_list), " LO power (LOuA) axis list, to be set with each change in frequency or LO power"
        print (LOfreqaxis,LOfreq_list), " LO frequency axis list"
        print (IFbandaxis,IFband_list), " IF band axis list"

    ordered_lists = orderLists(master_list_input)

    if sweepShape == "rectangular":
        master_list = makeparamslist_Rec(ordered_lists)
    
    ####################################################################
    ###### Initialize variables and list for the Control Sequence ######
    ####################################################################
    
    ### Determine if we need to run the chopper and how the output datafiles will be named
    # if 300 K and 77 K measurements are being made, give files a Y number to make them easy to find as pairs
    if ( (min(K_list) < 90) and (250 < max(K_list)) ):
        do_Ynum = True
        if ((not testmode) and (not chopper_off)):
            initialize() # To start the chopper
        # this triggers the Y factor folder to be created
        Y_trigger = K_list[0]
        K_actual  = K_list[0]
    else:
        do_Ynum = False
    
    # unpack the sorted lists of parameters
    master_K_list      = master_list[Kaxis]
    master_sisPot_list = master_list[sisVaxis]
    master_magpot_list = master_list[magaxis]
    if doing_UCA_list:
        master_UCA_list = master_list[LOpowaxis]
    else:
        master_LOuA_list = master_list[LOpowaxis]
    master_LOfreq_list = master_list[LOfreqaxis]
    master_IFband_list = master_list[IFbandaxis]
    
    # make sure all the lists are the same length
    Truth_list = []
    Truth_list.append(len(master_K_list     ) == len(master_sisPot_list))
    Truth_list.append(len(master_sisPot_list) == len(master_magpot_list))
    if doing_UCA_list:
        Truth_list.append(len(master_magpot_list) == len(master_UCA_list   ))
        Truth_list.append(len(master_UCA_list   ) == len(master_LOfreq_list))
    else:
        Truth_list.append(len(master_magpot_list) == len(master_LOuA_list   ))
        Truth_list.append(len(master_LOuA_list   ) == len(master_LOfreq_list))
    Truth_list.append(len(master_LOfreq_list) == len(master_IFband_list))
    if all(Truth_list):
        list_len = len(master_K_list)
        if verboseTop:
            print "List lengths are verified, starting control sequence"
            raw_input("Press Enter to Continue")
    else:
        print "list lengths in the function BiasSweep are not the same. " \
              "Search for 'Truth_list' in the code to find the source of this error."
        sys.exit()

    ######################################    
    ######################################
    ####### START CONTROL SEQUENCE #######
    ######################################
    ######################################
    if not testmode:
        # make sure the LO input from the signal generator is turned 'on' and and is set to a safe frequency
        safe_freq = 672 # GHz
        setfreq(safe_freq) # a safe frequency
        LOfreq_actual = safe_freq
        RFon()
    # a trigger for certain parameters thatI only collected once a sweep
    sisVsweep_trigger = master_sisPot_list[0]
    first_loop = True
    for param_index in range(list_len):
    ###########################
    ##### Set parameters ######
    ###########################     
        # unpack the values from the parameter lists
        K_thisloop      = master_K_list[param_index]
        sisPot_thisloop = master_sisPot_list[param_index]
        magpot_thisloop = master_magpot_list[param_index]
        if doing_UCA_list:
            UCA_thisloop    = master_UCA_list[param_index]
        else:
            LOuA_thisloop   = master_LOuA_list[param_index]
        LOfreq_thisloop = master_LOfreq_list[param_index]
        IFband_thisloop = master_IFband_list[param_index]
        
        if verboseTop:
            print "K_thisloop      = ", K_thisloop
            print "sisPot_thisloop = ", sisPot_thisloop
            print "magpot_thisloop = ", magpot_thisloop
            if doing_UCA_list:
                print "UCA_thisloop    = ", UCA_thisloop
            else:
                print "LOuA_thisloop   = ", LOuA_thisloop
            print "LOfreq_thisloop = ", LOfreq_thisloop
            print "IFband_thisloop = ", IFband_thisloop
        
        # Move the chopper K_list (if needed)
        if not (K_thisloop == K_actual):
            if do_Ynum:
                if ((not testmode) and (not first_loop)):
                    if  K_actual <= 150:
                        GoForth()
                    elif 150 < K_actual:
                        GoBack()
                    K_actual = K_thisloop
                    if (verboseTop):
                        print K_actual, "K: The command to move the chopper has been sent"
                    elif verboseSet:
                        Kmsg(K_actual)
                else:
                    print "testmode on, pretending to move the chopper"
        first_loop = False
        # Set UCA Voltage for the LO (if needed)
        if doing_UCA_list: # UCA values are set
            if not (UCA_thisloop == UCA_actual):
                if not testmode:
                    status = LabJackU3_DAQ0(UCA_thisloop)
                    UCA_actual = UCA_thisloop
                    if verboseSet:
                        UCAmsg(UCA_actual)
                else:
                    print "testmode on, pretending to set the UCA voltage"
                if verboseTop:
                    print "UCA voltage set to ", UCA_thisloop
        else:
            if not (LOuA_thisloop == LOuA_actual):
                # if this if statement is true that the LO power will get set at the Set LO frequency below
                if LOfreq_thisloop == LOfreq_actual:
                    if not testmode:    
                        setmag_highlow(LOuA_magpot) # set the Emagnet to a known position
                        magpot_actual = LOuA_magpot
                        if verboseSet:
                            magmsg(magpot_actual)

                        setSIS_only(LOuA_set_pot, sisV_feedback, verbose, careful)
                        sisPot_actual = LOuA_set_pot
                        if verboseSet:
                            sismsg(sisPot_actual)

                        sismV_actual, sisuA_actual, sisPot_actual, UCA_thisloop = setLOI(LOuA_thisloop, verbose, careful)
                        UCA_actual  = UCA_thisloop
                        LOuA_actual = LOuA_thisloop
                        if verboseSet:
                            UCAmsg(UCA_actual)
                            LOuAmsg(LOuA_actual)

                        if verboseTop:
                            print "Using the LO power setting algorithm 'setLOI' the LO power has been set."
                            print "LO uA set value:" + str('%2.4f' % LOuA_thisloop) + "uA  LO actual value:" + str('%2.4f' % sisuA_actual) + "uA"
                            print "at " + str('%2.4f' % sismV_actual) + "mV and a pot of " + str(sisPot_actual)
                            print "The user controlled attenuation is now set to " + str(UCA_actual) + "."
                            print "Resetting the sis bias and magnet potentiometers."

                        setmag_highlow(magpot_thisloop)
                        magpot_actual = magpot_thisloop
                        if verboseSet:
                            magmsg(magpot_actual)

                        setSIS_only(sisPot_thisloop, sisV_feedback, verbose, careful)
                        sisPot_actual = sisPot_thisloop
                        if verboseSet:
                            sismsg(sisPot_actual)

        # Set the LO frequency (if needed)
        if not (LOfreq_thisloop == LOfreq_actual):
            if not testmode:
                setfreq(LOfreq_thisloop)
                LOfreq_actual = LOfreq_thisloop
                if verboseSet:
                    LOfreqmsg(LOfreq_actual)

                if verboseTop:
                    "Setting to LO frequency to " + str('%3.3f' % LOfreq_actual) + " GHz"

                if not doing_UCA_list:
                    setmag_highlow(LOuA_magpot) # set the Electromagnet to a known position
                    magpot_actual = LOuA_magpot
                    if verboseSet:
                        magmsg(magpot_actual)

                    setSIS_only(LOuA_set_pot, sisV_feedback, verbose, careful)
                    sisPot_actual = LOuA_set_pot
                    if verboseSet:
                        sismsg(sisPot_actual)

                    sismV_actual, sisuA_actual, sisPot_actual, UCA_thisloop = setLOI(LOuA_thisloop, verbose, careful)
                    LOuA_actual = LOuA_thisloop
                    UCA_actual = UCA_thisloop
                    if verboseTop:
                        print "Using the LO power setting algorithm 'setLOI' the LO power has been set."
                        print "LO uA set value:" + str('%2.4f' % LOuA_thisloop) + "uA  LO actual value:" + str('%2.4f' % sisuA_actual) + "uA"
                        print "at " + str('%2.4f' % sismV_actual) + "mV and a pot of " + str(sisPot_actual)
                        print "The user controlled attenuation is now set to " + str(UCA_actual) + "."
                        print "Resetting the sis bias and magnet potentiometers."
                    elif verboseSet:
                        LOuAmsg(LOuA_actual)
                        UCAmsg(UCA_actual)

                    setmag_highlow(magpot_thisloop)
                    magpot_actual = magpot_thisloop
                    if verboseSet:
                        magmsg(magpot_actual)

                    setSIS_only(sisPot_thisloop, sisV_feedback, verbose, careful)
                    sisPot_actual = sisPot_thisloop
                    if verboseSet:
                        sismsg(sisPot_actual)

            else:
                print "Testmode is on, pretending to set frequency to ", LOfreq_thisloop
        
        # Set the SIS bias voltage by setting the pot position (if needed)
        if not (sisPot_thisloop == sisPot_actual):
            if not testmode:
                setSIS_only(sisPot_thisloop, sisV_feedback, verbose, careful)
                sisPot_actual = sisPot_thisloop
                if (verboseTop):
                    print "SIS bias potentiometer position set to ", sisPot_thisloop
                elif verboseSet:
                    sismsg(sisPot_actual)
            else:
                print 'testmode on, pretending to set the SIS pot'

        # Set magnet (if needed)
        if not (magpot_thisloop == magpot_actual):
            if not testmode:
                setmag_highlow(magpot_thisloop)
                magpot_actual = magpot_thisloop
                if (verboseTop):
                    print "Magnet potentiometer position set to ", magpot_thisloop
                elif verboseSet:
                    magmsg(magpot_actual)
            else:
                print 'testmode on, pretending to set the E-magnet pot'

        #### Not currently set to do anything
        # Set IFband (if needed)
        if not IFband_thisloop == IFband_actual:
            IFband_actual = IFband_thisloop
        
        # all parameters are now set
        
        ###################################
        ###### Write new directories ######
        ###################################
        # we only need to save certain data or make new folders once per SIS voltage sweep
        if verboseTop:
            print sisVsweep_trigger, " sisVsweep_trigger"
            print sisPot_thisloop, " sisPot_thisloop"

        ### make directories
        if do_Ynum:
            if sisVsweep_trigger == sisPot_thisloop:
                # change the Y number if this is a new hot-cold pair
                if Y_trigger == K_thisloop:
                    Ynum     = Ynum + 1
                    Ynum_str = 'Y' + str('%04.f' % Ynum)
                # make a new directory for the Y data
                if platform == 'win32':
                    Ypath = rawdir + Ynum_str + '\\'
                elif platform == 'darwin':
                    Ypath = rawdir + Ynum_str + '/'
                if not os.path.isdir(Ypath):
                    os.makedirs(Ypath)
            # determine if this is a hot of cold measurement
            if 250 < K_thisloop:
                if platform == 'win32':
                    filepath = Ypath + 'hot\\'
                elif platform == 'darwin':
                    filepath = Ypath + 'hot/'
            elif K_thisloop <= 250:
                if platform == 'win32':
                    filepath = Ypath + 'cold\\'
                elif platform == 'darwin':
                    filepath = Ypath + 'cold/'


            # make the hot or cold directory
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
        else:
            # each sweep gets it own folder if there is no Y factors to consider
            if platform == 'win32':
                filepath = rawdir + str('%05.f' % sweepN) + '\\'
            elif platform == 'darwin':
                filepath = rawdir + str('%05.f' % sweepN) + '/'
            # make the sweep directory to store the data
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
        if sisVsweep_trigger == sisPot_thisloop:
            sweepN = sweepN + 1
            # name the files and the path the directory specifically for the sweep data
            params_filename   = filepath + "params.csv"
            magdata_filename  = filepath + "magdata.csv"
            sisdata_filename  = filepath + "sisdata.csv"
            fast_filename     = filepath + "fastsweep.csv"
            unpumped_filename = filepath + "unpumpedsweep.csv"
            
        if platform == 'win32':
            SweepPath   = filepath + 'sweep\\'
        elif platform == 'darwin':
            SweepPath     = filepath + 'sweep/'
        # TP_filename is determined below in the take data section
        # SIS_bias_filename is determined in the take data section below TP_filename
        # make the folder where sweep data is to be stored
        if not os.path.isdir(SweepPath):
            os.makedirs(SweepPath)
                
        
        #######################
        ###### Take Data ######
        #######################
        
        ### Data that is only taken once per SIS Voltage sweep
        if sisVsweep_trigger == sisPot_thisloop:
            # measure the electromagnet
            V_mag_list   = []
            mA_mag_list  = []
            pot_mag_list = []
            if not testmode:
                for meas_index in range(mag_meas):
                    magV_actual, magmA_actual, magpot_actual = measmag(verbose)
                    V_mag_list.append(magV_actual)
                    mA_mag_list.append(magmA_actual)
                    pot_mag_list.append(magpot_actual)
            else:
                print "testmode on, pretending to measure the magnet"
            
            # measure the LO power
            # set the bias system to measure relative LO power
            if not testmode:
                setmag_highlow(LOuA_magpot)
                magpot_actual = LOuA_magpot
                if verboseSet:
                    magmsg(magpot_actual)

                setSIS_only(LOuA_set_pot, sisV_feedback, verbose, careful)
                sisPot_actual = LOuA_set_pot
                if verboseSet:
                    sismsg(sisPot_actual)

                mV_LO_list     = []
                uA_LO_list     = []
                tp_LO_list     = []
                pot_LO_list    = []
                time_stamp_LO_list = []
                for meas_index in range(UCA_meas):
                    sismV_actual, sisuA_actual, sistp, sisPot_actual, time_stamp = measSIS_TP(LOuA_set_pot, sisV_feedback, verbose, careful)
                    mV_LO_list.append(sismV_actual)
                    uA_LO_list.append(sisuA_actual)
                    tp_LO_list.append(sistp)
                    pot_LO_list.append(sisPot_actual)
                    time_stamp_LO_list.append(time_stamp)

                # reset the bias system
                setmag_highlow(magpot_thisloop)
                magpot_actual = magpot_thisloop
                if verboseSet:
                    magmsg(magpot_actual)

                setSIS_only(sisPot_thisloop, sisV_feedback, verbose, careful)
                sisPot_actual = sisPot_thisloop
                if verboseSet:
                    sismsg(sisPot_actual)

            else:
                print "testmode on, pretending to measure the SIS bias to determine LO power"

            # the fast bias sweep 
            if do_fastsweep:
                # set the feedback to whatever the fastsweep_feedback is set
                status = setfeedback(fastsweep_feedback)
                feedback_actual = fastsweep_feedback
                if verboseSet:
                    fbmsg(feedback_actual)
                if not testmode:
                    # do the sweep, get the data
                    pot_fast, mV_fast, uA_fast, tp_fast = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                else:
                    print "testmode on, pretending to do the fast SIS bias sweep"
                # reset the feedback (if no umpumped measurement is to be made)
                if not do_unpumpedsweep:        
                    status = setfeedback(sisV_feedback)
                    feedback_actual = sisV_feedback
                    if verboseSet:
                        fbmsg(feedback_actual)

            # a fast bias sweep with the LO fully attenuated (unpumped sweep)
            if do_unpumpedsweep:
                # set the feedback (if not set from fastSISsweep above)
                if not do_fastsweep:
                    status = setfeedback(fastsweep_feedback)
                    feedback_actual = fastsweep_feedback
                    if verboseSet:
                        fbmsg(feedback_actual)
                # fully attenuate the LO, UCA voltage = 5
                full_attenuation = 5 # V
                status = LabJackU3_DAQ0(full_attenuation)
                UCA_actual = full_attenuation
                if verboseSet:
                    UCAmsg(UCA_actual)

                if not testmode:
                    # do the sweep, get the data
                    pot_unpump, mV_unpump, uA_unpump, tp_unpump \
                        = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                else:
                    print "testmode on, pretending to do the fast unpumped SIS bias sweep"
                # reset the UCA voltage
                status = LabJackU3_DAQ0(UCA_thisloop)
                UCA_actual = UCA_thisloop
                if verboseSet:
                    UCAmsg(UCA_actual)
                # reset the feedback
                status = setfeedback(sisV_feedback)
                feedback_actual = sisV_feedback
                if verboseSet:
                    fbmsg(feedback_actual)
            # end sisVsweep_trigger if statement
                
        ### SIS Voltage sweep data taking
        # find out what step this is in the voltage sweep for naming reasons
        step_num = 0
        while True:
            step_num = step_num + 1
            TP_filename = SweepPath + 'TP' + str(step_num) + ".csv"
            if not os.path.isfile(TP_filename):
                break
        # SIS_bias_filename is not used until the Write data section
        SIS_bis_filename = SweepPath + str(step_num) + ".csv"
        # spectral filename
        spec_filename = SweepPath + "spec" + str(step_num) + ".csv"
        # SIS bias measurements taken with the THz bias computer
        mV_sweep_list         = []
        uA_sweep_list         = []
        tp_sweep_list         = []
        pot_sweep_list        = []
        time_stamp_sweep_list = []
        if not testmode:
            for meas_index in range(high_res_meas):
                mV_sweep, uA_sweep, tp_sweep, pot_sweep, time_stamp_sweep = measSIS_TP(sisPot_thisloop,
                                                                                       sisV_feedback, verbose, careful)
                mV_sweep_list.append(mV_sweep)
                uA_sweep_list.append(uA_sweep)
                tp_sweep_list.append(tp_sweep)
                pot_sweep_list.append(pot_sweep)
                time_stamp_sweep_list.append(time_stamp_sweep)
            # total Power measured rapidly from the LabJack
            ### Note ### The LabJack and spectral data is written here, NOT below in the 'Write' section of the code
            if getspecs:
                getspecPlusTP(spec_filename, TP_filename, TPSampleFrequency, verbose=verbose, linear_sc=spec_linear_sc,
                  freq_start=spec_freq_start, freq_stop=spec_freq_stop, sweep_time=spec_sweep_time,
                  video_band=spec_video_band, resol_band=spec_resol_band, attenu=spec_attenu)
            else:
                LJ_streamTP(TP_filename, TPSampleFrequency, TPSampleTime, verbose)
        else:
            print "testmode on, pretending to take SIS bias data and the TP measurement"
            n = open(TP_filename, 'w')
            n.close()
                                
        ########################
        ###### Write Data ######
        ######################## 
        
        if sisVsweep_trigger == sisPot_thisloop:
            # find the mA the magnet was set to is do_magisweep is True
            if do_magisweep:       
                try:
                    magiset = magi_list[magpot_list.index(magpot_thisloop)]
                except ValueError:
                    min_val = 999999.0
                    for pot_index in range(len(magpot_list)):
                        test_val = abs(magpot_list[pot_index] - magpot_thisloop)
                        if test_val < min_val:
                            min_val = test_val
                            min_index = pot_index
                    magiset = magi_list[min_index]

            # find the uA of Current that this UCA voltage is set to provide
            if do_LOuApresearch:
                try:
                    LOuAset = LOuA_list[UCA_list.index(UCA_thisloop)]
                except ValueError:
                    min_val = 999999.0
                    for UCA_index in range(len(UCA_list)):
                        test_val = abs(UCA_list[UCA_index] - UCA_thisloop)
                        if test_val < min_val:
                            min_val = test_val
                            min_index = UCA_index
                    LOuA_thisloop = LOuA_list[min_index]

            
            ### record sweep settings, params.csv
            params = open(params_filename, 'w')
            params.write('param, value\n')
            params.write('temp,' + str(K_thisloop) + '\n')
            if do_magisweep:
                params.write('magisweep,True\n')
                params.write('magiset,' +  str(magiset) + '\n')
            else:
                params.write('magisweep,False\n')
            params.write('magpot,' +  str(magpot_thisloop) + '\n')
            if do_LOuAsearch:
                params.write('LOuAsearch,True\n')
                params.write('LOuAset,'  + str(LOuA_thisloop) + '\n')
            else:
                params.write('LOuAsearch,False\n')
            params.write('UCA_volt,' + str(UCA_thisloop) + '\n')
            params.write('LOuA_set_pot,' + str(LOuA_set_pot) + '\n')
            params.write('LOuA_magpot,' + str(LOuA_magpot) + '\n')
            params.write('LOfreq,' + str(LOfreq_thisloop) + '\n')
            params.write('IFband,' + str(IFband_thisloop) + '\n')
            params.close()
        
        
            # record the magnet settings 
            magdata = open(magdata_filename, 'w')
            magdata.write('V, mA, pot \n')
            for magi_index in range(len(V_mag_list)):
                V_mag   = V_mag_list[magi_index]
                mA_mag  = mA_mag_list[magi_index]
                pot_mag = pot_mag_list[magi_index]
                magdata.write(str(V_mag) + ',' + str(mA_mag) + ',' + str(pot_mag) +  '\n')
            magdata.close()
            
            # record the LOuA data, LO power
            LOuAdata = open(sisdata_filename, 'w')
            LOuAdata.write('mV, uA, tp, pot, time \n')
            for LOuA_index in range(len(mV_LO_list)):
                mV_LO         = mV_LO_list[LOuA_index]
                uA_LO         = uA_LO_list[LOuA_index]
                tp_LO         = tp_LO_list[LOuA_index]
                pot_LO        = pot_LO_list[LOuA_index]
                time_stamp_LO = time_stamp_LO_list[LOuA_index]
                LOuAdata.write(str(mV_LO) + ',' + str(uA_LO) + ',' + str(tp_LO) +  ',' + str(pot_LO) + ',' + str(time_stamp_LO) + '\n')
            LOuAdata.close()
            
            # record the fast sweep
            if do_fastsweep:
                fastdata = open(fast_filename, 'w')
                fastdata.write('pot, mV, uA, tp \n')
                for jj in range(len(pot_fast)):
                    fastdata.write(str(pot_fast[jj])+','+str(mV_fast[jj])+','+str(uA_fast[jj])+','+str(tp_fast[jj])+'\n')
                fastdata.close()
                
            # record the unpumped sweep, LO off
            if do_unpumpedsweep:
                unpumpdata = open(unpumped_filename, 'w')
                unpumpdata.write('pot, mV, uA, tp \n')
                for jj in range(len(pot_unpump)):
                    unpumpdata.write(str(pot_unpump[jj])+','+str(mV_unpump[jj])+','+str(uA_unpump[jj])+','+str(tp_unpump[jj])+'\n')
                unpumpdata.close()
                
            # end sisVsweep_trigger if statement
        
        ### Write SIS bias data
        
        sis_sweepData = open(SweepPath + str(step_num) + ".csv", 'w')
        sis_sweepData.write('mV, uA, tp, pot, time \n')
        for sweep_index in range(len(mV_sweep_list)):
            mV_sis     = mV_sweep_list[sweep_index]
            uA_sis     = uA_sweep_list[sweep_index]
            tp_sis     = tp_sweep_list[sweep_index]
            pot_sis    = pot_sweep_list[sweep_index]
            time_stamp = time_stamp_sweep_list[sweep_index]
            meas_line = str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) + ',' + str(pot_sis) + ',' + str(time_stamp) +'\n'
            sis_sweepData.write(meas_line)
            if verboseTop:
                print meas_line
        sis_sweepData.close()
        
        # TP data from the LabJack is written if the 'Take Data' section of the script
                
        ######################################
        ###### Email part of the script ######
        ######################################
        
        if param_index == 0:
            StartTime = time.time()
            EmailTime = StartTime
        else:
            NowTime       = time.time()
            ElapsedTime   = NowTime - StartTime
            RemainingTime = (ElapsedTime/(param_index))*(list_len-(param_index+1))
            if verboseTop:
                r_hours = numpy.floor(RemainingTime/3600)
                r_secs  = numpy.mod(RemainingTime, 3600)
                r_mins  = numpy.floor(r_secs/60)
                r_secs  = numpy.mod(r_secs, 60)
                r_str   = str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)\
                          + ' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time \n '
                print "estimated time remaining: " + r_str
    
            # Email Options
            if FiveMinEmail:
                if 5 <= numpy.floor(ElapsedTime/60):
                    EmailTrigger = True
                    FiveMinEmail = False
                    
            if PeriodicEmail:
                ElapsedEmailTime = NowTime - EmailTime
                if seconds_per_email < ElapsedEmailTime:
                    EmailTrigger = True
    
            if EmailTrigger:
                e_hours = numpy.floor(ElapsedTime/3600)
                e_secs  = numpy.mod(ElapsedTime, 3600)
                e_mins  = numpy.floor(e_secs/60)
                e_secs  = numpy.mod(ElapsedTime, 60)
                e_str   = str('%02.f' % e_hours)+' hrs  '+str('%02.f' % e_mins)\
                +' mins  '+str('%02.f' % e_secs)+' secs  is the elapsed time \n'
                
                r_hours = numpy.floor(RemainingTime/3600)
                r_secs  = numpy.mod(RemainingTime, 3600)
                r_mins  = numpy.floor(r_secs/60)
                r_secs  = numpy.mod(RemainingTime, 60)
                r_str   = str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)\
                +' mins  '+str('%02.f' % r_secs)+' secs  is the estimated \
                remaining time \n '
                email_caleb('Bias Sweep Update', e_str + r_str)
                
                EmailTrigger = False
                EmailTime = NowTime
    
    # turn things off after a run
    if ((not testmode) and (not chopper_off)):
        DisableDrive()
    if not testmode:
        zeropots(verbose)
    if FinishedEmail:
        NowTime       = time.time()
        ElapsedTime   = NowTime - StartTime
        e_hours = numpy.floor(ElapsedTime/3600)
        e_secs  = numpy.mod(ElapsedTime,3600)
        e_mins  = numpy.floor(e_secs/60)
        e_secs  = numpy.mod(ElapsedTime,60)        
        e_str   = str('%02.f' % e_hours) + ' hrs  ' + str('%02.f' % e_mins)\
        + ' mins  '+str('%02.f' % e_secs)+' secs  is the elapsed time \n '
        email_caleb('Bias Sweep Finished', "The program BaisSweep.py has \
        reached its end, congratulations! \n " + e_str)
    if (verbose or verboseTop):
        print " "
        print "The program BaisSweep.py has reached its end, congratulations!"
    
    
    return master_list
    
        