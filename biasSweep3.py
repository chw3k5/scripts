__author__ = 'chwheele'

import os, sys, numpy, time
# Caleb's Programs
from profunc import windir, local_copy, googleDrive_copy, getYnums, getSnums, getAllparams
from LabJack_control import LabJackU3_DAQ0, LabJackU3_DAQ1, LJ_streamTP,enableLabJack, disableLabJack
from control import  opentelnet, closetelnet, measmag, setmag_only,setmag_highlow, setfeedback, \
    setSIS_only, measSIS_TP, zeropots, mag_channel,\
    default_magpot, default_sispot, default_LOfreq, default_UCA, default_IF, default_PMrange
from StepperControl import EnableDrive, initialize, GoForth, GoBack, DisableDrive, stepper_close
from LOinput import RFon, RFoff, setfreq
from email_sender   import email_caleb, text_caleb
from fastSISsweep   import getfastSISsweep
from getspec import get_multi_band_spec
from PID import SIS_mV_PID, Emag_PID, LO_PID
from HP437B import openHailingFrequencies, closeHailingFrequencies, setRange, range2uW
from biasSweepFunc import MakeSetDirs, makeLists, orderLists,makeparamslist_Rec,  order_lists_around_center,\
    makeparamslist_center, fbmsg, Kmsg, magmsg, sismsg, LOuAmsg, UCAmsg, LOfreqmsg, IFmsg, \
    getSISpotList, getEmagPotList, getLOfreqList, getLOpowList, sweepShutDown, GetTime, \
    sweepUpdateEmail, finishedEmailSender, testPowerRange


def setYorSnums(datadir,SISpot_List,do_Ynum):
    ### post list-making initialization
    # does the datadir exist? If not, we will make it!
    rawdir = MakeSetDirs(datadir)

    # Set the trigger This tells the program it needs to make directories
    sisVsweep_trigger = SISpot_List[0]
    Ynum=None
    sweepN=None

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
        Ynum -=1
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
        sweepN-=1


    return Ynum,sweepN, rawdir, sisVsweep_trigger


def singleSweepLoop(rawdir,
                    K_thisloop,SISpot_thisloop,magpot_thisloop,UCA_thisloop,
                    LOuA_thisloop,LOfreq_thisloop,IFband_thisloop,
                    K_actual,SISpot_actual,magpot_actual,UCA_actual,
                    LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,PM_range,

                    K_first,sisVsweep_trigger,
                    doing_UCA_list,useTHzComputer, do_Ynum,

                    Ynum=0,sweepN=0,redoFlag=False,

                    verbose=True, verboseTop=True, verboseSet=True, #careful=False,
                    sisPot_list2save=None,
                    # Parameter sweep behaviour
                    testMode=True, testModeWaitTime=None, chopper_off=True,
                    biasOnlyMode=False,
                    dwellTime_BenchmarkSIS=None,dwellTime_BenchmarkMag=None,
                    dwellTime_fastSweep=None,dwellTime_unpumped=None,
                    dwellTime_sisVsweep=None,

                    ## Benchmark Tests
                    # THz computer fast sweeps
                    do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
                    # measure the electromagnet and the SIS junction at their standard positions
                    benchSISmeasNum=10,benchMAGmeasNum=5,

                    # mV sweep Parameters
                    sisV_feedback=True,
                    SISbiasMeasNum=5,

                    # Fast sweeps
                    fSweepStart=61000, fSweepStop=65100, fSweepStep=200,

                    # Power meter read through LabJack
                    TPSampleFrequency=100, TPSampleTime=2,

                    # spectrum analyzer settings
                    getspecs=False, spec_linear_sc=True, spec_freq_vector=[],
                    spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30,
                    spec_attenu=0, lin_ref_lev=300, aveNum=1,

                    # Electromagnet Options
                    do_magisweep=False,
                    magi_list=None,EmagPotList=None,

                    # setting the local oscillator pump power
                    do_LOuAsearch=True,  do_LOuApresearch=False, LOuA_search_every_sweep=False,
                    LOuA_list=None,UCA_list=None,

                    # stepper motor control options
                    forth_dist = 0.25, back_dist = 0.25):

    if verboseTop:
        print "K_thisloop      = ", K_thisloop
        print "SISpot_thisloop = ", SISpot_thisloop
        print "magpot_thisloop = ", magpot_thisloop
        if doing_UCA_list:
            print "UCA_thisloop    = ", UCA_thisloop
        else:
            print "LOuA_thisloop   = ", LOuA_thisloop
        print "LOfreq_thisloop = ", LOfreq_thisloop
        print "IFband_thisloop = ", IFband_thisloop

    ######################################################
    ###### Special Setting for different loop modes ######
    ######################################################
    makeBenchmarkSIS=False
    makeBenchmarkMag=False
    fastSweepLoop = False
    unpumpedSweep=False
    resetRange = None
    if SISpot_thisloop == 'benchmarkSIS':
        makeBenchmarkSIS=True
        SISpot_thisloop=default_sispot
        magpot_thisloop=default_magpot
        feedback_thisloop = sisV_feedback
    elif SISpot_thisloop == 'benchmarkMag':
        makeBenchmarkMag=True
        SISpot_thisloop=default_sispot
        magpot_thisloop=default_magpot
        feedback_thisloop = sisV_feedback
    elif SISpot_thisloop == 'fastSweep':
        fastSweepLoop = True
        SISpot_thisloop=default_sispot
        magpot_thisloop=default_magpot
        feedback_thisloop = fastsweep_feedback
    elif SISpot_thisloop == 'unpumpedSweep':
        unpumpedSweep=True
        SISpot_thisloop=default_sispot
        magpot_thisloop=default_magpot
        feedback_thisloop = fastsweep_feedback
        UCA_thisloop = 5
    else:
        feedback_thisloop = sisV_feedback

    #################################################
    ###### Move the chopper K_list (if needed) ######
    #################################################
    if K_thisloop != K_actual:
        if testMode:
            print "Testmode is 'True', pretending to move the chopper"
        else:
            if not chopper_off:
                if K_actual == K_first:
                    GoForth(dist=forth_dist)
                else:
                    GoBack(dist=back_dist)
        K_actual = K_thisloop
        if verboseSet:Kmsg(K_actual)

    ########################################
    ###### Set the Feedback if needed ######
    ########################################
    if feedback_actual != feedback_thisloop:
        if not testMode:
            setfeedback(feedback_thisloop)
        else:
            print "testMode on, pretending to set feedback"
        feedback_actual = feedback_thisloop
        if verboseSet:fbmsg(feedback_actual)
        if testModeWaitTime is not None:time.sleep(testModeWaitTime)



    ##############################################################################
    ###### Set the SIS bias voltage by setting the pot position (if needed) ######
    ##############################################################################
    if not (SISpot_thisloop == SISpot_actual):
        if not testMode:
            setSIS_only(SISpot_thisloop, feedback_actual, verbose, False)
        else:
            print 'testMode on, pretending to set the SIS pot'
        SISpot_actual = SISpot_thisloop
        if verboseSet:
            sismsg(SISpot_actual)
            if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

    ####################################
    ###### Set magnet (if needed) ######
    ####################################
    if not (magpot_thisloop == magpot_actual):
        if not testMode:
            setmag_highlow(magpot_thisloop)
        else:
            print 'testMode on, pretending to set the E-magnet pot'
        magpot_actual = magpot_thisloop
        if verboseSet:
            magmsg(magpot_actual)
            if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

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
        LOuA_actual = LOuA_thisloop
    else:
        if ((not (LOuA_thisloop == LOuA_actual)) or ((LOuA_search_every_sweep) and
            (sisVsweep_trigger == SISpot_thisloop) and (K_actual==K_first))):
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
                    if useTHzComputer:setSIS_only(SISpot_thisloop, feedback_actual, verbose=False, careful=False)
                    SISpot_actual = SISpot_thisloop
                    if verboseSet:sismsg(SISpot_thisloop)
                else:
                    print "Testmode is on, pretending to search for the LO current"
                    UCA_thisloop = "Testmode on, this value would be set by the program 'LO_PID'"

                UCA_actual  = UCA_thisloop
                LOuA_actual = LOuA_thisloop
                if verboseSet:
                    UCAmsg(UCA_actual)
                    LOuAmsg(LOuA_actual)
                    if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)


    ##############################################
    ###### Set the LO frequency (if needed) ######
    ##############################################
    if (not (LOfreq_thisloop == LOfreq_actual)):
        if ((not testMode) and (not biasOnlyMode)):
            setfreq(LOfreq_thisloop)
            if testModeWaitTime is not None:time.sleep(testModeWaitTime)
        else:
            print "Testmode is on, pretending to set frequency to ", LOfreq_thisloop
        LOfreq_actual = LOfreq_thisloop
        if verboseSet:
            LOfreqmsg(LOfreq_actual)
            if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

        if not doing_UCA_list:
            if not testMode:
                UCA_thisloop, deriv_uA_UCAvoltage\
                    = LO_PID(uA_set=LOuA_thisloop, feedback=feedback_actual, verbose=verbose)
                # set the magnet to this loop's position
                if useTHzComputer:setmag_highlow(magpot_thisloop)
                magpot_actual = magpot_thisloop
                if verboseSet:
                    magmsg(magpot_thisloop)
                    if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

                # set the SIS pot to this loop's position
                if useTHzComputer:setSIS_only(SISpot_thisloop, feedback_actual, verbose=False, careful=False)
                SISpot_actual = SISpot_thisloop
                if verboseSet:
                    sismsg(SISpot_thisloop)
                    if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)
            else:
                print "Testmode is on, predending to search for the LO current"
                UCA_thisloop = "Testmode on, this value would be set by the program 'setLOI'"
            UCA_actual = UCA_thisloop


    #####################################
    ####### Set IFband (if needed) ######
    #####################################
    if not IFband_thisloop == IFband_actual:
        LabJackU3_DAQ1(IFband_thisloop)
        IFband_actual = IFband_thisloop
        if verboseSet:IFmsg(IFband_actual)

    #########################################################################
    #########################################################################
    ###### end sweep parameter changes/Start SIS Sweep Data Collection ######
    #########################################################################
    #########################################################################

    #################################################################
    ###### Make the path of the data and write new directories ######
    #################################################################
    if (((SISpot_thisloop==sisVsweep_trigger) or sisVsweep_trigger is None) and (K_first==K_actual)
        and (not any([makeBenchmarkSIS,makeBenchmarkMag, fastSweepLoop,unpumpedSweep]))):
        if verboseTop:
            print "New sweep triggered "
            print SISpot_thisloop, "=  SISpot_thisloop"
            print "making directories"
        if not redoFlag:
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

    if not os.path.isdir(filepath):
        os.makedirs(filepath)



    ####################################
    ###### Write Data Params Data ######
    ####################################
    if (SISpot_thisloop == sisVsweep_trigger or sisVsweep_trigger is None):
        if do_magisweep:
            try:
                magiset = magi_list[EmagPotList.index(magpot_thisloop)]
            except ValueError:
                min_val = 999999.0
                for pot_index in range(len(EmagPotList)):
                    test_val = abs(EmagPotList[pot_index] - magpot_thisloop)
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
        params_filename   = filepath + "params.csv"
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
        params.write('default_sispot,' + str(default_sispot) + '\n')
        params.write('default_magpot,' + str(default_magpot) + '\n')
        params.write('LOfreq,' + str(LOfreq_thisloop) + '\n')
        params.write('IFband,' + str(IFband_thisloop) + '\n')
        params.write('mag_chan,' + str(mag_channel) + '\n')
        params.close()

        ### record the SIS pot list

        if sisPot_list2save is not None:
            saveListFilename   = filepath + "sisPoList.csv"
            h = open(saveListFilename,'w')
            for writePot in sisPot_list2save:
                h.write(str(writePot)+'\n')
            h.close()


    #######################
    ###### Take Data ######
    #######################
    ###### Take Data ######
    #######################
    ###### Take Data ######
    #######################
    if makeBenchmarkSIS:
        sisdata_filename  = filepath + "sisdata.csv"
        ########################################################
        ###### Once per SIS voltage sweep Data Collection ######
        ########################################################
        if ((dwellTime_BenchmarkSIS is not None) and (K_thisloop == K_first)):
            if verboseTop: print 'The benchmark SIS bias measurement is dwelling for '\
                                 +str(dwellTime_BenchmarkSIS)+' seconds'
            time.sleep(dwellTime_BenchmarkSIS)

        # measure the LO power at default magnet and SISpot positions
        # set the bias system to measure relative LO power
        mV_LO_list     = []
        uA_LO_list     = []
        tp_LO_list     = []
        pot_LO_list    = []
        time_stamp_LO_list = []
        if not testMode:
            # measure the SIS junction
            for meas_index in range(benchSISmeasNum):
                sismV_actual, sisuA_actual, sistp, SISpot_actual, time_stamp \
                    = measSIS_TP(default_sispot, feedback_actual, verbose, careful=False)
                mV_LO_list.append(sismV_actual)
                uA_LO_list.append(sisuA_actual)
                tp_LO_list.append(sistp)
                pot_LO_list.append(SISpot_actual)
                time_stamp_LO_list.append(time_stamp)
            if verboseSet:
                LOuAmsg(LOuA_actual)
                UCAmsg(UCA_actual)
        else:
            print "testMode on, pretending to measure the SIS junction to determine LO power"
            if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

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

    elif makeBenchmarkMag:
        magdata_filename  = filepath + "magdata.csv"
        if ((dwellTime_BenchmarkMag is not None) and (K_thisloop == K_first)):
            if verboseTop: print 'The benchmark electromagnet measurement is dwelling for '\
                                 +str(dwellTime_BenchmarkMag)+' seconds'
            time.sleep(dwellTime_BenchmarkMag)

        # Get standard electromagnet data
        V_mag_list   = []
        mA_mag_list  = []
        pot_mag_list = []
        if not testMode:
            # measure the electromagnet
            for meas_index in range(benchMAGmeasNum):
                magV_actual, magmA_actual, magpot_actual = measmag(verbose)
                V_mag_list.append(magV_actual)
                mA_mag_list.append(magmA_actual)
                pot_mag_list.append(magpot_actual)
        else:
            print "testMode on, pretending to measure the magnet"
            if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)

        # record the magnet settings
        magdata = open(magdata_filename, 'w')
        magdata.write('V, mA, pot \n')
        for magi_index in range(len(V_mag_list)):
            V_mag   = V_mag_list[magi_index]
            mA_mag  = mA_mag_list[magi_index]
            pot_mag = pot_mag_list[magi_index]
            magdata.write(str(V_mag) + ',' + str(mA_mag) + ',' + str(pot_mag) +  '\n')
        magdata.close()

    elif fastSweepLoop:
        fast_filename     = filepath + "fastsweep.csv"
        if ((dwellTime_fastSweep is not None) and (K_thisloop == K_first)):
            if verboseTop: print 'The benchmark the fast sweep is dwelling for '\
                                 +str(dwellTime_fastSweep)+' seconds'
            time.sleep(dwellTime_fastSweep)

        # the fast bias sweep
        if do_fastsweep:
            if (testMode):
                pot_fast=[]
                mV_fast=[]
                uA_fast=[]
                tp_fast=[]
                print "testMode on, pretending to do the fast SIS bias sweep"
                if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)
            else:
                pot_fast, mV_fast, uA_fast, tp_fast \
                    = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)

            # record the fast sweep
            fastdata = open(fast_filename, 'w')
            fastdata.write('pot, mV, uA, tp \n')
            for jj in range(len(pot_fast)):
                fastdata.write(str(pot_fast[jj])+','+str(mV_fast[jj])+','+str(uA_fast[jj])+','+str(tp_fast[jj])+'\n')
            fastdata.close()

    elif unpumpedSweep:
        unpumped_filename = filepath + "unpumpedsweep.csv"
        if ((dwellTime_unpumped is not None) and (K_thisloop == K_first)):
            if verboseTop: print 'The benchmark the unpumped sweep is dwelling for '\
                                 +str(dwellTime_unpumped)+' seconds'
            time.sleep(dwellTime_unpumped)
        # a fast bias sweep with the LO fully attenuated (unpumped sweep)
        if do_unpumpedsweep:
            if (testMode or biasOnlyMode):
                pot_unpump=[]
                mV_unpump=[]
                uA_unpump=[]
                tp_unpump=[]
                "testMode or biasOnlyMode on, pretending to take the unpumped fast SIS voltage sweep"
                'pretending to fully attenuate the LO signal'
                if ((testModeWaitTime is not None)):time.sleep(testModeWaitTime)
            else:
                pot_unpump, mV_unpump, uA_unpump, tp_unpump \
                    = getfastSISsweep(fSweepStart, fSweepStop, fSweepStep, verbose)

            # record the unpumped sweep, LO off
            unpumpdata = open(unpumped_filename, 'w')
            unpumpdata.write('pot, mV, uA, tp \n')
            for jj in range(len(pot_unpump)):
                unpumpdata.write(str(pot_unpump[jj])+','+str(mV_unpump[jj])+','+str(uA_unpump[jj])+','+str(tp_unpump[jj])+'\n')
            unpumpdata.close()
    else:
        ###############################################
        ###### SIS voltage sweep Data Collection ######
        ###############################################
        SweepPath = windir(filepath + 'sweep/')
        # TP_filename is determined below in the take data section
        # SIS_bias_filename is determined in the take data section below TP_filename
        # make the folder where sweep data is to be stored
        if not os.path.isdir(SweepPath):
            os.makedirs(SweepPath)

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

        if ((dwellTime_sisVsweep is not None) and (K_thisloop == K_first)):
            if verboseTop: print 'The SIS bias measurement is dwelling for '\
                                 +str(dwellTime_sisVsweep)+' seconds'
            time.sleep(dwellTime_sisVsweep)
        ### SIS Voltage sweep data taking
        if not testMode:
            for meas_index in range(SISbiasMeasNum):
                mV_sweep, uA_sweep, tp_sweep, pot_sweep, time_stamp_sweep \
                    = measSIS_TP(SISpot_thisloop, sisV_feedback, verbose, careful=False)
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
                LJ_streamTP(TP_filename, TPSampleFrequency, TPSampleTime,PM_range=PM_range, verbose=verbose)
        else:
            print "testMode on, pretending to take SIS bias data and the TP measurement"
            if (testMode and (testModeWaitTime is not None)):time.sleep(testModeWaitTime)
            n = open(TP_filename, 'w')
            n.close()
            n = open(spec_filename, 'w')
            n.close()


        ### Write SIS bias data
        sis_sweepData = open(SweepPath + str(step_num) + ".csv", 'w')
        sis_sweepData.write('mV, uA, tp, pot, time \n')
        for sweep_index in range(len(mV_sweep_list)):
            mV_sis     = mV_sweep_list[sweep_index]
            uA_sis     = uA_sweep_list[sweep_index]
            tp_sis     = tp_sweep_list[sweep_index]
            pot_sis    = pot_sweep_list[sweep_index]
            time_stamp = time_stamp_sweep_list[sweep_index]
            meas_line = str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) + ',' + str(pot_sis) + ',' + str(time_stamp)
            sis_sweepData.write(meas_line+'\n')
            if verboseTop:
                print meas_line
        sis_sweepData.close()
        # TP data from the LabJack is written if the 'Take Data' section of the script

        # Test to see if the power meter needs to have its range reset
        TP_filenames=[]
        if do_Ynum:
            if K_first != K_actual:
                TP_filenames.append(TP_filename)
                try:TP_filenames.append(TP_filename.replace('hot','cold'))
                except:TP_filenames.append(TP_filename.replace('cold','hot'))
        else:
            TP_filenames.append(TP_filename)
        if TP_filename != []:
            aveTP = testPowerRange(TP_filenames)
            mWcoeff=range2uW(PM_range)
            mean_TP=numpy.mean(aveTP)
            if mWcoeff < mean_TP:
                resetRange=1
            elif mean_TP < 0.1*mWcoeff:
                resetRange=-1
        # end of the bias sweep loop



    # end of the data taking and writing section of the script


    if (testMode and (testModeWaitTime is not None)):
        print "Loop end"
        time.sleep(testModeWaitTime)

    if any([verbose,verboseSet,verboseTop]):
        print ''





    return K_actual,SISpot_actual,magpot_actual,UCA_actual,LOuA_actual,\
           LOfreq_actual,IFband_actual,feedback_actual,Ynum,sweepN,resetRange


def BiasSweepInit(verbose=True, verboseTop=True, verboseSet=True, warning=False,#careful=False,
                  testMode=True, testModeWaitTime=None, warmmode=False, turnRFoff=True,
                  chopper_off=False, biasOnlyMode=False,
                  sisV_feedback=True,
                  # stepper motor control options
                  stepper_vel = 0.5, stepper_accel = 1):
    ##############################################################################
    ###### Enable some instruments that will be required to make this sweep ######
    ##############################################################################
    if ((testModeWaitTime is not None) and (verboseSet)):time.sleep(testModeWaitTime)
    startTime = time.time()
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
            PM_range = default_PMrange
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
                PM_range = default_PMrange
            else:
                ### Open connection to the LabJack
                enableLabJack()
                # Turn off the UCA voltage (no attenuation)
                LabJackU3_DAQ0(default_UCA)
                UCA_actual = default_UCA
                if verboseSet:UCAmsg(UCA_actual)

                # tune the YIG filter to it default voltage
                LabJackU3_DAQ1(default_IF)
                IFband_actual = default_IF
                if verboseSet:IFmsg(IFband=default_IF)

                ### open communication to the signal generator and set the RF input to prescribed level and frequency
                setfreq(default_LOfreq)
                LOfreq_actual = default_LOfreq
                if verboseSet:LOfreqmsg(LOfreq_actual)

                RFon()
                if verboseSet: print "RF is on"
                # Open communication with the HP437B power meter
                openHailingFrequencies()
                setRange(default_PMrange, verbose=verbose)
                PM_range = default_PMrange
                if verboseSet: print "the HP437B power meter has been set to the default range of:",default_PMrange
                # Communication with the thing that sets the IF band pass would be here
                IFband_actual = default_IF
                if verboseSet:IFmsg(IFband_actual)

                if chopper_off:
                    pass
                else:
                    if warning:
                        raw_input("Place optical chopper in 300K position, hit anything to continue")
                    EnableDrive()
                    initialize(vel=stepper_vel, accel=stepper_accel, verbose=verbose)

    except:
        raise
        sweepShutDown(testMode=testMode,biasOnlyMode=biasOnlyMode,chopper_off=chopper_off,turnRFoff=turnRFoff)
        raise
        # email_caleb('Dead Bias Sweep', 'The Bias sweep script has hit some sort of exception')
        # text_caleb('The Bias sweep script has hit some sort of exception')



    return startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range



def BiasSweep(datadir, verbose=True, verboseTop=True, verboseSet=True, #careful=False,

              # Parameter sweep behaviour
              Kaxis=0, sisVaxis=1, magaxis=2, LOpowaxis=3, LOfreqaxis=4, IFbandaxis=5,
              testMode=True, testModeWaitTime=None, warmmode=False, turnRFoff=False,
              chopper_off=False, biasOnlyMode=False,
              warning=True,
              sweepShape="rectangular",
              dwellTime_BenchmarkSIS=None,dwellTime_BenchmarkMag=None,
              dwellTime_fastSweep=None,dwellTime_unpumped=None,
              dwellTime_sisVsweep=None,

              # email options
              FinishedEmail=False, FiveMinEmail=False, PeriodicEmail=False,
              emailGroppi=False,
              seconds_per_email=1200,

              ## Benchmark Tests
              do_benchmarkSIS=True,
              do_benchmarkMag=True,
              # THz computer fast sweeps
              do_fastsweep=False, do_unpumpedsweep=False, fastsweep_feedback=False,
              SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=100,
              SweepStart_feedFalse=65100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,
              # measure the electromagnet and the SIS juction at their standard positions
              benchSISmeasNum=10,benchMAGmeasNum=5,

              # mV sweep Parameters
              sisV_feedback=True, do_sisVsweep=False,
              sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1, sisVsweep_list=None,
              sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
              sisPot_feedTrue_list=None,
              sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
              sisPot_feedFalse_list=None,
              SISbiasMeasNum=5,

              # Powermeter read through LabJack
              TPSampleFrequency=100, TPSampleTime=2,

              # spectrum analyzer settings
              getspecs=False, spec_linear_sc=True, spec_freq_vector=[],
              spec_sweep_time='AUTO', spec_video_band=10, spec_resol_band=30,
              spec_attenu=0, lin_ref_lev=300, aveNum=1,

              # Chopper temperature list
              K_list=[296,77],

              # Local Ocsillator frequency selector
              LOfreq_start=672, LOfreq_stop=672, LOfreq_step=1,
              LOfreqs_list=None,

              # Intermediate Frequency Band
              IFband_start=1.42, IFband_stop=1.42, IFband_step=0.10,
              IFband_list=None,

              # Electromagnet Options
              do_magisweep=False, mag_meas=10,
              magisweep_start=32, magisweep_stop=32, magisweep_step=1,
              magisweep_list=None,
              magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
              magpotsweep_list=None,

              # setting the local ocsilattor pump power
              do_LOuAsearch=True,  do_LOuApresearch=False, LOuA_search_every_sweep=False,
              UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
              UCAsweep_list=None,
              LOuAsearch_start=14, LOuAsearch_stop=14, LOuAsearch_step=1,
              LOuAsearch_list=None,

              # stepper motor control options
              stepper_vel = 0.5, stepper_accel = 1, forth_dist = 0.25, back_dist = 0.25):
    #import shutil
    #shutil.rmtree(datadir)
    if ((testModeWaitTime is not None) and (verboseSet)):time.sleep(testModeWaitTime)
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

    startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
        = BiasSweepInit(verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, warning=warning,
                        testMode=testMode, testModeWaitTime=testModeWaitTime, warmmode=warmmode, turnRFoff=turnRFoff,
                        chopper_off=chopper_off, biasOnlyMode=biasOnlyMode,
                        sisV_feedback=sisV_feedback,
                        # stepper motor control options
                        stepper_vel=stepper_vel, stepper_accel=stepper_accel)

    ### A shut down procedure is executed at the end of the script not matter what exceptions are raised
    # try:
    if True:
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
        if do_benchmarkSIS:
            SISpot_List.append('benchmarkSIS')
        if do_benchmarkMag:
            SISpot_List.append('benchmarkMag')
        if do_fastsweep:
            SISpot_List.append('fastSweep')
        if do_unpumpedsweep:
            SISpot_List.append('unpumpedSweep')




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
            if IFband_list is None:
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
        Ynum,sweepN,rawdir,sisVsweep_trigger = setYorSnums(datadir,SISpot_List,do_Ynum)

        ####################################################
        ###### Start of Receiver Setting Control Loop ######
        ####################################################
        LOuA_actual=None
        loopStartTime = time.time()
        emailTime = loopStartTime
        param_index = -1
        redoFlag=False
        while True:
            param_index +=1
            if param_index == list_len:
                break
        ###########################
        ##### Set parameters ######
        ###########################
            ### unpack the values from the parameter lists
            K_thisloop      = master_K_list[param_index]
            sisPot_thisloop = master_sisPot_list[param_index]
            magpot_thisloop = master_magpot_list[param_index]
            if doing_UCA_list:
                UCA_thisloop    = master_UCA_list[param_index]
                LOuA_thisloop = None
            else:
                LOuA_thisloop   = master_LOuA_list[param_index]
                UCA_thisloop = None

            LOfreq_thisloop = master_LOfreq_list[param_index]
            IFband_thisloop = master_IFband_list[param_index]



            K_actual,SISpot_actual,magpot_actual,UCA_actual,LOuA_actual,\
                LOfreq_actual,IFband_actual,feedback_actual,Ynum,sweepN,resetRange\
                = singleSweepLoop(rawdir,
                                  K_thisloop,sisPot_thisloop,magpot_thisloop,UCA_thisloop,
                                  LOuA_thisloop,LOfreq_thisloop,IFband_thisloop,
                                  K_actual,sisPot_actual,magpot_actual,UCA_actual,
                                  LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,PM_range,

                                  K_first,sisVsweep_trigger,
                                  doing_UCA_list,useTHzComputer, do_Ynum,

                                  Ynum=Ynum,sweepN=sweepN,redoFlag=redoFlag,

                                  verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, #careful=False,

                                  # Parameter sweep behaviour
                                  testMode=testMode, testModeWaitTime=testModeWaitTime, chopper_off=chopper_off,
                                  biasOnlyMode=biasOnlyMode,
                                  dwellTime_BenchmarkSIS=dwellTime_BenchmarkSIS,
                                  dwellTime_BenchmarkMag=dwellTime_BenchmarkMag,
                                  dwellTime_fastSweep=dwellTime_fastSweep,dwellTime_unpumped=dwellTime_unpumped,
                                  dwellTime_sisVsweep=dwellTime_sisVsweep,

                                  ## Benchmark Tests
                                  # THz computer fast sweeps
                                  do_fastsweep=do_fastsweep, do_unpumpedsweep=do_unpumpedsweep,
                                  fastsweep_feedback=fastsweep_feedback,
                                  # measure the electromagnet and the SIS junction at their standard positions
                                  benchSISmeasNum=benchSISmeasNum,benchMAGmeasNum=benchMAGmeasNum,

                                  # mV sweep Parameters
                                  sisV_feedback=sisV_feedback,
                                  SISbiasMeasNum=SISbiasMeasNum,

                                  # Fast sweeps
                                  fSweepStart=fSweepStart, fSweepStop=fSweepStop, fSweepStep=fSweepStep,

                                  # Powermeter read through LabJack
                                  TPSampleFrequency=TPSampleFrequency, TPSampleTime=TPSampleTime,

                                  # spectrum analyzer settings
                                  getspecs=getspecs, spec_linear_sc=spec_linear_sc, spec_freq_vector=spec_freq_vector,
                                  spec_sweep_time=spec_sweep_time, spec_video_band=spec_video_band,
                                  spec_resol_band=spec_resol_band,
                                  spec_attenu=spec_attenu, lin_ref_lev=lin_ref_lev, aveNum=aveNum,

                                  # Electromagnet Options
                                  do_magisweep=do_magisweep,
                                  magi_list=magi_list,EmagPotList=EmagPotList,

                                  # setting the local oscillator pump power
                                  do_LOuAsearch=do_LOuAsearch,  do_LOuApresearch=do_LOuApresearch,
                                  LOuA_search_every_sweep=LOuA_search_every_sweep,
                                  LOuA_list=LOuA_list,UCA_list=UCA_list,

                                  # stepper motor control options
                                  forth_dist = forth_dist, back_dist = back_dist)

            redoFlag=False
            if resetRange is not None:
                new_PM_range=PM_range+resetRange
                if new_PM_range in [1,2,3,4,5]:
                    setRange(new_PM_range,verbose=verboseSet)
                    PM_range=new_PM_range
                    redoFlag=True
                elif new_PM_range == 0:
                    print "The most sensitive range of the power meter is currently set,"+\
                          " the range lowering flag will be ignored."
                elif new_PM_range == 6:
                    print "The highest power range of the power meter is currently set,"+\
                          " you my be damaging the power meter, add attenuators"

            if redoFlag:
                if do_Ynum:
                    param_index-=2
                else:
                    param_index-=1

            ######################################
            ###### Email part of the script ######
            ######################################
            emailTime = sweepUpdateEmail(loopStartTime=loopStartTime,loopsComplete=param_index+1,
                                         totalLoops=list_len,emailTime=emailTime,
                                         seconds_per_email=seconds_per_email,
                                         startTime=startTime,verbose=verboseTop,
                                         FiveMinEmail=FiveMinEmail,
                                         PeriodicEmail=PeriodicEmail,
                                         emailGroppi=emailGroppi)
    # except:
    #     raise
    #     # This should send some kind of fault email
    #     email_caleb('Dead Bias Sweep', 'The Bias sweep script has hit some sort of exception')
    #     text_caleb('The Bias sweep script has hit some sort of exception')
    # # turn Everything off
    # finally:
        sweepShutDown(testMode=testMode,biasOnlyMode=biasOnlyMode,chopper_off=chopper_off,turnRFoff=turnRFoff)
        if FinishedEmail:
            finishedEmailSender(loopStartTime=loopStartTime,startTime=startTime,emailGroppi=emailGroppi)



    # end of the gaint try statement
    if (verbose or verboseTop):
        print "\nThe program BaisSweep.py has reached its end, congratulations!"

    return


def rerunY(proYdatadir,rerunDir,turnRFoff=True, doEmail=False,verbose=True, verboseTop=True, verboseSet=True):


    paramTuple = getAllparams(paramsFile=proYdatadir+'hotproparams.csv')
    (K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V,
        meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,LOuA_set_pot,
        LOuA_magpot, meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp,
        stdSIS_tp, SIS_pot, del_time, LOfreq, IFband, meas_num,
        TP_int_time, TP_num, TP_freq, mag_chan) = paramTuple

    print '\nDoing a Rerun for the following values:'
    print 'magpot:',magpot,' UCA voltage:',UCA_volt,' IFband voltage:', IFband, ' LO frequency:',LOfreq

    BiasSweep(rerunDir, verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet,

        # Parameter sweep behaviour
        Kaxis=0, sisVaxis=1, magaxis=3, LOpowaxis=2, LOfreqaxis=4, IFbandaxis=5,
        testMode=False, testModeWaitTime=1, warmmode=False, turnRFoff=turnRFoff,
        chopper_off=False, biasOnlyMode=False,
        warning=False,
        sweepShape="rectangular",
        dwellTime_BenchmarkSIS=2,
        dwellTime_BenchmarkMag=2,
        dwellTime_fastSweep=2,
        dwellTime_unpumped=2,
        dwellTime_sisVsweep=1,

        # email options
        FinishedEmail=doEmail, FiveMinEmail=doEmail, PeriodicEmail=doEmail,
        emailGroppi=False,
        seconds_per_email=1200,

        ## Benchmark Tests
        do_benchmarkSIS=True,
        do_benchmarkMag=True,
        # measure the electromagnet and the SIS junction at their standard positions
        benchSISmeasNum=10,benchMAGmeasNum=5,
        # THz computer fast sweeps
        do_fastsweep=True, do_unpumpedsweep=False, fastsweep_feedback=False,
        SweepStart_feedTrue=65000, SweepStop_feedTrue=52000, SweepStep_feedTrue=500,
        SweepStart_feedFalse=66100, SweepStop_feedFalse=57000, SweepStep_feedFalse=100,

        # mV sweep Parameters
        sisV_feedback=True, do_sisVsweep=False, SISbiasMeasNum=5,
        sisVsweep_start=-0.1, sisVsweep_stop=2.5, sisVsweep_step=0.1,
        sisVsweep_list=None,
        sisPot_feedFalse_start=65100, sisPot_feedFalse_stop=57000, sisPot_feedFalse_step=100,
        sisPot_feedTrue_list=[63518,  63140, 62762, 62384,
                            62006,  61628, 61250, 60872,
                            60393,  59924, 59461, 59039,
                            58549,  58111, 57638, 57173,
                            56775],

        # [65430, 65491, 65037, 64949, 64774, 64697, 64571, 64480,
        #                       61250, 61127, 60872, 60581, 60393, 60125, 59924, 59684,
        #                       59461, 59223, 59039, 58831, 58549, 58345, 58111, 57879, 57638, 57418, 57173, 56987,
        #                       56775, 56525, 56299, 56052, 55826, 55582, 55369, 55123, 54955, 54732, 54471, 54247, 54013]
        sisPot_feedTrue_start=65000, sisPot_feedTrue_stop=52000, sisPot_feedTrue_step=100,
        sisPot_feedFalse_list=None,

        # Powermeter read through LabJack
        TPSampleFrequency=100, TPSampleTime=1,

        # spectrum analyzer settings
        getspecs=False, spec_linear_sc=True, spec_freq_vector=[0.0,0.4,1.0,1.6,2.2,2.5,2.8,3.1,3.4,4.0,4.6,5.2,6.4,12.4,24.4],
        spec_sweep_time='AUTO', spec_video_band=300, spec_resol_band=300,
        spec_attenu=0, lin_ref_lev=500, aveNum=64,

        # Chopper temperature list
        K_list=[296,78],

        # Local Ocsillator frequency selector
        LOfreq_start=650, LOfreq_stop=692, LOfreq_step=1,
        LOfreqs_list=[LOfreq],

        # Intermediate Frequency Band
        IFband_start=IFband, IFband_stop=IFband, IFband_step=0.10,

        # Electromagnet Options
        do_magisweep=False, mag_meas=10,
        magisweep_start=32, magisweep_stop=32, magisweep_step=1,
        magisweep_list=None,
        magpotsweep_start=40000, magpotsweep_stop=40000, magpotsweep_step=5000,
        magpotsweep_list=[magpot],

        # setting the local ocsilattor pump power
        do_LOuAsearch=False,  do_LOuApresearch=False, LOuA_search_every_sweep=False,
        UCAsweep_min=3.45, UCAsweep_max=3.45, UCAsweep_step=0.05,
        UCAsweep_list=[UCA_volt],
        LOuAsearch_start=14, LOuAsearch_stop=14, LOuAsearch_step=1,
        LOuAsearch_list=[16],

        # stepper motor control options
        stepper_vel = 0.5, stepper_accel = 1, forth_dist = 0.25, back_dist = 0.25)


    return



def rerunFromList(rerunFile='/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/foundYfiles/rerun.csv'):
    rerunFile = local_copy(windir(rerunFile))
    with open(rerunFile,'r') as reRunHandle:
        sweeps2rerun=reRunHandle.read().splitlines()
    lastIndex=len(sweeps2rerun)-1
    for (listIndex,proYdatadir) in list(enumerate(sweeps2rerun)):
        (parentDir,junk)=proYdatadir.split('prodata')
        parentDir = googleDrive_copy(parentDir)
        rerunDir = windir(parentDir+'rerun/')
        turnRFoff = False
        if lastIndex == listIndex:
            turnRFoff = True
        rerunY(proYdatadir,rerunDir,turnRFoff=turnRFoff,verbose=False)
    return








if __name__ == "__main__":
    # rerunY(proYdatadir='C:\\Users\\chwheele\\local_kappa_data\\Kappa\NA38\\IVsweep\\Alice\\LOfreq650-655\\prodata\\Y0004\\',
    #        rerunDir='C:\\Users\\chwheele\\local_kappa_data\\Kappa\NA38\\IVsweep\\Alice\\LOfreq650-655\\rerun\\')
    rerunFromList()



