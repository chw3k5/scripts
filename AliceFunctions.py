from biasSweep3 import singleSweepLoop, setYorSnums
from costFunc import cost4Y
from HP437B import setRange
from StepperControl import GoBack
generationNum_str='genNum'

def testGeneration(datadir,K_list,sisPot_str,rangeList,generationSize, population2test,
                   magPot_str, magPotSetVal, UCA_str, UCAsetVal, LOfreq_str, LOfreqSetVal,IF_volt_str,
                   IFvoltSetVal, sisPotSetVal,
                   sisPot_actual,magpot_actual,UCA_actual,LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,
                   sisPot_list,
                   verbose,verboseTop,verboseSet, testMode, chopper_off, Y2get, do_Ynum,PM_range,interation
                   ):
    updatedPopMembers=[]
    ### post list-making initialization
    if sisPot_str in rangeList:
        sisPot_list=[None]
    K_actual=K_list[0]
    resetRange=False
    Ynum,sweepN,rawdir,sisVsweep_trigger = setYorSnums(datadir=datadir,SISpot_List=sisPot_list,do_Ynum=do_Ynum)

    ####################################################
    ###### Start of Receiver Setting Control Loop ######
    ####################################################
    LOuA_actual=None
    param_index = -1
    redoFlag=False
    while True:
        param_index +=1
        if param_index == generationSize:
            break
        ###########################
        ##### Set parameters ######
        ###########################
        popMember = population2test[param_index]
        memberKeys = popMember.keys()
        ### unpack the values from the parameter lists
        if magPot_str in memberKeys:
            magpot_thisloop = popMember[magPot_str]
        else:
            magpot_thisloop = magPotSetVal

        if UCA_str in memberKeys:
            UCA_thisloop = popMember[UCA_str]
        else:
            UCA_thisloop = UCAsetVal
        LOuA_thisloop = None

        if LOfreq_str in memberKeys:
            LOfreq_thisloop = popMember[LOfreq_str]
        else:
            LOfreq_thisloop = LOfreqSetVal

        if IF_volt_str in memberKeys:
            IFband_thisloop = popMember[IF_volt_str]
        else:
            IFband_thisloop = IFvoltSetVal

        for sisPot_temp in sisPot_list:
            if sisPot_str in memberKeys:
                sisPot_thisloop = popMember[sisPot_str]
                sisPot_list2save = [popMember[sisPot_str]]
            elif sisPot_temp is None:
                sisPot_thisloop = sisPotSetVal
                sisPot_list2save = [sisPotSetVal]
            else:
                sisPot_thisloop = sisPot_temp
                sisPot_list2save = sisPot_list

            for K in K_list:
                K_thisloop = K
                K_actual,SISpot_actual,magpot_actual,UCA_actual,LOuA_actual,\
                    LOfreq_actual,IFband_actual,feedback_actual,Ynum,sweepN,resetRange\
                    = singleSweepLoop(rawdir,
                                      K_thisloop,sisPot_thisloop,magpot_thisloop,UCA_thisloop,
                                      LOuA_thisloop,LOfreq_thisloop,IFband_thisloop,
                                      K_actual,sisPot_actual,magpot_actual,UCA_actual,
                                      LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,PM_range,

                                      K_first=K_list[0],sisVsweep_trigger=sisVsweep_trigger,
                                      doing_UCA_list=True,useTHzComputer=True, do_Ynum=do_Ynum,

                                      Ynum=Ynum,sweepN=sweepN,redoFlag=redoFlag,

                                      verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, #careful=False,
                                      sisPot_list2save=sisPot_list2save,
                                      # Parameter sweep behaviour
                                      testMode=testMode, testModeWaitTime=1, chopper_off=chopper_off,
                                      biasOnlyMode=False,
                                      dwellTime_BenchmarkSIS=1,
                                      dwellTime_BenchmarkMag=1,
                                      dwellTime_fastSweep=1,dwellTime_unpumped=1,
                                      dwellTime_sisVsweep=1,

                                      ## Benchmark Tests
                                      # THz computer fast sweeps
                                      do_fastsweep=False, do_unpumpedsweep=False,
                                      fastsweep_feedback=False,
                                      # measure the electromagnet and the SIS junction at their standard positions
                                      benchSISmeasNum=10,benchMAGmeasNum=10,

                                      # mV sweep Parameters
                                      sisV_feedback=True,
                                      SISbiasMeasNum=5,

                                      # Fast sweeps
                                      #fSweepStart=fSweepStart, fSweepStop=fSweepStop, fSweepStep=fSweepStep,

                                      # Powermeter read through LabJack
                                      TPSampleFrequency=100, TPSampleTime=1,

                                      # spectrum analyzer settings
                                      getspecs=False, spec_linear_sc=True,
                                      spec_freq_vector=[0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2],
                                      #spec_sweep_time=spec_sweep_time, spec_video_band=spec_video_band,
                                      #spec_resol_band=spec_resol_band,
                                      #spec_attenu=spec_attenu, lin_ref_lev=lin_ref_lev, aveNum=aveNum,

                                      # Electromagnet Options
                                      do_magisweep=False,
                                      magi_list=None,EmagPotList=None,

                                      # setting the local oscillator pump power
                                      do_LOuAsearch=False,  do_LOuApresearch=False,
                                      LOuA_search_every_sweep=False,
                                      LOuA_list=None,UCA_list=None)


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
                param_index-=1

        popMember['Ynum']=Ynum
        popMember[generationNum_str]=interation
        popMember = cost4Y(popMember,datadir=datadir,Y2get=Y2get,verbose=verbose)
        updatedPopMembers.append(popMember)
    GoBack()
    return  updatedPopMembers