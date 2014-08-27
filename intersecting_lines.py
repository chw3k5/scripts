# intersecting_line.py
# This is the location of the Kappa Scripts on Caleb's Mac
import sys
func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)

#####################
###### Imports ######
#####################
import numpy
import os
import matplotlib
import shutil
matplotlib.rc('text', usetex=True)
from matplotlib import pyplot as plt
from operator import itemgetter
from YdataPro import YdataPro
from profunc import getYnums, getproparams, getprodata

#####################    
###### Options ######
#####################
verbose=True # True or False

# make sure all thes sets have been processed in the same way           
setnums = [1,2]

process_data = False # True or False

LO_current_min = 6
LO_current_max = 14 # uA

mV_min  = 1.90
mV_max  = 1.91
mV_step = 0.02
mV_arange = numpy.array(range(int(numpy.round(mV_min/mV_step)), int(numpy.round(mV_max/mV_step))))*mV_step

hot_temp  = 295 # kelvin
cold_temp =  80 # Kelvin

sisbias2plot = 'set' # the exect number ie 1.92, 'set' for the all the avaliable values on different plots, 'all' for all the value on the same plot
magi2plot    = 30.0 # the exect number ie 30.0, 'set' for the all the avaliable values on different plots, 'all' for all the value on the same plot
LOfreq2plot  = 672  # the exect number ie  672, 'set' for the all the avaliable values on different plots, 'all' for all the value on the same plot
IFband2plot  = 1.42 # the exect number ie 1.42, 'set' for the all the avaliable values on different plots, 'all' for all the value on the same plot

### Plot options
show_plot = False
save_plot = True 
do_eps    = True
### Processing Options ###

useOFFdata = False # True or False
Off_datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'

mono_switcher = True # makes data monotonic in mV
do_regrid=True
regrid_mesh=mV_step # in mV (default = 0.01)
do_conv = True
sigma   = 0.03 # in mV
min_cdf = 0.95 # fraction of Guassian used in kernal calulation


######################
###### Settings ######
######################


rootdir = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/"
search_str = 'Y'


# loop over sets folder 
intlindata = []
for setnum in setnums:
    setdatadir = rootdir + "set" + str(setnum) + "/"
    
    if process_data:
        YdataPro(verbose, setdatadir, True, search_str, [], useOFFdata, Off_datadir, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf)
    
    prodatadir = setdatadir + "prodata/"
    Ynums = getYnums(prodatadir, search_str)
    
    # loop over the Y numbers in each data set
    for Ynum in Ynums:
        # read in the data, mostly done with functions
        Ydatadir = prodatadir + Ynum + '/'
        paramsfile = Ydatadir + 'prohotparams.csv' 
        hot_K_val, hot_magisweep, hot_magiset, hot_magpot, hot_meanmag_V, hot_stdmag_V, hot_meanmag_mA, hot_stdmag_mA, hot_sisisweep, hot_sisiset, hot_UCA_volt, hot_meanSIS_mV, hot_stdSIS_mV, hot_meanSIS_uA, hot_stdSIS_uA, hot_meanSIS_tp, hot_stdSIS_tp, hot_SIS_pot, hot_del_time, hot_LOfreq, hot_IFband = getproparams(paramsfile)
        Yfactor, mV_array, hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean, hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std, cold_TP_std, hot_TP_num, cold_TP_num, hot_TP_freq, cold_TP_freq, hot_time_mean, cold_time_mean, hot_pot, cold_pot, hot_meas_num, cold_meas_num = getprodata(Ydatadir)
        mV_list = list(mV_array)
        for mV in mV_arange:
            min_val = 999999.0
            for mV_array_index in range(len(mV_array)):
                diff = abs(mV-mV_array[mV_array_index])
                if diff < min_val:
                    min_val = diff
                    mV_index = mV_array_index
            #                            0   ,      1   ,            2         ,            3          ,     4      ,         5         ,     6      ,     7     ,     8
            data_line = numpy.array((hot_temp, cold_temp, hot_TP_mean[mV_index], cold_TP_mean[mV_index], hot_sisiset, mV_array[mV_index], hot_magiset, hot_LOfreq, hot_IFband))
            intlindata.append(data_line)

def uniqify(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result
# Now we have all the data
intlindata_array = numpy.array(intlindata)
sisiset_type = uniqify(intlindata_array[:,4])
sisbias_type = uniqify(intlindata_array[:,5])
magi_type    = uniqify(intlindata_array[:,6])
LOfreq_type  = uniqify(intlindata_array[:,7])
IFband_type  = uniqify(intlindata_array[:,8])

plotdir = rootdir + 'setplots/intlin/'
if not os.path.isdir(plotdir):
    os.makedirs(plotdir)
plotdir = plotdir +  'sets' + str(setnums) + '/'
if os.path.isdir(plotdir):
    # remove old processed data
    shutil.rmtree(plotdir)
    # make a folder for new processed data
    os.makedirs(plotdir)
else:
    # make a folder for new processed data
    os.makedirs(plotdir)
def LOpowseries(sisbias2plot, magi2plot, LOfreq2plot, IFband2plot, plotdir):

    if sisbias2plot == 'all':
        sisbias_index = list(range(len(sisbias_type)))
    else:
	min_diff = 999999
        for sisbias_test_index in range(len(sisbias_type)):
            diff = abs(sisbias_type[sisbias_test_index] - sisbias2plot)
            if diff < min_diff:
                min_diff = diff
                sisbias_index = []
                sisbias_index.append(sisbias_test_index)
                
    if magi2plot == 'all':
        magi_index = list(range(len(magi_type)))
    else:
        min_diff = 999999
        for magi_test_index in range(len(magi_type)):
            diff = abs(magi_type[magi_test_index] - magi2plot)
            if diff < min_diff:
                min_diff = diff
                magi_index = []
                magi_index.append(magi_test_index)
             
    if LOfreq2plot == 'all':
        LOfreq_index = list(range(len(LOfreq_type)))
    else:
        min_diff = 999999
        for LOfreq_test_index in range(len(LOfreq_type)):
            diff = abs(LOfreq_type[LOfreq_test_index] - LOfreq2plot)
            if diff < min_diff:
                min_diff = diff
                LOfreq_index = []
                LOfreq_index.append(LOfreq_test_index)
        
    if IFband2plot == 'all':
        IFband_index = list(range(len(IFband_type)))
    else:
        min_diff = 999999
        for IFband_test_index in range(len(IFband_type)):
            diff = abs(IFband_type[IFband_test_index] - IFband2plot)
            if diff < min_diff:
                min_diff = diff
                IFband_index = []
                IFband_index.append(IFband_test_index)
                
    
    intlindata2plot_mask_temp = numpy.array([False]*len(intlindata))
    for n in range(len(sisbias_index)):
        temp_list = list(intlindata_array[:,5])
        temp_list2 = temp_list == sisbias_type[sisbias_index[n]]
        # 'OR' logic
        intlindata2plot_mask_temp = temp_list2+intlindata2plot_mask_temp
    intlindata2plot_mask = intlindata2plot_mask_temp
    
    intlindata2plot_mask_temp = numpy.array([False]*len(intlindata))
    for n in range(len(magi_index)):
        temp_list = list(intlindata_array[:,6])
        temp_list2 = temp_list == magi_type[magi_index[n]]
        # 'OR' logic
        intlindata2plot_mask_temp = temp_list2+intlindata2plot_mask_temp
    # "AND" logic
    intlindata2plot_mask = intlindata2plot_mask_temp*intlindata2plot_mask
    
    intlindata2plot_mask_temp = numpy.array([False]*len(intlindata))
    for n in range(len(LOfreq_index)):
        temp_list = list(intlindata_array[:,7])
        temp_list2 = temp_list == LOfreq_type[LOfreq_index[n]]
        # 'OR' logic
        intlindata2plot_mask_temp = temp_list2+intlindata2plot_mask_temp
    # "AND" logic
    intlindata2plot_mask = intlindata2plot_mask_temp*intlindata2plot_mask
    
    intlindata2plot_mask_temp = numpy.array([False]*len(intlindata))
    for n in range(len(IFband_index)):
        temp_list = list(intlindata_array[:,8])
        temp_list2 = temp_list == IFband_type[IFband_index[n]]
        # 'OR' logic
        intlindata2plot_mask_temp = temp_list2+intlindata2plot_mask_temp
    # "AND" logic
    intlindata2plot_mask = intlindata2plot_mask_temp*intlindata2plot_mask
    
    
    # with the mask made above we can plot the data
    intlindata2plot = []
    m_list          = []
    b_list          = []
    index_list = numpy.transpose(numpy.where((intlindata2plot_mask == True)))
    matplotlib.rcParams['legend.fontsize'] = 12.0
    fig, ax1 = plt.subplots()
    temperature_axis = numpy.arange(-300, 301,1)
    for n in index_list:# range(len(index_list)):
        single_line = intlindata[n]
        intlindata2plot.append(single_line)
    
    intlindata2plot_array = numpy.array(intlindata2plot)
    intlindata2plot_array = numpy.asarray(sorted(intlindata2plot_array,  key=itemgetter(4)))
    intlindata2plot = list(intlindata2plot_array)
    for single_line in intlindata2plot:
        hot_temp  = single_line[0]
        cold_temp = single_line[1]
        hot_pwr   = single_line[2]
        cold_pwr  = single_line[3]
        m = (hot_pwr-cold_pwr)/(hot_temp-cold_temp)
        m_list.append(m)
        b = hot_pwr-m*hot_temp
        b_list.append(b)
        pwr_axis = m*temperature_axis + b
        if (LO_current_min <= single_line[4] and single_line[4] <= LO_current_max and single_line[4] != 7.0):
            ax1.plot(temperature_axis, pwr_axis, label = str(single_line[4]) + ' $\mu$A')
            
    
    ax1.set_ylim([-0.1, .25])
    plt.title('magnet current: ' + str('%2.2f' % magi2plot) + ' mA   SIS bias voltage: ' + str('%2.2f' % sisbias2plot) + ' mV')
    plt.xlabel('temperature (K)')
    plt.ylabel('receiver power')

    plt.legend(loc=2)
    temper= -44
    plt.text(-20, 0.22, "$44 K = T^\prime$", fontsize=16, color="firebrick")
    ax1.plot([temper, temper],[-0.1, .25], color="firebrick")
    
    if show_plot:
        plt.ylabel('Current ($\mu$A)')
        plt.show()
        plt.draw()
    if save_plot:
        plotdir = plotdir + 'magi' + str('%2.2f' % magi2plot) + '/'
        if not os.path.isdir(plotdir):
            os.makedirs(plotdir)
        plotfilename = plotdir + 'SISbias' + str('%2.2f' % sisbias2plot) + '_LOfreq' + str('%3.2f' % LOfreq2plot) + '_IFband' + str('%2.2f' % IFband2plot)
        if do_eps:
            if verbose:
                print "saving EPS file"
            plt.savefig(plotfilename+".eps")
        else:
            if verbose:
                print "saving PNG file"
            plt.savefig(plotfilename+".png")
        plt.close("all")
    return

if sisbias2plot == 'set':
    sisbias2plot_array = numpy.array(sisbias_type)
else:
    sisbias2plot_array = numpy.array([sisbias2plot])
if magi2plot == 'set':
    magi2plot_array = numpy.array(magi_type)
else:
    magi2plot_array = numpy.array([magi2plot])
if LOfreq2plot == 'set':
    LOfreq2plot_array = numpy.array(LOfreq_type)
else:
    LOfreq2plot_array = numpy.array([LOfreq2plot])
if IFband2plot == 'set':
    IFband2plot_array = numpy.array(IFband_type)
else:
    IFband2plot_array = numpy.array([IFband2plot])
    
def param_array(zero_array, first_array, zero_len, first_len):
    import numpy
    loop_over = (first_len) - 1
    temp0_array = zero_array
    new_len = zero_len*first_len
    for n in range(loop_over):
        temp0_array = numpy.vstack((temp0_array, zero_array))
    zero_array = temp0_array
    zero_array = numpy.reshape(zero_array, new_len)
    
    loop_over = (zero_len) - 1
    temp1_array = first_array
    for n in range(loop_over):
        temp1_array = numpy.vstack((temp1_array, first_array))
    first_array = numpy.transpose(temp1_array)
    first_array = numpy.reshape(first_array, new_len)
    zero_len    = new_len
    first_len   = new_len
    return zero_array, first_array, zero_len, first_len

sisbias2plot_array, magi2plot_array, len_sisbias2plot_array, len_magi2plot_array = param_array(sisbias2plot_array, magi2plot_array, len(sisbias2plot_array), len(magi2plot_array))

LOfreq2plot_array_temp = LOfreq2plot_array
sisbias2plot_array, LOfreq2plot_array, len_sisbias2plot_array, len_LOfreq2plot_array = param_array(sisbias2plot_array, LOfreq2plot_array_temp, len_sisbias2plot_array, len(LOfreq2plot_array_temp))
magi2plot_array, LOfreq2plot_array, len_magi2plot_array, len_LOfreq2plot_array = param_array(magi2plot_array, LOfreq2plot_array_temp, len_magi2plot_array, len(LOfreq2plot_array_temp))

IFband2plot_array_temp = IFband2plot_array
sisbias2plot_array, IFband2plot_array, len_sisbias2plot_array, len_IFband2plot_array = param_array(sisbias2plot_array, IFband2plot_array_temp, len_sisbias2plot_array, len(IFband2plot_array_temp))
magi2plot_array, IFband2plot_array, len_magi2plot_array, len_IFband2plot_array = param_array(magi2plot_array, LOfreq2plot_array_temp, len_magi2plot_array, len(LOfreq2plot_array_temp))
LOfreq2plot_array, IFband2plot_array, len_LOfreq2plot_array, len_IFband2plot_array = param_array(LOfreq2plot_array, LOfreq2plot_array_temp, len_LOfreq2plot_array, len(LOfreq2plot_array_temp))

for n in range(len_sisbias2plot_array):
    
    LOpowseries(sisbias2plot_array[n], magi2plot_array[n], LOfreq2plot_array[n], IFband2plot_array[n], plotdir)