__author__ = 'chwheele'
import numpy, random, time
from biasSweep3 import BiasSweepInit, singleSweepLoop,setYorSnums
from profunc import windir,local_copy,  getSnums, getYnums, getParamDict, getSavedSISpotList,merge_dicts
from domath import make_monotonic
from HP437B import setRange
from costFunc import cost4Y, readCostFile, generateFilenames
from AliceFunctions import testGeneration

"""
This is program created by Caleb Wheeler and Trevor Toland to help with the searching of the parameter space of THz
test receivers. This program is the top level of control code that took 2 years to develop. The idea is that his code
will save a graduate student (or other unsavory worker) from some of the effort needed in making decisions about how
to search the parameter spaces of test receivers. The program is named Alice after Alice in Wonderland. Alice's dream
is to be the greatest graduate student of all time.
"""
testMode=False
warning=False
(verbose,verboseTop,verboseSet)=(True,True,True)
do_inital_search=False
K_list = [295,78]
turnRFoff=False
datadir=windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Alice/')
### map your parameter and watch them dance around the parameters plane

### If a value is not in range list then is has constant value
sisPot_list = []
sisPotSetVal = 59100
magPotSetVal = 100000
UCAsetVal = 0
LOfreqSetVal = 672
IFvoltSetVal = 0

sisPot_str='sisPot'
magPot_str='magPot'
UCA_str='UCA'
LOfreq_str='LOfreq'
IF_volt_str='IF_volt'
generationNum_str='genNum'
costY_str='costY'
rangeList={sisPot_str:(57000,65100),magPot_str:(65100,100000),UCA_str:(0,5,),LOfreq_str:(650,692),IF_volt_str:(0,5)}
dimSize = len(rangeList) # number of dimensions

alivePopNum = 0*dimSize # active breeding population
initPopNum  = alivePopNum
iterMax = 1000 # maximum iterations
F = 0.5 # DE step size [0,2]
CR = 0.7 #  crossover probability  [0, 1]
Y2get = 1.8 # VTR		"Value To Reach" (stop when func < VTR)



chopper_off=False
if len(K_list)<2:chopper_off=True

do_Ynum=False
if 1 < len(K_list):
    do_Ynum=True
# seed the differential evolution algorithm with some new randomly generated data
if do_inital_search:
    initPopulation = []
    for popIndex in range(initPopNum):
        popMemberDict = {}
        for key in rangeList.keys():
            (maxValue,minValue)=rangeList[key]
            if ((key == sisPot_str) or (key == magPot_str)):
                popMemberDict[key]=int(numpy.round((random.random()*abs(maxValue-minValue))+min([maxValue,minValue])))
            else:
                popMemberDict[key]=(random.random()*abs(maxValue-minValue))+min([maxValue,minValue])
        initPopulation.append(popMemberDict)

    ### Turn everything on
    startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
        = BiasSweepInit(verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, warning=warning,#careful=False,
                        testMode=testMode, testModeWaitTime=1, warmmode=False, turnRFoff=turnRFoff,
                        chopper_off=chopper_off, biasOnlyMode=False,
                        sisV_feedback=True)

    population2test=initPopulation
    LOuA_actual=None
    generationSize = alivePopNum
    rawdir = testGeneration(datadir,K_list,sisPot_str,rangeList,generationSize, population2test,
                       magPot_str, magPotSetVal, UCA_str, UCAsetVal, LOfreq_str, LOfreqSetVal,IF_volt_str,
                       IFvoltSetVal, sisPotSetVal,
                       sisPot_actual,magpot_actual,UCA_actual,LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,
                       sisPot_list,
                       verbose,verboseTop,verboseSet, testMode, chopper_off, Y2get, do_Ynum
                       )


# get the population data from the datadir file path
Ynums = None
Snums = None

if do_Ynum:
    Ynums = getYnums(rawdir)
else:
    Snums = getSnums(rawdir)

testedPopulation = []
for Ynum in Ynums:
    hotRawDir, coldRawDir, proYdir = generateFilenames(datadir,Ynum)
    costFile = proYdir+'costFunctionResults.csv'
    hotParamsFile = proYdir+'hotproparams.csv'
    coldParamsFile = proYdir+'coldproparams.csv'
    sisPotListFile = hotRawDir+"sisPoList.csv"

    hotParamDict = getParamDict(hotParamsFile)
    coldParamsDict = getParamDict(coldParamsFile)
    costDict = readCostFile(costFile)

    savedsisPotList = getSavedSISpotList(sisPotListFile)
    memberDict = {sisPot_str:savedsisPotList,
                  magPot_str:hotParamDict['magpot'],
                  UCA_str:hotParamDict['UCA_volt'],
                  LOfreq_str:hotParamDict['LOfreq'],
                  IF_volt_str:hotParamDict['IFband'],
                  'Ynum':Ynum,
                  'proYdir':proYdir,
                  generationNum_str:0}
    memberDict = merge_dicts(memberDict,costDict)
    testedPopulation.append(memberDict)

# rank by lowest to highest 'costY'
Ycosts = [memberDict[costY_str] for memberDict in testedPopulation]
[Ycosts,testedPopulation] = make_monotonic(list_of_lists=[Ycosts,testedPopulation],reverse=False)
print testedPopulation



if not do_inital_search:
    ### Turn everything on
    startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
        = BiasSweepInit(verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, warning=warning,#careful=False,
                        testMode=testMode, testModeWaitTime=1, warmmode=False, turnRFoff=turnRFoff,
                        chopper_off=chopper_off, biasOnlyMode=False,
                        sisV_feedback=True)



# except:
#     raise
#     # This should send some kind of fault email
#     email_caleb('Dead Bias Sweep', 'The Bias sweep script has hit some sort of exception')
#     text_caleb('The Bias sweep script has hit some sort of exception')
# # turn Everything off
# # finally:
#     sweepShutDown(testMode=testMode,biasOnlyMode=biasOnlyMode,chopper_off=chopper_off,turnRFoff=turnRFoff)
#     if FinishedEmail:
#         finishedEmailSender(loopStartTime=loopStartTime,startTime=startTime,emailGroppi=emailGroppi)
#
#
#
#     # end of the giant try statement
#     if (verbose or verboseTop):
#     print "\nThe program Alice has finished her walk"


