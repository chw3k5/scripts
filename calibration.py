__author__ = 'chw3k5'
from control import opentelnet, closetelnet, setmag_only, measmag, mag_channel
from profunc import windir, ProcessMatrix
from agilent34410A import Agilent34410ADriver

from sys import exit
from time import sleep
from shutil import copyfile
import os
from scipy import stats
from atpy import Table
from matplotlib import pyplot as plt
import numpy as np

"""
Calibration procedures for some devices including:
The Electromagnet
"""
magpath='/Users/chw3k5/Google Drive/Kappa/NA38/calibration/mag/'
offset_channel = '10' # string number

do_magcalsweep = False
do_makeoffsets = True

def fetchoffset(filename,path=''):
    default_path = windir('/Users/chw3k5/Google Drive/Kappa/NA38/calibration/mag/')
    fullname = None
    local_filename = path+filename
    default_filename = default_path+filename
    if os.path.isfile(local_filename):
        fullname = local_filename
    elif os.path.isfile(default_filename):
        fullname = default_filename
        copyfile(default_filename, local_filename)
    if fullname is None:
        m = 1.
        b = 0.
    else:
        offsets = Table(fullname, type="ascii", delimiter=",")
        m = float(offsets.m)
        b = float(offsets.b)
    return m, b


def make_magpot_function(mag_channel, filepath):
    pot_function_filename = "channel"+str(mag_channel)+"_magpot2mA.csv"

    lookup_filename = filepath+'channel'+str(mag_channel)+'.csv'
    lookup_file = Table(lookup_filename, type="ascii", delimiter=",")
    magpot = lookup_file.pot
    mA     = lookup_file.mA_meas

    raw_matrix = np.zeros((len(magpot), 2))
    raw_matrix[:,0] = magpot
    raw_matrix[:,1] = mA
    pro_matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix \
        = ProcessMatrix(raw_matrix, mono_switcher=True, do_regrid=True, do_conv=False,
                        regrid_mesh=1., min_cdf=0.9, sigma=5, verbose=False)

    pro_magpot = pro_matrix[:,0]
    pro_mA     = pro_matrix[:,1]

    pot_file = open(pot_function_filename, 'w')
    pot_file.write('pot,mA_meas\n')
    for n in range(len(pro_magpot)):
        pot_file.write(str('%6f' % pro_magpot[n])+','+str(pro_mA[n])+'\n')
    pot_file.close()



    return

def magpot_lookup(mA_to_find, mag_channel, lookup_filepath=None):
    if not os.path.isfile(lookup_filepath):
        lookup_filepath = '/Users/chw3k5/Google Drive/Kappa/NA38/calibration/mag/'
    lookup_filepath = windir(lookup_filepath)

    pot_function_filename = "channel"+str(mag_channel)+"_magpot2mA.csv"
    if not os.path.isfile(lookup_filepath+pot_function_filename):
        make_magpot_function(mag_channel, lookup_filepath)

    pot_function = Table(pot_function_filename, type="ascii", delimiter=",")
    magpot = pot_function.pot
    mA     = pot_function.mA_meas



    mA_diff = abs(mA - mA_to_find)
    found_pot = np.round(magpot(mA_diff.index(min(mA_diff))))

    return found_pot


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
    defult_calfilename = windir('/Users/chw3k5/Google Drive/Kappa/NA38/calibration/mag/channel'+str(mag_channel)+'.csv')

    calfilename = path+'channel'+mag_channel+'.csv'
    if (os.path.isfile(defult_calfilename) or os.path.isfile(calfilename)):
        if not os.path.isfile(calfilename):
            calfilename = defult_calfilename
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
            offset_file = open(path+str(mag_channel)+str(from_type)+'-'+str(final_type)+'.csv', 'w')
            offset_file.write('m,b,r,p,std_err\n')

            offset_file.write(write_str+'\n')
            offset_file.close()
            print "Offset file written"


    else:
        print "The calfile was not found:",calfilename


    return

if __name__ == "__main__":
    if do_magcalsweep:
        filename = magpath+'channel'+mag_channel+'.csv'
        magnet_cal_sweep(filename)
    if do_makeoffsets:
        magnet_find_offset(magpath,offset_channel,caltype=('mA_biascom','mA_meas'))