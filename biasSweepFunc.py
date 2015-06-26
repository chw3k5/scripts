__author__ = 'chwheele'
import os, numpy, sys, time
from control import default_magpot, default_sispot, default_LOfreq, default_UCA,\
    setfeedback, setSIS, setmag_highlow, setSIS_only, zeropots, closetelnet
from LOinput import RFoff
from LabJack_control import LabJackU3_DAQ0, disableLabJack
from StepperControl import DisableDrive, stepper_close
from profunc import windir
from PID import SIS_mV_PID, Emag_PID, LO_PID
from datetime import datetime, timedelta
from email_sender import email_caleb, email_groppi

def GetTime(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1,1,1) + sec
    #"DAYS:HOURS:MIN:SEC"
    time_str="%d days : %d hours : %d minutes : %d seconds" % (d.day-1, d.hour, d.minute, d.second)
    return time_str

def sweepUpdateEmail(loopStartTime,loopsComplete,totalLoops,emailTime,
                     seconds_per_email=1200,
                     startTime=None,verbose=False,
                     FiveMinEmail=False,PeriodicEmail=False,emailGroppi=False):
    EmailTrigger = False
    nowTime       = time.time()
    loopElapsedTime   = nowTime - loopStartTime
    if startTime is not None:
        totalElapsedTime = nowTime - startTime
        totalElapsedTime_str = GetTime(totalElapsedTime)
    else:
        totalElapsedTime_str = None
    remainingTime = (loopElapsedTime/(loopsComplete+1))*(totalLoops-(loopsComplete))
    finishTime = nowTime+remainingTime
    loopElapsedTime_str = GetTime(loopElapsedTime)
    remainingTime_str = GetTime(remainingTime)
    localFinishTime_str = time.strftime('%d   %H : %M : %S', time.localtime(finishTime))
    if verbose:
        print 'The sweep loop elapsed time:',loopElapsedTime_str
        if totalElapsedTime_str is not None:print 'The total elapsed time:     ',totalElapsedTime_str
        print 'The remaining time:         ', remainingTime_str
        print 'The estimated Finish time:  ',localFinishTime_str
    # Email Options
    if FiveMinEmail:
        if 300 <= int(loopElapsedTime):
            EmailTrigger = True
            FiveMinEmail = False
    if PeriodicEmail:
        ElapsedEmailTime = nowTime - emailTime
        if seconds_per_email < ElapsedEmailTime:
            EmailTrigger = True

    if EmailTrigger:
        if totalElapsedTime_str is not None:email_str = 'The total elapsed time\n' +totalElapsedTime_str + '\n\n'
        else: email_str=''
        email_str += 'The sweep loop elapsed time\n' + loopElapsedTime +'\n\n'
        email_str += 'The remaining time\n'+ remainingTime_str + '\n\n'
        email_str += 'The estimated Finish time\n'+localFinishTime_str

        email_caleb('Bias Sweep Update', email_str)
        if emailGroppi:
            email_groppi('Bias Sweep Update', email_str)
        EmailTime = nowTime
    return emailTime

def finishedEmailSender(loopStartTime,startTime=None,emailGroppi=False):
    nowTime       = time.time()
    loopElapsedTime   = nowTime - loopStartTime
    if startTime is not None:
        totalElapsedTime = nowTime - startTime
        totalElapsedTime_str = GetTime(totalElapsedTime)
    else:
        totalElapsedTime_str = None

    loopElapsedTime_str = GetTime(loopElapsedTime)

    localFinishTime_str = time.strftime('%d %H:%M:%S', time.localtime(nowTime))
    email_str = 'The Finish time\n'+localFinishTime_str +'\n\n'
    if totalElapsedTime_str is not None:email_str += 'The total elapsed time\n' +totalElapsedTime_str + '\n\n'
    email_str += 'The sweep loop elapsed time\n' + loopElapsedTime_str +'\n\n'
    email_str += "The program BaisSweep.py has reached its end, congratulations!"
    email_caleb('Bias Sweep Finished '+localFinishTime_str, email_str)
    if emailGroppi:
        email_groppi('Bias Sweep Finished on: '+localFinishTime_str, email_str)
    return

def sweepShutDown(testMode=False,biasOnlyMode=False,chopper_off=False,turnRFoff=True):
    print '\nEntering shut down sequence'
    if testMode:
        print 'testMode is on, there is nothing to shut down'
    else:
        print 'zeroing the THz computer potentiometers'
        zeropots(True)
        print 'closing THz computer connection'
        closetelnet()
        if not biasOnlyMode:
            if turnRFoff:
                print 'turning off the signal generators output'
                RFoff()
            else:
                print "THE RF SIGNAL IS STILL ON!"
            print 'closing LabJack connection'
            disableLabJack()
            if not chopper_off:
                print 'Turning off the stepper drive'
                DisableDrive()
                print 'closing connection to stepper motor controller'
                stepper_close()
    print '\nshut down dance complete'
    return


def MakeSetDirs(datadir):
    # does the datadir exist? If not, we will make it!
    datadir    = windir(datadir)
    rawdatadir = windir(datadir+'rawdata/')
    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    if not os.path.isdir(rawdatadir):
        os.makedirs(rawdatadir)
    return rawdatadir

def makeLists(start, stop, step):
    step = abs(step)
    newlist = []
    if start < stop:
        if (isinstance(start, int) and isinstance(stop, int) and isinstance(step, int)):
            newlist = range(start, stop, step)
        else:
            newlist = list(numpy.arange(start, stop, step))
    elif stop < start:
        step = step*-1
        if (isinstance(start, int) and isinstance(stop, int) and isinstance(step, int)):
            newlist = range(start, stop, step)
        else:
            newlist = list(numpy.arange(start, stop, step))
    elif start == stop:
        newlist = [start]
    return newlist

def orderLists(master_list_input):
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
            print "The function orderLists needs a list of tuples\n"+ \
            "with each tuple containing (int, list). Something other than an int\n"+ \
            "was found: ", axis_num

        if isinstance(single_list, list):
            unordered_lists.append(single_list)
        else:
            print "The function orderLists needs a list of tuples\n"+\
            "with each tuple containing (int, list). Something other than a list\n"+ \
            "was found: ", single_list

    for n in range(num_of_lists):
        axis_num_count = axis_list.count(n)
        if axis_num_count == 1:
            pass
        elif axis_num_count < 1:
            print "In the function oderLists the axis: ", n, " is not listed."
            print " Axis_nums should start with 0 and increment by one with each", \
            "axis having a unique number"
            print "see axis_list:", axis_list
        elif 1 < axis_num_count:
            print "In the function oderLists the axis: ", n, " appears ", \
            axis_num_count, " times, it should be unique."
            print " Axis_nums should start with 0 and increment by one with each", \
            "axis having a unique number"
            print "see axis_list:", axis_list

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

def order_lists_around_center(the_list):

    reordered_list = []
    #the_array = numpy.array(the_list)
    list_center = abs(the_list[0]+the_list[-1])/2.0
    diff_from_center = list(the_list-list_center)
    for diff_val in sorted(diff_from_center):
        val_index = diff_from_center.index(diff_val)
        reordered_list.append(the_list[val_index])
    return reordered_list

def makeparamslist_center(lists):
    master_lists = []
    listn = lists[0]
    listn_len = len(listn)
    for a_list in lists:
        ordered_list = order_lists_around_center(a_list)
        #ordered_lists.ordered

    return master_lists

def fbmsg(feedback):
    print "Feedback has been set to: " , str(feedback)
    return

def Kmsg(Kval):
    try:
        str_val = str(float(Kval))
    except TypeError:
        str_val = Kval
    print "The chopper should be set for " , str_val , " K"
    return

def magmsg(magpot):
    try:
        str_val = str('%06.0f' % float(magpot))
    except TypeError:
        print magpot,
        str_val = magpot
    if int(magpot) == int(default_magpot):
         print "The SIS bias pot has ben set the default value: " , str_val
    else:
        print "The magnet pot has ben set to: " , str_val
    return

def sismsg(sisPot):
    try:
        str_val = str('%06.0f' % float(sisPot))
        if int(sisPot) == int(default_sispot):
             print "The SIS bias pot has ben set the default value: " , str_val
        else:
            print "The SIS bias pot has ben set to: " , str_val
    except TypeError:
        str_val = sisPot
        print "The SIS bias pot has ben set to: " , str_val
    except ValueError:
        str_val = sisPot
        print "The SIS bias pot has ben set to: " , str_val

    return

def LOuAmsg(LOuA):
    try:
        str_val = str('%2.3f' % LOuA)
    except TypeError:
        str_val = LOuA
    print "The LO current has been set to " , str_val , "uA"
    return

def UCAmsg(UCA):
    try:
        str_val = str('%1.4f' % UCA)
    except TypeError:
        str_val = UCA
    print "The UCA Voltage has been set to " , str_val , "V"
    return

def LOfreqmsg(freq):
    try:
        str_val = str('%3.3f' % freq)
    except TypeError:
        str_val = freq
    print "The LO frequency has be set to " , str_val , "GHz"
    return

def IFmsg(IFband):
    try:
        str_val = str('%1.4f' % IFband)
    except TypeError:
        str_val = IFband
    print "The IF band width has been set to " , str_val , "GHz"
    return

def getSISpotList(sisV_feedback,useTHzComputer=False,
                  do_sisVsweep=False, verbose=False, verboseTop=False, verboseSet=False,
                  sisVsweep_list=None,
                  sisVsweep_start=1.3, sisVsweep_stop=1.3, sisVsweep_step=0.1,
                  sisPot_feedTrue_list=None,
                  sisPot_feedTrue_start=59100, sisPot_feedTrue_stop=59100, sisPot_feedTrue_step=100,
                  sisPot_feedFalse_list=None,
                  sisPot_feedFalse_start=64000, sisPot_feedFalse_stop=64000, sisPot_feedFalse_step=200
                  ):
    SISpot_List=[]

    # set the feedback
    if useTHzComputer:setfeedback(feedback=sisV_feedback)
    feedback_actual = sisV_feedback
    if verboseSet:fbmsg(feedback_actual)

    # set the magnet to default position
    if useTHzComputer:setmag_highlow(default_magpot)
    magpot_actual = default_magpot
    if verboseSet:magmsg(magpot_actual)

    # This mode takes a list of voltages and uses a PID program to find the corresponding pot positions
    if do_sisVsweep:
        if useTHzComputer:
            print "The SIS voltage Sweep is not available in test mode, select something else or turn off test mode"
            print "Initiating systems shutdown"
            sweepShutDown()
            sys.exit()
        if verboseTop: print "Finding SIS pot positions for each magnet Voltage in 'sisV_list'."
        if sisVsweep_list is not None:
            sisV_list = sisVsweep_list
        else:
            sisV_list = makeLists(sisVsweep_start, sisVsweep_stop, sisVsweep_step)
        SISpot_List = []
        first_pot=65100
        deriv_mV_sispot = 1
        mV_first = 0
        sismV_first = sisV_list[0]
        len_sisV_list_str = str(len(sisV_list))
        for sismV in sisV_list:
            if sismV_first == sismV:
                second_pot=56800
            else:
                mV_diff = mV_first-sismV
                second_pot = first_pot + mV_diff/deriv_mV_sispot
            if verboseTop:
                print str(sisV_list.index(sismV)+1)+" of "+len_sisV_list_str+\
                      "  Finding the potentiometer position for the sis bias voltage of " +\
                      str('%1.3f' % sismV) + 'mV'
            sisPot_actual, deriv_mV_sispot = SIS_mV_PID(mV_set=sismV,
                                                        feedback=feedback_actual,
                                                        sleep_per_set=2, meas_number=5,
                                                        min_diff_sispot=5,
                                                        first_pot=first_pot, second_pot=second_pot,
                                                        verbose=verbose)
            SISpot_List.append(sisPot_actual)
            if verboseSet: sismsg(sisPot_actual)
            first_pot = sisPot_actual
            mV_first = sismV

    # This mode just makes list of SIS pot positions based on a specified range of pot positions
    else:
        sisV_list = None
        if sisV_feedback:
            if sisPot_feedTrue_list is not None:
                SISpot_List = sisPot_feedTrue_list
            else:
                SISpot_List = makeLists(sisPot_feedTrue_start, sisPot_feedTrue_stop, sisPot_feedTrue_step)
        else:
            if sisPot_feedFalse_list is not None:
                SISpot_List=sisPot_feedFalse_list
            else:
                SISpot_List = makeLists(sisPot_feedFalse_start, sisPot_feedFalse_stop, sisPot_feedFalse_step)
    # round the sisPot list to integers, this is needed comparisons to triggers later on in the script
    for Pot_index in range(len(SISpot_List)):
        SISpot_List[Pot_index] = int(round(SISpot_List[Pot_index]))

    # set the SIS pot to the default position
    if useTHzComputer:setSIS_only(default_sispot, feedback_actual, verbose=False, careful=False)
    sisPot_actual = default_sispot
    if verboseSet:sismsg(sisPot_actual)

    SISpot_List = list(SISpot_List)
    return SISpot_List, feedback_actual, sisPot_actual, magpot_actual

def getEmagPotList(useTHzComputer=False,
                   do_magisweep=False,
                   verbose=False, verboseTop=False, verboseSet=False,
                   magisweep_list=None,
                   magisweep_start=60.0, magisweep_stop=5.0, magisweep_step=-1.0,
                   magpotsweep_list=None,
                   magpotsweep_start=110000, magpotsweep_stop=70000, magpotsweep_step=-2000):
    if do_magisweep:
        if verboseTop:
            print "Finding Electromagnet pot positions for each magnet current in 'magi_list'."
        if magisweep_list is None:
            magi_list = makeLists(magisweep_start, magisweep_stop, magisweep_step)
        else:
            magi_list = magisweep_list
        EmagPotList  = []

        for magi in magi_list:
            magpot_actual, deriv_mA_magpot = Emag_PID(mA_set=magi,verbose=verbose)
            EmagPotList .append(numpy.round(magpot_actual))
            if verboseSet:magmsg(magpot_actual)
        # arrange values from biggest to smallest
        EmagPotList.sort()
        if EmagPotList [-1] < EmagPotList [0]: EmagPotList  = reversed(EmagPotList )
    else:
        magi_list = None
        if magpotsweep_list is None:
            EmagPotList  = makeLists(magpotsweep_start, magpotsweep_stop, magpotsweep_step)
        else:
            EmagPotList  = magpotsweep_list

    # set the magnet to default position
    if useTHzComputer:setmag_highlow(default_magpot)
    magpot_actual = default_magpot
    if verboseSet:magmsg(magpot_actual)

    return EmagPotList, magi_list, magpot_actual

def getLOfreqList(biasOnlyMode=True,
                  LOfreqs_list=None,
                  LOfreq_start=650.0,
                  LOfreq_stop=692.0,
                  LOfreq_step=1.0):
    if biasOnlyMode:
        LOfreq_list = ['biasOnlyMode']
    else:
        if LOfreqs_list is None:
            LOfreq_list = list(makeLists(LOfreq_start, LOfreq_stop, LOfreq_step))
        else:
            LOfreq_list = LOfreqs_list
    return LOfreq_list

def getLOpowList(sisV_feedback,useTHzComputer=False,
                 testMode=True,
                 biasOnlyMode=True,
                 do_LOuAsearch=False,
                 do_LOuApresearch=False,
                 lenLOfreqList=1,
                 verbose=False, verboseTop=False, verboseSet=False,
                 LOuAsearch_list=None,
                 LOuAsearch_start=16.0, LOuAsearch_stop=16.0, LOuAsearch_step=1.0,
                 UCAsweep_list=None,
                 UCAsweep_min=0.0, UCAsweep_max=3.8, UCAsweep_step=0.5
                 ):
    setLabJack=True
    if (biasOnlyMode or testMode):
        setLabJack=False

    # set the UCA voltage to zero
    if setLabJack: LabJackU3_DAQ0(default_UCA)
    UCA_actual = default_UCA
    if verboseSet:UCAmsg(UCA_actual)

    # set the magnet to default position
    if useTHzComputer:setmag_highlow(default_magpot)
    magpot_actual = default_magpot
    if verboseSet:magmsg(magpot_actual)

    if useTHzComputer:setfeedback(feedback=sisV_feedback)
    feedback_actual = sisV_feedback
    if verboseSet:fbmsg(feedback_actual)

    # set the SIS pot to the default position
    if useTHzComputer:setSIS_only(default_sispot, feedback_actual, verbose=False, careful=False)
    sisPot_actual = default_sispot
    if verboseSet:sismsg(sisPot_actual)

    if biasOnlyMode:
        UCA_list  = ['biasOnlyMode']
        LOuA_list = ['biasOnlyMode']
    elif ((do_LOuAsearch) and (do_LOuApresearch) and (not testMode)):
        if verboseTop:
            print "Finding SIS pot positions for each SIS current in 'LOuA_list'."
            print "This option is found when do_LOuAsearch and do_LOuApresearch are both True."
            print "This list is discarded if both LO power (LOuA) and LO frequency are both changing in a single run"
        if LOuAsearch_list is None:
            LOuA_list = makeLists(LOuAsearch_start, LOuAsearch_stop, LOuAsearch_step)
        else:
            LOuA_list = LOuAsearch_list

        UCA_list = []
        for LOuA in LOuA_list:
            UCA_actual, deriv_uA_UCAvoltage = LO_PID(uA_set=LOuA, feedback=feedback_actual, verbose=verbose)
            if verboseTop: print "UCA = " + str(UCA_actual) + " V  for LOuA = " + str(LOuA) + " uA"
            elif verboseSet:
                LOuAmsg(LOuA)
                UCAmsg(UCA_actual)

         # set the UCA voltage to zero
        LabJackU3_DAQ0(default_UCA)
        UCA_actual = default_UCA
        if verboseSet:UCAmsg(UCA_actual)

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
    if ((1 < lenLOfreqList) and (do_LOuAsearch == False) and (1 < len(UCA_list))):
        print "It is not recommended to step LO frequency and UCA voltage with in the same run."
        print "LO power can change as a function of frequency"
        if raw_input("Press Enter to continue or anything else to quit, you have been warned") != '':
            print "Initiating systems shutdown"
            sweepShutDown()
            sys.exit()


    return LOuA_list, UCA_list, feedback_actual, sisPot_actual, magpot_actual, UCA_actual
