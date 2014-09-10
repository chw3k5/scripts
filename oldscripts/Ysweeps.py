#import telnetlib
#import atpy
#import time
import subprocess
from pylab import *
import numpy
#import glob
#import scipy.stats
#from collections import Counter
import sys
import os
import datetime

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
    
from YfactorGuts     import YfactorGuts
from setmag          import setmag
from LabJackU3_DAQ0  import LabJackU3_DAQ0 
import StepperControl
from zeropots        import zeropots
from get_files       import get_files
from offMeasurement  import offMeasurement
from hotMeasurement  import hotMeasurement
from coldMeasurement import coldMeasurement
from email_sender    import email_caleb

###################################
######### General Options #########
###################################

setNum = 7

verbose='N' # Y, N, T (test)
datadir     = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setNum)+'/'
Ynum        = 1    # change this everytime you write to the same directory, it makes a group of sweeps for a given Yfactor
sweepNstart = 1   # change every sweep, this sould be unique for each sweep
Offnum      = setNum

doWide            = True
doNarrow          = True
doNewOff          = True
Y_CalcandPlot     = False
zeroall           = True # False just zeros the SIS bias

speak1 = "Put the Stepper Motor in the 300 kay measurement position"
speak2 = "Turn off the double you bee eh 23"
speak3 = "Turn the double you bee eh 23 back on now"
speak4 = "All sweeps are now complete"

#################################
######### Sweep Options #########
#################################

LO          = 672   # must be a number
IFband      = 1.42  # must be a number
MagSweeps   = range(0, 30001, 2500) # range(0,3000,200) # (Start pot position, end pot position, pot step size) # (0,1,1)
UCA_Sweeps  = numpy.arange(3.64, 3.90 ,0.03) # numpy.arange(3.70,3.40,-0.02) # in Volts (Start voltage, end voltage, pot voltage step size) # (3.53,3.54,1)
#UCA_Sweeps   =numpy.array([3.77])

num_of_magsweeps = len(MagSweeps)
num_of_UCAsweeps = len(UCA_Sweeps)
totalsweeps      = num_of_UCAsweeps*num_of_magsweeps

# for the Off mearsuement only
LO_off      = 672   # (GHz) must be a number 
IFband_off  = 1.420 # (GHz) must be a number 
magpot_off  = 25000     # must be a number
UCA_vOff    = 3.75  # must be a number

#sweep 0 65100 52600 500
WideSweepStart   = 65100 # defualt 65100
WideSweepStop    = 52600 # defualt 52600
WideSweepStep    = 25    # defualt 25
NarrowSweepStart = 60000 # defualt 60000
NarrowSweepStop  = 54000 # default 55000
NarrowSweepStep  = 20     # default 10


############################
####### Plot Options #######
############################
show_plots=False
save_plots=True
tp_plots=True
wide_lineW=1
narrow_lineW=3

###########################################
######### Data Processing Options #########
###########################################

mono_switcher=True # makes data monotonic in mV

do_regrid=True
regrid_mesh=0.01 # in mV (default = 0.01)

do_conv = True
sigma   = 0.05 # in mV
min_cdf = 0.95 # fraction of Guassian used in kernal calulation

do_yfactor=True
start_Yrange = 1.2 # in mV
end_Yrange   = 2.0 # in mV

###########################################
######### Email Sending Options #########
###########################################
send_5min_email     = True
send_1hour_email    = True
send_4hour_email    = True
send_8hour_email    = False
send_finished_email = True
fin_subject   = "Mearsurment Finished"
fin_body_text = "Your Mearsurment finisded and zerod the pots before sending this email"

#####################################################
################## Start of Script ##################
#####################################################

# Make correct directorys if they do not exist
if not os.path.isdir(datadir):
    os.makedirs(datadir)
    os.makedirs(datadir+'/plots')   
    os.makedirs(datadir+'/data')
if not os.path.isdir(datadir+'/plots'):
    os.makedirs(datadir+'/plots')
if not os.path.isdir(datadir+'/data'):
    os.makedirs(datadir+'/data')
    
start_time  = datetime.datetime.now()


########## Set up stepper Motor
status = StepperControl.initialize()
if status == False:
    print "The function StepperControlinitialize failed, exiting this script"
    sys.exit()  


N = sweepNstart
########## Do the Off sweeps first
if doNewOff:
    ### set UCA voltage
    status = LabJackU3_DAQ0(abs(UCA_vOff))
    if status == False:
        print "The function LabJackU3_DAQ0 failed, exiting this script"
        sys.exit()
    ### set the magnet pot position
    status, mA_mag, V_mag = setmag(magpot_off)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    # Pause and speck to me to turn WBA23 off
    subprocess.call(['say', speak2])
    raw_input('Turn OFF the WBA23 (1st LNA), then hit Enter to continue...')
    # remove files that aready have the same Y number
    search_str="*_OFF"+str('%02.f' % Offnum)+"_*"
    files = []
    status   = False
    files, status = get_files(datadir, search_str, False, 'N' )
    if not files == []:
        print 'Removing Old OFF'+str('%02.f' % Offnum)+ ' files'
        for zz in range(len(files)):
            temp_str='rm '+str(files[zz])
            os.system(temp_str)
        
    N = offMeasurement(doWide, doNarrow, N, datadir, LO_off, IFband_off, magpot_off, mA_mag, UCA_vOff, Offnum, WideSweepStart, WideSweepStop, WideSweepStep, NarrowSweepStart, NarrowSweepStop, NarrowSweepStep)
    
    # Pause and speck to me to turn WBA23 back on after completing the power off measurments 
    subprocess.call(['say', speak3])
    raw_input('Turn ON the WBA23 (1st LNA), then hit Enter to continue...')
    
########## End of the Off measurments 

########## Start the Giant loops of parameter's to sweep

for y in range(num_of_magsweeps):
    ### set the magnet pot position
    magpot = MagSweeps[y]
    status, mA_mag, V_mag = setmag(magpot)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    
    for z in range(num_of_UCAsweeps):
        # remove files that aready have the same Y number
        search_str="*_Y"+str('%03.f' % Ynum)+"_*"
        files = []
        status   = False
        files, status = get_files(datadir, search_str, False, 'N' )
        if not files == []:
            print 'Removing Old Y'+str('%02.f' % Ynum)+ ' files'
            for zz in range(len(files)):
                temp_str='rm '+str(files[zz])
                os.system(temp_str)
        
        ### set UCA voltage
        UCA_voltage = UCA_Sweeps[z]
        status = LabJackU3_DAQ0(abs(UCA_voltage))
        if status == False:
            print "The function LabJackU3_DAQ0 failed, exiting this script"
            sys.exit()
            
        current_sweep = y*num_of_UCAsweeps+z+1
        now_time  = datetime.datetime.now()
        elapsed_time = now_time - start_time
        days = elapsed_time.days
        secs = elapsed_time.seconds
        
        if not days == 0:            
            secs = secs + days*86400
            
        SecsPerSweep   = secs/current_sweep
        r_secs = (totalsweeps - current_sweep)*SecsPerSweep
        
        hours = numpy.floor(secs/3600)
        secs  = numpy.mod(secs,3600)
        mins  = numpy.floor(secs/60)
        secs  = numpy.mod(secs,60)
        
        r_hours = numpy.floor(r_secs/3600)
        r_secs  = numpy.mod(r_secs,3600)
        r_mins  = numpy.floor(r_secs/60)
        r_secs  = numpy.mod(r_secs,60)
        
        if (send_5min_email and (mins >= 5 or hours >= 1)):
            send_5min_email = False
            email_caleb('5 minute email', str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time')
        if (send_1hour_email and (hours >= 1)):
            send_1hour_email = False
            email_caleb('1 hour email', str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time')
        if (send_4hour_email and hours >= 4):
            send_4hour_email = False
            email_caleb('4 hour email', str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time')
        if (send_8hour_email and hours >= 8):
            send_8hour_email = False
            email_caleb('8 hour email', str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time')
        
        print "Doing Y factor "+str(current_sweep)+' of '+str(totalsweeps)+'  '+str('%02.f' % hours)+' hrs  '+str('%02.f' % mins)+' mins  '+str('%02.f' % secs)+' secs have elespsed'
        print str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time'
        print 'LO'+str('%3.f' % LO)+'_IFband'+str('%1.3f' % IFband)+'_magpot'+str('%06.f' % magpot)+str('%02.3f' % mA_mag)+'_UCA'+str('%1.3f' % UCA_voltage)
        print ' ' 
        ########## Start 300 K measurement
        N = hotMeasurement(doWide, doNarrow, N, datadir, LO, IFband, magpot, mA_mag, UCA_voltage, Ynum, Offnum, WideSweepStart, WideSweepStop, WideSweepStep, NarrowSweepStart, NarrowSweepStop, NarrowSweepStep)
        
        ### Move the Chopper
        status = StepperControl.GoForth()
        if status == False:
            print "The function StepperControl.GoForth() failed, exiting this script"
            sys.exit()
        
        ########## Start 77K measurements 
        N = coldMeasurement(doWide, doNarrow, N, datadir, LO, IFband, magpot, mA_mag, UCA_voltage, Ynum, Offnum, WideSweepStart, WideSweepStop, WideSweepStep, NarrowSweepStart, NarrowSweepStop, NarrowSweepStep)

        ### Move the Chopper
        status = StepperControl.GoForth()
        if status == False:
            print "The function StepperControl.GoForth() failed, exiting this script"
            sys.exit()
        ########### End of data gathering
    
        #######################
        ####################### Y Factor calulator and Plotting  
        #######################
        # Y factor calculations and plot options
        if Y_CalcandPlot: 
            status = YfactorGuts(datadir, verbose, 'Y'+str('%03.f' % Ynum), Offnum, '*.csv', show_plots, save_plots, tp_plots, wide_lineW, narrow_lineW, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf, do_yfactor, start_Yrange, end_Yrange)
            if status == False:
                print "The function YfactorGuts failed, exiting this script"
                print "the data was for set for "+Ynum
                sys.exit()
        Ynum = Ynum+1
        ######## End of loops

status = StepperControl.DisableDrive()
if status == False:
    print "The function StepperControlinitialize failed, exiting this script"
    sys.exit()
status = LabJackU3_DAQ0(0)
zeropots()

if send_finished_email:
    email_caleb(fin_subject, fin_body_text)

subprocess.call(['say', speak4])
print "The script has reached the end"  