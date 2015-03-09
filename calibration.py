__author__ = 'chw3k5'
from control import opentelnet, closetelnet, setmag_only, measmag, mag_channel
from profunc import windir
from agilent34410A import Agilent34410ADriver

from sys import exit
from time import sleep
import os
from scipy import stats
from atpy import Table
from matplotlib import pyplot as plt
import numpy as np

"""
Calibration procedures for some devices including:
The Electromagnet
"""

#####################
### Electromagnet ###
#####################

def magnet_cal_sweep(filename, test_pots=range(0,129001,1000),sleep_after_set=1, meas_per_pos=10,verbose=True):
    filename = windir(filename)
    opentelnet()
    multimeter = Agilent34410ADriver()


    calfile = open(filename, 'w')
    calfile.write('pot,V_biascom,mA_biascom,mA_meas\n')
    for current_pot in test_pots:
        if verbose:
            print 'current pot  ',current_pot

        setmag_only(current_pot)
        sleep(sleep_after_set)
        for measurement_number in range(meas_per_pos):
            V_biascom, mA_biascom, pot_biascom = measmag(verbose)

            A_meas = multimeter.read_current()
            try:
                mA_meas = float(A_meas)*1000.0
            except:
                sleep(1)
                A_meas  = multimeter.read_current()
                mA_meas = float(A_meas)*1000.0


            write_string=str(pot_biascom)+','+str(V_biascom)+','+str(mA_biascom)+','+str(mA_meas)
            if verbose:
                print 'current meas ',write_string
            calfile.write(write_string+'\n')
    setmag_only(65100)
    calfile.close()
    closetelnet()
    return


def magnet_find_offset(path,mag_channel,caltype=('V_biascom','mA_biascom')):
    calfilename = path+'channel'+mag_channel+'.csv'
    if os.path.isfile(calfilename):
        calfile = Table(calfilename, type="ascii", delimiter=",")
        keys = calfile.keys()
        from_type=str(caltype[0])
        final_type=str(caltype[1])
        if from_type == 'pot':
            x = calfile.pot
        elif from_type == 'V_biascom':
            x = calfile.V_biascom
        elif from_type == 'mA_biascom':
            x = calfile.mA_biascom
        elif from_type == 'V_meas':
            x = calfile.V_meas
        elif from_type == 'mA_meas':
            x = calfile.mA_meas
        else:
            print "calibration column x:",from_type," not found"
            print 'check the calfile:',calfilename
            exit()

        if final_type == 'pot':
            y = calfile.pot
        elif final_type == 'V_biascom':
            y = calfile.V_biascom
        elif final_type == 'mA_biascom':
            y = calfile.mA_biascom
        elif final_type == 'V_meas':
            y = calfile.V_meas
        elif final_type == 'mA_meas':
            y = calfile.mA_meas
        else:
            print "calibration column 7:",final_type," not found"
            print 'check the calfile:',calfilename
            exit()

        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        plt.plot(x,y,linewidth=1,color='red',marker='o',markersize=10)
        plt.plot([max(x),min(x)],[max(x)*slope+intercept,min(x)*slope+intercept],linewidth=3)
        plt.xlabel('m='+str(slope)+'    b='+str(intercept)+'     '+str(from_type))
        plt.ylabel(str(final_type))
        plt.title("R:"+str(r_value)+'  p:'+str(p_value)+"  std_err:"+str(std_err))
        print 'Close the plot for prompt'
        plt.show()

        write_str=str(slope)+','+str(intercept)+','+str(r_value)+','+str(p_value)+','+str(std_err)
        print '\n','from: '+str(from_type)+'   to: '+str(final_type)+'\n',write_str
        hold=raw_input('1 to accept this offset')
        if hold == '1':
            offset_file = open(path+str(mag_channel)+str(from_type)+'-'+str(final_type), 'w')
            offset_file.write('m,b,r,p,std_err\n')

            offset_file.write(write_str+'\n')
            offset_file.close()
            print "Offset file written"


    else:
        print "The calfile was not found:",calfilename


    return

path='/Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/mag/'
#path='/Users/chw3k5/Google Drive/Kappa/NA38/calibration/mag/'
filename = path+'channel'+mag_channel+'.csv'
magnet_cal_sweep(filename)
#magnet_find_offset(path,mag_channel,caltype=('mA_biascom','A_meas'))