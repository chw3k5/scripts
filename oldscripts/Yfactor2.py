# 2nd Y factor calculator and Plot Maker created February 7, 2014

# Notes
# Y parameter CSV Files come in a varitiy of flavors with up to 6 files.
# For a single Y number (Y##), seen in the names of the files
# the current naming convention is (LNA off, hot load, and cold load)
# corrisponding to (LO###_IFband#.##_magpot#####_UCA#.##_W300K_Y##_####, 
# or LO###_IFband#.##_magpot#####_UCA#.##_NOff_Y##_####).
# Sweeps can be wide (W) or narrow (N); this is the Letter before the Y number.
# At least 3 files must be present LNA off, hot, and cold. Also I expect the 
# the files to either be all (W) or (N), but the code is made to either or both.
# If all 6 files are present and selected below, the Y-factor will be calculated
# from the (N) files and the (W) files will be only be plotted.

# Having more than one 'Y' in the filename will return bad results
# However, having any number of 'Y's in the directory path is fine

import atpy
from pylab import *
import numpy
import glob
import scipy.stats
import time
from collections import Counter
import sys

print "Y factor calculator and Plot Maker created October 29, 2013"

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
    
# Now I import the scripts functions and programs that I have made to make my life easier
    
#from happybirthday import happyBirthdayEmily # This is a test program the prints the birthday song
from csvFormat    import csvFormat
from get_files    import get_files
from find_Ynums   import find_Ynums
from Y_jobs2      import Y_jobs2
from mono_switch  import mono_switch
from regrid       import regrid
from data2Yfactor import data2Yfactor
from Yfac_plotter import Yfac_plotter

#####
##### location of IV and TP parameter files, the data files
#####
#dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/LO_sweeps_set1/'
#dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/mag_sweeps_set2/'
#dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/LO_hot_cold_sweeps_set3/'
#dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/LO_hot_cold_sweeps_set4/'
#dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/LO_hot_cold_sweeps_set5/'
dir='/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/set6/'


#####
##### Here we make sure the csv files are formated in the way this script needs 
#####
verbose='N' # Y, N, T (test)
search_str='*.csv' # The search string for finding files
status = False
status = csvFormat(dir, search_str, verbose )
if status == False:
    print 'csvFormat has failed, exiting this script'
    sys.exit()

#############################
############################# Here are all the options for this script
#############################

verbose='Y' # Y, N, T (test)

# plot options 
show_plots=True
save_plots=True
tp_plots=True
wide_lineW=1
narrow_lineW=3


mono_switcher=True # makes data monotonic in mV, this switches values until the data is monotonic
mono_mesh=0.0000001 # (default = 0.000001)  threshhold for when things are equal in switcher
max_equal=1000 # (default = 100) the maximum times mV[n] can equal mV[n+1] before the loop is terminated
max_loop=100000 # (default = 100000) the maximum times the loop can continue before terminating

do_regrid=True
regrid_mesh=0.01 # in mV (default = 0.01)

do_yfactor=True
start_Yrange = 1.5 # in mV
end_Yrange   = 2.3 # in mV

load_params=False # (True or False) Load file names, and possibly other parameters, from params.csv in the folder dir
load_search_str='*.csv' # example Y-factor files: UCA3.55_077K_Y01_N_sweep0107.csv, LNA_off_300K_Y01_W_sweep0105.csv
search_4Ynums=False
if not search_4Ynums:
    Ynums=['Y01'] # make a list array seporate array values with commas like Ynums = ['Y01', 'Y02']

#############################
############################# 
#############################



#####
##### get the file names of the data that is to be analyzed
#####
csvfiles = []
status   = False
csvfiles, status = get_files(dir, load_search_str, load_params, verbose )
if status == False:
    print "The function get_files failed, exiting this script"
    sys.exit()

#####
##### get the Y numbers of the data that was just read in 
#####
# Having more than one 'Y' in the filename will return bad results
# However, having any number of 'Y's in the directory path is fine
if search_4Ynums:
    status   = False
    Ynums=[]
    Ynums, status = find_Ynums(csvfiles, verbose)
    if status == False:
        print "The function get_files failed, exiting this script"
        sys.exit()
    if not Ynums:
        print "No Y numbers where returned by find_Ynums, exiting the script"
	sys.exit()

#####
##### Start the Giant Loop for different Y-factor sweeps
#####
if not verbose == 'N':
    print "Starting the Giant Y-factor loop; here we go!"
    print " "
for n in range(len(Ynums)): # start Y factor loop
    mV_Yfactor=[]
    max_Yfactor=[]
    mV_max_Yfactor=[]
    LO_val=[]
    IFband_val=[]
    magpot_val=[]
    UCA_val=[]
    wide_off_uA=[]
    wide_hot_uA=[]
    wide_cold_uA=[]
    narrow_off_uA=[]
    narrow_hot_uA=[]
    narrow_cold_uA=[]
    wide_off_tp=[]
    wide_hot_tp=[]
    wide_cold_tp=[]
    narrow_off_tp=[]
    narrow_hot_tp=[]
    narrow_cold_tp=[]
    Yfactor=[]
    wide_off_mV=[]
    wide_hot_mV=[]
    wide_cold_mV=[]
    narrow_off_mV=[]
    narrow_hot_mV=[]
    narrow_cold_mV=[]
    
    Y_search_str="*"+Ynums[n]+search_str
    Y_csvfiles = []
    status   = False
    Y_csvfiles, status = get_files(dir, Y_search_str, False, verbose )
    if status == False:
        print "The function get_files failed, exiting this script"
        sys.exit()

    #####
    ##### Now we discover what kind of data each file has, and we give each file a special name
    #####
    status=False
    wide_off_csv, wide_hot_csv, wide_cold_csv, narrow_off_csv, narrow_off_csv, narrow_hot_csv, narrow_cold_csv, LO_val, IFband_val, magpot_val, UCA_val, status = Y_jobs2(Y_csvfiles)
    if status == False:
        print "The function Y_jobs failed, exiting this script"
        print "This is could be due to improper formating"
        sys.exit()
    
    #####
    ##### Now we need determine if we doing 6(max) files per Y factor or 3 files (min),
    ##### but mostly we just report our finding to the user
    
    if ((not wide_off_csv) or (not wide_hot_csv) or (not wide_cold_csv)):
        wide_missing=True
        if not wide_off_csv:
            print "wide_off_csv is empty, so the data for a wide band LNA off was not found"
        if not wide_hot_csv:
            print "wide_hot_csv is empty, so the data for a wide band hot load was not found"
        if not wide_cold_csv:
            print "wide_cold_csv is empty, so the data for a wide band cold load was not found"
    else:
        wide_missing=False
    if ((not narrow_off_csv) or (not narrow_hot_csv) or (not narrow_cold_csv)):
        narraw_missing=True
        if not narrow_off_csv:
            print "narrow_off_csv is empty, so the data for a narrow band LNA off was not found"
        if not narrow_hot_csv:
            print "narrow_hot_csv is empty, so the data for a narrow band hot load was not found"
        if not narrow_cold_csv:
            print "narrow_cold_csv is empty, so the data for a narrow band cold load was not found"
    else:
        narrow_missing=False
    
    if ((not wide_missing) and (not narrow_missing)): 
        if not verbose == 'N': 
            print "Your papers are in order: All 6 files are found. Narrow band data will"
            print "be used for the actual calculation of Y Factor but the wide band data"
            print "will be availble for other calulations and ploting."
            print " "
    elif ((wide_missing) and (not narrow_missing)):
        if not verbose == 'N':
            print "Some (or all) wide band data was missing. Only narrow band data will"
            print "be avaible for calculations, some calulations may not be availible"
            print " "
    elif ((not wide_missing) and (narrow_missing)):
        if not verbose == 'N':
            print "Some (or all) narrow band data was missing. Only wide band data will"
            print "be avaible for calculations. Wide band data is not optimal for calulations"
            print "of Y-factor."
            print " "
    elif ((wide_missing) and (narrow_missing)):
        print "Some (or all) data is missing from both wide band and narrow band sets."
        print "Honestly, the script should not have made it this far. Killing the script now"
        sys.exit()
                
                
    #####
    ##### Now we read in the data
    #####
    # verbose = 'T'
    if (not wide_missing):
        wide_off = atpy.Table(wide_off_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print wide_off_csv
            print wide_off[0:3]
        
        wide_hot = atpy.Table(wide_hot_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print wide_hot_csv
            print wide_hot[0:3]
        
        wide_cold = atpy.Table(wide_cold_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print wide_cold_csv
            print wide_cold[0:3]
                   
    if (not narrow_missing):
        narrow_off = atpy.Table(narrow_off_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print narrow_off_csv
            print narrow_off[0:3]
        
        narrow_hot = atpy.Table(narrow_hot_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print narrow_hot_csv
            print narrow_hot[0:3]
        
        narrow_cold = atpy.Table(narrow_cold_csv, type="ascii", delimiter=",")
        if verbose == 'T':
            print narrow_cold_csv
            print narrow_cold[0:3]
    if not verbose == 'N':
        print "The data has been read in."
        
    #####
    ##### Now I take the list arrays and turn them into 1D arrays with discriptive names
    #####
    
    if (not wide_missing):
        wide_off_mV=wide_off.mV
        wide_off_uA=wide_off.uA
        wide_off_tp=wide_off.tp
        
        wide_hot_mV=wide_hot.mV
        wide_hot_uA=wide_hot.uA
        wide_hot_tp=wide_hot.tp
        
        wide_cold_mV=wide_cold.mV
        wide_cold_uA=wide_cold.uA
        wide_cold_tp=wide_cold.tp
        
    if (not narrow_missing):
        narrow_off_mV=narrow_off.mV
        narrow_off_uA=narrow_off.uA
        narrow_off_tp=narrow_off.tp
        
        narrow_hot_mV=narrow_hot.mV
        narrow_hot_uA=narrow_hot.uA
        narrow_hot_tp=narrow_hot.tp
        
        narrow_cold_mV=narrow_cold.mV
        narrow_cold_uA=narrow_cold.uA
        narrow_cold_tp=narrow_cold.tp
        
    #####
    ##### Now we make the data monotonic in mV
    #####
    # my monotinic function likes data to be in one 2D-array with 
    # data[:,0] to be the data that is being made monotonic
    
    #verbose = 'T'
    if mono_switcher==True:
        if (not wide_missing):
            data=numpy.empty((len(wide_off_mV),3))
            data[:,0]=wide_off_mV
            data[:,1]=wide_off_uA
            data[:,2]=wide_off_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+wide_off_csv
                sys.exit()
            wide_off_mV_mono=mono_data[:,0]
            wide_off_uA_mono=mono_data[:,1]
            wide_off_tp_mono=mono_data[:,2]
            
            data=numpy.empty((len(wide_hot_mV),3))
            data[:,0]=wide_hot_mV
            data[:,1]=wide_hot_uA
            data[:,2]=wide_hot_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+wide_hot_csv
                sys.exit()
            wide_hot_mV_mono=mono_data[:,0]
            wide_hot_uA_mono=mono_data[:,1]
            wide_hot_tp_mono=mono_data[:,2]
            
            data=numpy.empty((len(wide_cold_mV),3))
            data[:,0]=wide_cold_mV
            data[:,1]=wide_cold_uA
            data[:,2]=wide_cold_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+wide_cold_csv
                sys.exit()
            wide_cold_mV_mono=mono_data[:,0]
            wide_cold_uA_mono=mono_data[:,1]
            wide_cold_tp_mono=mono_data[:,2]
            
            # set mono data to the default handle
            wide_off_mV=wide_off_mV_mono
            wide_off_uA=wide_off_uA_mono
            wide_off_tp=wide_off_tp_mono
            wide_hot_mV=wide_hot_mV_mono
            wide_hot_uA=wide_hot_uA_mono
            wide_hot_tp=wide_hot_tp_mono
            wide_cold_mV=wide_cold_mV_mono
            wide_cold_uA=wide_cold_uA_mono
            wide_cold_tp=wide_cold_tp_mono
            

        if (not narrow_missing):
            data=numpy.empty((len(narrow_off_mV),3))
            data[:,0]=narrow_off_mV
            data[:,1]=narrow_off_uA
            data[:,2]=narrow_off_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+narrow_off_csv
                sys.exit()
            narrow_off_mV_mono=mono_data[:,0]
            narrow_off_uA_mono=mono_data[:,1]
            narrow_off_tp_mono=mono_data[:,2]
            
            data=numpy.empty((len(narrow_hot_mV),3))
            data[:,0]=narrow_hot_mV
            data[:,1]=narrow_hot_uA
            data[:,2]=narrow_hot_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+narrow_hot_csv
                sys.exit()
            narrow_hot_mV_mono=mono_data[:,0]
            narrow_hot_uA_mono=mono_data[:,1]
            narrow_hot_tp_mono=mono_data[:,2]
            
            data=numpy.empty((len(narrow_cold_mV),3))
            data[:,0]=narrow_cold_mV
            data[:,1]=narrow_cold_uA
            data[:,2]=narrow_cold_tp
            status=False
            mono_data, status = mono_switch(data,max_loop,mono_mesh,max_equal,verbose)
            if status == False:
                print "The function mono_switch failed, exiting this script"
                print "the data was from "+narrow_cold_csv
                sys.exit()
            narrow_cold_mV_mono=mono_data[:,0]
            narrow_cold_uA_mono=mono_data[:,1]
            narrow_cold_tp_mono=mono_data[:,2]
            
            # set mono data to the default handle
            narrow_off_mV=narrow_off_mV_mono
            narrow_off_uA=narrow_off_uA_mono
            narrow_off_tp=narrow_off_tp_mono
            narrow_hot_mV=narrow_hot_mV_mono
            narrow_hot_uA=narrow_hot_uA_mono
            narrow_hot_tp=narrow_hot_tp_mono
            narrow_cold_mV=narrow_cold_mV_mono
            narrow_cold_uA=narrow_cold_uA_mono
            narrow_cold_tp=narrow_cold_tp_mono
    # end of monotonic if statment and assignments   
    
    #####
    ##### Here we rigrid the data with even spacing
    #####
    # my regrid function likes data to be in one 2D-array with 
    # data[:,0] to be the data that is being made to have even spacing.
    # My regridding function requires that the data be monotonic when compared
    # to the regrid_mesh
    
    #verbose = 'Y'
    if ((do_regrid == True) and (mono_switcher==True)): 
        if (not wide_missing):
            data=numpy.empty((len(wide_off_mV),3))
            data[:,0]=wide_off_mV
            data[:,1]=wide_off_uA
            data[:,2]=wide_off_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+wide_off_csv
                sys.exit()
            wide_off_mV_regrid=regrid_data[:,0]
            wide_off_uA_regrid=regrid_data[:,1]
            wide_off_tp_regrid=regrid_data[:,2]
    
            data=numpy.empty((len(wide_hot_mV),3))
            data[:,0]=wide_hot_mV
            data[:,1]=wide_hot_uA
            data[:,2]=wide_hot_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+wide_hot_csv
                sys.exit()
            wide_hot_mV_regrid=regrid_data[:,0]
            wide_hot_uA_regrid=regrid_data[:,1]
            wide_hot_tp_regrid=regrid_data[:,2]  
            
            data=numpy.empty((len(wide_cold_mV),3))
            data[:,0]=wide_cold_mV
            data[:,1]=wide_cold_uA
            data[:,2]=wide_cold_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+wide_cold_csv
                sys.exit()
            wide_cold_mV_regrid=regrid_data[:,0]
            wide_cold_uA_regrid=regrid_data[:,1]
            wide_cold_tp_regrid=regrid_data[:,2]
            
            # set regrid data to the default handle
            wide_off_mV=wide_off_mV_regrid
            wide_off_uA=wide_off_uA_regrid
            wide_off_tp=wide_off_tp_regrid
            wide_hot_mV=wide_hot_mV_regrid
            wide_hot_uA=wide_hot_uA_regrid
            wide_hot_tp=wide_hot_tp_regrid
            wide_cold_mV=wide_cold_mV_regrid
            wide_cold_uA=wide_cold_uA_regrid
            wide_cold_tp=wide_cold_tp_regrid
            
        if (not narrow_missing):
            data=numpy.empty((len(narrow_off_mV),3))
            data[:,0]=narrow_off_mV
            data[:,1]=narrow_off_uA
            data[:,2]=narrow_off_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+narrow_off_csv
                sys.exit()
            narrow_off_mV_regrid=regrid_data[:,0]
            narrow_off_uA_regrid=regrid_data[:,1]
            narrow_off_tp_regrid=regrid_data[:,2]
    
            data=numpy.empty((len(narrow_hot_mV),3))
            data[:,0]=narrow_hot_mV
            data[:,1]=narrow_hot_uA
            data[:,2]=narrow_hot_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+narrow_hot_csv
                sys.exit()
            narrow_hot_mV_regrid=regrid_data[:,0]
            narrow_hot_uA_regrid=regrid_data[:,1]
            narrow_hot_tp_regrid=regrid_data[:,2]  
            
            data=numpy.empty((len(narrow_cold_mV),3))
            data[:,0]=narrow_cold_mV
            data[:,1]=narrow_cold_uA
            data[:,2]=narrow_cold_tp
            status=False
            regrid_data, status = regrid(data, regrid_mesh, verbose)
            if status == False:
                print "The function regrid failed, exiting this script"
                print "the data was from "+narrow_cold_csv
                sys.exit()
            narrow_cold_mV_regrid=regrid_data[:,0]
            narrow_cold_uA_regrid=regrid_data[:,1]
            narrow_cold_tp_regrid=regrid_data[:,2]
            
            # set regrid data to the default handle
            narrow_off_mV=narrow_off_mV_regrid
            narrow_off_uA=narrow_off_uA_regrid
            narrow_off_tp=narrow_off_tp_regrid
            narrow_hot_mV=narrow_hot_mV_regrid
            narrow_hot_uA=narrow_hot_uA_regrid
            narrow_hot_tp=narrow_hot_tp_regrid
            narrow_cold_mV=narrow_cold_mV_regrid
            narrow_cold_uA=narrow_cold_uA_regrid
            narrow_cold_tp=narrow_cold_tp_regrid
    # this is the end of the regridding part of the script

    #####
    ##### Start Y-Factor Calulation
    #####
    if ((do_yfactor==True) and (do_regrid == True) and (mono_switcher==True)):
        if not narrow_missing:
            print " "
            print "Doing Y factor calulaition with narrow data set."
            
            #off_mV_narrow_off_mV
            hot_mV=narrow_hot_mV
            cold_mV=narrow_cold_mV
            off_tp=narrow_off_tp
            hot_tp=narrow_hot_tp
            cold_tp=narrow_cold_tp
            status=False
            mV_Yfactor, Yfactor, mV_max_Yfactor, max_Yfactor, status = data2Yfactor(hot_mV, cold_mV, off_tp, hot_tp, cold_tp, start_Yrange, end_Yrange, regrid_mesh, verbose)
            if status == False:
                print "The function data2Yfactor failed, exiting this script"
                print "the data was from the narrow set for "+Ynums[n]
                sys.exit()
            
        
        
        elif ((narrow_missing) and (not wide_missing )):
            print " "
            print "Doing Y factor calulaition with the only data set availible, the wide data set"
        
        
    
    #####
    ##### Start the plotting part of the script
    #####
    if show_plots:
        status = False
        status = Yfac_plotter(dir, wide_lineW, narrow_lineW, mV_Yfactor, start_Yrange, end_Yrange, max_Yfactor, mV_max_Yfactor, Ynums[n], LO_val, IFband_val, magpot_val, UCA_val, wide_missing, narrow_missing, do_yfactor, do_regrid, mono_switcher, save_plots, wide_off_uA, wide_hot_uA, wide_cold_uA, narrow_off_uA, narrow_hot_uA, narrow_cold_uA, wide_off_tp, wide_hot_tp, wide_cold_tp, narrow_off_tp, narrow_hot_tp, narrow_cold_tp,Yfactor,wide_off_mV,wide_hot_mV,wide_cold_mV,narrow_off_mV,narrow_hot_mV,narrow_cold_mV)
        if status == False:
            print "The function data2Yfactor failed, exiting this script"
            print "the data was from the narrow set for "+Ynums[n]
            sys.exit()
            

print "the end of Yfactor.py has been reached"
