import os, numpy
from datapro import YdataPro
from profunc import windir, local_copy, makeORclear_plotdir
from SetGrab import getYsweeps, tp_int_cut, LOuAset_cut, LOuAdiff_cut, mV_bias_cut_Y, LOfreq_cut, YfactorFilter
from domath import make_monotonic, filter_on_occurrences
from dataPhil_plotting import sweepPlotter


###############
### Options ###
###############

# general
verbose         = True
show_plots      = False
save_plots      = True
clear_old_plots = True
do_eps          = True


# data processing
process_data  = False
Ynums         = None
search_str    = 'Y'
search_4Ynums = True
mono_switcher_mV = True
do_regrid_mV     = True
regrid_mesh_mV   = 0.01
do_conv_mV       = True
sigma_mV         = 0.03
min_cdf_mV       = 0.95
remove_spikes    = False
do_normspectra   = False
norm_freq        = 1.42
norm_band        = 0.060
do_freq_conv     = True
min_cdf_freq     = 0.90
sigma_GHz        = 0.10



######################
### Parameter Cuts ###
######################
# total power integration time
min_tp_int = None # at least this, None is any
max_tp_int = None # at most this, None is any
# the attempted setting of LO pump power in uA
min_LOuAset =  None # at least this, None is any
max_LOuAset = None # at least this, None is any
# The maximum difference between the set and measured LO pump power
maxdiff_LOuA = None # None is any
# select an LO frequency to look at
LOfreq_to_get = None # this number is rounded to the near integer, None is any
# reorder the Ysweeps list in terms of lowest to highest LOuA (meanSIS_uA)
sort_LOuA = False


### Will only work for Y factor
# mV bias cuts
mV_bias_min = None # at least this, None is any
mV_bias_max = None # at most this, None is any

maxYfactor_atLeastThis = 0.9 # None is any



##################################################################
###### Output files with Y factors over the Threshold value ######
##################################################################
outputYfilenames=True
clear_oldYfilenames = False
outputYpath=local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/foundYfiles/'))
outYfile='rerun.csv'
Y_threshold = None



###############################################################
### All the sets of data to collect the processed data from ###
###############################################################
setnames = []
#setnames.extend(['set4','set5','set6','set7','LOfreq'])
#setnames.extend(['Mar28/LOfreq_wspec'])#,'Mar28/LOfreq_wspec2','Mar28/moonshot','Mar28/Mag_sweep','Mar28/LOfreq'])
#setnames.extend(['Mar24_15/LO_power','Mar24_15/Yfactor_test'])
#setnames.extend(['Nov05_14/Y_LOfreqMAGLOuA','Nov05_14/Y_MAG','Nov05_14/Y_MAG2','Nov05_14/Y_MAG3','Nov05_14/Y_standard'])
#setnames.extend(['Oct20_14/LOfreq','Oct20_14/Y_LO_pow','Oct20_14/Y_MAG','Oct20_14/Y_MAG2','Oct20_14'])
#setnames.extend(['Jun08_15/magSweep2','Jun08_15/magSweep3'])
#setnames.extend(['Jun08_15/newBS_magSweep'])
# possibleLOfreqs=range(650,693)
# setnames.extend(['Jun08_15/LOfreq/'+str(freq) for freq in possibleLOfreqs])
# possibleLOfreqs=range(650,693)
# setnames.extend(['Jun08_15/bestLOfreq/'+str(freq) for freq in possibleLOfreqs])
# possibleLOfreqs = [660,664,665,672,677,685]
# setnames.extend(['Jun08_15/magsweep/'+str(freq) for freq in possibleLOfreqs])
# standingWaveNums = [6,7,8,9]
# for standingWaveNum in standingWaveNums:
#     possibleLOfreqs=range(650,693)
#     setnames.extend(['Jun08_15/standingWaveTest'+str(standingWaveNum)+'/'+str(freq) for freq in possibleLOfreqs])
#
# setnames.extend(['Jun08_15/standingWaveTest10'])
#
# setnames.extend(['Jun08_15/standingWaveTest_noChopper'])
#
# setnames.extend(['Jun08_15/standingWaveTest_noChopper_5papers'])

# setnames.extend(['Jun08_15/standingWaveTest_noChopper_5papers_24Voff_LJdisCon'])
#
# setnames.extend(['Alice/LOfreq_UCA2','Alice/LOfreq_UCA2'])
# setnames.extend(['Alice/SISpot_MAGpot','Alice/SISpot_MAGpot2'])
# setnames.extend(['Alice/LOfreq','Alice/LOfreq2','Alice/LOfreq3','Alice/LOfreq4'])

# freqVector = range(650,681,5)
# for index in range(len(freqVector)-1):
#     dirString = 'Alice/LOfreq'+str(freqVector[index])+'-'+str(freqVector[index+1])
#     setnames.append(dirString)

freqVector = range(650,671,5)
for index in range(len(freqVector)-1):
    dirString = 'Alice/LOfreq'+str(freqVector[index])+'-'+str(freqVector[index+1])
    setnames.append(dirString+'/rerun')

# freqVector = range(654,687,2)
# for index in range(len(freqVector)-1):
#     dirString = 'Alice_3p/LOfreq'+str(freqVector[index])+'-'+str(freqVector[index+1])
#     setnames.append(dirString)

freqVector = range(658,669,2)
for index in range(len(freqVector)-1):
    dirString = 'Alice_3p/LOfreq'+str(freqVector[index])+'-'+str(freqVector[index+1])
    setnames.append(dirString+'/rerun')

freqVector = range(670,675,2)
for index in range(len(freqVector)-1):
    dirString = 'Alice_3p/LOfreq'+str(freqVector[index])+'-'+str(freqVector[index+1])
    setnames.append(dirString+'/rerun')

# setnames.extend(['Alice_3p/LOfreq676-678'])

parent_folder = '/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/'
fullpaths_raw = [windir(parent_folder + setname + '/') for setname in setnames]
parent_folder = local_copy(parent_folder)
fullpaths = [windir(parent_folder + setname + '/') for setname in setnames]
print fullpaths




################################
###### Do data processing ######
################################
if process_data:
    for fullpath in fullpaths_raw:
        YdataPro(fullpath, verbose=verbose, search_4Ynums=search_4Ynums, search_str=search_str,
                 Ynums=Ynums, use_google_drive=False,
                 useOFFdata=False, Off_datadir='',
                 mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, regrid_mesh_mV=regrid_mesh_mV,
                 do_conv_mV=do_conv_mV, sigma_mV=sigma_mV, min_cdf_mV=min_cdf_mV,
                 remove_spikes=remove_spikes,do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                 do_freq_conv=do_freq_conv, min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz)




##############################
###### Get all the data ######
##############################
Ysweeps = getYsweeps(fullpaths, Ynums=Ynums, verbose=verbose)

##############################################################
###### Cut the data you have based on optional criteria ######
##############################################################

### Total power integration Time ###
if ((min_tp_int is not None) and (max_tp_int is not None)):
    Ysweeps = tp_int_cut(Ysweeps, min_tp_int=min_tp_int, max_tp_int=max_tp_int, verbose=verbose)
### the range of LO powers in uA ###
if ((min_LOuAset is not None) and (max_LOuAset is not None)):
    Ysweeps = LOuAset_cut(Ysweeps, min_LOuAset=min_LOuAset, max_LOuAset=max_LOuAset, verbose=verbose)
### the diffence between the measured LO power in uA and the LO power the was supposed to be set ###
if (maxdiff_LOuA is not None):
    Ysweeps = LOuAdiff_cut(Ysweeps, max_diff=maxdiff_LOuA, verbose=verbose)
### select a singel LO frequency
if LOfreq_to_get is not None:
    Ysweeps = LOfreq_cut(Ysweeps,LOfreq_to_get)
### reorder the Y sweeps for lowest to higher LO power (meanSIS_uA)
if sort_LOuA:
    LOuA_Ysweep_sort_list = []
    for Ysweep in Ysweeps:
         LOuA_Ysweep_sort_list.append(numpy.mean(Ysweep.meanSIS_uA))
    [new_LOuA_order,Ysweeps] = make_monotonic([LOuA_Ysweep_sort_list,Ysweeps])

### Yfactor cut
if ((mV_bias_min is not None) and (mV_bias_max is not None)):
    Ysweeps = mV_bias_cut_Y(Ysweeps, mV_min=mV_bias_min, mV_max=mV_bias_max, verbose=verbose)

# Cut based on max Y factor value
if maxYfactor_atLeastThis is not None:
    Ysweeps = YfactorFilter(Ysweeps, maxYfactor_atLeastThis=maxYfactor_atLeastThis, verbose=verbose)
























######################################################
###### Output files that made survived the cuts ######
######################################################
if outputYfilenames:
    if save_plots:
        makeORclear_plotdir(outputYpath,clear_flag=clear_oldYfilenames)
    longYfilename = outputYpath+outYfile

    if ((not clear_oldYfilenames) and (os.path.isfile(longYfilename))):
        file_handle = open(longYfilename,'a')
    else:
        file_handle = open(longYfilename,'w')

    for Ysweep in Ysweeps:
        (max_Yfactor, max_y_error, max_y_mV,
         max_y_mVerror, max_y_uA,max_y_uAerror,
         max_y_TP, max_y_TPerror, max_y_pot) = Ysweep.find_max_yfactor_pm()

        if Y_threshold <= max_Yfactor:
            print max_Yfactor,Ysweep.proYdatadir,Ysweep.LOfreq
            file_handle.write(Ysweep.proYdatadir+'\n')
    file_handle.close()
