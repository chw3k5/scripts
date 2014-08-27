# This is the calibration file for the ElectroMag. Use this file to 
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
    
from calibration import magcal
from operator    import itemgetter
from regrid      import regrid
from conv        import conv

########################################
###### Magnet Calibration Options ######
########################################
verbose='Y'
do_NewMagCal  = True
# For New Calibrations Only
filename      = "magcal.csv"
potstep       = 1000
MesPerPot     = 9 # should be an odd number for Median calulation

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
rawfilename='raw_'+filename

if do_NewMagCal:
    magcal(rawfilename, potstep, MesPerPot)
    
raw = atpy.Table("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/mag/"+rawfilename, type="ascii", delimiter=",")

data      = numpy.zeros(numpy.shape(raw))
data[:,0] = raw.pot
data[:,1] = raw.V_mean
data[:,2] = raw.mA_mean
data[:,3] = raw.V_median
data[:,4] = raw.mA_median
data[:,5] = raw.V_stdev
data[:,6] = raw.mA_stdev

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
max_mA=max(data[:,2])
min_mA=min(data[:,2])
max_V=max(data[:,1])
min_V=min(data[:,1])

mA_scale = max_mA - min_mA
V_scale  = max_V  - min_V

if do_potVSevery:
    plt.clf()
    
    plt.plot(data[:,0], data[:,2] , linewidth=lineW, color = 'red', label='mean mA')
    plt.plot(data[:,0], data[:,4] , linewidth=lineW, color = 'orange', label='median mA')
    plt.plot(data[:,0], data[:,1]*(V_scale/mA_scale) , linewidth=lineW, color = 'blue', label='mean V')
    plt.plot(data[:,0], data[:,3]*(V_scale/mA_scale) , linewidth=lineW, color = 'green', label='median V')
    
    #plt.xlim(xaxis_min,xaxis_max)
    plt.ylim(-50,50)
    rcParams['legend.fontsize'] = 10
    plt.legend(loc=0)
    plt.xlabel('Pot Value')
    plt.ylabel('Everthing Els,e Normalized to Curent mA')
    plt.title("Magnet Calibration")
    if show_plots:
        plt.show()
        plt.draw()
        time.sleep(1)
    if save_plots:
        savefig("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/mag/plot.png")
        print "plot saved to: /Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/mag/plot.png"
