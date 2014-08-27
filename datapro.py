def ProParmsFiles(dirnames, proparamsfile, verbose):
    from profunc import getparams, getSISdata, getmagdata
    import os, numpy
    params_found        = False
    standSISdata_found  = False
    standmagdata_found  = False
    ###### Processing Params file ######
    paramsfile = dirnames + 'params.csv'
    if os.path.isfile(paramsfile):
        params_found  = True
        # load the params file for the data
        K_val, magisweep, magiset, magpot, sisisweep, sisiset, UCA_volt,       \
        LOfreq, IFband = getparams(paramsfile)
    
    ##### Processing Standard SIS bias measurments ######
    standSISdatafile = dirnames + 'sisdata.csv'
    if os.path.isfile(standSISdatafile):
        standSISdata_found  = True
        # load the standard SIS bias measurments for the data
        standSISdata_mV, standSISdata_uA, standSISdata_tp, standSISdata_pot,   \
        standSISdata_time = getSISdata(standSISdatafile)
    
    ###### Processing Standard eletromagnet measurments ######
    standmagdatafile = dirnames + 'magdata.csv'
    if os.path.isfile(standmagdatafile):
        standmagdata_found  = True
        # load the standard electromagnet measurments for the data
        standmagdata_V, standmagdata_mA, standmagdata_pot =                    \
        getmagdata(standmagdatafile)
    
    ### processed parameter file (uses at most 'params.csv', 'sisdata.csv', 'magdata.csv')
    # record the parameters of every sweep
    n = open(proparamsfile, 'w')
    if params_found:
        n.write('param, value\n')
        n.write('temp,' + str(K_val) + '\n')
        if magisweep == True:
            n.write('magisweep,True\n')
            n.write('magiset,' +  str(magiset) + '\n')
            n.write('magpot,'  +  str(round(magpot)) + '\n')
        else:
            n.write('magisweep,False\n')
            n.write('magpot,' +  str(magpot) + '\n')
    if standmagdata_found:
        n.write('meanmag_V,'  + str(numpy.mean(standmagdata_V))  + '\n')
        n.write('stdmag_V,'   + str(numpy.std(standmagdata_V))   + '\n')
        n.write('meanmag_mA,' + str(numpy.mean(standmagdata_mA)) + '\n')
        n.write('stdmag_mA,'  + str(numpy.std(standmagdata_mA))  + '\n')
    if params_found:
        if sisisweep == True:
            n.write('sisisweep,True\n')
            n.write('sisiset,'  + str(sisiset)    + '\n')
            n.write('UCA_volt,' + str(UCA_volt)   + '\n')
        else:
            n.write('sisisweep,False\n')
            n.write('UCA_volt,' + str(UCA_volt) + '\n')
    if standSISdata_found:
        n.write('meanSIS_mV,' + str(numpy.mean(standSISdata_mV)) + '\n')
        n.write('stdSIS_mV,'  + str(numpy.std(standSISdata_mV))  + '\n')
        n.write('meanSIS_uA,' + str(numpy.mean(standSISdata_uA)) + '\n')
        n.write('stdSIS_uA,'  + str(numpy.std(standSISdata_uA))  + '\n')
        n.write('meanSIS_tp,' + str(numpy.mean(standSISdata_tp)) + '\n')
        n.write('stdSIS_tp,'  + str(numpy.std(standSISdata_tp))  + '\n')
        n.write('SIS_pot,'    + str(standSISdata_pot[0])         + '\n')
        n.write('del_time,'   +                                                \
        str(numpy.max(standSISdata_time) - numpy.min(standSISdata_time))+'\n')
    if params_found:
        n.write('LOfreq,' + str(LOfreq) + '\n')
        n.write('IFband,' + str(IFband) + '\n')
    n.close()
    
    return params_found, standSISdata_found, standmagdata_found

def ProFastIV(fastIV_filename,  prodataname):
    from profunc import get_fastIV, ProcessMatrix
    import numpy, os
    fastIV_found = False
    if os.path.isfile(fastIV_filename):
        fastIV_found = True
        # load the fast IV data
        mV_fastIV, uA_fastIV, tp_fastIV, pot_fastIV =get_fastIV(fastIV_filename)
        # put the data into a matrix for processing    
        fast_matrix = numpy.zeros((len(mV_fastIV), 4))
        fast_matrix[:,0] = mV_fastIV
        fast_matrix[:,1] = uA_fastIV
        fast_matrix[:,2] = tp_fastIV
        fast_matrix[:,3] = pot_fastIV
        # process the matrix
        fast_matrix, fast_raw_matrix, fast_mono_matrix, fast_regrid_matrix,    \
        fast_conv_matrix = ProcessMatrix(fast_matrix, mono_switcher,           \
        do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
        # put the information back into 1-D arrays
        mV_fast  = fast_matrix[:,0]
        uA_fast  = fast_matrix[:,1]
        tp_fast  = fast_matrix[:,2]
        pot_fast = fast_matrix[:,3]
        # save fastIV processed data
        n = open(prodataname, 'w')
        n.write('mV,uA,tp,pot\n')
        for mV_index in range(len(mV_fast)):
            writeline = str(mV_fast[mV_index]) + ',' + str(uA_fast[mV_index])  \
            + ',' + str(tp_fast[mV_index]) + ',' + str(pot_fast[mV_index]) +'\n'
            n.write(writeline)
        n.close()
    return fastIV_found

def AstroDataPro(datadir, prodataname):
    from sys import platform
    import glob, numpy
    from profunc import getSISdata, getLJdata, ProcessMatrix
    astrosweep_found = True
    if platform == 'win32':
         sweepdir = datadir + 'sweep\\'
    elif platform == 'darwin':
        sweepdir = datadir + 'sweep/'
    TP_list = glob.glob(sweepdir + "TP*.csv")
    if not TP_list == []:
        astrosweep_found = True
        sweep_pot       = []
        sweep_meas_num  = []
        sweep_mV_mean   = []
        sweep_mV_std    = []
        sweep_uA_mean   = []
        sweep_uA_std    = []
        sweep_TP_mean   = []
        sweep_TP_std    = []
        sweep_TP_num    = []
        sweep_TP_freq   = []
        sweep_time_mean = []
        for sweep_index in range(len(TP_list)):
            # read in SIS data for each sweep step
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time =                   \
            getSISdata(sweepdir + str(sweep_index + 1) + '.csv')
            print sweepdir + str(sweep_index + 1) + '.csv'
            sweep_pot.append(temp_pot[0])
            sweep_meas_num.append(len(temp_mV))
            sweep_mV_mean.append(numpy.mean(temp_mV))
            sweep_mV_std.append(numpy.std(temp_mV))
            sweep_uA_mean.append(numpy.mean(temp_uA))
            sweep_uA_std.append(numpy.std(temp_uA))
            sweep_time_mean.append(numpy.mean(temp_time))
            temp_TP, TP_freq = getLJdata(sweepdir + "TP" +                     \
            str(sweep_index + 1) + '.csv')
            sweep_TP_mean.append(numpy.mean(temp_tp))
            sweep_TP_std.append(numpy.std(temp_tp))
            sweep_TP_num.append(len(temp_TP))
            sweep_TP_freq.append(TP_freq)
        # put the data into a matrix for processing
        matrix  = numpy.zeros((len(sweep_mV_mean), 11))
        matrix[:,0]  = sweep_mV_mean
        matrix[:,1]  = sweep_mV_std
        matrix[:,2]  = sweep_uA_mean
        matrix[:,3]  = sweep_uA_std
        matrix[:,4]  = sweep_TP_mean
        matrix[:,5]  = sweep_TP_std
        matrix[:,6]  = sweep_TP_num
        matrix[:,7]  = sweep_TP_freq
        matrix[:,8]  = sweep_time_mean
        matrix[:,9]  = sweep_pot
        matrix[:,10] = sweep_meas_num
        # process the matrix
        matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix =          \
        ProcessMatrix(matrix, mono_switcher, do_regrid,                        \
        do_conv, regrid_mesh, min_cdf, sigma, verbose)
        # put the information back into 1-D arrays
        sweep_mV_mean   = matrix[:,0]
        sweep_mV_std    = matrix[:,1]
        sweep_uA_mean   = matrix[:,2]
        sweep_uA_std    = matrix[:,3]
        sweep_TP_mean   = matrix[:,4]
        sweep_TP_std    = matrix[:,5]
        sweep_TP_num    = matrix[:,6]
        sweep_TP_freq   = matrix[:,7]
        sweep_time_mean = matrix[:,8]
        sweep_pot       = matrix[:,9]
        sweep_meas_num  = matrix[:,10]
        ### save the results of this calulations
        n = open(prodataname, 'w')
        n.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,TP_num,TP_freq,\
time_mean,pot,meas_num\n')
        for sweep_index in range(len(sweep_mV_mean)):
            n.write(str(sweep_mV_mean[sweep_index]) + ',' +                    \
            str(sweep_mV_std[sweep_index])    + ',' +                          \
            str(sweep_uA_mean[sweep_index])   + ',' +                          \
            str(sweep_uA_std[sweep_index])    + ',' +                          \
            str(sweep_TP_mean[sweep_index])   + ',' +                          \
            str(sweep_TP_std[sweep_index])    + ',' +                          \
            str(sweep_TP_num[sweep_index])    + ',' +                          \
            str(sweep_TP_freq[sweep_index])   + ',' +                          \
            str(sweep_time_mean[sweep_index]) + ',' +                          \
            str(sweep_pot[sweep_index])       + ',' +                          \
            str(sweep_meas_num[sweep_index]) +'\n')
        n.close()
    return astrosweep_found, sweep_mV_mean, sweep_TP_mean


def SweepPro(datadir, proparamsfile, prodataname_fast, prodataname_unpump, prodataname_ast):
    ###### Make the parameters file
    params_found, standSISdata_found, standmagdata_found =                     \
    ProParmsFiles(datadir, proparamsfile, verbose)
    
    ###### Processing fastIV data (data taken using the bais computer's sweep command)
    fastIV_filename = datadir + 'fastsweep.csv'
    fastIV_found = ProFastIV(fastIV_filename,  prodataname_fast)
    
    ###### Processing unpumped IV data (data taken using the bais computer's sweep command)
    #unpumped_found
    unpumped_filename  = datadir + 'unpumpedsweep.csv'
    unpumped_found    = ProFastIV(unpumped_filename,  prodataname_unpump)        
    
    ### get the astronomy quality sweep data for this Y sweep
    astrosweep_found, sweep_mV_mean, sweep_TP_mean =                         \
    AstroDataPro(datadir, prodataname_ast)
    
    return params_found, standSISdata_found, standmagdata_found,               \
    fastIV_found, unpumped_found, astrosweep_found, sweep_mV_mean,            \
    sweep_TP_mean


def SweepDataPro(datadir, verbose=False, search_4Sweeps=True, search_str='Y',  \
Snums=[], mono_switcher=True, do_regrid=True, regrid_mesh=0.01,                \
do_conv=True, sigma=0.03, min_cdf=0.95):
    import sys
    from sys import platform
    import os
    import shutil
    
    # This is the location of the Kappa Scripts on Caleb's Mac
    if platform == 'win32':
        func_dir='C:\\Users\\MtDewar\\Documents\\Kappa\\scripts'
    elif platform == 'darwin':
        func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)

    from profunc import getSnums   
    if platform == 'win32':
        prodatadir = datadir + "prodata\\"
    elif platform == 'darwin':
        prodatadir = datadir + "prodata/"
    if os.path.isdir(prodatadir):
        # remove old processed data
        shutil.rmtree(prodatadir)
        # make a folder for new processed data
        os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)
    
    if platform == 'win32':
        rawdatadir = datadir + "rawdata\\"
    elif platform == 'darwin':    
        rawdatadir = datadir + "rawdata/"
    ### Find all the Y## directory if search_4Ynums = True
    if search_4Sweeps:
        Snums = getSnums(rawdatadir)                   
        
    ### step through all the Ynumbers and Process their files
    for Snum in Snums:
        if platform == 'win32':
            sweepdir = rawdatadir + Snum + '\\'
        elif platform == 'darwin':
            sweepdir = rawdatadir + Snum + '/'
        if verbose:
            print 'reducing data in: ' + sweepdir
        # make the directory where this data goes
        if platform == 'win32':
            prodatadir = datadir + "prodata\\" + Snum + '\\'
        elif platform == 'darwin':
            prodatadir = datadir + "prodata/" + Snum + '/'
        if not os.path.isdir(prodatadir):
            os.makedirs(prodatadir)
        #####################################
        #### Start Sweep data Processing ####
        #####################################
        
        proparamsfile      = prodatadir + 'proparams.csv'
        prodataname_fast   = prodatadir + 'fastIV.csv'
        prodataname_unpump = prodatadir + 'unpumped.csv'
        prodataname_ast    = prodatadir + 'data.csv'
        
        params_found, standSISdata_found, standmagdata_found,                  \
        fastIV_found, unpumped_found, astrosweep_found,                        \
        _sweep_mV_mean,_sweep_TP_mean = SweepPro(sweepdir,                     \
        proparamsfile, prodataname_fast, prodataname_unpump,                   \
        prodataname_ast)

    return

def YdataPro(datadir, verbose=False, search_4Ynums=True, search_str='Y',       \
Ynums=[], useOFFdata=False, Off_datadir='', mono_switcher=True,                \
do_regrid=True, regrid_mesh=0.01, do_conv=True, sigma=0.03, min_cdf=0.95):
    import sys
    from sys import platform
    import os
    import shutil
    
    # This is the location of the Kappa Scripts on Caleb's Mac
    if platform == 'win32':
        func_dir='C:\\Users\\MtDewar\\Documents\\Kappa\\scripts'
    elif platform == 'darwin':
        func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)

    from profunc import getYnums
    from domath import data2Yfactor
    if platform == 'win32':
        prodatadir = datadir + "prodata\\"
    elif platform == 'darwin':
        prodatadir = datadir + "prodata/"
    if os.path.isdir(prodatadir):
        # remove old processed data
        shutil.rmtree(prodatadir)
        # make a folder for new processed data
        os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)
    
    if platform == 'win32':
        rawdatadir = datadir + "rawdata\\"
    elif platform == 'darwin':
        rawdatadir = datadir + "rawdata/"
    ### Find all the Y## directory if search_4Ynums = True
    if search_4Ynums:
        Ynums = getYnums(rawdatadir, search_str)                   
        
    ### step through all the Ynumbers and Process their files
    for Ynum_index in range(len(Ynums)):
        Ynum = Ynums[Ynum_index]
        if platform == 'win32':
            Ydatadir = rawdatadir + Ynum + '\\'
        elif platform == 'darwin':   
            Ydatadir = rawdatadir + Ynum + '/'
        if verbose:
            print 'reducing data in: ' + Ydatadir
        # make the directory where this data goes
        if platform == 'win32':
            prodatadir = datadir + "prodata\\" + Ynum + '\\'
        elif platform == 'darwin':
            prodatadir = datadir + "prodata/" + Ynum + '/'
        if not os.path.isdir(prodatadir):
            os.makedirs(prodatadir)
            
        ###################################
        #### Start Hot data Processing ####
        ###################################
        if platform == 'win32':
            hotdir            = Ydatadir   + 'hot\\'
        elif platform == 'darwin':
            hotdir            = Ydatadir   + 'hot/'
        hotproparamsfile      = prodatadir + 'proparams.csv'
        hotprodataname_fast   = prodatadir + 'hotfastIV.csv'
        hotprodataname_unpump = prodatadir + 'hotunpumped.csv'
        hotprodataname_ast    = prodatadir + 'hotdata.csv'
        
        hotparams_found, hotstandSISdata_found, hotstandmagdata_found,         \
        fastIVhot_found, hotunpumped_found, astrosweephot_found,               \
        hot_sweep_mV_mean,hot_sweep_TP_mean = SweepPro(hotdir,                 \
        hotproparamsfile, hotprodataname_fast, hotprodataname_unpump,          \
        hotprodataname_ast)
        
        ####################################
        #### Start Cold data Processing ####
        ####################################
        if platform == 'win32':
            colddir            = Ydatadir   + 'cold\\'
        elif platform == 'darwin':
            colddir            = Ydatadir   + 'cold/'
        coldproparamsfile      = prodatadir + 'proparams.csv'
        coldprodataname_fast   = prodatadir + 'coldfastIV.csv'
        coldprodataname_unpump = prodatadir + 'coldunpumped.csv'
        coldprodataname_ast    = prodatadir + 'colddata.csv'
        
        coldparams_found, coldstandSISdata_found, coldstandmagdata_found,         \
        fastIVcold_found, coldunpumped_found, astrosweepcold_found,               \
        cold_sweep_mV_mean,cold_sweep_TP_mean = SweepPro(colddir,                 \
        coldproparamsfile, coldprodataname_fast, coldprodataname_unpump,          \
        coldprodataname_ast)
        
        ####################################
        ###### The Yfactor calulation ######
        ####################################
        off_tp = 0 # need to fix this in the future
        if (astrosweephot_found and astrosweepcold_found):
            if verbose:
                print "doing Y factor calulation"
            mV_Yfactor, Yfactor, status = data2Yfactor(hot_sweep_mV_mean, cold_sweep_mV_mean, off_tp, hot_sweep_TP_mean, cold_sweep_TP_mean, regrid_mesh, verbose)
            # save the results of the Y factor calculation 
            o = open(prodatadir + 'Ydata.csv', 'w')
            o.write('mV_Yfactor,Yfactor\n')
            for sweep_index in range(len(mV_Yfactor)):
                o.write(str(mV_Yfactor[sweep_index]) + ',' + str(Yfactor[sweep_index]) + '\n')    
            o.close()
    if verbose:
        print "The YdataPro function has completed"
        
    return

###################################
######### General Options #########
###################################
from sys import platform
verbose=True # True or False (default is False)

##### location of IV and TP parameter files, the data files
setnum  = 3
#datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'

if platform == 'win32':
    datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\set" +str(setnum) + "\\"
    #datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\test\\"
elif platform == 'darwin':    
    #datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test3/'
    datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'


search_4Ynums = True # (the default is True)
search_str = 'Y' # default is 'Y'
Ynums=['Y0001'] # make a list array seporate array values with commas like Ynums = ['Y01', 'Y02'] (defult is empty set [])

useOFFdata = False # True or False
Off_datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'

###########################################
######### Data Processing Options #########
###########################################

mono_switcher = True # makes data monotonic in mV (defualt = True)

do_regrid     = True # regrids data to uniform spacing (defualt = True)
regrid_mesh   = 0.01 # in mV (default = 0.01)

do_conv = True # does a guassian convolation of the data after regridding (default is True)
sigma   = 0.03 # in mV (default = 0.03)
min_cdf = 0.95 # fraction of Guassian used in kernal calulation (defualt = 0.95)

#YdataPro(datadir, verbose=True)
#SweepDataPro(datadir, verbose=True, search_4Sweeps=False, Snums=['00001'])