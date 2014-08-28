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
    

def BiasSweep(datadir, verbose=True, verboseTop=True, careful=False,
sweepNstart=0, Ynum=0, testmode=False,
do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
SweepStart_feedFalse=65100, SweepStop_feedFalse=57000,
SweepStep_feedFalse=100,
sisV_feedback=True, do_sisVsweep=True, high_res_meas=5,
TPSampleFrequency=100, TPSampleTime=2,
sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000,
sisPot_feedFalse_step=100,
sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000,
sisPot_feedTrue_step=100,
getspecs=False, spec_linear_sc=True, spec_freq_start=0, spec_freq_stop=6,
spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30, spec_attenu=0,
Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
K_list=[296],
LOfreq_start=672, LOfreq_stop=672, LOfreq_step=1,
IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
do_magisweep=True, mag_meas=10,
magisweep_start=32, magisweep_stop=32, magisweep_step=1,
magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
do_sisisweep=True, UCA_set_pot=56800, UCA_meas=10,
sisisweep_start=12, sisisweep_stop=12, sisisweep_step=1,
sisi_magpot=103323, sisi_cheat_num=56666,
UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
sweepShape="rectangular",
FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
seconds_per_email=1200, chopper_off=False, presearch_LOuA=True
):

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
        from StepperControl import initialize, GoForth, DisableDrive
    from email_sender   import email_caleb
    from fastSISsweep   import getfastSISsweep
    from getspec import getspecPlusTP
    
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
        do_sisisweep = False
    else:
        status = setfeedback(sisV_feedback)
    if do_sisVsweep:
        if verboseTop:
            print "Finding SIS pot positions for each magnet Voltage in 'sisV_list'."
        sisV_list = makeLists(sisVsweep_start, sisVsweep_stop, sisVsweep_step)
        sisPot_list = []
        cheat_num_temp = 65100 # center position of the SIS pot
        for sisV in sisV_list:
            if verboseTop:
                print "Finding the potentiometer position for the sis bias voltage of " + str('%1.3f' % sisV) + 'mV'
            mV_sis_temp, uA_sis_temp, pot_sis_temp = setSIS_Volt(sisV, verbose,
            careful, cheat_num_temp)
            sisPot_list.append(pot_sis_temp)
            cheat_num_temp = pot_sis_temp
    else:
        sisV_list = []
        if sisV_feedback:
            sisPot_list = makeLists(sisPot_feedTrue_start,
            sisPot_feedTrue_stop, sisPot_feedTrue_step)
        elif sisV_feedback == False:
            sisPot_list = makeLists(sisPot_feedFalse_start,
            sisPot_feedFalse_stop, sisPot_feedFalse_step)
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
        if presearch_LOuA:
            for magi in magi_list:
                V_mag_temp, mA_mag_temp, pot_mag_temp = setmagI(magi, verbose, careful)
                magpot_list.append(pot_mag_temp)
            magpot_list.sort
            if magpot_list[-1] < magpot_list[0]:
                magpot_list.reverse()

    else:
        magi_list = []
        magpot_list = makeLists(magpotsweep_start, magpotsweep_stop, magpotsweep_step)
    
    # LO power
    if (do_sisisweep and presearch_LOuA):
        if verboseTop:
            print "Finding SIS pot positions for each SIS current in \
            'sisi_list'."
        sisi_list = makeLists(sisisweep_start, sisisweep_stop, sisisweep_step)
        UCA_list  = []
        setmag_highlow(sisi_magpot) # set the Emagnet to a known position
        setSIS_only(UCA_set_pot, sisV_feedback, verbose, careful) # set the SIS bias to a known position
        for sisi in sisi_list:
            mV_sis_temp, uA_sis_temp, pot_sis_temp, UCA_val_temp = setLOI(sisi, verbose, careful)
            UCA_list.append(UCA_val_temp)
    else:
        sisi_list = makeLists(sisisweep_start, sisisweep_stop, sisisweep_step)
        UCA_list = makeLists(UCAsweep_min, UCAsweep_max, UCAsweep_step)
    
    # LO Frequency
    LOfreq_list = makeLists(LOfreq_start, LOfreq_stop, LOfreq_step)
    if (1 < len(LOfreq_list)) and (1 < len(UCA_list)):
        presearch_LOuA = False
    
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
    
    #########################################################################
    ####### From each unique list of parameter, make the master list of every 
    # parameter set to be run ######
    ################################
    if presearch_LOuA:
        master_list_input = [(Kaxis,K_list), (sisVaxis,sisPot_list),
        (LOfreqaxis,LOfreq_list), (IFbandaxis,IFband_list)]
        if verboseTop:
            print (Kaxis,K_list), " K axis list"
            print (sisVaxis,sisPot_list), " SIS Voltage axis list"
            print (magaxis,magpot_list), " Electromagnet axis list"
            print (LOpowaxis,UCA_list), " LO power (UCA) axis list"
            print (LOfreqaxis,LOfreq_list), " LO frequency axis list"
            print (IFbandaxis,IFband_list), " IF band axis list"
    else:
        master_list_input = [(Kaxis,K_list), (sisVaxis,sisPot_list),
        (magaxis,magpot_list), (LOpowaxis,sisi_list),
        (LOfreqaxis,LOfreq_list), (IFbandaxis,IFband_list)]
        if verboseTop:
            print (Kaxis,K_list), " K axis list"
            print (sisVaxis,sisPot_list), " SIS Voltage axis list"
            print (magaxis,magpot_list), " Electromagnet axis list"
            print (LOpowaxis,sisi_list), " LO power (sisi) axis list"
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
    else:
        do_Ynum = False
    
    # initialize some variables
    K_last      = -999999
    sisPot_last = -999999
    magpot_last = -999999
    UCA_last    = -999999
    sisi_last   = -999999
    LOfreq_last = -999999
    IFband_last = -999999
    EmailTrigger = False
    sweepN = sweepNstart
    
    # unpack the sorted lists of parameters
    master_K_list      = master_list[Kaxis]
    master_sisPot_list = master_list[sisVaxis]
    master_magpot_list = master_list[magaxis]
    if presearch_LOuA:
        master_UCA_list    = master_list[LOpowaxis]
    else:
        master_sisi_list   = master_list[LOpowaxis]
    master_LOfreq_list = master_list[LOfreqaxis]
    master_IFband_list = master_list[IFbandaxis]
    
    # make sure all the lists are the same length
    Truth_list = []
    Truth_list.append(len(master_K_list     ) == len(master_sisPot_list))
    Truth_list.append(len(master_sisPot_list) == len(master_magpot_list))
    if presearch_LOuA:
        Truth_list.append(len(master_magpot_list) == len(master_UCA_list   ))
        Truth_list.append(len(master_UCA_list   ) == len(master_LOfreq_list))
    else:
        Truth_list.append(len(master_magpot_list) == len(master_sisi_list   ))
        Truth_list.append(len(master_sisi_list   ) == len(master_LOfreq_list))
    Truth_list.append(len(master_LOfreq_list) == len(master_IFband_list))
    if all(Truth_list):
        list_len = len(master_K_list)
        if verboseTop:
            print "List lengths are verified, starting control sequence"
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
        setfreq(672)
        RFon()
    # a trigger for certain parameters thatI only collected once a sweep
    sisVsweep_trigger = master_sisPot_list[0]
    for param_index in range(list_len):
    ###########################
    ##### Set parameters ######
    ###########################     
        # unpack the values from the parameter lists
        K_current      = master_K_list[param_index]
        sisPot_current = master_sisPot_list[param_index]
        magpot_current = master_magpot_list[param_index]
        if presearch_LOuA:
            UCA_current    = master_UCA_list[param_index]
        else:
            sisi_current   = master_sisi_list[param_index] 
        LOfreq_current = master_LOfreq_list[param_index]
        IFband_current = master_IFband_list[param_index]
        
        if verboseTop:
            print "K_currnet      = ", K_current
            print "sisPot_current = ", sisPot_current
            print "magpot_currnet = ", magpot_current
            if presearch_LOuA:
                print "UCA_current    = ", UCA_current
            else:
                print "sisi_current   = ", sisi_current
            print "LOfreq_current = ", LOfreq_current
            print "IFband_current = ", IFband_current
        
        # Move the chopper K_list (if needed)
        if not (K_current == K_last):
            if do_Ynum:
                if not testmode:
                    GoForth()
                else:
                    print "testmode on, pretending to move the chopper"
                if (verboseTop):
                    print "The command to move the chopper has been sent"
            K_last = K_current
        
        
        # Set UCA Voltage for the LO (if needed)
        if presearch_LOuA:
            if not (UCA_current == UCA_last):
                if not testmode:
                    status = LabJackU3_DAQ0(UCA_current)
                else:
                    print "testmode on, pretending to set the UCA voltage"
                if (verboseTop):
                    print "UCA voltage set to ", UCA_current
                UCA_last = UCA_current
        else:
            if not (sisi_current == sisi_last):
                # if this if statement is true that the LO power will get set at the Set LO frequency below
                if LOfreq_current == LOfreq_last:
                    if not testmode:    
                        setmag_highlow(sisi_magpot) # set the Emagnet to a known position
                        setSIS_only(UCA_set_pot, sisV_feedback, verbose, careful)
                        mV_sis_temp, uA_sis_temp, sisPot_temp, UCA_current = setLOI(sisi_current, verbose, careful)
                        setmag_highlow(magpot_current)
                        setSIS_only(sisPot_current, sisV_feedback, verbose, careful)
                        
                sisi_last = sisi_current
        
        
        # Set the LO frequency (if needed)
        if not (LOfreq_current == LOfreq_last):
            setmag_highlow(sisi_magpot) # set the Emagnet to a known position
            magpot_current = sisi_magpot
            setSIS_only(UCA_set_pot, sisV_feedback, verbose, careful)
            setfreq(LOfreq_current)
            mV_sis_temp, uA_sis_temp, sisPot_temp, UCA_current = setLOI(sisi_current, verbose, careful)
            setmag_highlow(magpot_current)
            setSIS_only(sisPot_current, sisV_feedback, verbose, careful)
            LOfreq_last = LOfreq_current
            print "Here"
        
        # Set the SIS bias voltage by setting the pot position (if needed)
        if not (sisPot_current == sisPot_last):
            if not testmode:
                setSIS_only(sisPot_current, sisV_feedback, verbose, careful)
            else:
                print 'testmode on, pretending to set the SIS pot'
            if (verboseTop):
                print "SIS bias potentiometer position set to ", sisPot_current
            sisPot_last = sisPot_current
        
        # Set magnet (if needed)
        if not (magpot_current == magpot_last):
            if not testmode:
                setmag_highlow(magpot_current)
            else:
                print 'testmode on, pretending to set the E-magnet pot'
            if (verboseTop):
                print "Magnet potentiometer position set to ", magpot_current
            magpot_last    = magpot_current 
            
            
        #### Not currently set to do anything
        # Set IFband (if needed)
        if not IFband_current == IFband_last:
            IFband_last = IFband_current
        
        # all parameters are now set
        
        ###################################
        ###### Write new directories ######
        ###################################
        # we only need to save certain data or make new folders once per SIS voltage sweep
        if verboseTop:
            print sisVsweep_trigger, " sisVsweep_trigger"
            print sisPot_current, " sisPot_current"
        if sisVsweep_trigger == sisPot_current:
            sweepN = sweepN + 1
            ### make directories
            if do_Ynum:
                # change the Y number if this is a new hot-cold pair
                if Y_trigger == K_current:
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
                if 250 < K_current:
                    if platform == 'win32':
                        filepath = Ypath + 'hot\\'
                    elif platform == 'darwin':
                        filepath = Ypath + 'hot/'    
                else:
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
        if sisVsweep_trigger == sisPot_current:
            # measure the electromagnet
            V_mag_list   = []
            mA_mag_list  = []
            pot_mag_list = []
            if not testmode:
                for meas_index in range(mag_meas):
                    V_mag, mA_mag, pot_mag = measmag(verbose)
                    V_mag_list.append(V_mag)
                    mA_mag_list.append(mA_mag)
                    pot_mag_list.append(pot_mag)
            else:
                print "testmode on, pretending to measure the magnet"
            
            # measure the LO power
            # set the bias system to measure relative LO power
            setmag_highlow(sisi_magpot)
            setSIS_only(UCA_set_pot, sisV_feedback, verbose, careful)
            mV_LO_list     = []
            uA_LO_list     = []
            tp_LO_list     = []
            pot_LO_list    = []
            time_stamp_LO_list = []
            if not testmode:
                for meas_index in range(UCA_meas):
                    mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(UCA_set_pot, sisV_feedback, verbose, careful)
                    mV_LO_list.append(mV_sis)
                    uA_LO_list.append(uA_sis)
                    tp_LO_list.append(tp_sis)
                    pot_LO_list.append(pot_sis)
                    time_stamp_LO_list.append(time_stamp)
            else:
                print "testmode on, pretending to measure the SIS bias to determine LO power"
            # reset the bias system
            setmag_highlow(magpot_current)
            setSIS_only(sisPot_current, sisV_feedback, verbose, careful)
            
            # the fast bias sweep 
            if do_fastsweep:
                # set the feedback to whatever the fastsweep_feedback is set
                status = setfeedback(fastsweep_feedback)
                if not testmode:
                    # do the sweep, get the data
                    pot_fast, mV_fast, uA_fast, tp_fast = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                else:
                    print "testmode on, pretending to do the fast SIS bias sweep"
                # reset the feedback (if no umpumped measurement is to be made)
                if not do_unpumpedsweep:        
                    status = setfeedback(sisV_feedback)
                    
            # a fast bias sweep with the LO fully attenuated (unpumped sweep)
            if do_unpumpedsweep:
                # set the feedback (if not set from fastSISsweep above)
                if not do_fastsweep:
                    status = setfeedback(fastsweep_feedback)
                # fully attenuate the LO, UCA voltage = 5
                status = LabJackU3_DAQ0(5)
                if not testmode:
                    # do the sweep, get the data
                    pot_unpump, mV_unpump, uA_unpump, tp_unpump =getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                else:
                    print "testmode on, pretending to do the fast unpumped SIS bias sweep"
                # reset the UCA voltage
                status = LabJackU3_DAQ0(UCA_current)
                # reset the feedback
                status = setfeedback(sisV_feedback)
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
                mV_sweep, uA_sweep, tp_sweep, pot_sweep, time_stamp_sweep = measSIS_TP(sisPot_current,
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
        
        if sisVsweep_trigger == sisPot_current:
            # find the mA the magnet was set to is do_magisweep is True
            if do_magisweep:       
                try:
                    magiset = magi_list[magpot_list.index(magpot_current)]
                except ValueError:
                    min_val = 999999.0
                    for pot_index in range(len(magpot_list)):
                        test_val = abs(magpot_list[pot_index] - magpot_current)
                        if test_val < min_val:
                            min_val = test_val
                            min_index = pot_index
                    magiset = magi_list[min_index]
            # find the uA of Current that this UCA voltage is set to provide
            if do_sisisweep:
                try:
                    sisiset = sisi_list[UCA_list.index(UCA_current)]
                except ValueError:
                    min_val = 999999.0
                    for UCA_index in range(len(UCA_list)):
                        test_val = abs(UCA_list[UCA_index] - UCA_current)
                        if test_val < min_val:
                            min_val = test_val
                            min_index = UCA_index
                    sisiset = sisi_list[min_index] 
            
            ### record sweep settings, params.csv
            params = open(params_filename, 'w')
            params.write('param, value\n')
            params.write('temp,' + str(K_current) + '\n')
            if do_magisweep:
                params.write('magisweep,True\n')
                params.write('magiset,' +  str(magiset) + '\n')
                params.write('magpot,'  +  str(magpot_current)       + '\n')
            else:
                params.write('magisweep,False\n')
                params.write('magpot,' +  str(magpot_current) + '\n')
            if do_sisisweep:
                params.write('sisisweep,True\n')
                params.write('sisiset,'  + str(sisiset) + '\n')
                params.write('UCA_volt,' + str(UCA_current)   + '\n')
            else:
                params.write('sisisweep,False\n')
                params.write('UCA_volt,' + str(UCA_current) + '\n')
            params.write('LOfreq,' + str(LOfreq_current) + '\n')
            params.write('IFband,' + str(IFband_current) + '\n')
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
            
            # record the sisi data, LO power
            sisidata = open(sisdata_filename, 'w')
            sisidata.write('mV, uA, tp, pot, time \n')
            for sisi_index in range(len(mV_LO_list)):
                mV_LO         = mV_LO_list[sisi_index]
                uA_LO         = uA_LO_list[sisi_index]
                tp_LO         = tp_LO_list[sisi_index]
                pot_LO        = pot_LO_list[sisi_index]
                time_stamp_LO = time_stamp_LO_list[sisi_index] 
                sisidata.write(str(mV_LO) + ',' + str(uA_LO) + ',' + str(tp_LO) +  ',' + str(pot_LO) + ',' + str(time_stamp_LO) + '\n')
            sisidata.close()
            
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
    
        