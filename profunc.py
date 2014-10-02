import atpy
import numpy
import os, sys
import shutil
from sys import platform
from domath import regrid, conv, FindOverlap # Caleb's Programs
from operator import itemgetter

def getparams(filename):
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
    return K_val, magisweep, magiset, magpot, LOuAsearch, LOuAset, UCA_volt, LOuA_set_pot, LOuA_magpot, LOfreq, IFband
    
def getproparams(filename):
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


    return K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,\
           LOuA_set_pot, LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
           del_time, LOfreq, IFband, meas_num, TP_int_time, TP_num, TP_freq

def getmultiParams(ParamsFile_list):
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

    for ParamsFile in ParamsFile_list:

        K_val_temp, magisweep_temp, magiset_temp, magpot_temp, meanmag_V_temp, stdmag_V_temp, \
        meanmag_mA_temp, stdmag_mA_temp, LOuAsearch_temp, LOuAset_temp, UCA_volt_temp, LOuA_set_pot_temp,\
        LOuA_magpot_temp, meanSIS_mV_temp, stdSIS_mV_temp, meanSIS_uA_temp, stdSIS_uA_temp, meanSIS_tp_temp,\
        stdSIS_tp_temp, SIS_pot_temp, del_time_temp, LOfreq_temp, IFband_temp, meas_num_temp, \
        TP_int_time_temp, TP_num_temp, TP_freq_temp \
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

    return K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, \
           meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,LOuA_set_pot, \
           LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, \
           stdSIS_tp, SIS_pot, del_time, LOfreq, IFband, meas_num, \
           TP_int_time, TP_num, TP_freq



def get_fastIV(filename):
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
    V   = []
    mA  = []
    pot = []
    
    SISdata = atpy.Table(filename, type="ascii", delimiter=",")
    keys = SISdata.keys()
    
    if 'V'   in keys: V    = SISdata.V
    if 'mA'  in keys: mA   = SISdata.mA
    if 'pot' in keys: pot  = SISdata.pot
    
    return V, mA, pot
    
def getLJdata(filename):
    if platform == 'win32':
        tempfilename = 'C:\\Users\\MtDewar\\Documents\\deleteME.csv'
    elif platform == 'darwin':
        tempfilename = '/Users/chw3k5/deleteME.csv'

    with open(filename, 'r') as f:
        first_line = f.readline()
        data =  f.read().splitlines(True)
    shutil.copyfile(filename,tempfilename)
    with open(tempfilename, 'w') as fout:
        fout.writelines(data[0:])

    position=first_line.find('=', 0)
    if not position == -1:
        TP_freq = float(first_line[position+1:])
    else:
        TP_freq = []
        print "The frequency of the total power measurment could not be found."
        print "The function getLJdata in profunc.py was looking for a number after an equals sign '='."
        print "Returning a null list"

    data = atpy.Table(tempfilename, type="ascii", delimiter=",")
    TP = data.tp
    os.remove(tempfilename)

    return TP, TP_freq

def renamespec(filename):
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
    data = atpy.Table(filename, type="ascii", delimiter=",")
    freqs = data.GHz
    pwr  = data.pwr
    return freqs, pwr


def getproSweep(datadir):
    datafile  = datadir + 'data.csv'
    if os.path.exists(datafile):
        temp = atpy.Table(datafile, type="ascii", delimiter=",")
        mV_mean   = temp.mV_mean
        mV_std    = temp.mV_std
        uA_mean   = temp.uA_mean
        uA_std    = temp.uA_std
        TP_mean   = temp.TP_mean
        TP_std    = temp.TP_std
        TP_num    = temp.TP_num
        TP_freq   = temp.TP_freq
        time_mean = temp.time_mean
        pot       = temp.pot
        meas_num  = temp.meas_num
        astroprodata_found = True
    else:
        mV_mean   = None
        mV_std    = None
        uA_mean   = None
        uA_std    = None
        TP_mean   = None
        TP_std    = None
        TP_num    = None
        TP_freq   = None
        time_mean = None
        pot       = None
        meas_num  = None
        astroprodata_found = False
    
    return mV_mean, mV_std,  uA_mean, uA_std,TP_mean, TP_std, TP_num, TP_freq, \
    time_mean, pot, meas_num, astroprodata_found
     
def getproYdata(datadir):
    hotdatafile  = datadir + 'hotdata.csv'
    colddatafile = datadir + 'colddata.csv'
    Ydatafile    = datadir + 'Ydata.csv'


    if os.path.exists(hotdatafile):
        temp = atpy.Table(hotdatafile, type="ascii", delimiter=",")
        hot_mV_mean   = temp.mV_mean
        hot_mV_std    = temp.mV_std
        hot_uA_mean   = temp.uA_mean
        hot_uA_std    = temp.uA_std
        hot_TP_mean   = temp.TP_mean
        hot_TP_std    = temp.TP_std
        hot_time_mean = temp.time_mean
        hot_pot       = temp.pot
        hotdatafound  = True
    else:
        hot_mV_mean   = None
        hot_mV_std    = None
        hot_uA_mean   = None
        hot_uA_std    = None
        hot_TP_mean   = None
        hot_TP_std    = None
        hot_time_mean = None
        hot_pot       = None
        hotdatafound  = False

    if os.path.exists(colddatafile):
        temp = atpy.Table(colddatafile, type="ascii", delimiter=",")
        cold_mV_mean   = temp.mV_mean
        cold_mV_std    = temp.mV_std
        cold_uA_mean   = temp.uA_mean
        cold_uA_std    = temp.uA_std
        cold_TP_mean   = temp.TP_mean
        cold_TP_std    = temp.TP_std
        cold_time_mean = temp.time_mean
        cold_pot       = temp.pot
        colddatafound  = True
    else:
        temp = atpy.Table(colddatafile, type="ascii", delimiter=",")
        cold_mV_mean   = None
        cold_mV_std    = None
        cold_uA_mean   = None
        cold_uA_std    = None
        cold_TP_mean   = None
        cold_TP_std    = None
        cold_time_mean = None
        cold_pot       = None
        colddatafound  = False

    if os.path.exists(Ydatafile):
        temp = atpy.Table(Ydatafile, type="ascii", delimiter=",")
        mV_Yfactor = temp.mV_Yfactor
        Yfactor    = temp.Yfactor
        Ydatafound = True
    else:
        mV_Yfactor = None
        Yfactor    = None
        Ydatafound = False
    
    # make sure all the Y mV data overlaps
    if (hotdatafound and colddatafound and Ydatafound):
        if 1 < len(hot_mV_mean):
            mesh = (hot_mV_mean[1]-hot_mV_mean[0])
        else:
            mesh=0.01
        status, hot_start, cold_start, list_length = FindOverlap(hot_mV_mean, cold_mV_mean, mesh)
        if not status:
            print "The function 'FindOverlap' failed in 'getproYdata' for file:", datadir
            print "Killing Script"
            sys.exit()
        hot_end  = hot_start  + list_length

        mV = hot_mV_mean[hot_start:hot_end]
        status, mV_start, Yfactor_start, list_length = FindOverlap(mV, mV_Yfactor, mesh)
        if not status:
            print "The function 'FindOverlap' (2nd call) failed in 'getproYdata' for file:", datadir
            print "Killing Script"
            sys.exit()

        Yfactor_end = Yfactor_start + list_length

        hot_start  += mV_start
        cold_start += mV_start
        hot_end     = hot_start  + list_length
        cold_end    = cold_start + list_length

        mV = mV[mV_start:list_length+mV_start]

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

        Yfactor    = Yfactor[Yfactor_start:Yfactor_end]
        mV_Yfactor = mV_Yfactor[Yfactor_start:Yfactor_end]

    else:
        mV = None

        
    return Yfactor, mV_Yfactor, hot_mV_mean, cold_mV_mean, mV, \
           hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean, \
           hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std, cold_TP_std,\
           hot_time_mean, cold_time_mean, hot_pot, cold_pot,\
           hotdatafound, colddatafound, Ydatafound
    
def getYnums(datadir, search_str):
    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(datadir):
        alldirs.append(dirs)
    try:
        topdirs = alldirs[0]
    except IndexError:
        print "This error happens when the directory specified:" + str(datadir)
        print "Does not exist. Check that the directory is correct and try egain."
        print "Here is the variable that had the error 'alldirs':"+str(alldirs)
        print "Killing script."
        sys.exit()
    Ynums = []
    for topdir_index in range(len(topdirs)):
        test_dir = topdirs[topdir_index]
        if test_dir[0] == search_str:
            Ynums.append(test_dir)
                
    return Ynums
    
def getSnums(datadir):
    search_str = 'Y'
    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(datadir):
        alldirs.append(dirs)
    try:
        topdirs = alldirs[0]
    except IndexError:
        print "This error happens when the directory specified:" + str(datadir)
        print "Does not exist. Check that the directory is correct and try egain."
        print "Here is the variable that had the error 'alldirs':"+str(alldirs)
        print "Killing script."
        sys.exit()
    Snums = []
    for topdir_index in range(len(topdirs)):
        test_dir = topdirs[topdir_index]
        if not test_dir[0] == search_str:
            Snums.append(test_dir)
                
    return Snums

def GetProDirsNames(datadir, search_4nums, nums):
    if platform == 'win32':
        prodatadir = datadir + 'prodata\\'
        plotdir    = datadir + 'plots\\'
    elif platform == 'darwin':
        prodatadir = datadir + 'prodata/'
        plotdir    = datadir + 'plots/'
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
        nums = alldirs[0]
    return nums, prodatadir, plotdir



def ProcessMatrix(raw_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose):
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

