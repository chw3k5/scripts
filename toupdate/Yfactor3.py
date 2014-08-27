# 3nd Y factor calculator and Plot Maker created February 10, 2014

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

import sys

print "Y factor calculator and Plot Maker created October 29, 2013"
print "Modified April 6, 2014"

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
from YfactorGuts  import YfactorGuts
from renamer      import renamer

###########################################
######### Data Processing Options #########
###########################################

mono_switcher=True # makes data monotonic in mV

do_regrid=True
regrid_mesh=0.01 # in mV (default = 0.01)

do_conv = True
sigma   = 0.03 # in mV
min_cdf = 0.95 # fraction of Guassian used in kernal calulation

do_yfactor=True
start_Yrange = 1.1 # in mV
end_Yrange   = 2.2 # in mV

################################
######### Plot Options #########
################################
show_plots=True
save_plots=True
tp_plots=True
wide_lineW=1
narrow_lineW=2

###################################
######### General Options #########
###################################

verbose='N' # Y, N, T (test)
do_rename = True # false in general

##### location of IV and TP parameter files, the data files
setnum=3

dir='/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'
setdata=dir+'data/set'+str(setnum)+'data.csv' # the place where Yfactor data is saved
Offnum = setnum
load_params=False # (True or False) Load file names, and possibly other parameters, from params.csv in the folder dir
load_search_str='*.csv' # example LO672_IFband1.42_magpot65100_UCA0.00_W300K_Y01_0150.csv

search_4Ynums=False
if not search_4Ynums:
    Ynums=['Y0020'] # make a list array seporate array values with commas like Ynums = ['Y01', 'Y02']

format_search_str='*.csv' # The search string for finding files


#######################################
######### Start of the Script #########
#######################################

#####
##### Search for and reformat files (I don't really use this anymore)
#####
status = False
status = csvFormat(dir, format_search_str, verbose )
if status == False:
    print 'csvFormat has failed, exiting this script'
    sys.exit()

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
##### Rename the files to make a (new) standard format
#####
if do_rename:
    renamer(csvfiles)
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
plfile = open(setdata,'w')
plfile.write("start_Yrange, end_Yrange, max_Yfactor, mV_max_Yfactor, min_Yfactor, mV_min_Yfactor, mean_Yfactor, Ynum, LO_val, IFband_val, magpot_pos, mag_mA, UCA_val \n")
for n in range(len(Ynums)): # start Y factor loop
    Ynum=Ynums[n]
    if (not Ynum == ''):
        status = False
        status, start_Yrange, end_Yrange, max_Yfactor, mV_max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, Ynum, LO_val, IFband_val, magpot_val, UCA_val = YfactorGuts(dir, verbose, Ynum, Offnum, load_search_str, show_plots, save_plots, tp_plots, wide_lineW, narrow_lineW, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf, do_yfactor, start_Yrange, end_Yrange)
        if status == False:
            print "The function YfactorGuts failed, exiting this script"
            print "the data was for set for "+Ynum
            sys.exit()
        magpot_pos=magpot_val[0:6]
        mag_mA=magpot_val[6:]
        plfile.write(str('%01.2f' % start_Yrange) + "," + str('%01.2f' % end_Yrange) + "," + str('%01.4f' % max_Yfactor) + "," + str('%01.4f' % mV_max_Yfactor) + "," + str('%01.4f' % min_Yfactor) + "," + str('%01.4f' % mV_min_Yfactor) + "," + str('%01.4f' % mean_Yfactor) + "," + Ynum + "," + LO_val + "," + IFband_val + "," + magpot_pos + ',' +mag_mA + "," + UCA_val+"\n")  
plfile.close()
print "the end of Yfactor3.py has been reached"
