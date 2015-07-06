__author__ = 'chwheele'
import numpy, random, time
from biasSweep3 import BiasSweepInit, singleSweepLoop,setYorSnums, sweepShutDown
from profunc import windir,local_copy,  getSnums, getYnums, getParamDict, getSavedSISpotList, merge_dicts
from domath import make_monotonic
from HP437B import setRange
from costFunc import cost4Y, readCostFile, generateFilenames
from AliceFunctions import testGeneration
from diffEvo import differentialEvolution

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
do_inital_search=True
survivalOrFittest=False
K_list = [295,78]
turnRFoff=False

### map your parameter and watch them dance around the parameters plane

### If a value is not in range list then is has constant value
sisPotSetVal = 59100
sisPot_list = [sisPotSetVal]
magPotSetVal = 100000
UCAsetVal = 3.09831892665
LOfreqSetVal =  671.986
IFvoltSetVal = 4

sisPot_str='sisPot'
magPot_str='magPot'
UCA_str='UCA'
LOfreq_str='LOfreq'
IF_volt_str='IF_volt'
generationNum_str='genNum'
costY_str='costY'

LOfreq_vector = range(655,692,5)
firstLoop=True
for freqIndex in range(len(LOfreq_vector)-1):
    LOfreqMin=LOfreq_vector[freqIndex]
    LOfreqMax=LOfreq_vector[freqIndex+1]
    #rangeList={sisPot_str:(57000,65100),magPot_str:(65100,100000),),LOfreq_str:(650,692),IF_volt_str:(0,5)}
    rangeList={sisPot_str:(57800,59300),magPot_str:(78000,81000),LOfreq_str:(LOfreqMin,LOfreqMax),IF_volt_str:(0,5),UCA_str:(0,5)}
    datadir=windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Alice/LOfreq'+str(LOfreqMin)+'-'+str(LOfreqMax)+'/')

    dimSize = len(rangeList) # number of dimensions

    generationSize = 10*dimSize # active breeding population
    initPopNum  = max(generationSize+10,40)
    interationMax = 6 # maximum iterations
    F = 0.5 # DE step size [0,2]
    crossOverProb = 0.8 #  crossover probability  [0, 1]
    Y2get = 2.0 # VTR		"Value To Reach" (stop when func < VTR)
    strategyDE = 2 # [1,2,3,4,5] are the options
    euthanizeGrandPaAfter = 3


    interation = 0

    chopper_off=False
    if len(K_list)<2:chopper_off=True

    rawdir=datadir+'rawdata/'

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
        if firstLoop:
            startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
                = BiasSweepInit(verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, warning=warning,#careful=False,
                                testMode=testMode, testModeWaitTime=1, warmmode=False, turnRFoff=turnRFoff,
                                chopper_off=chopper_off, biasOnlyMode=False,
                                sisV_feedback=True)

        population2test=initPopulation
        LOuA_actual=None
        updatedPopMembers\
            = testGeneration(datadir,K_list,sisPot_str,rangeList,initPopNum, population2test,
                           magPot_str, magPotSetVal, UCA_str, UCAsetVal, LOfreq_str, LOfreqSetVal,IF_volt_str,
                           IFvoltSetVal, sisPotSetVal,
                           sisPot_actual,magpot_actual,UCA_actual,LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,
                           sisPot_list,
                           verbose,verboseTop,verboseSet, testMode, chopper_off, Y2get, do_Ynum,PM_range,interation
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
                      generationNum_str:interation}
        memberDict = merge_dicts(memberDict,costDict)
        testedPopulation.append(memberDict)

    # rank by lowest to highest 'costY'
    Ycosts = [memberDict[costY_str] for memberDict in testedPopulation]
    [Ycosts,testedPopulation] = make_monotonic(list_of_lists=[Ycosts,testedPopulation],reverse=False)

    if generationSize < len(testedPopulation):
        parentPopulation=testedPopulation[:generationSize]
    else:
        parentPopulation = testedPopulation

    allPopulation = testedPopulation


    if (not do_inital_search and firstLoop):
        ### Turn everything on
        startTime,feedback_actual,magpot_actual,sisPot_actual,UCA_actual,LOfreq_actual,IFband_actual,PM_range\
            = BiasSweepInit(verbose=verbose, verboseTop=verboseTop, verboseSet=verboseSet, warning=warning,#careful=False,
                            testMode=testMode, testModeWaitTime=1, warmmode=False, turnRFoff=turnRFoff,
                            chopper_off=chopper_off, biasOnlyMode=False,
                            sisV_feedback=True)


    #########################################
    ### Great differential evolution loop ###
    #########################################

    while interation <= interationMax:
        interation+=1
        print "##########################"
        print "###### Generation "+str(interation)+" ######"
        print "##########################"
        time.sleep(5)
        # the best population should be the first member of the list
        mutantPop,parentPopulation \
            = differentialEvolution(parentPopulation,rangeList,crossOverProb=crossOverProb,strategy=strategyDE,F=F)

        LOuA_actual=None
        testedMutantPop = \
            testGeneration(datadir,K_list,sisPot_str,rangeList,generationSize, mutantPop,
                           magPot_str, magPotSetVal, UCA_str, UCAsetVal, LOfreq_str, LOfreqSetVal,IF_volt_str,
                           IFvoltSetVal, sisPotSetVal,
                           sisPot_actual,magpot_actual,UCA_actual,LOuA_actual,LOfreq_actual,IFband_actual,feedback_actual,
                           sisPot_list,
                           verbose,verboseTop,verboseSet, testMode, chopper_off, Y2get, do_Ynum,PM_range,interation)


        # rank by lowest to highest 'costY'
        if survivalOrFittest:
            Ycosts = [memberDict[costY_str] for memberDict in testedMutantPop]
            [Ycosts,testedMutantPop] = make_monotonic(list_of_lists=[Ycosts,testedMutantPop],reverse=False)
        else:
            newParentList=[]
            for popIndex in range(generationSize):
                parentMember=parentPopulation[popIndex]
                mutantMember=testedMutantPop[popIndex]
                mutantMember[generationNum_str]=interation

                parentYcost = parentMember[costY_str]
                mutantYcost = mutantMember[costY_str]

                parentGenNum = parentMember[generationNum_str]
                mutantGenNum = mutantMember[generationNum_str]

                genDiff = mutantGenNum-parentGenNum
                if verboseTop: print "parentYcost:",parentYcost,'  mutantYcost:',mutantYcost
                if ((mutantYcost < parentYcost) or (euthanizeGrandPaAfter <= genDiff)):
                    newParentList.append(mutantMember)
                    if verboseTop: print "Mutant Replaces Parent"
                else:
                    newParentList.append(parentMember)
        parentPopulation = newParentList
    firstLoop=False


# except:
#     raise
#     # This should send some kind of fault email
#     email_caleb('Dead Bias Sweep', 'The Bias sweep script has hit some sort of exception')
#     text_caleb('The Bias sweep script has hit some sort of exception')
# # turn Everything off
# # finally:
sweepShutDown(testMode=testMode,biasOnlyMode=False,chopper_off=True,turnRFoff=turnRFoff)
# if FinishedEmail:
#     finishedEmailSender(loopStartTime=loopStartTime,startTime=startTime,emailGroppi=emailGroppi)

#
#
#     # end of the giant try statement
#     if (verbose or verboseTop):
#     print "\nThe program Alice has finished her walk"


