__author__ = 'chwheele'

import os, sys, numpy, time
# Caleb's Programs
from profunc import windir, getYnums, getSnums
from LabJack_control import LabJackU3_DAQ0, LJ_streamTP,enableLabJack, disableLabJack
from control import  opentelnet, closetelnet, measmag, setmag_only,setmag_highlow, setfeedback, \
    setSIS_only, measSIS_TP, zeropots, mag_channel,\
    default_magpot, default_sispot, default_LOfreq, default_UCA, default_IF
from StepperControl import EnableDrive, initialize, GoForth, GoBack, DisableDrive, stepper_close
from LOinput import RFon, RFoff, setfreq
from email_sender   import email_caleb
from fastSISsweep   import getfastSISsweep
from getspec import get_multi_band_spec
from PID import SIS_mV_PID, Emag_PID, LO_PID
from biasSweepFunc import MakeSetDirs, makeLists, orderLists,makeparamslist_Rec,  order_lists_around_center,\
    makeparamslist_center, fbmsg, Kmsg, magmsg, sismsg, LOuAmsg, UCAmsg, LOfreqmsg, IFmsg, \
    getSISpotList, getEmagPotList, getLOfreqList, getLOpowList, sweepShutDown




def BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, #careful=False,

              # Parameter sweep behaviour
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              testMode=True, warmmode=False, #turnRFoff=True,
              chopper_off=False, biasOnlyMode=False,
              warning=True,
              sleepForStandMeas = 5, high_res_meas=5,
              sweepShape="rectangular",
              dwellTime_Benchmark=None, dwellTime_sisVsweep=None,

              # email options
              FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
              seconds_per_email=1200,

              # Benchmark Tests
              do_benchmarkTest=True,
                # THz computer fast sweeps
              do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
                # measure the electromagnet and the SIS juction at their standard positions
              UCA_meas=10,

              # mV sweep Parameters
              sisV_feedback=True, do_sisVsweep=True,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1, sisVsweep_list=None,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_list=None,
              sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
              sisPot_feedFalse_list=None,

              # Powermeter read through LabJack
              TPSampleFrequency=100, TPSampleTime=2,

              # spectrum analyzer settings
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[],
              spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=300, aveNum=1,

              # Chopper temperature list
              K_list=[296],

              # Local Ocsillator frequency selector
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=1,
              LOfreqs_list=None,

              # Intermediate Frequency Band
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,

              # Electromagnet Options
              do_magisweep=True, mag_meas=10,
              magisweep_start=32, magisweep_stop=32, magisweep_step=1,
              magisweep_list=None,
              magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
              magpotsweep_list=None,

              # setting the local ocsilattor pump power
              do_LOuAsearch=True,  do_LOuApresearch=True, LOuA_search_every_sweep=False,
              UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
              UCAsweep_list=None,
              LOuAsearch_start=14, LOuAsearch_stop=14, LOuAsearch_step=1,
              LOuAsearch_list=None,

              # stepper motor control options
              stepper_vel = 0.5, stepper_accel = 1, forth_dist = 0.25, back_dist = 0.25):

    ######################################
    ###### Test mode configurations ######
    ######################################
    useTHzComputer=True
    # testmode exists so the program can be run without controlling external instruments
    if testMode:
        useTHzComputer=False
        chopper_off = True
        do_sisVsweep = False
        do_magisweep = False
        do_LOuAsearch = False
        do_LOuApresearch = False
        print 'Entering Test mode, no instruments will be controlled'
        if raw_input('Press Enter to accept this type anything to cancel') != '':
            sys.exit()

    # setting to make things work if we are ONLY testing the THz bias computer
    elif biasOnlyMode:
        chopper_off = True
        do_LOuAsearch = False
        do_LOuApresearch = False
        print 'Entering Test mode, no instruments will be controlled'
        if raw_input('Press Enter to accept this type anything to cancel') != '':
            sys.exit()

    if verbose:
        verboseSet=True
        verboseTop=True

    ### Determine if we need to run the chopper and how the output datafiles will be named
    # if 300 K and 77 K measurements are being made, give files a Y number to make them easy to find as pairs
    do_Ynum = True
    K_actual  = max(K_list)
    if verboseSet:Kmsg(K_actual)
    K_first = K_actual # this triggers the Y factor folder to be created
    len_K_list = len(K_list)
    if 1 == len_K_list:
        do_Ynum = False
        chopper_off = True
    elif 2 < len_K_list:
        print "The variable K_list can only have one value or two values only, try again..."
        sys.exit()
    else:
        temp_K_list = []
        temp_K_list.append(max(K_list))
        temp_K_list.append(min(K_list))
        K_list = temp_K_list

    ### A shut down procedure is executed at the end of the script not matter what exceptions are raised
    try:
        ##############################################################################
        ###### Enable some instruments that will be required to make this sweep ######
        ##############################################################################
        if testMode:
            feedback_actual = sisV_feedback
            magpot_actual = default_magpot
            sisPot_actual = default_sispot
            UCA_actual = default_UCA
            LOfreq_actual = default_LOfreq
            IFband_actual = default_IF
        else:
            ### Enable the THz bias computer
            opentelnet()
            # set the feedback
            setfeedback(feedback=sisV_feedback)
            feedback_actual = sisV_feedback
            if verboseSet:fbmsg(feedback_actual)
            # set the magnet to default position
            setmag_highlow(default_magpot)
            magpot_actual = default_magpot
            if verboseSet:magmsg(magpot_actual)
            # set the SIS pot
            setSIS_only(default_sispot, feedback_actual, verbose=False, careful=False)
            sisPot_actual = default_sispot
            if verboseSet:sismsg(sisPot_actual)

            if biasOnlyMode:
                UCA_actual = default_UCA
                LOfreq_actual = default_LOfreq
                IFband_actual = default_IF
            else:
                ### Open connection to the LabJack
                enableLabJack()
                # Turn off the UCA voltage (no attenuation)
                LabJackU3_DAQ0(default_UCA)
                UCA_actual = default_UCA
                if verboseSet:UCAmsg(UCA_actual)

                ### open communication to the signal generator and set the RF input to prescribed level and frequency
                setfreq(default_LOfreq)
                LOfreq_actual = default_LOfreq
                if verboseSet:LOfreqmsg(LOfreq_actual)
                # Enable the optical chopper

                # Communication with the thing that sets the IF band pass would be here
                IFband_actual = default_IF
                if verboseSet:IFmsg(IFband_actual)

                if chopper_off:
                    pass
                else:
                    if warning:
                        raw_input("Place optical chopper in 300K position")
                    EnableDrive()
                    initialize(vel=stepper_vel, accel=stepper_accel, verbose=verbose)

                    

        #######################################
        ###### Sort the sweep parameters ######
        #######################################

        ###### get the SIS voltage potentiometer parameters values from this function ######
        SISpot_List, feedback_actual, sisPot_actual, magpot_actual\
            = getSISpotList(sisV_feedback,useTHzComputer=useTHzComputer,
                            do_sisVsweep=do_sisVsweep, verbose=verbose,
                            verboseTop=verboseTop, verboseSet=verboseSet,
                            sisVsweep_list=sisVsweep_list, sisVsweep_start=sisVsweep_start,
                            sisVsweep_stop=sisVsweep_stop, sisVsweep_step=sisVsweep_step,
                            sisPot_feedTrue_list=sisPot_feedTrue_list, sisPot_feedTrue_start=sisPot_feedTrue_start,
                            sisPot_feedTrue_stop=sisPot_feedTrue_stop, sisPot_feedTrue_step=sisPot_feedTrue_step,
                            sisPot_feedFalse_list=sisPot_feedFalse_list, sisPot_feedFalse_start=sisPot_feedFalse_start,
                            sisPot_feedFalse_stop=sisPot_feedFalse_stop, sisPot_feedFalse_step=sisPot_feedFalse_step)
        if do_benchmarkTest:
            SISpot_List.append('benchMarkTest')


        ####### get the Electromagnet potentiometer values from this function #####
        EmagPotList, magi_list, magpot_actual\
            = getEmagPotList(useTHzComputer=useTHzComputer,
                   do_magisweep=do_magisweep,
                   verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet,
                   magisweep_list=magisweep_list, magisweep_start=magisweep_start,
                   magisweep_stop=magisweep_stop, magisweep_step=magisweep_step,
                   magpotsweep_list=magpotsweep_list, magpotsweep_start=magpotsweep_start,
                   magpotsweep_stop=magpotsweep_stop, magpotsweep_step=magpotsweep_step)

        ###### LO Frequency #####
        LOfreq_list = getLOfreqList(biasOnlyMode=biasOnlyMode,
                                    LOfreqs_list=LOfreqs_list,
                                    LOfreq_start=LOfreq_start,
                                    LOfreq_stop=LOfreq_stop,
                                    LOfreq_step=LOfreq_step)
        # this a catch for if the value of presearch needed to be changed
        # presearch is not an effective tool if both the LO frequency and LO power are being changed in single run
        lenLOfreqList = len(LOfreq_list)
        if ((1 < lenLOfreqList) and do_LOuApresearch):
            do_LOuApresearch = False
            print "do_LOuApresearch was changed to be False,"+\
                  "since the list of frequencies for this data run is greater than 1"


        ###### LO power #####
        LOuA_list, UCA_list, feedback_actual, sisPot_actual, magpot_actual, UCA_actual\
            = getLOpowList(sisV_feedback,useTHzComputer=useTHzComputer,
                           biasOnlyMode=biasOnlyMode,
                           testMode=testMode,
                           do_LOuAsearch=do_LOuAsearch,
                           do_LOuApresearch=do_LOuApresearch,
                           lenLOfreqList=lenLOfreqList,
                           verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet,
                           LOuAsearch_list=LOuAsearch_list,
                           LOuAsearch_start=LOuAsearch_start, LOuAsearch_stop=LOuAsearch_stop,
                           LOuAsearch_step=LOuAsearch_step,
                           UCAsweep_list=UCAsweep_list,
                           UCAsweep_min=UCAsweep_min, UCAsweep_max=UCAsweep_max, UCAsweep_step=UCAsweep_step)


        ###### IF bandwidth center frequencies
        if biasOnlyMode:
            IFband_list = ['biasOnlyMode']
        else:
            IFband_list = makeLists(IFband_start, IFband_stop, IFband_step)

        ####### fast and unpumped sweep settings
        if fastsweep_feedback:
            fSweepStart = SweepStart_feedTrue
            fSweepStop  = SweepStop_feedTrue
            fSweepStep  = SweepStep_feedTrue
        else:
            fSweepStart = SweepStart_feedFalse
            fSweepStop  = SweepStop_feedFalse
            fSweepStep  = SweepStep_feedFalse

        #########################################################################################################
        ####### From each unique list of parameters, make the master list of every parameter set to be run ######
        #########################################################################################################
        doing_UCA_list = (do_LOuApresearch or (do_LOuAsearch == False) or (UCAsweep_list is not None))
        master_list_input = []
        master_list_input.append((Kaxis,K_list))
        master_list_input.append((sisVaxis,SISpot_List))
        master_list_input.append((magaxis,EmagPotList))
        if doing_UCA_list:
            master_list_input.append((LOpowaxis,UCA_list))
        else:
            master_list_input.append((LOpowaxis,LOuA_list))
        master_list_input.append((LOfreqaxis,LOfreq_list))
        master_list_input.append((IFbandaxis,IFband_list))
        if verboseTop:
            print (Kaxis,K_list), " K axis list"
            print (sisVaxis,SISpot_List), " SIS Voltage axis list"
            print (magaxis,EmagPotList), " Electromagnet axis list"
            if doing_UCA_list:
                print (LOpowaxis,UCA_list), " LO power (UCA) axis list"
            else:
                print (LOpowaxis,LOuA_list), " LO power (LOuA) axis list, to be set with each change in frequency or LO power"
            print (LOfreqaxis,LOfreq_list), " LO frequency axis list"
            print (IFbandaxis,IFband_list), " IF band axis list"

        ordered_lists = orderLists(master_list_input)

        #if sweepShape == "rectangular":
        master_list = makeparamslist_Rec(ordered_lists)

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
                if warning:
                    user_input = raw_input("Press Enter to Continue or anything else to abort")
                    if user_input != '':
                        sweepShutDown(testMode=testMode,biasOnlyMode=biasOnlyMode,chopper_off=chopper_off)
                        sys.exit()
        else:
            print "list lengths in the function BiasSweep are not the same. " \
                  "Search for 'Truth_list' in the code to find the source of this error."
            sys.exit()

        ### post list-making initialization
        # does the datadir exist? If not, we will make it!
        rawdir = MakeSetDirs(datadir)

        # Set the trigger This tells the program it needs to make directories
        sisVsweep_trigger = SISpot_List[0]


        if do_Ynum:
            # find the higher integer Y number in this directory and set the new sweep to Ynum+1
            Ynums = getYnums(rawdir)
            # name this new data something different
            Ynum = 1
            while True:
                format_Ynum = 'Y'+str('%04.f' % Ynum)
                if format_Ynum in Ynums:
                    Ynum += 1
                else:
                    break
        else:
            Snums = getSnums(rawdir)
            # name this new data something different
            sweepN = 1
            while True:
                format_sweepN = str('%05.f' % sweepN)
                if format_sweepN in Snums:
                    sweepN += 1
                else:
                    break

        ####################################################
        ###### Start of Receiver Setting Control Loop ######
        ####################################################
        first_loop = True
        for param_index in range(list_len):

        ###########################
        ##### Set parameters ######
        ###########################
            ### unpack the values from the parameter lists
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


            if sisPot_thisloop == 'benchMarkTest':
                makeBenchmarkMeasurments=True
                sisPot_thisloop=default_sispot
                magpot_thisloop=default_magpot
            else:
                makeBenchmarkMeasurments=False

            #################################################
            ###### Move the chopper K_list (if needed) ######
            #################################################
            if not chopper_off:
                if not (K_thisloop == K_actual):
                    if testMode:
                        print "Testmode is 'True', pretending to move the chopper"
                    else:
                        if K_actual == K_first:
                            GoForth(dist=forth_dist)
                        else:
                            GoBack(dist=back_dist)
                    K_actual = K_thisloop
                    if verboseSet:Kmsg(K_actual)

            ####################################################
            ###### Set UCA Voltage for the LO (if needed) ######
            ####################################################
            if doing_UCA_list: # UCA values are set
                if not (UCA_thisloop == UCA_actual):
                    if ((not testMode) and (not biasOnlyMode)):
                        status = LabJackU3_DAQ0(UCA_thisloop)
                    else:
                        print "Testmode on, pretending to set the UCA voltage"
                    UCA_actual = UCA_thisloop
                    if verboseSet:UCAmsg(UCA_actual)
            else:
                if ((not (LOuA_thisloop == LOuA_actual)) or ((LOuA_search_every_sweep) and
                    (sisVsweep_trigger == sisPot_thisloop) and (K_actual==K_first))):
                    # if this if statement is true that the LO power will get set at the Set LO frequency below
                    if ((LOfreq_thisloop == LOfreq_actual)):
                        if ((not testMode) and (not biasOnlyMode)):
                            UCA_thisloop, deriv_uA_UCAvoltage \
                                = LO_PID(uA_set=LOuA_thisloop, feedback=feedback_actual, verbose=verbose)
                            # set the magnet to this loop's position
                            if useTHzComputer:setmag_highlow(magpot_thisloop)
                            magpot_actual = magpot_thisloop
                            if verboseSet:magmsg(magpot_thisloop)
                            # set the SIS pot to this loop's position
                            if useTHzComputer:setSIS_only(sisPot_thisloop, feedback_actual, verbose=False, careful=False)
                            sisPot_actual = sisPot_thisloop
                            if verboseSet:sismsg(sisPot_thisloop)
                        else:
                            print "Testmode is on, pretending to search for the LO current"
                            UCA_thisloop = "Testmode on, this value would be set by the program 'LO_PID'"
                        UCA_actual  = UCA_thisloop
                        LOuA_actual = LOuA_thisloop
                        if verboseSet:
                            UCAmsg(UCA_actual)
                            LOuAmsg(LOuA_actual)

            ##############################################
            ###### Set the LO frequency (if needed) ######
            ##############################################
            if (not (LOfreq_thisloop == LOfreq_actual)):
                if ((not testMode) and (not biasOnlyMode)):
                    setfreq(LOfreq_thisloop)
                else:
                    print "Testmode is on, pretending to set frequency to ", LOfreq_thisloop
                LOfreq_actual = LOfreq_thisloop
                if verboseSet: LOfreqmsg(LOfreq_actual)

                if not doing_UCA_list:
                    if not testMode:
                        UCA_thisloop, deriv_uA_UCAvoltage\
                            = LO_PID(uA_set=LOuA_thisloop, feedback=feedback_actual, verbose=verbose)
                        # set the magnet to this loop's position
                        if useTHzComputer:setmag_highlow(magpot_thisloop)
                        magpot_actual = magpot_thisloop
                        if verboseSet:magmsg(magpot_thisloop)
                        # set the SIS pot to this loop's position
                        if useTHzComputer:setSIS_only(sisPot_thisloop, feedback_actual, verbose=False, careful=False)
                        sisPot_actual = sisPot_thisloop
                        if verboseSet:sismsg(sisPot_thisloop)
                    else:
                        print "Testmode is on, predending to search for the LO current"
                        UCA_thisloop = "Testmode on, this value would be set by the program 'setLOI'"
                    UCA_actual = UCA_thisloop


            ##############################################################################
            ###### Set the SIS bias voltage by setting the pot position (if needed) ######
            ##############################################################################
            if not (sisPot_thisloop == sisPot_actual):
                if not testMode:
                    setSIS_only(sisPot_thisloop, feedback_actual, verbose, False)
                else:
                    print 'testMode on, pretending to set the SIS pot'
                sisPot_actual = sisPot_thisloop
                if verboseSet:sismsg(sisPot_actual)

            ####################################
            ###### Set magnet (if needed) ######
            ####################################
            if not (magpot_thisloop == magpot_actual):
                if not testMode:
                    setmag_highlow(magpot_thisloop)
                else:
                    print 'testMode on, pretending to set the E-magnet pot'
                magpot_actual = magpot_thisloop
                if verboseSet: magmsg(magpot_actual)

            #### Not currently set to do anything
            ####### Set IFband (if needed) ######
            #####################################
            if not IFband_thisloop == IFband_actual:
                IFband_actual = IFband_thisloop

            #########################################################################
            #########################################################################
            ###### end sweep parameter changes/Start SIS Sweep Data Collection ######
            #########################################################################
            #########################################################################


            #################################################################
            ###### Make the path of the data and write new directories ######
            #################################################################
            if ((sisPot_thisloop==sisVsweep_trigger) and (K_first==K_actual)):
                if verboseTop:
                    print "New sweep triggered "
                    print sisPot_thisloop, "=  sisPot_thisloop"
                    print "making directories"
                if do_Ynum:
                    Ynum = Ynum + 1
                else:
                    sweepN = sweepN + 1

            if do_Ynum:
                Ynum_str = 'Y' + str('%04.f' % Ynum)
                Ypath = windir(rawdir + Ynum_str + '/')
                # determine if this is a hot of cold measurement
                if K_thisloop == K_first:
                    filepath = Ypath + 'hot/'
                else:
                    filepath = Ypath + 'cold/'
            else:
                filepath = windir(rawdir + str('%05.f' % sweepN) + '/')
            # name the files and the path the directory specifically for the sweep data
            params_filename   = filepath + "params.csv"
            magdata_filename  = filepath + "magdata.csv"
            sisdata_filename  = filepath + "sisdata.csv"
            fast_filename     = filepath + "fastsweep.csv"
            unpumped_filename = filepath + "unpumpedsweep.csv"
            SweepPath = windir(filepath + 'sweep/')
            # TP_filename is determined below in the take data section
            # SIS_bias_filename is determined in the take data section below TP_filename
            # make the folder where sweep data is to be stored
            if not os.path.isdir(SweepPath):
                os.makedirs(SweepPath)


            #######################
            ###### Take Data ######
            #######################
            ###### Take Data ######
            #######################
            ###### Take Data ######
            #######################
            if makeBenchmarkMeasurments:
                ########################################################
                ###### Once per SIS voltage sweep Data Collection ######
                ########################################################
                if dwellTime_Benchmark is not None:
                    time.sleep(dwellTime_Benchmark)
                # measure the LO power at default magnet and SISpot positions
                # set the bias system to measure relative LO power
                if sisVsweep_trigger == sisPot_thisloop:
                    mV_LO_list     = []
                    uA_LO_list     = []
                    tp_LO_list     = []
                    pot_LO_list    = []
                    time_stamp_LO_list = []
                    if not testMode:
                        # measure the SIS junction
                        for meas_index in range(UCA_meas):
                            sismV_actual, sisuA_actual, sistp, sisPot_actual, time_stamp \
                                = measSIS_TP(default_sispot, feedback_actual, verbose, careful=False)
                            mV_LO_list.append(sismV_actual)
                            uA_LO_list.append(sisuA_actual)
                            tp_LO_list.append(sistp)
                            pot_LO_list.append(sisPot_actual)
                            time_stamp_LO_list.append(time_stamp)
                        if verboseSet:
                            LOuAmsg(LOuA_actual)
                            UCAmsg(UCA_actual)
                    else:
                        print "testMode on, pretending to measure the SIS junction to determine LO power"

                # Get standard electromagnet data
                if sisVsweep_trigger == sisPot_thisloop:
                    V_mag_list   = []
                    mA_mag_list  = []
                    pot_mag_list = []
                    if not testMode:
                        # measure the electromagnet
                        for meas_index in range(mag_meas):
                            magV_actual, magmA_actual, magpot_actual = measmag(verbose)
                            V_mag_list.append(magV_actual)
                            mA_mag_list.append(magmA_actual)
                            pot_mag_list.append(magpot_actual)
                    else:
                        print "testMode on, pretending to measure the magnet"



                # the fast bias sweep
                if do_fastsweep:
                    if (testMode):
                        "testMode on, pretending to the fast SIS voltage sweep"
                    else:
                        # set the feedback to whatever the fastsweep_feedback is set
                        status = setfeedback(fastsweep_feedback)
                        feedback_actual = fastsweep_feedback
                        if verboseSet:
                            fbmsg(feedback_actual)
                        if not testMode:
                            # do the sweep, get the data
                            pot_fast, mV_fast, uA_fast, tp_fast = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                        else:
                            print "testMode on, pretending to do the fast SIS bias sweep"
                        # reset the feedback (if no umpumped measurement is to be made)
                        if not do_unpumpedsweep:
                            status = setfeedback(sisV_feedback)
                            feedback_actual = sisV_feedback
                            if verboseSet:
                                fbmsg(feedback_actual)

                # a fast bias sweep with the LO fully attenuated (unpumped sweep)
                if do_unpumpedsweep:
                    if (testMode or biasOnlyMode):
                        "testMode or biasOnlyMode on, pretending to the unpumped fast SIS voltage sweep"
                        'pretending to fully attenuate the LO signal'
                    else:
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
                    if verboseSet:UCAmsg(UCA_actual)

                    if testMode:
                        print "pretending to sweep"
                    else:
                        if biasOnlyMode:
                            print "The LO's UCA voltage is not controled in baisOnlyMode for unpumper sweeps"
                        # do the sweep, get the data
                        pot_unpump, mV_unpump, uA_unpump, tp_unpump \
                            = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)
                    if (testMode or biasOnlyMode):
                        print 'pretending to reset the feedback and the LO attenuation to the values for this loop'
                    else:
                        # reset the UCA voltage
                        status = LabJackU3_DAQ0(UCA_thisloop)
                        # reset the feedback
                        status = setfeedback(sisV_feedback)
                    UCA_actual = UCA_thisloop
                    if verboseSet: UCAmsg(UCA_actual)
                    feedback_actual = sisV_feedback
                    if verboseSet: fbmsg(feedback_actual)
                # end of Benchmark measurements
            else:
                ###############################################
                ###### SIS voltage sweep Data Collection ######
                ###############################################
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

                if dwellTime_sisVsweep is not None:
                    time.sleep(dwellTime_sisVsweep)
                ### SIS Voltage sweep data taking
                if not testMode:
                    for meas_index in range(high_res_meas):
                        mV_sweep, uA_sweep, tp_sweep, pot_sweep, time_stamp_sweep \
                            = measSIS_TP(sisPot_thisloop, sisV_feedback, verbose, careful=False)
                        mV_sweep_list.append(mV_sweep)
                        uA_sweep_list.append(uA_sweep)
                        tp_sweep_list.append(tp_sweep)
                        pot_sweep_list.append(pot_sweep)
                        time_stamp_sweep_list.append(time_stamp_sweep)
                    # total Power measured rapidly from the LabJack
                    ### Note ### The LabJack and spectral data is written here, NOT below in the 'Write' section of the code
                    if getspecs:
                        get_multi_band_spec(spec_filename, TP_filename, TPSampleFrequency,
                                            verbose=verbose, linear_sc=spec_linear_sc,
                                            spec_freq_vector=spec_freq_vector, sweep_time=spec_sweep_time,
                                            video_band=spec_video_band, resol_band=spec_resol_band, attenu=spec_attenu,
                                            lin_ref_lev=lin_ref_lev, aveNum=aveNum,)
                    else:
                        LJ_streamTP(TP_filename, TPSampleFrequency, TPSampleTime, verbose)
                else:
                    print "testMode on, pretending to take SIS bias data and the TP measurement"
                    n = open(TP_filename, 'w')
                    n.close()










        # add a blank line to the output to show the end of a loop
        if any([verbose,verboseSet,verboseTop]):
            print ''
    # turn Everything off
    finally:
        sweepShutDown(testMode=testMode,biasOnlyMode=biasOnlyMode,chopper_off=chopper_off)

    return

if __name__ == "__main__":
    BiasSweep('/Users/chw3k5/local_kappa_data/Kappa/NA38/IVsweep/newBiasSweepTest/',
              K_list=[296,77],
              magpotsweep_list=[66666])



