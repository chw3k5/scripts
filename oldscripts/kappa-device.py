# For ploting the data of dipped devices. Updated March 10, 2014

import atpy
from matplotlib import *
from pylab import *
import numpy
import scipy.stats
import time
import sys
from get_files    import get_files
from operator     import itemgetter
from regrid       import regrid
from conv         import conv
from derivative   import derivative
from findlinear   import findlinear
from resfitter    import resfitter

verbose = 'Y'

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

########## Data Options ############
verbose = 'Y'

do_Qfactor    = False # may not be working/updates

mono_switcher = True # makes data monotonic in mV

do_regrid     = True
regrid_mesh   = 0.005 # in mV (default = 0.01)

do_conv       = True
sigma         = 0.03 # in mV (0.03 mV)
min_cdf       = 0.95 # fraction of Guassian used in kernal calulation

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
linif=1.1 # y'' is linear if it is below this fraction of the max( abs( y''))

do_old_script = False

datadir     = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/dip/'
load_search_str = 'NA38_warm.csv' # load files that match this search string in the folder 'datadir'
load_params     = False # load files from a list in a file called params.csv


########## Plot options ############
plt.clf()

plot_final_data   = True
over_plot         = False # for making plots with all devices
save_plot         = True

# these are for testing and comparison to final data which is the results of the options above
plot_raw_data     = False
plot_mono_data    = False
plot_regrid_data  = False
plot_conv_data    = False
plot_1stderiv     = False
plot_1stderivconv = False
plot_2ndderiv     = False
plot_2ndderivconv = False
plot_lin_lines    = True


##################################
######## Start the script ########
##################################

#####
##### get the file names of the data that is to be analyzed
#####
csvfiles = []
status   = False
csvfiles, status = get_files(datadir, load_search_str, load_params, verbose )
if status == False:
    print "The function get_files failed, exiting this script"
    sys.exit()

    
#Open a file to write all of the device names and their q-factor
if do_Qfactor:
    plfile = open("qfactors.csv",'w')
    plfile.write("device, Q\n")


#Loop through all of the device files
for file in csvfiles:
    ############## 
    ############## get the data and assign it convinent names
    ##############  
    dev = atpy.Table(file, type="ascii", delimiter=",")
    print file
    mV = dev.mV
    uA = dev.uA
    ShortName=file[len(file)-8:len(file)-4]
    
    ############## 
    ############## make date monotonic in mV
    ##############
    if mono_switcher:
        data      = numpy.zeros((len(mV),2))
        data[:,0] = mV
        data[:,1] = uA
        mono_data = numpy.asarray(sorted(data, key=itemgetter(0))) 
        mono_mV   = mono_data[:,0]
        mV        = mono_mV
        mono_uA   = mono_data[:,1]
        uA        = mono_uA
        
    ############## 
    ############## Regrid the data
    ##############
    if ((do_regrid == True) and (mono_switcher==True)): 
        data      = numpy.zeros((len(mV),2))
        data[:,0] = mV
        data[:,1] = uA
        status=False
        regrid_data, status = regrid(data, regrid_mesh, verbose)
        if status == False:
            print "The function regrid failed, exiting this script"
            print "the data was from "+file
            sys.exit()
        regrid_mV = regrid_data[:,0]
        mV        = regrid_mV
        regrid_uA = regrid_data[:,1]
        uA        = regrid_uA
        
    ############## 
    ############## convolve the data
    ##############
    if ((do_conv) and (do_regrid == True) and (mono_switcher==True)): 
        data      = numpy.zeros((len(mV),2))
        data[:,0] = mV
        data[:,1] = uA
        status=False
        conv_data, status = conv(data, regrid_mesh, min_cdf, sigma, verbose)
        if not status:
            print "The function conv failed, exiting this script"
            print "the data was from "+file
            sys.exit()
        conv_mV = conv_data[:,0]
        mV      = conv_mV
        conv_uA = conv_data[:,1]
        uA      = conv_uA
        
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
    
                if do_Qfactor:
                    plfile.write("%s, " % ShortName)
                    plfile.write("%f\n" % qq)   #
                   

    
    
    ###########################################
    ################ Plot Data ################
    ###########################################
    if over_plot:
        plt.plot(mV, uA, linewidth=1, label=ShortName)
        plt.legend(loc=0)
        rcParams['legend.fontsize'] = 10
        plt.xlim(0.,6.)
        plt.ylim(-50.,200)
        plt.xlabel('Voltage (mV)')
        plt.ylabel('Current (uA)')
        plt.show()
    else:
        plt.clf()
        plt.plot(dev.mV, dev.uA, linewidth=3, color = "orange", label='data')
        
        if plot_raw_data:
            plt.plot(dev.mV, dev.uA, linewidth=1, color = "purple", label='raw data')
            
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
                    

        plt.title("Device: "+ShortName + " Ratio: "+str('%2.2f' % qq))
        # plt.xlim(0.,6.)
        # plt.ylim(-50.,max(dev.uA)+20.)
        plt.legend(loc=0)
        rcParams['legend.fontsize'] = 12
        plt.xlabel('Voltage (mV)')
        plt.ylabel('Current (uA)')
        
        plt.show()
        plt.draw()
        time.sleep(1)
        if save_plot:
            savefig(datadir+'plots/'+ ShortName+".png")
            
        
if do_Qfactor:
    pfile.close()

if save_plot:
    if over_plot:
        savefig(datadir+'plots/over_plots.png')
        
# print "I love you, Stinky."