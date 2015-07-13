__author__ = 'chwheele'

import os
from profunc import get_fastIV

def DataTrimmer(min_trim, max_trim, ordered_set, trim_list):
    if len(list(ordered_set)) < 2:
        status      = True
        trimmed      = ordered_set
        trimmed_list = trim_list
    else:
        if min_trim is not None:
            set_max = max(ordered_set)
        else:
            set_max = None
        if max_trim is not None:
            set_min = min(ordered_set)
        else:
            set_min = None
        index_min_trim = 0
        min4min_trim = None
        status = True
        trimmed = None
        if not ((max_trim is None) and (min_trim is None)):
            if ((max_trim is not None) and (min_trim is not None) and (max_trim < min_trim)):
                print "max_trim is less than or equal to min_trim, min trim must be strictly less than max_trim"
                print "min_trim:", min_trim
                print "max_trim:", max_trim
                print "returning status=False"
                status = False
            else:
                # Min trim
                if min_trim is not None:
                    if min_trim < set_max:
                        for index_min_trim in range(len(ordered_set[:])):
                            if min_trim <= ordered_set[index_min_trim]:
                                min_trimmed = ordered_set[index_min_trim:]
                                #print ordered_set[index_min_trim]
                                min4min_trim = min(min_trimmed)
                                break
                    else:
                        min_trimmed = ordered_set
                else:
                    min4min_trim = set_min
                    min_trimmed = ordered_set

                if max_trim is not None:
                    # Max trim
                    if min4min_trim < max_trim:
                        for index_max_trim in reversed(range(len(min_trimmed[:]))):
                            if min_trimmed[index_max_trim] <= max_trim:
                                trimmed = min_trimmed[:index_max_trim]
                                break
                    else:
                        print max_trim, "=max_trim is greater than the minimum of the the ordered set that has been already been trimmed sweep, that is:", min4min_trim
                        print "The min value of the ordered set before trimming was:", set_min
                        print "It is likely that the difference of max_trim and min_trim is greater that the spacing of values in the ordered set"
                        print "min_trim:", min_trim
                        print "max_trim:", max_trim
                        print "ordered_set:", ordered_set
                        print "min_trimmed:", min4min_trim
                        print "returning status=False"
                        status = False
                else:
                    trimmed = min_trimmed
        else:
            trimmed = ordered_set

        #print trimmed[0],trimmed[-1]
        # trim the corresponding values in the list dependent variables
        trimmed_list = []
        if ((trim_list != []) and (status)):
            list_length = len(trimmed)
            index_max_trim = index_min_trim + list_length
            for trim in trim_list:
                trimmed_list.append(trim[index_min_trim:index_max_trim])

    return status, trimmed, trimmed_list

def Params_2_str(param_vals, format_str, btype=None):
    if btype == 'sq':
        out_str = "["
    elif btype == 'curl':
        out_str = "{"
    elif btype == 'round':
        out_str = "("
    else:
        out_str = ''
    try:
        out_str += str(format_str % param_vals)
    except TypeError:
        vals_len = len(param_vals)
        if vals_len == 1:
            out_str += str(format_str % param_vals)
        elif 1 < vals_len:
            for n in range(vals_len - 1):
                out_str += str(format_str % param_vals[n]) + ', '
            out_str += str(format_str % param_vals[-1])
    if btype == 'sq':
        out_str += "]"
    elif btype == 'curl':
        out_str += "}"
    elif btype == 'round':
        out_str += ")"

    return out_str


### Do Cuts Based on Parameters
# total power integration time
def tp_int_cut(sweeps, min_tp_int=None, max_tp_int=None, verbose=False):
    tp_int_cut_sweeps = []
    if verbose:
        print 'cutting for total power integration time'
    for sweep in sweeps:
        tp_int_time = sweep.tp_int_time
        if ((min_tp_int is None) or (min_tp_int  <= tp_int_time)) and (
            (max_tp_int is None) or (tp_int_time <=  max_tp_int)):
            tp_int_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return tp_int_cut_sweeps

# LO pump power in uA (that my code attempt to set)
def LOuAset_cut(sweeps, min_LOuAset=None, max_LOuAset=None, verbose=False):
    LOuAset_cut_sweeps = []
    if verbose:
        print 'cutting the LO pump power that the code attempted to set'
    for sweep in sweeps:
        LOuAset = sweep.LOuAset
        if ((min_LOuAset is None) or (min_LOuAset  <= LOuAset)) and (
            (max_LOuAset is None) or (LOuAset <=  max_LOuAset)):
            LOuAset_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return LOuAset_cut_sweeps

# Cut if the difference between LO pump power and the standard measurement is too great
def LOuAdiff_cut(sweeps, max_diff=1.0, verbose=False):
    LOuAdiff_cut_sweeps = []
    if verbose:
        print 'cutting sweep with the difference of measured LO pump power and attempted setting of LO power greater then', max_diff, 'uA'
    for sweep in sweeps:
        LOuAset    = sweep.LOuAset
        meanSIS_uAs = sweep.meanSIS_uA
        over_max_diff = False
        for meanSIS_uA in meanSIS_uAs:
            diff = abs(LOuAset - meanSIS_uA)
            if max_diff <= diff:
                over_max_diff = True
                break
        if not over_max_diff:
            LOuAdiff_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return LOuAdiff_cut_sweeps


def LOfreq_cut(sweeps,LOfreq):
    new_sweeps = []
    try:
        LOfreq = np.round(LOfreq)
        for sweep in sweeps:
            if np.round(sweep.LOfreq) == LOfreq:
                new_sweeps.append(sweep)
    except:
        new_sweeps = sweeps
    return new_sweeps




def mV_bias_cut_Y(Ysweeps, mV_min=None, mV_max=None, verbose=False):
    mV_bias_cut_Ysweeps = []

    for Ysweep in Ysweeps:
        # cuts for the power meter acquired data
        if Ysweep.Ydatafound:
            if mV_min is not None:
                new_mV_Yfactor = []
                new_Yfactor = []
                for (mV_index,mV) in list(enumerate(Ysweep.mV_Yfactor)):
                    if mV_min <= mV:
                        new_mV_Yfactor.append(Ysweep.mV_Yfactor[mV_index])
                        new_Yfactor.append(Ysweep.Yfactor[mV_index])
                Ysweep.mV_Yfactor = new_mV_Yfactor
                Ysweep.Yfactor = new_Yfactor
            if mV_max is not None:
                new_mV_Yfactor = []
                new_Yfactor = []
                for (mV_index,mV) in list(enumerate(Ysweep.mV_Yfactor)):
                    if mV <= mV_max:
                        new_mV_Yfactor.append(Ysweep.mV_Yfactor[mV_index])
                        new_Yfactor.append(Ysweep.Yfactor[mV_index])
                Ysweep.mV_Yfactor = new_mV_Yfactor
                Ysweep.Yfactor = new_Yfactor

        else:
            if verbose:
                print "Power meter Y data not found for:",Ysweep.longDescription()

    for Ysweep in Ysweeps:
        # cuts for the spectrum analyzer data
        if Ysweep.spec_data_found:
            if mV_min is not None:
                for (sweep_index,hot_mV) in list(enumerate(Ysweep.spec_hot_mV_mean_list[:])):
                    if hot_mV <= mV_min:
                        index_to_remove = Ysweep.spec_hot_mV_mean_list.index(hot_mV)

                        Ysweep.spec_freq_list.pop(index_to_remove)
                        Ysweep.spec_Yfactor_list.pop(index_to_remove)
                        Ysweep.spec_hot_pwr_list.pop(index_to_remove)
                        Ysweep.spec_hot_pot_list.pop(index_to_remove)
                        Ysweep.spec_hot_mV_mean_list.pop(index_to_remove)
                        Ysweep.spec_hot_tp_list.pop(index_to_remove)
                        Ysweep.spec_hot_spike_list_list.pop(index_to_remove)
                        Ysweep.spec_hot_spikes_inband_list.pop(index_to_remove)
                        Ysweep.spec_hot_sweep_index_list.pop(index_to_remove)
                        Ysweep.spec_cold_pwr_list.pop(index_to_remove)
                        Ysweep.spec_cold_pot_list.pop(index_to_remove)
                        Ysweep.spec_cold_mV_mean_list.pop(index_to_remove)
                        Ysweep.spec_cold_tp_list.pop(index_to_remove)
                        Ysweep.spec_cold_spike_list_list.pop(index_to_remove)
                        Ysweep.spec_cold_spikes_inband_list.pop(index_to_remove)
                        Ysweep.spec_cold_sweep_index_list.pop(index_to_remove)

            if mV_max is not None:
                for (sweep_index,hot_mV) in list(enumerate(Ysweep.spec_hot_mV_mean_list[:])):
                    if  mV_max <= hot_mV:
                        index_to_remove = Ysweep.spec_hot_mV_mean_list.index(hot_mV)

                        Ysweep.spec_freq_list.pop(index_to_remove)
                        Ysweep.spec_Yfactor_list.pop(index_to_remove)
                        Ysweep.spec_hot_pwr_list.pop(index_to_remove)
                        Ysweep.spec_hot_pot_list.pop(index_to_remove)
                        Ysweep.spec_hot_mV_mean_list.pop(index_to_remove)
                        Ysweep.spec_hot_tp_list.pop(index_to_remove)
                        Ysweep.spec_hot_spike_list_list.pop(index_to_remove)
                        Ysweep.spec_hot_spikes_inband_list.pop(index_to_remove)
                        Ysweep.spec_hot_sweep_index_list.pop(index_to_remove)
                        Ysweep.spec_cold_pwr_list.pop(index_to_remove)
                        Ysweep.spec_cold_pot_list.pop(index_to_remove)
                        Ysweep.spec_cold_mV_mean_list.pop(index_to_remove)
                        Ysweep.spec_cold_tp_list.pop(index_to_remove)
                        Ysweep.spec_cold_spike_list_list.pop(index_to_remove)
                        Ysweep.spec_cold_spikes_inband_list.pop(index_to_remove)
                        Ysweep.spec_cold_sweep_index_list.pop(index_to_remove)

    for Ysweep in Ysweeps[:]:
        if ((Ysweep.Ydatafound) or (Ysweep.spec_data_found)):
            if  ((Ysweep.Yfactor == []) or (Ysweep.Yfactor is None)):
               Ysweep.Ydatafound=False
            if  ((Ysweep.spec_Yfactor_list == []) or (Ysweep.spec_Yfactor_list is None)):
                Ysweep.spec_data_found=False

            if (((Ysweep.Yfactor != []) and (Ysweep.Yfactor is not None)) or ((Ysweep.spec_Yfactor_list != [])and(Ysweep.spec_Yfactor_list is not None))):
                mV_bias_cut_Ysweeps.append(Ysweep)



    return mV_bias_cut_Ysweeps

def YfactorFilter(Ysweeps, maxYfactor_atLeastThis=1.0, verbose=False):
    newYsweeps=[]
    for Ysweep in Ysweeps:
        (max_Yfactor, max_y_error, max_y_mV,
         max_y_mVerror, max_y_uA,max_y_uAerror,
         max_y_TP, max_y_TPerror, max_y_pot) \
            = Ysweep.find_max_yfactor_pm()
        if maxYfactor_atLeastThis <= max_Yfactor:
            newYsweeps.append(Ysweep)
    return newYsweeps