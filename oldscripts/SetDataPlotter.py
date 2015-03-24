import sys
import atpy
import numpy
import os
import glob
from matplotlib import pyplot as plt
import matplotlib
import shutil
import time
matplotlib.rc('text', usetex=True)

# This is the location of the Kappa Scripts on Caleb's Mac
func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
func_dir_exists=False
for n in range(len(sys.path)):
    if sys.path[n] == func_dir:
        func_dir_exists=True
if not func_dir_exists:
    sys.path.append(func_dir)
# Now I import the scripts functions and programs that I have made to make my life easier
from heatmap import map4setdata

##############################
###### Set Data Options ######
##############################
rootdir    = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'
setNums  = [3]
show_plots  = False
save_plots  = True
for_movie   = False

grideges4charlen = 3    # number of gris edges per chariterisic length, 3 edges is 3^2=9 grids per characteristic square  
near_neigh       = 9    # Specify a number of write 'False' use all all values 

# More than one option selelected sweeps the options
x_options = [0] # 0 magnet current, 1 SIS current
y_options = [1] # 0 magnet current, 1 SIS current
z_options = [0] # 0 Yfactor

# Set characteristic lengths 
char_len_magi  = 1 # mA of magnet current
char_len_sisi  = 1 # uA of SIS current measued at a constant voltage

###############################################
######### Y Factor Processing Options #########
###############################################



###################################
######### Data Processing #########
###################################
#Ynum,sisi_voltage,mV,magpot,magi,hot_mV_std,hot_uA_mean,hot_uA_std,hot_TP_mean,hot_TP_std,hot_TP_num,hot_TP_freq,hot_time_mean,hot_pot,hot_meas_num,cold_mV_std,cold_uA_mean,cold_uA_std,cold_TP_mean,cold_TP_std,cold_TP_num,cold_TP_freq,cold_time_mean,cold_pot,cold_meas_num,Yfactor
datadirs = []
for set_index in range(len(setNums)):
    datadirs.append(rootdir + 'set' + str(setNums[set_index]) + '/setdata/')
Y_list = [os.path.basename(x) for x in glob.glob(datadirs[0] + "Y*mV.csv")]

for iii in range(len(Y_list)):
    
    for i1 in range(len(x_options)):
        x_option = x_options[i1]
        x=[]
        if x_option == 0:
            char_len_x = char_len_magi
            for ii1 in range(len(datadirs)):
                datadir=datadirs[ii1]
                temp_data = atpy.Table(datadir + Y_list[iii], type="ascii", delimiter=",")
                x.extend(temp_data.magi)
                x_handle = "Magnet current (mA)"
        elif x_option == 1:
            char_len_x = char_len_sisi
            for ii1 in range(len(datadirs)):
                datadir=datadirs[ii1]
                print datadir
                temp_data = atpy.Table(datadir + Y_list[iii], type="ascii", delimiter=",")
                x.extend(temp_data.hot_uA_mean)
                x_handle = "SIS current ($\mu$A) at " + str(temp_data.sisi_voltage[0]) + " mV"
        else:
            print "The x_option selected was not found. The option was: "+ str(x_option)
            sys.exit()
    
        for i2 in range(len(y_options)):
            y_option = y_options[i2]
            y = []
            if y_option == 0:
                char_len_y = char_len_magi
                for ii2 in range(len(datadirs)):
                    datadir=datadirs[ii2]
                    print datadir
                    temp_data = atpy.Table(datadir + Y_list[iii], type="ascii", delimiter=",")
                    y.extend(temp_data.magi)
                    y_handle = "Magnet currnet (mA)"
            elif y_option == 1:
                char_len_y = char_len_sisi
                for ii2 in range(len(datadirs)):
                    datadir=datadirs[ii2]
                    print datadir
                    temp_data = atpy.Table(datadir + Y_list[iii], type="ascii", delimiter=",")
                    y.extend(temp_data.hot_uA_mean)
                    y_handle = "SIS current ($\mu$A) at " + str(temp_data.sisi_voltage[0]) + " mV"
            else:
                print "The y_option selected was not found. The option was: "+ str(y_option)
                sys.exit()
                
            for i3 in range(len(z_options)):
                z_option = z_options[i3]
                z = []
                if z_option == 0:
                    for ii3 in range(len(datadirs)):
                        datadir=datadirs[ii3]
                        print datadir
                        temp_data = atpy.Table(datadir + Y_list[iii], type="ascii", delimiter=",")
                        z.extend(temp_data.Yfactor)
                        z_handle="Y factor at " + str('%1.2f' % temp_data.YmV[0]) + 'mV'
                        levels = numpy.arange(1.3, 2.11, 0.05)
                else:
                    print "The z_option selected was not found. The option was: "+ str(z_option)
                    sys.exit()
                
                mV_handle = str('%1.2f' % temp_data.YmV[0]) + 'mV'
                plottitle = z_handle
                #if (i1 == 0 and i2 == 0 and i3 == 0 and iii == 0):
                setplotdir = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/setplots/"
                if not os.path.isdir(setplotdir):
                    os.makedirs(setplotdir)    
                saveplotdir = setplotdir +  y_handle.replace(' ','_').replace('$\\mu$','u')+"__"+x_handle.replace(' ','_')+"__set"+str(setNums)+'/'
                #shutil.rmtree(saveplotdir)
                if not os.path.isdir(saveplotdir):
                    os.makedirs(saveplotdir)
                if for_movie:
                    saveplotname=saveplotdir+str(iii)+".eps"
                else:
                    saveplotname=saveplotdir+mV_handle.replace(' ','_')+".eps"
                
                ### start plotting the data here ###
                
                
                
                map4setdata(show_plots, save_plots, saveplotname, grideges4charlen, near_neigh, char_len_x, char_len_y, x, y, z, levels, x_handle, y_handle, plottitle)
                