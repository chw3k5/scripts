__author__ = 'chwheele'

import os, sys, numpy, time
# Caleb's Programs
from profunc import windir, getYnums, getSnums
from LabJack_control import LabJackU3_DAQ0, LJ_streamTP,enableLabJack, disableLabJack
from control import  opentelnet, closetelnet, measmag, setmag_only,setmag_highlow, setfeedback, \
    setSIS_only, measSIS_TP, zeropots, mag_channel, default_magpot, default_sispot
from StepperControl import EnableDrive, initialize, GoForth, GoBack, DisableDrive, stepper_close
from LOinput import RFon, RFoff, setfreq
from email_sender   import email_caleb
from fastSISsweep   import getfastSISsweep
from getspec import get_multi_band_spec
from PID import SIS_mV_PID, Emag_PID, LO_PID
from biasSweepFunc import MakeSetDirs, makeLists, orderLists,makeparamslist_Rec,  order_lists_around_center,\
    makeparamslist_center, fbmsg, Kmsg, magmsg, sismsg, LOuAmsg, UCAmsg, LOfreqmsg, IFmsg, \
    getSISpotList



def BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, careful=False,
              testMode=False, warmmode=False, do_set_mag_highlow=False, turnRFoff=True,
              do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              sisV_feedback=True, do_sisVsweep=True,
              TPSampleFrequency=100, TPSampleTime=2,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1, sisVsweep_list=None,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_list=None,
              sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
              sisPot_feedFalse_list=None,
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[],
              spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=300, aveNum=1,
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              K_list=[296],

              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=1,
              LOfreqs_list=None,

              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,

              do_magisweep=True, mag_meas=10,
              magisweep_start=32, magisweep_stop=32, magisweep_step=1,
              magisweep_list=None,
              magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
              magpotsweep_list=None,


              do_LOuAsearch=True, LOuA_search_every_sweep=False,
              UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
              UCAsweep_list=None,
              LOuAsearch_start=14, LOuAsearch_stop=14, LOuAsearch_step=1,
              LOuAsearch_list=None,


              sweepShape="rectangular",
              FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
              seconds_per_email=1200, chopper_off=False, do_LOuApresearch=True, biasOnlyMode=False,
              warning=False,

              sleepForStandMeas = 5, high_res_meas=5, UCA_meas=10,

              stepper_vel = 0.5, stepper_accel = 1, forth_dist = 0.25, back_dist = 0.25):

    ######################################
    ###### Test mode configurations ######
    ######################################

    # testmode exists so the program can be run without controlling external instruments
    if testMode:
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
    ##############################################################################
    ###### Enable some instruments that will be required to make this sweep ######
    ##############################################################################
    if not testMode:
        # Enable the THz bias computer
        opentelnet()
        if not biasOnlyMode:
            # Open connection to the LabJack
            enableLabJack()
            # open communication to the signal generator and set the RF input to prescribed level and frequency
            setfreq()
            # Enable the optical chopper
            if not chopper_off:
                EnableDrive()


    ### A shout down procedure is executed at the end of the script not matter what exceptions are raised
    try:
        #######################################
        ###### Sort the sweep parameters ######
        #######################################

        ###### get the SIS voltage pot parameters out of this
        SISpot_List, feedback_actual, sisPot_actual, magpot_actual\
            = getSISpotList(sisV_feedback,
                            do_sisVsweep=do_sisVsweep, verbose=verbose,
                            verboseTop=verboseTop, verboseSet=verboseSet,
                            sisVsweep_list=sisVsweep_list, sisVsweep_start=sisVsweep_start,
                            sisVsweep_stop=sisVsweep_stop, sisVsweep_step=sisVsweep_step,
                            sisPot_feedTrue_list=sisPot_feedTrue_list, sisPot_feedTrue_start=sisPot_feedTrue_start,
                            sisPot_feedTrue_stop=sisPot_feedTrue_stop, sisPot_feedTrue_step=sisPot_feedTrue_step,
                            sisPot_feedFalse_list=sisPot_feedFalse_list, sisPot_feedFalse_start=sisPot_feedFalse_start,
                            sisPot_feedFalse_stop=sisPot_feedFalse_stop, sisPot_feedFalse_step=sisPot_feedFalse_step)

        # Electromagnet
        if do_magisweep:
            if verboseTop:
                print "Finding Electromagnet pot positions for each magnet current in 'magi_list'."
            if magisweep_list is None:
                magi_list = makeLists(magisweep_start, magisweep_stop, magisweep_step)
            else:
                magi_list = magisweep_list
            magpot_list = []

            for magi in magi_list:
                magpot_actual, deriv_mA_magpot = Emag_PID(mA_set=magi,verbose=verbose)
                magpot_list.append(numpy.round(magpot_actual))
                if verboseSet:magmsg(magpot_actual)
            # arrange value from biggest to smallest
            magpot_list.sort()
            if magpot_list[-1] < magpot_list[0]: magpot_list = reversed(magpot_list)

        else:
            magi_list = None
            if magpotsweep_list is None:
                magpot_list = makeLists(magpotsweep_start, magpotsweep_stop, magpotsweep_step)
            else:
                magpot_list = magpotsweep_list

        # LO Frequency
        if biasOnlyMode:
            LOfreq_list = ['biasOnlyMode']
        else:
            if LOfreqs_list is None:
                LOfreq_list = list(makeLists(LOfreq_start, LOfreq_stop, LOfreq_step))
            else:
                LOfreq_list = LOfreqs_list
            # this a catch for if the value of presearch needed to be changed
            # presearch is not an effective tool if both the LO frequency and LO power are being changed in single run
            if ((1 < len(LOfreq_list)) and do_LOuApresearch):
                do_LOuApresearch = False
                print "do_LOuApresearch was changes to be False since the list of frequencies for this data run is greater than 1"

        # LO power
        if biasOnlyMode:
            UCA_list  = ['biasOnlyMode']
            LOuA_list = ['biasOnlyMode']
        elif (do_LOuAsearch and do_LOuApresearch):
            if verboseTop:
                print "Finding SIS pot positions for each SIS current in 'LOuA_list'."
                print "This option is found when do_LOuAsearch and do_LOuApresearch are both True."
                print "This list is discarded if both LO power (LOuA) and LO frequency are both changing in a single run"
            if LOuAsearch_list is None:
                LOuA_list = makeLists(LOuAsearch_start, LOuAsearch_stop, LOuAsearch_step)
            else:
                LOuA_list = LOuAsearch_list

            # set the Electromagnet to a known position
            if do_set_mag_highlow: setmag_highlow(default_magpot)
            else: setmag_only(default_magpot)
            magpot_actual = default_magpot
            if verboseSet:magmsg(magpot_actual)

            # set the SIS pot to a known position
            setSIS_only(default_sispot, feedback_actual, verbose, careful) # set the SIS bias to a known position
            sisPot_actual = default_sispot
            if verboseSet:sismsg(sisPot_actual)

            UCA_list = []
            for LOuA in LOuA_list:
                UCA_actual, deriv_uA_UCAvoltage = LO_PID(uA_set=LOuA, feedback=feedback_actual, verbose=verbose)
                if verboseTop: print "UCA = " + str(UCA_actual) + " V  for LOuA = " + str(LOuA) + " uA"
                elif verboseSet:
                    LOuAmsg(LOuA)
                    UCAmsg(UCA_actual)

        elif (do_LOuAsearch and (do_LOuApresearch == False)):
            if LOuAsearch_list is None:
                LOuA_list = makeLists(LOuAsearch_start, LOuAsearch_stop, LOuAsearch_step)
            else:
                LOuA_list = LOuAsearch_list
            UCA_list  = None
        else:
            LOuA_list = None
            if UCAsweep_list is None:
                UCA_list  = makeLists(UCAsweep_min, UCAsweep_max, UCAsweep_step)
            else:
                UCA_list = UCAsweep_list
        if ((1 < len(LOfreq_list)) and (do_LOuAsearch == False) and (1 < len(UCA_list))):
            print "It is not recommended to step LO frequency and UCA voltage with in the same run."
            print "LO power can change as a function of frequency"
            raw_input("Press Enter to continue, you have been warned")

        # IF bandwidth Center
        if biasOnlyMode:
            IFband_list = ['biasOnlyMode']
        else:
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





        ##############################
        ###### Make directories ######
        ##############################
        # does the datadir exist? If not, we will make it!
        MakeSetDirs(datadir)
        rawdir = datadir + "rawdata/"




    # turn Everything off
    finally:
        if testMode:
            pass
        elif not testMode:
            zeropots(True)
            closetelnet()
            RFoff()
            if not biasOnlyMode:
                disableLabJack()
                # Enable the optical chopper
                if not chopper_off:
                    DisableDrive()

    ##########################
    ###### START SCRIPT ######
    ##########################


    #### make the parameter lists from user specified parameters
    # SIS bias
    # set feedback for the script here












    return