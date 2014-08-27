def YdataPro(verbose, datadir, search_4Ynums, search_str, Ynums, useOFFdata, Off_datadir, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf, do_fastIV):
    import sys
    import glob
    import numpy
    import os
    import shutil
    from operator import itemgetter
    
    # This is the location of the Kappa Scripts on Caleb's Mac
    func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)

    from profunc import getparams, getSISdata, get_fastIV, getmagdata, getLJdata, getYnums
    from domath import regrid, conv, data2Yfactor
    
    fastIVhot_found  = False
    fastIVcold_found = False
    
    prodatadir = datadir + "prodata/"
    if os.path.isdir(prodatadir):
        # remove old processed data
        shutil.rmtree(prodatadir)
        # make a folder for new processed data
        os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)
    
    rawdatadir = datadir + "rawdata/"
    ### Find all the Y## directory if search_4Ynums = True
    if search_4Ynums:
        Ynums = getYnums(rawdatadir, search_str)                   
        
    ### step through all the Ynumbers and Process their files
    for Ynum_index in range(len(Ynums)):
        Ynum = Ynums[Ynum_index]
        Ydatadir = rawdatadir + Ynum + '/'
        if verbose:
            print 'reducing data in: ' + Ydatadir
            
        
        ### get the hot Y factor data
        hotdir = Ydatadir + 'hot/'
        paramsfile = hotdir + 'params.csv'
        # load the parametes of the data
        hot_K_val, hot_magisweep, hot_magiset, hot_magpot, hot_sisisweep, hot_sisiset, hot_UCA_volt, hot_LOfreq, hot_IFband = getparams(paramsfile)
        
        ### get the standard measurments for this Y sweep
        # SIS data
        standSISdatafile = hotdir + 'sisdata.csv'
        hot_standSISdata_mV, hot_standSISdata_uA, hot_standSISdata_tp, hot_standSISdata_pot, hot_standSISdata_time = getSISdata(standSISdatafile)
        
        # magnet data
        standmagdatafile = hotdir + 'magdata.csv'
        hot_standmagdata_V, hot_standmagdata_mA, hot_standmagdata_pot = getmagdata(standmagdatafile)
        
        ### get the hot fastIV data
        if do_fastIV:
            fastIV_filename = hotdir + 'fastsweep.csv'
            if os.path.isfile(fastIV_filename):
                 mV_fastIVhot, uA_fastIVhot, tp_fastIVhot, pot_fastIVhot = get_fastIV(fastIV_filename)
                 fastIVhot_found = True
            else:
                if verbose:
                    print "fast IV data not found in: " + fastIV_filename
        
        ### get the astronomy quality sweep data for this Y sweep
        sweepdir = hotdir + 'sweep/'
        
        TP_list = glob.glob(sweepdir + "TP*.csv")
        
        hot_sweep_pot = []
        hot_sweep_meas_num  = []
        
        hot_sweep_mV_mean = []
        hot_sweep_mV_std  = []
        
        hot_sweep_uA_mean = []
        hot_sweep_uA_std  = []
        
        hot_sweep_TP_mean = []
        hot_sweep_TP_std  = []
        hot_sweep_TP_num  = []
        hot_sweep_TP_freq = []
        
        hot_sweep_time_mean = []
        
        for sweep_index in range(len(TP_list)):
            # read in SIS data for each sweep step
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(sweepdir + str(sweep_index + 1) + '.csv')
            hot_sweep_pot.append(temp_pot[0])
            hot_sweep_meas_num.append(len(temp_mV))
            
            hot_sweep_mV_mean.append(numpy.mean(temp_mV))
            hot_sweep_mV_std.append(numpy.std(temp_mV))
            
            hot_sweep_uA_mean.append(numpy.mean(temp_uA))
            hot_sweep_uA_std.append(numpy.std(temp_uA))
    
            hot_sweep_time_mean.append(numpy.mean(temp_time))
            
            temp_TP, TP_freq = getLJdata(sweepdir + "TP" + str(sweep_index + 1) + '.csv')
            
            hot_sweep_TP_mean.append(numpy.mean(temp_tp))
            hot_sweep_TP_std.append(numpy.std(temp_tp))
            hot_sweep_TP_num.append(len(temp_TP))
            hot_sweep_TP_freq.append(TP_freq)
            
        
        ### get the cold Y factor data
        colddir = Ydatadir + 'cold/'
        paramsfile = colddir + 'params.csv'
        # load the parametes of the data
        cold_K_val, cold_magisweep, cold_magiset, cold_magpot, cold_sisisweep, cold_sisiset, cold_UCA_volt, cold_LOfreq, cold_IFband = getparams(paramsfile)
        
        ### get the cold fastIV data
        if do_fastIV:
            fastIV_filename = colddir + 'fastsweep.csv'
            if os.path.isfile(fastIV_filename):
                 mV_fastIVcold, uA_fastIVcold, tp_fastIVcold, pot_fastIVcold = get_fastIV(fastIV_filename)
                 fastIVcold_found = True
            else:
                if verbose:
                    print "fast IV data not found in: " + fastIV_filename
        
        ### get the standard measurments for this Y sweep
        # SIS data
        standSISdatafile = colddir + 'sisdata.csv'
        cold_standSISdata_mV, cold_standSISdata_uA, cold_standSISdata_tp, cold_standSISdata_pot, cold_standSISdata_time = getSISdata(standSISdatafile)
        
        # magnet data
        standmagdatafile = colddir + 'magdata.csv'
        cold_standmagdata_V, cold_standmagdata_mA, cold_standmagdata_pot = getmagdata(standmagdatafile)
        
        ### get the sweep data for this Y sweep
        sweepdir = colddir + 'sweep/'
        
        TP_list = glob.glob(sweepdir + "TP*.csv")
        
        cold_sweep_pot = []
        cold_sweep_meas_num  = []
        
        cold_sweep_mV_mean = []
        cold_sweep_mV_std  = []
        
        cold_sweep_uA_mean = []
        cold_sweep_uA_std  = []
        
        cold_sweep_TP_mean = []
        cold_sweep_TP_std  = []
        cold_sweep_TP_num  = []
        cold_sweep_TP_freq = []
        
        cold_sweep_time_mean = []
        
        for sweep_index in range(len(TP_list)):
            # read in SIS data for each sweep step
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(sweepdir + str(sweep_index + 1) + '.csv')
            cold_sweep_pot.append(temp_pot[0])
            cold_sweep_meas_num.append(len(temp_mV))
            
            cold_sweep_mV_mean.append(numpy.mean(temp_mV))
            cold_sweep_mV_std.append(numpy.std(temp_mV))
            
            cold_sweep_uA_mean.append(numpy.mean(temp_uA))
            cold_sweep_uA_std.append(numpy.std(temp_uA))
    
            cold_sweep_time_mean.append(numpy.mean(temp_time))
            
            temp_TP, TP_freq = getLJdata(sweepdir + "TP" + str(sweep_index + 1) + '.csv')
            
            cold_sweep_TP_mean.append(numpy.mean(temp_tp))
            cold_sweep_TP_std.append(numpy.std(temp_tp))
            cold_sweep_TP_num.append(len(temp_TP))
            cold_sweep_TP_freq.append(TP_freq)
            
        # Now I put the data into a matrix so I can do math on it, God I love the maths
        
        # the fast data set
        if fastIVhot_found:
            fasthot_matrix = numpy.zeros((len(mV_fastIVhot), 4))
            
            fasthot_matrix[:,0] = mV_fastIVhot
            fasthot_matrix[:,1] = uA_fastIVhot
            fasthot_matrix[:,2] = tp_fastIVhot
            fasthot_matrix[:,3] = pot_fastIVhot
        if fastIVcold_found:    
            fastcold_matrix = numpy.zeros((len(mV_fastIVcold), 4))
            
            fastcold_matrix[:,0] = mV_fastIVcold
            fastcold_matrix[:,1] = uA_fastIVcold
            fastcold_matrix[:,2] = tp_fastIVcold
            fastcold_matrix[:,3] = pot_fastIVcold
        
        # the main data set
        hot_matrix  = numpy.zeros((len(hot_sweep_mV_mean), 11))
        cold_matrix = numpy.zeros((len(cold_sweep_mV_mean),11))
        
        hot_matrix[:,0]  = hot_sweep_mV_mean
        hot_matrix[:,1]  = hot_sweep_mV_std
        hot_matrix[:,2]  = hot_sweep_uA_mean
        hot_matrix[:,3]  = hot_sweep_uA_std
        hot_matrix[:,4]  = hot_sweep_TP_mean
        hot_matrix[:,5]  = hot_sweep_TP_std
        hot_matrix[:,6]  = hot_sweep_TP_num
        hot_matrix[:,7]  = hot_sweep_TP_freq
        hot_matrix[:,8]  = hot_sweep_time_mean
        hot_matrix[:,9]  = hot_sweep_pot
        hot_matrix[:,10] = hot_sweep_meas_num
    
        cold_matrix[:,0]  = cold_sweep_mV_mean
        cold_matrix[:,1]  = cold_sweep_mV_std
        cold_matrix[:,2]  = cold_sweep_uA_mean
        cold_matrix[:,3]  = cold_sweep_uA_std
        cold_matrix[:,4]  = cold_sweep_TP_mean
        cold_matrix[:,5]  = cold_sweep_TP_std
        cold_matrix[:,6]  = cold_sweep_TP_num
        cold_matrix[:,7]  = cold_sweep_TP_freq
        cold_matrix[:,8]  = cold_sweep_time_mean
        cold_matrix[:,9]  = cold_sweep_pot
        cold_matrix[:,10] = cold_sweep_meas_num
        
        ### Start the data processing part of this script
        # save the raw data in case you need to test something with it
        raw_hot_matrix  = hot_matrix
        raw_cold_matrix = cold_matrix
        if fastIVhot_found:
            raw_fasthot_matrix = fasthot_matrix
        if fastIVcold_found:
            raw_fastcold_matrix = fastcold_matrix
            
        # make the data monotinic in mV
        if (mono_switcher or do_regrid or do_conv):
            mono_hot_matrix  = numpy.asarray(sorted(hot_matrix,  key=itemgetter(0)))
            mono_cold_matrix = numpy.asarray(sorted(cold_matrix, key=itemgetter(0)))
            
            hot_matrix  = mono_hot_matrix
            cold_matrix = mono_cold_matrix
            
            if fastIVhot_found:
                mono_fasthot_matrix  = numpy.asarray(sorted(fasthot_matrix,  key=itemgetter(0)))
                fasthot_matrix = mono_fasthot_matrix
            if fastIVcold_found:
                mono_fastcold_matrix  = numpy.asarray(sorted(fastcold_matrix,  key=itemgetter(0)))
                fastcold_matrix = mono_fastcold_matrix                
        # regrid the data in mV 
        if (do_regrid or do_conv):
            regrid_hot_matrix, status  = regrid(hot_matrix,  regrid_mesh, verbose)
            regrid_cold_matrix, status = regrid(cold_matrix, regrid_mesh, verbose)
                
            hot_matrix  = regrid_hot_matrix
            cold_matrix = regrid_cold_matrix
            
            if fastIVhot_found:
                regrid_fasthot_matrix, status  = regrid(fasthot_matrix,  regrid_mesh, verbose)
                fasthot_matrix = regrid_fasthot_matrix
            if fastIVcold_found:
                regrid_fastcold_matrix, status  = regrid(fastcold_matrix, regrid_mesh, verbose)
                fastcold_matrix = regrid_fastcold_matrix 
        
        # do a convoltion to the data, this does not effect mV
        if do_conv:
            conv_hot_matrix, status  = conv(hot_matrix,  regrid_mesh, min_cdf, sigma, verbose)
            conv_cold_matrix, status = conv(cold_matrix, regrid_mesh, min_cdf, sigma, verbose)
            
            hot_matrix  = regrid_hot_matrix
            cold_matrix = regrid_cold_matrix
            
            if fastIVhot_found:
                conv_fasthot_matrix, status  = conv(fasthot_matrix,  regrid_mesh, min_cdf, sigma, verbose)
                fasthot_matrix = conv_fasthot_matrix
            if fastIVcold_found:
                conv_fastcold_matrix  = conv(fastcold_matrix, regrid_mesh, min_cdf, sigma, verbose)
                fastcold_matrix, status = conv_fastcold_matrix 
            
        # put the information back into 1-D arrays
        hot_sweep_mV_mean   = hot_matrix[:,0]
        hot_sweep_mV_std    = hot_matrix[:,1]
        hot_sweep_uA_mean   = hot_matrix[:,2]
        hot_sweep_uA_std    = hot_matrix[:,3]
        hot_sweep_TP_mean   = hot_matrix[:,4]
        hot_sweep_TP_std    = hot_matrix[:,5]
        hot_sweep_TP_num    = hot_matrix[:,6]
        hot_sweep_TP_freq   = hot_matrix[:,7]
        hot_sweep_time_mean = hot_matrix[:,8]
        hot_sweep_pot       = hot_matrix[:,9]
        hot_sweep_meas_num  = hot_matrix[:,10]
        
        cold_sweep_mV_mean   = cold_matrix[:,0]
        cold_sweep_mV_std    = cold_matrix[:,1]
        cold_sweep_uA_mean   = cold_matrix[:,2]
        cold_sweep_uA_std    = cold_matrix[:,3]
        cold_sweep_TP_mean   = cold_matrix[:,4]
        cold_sweep_TP_std    = cold_matrix[:,5]
        cold_sweep_TP_num    = cold_matrix[:,6]
        cold_sweep_TP_freq   = cold_matrix[:,7]
        cold_sweep_time_mean = cold_matrix[:,8]
        cold_sweep_pot       = cold_matrix[:,9]
        cold_sweep_meas_num  = cold_matrix[:,10]
        
        # make the directory where this data goes
        prodatadir = datadir + "prodata/" + Ynum + '/'
        if not os.path.isdir(prodatadir):
            os.makedirs(prodatadir)
        
        if fastIVhot_found:
            mV_fasthot = fasthot_matrix[:,0]
            uA_fasthot = fasthot_matrix[:,1]
            tp_fasthot = fasthot_matrix[:,2]
            pot_fasthot = fasthot_matrix[:,3]
            
            # save fastIV hot processed data
            n = open(prodatadir + 'hotfastIV.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_fasthot)):
                writeline = str(mV_fasthot[mV_index]) + ',' + str(uA_fasthot[mV_index]) + ',' + str(tp_fasthot[mV_index]) + ',' + str(pot_fasthot[mV_index]) + '\n'
                n.write(writeline)
            n.close()
            
        if fastIVcold_found:
            mV_fastcold = fastcold_matrix[:,0]
            uA_fastcold = fastcold_matrix[:,1]
            tp_fastcold = fastcold_matrix[:,2]
            pot_fastcold = fastcold_matrix[:,3]
            
            # save fastIV cold processed data
            n = open(prodatadir + 'coldfastIV.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_fastcold)):
                writeline = str(mV_fastcold[mV_index]) + ',' + str(uA_fastcold[mV_index]) + ',' + str(tp_fastcold[mV_index]) + ',' + str(pot_fastcold[mV_index]) + '\n'
                n.write(writeline)
            n.close()
        
        ### The Yfactor calulation
        off_tp = 0 # need to fix this in the future
        if verbose:
            print "doing Y factor calulation"
        mV_Yfactor, Yfactor, status = data2Yfactor(hot_sweep_mV_mean, cold_sweep_mV_mean, off_tp, hot_sweep_TP_mean, cold_sweep_TP_mean, regrid_mesh, verbose)
        
        ### save the results of this calulations
        # hot data
        n = open(prodatadir + 'hotdata.csv', 'w')
        n.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,TP_num,TP_freq,time_mean,pot,meas_num\n')
        for sweep_index in range(len(hot_sweep_mV_mean)):
            n.write(str(hot_sweep_mV_mean[sweep_index]) + ',' + str(hot_sweep_mV_std[sweep_index]) + ',' + str(hot_sweep_uA_mean[sweep_index]) + ',' + str(hot_sweep_uA_std[sweep_index]) + ',' + str(hot_sweep_TP_mean[sweep_index]) + ',' + str(hot_sweep_TP_std[sweep_index]) + ',' + str(hot_sweep_TP_num[sweep_index]) + ',' + str(hot_sweep_TP_freq[sweep_index]) + ',' + str(hot_sweep_time_mean[sweep_index]) + ',' + str(hot_sweep_pot[sweep_index]) + ',' + str(hot_sweep_meas_num[sweep_index]) +'\n')
        n.close()
        
        # cold data
        m = open(prodatadir + 'colddata.csv', 'w')
        m.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,TP_num,TP_freq,time_mean,pot,meas_num\n')
        for sweep_index in range(len(cold_sweep_mV_mean)):
            m.write(str(cold_sweep_mV_mean[sweep_index]) + ',' + str(cold_sweep_mV_std[sweep_index]) + ',' + str(cold_sweep_uA_mean[sweep_index]) + ',' + str(cold_sweep_uA_std[sweep_index]) + ',' + str(cold_sweep_TP_mean[sweep_index]) + ',' + str(cold_sweep_TP_std[sweep_index]) + ',' + str(cold_sweep_TP_num[sweep_index]) + ',' + str(cold_sweep_TP_freq[sweep_index]) + ',' + str(cold_sweep_time_mean[sweep_index]) + ',' + str(cold_sweep_pot[sweep_index]) + ',' + str(cold_sweep_meas_num[sweep_index]) +'\n')
        m.close()
        
        # Y factor data
        o = open(prodatadir + 'Ydata.csv', 'w')
        o.write('mV_Yfactor,Yfactor\n')
        for sweep_index in range(len(mV_Yfactor)):
            o.write(str(mV_Yfactor[sweep_index]) + ',' + str(Yfactor[sweep_index]) + '\n')    
        o.close()
        
        # hot parameter files
        proparamsfile = prodatadir + 'prohotparams.csv'
        # record the parameters of every sweep
        n = open(proparamsfile, 'w')
        n.write('param, value\n')
        n.write('temp,' + str(hot_K_val) + '\n')
        if hot_magisweep == True:
            n.write('magisweep,True\n')
            n.write('magiset,' +  str(hot_magiset) + '\n')
            n.write('magpot,'  +  str(numpy.round(hot_magpot))       + '\n')
        else:
            n.write('magisweep,False\n')
            n.write('magpot,' +  str(hot_magpot) + '\n')
        n.write('meanmag_V,'  + str(numpy.mean(hot_standmagdata_V))  + '\n')
        n.write('stdmag_V,'   + str(numpy.std(hot_standmagdata_V))   + '\n')
        n.write('meanmag_mA,' + str(numpy.mean(hot_standmagdata_mA)) + '\n')
        n.write('stdmag_mA,'  + str(numpy.std(hot_standmagdata_mA))  + '\n')
        if hot_sisisweep == True:
            n.write('sisisweep,True\n')
            n.write('sisiset,'  + str(hot_sisiset)    + '\n')
            n.write('UCA_volt,' + str(hot_UCA_volt)   + '\n')
        else:
            n.write('sisisweep,False\n')
            n.write('UCA_volt,' + str(hot_UCA_volt) + '\n')
        n.write('meanSIS_mV,' + str(numpy.mean(hot_standSISdata_mV)) + '\n')
        n.write('stdSIS_mV,'  + str(numpy.std(hot_standSISdata_mV))  + '\n')
        n.write('meanSIS_uA,' + str(numpy.mean(hot_standSISdata_uA)) + '\n')
        n.write('stdSIS_uA,'  + str(numpy.std(hot_standSISdata_uA))  + '\n')
        n.write('meanSIS_tp,' + str(numpy.mean(hot_standSISdata_tp)) + '\n')
        n.write('stdSIS_tp,'  + str(numpy.std(hot_standSISdata_tp))  + '\n')
        n.write('SIS_pot,'    + str(hot_standSISdata_pot[0])         + '\n')
        n.write('del_time,'   + str(numpy.max(hot_standSISdata_time) - numpy.min(hot_standSISdata_time))  + '\n')
        n.write('LOfreq,' + str(hot_LOfreq) + '\n')
        n.write('IFband,' + str(hot_IFband) + '\n')
        n.close()        
        
        # cold parameter files
        proparamsfile = prodatadir + 'procoldparams.csv'
        # record the parameters of every sweep
        n = open(proparamsfile, 'w')
        n.write('param, value\n')
        n.write('temp,' + str(cold_K_val) + '\n')
        if cold_magisweep == True:
            n.write('magisweep,True\n')
            n.write('magiset,' +  str(cold_magiset) + '\n')
            n.write('magpot,'  +  str(numpy.round(cold_magpot))       + '\n')
        else:
            n.write('magisweep,False\n')
            n.write('magpot,' +  str(cold_magpot) + '\n')
        n.write('meanmag_V,'  + str(numpy.mean(cold_standmagdata_V))  + '\n')
        n.write('stdmag_V,'   + str(numpy.std(cold_standmagdata_V))   + '\n')
        n.write('meanmag_mA,' + str(numpy.mean(cold_standmagdata_mA)) + '\n')
        n.write('stdmag_mA,'  + str(numpy.std(cold_standmagdata_mA))  + '\n')
        if cold_sisisweep == True:
            n.write('sisisweep,True\n')
            n.write('sisiset,'  + str(cold_sisiset)    + '\n')
            n.write('UCA_volt,' + str(cold_UCA_volt)   + '\n')
        else:
            n.write('sisisweep,False\n')
            n.write('UCA_volt,' + str(cold_UCA_volt) + '\n')
        n.write('meanSIS_mV,' + str(numpy.mean(cold_standSISdata_mV)) + '\n')
        n.write('stdSIS_mV,'  + str(numpy.std(cold_standSISdata_mV))  + '\n')
        n.write('meanSIS_uA,' + str(numpy.mean(cold_standSISdata_uA)) + '\n')
        n.write('stdSIS_uA,'  + str(numpy.std(cold_standSISdata_uA))  + '\n')
        n.write('meanSIS_tp,' + str(numpy.mean(cold_standSISdata_tp)) + '\n')
        n.write('stdSIS_tp,'  + str(numpy.std(cold_standSISdata_tp))  + '\n')
        n.write('SIS_pot,'    + str(cold_standSISdata_pot[0])         + '\n')
        n.write('del_time,'   + str(numpy.max(cold_standSISdata_time) - numpy.min(cold_standSISdata_time))  + '\n')
        n.write('LOfreq,' + str(cold_LOfreq) + '\n')
        n.write('IFband,' + str(cold_IFband) + '\n')
        n.close()
        
        
        if verbose:
            print ' '
    if verbose:
        print "The YdataPro function has completed"
        
    
    return

###################################
######### General Options #########
###################################

verbose=True # True or False

##### location of IV and TP parameter files, the data files
setnum  = 4
datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/initialize/'
#datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set2/'

search_4Ynums = True
search_str = 'Y'
Ynums=['Y0001'] # make a list array seporate array values with commas like Ynums = ['Y01', 'Y02']
do_fastIV = False

useOFFdata = False # True or False
Off_datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'

###########################################
######### Data Processing Options #########
###########################################

mono_switcher = True # makes data monotonic in mV

do_regrid=True
regrid_mesh=0.01 # in mV (default = 0.01)

do_conv = True
sigma   = 0.03 # in mV
min_cdf = 0.95 # fraction of Guassian used in kernal calulation

YdataPro(verbose, datadir, search_4Ynums, search_str, Ynums, useOFFdata, Off_datadir, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf, do_fastIV)