# This is the calibration file for the LO. Use this file to 
# do new calibration sweeps or plot exising sweeps
import sys
import atpy
import numpy
import matplotlib as plt
from pylab import *
import time

verbose='N'
# This is the location of the Kappa Scripts on Caleb's Mac
func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        if not verbose == 'N':
            print "The path to programs and functions exists"
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)
    print "The path "+func_dir+" has been added to sys.path"
    
from calibration import LOcal
from operator    import itemgetter
from regrid      import regrid
from conv        import conv

########################################
###### Magnet Calibration Options ######
########################################
verbose='Y'
do_NewLOCal  = True
# For New Calibrations Only
LO_val          = 672
IF_band         = 1.42
biaspot_feedoff = range(63000, 58000, -20)
biaspot_feedon  = range(60000, 54000, -20) 
UCAs            = numpy.arange(3.00, 4.501, 0.01)  
filenotes       = "1"
NumOfMeasu      = 9 # should be an odd number for Median calulation

# Plot Options
lineW         = 3
save_plots    = True
show_plots    = True
do_potVSevery = True

# Data Processing Options
regrid_mesh=1 # in pot position
do_conv = False
sigma   = 3 # in pot position 
min_cdf = 0.95 # fraction of Guassian used in kernal calulation

##############################
###### Start the Script ######
##############################

if do_NewLOCal:
    LOcal(filenotes, biaspot_feedoff, biaspot_feedon, UCAs, NumOfMeasu, IF_band, LO_val)

for m in range(2):
    if m == 0:
        feedback_str=_feedbackOFF
        biaspot=biaspot_feedoff
    else:
        feedback_str=_feedbackON
        biaspot=biaspot_feedon
    for n in range(len(biaspot)):
        savefile    = filedir + "LOcal_LO"+str(LO_val)+"_IF"+str(IF_band)+"_biaspot"+str(biaspot[q])+feedback_str+"_notes"+filenotes 
        
        raw = atpy.Table(savefile+".csv", type="ascii", delimiter=",")

    data      = numpy.zeros(numpy.shape(raw))
    data[:,0] = raw.UCA
    data[:,1] = raw.mV_mean
    data[:,2] = raw.uA_mean
    data[:,3] = raw.mV_median
    data[:,4] = raw.uA_median
    data[:,5] = raw.mV_stdev
    data[:,6] = raw.uA_stdev

    raw_data=data
    
    status=False
    regrid_data, status = regrid(data, regrid_mesh, verbose)
    if status == False:
        print "The function regrid failed, exiting this script"
        sys.exit()
    data = regrid_data
    
    if do_conv:
        status=False
        conv_data, status = conv(data, regrid_mesh, min_cdf, sigma, verbose)
        if not status:
            print "The function conv failed, exiting this script"
            sys.exit()
        data=conv_data
        
    ###########################
    ###### Plotting Part ######
    ###########################
    max_uA=max(data[:,2])
    min_uA=min(data[:,2])
    max_mV=max(data[:,1])
    min_mV=min(data[:,1])
    
    uA_scale = max_uA - min_uA
    mV_scale = max_mV - min_mV
    
    if do_potVSevery:
        plt.clf()
        
        plt.plot(data[:,0], data[:,2] , linewidth=lineW, color = 'red', label='mean uA')
        plt.plot(data[:,0], data[:,4] , linewidth=lineW, color = 'orange', label='median uA')
        plt.plot(data[:,0], data[:,1]*(V_scale/mA_scale) , linewidth=lineW, color = 'blue', label='mean mV')
        plt.plot(data[:,0], data[:,3]*(V_scale/mA_scale) , linewidth=lineW, color = 'green', label='median mV')
        
        #plt.xlim(xaxis_min,xaxis_max)
        plt.ylim(-50,50)
        rcParams['legend.fontsize'] = 10
        plt.legend(loc=0)
        plt.xlabel('UCA Value')
        plt.ylabel('Everthing Else, Normalized to Curent uA')
        plt.title("LO Calibration")
        if show_plots:
            plt.show()
            plt.draw()
            time.sleep(1)
        if save_plots:
            savefig(savefile+".png")
            print "Plot saved as :"+savefile+".png"
