__author__ = 'chwheele'
import os, numpy, sys
from control import default_magpot, default_sispot, setfeedback, setSIS, setmag_highlow
from profunc import windir
from PID import SIS_mV_PID


def MakeSetDirs(datadir):
    # does the datadir exist? If not, we will make it!
    rawdatadir = datadir+'rawdata/'
    datadir    = windir(datadir)
    rawdatadir = windir(rawdatadir)
    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    if not os.path.isdir(rawdatadir):
        os.makedirs(rawdatadir)
    return

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
            sys.exit()
        if isinstance(single_list, list):
            unordered_lists.append(single_list)
        else:
            print "The function orderLists needs a list of tuples\n"+\
            "with each tuple containing (int, list). Something other than a list\n"+ \
            "was found: ", single_list
            sys.exit()

    for n in range(num_of_lists):
        axis_num_count = axis_list.count(n)
        if axis_num_count == 1:
            pass
        elif axis_num_count < 1:
            print "In the function oderLists the axis: ", n, " is not listed."
            print " Axis_nums should start with 0 and increment by one with each", \
            "axis having a unique number"
            print "see axis_list:", axis_list
            sys.exit()
        elif 1 < axis_num_count:
            print "In the function oderLists the axis: ", n, " appears ", \
            axis_num_count, " times, it should be unique."
            print " Axis_nums should start with 0 and increment by one with each", \
            "axis having a unique number"
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
    except TypeError:
        str_val = sisPot
    if int(sisPot) == int(default_sispot):
         print "The SIS bias pot has ben set the default value: " , str_val
    else:
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

def getSISpotList(sisV_feedback,
                  do_sisVsweep=False, verbose=False, verboseTop=False, verboseSet=False,
                  sisVsweep_list=None,
                  sisVsweep_start=1.3, sisVsweep_stop=1.3, sisVsweep_step=0.1,
                  sisPot_feedTrue_list=None,
                  sisPot_feedTrue_start=59100, sisPot_feedTrue_stop=59100, sisPot_feedTrue_step=100,
                  sisPot_feedFalse_list=None,
                  sisPot_feedFalse_start=64000, sisPot_feedFalse_stop=64000, sisPot_feedFalse_step=200
                  ):
    SISpot_List=None

    # set the feedback
    setfeedback(feedback=sisV_feedback)
    feedback_actual = sisV_feedback
    if verboseSet: fbmsg(feedback_actual)

    # set the magnet
    setmag_highlow(default_magpot)
    magpot_actual = default_magpot
    if verboseSet: magmsg(feedback_actual)

    # This mode takes a list of voltages and uses a PID program to find the corresponding pot positions
    if do_sisVsweep:
        if verboseTop: print "Finding SIS pot positions for each magnet Voltage in 'sisV_list'."
        if sisVsweep_list is not None:
            sisV_list = sisVsweep_list
        else:
            sisV_list = makeLists(sisVsweep_start, sisVsweep_stop, sisVsweep_step)
        sisPot_list = []
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
            sisPot_list.append(sisPot_actual)
            if verboseSet: sismsg(sisPot_actual)
            first_pot = sisPot_actual
            mV_first = sismV

    # This mode just makes list of SIS pot positions based on a specified range of pot positions
    else:
        sisV_list = None
        if feedback_actual:
            if sisPot_feedTrue_list is not None:
                sisPot_list = sisPot_feedTrue_list
            else:
                sisPot_list = makeLists(sisPot_feedTrue_start, sisPot_feedTrue_stop, sisPot_feedTrue_step)
        else:
            if sisPot_feedFalse_list is not None:
                sisPot_list=sisPot_feedFalse_list
            else:
                sisPot_list = makeLists(sisPot_feedFalse_start, sisPot_feedFalse_stop, sisPot_feedFalse_step)
    # round the sisPot list to integers, this is needed comparisons to triggers later on in the script
    for Pot_index in range(len(sisPot_list)):
        sisPot_list[Pot_index] = int(round(sisPot_list[Pot_index]))

    # set the SIS pot
    mV_sis, uA_sis, sisPot_actual = setSIS(default_sispot, feedback_actual, verbose=False, careful=False)
    if verboseSet: sismsg(sisPot_actual)

    return SISpot_List, feedback_actual, sisPot_actual, magpot_actual







