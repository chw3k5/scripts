import telnetlib
import time
from pylab import *
import numpy
import glob
import scipy.stats
import sys
import os
import atpy
from operator import itemgetter

from get_files      import get_files
from regrid         import regrid
from conv           import conv
from derivative     import derivative
from findlinear     import findlinear
from resfitter      import resfitter
from Y_jobs2        import ReadInSettings1

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

##############################
####### Other Options ########
##############################

verbose='N' 
datadir     = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/magsweep/'
search_str='*.csv' # The search string for finding files


################################
####### Start of Script ######## 
################################



#####
##### get the file names of the data that is to be analyzed
#####
csvfiles = []
status   = False
csvfiles, status = get_files(datadir, search_str, False, verbose )
if status == False:
    print "The function get_files failed, exiting this script"
    sys.exit()
    
for n in range(len(csvfiles)):
################ the data processing part of the script.
        LO, IFband, magpot,  UCA_val, sweepTemp, sweepN, status = ReadInSettings1(csvfiles[n])
        mA_mag='0'
        raw_data = atpy.Table(csvfiles[n], type="ascii", delimiter=",")
        raw_mV = raw_data.mV
        raw_uA = raw_data.uA
        raw_tp = raw_data.tp

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
        rcParams['legend.fontsize'] = 10
        plt.legend(loc=0)
        plt.xlabel('Voltage (mV)')
        plt.ylabel('Current (uA)')
        plt.title("LO"+LO+" IFband"+IFband+" magpot"+magpot+"@"+mA_mag+"mA UCA:"+UCA_val)
        if show_plot:
            plt.show()
            plt.draw()
            time.sleep(1)
        if save_plots:
            saveplotdir=datadir+'plots/'+sweepN+'_LO'+LO+'_IFband'+IFband+'_magpot'+ magpot+'_mag'+mA_mag+'mA_'+'_UCA'+UCA_val+'_'+sweepTemp+".png"
            savefig(saveplotdir)
            print "plot saved to: "+saveplotdir
   
# after the loops have finished      
tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
tn.write('feedback 0 \n')
time.sleep(1)
tn.write('zeropots \n')
time.sleep(1)
tn.close()
### Not finished yet