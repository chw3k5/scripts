import atpy
import numpy
import os, sys
import shutil
import random, string
from sys import platform
from domath import regrid, conv, FindOverlap # Caleb's Programs
from operator import itemgetter
import pickle
import glob
from HP437B import range2uW

def windir(filepath):
    if platform == 'win32':
        # the old filing system
        tempfilepath = filepath.replace('/Users/chw3k5/Documents/Grad_School/', 'C:\\Users\\chwheele\\Documents\\')
        # my new system using Google Drive
        if tempfilepath == filepath:
            tempfilepath = filepath.replace('/Users/chw3k5/','C:\\Users\\chwheele\\')
            #print tempfilepath
        #tempfilepath = tempfilepath.replace('IVsweep','sweep')
        winfilepath  = tempfilepath.replace('/','\\')
    else:
        winfilepath = filepath
    return winfilepath

def local_copy(filepath):
    newfilepath = filepath.replace('Google Drive', 'local_kappa_data')
    return newfilepath

def getSavedSISpotList(fileName):
    potList = None
    with open(fileName) as f:
        potData = f.readlines()
    for potDatum in potData:
        if potList is None:
            potList = []
        potValue = potDatum.replace('\n','')
        potList.append(int(potValue))
    return potList

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def getParamDict(paramsFile):
    paramsFile = windir(paramsFile)

    # Update this with new definitions
    header_str = 'param'
    temperature_str = 'temp'
    magCurrentSearch_str = 'magisweep'
    magCurrent_str = 'magiset'
    magPot_str = 'magpot'
    LOuAsearch = 'LOuAsearch'
    LOuAset_str = 'LOuAset'
    LOuAsetPot_str = 'LOuA_set_pot'
    LOuAmagPot_str = 'LOuA_magpot'
    LOfreq_str = 'LOfreq'
    IFband_str = 'IFband'
    magChan_str = 'mag_chan'
    meanMagV_str = 'meanmag_V'
    stdMagV_str = 'stdmag_V'
    meanMagmA_str =  'meanmag_mA'
    stdMagmA_str = 'stdmag_mA'
    UCA_volt_str =  'UCA_volt'
    TP_freq_str = 'TP_freq'
    TPnum_str = 'TP_num'
    TPintTime_str = 'TP_int_time'
    measNum_str = 'meas_num'
    delTime_str = 'del_time'
    sisPot_str = 'SIS_pot'
    std_sisTP_str =  'stdSIS_tp'
    mean_sisTP_str = 'meanSIS_tp'
    std_sis_uA_str = 'stdSISuA'
    meanSIS_uA_str = 'meanSIS_uA'
    stdSISmV_str = 'stdSIS_mV'
    meanSISmV_str = 'meanSIS_mV'

    # Update this with new definitions
    list_of_strings = [header_str, temperature_str, magCurrentSearch_str, magCurrent_str, magPot_str, LOuAsearch,
                       LOuAset_str, LOuAsetPot_str, LOuAmagPot_str, LOfreq_str, IFband_str, magChan_str, meanMagV_str,
                       stdMagV_str, meanMagmA_str, stdMagmA_str, UCA_volt_str, TP_freq_str, TPnum_str, TPintTime_str,
                       measNum_str, delTime_str, sisPot_str, std_sisTP_str, mean_sisTP_str, std_sis_uA_str,
                       meanSIS_uA_str, stdSISmV_str, meanSISmV_str]

    with open(paramsFile) as f:
        paramsData = f.readlines()
    paramsDict = {}
    for singleLine in paramsData:
        (dataType,value)=singleLine.split(',')
        value = value.replace('\n','')
        paramsDict[dataType]=value
        if dataType in list_of_strings:
            paramsDict[dataType]=value
        else:
            print 'Data type not valid for definition getParamsDict in profunc.py '
            print "dataType:",dataType
            print 'value:', value

    return paramsDict

def getparams(filename):
    if platform == 'win32':
        filename = windir(filename)
    K_val        = None
    magisweep    = None
    magiset      = None
    magpot       = None
    LOuAsearch   = None
    LOuAset      = None
    UCA_volt     = None
    LOuA_set_pot = None
    LOuA_magpot  = None
    LOfreq       = None
    IFband       = None
    mag_chan     = '9'
    params = atpy.Table(filename, type="ascii", delimiter=",")
    for params_index in range(len(params.param)):
        if params.param[params_index] == 'temp':
            K_val = float(params.value[params_index])
        elif params.param[params_index] == 'magisweep':
            magisweep = params.value[params_index]
            if magisweep == 'True':
                magisweep = True
            else:
                magisweep = False
        elif params.param[params_index] == 'magiset':
            magiset = float(params.value[params_index])
        elif params.param[params_index] == 'magpot':
            magpot = int(numpy.round(float(params.value[params_index])))
        elif ((params.param[params_index] == 'sisisweep') or (params.param[params_index] == 'LOuAsearch')):
            LOuAsearch = params.value[params_index]
            if LOuAsearch == 'True':
                LOuAsearch = True
            else:
                LOuAsearch = False
        elif ((params.param[params_index] == 'sisiset') or (params.param[params_index] == 'LOuAset')):
            LOuAset = float(params.value[params_index])
        elif params.param[params_index] == 'UCA_volt':
            if params.value[params_index] != 'biastestmode':
                UCA_volt = float(params.value[params_index])
        elif ((params.param[params_index] == 'sisi_set_pot') or (params.param[params_index] == 'LOuA_set_pot')):
            if params.value[params_index] != 'biastestmode':
                LOuA_set_pot = float(params.value[params_index])
        elif ((params.param[params_index] == 'sisi_magpot') or (params.param[params_index] == 'LOuA_magpot')):
            if params.value[params_index] != 'biastestmode':
                LOuA_magpot = float(params.value[params_index])
        elif params.param[params_index] == 'LOfreq':
            if params.value[params_index] != 'biastestmode':
                LOfreq = float(params.value[params_index])
        elif params.param[params_index] == 'IFband':
            if params.value[params_index] != 'biastestmode':
                IFband = float(params.value[params_index])
        elif params.param[params_index] == 'mag_chan':
            mag_chan = params.value[params_index]
    return K_val, magisweep, magiset, magpot, LOuAsearch, LOuAset, UCA_volt, LOuA_set_pot, LOuA_magpot, LOfreq, IFband, mag_chan
    
def getproparams(filename):
    if platform == 'win32':
        filename = windir(filename)
    K_val        = None
    magisweep    = None
    magiset      = None
    magpot       = None
    meanmag_V    = None
    stdmag_V     = None
    meanmag_mA   = None
    stdmag_mA    = None
    LOuAsearch   = None
    LOuAset      = None
    UCA_volt     = None
    LOuA_set_pot = None
    LOuA_magpot  = None
    meanSIS_mV   = None
    stdSIS_mV    = None
    meanSIS_uA   = None
    stdSIS_uA    = None
    meanSIS_tp   = None
    stdSIS_tp    = None
    SIS_pot      = None
    del_time     = None
    LOfreq       = None
    IFband       = None
    meas_num     = None
    TP_int_time  = None
    TP_num       = None
    TP_freq      = None
    mag_chan     = None

    params = atpy.Table(filename, type="ascii", delimiter=",")
    for params_index in range(len(params.param)):
        if params.param[params_index] == 'temp':
            K_val = float(params.value[params_index])
        elif params.param[params_index] == 'magisweep':
            magisweep = params.value[params_index]
            if magisweep == 'True':
                magisweep = True
            else:
                magisweep = False
        elif params.param[params_index] == 'magiset':
            magiset = float(params.value[params_index])
        elif params.param[params_index] == 'magpot':
            magpot = int(numpy.round(float(params.value[params_index])))
        elif params.param[params_index] == 'meanmag_V':
            meanmag_V = float(params.value[params_index])
        elif params.param[params_index] == 'stdmag_V':
            stdmag_V= float(params.value[params_index])    
        elif params.param[params_index] == 'meanmag_mA':
            meanmag_mA = float(params.value[params_index])  
        elif params.param[params_index] == 'stdmag_mA':
            stdmag_mA = float(params.value[params_index])
        elif params.param[params_index] == 'LOuAsearch':
            LOuAsearch = params.value[params_index]
            if LOuAsearch == 'True':
                LOuAsearch = True
            else:
                LOuAsearch = False
        elif params.param[params_index] == 'LOuAset':
            LOuAset = float(params.value[params_index])
        elif params.param[params_index] == 'UCA_volt':
            if params.value[params_index] != 'None':
                UCA_volt = float(params.value[params_index])
        elif params.param[params_index] == 'LOuA_set_pot':
            LOuA_set_pot = float(params.value[params_index])
        elif params.param[params_index] == 'LOuA_magpot':
            LOuA_magpot = float(params.value[params_index])
        elif params.param[params_index] == 'meanSIS_mV':
            meanSIS_mV = float(params.value[params_index])
        elif params.param[params_index] == 'stdSIS_mV':
            stdSIS_mV = float(params.value[params_index])
        elif params.param[params_index] == 'meanSIS_uA':
            meanSIS_uA = float(params.value[params_index])
        elif params.param[params_index] == 'stdSIS_uA':
            stdSIS_uA = float(params.value[params_index])
        elif params.param[params_index] == 'meanSIS_tp':
            meanSIS_tp = float(params.value[params_index])
        elif params.param[params_index] == 'stdSIS_tp':
            stdSIS_tp = float(params.value[params_index])
        elif params.param[params_index] == 'SIS_pot':
            SIS_pot = float(params.value[params_index])
        elif params.param[params_index] == 'del_time':
            del_time = float(params.value[params_index])
        elif params.param[params_index] == 'LOfreq':
            if params.value[params_index] != 'None':
                LOfreq = float(params.value[params_index])
        elif params.param[params_index] == 'IFband':
            if params.value[params_index] != 'None':
                IFband = float(params.value[params_index])
        elif params.param[params_index] == 'meas_num':
            meas_num = float(params.value[params_index])
        elif params.param[params_index] == 'TP_int_time':
            TP_int_time = float(params.value[params_index])
        elif params.param[params_index] == 'TP_num':
            TP_num = float(params.value[params_index])
        elif params.param[params_index] == 'TP_freq':
            TP_freq = float(params.value[params_index])
        elif params.param[params_index] == 'mag_chan':
            mag_chan = params.value[params_index]


    return K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,\
           LOuA_set_pot, LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
           del_time, LOfreq, IFband, meas_num, TP_int_time, TP_num, TP_freq, mag_chan

def getmultiParams(ParamsFile_list):
    if platform == 'win32':
        ParamsFile_list = [windir(ParamsFile) for ParamsFile in ParamsFile_list[:]]

    K_val        = []
    magisweep    = []
    magiset      = []
    magpot       = []
    meanmag_V    = []
    stdmag_V     = []

    meanmag_mA   = []
    stdmag_mA    = []
    LOuAsearch   = []
    LOuAset      = []
    UCA_volt     = []
    LOuA_set_pot = []

    LOuA_magpot  = []
    meanSIS_mV   = []
    stdSIS_mV    = []
    meanSIS_uA   = []
    stdSIS_uA    = []
    meanSIS_tp   = []

    stdSIS_tp    = []
    SIS_pot      = []
    del_time     = []
    LOfreq       = []
    IFband       = []
    meas_num     = []

    TP_int_time  = []
    TP_num       = []
    TP_freq      = []
    mag_chan     = []

    for ParamsFile in ParamsFile_list:

        K_val_temp, magisweep_temp, magiset_temp, magpot_temp, meanmag_V_temp, stdmag_V_temp, \
        meanmag_mA_temp, stdmag_mA_temp, LOuAsearch_temp, LOuAset_temp, UCA_volt_temp, LOuA_set_pot_temp,\
        LOuA_magpot_temp, meanSIS_mV_temp, stdSIS_mV_temp, meanSIS_uA_temp, stdSIS_uA_temp, meanSIS_tp_temp,\
        stdSIS_tp_temp, SIS_pot_temp, del_time_temp, LOfreq_temp, IFband_temp, meas_num_temp, \
        TP_int_time_temp, TP_num_temp, TP_freq_temp, mag_chan_temp\
            = getproparams(ParamsFile)

        K_val.append(K_val_temp)
        magisweep.append(magisweep_temp)
        magiset.append(magiset_temp)
        magpot.append(magpot_temp)
        meanmag_V.append(meanmag_V_temp)
        stdmag_V.append(stdmag_V_temp)

        meanmag_mA.append(meanmag_mA_temp)
        stdmag_mA.append(stdmag_mA_temp)
        LOuAsearch.append(LOuAsearch_temp)
        LOuAset.append(LOuAset_temp)
        UCA_volt.append(UCA_volt_temp)
        LOuA_set_pot.append(LOuA_set_pot_temp)

        LOuA_magpot.append(LOuA_magpot_temp)
        meanSIS_mV.append(meanSIS_mV_temp)
        stdSIS_mV.append(stdSIS_mV_temp)
        meanSIS_uA.append(meanSIS_uA_temp)
        stdSIS_uA.append(stdSIS_uA_temp)
        meanSIS_tp.append(meanSIS_tp_temp)

        stdSIS_tp.append(stdSIS_tp_temp)
        SIS_pot.append(SIS_pot_temp)
        del_time.append(del_time_temp)
        LOfreq.append(LOfreq_temp)
        IFband.append(IFband_temp)
        meas_num.append(meas_num_temp)

        TP_int_time.append(TP_int_time_temp)
        TP_num.append(TP_num_temp)
        TP_freq.append(TP_freq_temp)
        mag_chan.append(mag_chan_temp)

    # the test to determine if all the parameters are the same or not
    K_val_sametest        = True
    magisweep_sametest    = True
    magiset_sametest      = True
    magpot_sametest       = True
    meanmag_V_sametest    = True
    stdmag_V_sametest     = True

    meanmag_mA_sametest   = True
    stdmag_mA_sametest    = True
    LOuAsearch_sametest   = True
    LOuAset_sametest      = True
    UCA_volt_sametest     = True
    LOuA_set_pot_sametest = True

    LOuA_magpot_sametest  = True
    meanSIS_mV_sametest   = True
    stdSIS_mV_sametest    = True
    meanSIS_uA_sametest   = True
    stdSIS_uA_sametest    = True
    meanSIS_tp_sametest   = True

    stdSIS_tp_sametest    = True
    SIS_pot_sametest      = True
    del_time_sametest     = True
    LOfreq_sametest       = True
    IFband_sametest       = True
    meas_num_sametest     = True

    TP_int_time_sametest  = True
    TP_num_sametest       = True
    TP_freq_sametest      = True
    mag_chan_sametest     = True

    ParamsFile_list_len = len(ParamsFile_list)
    if 1 < ParamsFile_list_len:
        for n in range(ParamsFile_list_len - 1):
            if K_val[n] != K_val[n+1]:
                K_val_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if magisweep[n] != magisweep[n+1]:
                magisweep_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if magiset[n] != magiset[n+1]:
                magiset_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if magpot[n] != magpot[n+1]:
                magpot_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if meanmag_V[n] != meanmag_V[n+1]:
                meanmag_V_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if stdmag_V[n] != stdmag_V[n+1]:
                stdmag_V_sametest = False
                break

        for n in range(ParamsFile_list_len - 1):
            if meanmag_mA[n] != meanmag_mA[n+1]:
                meanmag_mA_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if stdmag_mA[n] != stdmag_mA[n+1]:
                stdmag_mA_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if LOuAsearch[n] != LOuAsearch[n+1]:
                LOuAsearch_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if LOuAset[n] != LOuAset[n+1]:
                LOuAset_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if UCA_volt[n] != UCA_volt[n+1]:
                UCA_volt_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if LOuA_set_pot[n] != LOuA_set_pot[n+1]:
                LOuA_set_pot_sametest = False
                break

        for n in range(ParamsFile_list_len - 1):
            if LOuA_magpot[n] != LOuA_magpot[n+1]:
                LOuA_magpot_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if meanSIS_mV[n] != meanSIS_mV[n+1]:
                meanSIS_mV_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if stdSIS_mV[n] != stdSIS_mV[n+1]:
                stdSIS_mV_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if meanSIS_uA[n] != meanSIS_uA[n+1]:
                meanSIS_uA_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if stdSIS_uA[n] != stdSIS_uA[n+1]:
                stdSIS_uA_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if meanSIS_tp[n] != meanSIS_tp[n+1]:
                meanSIS_tp_sametest = False
                break

        for n in range(ParamsFile_list_len - 1):
            if  stdSIS_tp[n] !=  stdSIS_tp[n+1]:
                stdSIS_tp_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if SIS_pot[n] != SIS_pot[n+1]:
                SIS_pot_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if del_time[n] != del_time[n+1]:
                del_time_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if LOfreq[n] != LOfreq[n+1]:
                LOfreq_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if IFband[n] != IFband[n+1]:
                IFband_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if meas_num[n] != meas_num[n+1]:
                meas_num_sametest = False
                break

        for n in range(ParamsFile_list_len - 1):
            if TP_int_time[n] != TP_int_time[n+1]:
                TP_int_time_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if TP_num[n] != TP_num[n+1]:
                TP_num_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if TP_freq[n] != TP_freq[n+1]:
                TP_freq_sametest = False
                break
        for n in range(ParamsFile_list_len - 1):
            if mag_chan[n] != mag_chan[n+1]:
                mag_chan_sametest = False
                break


        if K_val_sametest:
            K_val = K_val[0]
        if magisweep_sametest:
            magisweep = magisweep[0]
        if magiset_sametest:
            magiset = magiset[0]
        if magpot_sametest:
            magpot = magpot[0]
        if meanmag_V_sametest:
            meanmag_V = meanmag_V[0]
        if stdmag_V_sametest:
            stdmag_V = stdmag_V[0]

        if meanmag_mA_sametest:
            meanmag_mA = meanmag_mA[0]
        if stdmag_mA_sametest:
            stdmag_mA = stdmag_mA[0]
        if LOuAsearch_sametest:
            LOuAsearch = LOuAsearch[0]
        if LOuAset_sametest:
            LOuAset = LOuAset[0]
        if UCA_volt_sametest:
            UCA_volt = UCA_volt[0]
        if LOuA_set_pot_sametest:
            LOuA_set_pot = LOuA_set_pot[0]

        if LOuA_magpot_sametest:
            LOuA_magpot = LOuA_magpot[0]
        if meanSIS_mV_sametest:
            meanSIS_mV = meanSIS_mV[0]
        if stdSIS_mV_sametest:
            stdSIS_mV = stdSIS_mV[0]
        if meanSIS_uA_sametest:
            meanSIS_uA = meanSIS_uA[0]
        if stdSIS_uA_sametest:
            stdSIS_uA = stdSIS_uA[0]
        if meanSIS_tp_sametest:
            meanSIS_tp = meanSIS_tp[0]

        if stdSIS_tp_sametest:
            stdSIS_tp = stdSIS_tp[0]
        if SIS_pot_sametest:
            SIS_pot = SIS_pot[0]
        if del_time_sametest:
            del_time = del_time[0]
        if LOfreq_sametest:
            LOfreq = LOfreq[0]
        if IFband_sametest:
            IFband = IFband[0]
        if meas_num_sametest:
            meas_num = meas_num[0]

        if TP_int_time_sametest:
            TP_int_time = TP_int_time[0]
        if TP_num_sametest:
            TP_num = TP_num[0]
        if TP_freq_sametest:
            TP_freq = TP_freq[0]
        if mag_chan_sametest:
            mag_chan = mag_chan[0]

    return K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, \
           meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,LOuA_set_pot, \
           LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, \
           stdSIS_tp, SIS_pot, del_time, LOfreq, IFband, meas_num, \
           TP_int_time, TP_num, TP_freq, mag_chan



def get_fastIV(filename):
    if platform == 'win32':
        filename = windir(filename)
    mV   = []
    uA   = []
    tp   = []
    pot  = []
   
    SISdata = atpy.Table(filename, type="ascii", delimiter=",")
    keys = SISdata.keys()
    
    if 'mV'   in keys: mV   = SISdata.mV
    if 'uA'   in keys: uA   = SISdata.uA
    if 'tp'   in keys: tp   = SISdata.tp
    if 'pot'  in keys: pot  = SISdata.pot
    
    return mV, uA, tp, pot
  
def getSISdata(filename):
    filename = windir(filename)
    mV   = []
    uA   = []
    tp   = []
    pot  = []
    time = []
    SISdata = atpy.Table(filename, type="ascii", delimiter=",")
    keys = SISdata.keys()

    if 'mV'   in keys: mV   = SISdata.mV
    if 'uA'   in keys: uA   = SISdata.uA
    if 'tp'   in keys: tp   = SISdata.tp
    if 'pot'  in keys: pot  = SISdata.pot
    if 'time' in keys: time = SISdata.time
    
    return mV, uA, tp, pot, time
    
def getmagdata(filename):
    if platform == 'win32':
        filename = windir(filename)
    V   = []
    mA  = []
    pot = []
    
    MAGdata = atpy.Table(filename, type="ascii", delimiter=",")
    keys = MAGdata.keys()
    
    if 'V'   in keys: V    = MAGdata.V
    if 'mA'  in keys: mA   = MAGdata.mA
    if 'pot' in keys: pot  = MAGdata.pot
    
    return V, mA, pot
    
def getLJdata(filename):
    PM_range = None
    rand_int = random.randint(0, 1000)
    if platform == 'win32':
        filename = windir(filename)
    tempfilename = '/Users/chw3k5/Documents/Grad_School/deleteME'+str(rand_int)+'.csv'
    if platform == 'win32':
        tempfilename = windir(tempfilename)


    with open(filename, 'r') as f:
        first_line = f.readline()
        data =  f.read().splitlines(True)
    shutil.copyfile(filename,tempfilename)
    with open(tempfilename, 'w') as fout:
        fout.writelines(data[0:])

    try:
        [freq_str,PM_str] = string.split(first_line,',')
        [junk,TP_freq_str] = string.split(freq_str,'=')
        TP_freq=float(TP_freq_str)
        [junk,PM_range_str] = string.split(PM_str,'=')
        PM_range=int(PM_range_str)
    except:
        [junk,TP_freq_str] = string.split(first_line,'=')
        TP_freq=float(TP_freq_str)
        PM_range=None

    mWcoeff = range2uW(PM_range)

    data = atpy.Table(tempfilename, type="ascii", delimiter=",")
    TP = list(mWcoeff*numpy.array(data.tp))
    os.remove(tempfilename)

    return TP, TP_freq, PM_range

def renamespec(filename):
    if platform == 'win32':
        filename = windir(filename)
    old = open(filename, 'r')
    t = open('temp.csv', 'w')
    first = True
    for line in old:
        if first:
            t.write("GHz,pwr\n")
            print line
            first = False
        else:
            t.write(line)
    old.close()
    t.close()
    os.remove(filename)
    os.rename('temp.csv', filename)
    return


def readspec(filename):
    if platform == 'win32':
        filename = windir(filename)
    data = atpy.Table(filename, type="ascii", delimiter=",")
    freqs = data.GHz
    pwr  =  (data.pwr)**2
    return freqs, pwr

def getpromagSweep(datadir):
    datafile = datadir + 'data.csv'
    V_mean   = None
    V_std    = None
    mA_mean  = None
    mA_std   = None
    pot      = None
    prodata_found = False

    if platform == 'win32':
        datafile = windir(datafile)
    if os.path.exists(datafile):
        temp = atpy.Table(datafile, type="ascii", delimiter=",")
        keys = temp.keys()
        if 'V_mean' in keys: V_mean = temp.V_mean
        if 'V_std'  in keys: V_std  = temp.V_std

        if 'mA_mean' in keys: mA_mean = temp.mA_mean
        if 'mA_std'  in keys: mA_std  = temp.mA_std

        if 'pot'     in keys: pot     = temp.pot
        prodata_found = True


    return V_mean, V_std,  mA_mean, mA_std, pot, prodata_found

def getproSweep(datadir):
    datafile  = datadir + 'data.csv'
    mV_mean   = None
    mV_std    = None
    uA_mean   = None
    uA_std    = None
    TP_mean   = None
    TP_std    = None
    time_mean = None
    pot       = None
    prodata_found = False

    if platform == 'win32':
        datafile = windir(datafile)
    if os.path.exists(datafile):
        temp = atpy.Table(datafile, type="ascii", delimiter=",")
        keys = temp.keys()
        if 'mV_mean' in keys: mV_mean = temp.mV_mean
        if 'mV_std'  in keys: mV_std  = temp.mV_std

        if 'uA_mean' in keys: uA_mean = temp.uA_mean
        if 'uA_std'  in keys: uA_std  = temp.uA_std

        if 'TP_mean' in keys: TP_mean = temp.TP_mean
        if 'TP_std'  in keys: TP_std  = temp.TP_std

        if 'pot'     in keys: pot     = temp.pot
        if 'time_mean' in keys: time_mean = temp.time_mean
        prodata_found = True

    
    return mV_mean, mV_std,  uA_mean, uA_std,TP_mean, TP_std, \
    time_mean, pot, prodata_found

def getprorawdata(datadir):
    if platform == 'win32':
        datadir = windir(datadir)
    hotdatafile  = datadir + 'hotraw_data.csv'
    colddatafile = datadir + 'coldraw_data.csv'

    hotdatafound  = False
    hot_mV_mean   = None
    hot_mV_std    = None
    hot_uA_mean   = None
    hot_uA_std    = None
    hot_TP_mean   = None
    hot_TP_std    = None

    colddatafound  = False
    cold_mV_mean   = None
    cold_mV_std    = None
    cold_uA_mean   = None
    cold_uA_std    = None
    cold_TP_mean   = None
    cold_TP_std    = None

    if os.path.exists(hotdatafile):
        hot_data = atpy.Table(hotdatafile, type="ascii", delimiter=",")
        hot_keys = hot_data.keys()
        hotdatafound  = True
        if 'mV_mean' in hot_keys: hot_mV_mean = hot_data.mV_mean
        if 'mV_std'  in hot_keys: hot_mV_std  = hot_data.mV_std
        if 'uA_mean' in hot_keys: hot_uA_mean = hot_data.uA_mean
        if 'uA_std'  in hot_keys: hot_uA_std  = hot_data.uA_std
        if 'TP_mean' in hot_keys: hot_TP_mean = hot_data.TP_mean
        if 'TP_std'  in hot_keys: hot_TP_std  = hot_data.TP_std

    if os.path.exists(colddatafile):
        cold_data = atpy.Table(colddatafile, type="ascii", delimiter=",")
        cold_keys = cold_data.keys()
        colddatafound  = True
        if 'mV_mean' in cold_keys: cold_mV_mean = cold_data.mV_mean
        if 'mV_std'  in cold_keys: cold_mV_std  = cold_data.mV_std
        if 'uA_mean' in cold_keys: cold_uA_mean = cold_data.uA_mean
        if 'uA_std'  in cold_keys: cold_uA_std  = cold_data.uA_std
        if 'TP_mean' in cold_keys: cold_TP_mean = cold_data.TP_mean
        if 'TP_std'  in cold_keys: cold_TP_std  = cold_data.TP_std


    return hot_mV_mean, cold_mV_mean, hot_mV_std, cold_mV_std,\
           hot_uA_mean, cold_uA_mean, hot_uA_std, cold_uA_std,\
           hot_TP_mean, cold_TP_mean, hot_TP_std, cold_TP_std,\
           hotdatafound, colddatafound



def getproYdata(datadir):
    if platform == 'win32':
        datadir = windir(datadir)
    hotdatafile  = datadir + 'hotdata.csv'
    colddatafile = datadir + 'colddata.csv'
    Ydatafile    = datadir + 'Ydata.csv'

    hot_mV_mean   = None
    hot_mV_std    = None
    hot_uA_mean   = None
    hot_uA_std    = None
    hot_TP_mean   = None
    hot_TP_std    = None
    hot_time_mean = None
    hot_pot       = None
    hotdatafound  = False

    cold_mV_mean   = None
    cold_mV_std    = None
    cold_uA_mean   = None
    cold_uA_std    = None
    cold_TP_mean   = None
    cold_TP_std    = None
    cold_time_mean = None
    cold_pot       = None
    colddatafound  = False

    Yfactor    = None
    yerror = None
    y_pot = None
    y_mV = None
    y_mVerror = None
    y_uA = None
    y_uAerror = None
    y_TP = None
    y_TPerror = None
    Ydatafound = False


    if os.path.exists(hotdatafile):
        hot_data = atpy.Table(hotdatafile, type="ascii", delimiter=",")
        hot_keys = hot_data.keys()
        hotdatafound  = True
        if 'mV_mean'   in hot_keys: hot_mV_mean   = hot_data.mV_mean
        if 'mV_std'    in hot_keys: hot_mV_std    = hot_data.mV_std
        if 'uA_mean'   in hot_keys: hot_uA_mean   = hot_data.uA_mean
        if 'uA_std'    in hot_keys: hot_uA_std    = hot_data.uA_std
        if 'TP_mean'   in hot_keys: hot_TP_mean   = hot_data.TP_mean
        if 'TP_std'    in hot_keys: hot_TP_std    = hot_data.TP_std
        if 'time_mean' in hot_keys: hot_time_mean = hot_data.time_mean
        if 'pot'       in hot_keys: hot_pot       = hot_data.pot
    if os.path.exists(colddatafile):
        cold_data = atpy.Table(colddatafile, type="ascii", delimiter=",")
        cold_keys = cold_data.keys()
        colddatafound  = True
        if 'mV_mean'   in cold_keys: cold_mV_mean   = cold_data.mV_mean
        if 'mV_std'    in cold_keys: cold_mV_std    = cold_data.mV_std
        if 'uA_mean'   in cold_keys: cold_uA_mean   = cold_data.uA_mean
        if 'uA_std'    in cold_keys: cold_uA_std    = cold_data.uA_std
        if 'TP_mean'   in cold_keys: cold_TP_mean   = cold_data.TP_mean
        if 'TP_std'    in cold_keys: cold_TP_std    = cold_data.TP_std
        if 'time_mean' in cold_keys: cold_time_mean = cold_data.time_mean
        if 'pot'       in cold_keys: cold_pot       = cold_data.pot
    if os.path.exists(Ydatafile):
        Y_data = atpy.Table(Ydatafile, type="ascii", delimiter=",")
        Y_keys = Y_data.keys()
        Ydatafound = True
        if 'Yfactor'    in Y_keys: Yfactor    = Y_data.Yfactor
        if 'yerror'     in Y_keys: yerror    = Y_data.yerror
        if 'y_pot' in Y_keys: y_pot = Y_data.y_pot
        if 'mV_Yfactor' in Y_keys: y_mV = Y_data.mV_Yfactor # An old verson of the code used this
        if 'y_mV' in Y_keys: y_mV = Y_data.y_mV
        if 'mVerror' in Y_keys: mVerror = Y_data.mVerror
        if 'y_uA' in Y_keys: y_uA = Y_data.y_uA
        if 'y_uAerror' in Y_keys: y_uAerror = Y_data.y_uAerror
        if 'y_TP' in Y_keys: y_TP = Y_data.y_TP
        if 'y_TPerror' in Y_keys: y_TPerror = Y_data.y_TPerror

    # make sure all the Hot and cold data overlaps (The Y data is on the raw data scale)
    if ((1 < len(list(hot_mV_mean))) and (1 < len(list(cold_mV_mean)))
        and (hotdatafound) and (colddatafound)):
        if 1 < len(hot_mV_mean):
            mesh = (hot_mV_mean[1]-hot_mV_mean[0])
        else:
            mesh=0.01
        status, hot_start, cold_start, list_length = FindOverlap(hot_mV_mean, cold_mV_mean, mesh)
        if not status:
            print "The function 'FindOverlap' failed in 'getproYdata' for file:", datadir
            print "Killing Script"
            sys.exit()

        # hot_end  = hot_start  + list_length
        # mV = hot_mV_mean[hot_start:hot_end]
        # status, mV_start, Yfactor_start, list_length = FindOverlap(mV, mV_Yfactor, mesh)
        # if not status:
        #     print "The function 'FindOverlap' (2nd call) failed in 'getproYdata' for file:", datadir
        #     print "Killing Script"
        #     sys.exit()



        hot_end     = hot_start  + list_length
        cold_end    = cold_start + list_length

        mV = hot_mV_mean[hot_start:hot_end]

        hot_mV_mean   = hot_mV_mean[hot_start:hot_end]
        hot_mV_std    = hot_mV_std[hot_start:hot_end]
        hot_uA_mean   = hot_uA_mean[hot_start:hot_end]
        hot_uA_std    = hot_uA_std[hot_start:hot_end]
        hot_TP_mean   = hot_TP_mean[hot_start:hot_end]
        hot_TP_std    = hot_TP_std[hot_start:hot_end]
        hot_time_mean = hot_time_mean[hot_start:hot_end]
        hot_pot       = hot_pot[hot_start:hot_end]

        cold_mV_mean   = cold_mV_mean[cold_start:cold_end]
        cold_mV_std    = cold_mV_std[cold_start:cold_end]
        cold_uA_mean   = cold_uA_mean[cold_start:cold_end]
        cold_uA_std    = cold_uA_std[cold_start:cold_end]
        cold_TP_mean   = cold_TP_mean[cold_start:cold_end]
        cold_TP_std    = cold_TP_std[cold_start:cold_end]
        cold_time_mean = cold_time_mean[cold_start:cold_end]
        cold_pot       = cold_pot[cold_start:cold_end]


    else:
        mV = None

        
    return Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror,\
           hot_mV_mean, cold_mV_mean, mV, \
           hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean, \
           hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std, cold_TP_std,\
           hot_time_mean, cold_time_mean, hot_pot, cold_pot,\
           hotdatafound, colddatafound, Ydatafound
    
def getYnums(datadir, search_str='Y'):
    if platform == 'win32':
        datadir = windir(datadir)

    # check to see if the path exists
    if not os.path.isdir(datadir):
        print 'The path', datadir
        print 'does not exist'
        print 'check the path and try again, killing script'
        sys.exit()

    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(datadir):
        alldirs.append(dirs)
    try:
        topdirs = alldirs[0]
        len_topdirs = len(topdirs)
    except IndexError:
        print "This error happens when the directory specified:" + str(datadir)
        print "Does is empty. Check that the directory is correct and try egain."
        print "Here is the variable that had the error 'alldirs':"+str(alldirs)
        len_topdirs = None
    Ynums = []
    if len_topdirs is not None:
        for topdir_index in range(len(topdirs)):
            test_dir = topdirs[topdir_index]
            if test_dir[0] == search_str:
                Ynums.append(test_dir)
                
    return Ynums
    
def getSnums(datadir):

    if platform == 'win32':
        datadir = windir(datadir)
    search_str = 'Y'

        # check to see if the path exists
    if not os.path.isdir(datadir):
        print 'The path', datadir
        print 'does not exist'
        print 'check the path and try again, killing script'
        sys.exit()

    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(datadir):
        alldirs.append(dirs)
    try:
        topdirs = alldirs[0]
        len_topdirs = len(topdirs)
    except IndexError:
        print "This error happens when the directory specified:" + str(datadir)
        print "Is empty. Check that the directory is correct and try egain."
        print "Here is the variable that had the error 'alldirs':"+str(alldirs)
        len_topdirs = None
    Snums = []
    if len_topdirs is not None:
        for topdir_index in range(len(topdirs)):
            test_dir = topdirs[topdir_index]
            if not test_dir[0] == search_str:
                Snums.append(test_dir)
                
    return Snums

def GetProDirsNames(datadir, search_4nums, nums):
    prodatadir = datadir + 'prodata/'
    plotdir    = datadir + 'plots/'
    if platform == 'win32':
        prodatadir = windir(prodatadir)
        plotdir    = windir(plotdir)

    if os.path.isdir(plotdir):
        None
        # remove old processed data
        # shutil.rmtree(plotdir)
        # make a folder for new processed data
        # os.makedirs(plotdir)
    else:
        # make a folder for new processed data
        os.makedirs(plotdir)
    if search_4nums:
        # get the Y numbers from the directory names in the datadir directory
        alldirs = []
        for root, dirs, files in os.walk(prodatadir):
            alldirs.append(dirs)
        try:
            nums = alldirs[0]
        except IndexError:
            print "The variable alldir[0] causes an IndexError, the value of alldir is :"
            print alldirs
            print "Check the directories prodatadir:"
            print prodatadir
            print "and plotdir:"
            print plotdir
            print "to see if they have the directories you are searching for"
            print "Killing script"
            sys.exit()
    return nums, prodatadir, plotdir


def getpro_spec(prodir):
    search_str = windir(prodir + 'hotspecdata_*.npy')
    spec_list_len = len(glob.glob(search_str))

    freq_list=[]
    Yfactor_list=[]
    hot_pwr_list=[]
    hot_pot_list=[]
    hot_mV_mean_list=[]
    hot_tp_list=[]
    hot_spike_list_list=[]
    hot_spikes_inband_list=[]
    hot_sweep_index_list=[]
    cold_pwr_list=[]
    cold_pot_list=[]
    cold_mV_mean_list=[]
    cold_tp_list=[]
    cold_spike_list_list=[]
    cold_spikes_inband_list=[]
    cold_sweep_index_list=[]


    spec_data_found = False
    for spectal_index in range(spec_list_len):
        spec_data_found = True
        Y_factor_file = windir(prodir + "Y"+str(spectal_index+1)+".npy")

        with open(Y_factor_file,'r') as f:
            pickled_string = f.read()

        Ydata = pickle.loads(pickled_string)
        (freq,Yfactor,
            hot_pwr ,hot_pot ,hot_mV_mean ,hot_tp ,hot_spike_list ,hot_spikes_inband ,hot_sweep_index,
            cold_pwr,cold_pot,cold_mV_mean,cold_tp,cold_spike_list,cold_spikes_inband,cold_sweep_index) = Ydata

        freq_list.append(freq)
        Yfactor_list.append(Yfactor)
        hot_pwr_list.append(hot_pwr)
        hot_pot_list.append(hot_pot)
        hot_mV_mean_list.append(hot_mV_mean)
        hot_tp_list.append(hot_tp)
        hot_spike_list_list.append(hot_spike_list)
        hot_spikes_inband_list.append(hot_spikes_inband)
        hot_sweep_index_list.append(hot_sweep_index)
        cold_pwr_list.append(cold_pwr)
        cold_pot_list.append(cold_pot)
        cold_mV_mean_list.append(cold_mV_mean)
        cold_tp_list.append(cold_tp)
        cold_spike_list_list.append(cold_spike_list)
        cold_spikes_inband_list.append(cold_spikes_inband)
        cold_sweep_index_list.append(cold_sweep_index)



    return spec_data_found, freq_list,Yfactor_list,\
           hot_pwr_list,hot_pot_list,hot_mV_mean_list,hot_tp_list,\
           hot_spike_list_list,hot_spikes_inband_list,hot_sweep_index_list,\
           cold_pwr_list,cold_pot_list,cold_mV_mean_list,cold_tp_list,\
           cold_spike_list_list,cold_spikes_inband_list,cold_sweep_index_list


def ProcessMatrix(raw_matrix, mono_switcher=True, do_regrid=False,
                  do_conv=False, regrid_mesh=0.01, min_cdf=0.9, sigma=5, verbose=False):
    matrix        = raw_matrix
    mono_matrix   = False
    regrid_matrix = False
    conv_matrix   = False
    # make the data monotonic in mV
    if (mono_switcher or do_regrid or do_conv):
        mono_matrix  = numpy.asarray(sorted(matrix,  key=itemgetter(0)))
        matrix  = mono_matrix               
    # regrid the data in mV 
    if (do_regrid or do_conv):
        regrid_matrix, status  = regrid(matrix,  regrid_mesh, verbose)
        matrix = regrid_matrix
    # do a convolution to the data, this does not effect mV
    if do_conv:
        conv_matrix, status  = conv(matrix,  regrid_mesh, min_cdf, sigma, verbose)
        matrix = conv_matrix
        
    return matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix





def find_max_yfactor_spec(spec_Yfactor_list,spec_freq_list,spec_hot_mV_mean_list,spec_cold_mV_mean_list,
                          min_freq=None,max_freq=None):
    max_Yfactor      = None
    max_Yfactor_mV   = None
    max_Yfactor_freq = None
    ave_Yfactor      = None
    image_of_spec_Yfactor_list      = spec_Yfactor_list[:]
    image_of_spec_freq_list         = spec_freq_list[:]
    image_of_spec_hot_mV_mean_list  = spec_hot_mV_mean_list[:]
    image_of_spec_cold_mV_mean_list = spec_cold_mV_mean_list[:]

    max_Yfactor      = -1
    max_Yfactor_mV   = -1
    max_Yfactor_freq = -1
    ave_Yfactor      = -1
    if min_freq is not None:
        for list_index in range(len(image_of_spec_freq_list[:])):
            spec_Yfactor  = image_of_spec_Yfactor_list[list_index]
            spec_freqs    = image_of_spec_freq_list[list_index]
            spec_hot_mV   = image_of_spec_hot_mV_mean_list[list_index]
            spec_cold_mV  = image_of_spec_cold_mV_mean_list[list_index]

            spec_freq_temp = []
            spec_Yfactor_temp = []
            spec_hot_mV_temp = None
            spec_cold_mV_temp = None
            for (f_index,freq) in list(enumerate(spec_freqs)):
                if min_freq <= freq:
                    spec_freq_temp.append(freq)
                    spec_Yfactor_temp.append(spec_Yfactor[f_index])
                    if spec_hot_mV_temp is None:
                        spec_hot_mV_temp  = spec_hot_mV
                        spec_cold_mV_temp = spec_cold_mV

            image_of_spec_freq_list[list_index]         = spec_freq_temp
            image_of_spec_Yfactor_list[list_index]      = spec_Yfactor_temp
            image_of_spec_hot_mV_mean_list[list_index]  = spec_hot_mV_temp
            image_of_spec_cold_mV_mean_list[list_index] = spec_cold_mV_temp


    if max_freq is not None:
        for list_index in range(len(image_of_spec_freq_list[:])):
            spec_freqs     = image_of_spec_freq_list[list_index]
            spec_Yfactor  = image_of_spec_Yfactor_list[list_index]
            spec_hot_mV   = image_of_spec_hot_mV_mean_list[list_index]
            spec_cold_mV  = image_of_spec_cold_mV_mean_list[list_index]

            spec_freq_temp = []
            spec_Yfactor_temp = []
            spec_hot_mV_temp = None
            spec_cold_mV_temp = None
            for (f_index,freq) in list(enumerate(spec_freqs)):
                if freq <= max_freq:
                    spec_freq_temp.append(freq)
                    spec_Yfactor_temp.append(spec_Yfactor[f_index])
                    if spec_hot_mV_temp is None:
                        spec_hot_mV_temp  = spec_hot_mV
                        spec_cold_mV_temp = spec_cold_mV

            image_of_spec_freq_list[list_index]         = spec_freq_temp
            image_of_spec_Yfactor_list[list_index]      = spec_Yfactor_temp
            image_of_spec_hot_mV_mean_list[list_index]  = spec_hot_mV_temp
            image_of_spec_cold_mV_mean_list[list_index] = spec_cold_mV_temp

    list_of_max_Yfactors     = []
    list_of_max_Yfactor_freq = []
    list_of_max_Yfactor_mV   = []
    list_of_ave_Yfactors     = []
    tuple_of_max_Yfactor_for_plot=([],[],-1)
    tuple_of_avg_Yfactor_for_plot=([],[],-1)


    for list_index in range(len(image_of_spec_freq_list[:])):
        spec_Yfactor         = list(image_of_spec_Yfactor_list[list_index])
        Yfactor_freq         = list(image_of_spec_freq_list[list_index])
        local_max_Yfactor_mV = (image_of_spec_hot_mV_mean_list[list_index]
                                + image_of_spec_cold_mV_mean_list[list_index])/2.0

        local_max_Yfactor      = max(spec_Yfactor)
        index_of_max_Yfactor   = spec_Yfactor.index(local_max_Yfactor)
        local_max_Yfactor_freq = Yfactor_freq[index_of_max_Yfactor]
        local_ave_Yfactor      = numpy.mean(spec_Yfactor)

        if max_Yfactor < local_max_Yfactor:
            max_Yfactor    = local_max_Yfactor
            max_Yfactor_mV = local_max_Yfactor_mV
            max_Yfactor_freq   = local_max_Yfactor_freq
            tuple_of_max_Yfactor_for_plot = (Yfactor_freq,spec_Yfactor,local_max_Yfactor_mV)

        if ave_Yfactor < local_ave_Yfactor:
            ave_Yfactor = local_ave_Yfactor
            tuple_of_avg_Yfactor_for_plot = (Yfactor_freq,spec_Yfactor,local_max_Yfactor_mV)

        list_of_max_Yfactors.append(local_max_Yfactor)
        list_of_max_Yfactor_freq.append(local_max_Yfactor_freq)
        list_of_max_Yfactor_mV.append(local_max_Yfactor_mV)
        list_of_ave_Yfactors.append(ave_Yfactor)

    return max_Yfactor, max_Yfactor_mV, max_Yfactor_freq, ave_Yfactor,\
           tuple_of_max_Yfactor_for_plot, tuple_of_avg_Yfactor_for_plot

