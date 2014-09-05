def getparams(filename):
    import atpy
    import numpy
    K_val        = None
    magisweep    = None
    magiset      = None
    magpot       = None
    LOuAsearch    = None
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
            UCA_volt = float(params.value[params_index])
        elif ((params.param[params_index] == 'sisi_set_pot') or (params.param[params_index] == 'LOuA_set_pot')):
            LOuA_set_pot = float(params.value[params_index])
        elif ((params.param[params_index] == 'sisi_magpot') or (params.param[params_index] == 'LOuA_magpot')):
            LOuA_magpot = float(params.value[params_index])
        elif params.param[params_index] == 'LOfreq':
            LOfreq = float(params.value[params_index])
        elif params.param[params_index] == 'IFband':
            IFband = float(params.value[params_index])
    return K_val, magisweep, magiset, magpot, LOuAsearch, LOuAset, UCA_volt, LOuA_set_pot, LOuA_magpot, LOfreq, IFband
    
def getproparams(filename):
    import atpy
    import numpy
    K_val        = None
    magisweep    = None
    magiset      = None
    magpot       = None
    meanmag_V    = None
    stdmag_V     = None
    meanmag_mA   = None
    stdmag_mA    = None
    LOuAsearch    = None
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
            LOfreq = float(params.value[params_index])
        elif params.param[params_index] == 'IFband':
            IFband = float(params.value[params_index])
    return K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,\
            LOuA_set_pot, LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
            del_time, LOfreq, IFband

def get_fastIV(filename):
    import atpy
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
    import atpy
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
    import atpy
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
    import shutil
    import atpy
    import os
    from sys import platform
    # this is a test filename
    #filename = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test/rawdata/Y0001/hot/sweep/TP1.csv'
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
    import os
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
    import atpy
    data = atpy.Table(filename, type="ascii", delimiter=",")
    freqs = data.GHz
    pwr  = data.pwr
    return freqs, pwr


def getproSweep(datadir):
    import atpy
    datafile  = datadir + 'data.csv'
    
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
    
    return mV_mean, mV_std,  uA_mean, uA_std,TP_mean, TP_std, TP_num, TP_freq, \
    time_mean, pot, meas_num
     
def getproYdata(datadir):
    import atpy
    hotdatafile  = datadir + 'hotdata.csv'
    colddatafile = datadir + 'colddata.csv'
    Ydatafile    = datadir + 'Ydata.csv'
    
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
    
    # make sure all the Y mV data overlaps
    first_hot  = hot_mV_mean[0]
    first_cold = cold_mV_mean[0]
    first_Y    = mV_Yfactor[0]
    max_first  = max(first_hot, first_cold, first_Y)
    
    len_hot    = len(hot_mV_mean)
    len_cold   = len(cold_mV_mean)
    len_Y      = len(mV_Yfactor)
    
    last_hot   = hot_mV_mean[len_hot-1]
    last_cold  = cold_mV_mean[len_cold-1]
    last_Y     = mV_Yfactor[len_Y-1]
    
    if ((first_hot == first_cold) and (first_cold == first_Y) and (last_hot == last_cold) and (last_cold == last_Y)):
        mV = hot_mV_mean
    else:
        finished   = False
        hot_count  = 0
        cold_count = 0
        Y_count    = 0
        first_match = True
        while not finished:
            if ((len_hot == hot_count) or (len_cold == cold_count) or (len_Y == Y_count)):
                finished = True
            elif ((hot_mV_mean[hot_count] == cold_mV_mean[cold_count]) and (cold_mV_mean[cold_count] == mV_Yfactor[Y_count])):
                if first_match:
                    first_match = False
                    hot_start  = hot_count
                    cold_start = cold_count
                    Y_start    = Y_count
                hot_count  = hot_count  + 1
                cold_count = cold_count + 1
                Y_count    = Y_count    + 1

            else:
                if hot_mV_mean[hot_count] < max_first:
                    hot_count  = hot_count  + 1
                if cold_mV_mean[cold_count] < max_first:
                    cold_count = cold_count + 1
                if mV_Yfactor[Y_count] < max_first:
                    Y_count = Y_count + 1
        mV = hot_mV_mean[hot_start:hot_count]
        hot_mV_std    = hot_mV_std[hot_start:hot_count]
        hot_uA_mean   = hot_uA_mean[hot_start:hot_count]
        hot_uA_std    = hot_uA_std[hot_start:hot_count]
        hot_TP_mean   = hot_TP_mean[hot_start:hot_count]
        hot_TP_std    = hot_TP_std[hot_start:hot_count]
        hot_TP_num    = hot_TP_num[hot_start:hot_count]
        hot_TP_freq   = hot_TP_freq[hot_start:hot_count]
        hot_time_mean = hot_time_mean[hot_start:hot_count]
        hot_pot       = hot_pot[hot_start:hot_count]
        hot_meas_num  = hot_meas_num[hot_start:hot_count]
        
        cold_mV_std    = cold_mV_std[cold_start:cold_count]
        cold_uA_mean   = cold_uA_mean[cold_start:cold_count]
        cold_uA_std    = cold_uA_std[cold_start:cold_count]
        cold_TP_mean   = cold_TP_mean[cold_start:cold_count]
        cold_TP_std    = cold_TP_std[cold_start:cold_count]
        cold_TP_num    = cold_TP_num[cold_start:cold_count]
        cold_TP_freq   = cold_TP_freq[cold_start:cold_count]
        cold_time_mean = cold_time_mean[cold_start:cold_count]
        cold_pot       = cold_pot[cold_start:cold_count]
        cold_meas_num  = cold_meas_num[cold_start:cold_count]
        
        Yfactor = Yfactor[Y_start:Y_count]
        
    return Yfactor, mV, hot_mV_std, cold_mV_std, hot_uA_mean, cold_uA_mean,    \
    hot_uA_std, cold_uA_std, hot_TP_mean, cold_TP_mean, hot_TP_std,            \
    cold_TP_std, hot_TP_num, cold_TP_num, hot_TP_freq, cold_TP_freq,           \
    hot_time_mean, cold_time_mean, hot_pot, cold_pot,                          \
    hot_meas_num, cold_meas_num
    
def getYnums(datadir, search_str):
    import os
    # get the Y numbers from the directory names in the datadir directory
    alldirs = []
    for root, dirs, files in os.walk(datadir):
        alldirs.append(dirs)
    topdirs = alldirs[0]
    Ynums = []
    for topdir_index in range(len(topdirs)):
        test_dir = topdirs[topdir_index]
        if test_dir[0] == search_str:
            Ynums.append(test_dir)
                
    return Ynums
    
def getSnums(datadir):
    import os
    import sys
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

def ProcessMatrix(raw_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose):
    import numpy
    from domath import regrid, conv
    from operator import itemgetter
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
    
def do_derivative(matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose):
    from domath import conv, derivative
    
    status, der1 = derivative(matrix, der1_int)
    
    if do_der1_conv:
        der1, status  = conv(der1,  regrid_mesh, der1_min_cdf, der1_sigma, verbose)
        
    status, der2 = derivative(der1, der2_int)
    
    if do_der2_conv:
        der2, status  = conv(der2,  regrid_mesh, der2_min_cdf, der2_sigma, verbose)
    
    return der1, der2