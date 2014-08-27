import sys
import os
import atpy

# Import this is the directory that has my scripts
#func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
#func_dir_exists=False
#for n in range(len(sys.path)):
#    if sys.path[n] == func_dir:
#        func_dir_exists=True
#if not func_dir_exists:
#    sys.path.append(func_dir)
    
setnum = 1
search_4Ynums = True
Ynums = ['Y0030']

#datadir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set' + str(setnum) + '/'
datadir    = '/Users/nhinkel/Desktop/Yfactor/set' + str(setnum) + '/'
prodatadir = datadir + 'prodata/'
plotdir = datadir + 'plots/'

if search_4Ynums:
    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(prodatadir):
        alldirs.append(dirs)
    Ynums = alldirs[0]

for Ynum_index in range(len(Ynums)):
    Ynum = Ynums[Ynum_index]
    
    hotdatafile  = prodatadir + Ynum + '/hotdata.csv'
    colddatafile = prodatadir + Ynum + '/colddata.csv'
    Ydatafile    = prodatadir + Ynum + '/Ydata.csv'
    
    temp = atpy.Table(hotdatafile, type="ascii", delimiter=",")    
    hot_mV_mean   = temp.mV_mean
    hot_mV_std    = temp.mV_std
    hot_uA_mean   = temp.uA_mean
    hot_uA_std    = temp.uA_std
    hot_TP_mean   = temp.TP_mean
    hot_TP_std    = temp.TP_std
    hot_TP_num    = temp.TP_num
    hot_TP_freq   = temp.TP_freq
    hot_time_mean = temp.time_mean
    hot_pot       = temp.pot
    hot_meas_num  = temp.meas_num
    
    temp = atpy.Table(colddatafile, type="ascii", delimiter=",")    
    cold_mV_mean   = temp.mV_mean
    cold_mV_std    = temp.mV_std
    cold_uA_mean   = temp.uA_mean
    cold_uA_std    = temp.uA_std
    cold_TP_mean   = temp.TP_mean
    cold_TP_std    = temp.TP_std
    cold_TP_num    = temp.TP_num
    cold_TP_freq   = temp.TP_freq
    cold_time_mean = temp.time_mean
    cold_pot       = temp.pot
    cold_meas_num  = temp.meas_num
    
    temp = atpy.Table(Ydatafile, type="ascii", delimiter=",")
    mV_Yfactor = temp.mV_Yfactor
    Yfactor    = temp.Yfactor

    execfile("yfact_plot.py")
    
    