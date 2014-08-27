import sys
import atpy
import numpy
import os
print "Y factor Set data processing and Plot Maker created April 3, 2014"
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

from heatmap      import map4setdata
from autoYfactor  import autoYfactor

#from csvFormat    import csvFormat
#from get_files    import get_files
#from find_Ynums   import find_Ynums
#from YfactorGuts  import YfactorGuts
##############################
###### Set Data Options ######
##############################

setNums  = [6]
show_plots  = False
save_plots  = True
for_movie   = True

#datadirs = []
#setdir = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/"
#for n in range(len(setNums)):
#    datadirs.append(setdir+"set"+str(setNums[n])+"/data/set"+str(setNums[n])+"data.csv") 

grideges4charlen = 3    # number of gris edges per chariterisic length, 3 edges is 3^2=9 grids per characteristic square  
near_neigh       = 9    # Specify a number of write 'False' use all all values 

# More than one option selelected sweeps the options
x_options = [0] # 0 magpot position, 1 UCA value
y_options = [1] # 0 magpot position, 1 UCA value
z_options = [0,1,2] # 0 Yfactor Max, 1 Yfactor Mean, 2 Yfactor Min

# Set characteristic lengths 
char_len_magpot  = 1000 # pots steps per characteristic length for this data
char_len_UCA     = 0.01 # Vols of UCA per characteristic length for this data

###############################################
######### Y Factor Processing Options #########
###############################################

do_recalc = False # Automatically triggered if Yfactor files do not exist

Begin_start_Yrange = 1.2 # in mV
End_end_Yrange     = 2.2 # in mV
bandwidth          = 0.05 # in mV

start_Yranges = numpy.arange(Begin_start_Yrange,End_end_Yrange,bandwidth)
end_Yranges   = start_Yranges + bandwidth


################################
######### Plot Options #########
################################
#show_plots=True
#save_plots=True
tp_plots=True
wide_lineW=1
narrow_lineW=1

###################################
######### General Options #########
###################################
for iii in range(len(start_Yranges)):
    start_Yrange = start_Yranges[iii]
    end_Yrange  = end_Yranges[iii]
    mV_handle= str(start_Yrange)+"-"+str(end_Yrange)+ "mV"
    datadirs = []
    for ii in range(len(setNums)):
        verbose='N' # Y, N, T (test)
        ##### location of IV and TP parameter files, the data files
        setnum=setNums[ii]
        dir='/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'
        setdata=dir+'data/set'+str(setnum)+ '_' + mV_handle +'_data.csv'
        datadirs.append(setdata)
        autoYfactor(setnum, start_Yrange, end_Yrange, do_recalc)
    do_recalc = False # no need to keep rerunning after doing it once for each data set
        
    #############################################
    ###### Set handling part of the Script ######
    #############################################
    
    for i1 in range(len(x_options)):
        x_option = x_options[i1]
        x=[]
        if x_option == 0:
            char_len_x = char_len_magpot
            for ii1 in range(len(datadirs)):
                datadir=datadirs[ii1]
                print datadir
                temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                x.extend(temp_data.magpot_pos)
                x_handle = "Mag Pot Position"
        elif x_option == 1:
            char_len_x = char_len_UCA
            for ii1 in range(len(datadirs)):
                datadir=datadirs[ii1]
                print datadir
                temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                x.extend(temp_data.UCA_val)
                x_handle = "UCA (Volts)"
        else:
            print "The x_option selected was not found. The option was: "+ str(x_option)
            sys.exit()
    
        for i2 in range(len(y_options)):
            y_option = y_options[i2]
            y = []
            if y_option == 0:
                char_len_y = char_len_magpot
                for ii2 in range(len(datadirs)):
                    datadir=datadirs[ii2]
                    print datadir
                    temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                    y.extend(temp_data.magpot_pos)
                    y_handle = "Mag Pot Position"
            elif y_option == 1:
                char_len_y = char_len_UCA
                for ii2 in range(len(datadirs)):
                    datadir=datadirs[ii2]
                    print datadir
                    temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                    y.extend(temp_data.UCA_val)
                    y_handle = "UCA (Volts)"
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
                        temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                        z.extend(temp_data.max_Yfactor)
                        z_handle="Max Y factor"
                        levels = numpy.arange(1.0, 2.501, 0.01)
                elif z_option == 1:
                    for ii3 in range(len(datadirs)):
                        datadir=datadirs[ii3]
                        print datadir
                        temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                        z.extend(temp_data.mean_Yfactor)
                        z_handle="Mean Y factor"
                        levels = numpy.arange(1.0, 2.01, 0.01)
                elif z_option == 2:
                    for ii3 in range(len(datadirs)):
                        datadir=datadirs[ii3]
                        print datadir
                        temp_data = atpy.Table(datadir, type="ascii", delimiter=",")
                        z.extend(temp_data.min_Yfactor)
                        z_handle="Min Y factor"
                        levels = numpy.arange(1.0, 2.01, 0.01)
                else:
           	    print "The z_option selected was not found. The option was: "+ str(z_option)
                    sys.exit()
                mV_handle = str(temp_data.start_Yrange[0])+"-"+str(temp_data.end_Yrange[0])+ " mV"
                plottitle = z_handle+ " over "+mV_handle
                saveplotdir="/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/Ydataplots/" + z_handle.replace(' ','_')+"__"+y_handle.replace(' ','_')+"__"+x_handle.replace(' ','_')+"__set"+str(setNums)+'/'
                if not os.path.isdir(saveplotdir):
                    os.makedirs(saveplotdir)
                if for_movie:
                    saveplotname=saveplotdir+str(iii)+".png"
                else:
                    saveplotname=saveplotdir+mV_handle.replace(' ','_')+".png"
                map4setdata(show_plots, save_plots, saveplotname, grideges4charlen, near_neigh, char_len_x, char_len_y, x, y, z, levels, x_handle, y_handle, plottitle)
                