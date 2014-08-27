import telnetlib
import time
from pylab import *
import numpy
import glob
import scipy.stats
import sys
import os
from operator import itemgetter

from domath         import regrid, conv, derivative, findlinear, resfitter
from setmagI        import setmag
from setfeedback    import setfeedback

from control import LabJackU3_DAQ0, setmagI, setfeedback
from IVsweeps       import IVsweeps



############################
####### Plot Options #######
############################

plt.clf()
save_plots = True
plot_uA    = True
plot_tp    = True
stack_plot = False
show_plot  = False 
lineW      = 5

# these are for testing and comparison to final data which is the results of the options above
plot_raw_data     = True
plot_mono_data    = False
plot_regrid_data  = False
plot_conv_data    = False
plot_1stderiv     = False
plot_1stderivconv = False
plot_2ndderiv     = False
plot_2ndderivconv = False
plot_lin_lines    = True

#############################
####### Sweep Options #######
#############################

verbose='N' 
datadir     = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/magsweep/'
LO          = '672'
IFband      = '1.42' 
sweepTemp   = '4K'
notes       = ''
sweepNstart = 143   # change every sweep, this sould be unique for each sweep

feedback   = False


if feedback:
    SweepStart    = 65000  # defult is 60000 for feedback on
    SweepStop     = 52000  # defult is 55000 for feedback on (This doen't need exactly right, it will get reset if it is not a multiple of SweepStep)
    SweepStep     = 50     # defult is 25
elif not feedback:
    SweepStart    = 65100  # defult is 65100 for feedback off 
    SweepStop     = 57000  # defult is 62000 for feedback off, (This doen't need exactly right, it will get reset if it is not a multiple of SweepStep)
    SweepStep     = 25     # defult is 50
else:
    print "feedback not set to True or False"
    sys.exit()

#UCASweeps = arange(3.60, 4.00, 0.03) # must be a number (Volts)
UCASweeps = arange(3.45751953, 3.458, 0.01) # must be a number (Volts)
num_of_UCAsweeps=len(UCASweeps)

#MagSweeps = range(0, 16000, 500)
MagSweeps=range(20000,20001,5)
num_of_magsweeps=len(MagSweeps)


#######################################
####### Data Processing options #######
#######################################

mono_switcher=True # makes data monotonic in mV

do_regrid=True
regrid_mesh=0.01 # in mV (default = 0.01)

do_conv = True
sigma   = 0.03 # in mV
min_cdf = 0.95 # fraction of Guassian used in kernal calulation

do_1stderiv      = True
int_1stderiv     = 1
do_conv1stderiv  = True
sigma_1stderiv   = 0.10 # in mV (0.10 mV)
min_cdf_1stderiv = 0.80 # fraction of Guassian used in kernal calulation

do_2ndderiv      = True
int_2ndderiv     = 1
do_conv2ndderiv  = True
sigma_2ndderiv   = 0.01 # in mV (0.10 mV)
min_cdf_2ndderiv = 0.80 # fraction of Guassian used in kernal calulation

do_findlinear    = True # find the linear regoins using the 2nd derivative
linif=0.3 # y'' is linear if it is below this fraction of the max( abs( y''))


####### this is the part where we talk to the thzbias computer

# feedback is turned on of off here
status = setfeedback(feedback)
if status == False:
    print "The function setfeedback failed, exiting this script"
    sys.exit()
    
    
### Start of UCA voltage Sweeping loop
for m in range(num_of_UCAsweeps):
    UCA_voltage=UCASweeps[m]
    status = LabJackU3_DAQ0(abs(UCA_voltage))
    if status == False:
        print "The function LabJackU3_DAQ0 failed, exiting this script"
        sys.exit()
 
    ############## Start of the magnet sweeping loop    
    for n in range(num_of_magsweeps):
        if (n==0 and m==0):
            sweepN=sweepNstart
        else:
            sweepN=sweepN+1
            
        magpot=MagSweeps[n]
        fullname=datadir+'LO'+LO+'_IFband'+IFband+'_magpot'+str('%06.f' % magpot)+'_UCA'+str('%1.3f' % UCA_voltage)+'_'+sweepTemp+'_'+notes+'_'+str('%04.f' % sweepN)
        print 'Sweep '+str((m)*(n+1)+(n+1))+' of '+str(num_of_UCAsweeps*num_of_magsweeps)
        
        ### set the magnet pot position
        
        status, mA_mag, V_mag = setmag(magpot)
        if status == False:
            print "The function setmag failed, exiting this script"
            sys.exit()
        
        ############### Start Bias Sweep
        # do the sweep
        status, raw_mV, raw_uA, raw_tp = IVsweeps(SweepStart, SweepStop, SweepStep, feedback, fullname)
        if status == False:
            print "The function IVsweeps failed, exiting this script"
            sys.exit()    
        
        ################ the data processing part of the script.
        if mono_switcher:
            data=numpy.zeros((len(raw_mV),3))
            data[:,0]=raw_mV
            data[:,1]=raw_uA
            data[:,2]=raw_tp
    
            mono_data = numpy.asarray(sorted(data, key=itemgetter(0)))
    
            mV_mono=mono_data[:,0]
            uA_mono=mono_data[:,1]
            tp_mono=mono_data[:,2]
            mV=mV_mono
            uA=uA_mono
            tp=tp_mono
        else:
            mV=raw_mV
            uA=raw_uA
            tp=raw_tp
            
        if do_regrid:
            if not mono_switcher:
                print "mono switch needs to be turned on before doing a regrid of the data, exiting this scrip"
                sys.exit()
            data=numpy.zeros((len(mV),3))
            data[:,0]=mV
            data[:,1]=uA
            data[:,2]=tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                sys.exit()
            mV_regrid=regrid_data[:,0]
            uA_regrid=regrid_data[:,1]
            tp_regrid=regrid_data[:,2]
            mV=mV_regrid
            uA=uA_regrid
            tp=tp_regrid
            
        if do_conv:
            data=numpy.zeros((len(mV),3))
            data[:,0]=mV
            data[:,1]=uA
            data[:,2]=tp
            status=False
            conv_data, status = conv(data, regrid_mesh, min_cdf, sigma, verbose)
            if not status:
                print "The function conv failed, exiting this script"
                sys.exit()
            uA=conv_data[:,1]
            tp=conv_data[:,2]
            
        ############## 
        ############## the derivative calulations
        ##############
        
        ##### 1st derivative
        if ((do_1stderiv) and (do_conv) and (do_regrid == True) and (mono_switcher==True)):
            data      = numpy.zeros((len(mV),2))
            data[:,0] = mV
            data[:,1] = uA
            status=False
            status, deriv1_data= derivative(data, int_1stderiv)
            if not status:
                print "The function derivative (1st) failed, exiting this script"
                print "the data was from "+file
                sys.exit()
            deriv1_mV = deriv1_data[:,0]
            deriv1_uA = deriv1_data[:,1]
            
            ##### convolution for 1st derivative 
            if do_conv1stderiv:
                data      = numpy.zeros((len(deriv1_mV),2))
                data[:,0] = deriv1_mV
                data[:,1] = deriv1_uA
                status=False
                conv_data, status = conv(data, regrid_mesh, min_cdf_1stderiv, sigma_1stderiv, verbose)
                if not status:
                    print "The function conv failed within the 1st derivative calculation, exiting this script"
                    print "the data was from "+file
                    sys.exit()
                deriv1_conv_mV = conv_data[:,0]
                deriv1_conv_uA = conv_data[:,1]
                
            ##### 2nd derivative
            if do_2ndderiv:
                if do_conv1stderiv:
                    data      = numpy.zeros((len(deriv1_conv_mV),2))
                    data[:,0] = deriv1_conv_mV
                    data[:,1] = deriv1_conv_uA
                else:
                    data      = numpy.zeros((len(deriv1_mV),2))
                    data[:,0] = deriv1_mV
                    data[:,1] = deriv1_uA
                status=False
                status, deriv2_data= derivative(data, int_2ndderiv)
                if not status:
                    print "The function derivative (2nd) failed, exiting this script"
                    print "the data was from "+file
                    sys.exit()
                deriv2_mV = deriv2_data[:,0]
                deriv2_uA = deriv2_data[:,1]
                
                ##### convolution for 2nd derivative 
                if do_conv2ndderiv:
                    data      = numpy.zeros((len(deriv2_mV),2))
                    data[:,0] = deriv2_mV
                    data[:,1] = deriv2_uA
                    status=False
                    conv_data, status = conv(data, regrid_mesh, min_cdf_2ndderiv, sigma_2ndderiv, verbose)
                    if not status:
                        print "The function conv failed within the 2nd derivative calculation, exiting this script"
                        print "the data was from "+file
                        sys.exit()
                    deriv2_conv_mV = conv_data[:,0]
                    deriv2_conv_uA = conv_data[:,1]
                    
                if do_findlinear:
                    if do_conv2ndderiv:
                        x       = deriv2_conv_mV
                        ydprime = deriv2_conv_uA
                    else:
                        x       = deriv2_mV
                        ydprime = deriv2_uA
        
                    status, lin_start, lin_end = findlinear(x, ydprime, linif, verbose)
                    if not status:
                        print "The function findlinear failed, exiting this script"
                        print "the data was from "+file
                        sys.exit()
                    
                    slopes, bestfits_mV, bestfits_uA = resfitter(mV, uA, lin_start, lin_end)
                    res=(1/slopes)*1000
                    con=1/res
                    qq = res[len(lin_end)-1]/res[len(lin_end)-2]
    
    
        # the plotting part
        if not stack_plot:
            plt.clf()
        
        yaxis_top=max(max(uA),max(tp))
        yaxis_bot=min(min(uA),min(tp))
        xaxis_max=max(mV)
        xaxis_min=min(mV)
        xaxis_size=xaxis_max-xaxis_min
        
        yaxis_size=yaxis_top-yaxis_bot
        yaxis_max=yaxis_top + 0.1*yaxis_size
        yaxis_min=yaxis_bot - 0.1*yaxis_size
    
        tp_scale=yaxis_top/max(tp)
    
        
    
        if plot_uA:    
            plt.plot(mV, uA         , linewidth=lineW, color = 'orange', label='IV')        
            if plot_raw_data:
                plt.plot(raw_mV, raw_uA, linewidth=2, color = "purple", label='raw data')
    
            
            
            if (plot_mono_data and mono_switcher):
                plt.plot(mono_mV, mono_uA, linewidth=1, color = "red", label='mono data')
            
            if (plot_regrid_data and do_regrid and mono_switcher):
                plt.plot(regrid_mV, regrid_uA, linewidth=1, color = "yellow", label='regrid data')
            
            if (plot_conv_data and do_conv and do_regrid and mono_switcher):
                plt.plot(conv_mV, conv_uA, linewidth=1, color = "blue", label='conv data')
            
            if (do_1stderiv and do_conv and do_regrid and mono_switcher):
                if (plot_1stderiv):
                    plt.plot(deriv1_mV, deriv1_uA, linewidth=1, color = "green", label='1st deriv')
                if (plot_1stderivconv and do_conv1stderiv):
                    plt.plot(deriv1_conv_mV, deriv1_conv_uA, linewidth=1, color = "red", label='1st deriv conv')
                if do_2ndderiv:
                    if (plot_2ndderiv):
                        plt.plot(deriv2_mV, deriv2_uA, linewidth=1, color = "blue", label='2st deriv')
                    if (plot_2ndderivconv and do_conv2ndderiv):
                        plt.plot(deriv2_conv_mV, deriv2_conv_uA, linewidth=1, color = "yellow", label='2st deriv conv')            
                    if plot_lin_lines:
            	       for ii in range(len(lin_end)):
                            plt.plot(bestfits_mV[:,ii],bestfits_uA[:,ii], linewidth=1, color = "black", label = str('%3.1f' % res[ii]) + ' Ohms')
        if plot_tp:
            plt.plot(mV, tp*tp_scale, linewidth=lineW, color = 'blue', label='TP')              
            if plot_raw_data:
                plt.plot(raw_mV, raw_tp*tp_scale, linewidth=2, color = "dodgerblue", label='tp raw data')

    
        plt.xlim(xaxis_min,xaxis_max)
        plt.ylim(yaxis_min,yaxis_max)
        rcParams['legend.fontsize'] = 14
        plt.legend(loc=0)
        plt.xlabel('Voltage (mV)')
        plt.ylabel('Current (uA)')
        plt.title("LO"+LO+" IFband"+IFband+" magpot"+str(magpot)+str('%02.3f' % float(mA_mag))+" UCA:"+str(UCA_voltage))
        if show_plot:
            plt.show()
            plt.draw()
            time.sleep(1)
        if save_plots:
            saveplotdir=datadir+'plots/'+str('%04.f' % sweepN)+'LO'+LO+'_IFband'+IFband+'_magpot'+str('%06.f' % magpot)+'_mag'+str('%2.4f' % float(mA_mag))+'mA_'+'_UCA'+str('%1.3f' % UCA_voltage)+'_'+sweepTemp+'_'+notes+'_'+".png"
            savefig(saveplotdir)
            print "plot saved to: "+saveplotdir
   
# after the loops have finished      
tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
tn.write('feedback 0 \n')
time.sleep(1)
tn.write('zeropots \n')
time.sleep(1)
tn.close()
    