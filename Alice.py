__author__ = 'chwheele'
import numpy, random, time
from biasSweep3 import BiasSweepInit, singleSweepLoop,setYorSnums
from profunc import windir,local_copy



"""
This is program created by Caleb Wheeler and Trevor Toland to help with the searching of the parameter space of THz
test receivers. This program is the top level of control code that took 2 years to develop. The idea is that his code
will save a graduate student (or other unsavory worker) from some of the effort needed in making decisions about how
to search the parameter spaces of test receivers. The program is named Alice after Alice in Wonderland. Alice's dream
is to be the greatest graduate student of all time.
"""


turnRFoff=False
datadir=windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Alice/')
### map your parameter and watch them dance around the parameters plane


rangeList=[(57000,65100,'sisPot'),(65100,100000,'magPot'),(0,5,'UCA'),(650,692,'LOfreq'),(3.5,3.5,'IF_volt')]
dimSize = len(rangeList) # number of dimensions

popNumber = 10*dimSize # active breeding population
iterMax = 1000 # maximum iterations
F = 0.5 # DE step size [0,2]
CR = 0.7 #  crossover probabililty  [0, 1]
VTR = 1.e-6 # VTR		"Value To Reach" (stop when func < VTR)

population=numpy.zeros((popNumber,dimSize))
for dimIndex in range(dimSize):
    (dimMax,dimMin,type_str)=rangeList[dimIndex]
    if type_str == 'sisPot':
        pass

    for popIndex in range(popNumber):
        population[popIndex,dimIndex]=(random.random()*abs(dimMin-dimMax))+min([dimMin,dimMax])

print population





### Turn everything on
startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
    = BiasSweepInit(verbose=True, verboseTop=True, verboseSet=True, warning=False,#careful=False,
                    testMode=True, testModeWaitTime=None, warmmode=False, turnRFoff=turnRFoff,
                    chopper_off=False, biasOnlyMode=False,
                    sisV_feedback=True,
                    # stepper motor control options
                    stepper_vel = 0.5, stepper_accel = 1)


# Find the best spot in the initial population



### post list-making initialization
Ynum,sweepN,rawdir,sisVsweep_trigger = setYorSnums(datadir=datadir,SISpot_List=None,do_Ynum=True)

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
                          do_magisweep=do_magisweep, mag_meas=mag_meas,
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
print "\nThe program Alice has finished her walk"


