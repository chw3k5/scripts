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
        K_val, magisweep, magiset, magpot, LOuAsearch, LOuAset, UCA_volt, LOuA_set_pot, LOuA_magpot, LOfreq, IFband \
            = getparams(paramsfile)
    
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
        if LOuAsearch == True:
            n.write('LOuAsearch,True\n')
            n.write('LOuAset,'  + str(LOuAset)    + '\n')
            n.write('UCA_volt,' + str(UCA_volt)   + '\n')
        else:
            n.write('LOuAsearch,False\n')
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

def ProFastIV(fastIV_filename,  prodataname, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose):
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
        fast_conv_matrix = ProcessMatrix(fast_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf,
                                         sigma, verbose)
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

def AstroDataPro(datadir, prodataname, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose):
    import sys
    from sys import platform
    import glob, numpy
    from profunc import getSISdata, getLJdata, ProcessMatrix
    astrosweep_found = False
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
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(sweepdir + str(sweep_index + 1) + '.csv')
            if verbose:
                print sweepdir + str(sweep_index + 1) + '.csv'
            sweep_pot.append(temp_pot[0])
            sweep_meas_num.append(len(temp_mV))
            sweep_mV_mean.append(numpy.mean(temp_mV))
            sweep_mV_std.append(numpy.std(temp_mV))
            sweep_uA_mean.append(numpy.mean(temp_uA))
            sweep_uA_std.append(numpy.std(temp_uA))
            sweep_time_mean.append(numpy.mean(temp_time))
            temp_TP, TP_freq = getLJdata(sweepdir + "TP" + str(sweep_index + 1) + '.csv')
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
        matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix \
            = ProcessMatrix(matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
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
        ### save the results of this calculations
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
    else:
        print "No total Power data was found in ", datadir
        print "Killing Script"
        sys.exit()

    return astrosweep_found, sweep_mV_mean, sweep_TP_mean

def GetSpecData(datadir, specdataname, do_norm=True,  norm_freq=1.42, norm_band=0.060,  mono_switcher_mV=True,
                do_regrid_mV=True, do_conv_mV=False, regrid_mesh_mV=0.01, min_cdf_mV=0.90, sigma_mV=0.03,
                do_freq_conv=False, min_cdf_freq=0.90, sigma_GHz=0.05, verbose=False):
    do_renamespec = False
    import sys
    from sys import platform
    import glob, numpy
    from profunc import getSISdata, readspec, ProcessMatrix, renamespec
    from domath import conv
    specsweep_found = False
    if platform == 'win32':
         sweepdir = datadir + 'sweep\\'
    elif platform == 'darwin':
        sweepdir = datadir + 'sweep/'
    spec_list = glob.glob(sweepdir + "spec*.csv")
    if not spec_list == []:
        specsweep_found = True
        sweep_pot       = []
        sweep_mV_mean   = []
        sweep_freqs     = []
        sweep_pwr       = []
        for sweep_index in range(len(spec_list)):
            # read in SIS data for each sweep step
            biasfilename = sweepdir + str(sweep_index + 1) + '.csv'
            specfilename = sweepdir + "spec" +str(sweep_index + 1) + '.csv'
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(biasfilename)
            if verbose:
                print specfilename
            sweep_pot.append(temp_pot[0])
            sweep_mV_mean.append(numpy.mean(temp_mV))

            # this is an option I once needed to replace a bad header for the spectral data file
            if do_renamespec:
                renamespec(specfilename)

            # read in the spectral data
            temp_freqs, temp_pwr = readspec(specfilename)
            # start to process the spectral data, normalize it and put it in a 2D list
            if sweep_freqs == []:
                sweep_freqs = temp_freqs
                # Find normalization band indexes
                normfreq_indexes = []
                norm_radius = norm_band/2.0
                freqs_out_of_band = True
                for freq_index in range(len(sweep_freqs)):
                    if abs(sweep_freqs[freq_index]-norm_freq) <= norm_radius:
                        normfreq_indexes.append(freq_index)
                        freqs_out_of_band = False
                if freqs_out_of_band:
                    print "No frequencies were for the center frequency of ", norm_freq, " GHz"
                    print "for the band_with of ", norm_band, "GHz"
                    print "In the directory ", datadir, " for sweep 1"
                    print "Killing Script"
                    sys.exit()
            # make sure the frequencies of all spectra in a given sweep line up
            elif not ((abs(sweep_freqs[0] - temp_freqs[0]) < 0.0001) and (abs(sweep_freqs[-1] - temp_freqs[-1]) < 0.0001)):
                print "Somehow the sweep start and stop frequencies in the sweep dir ", datadir
                print "are not the same for sweep 1 and sweep ", sweep_index
                print "Killing script"
                sys.exit()

            # Normalization
            if do_norm:
                inband_spec_pwr = []
                for norm_index in range(len(normfreq_indexes)):
                    inband_spec_pwr.append(temp_pwr[norm_index])
                ave_inband_spec_pwr = numpy.mean(inband_spec_pwr)
                norm_scale = numpy.mean(temp_tp)/ave_inband_spec_pwr
                sweep_pwr.append(temp_pwr*norm_scale)
            else:
                 sweep_pwr.append(temp_pwr)

        ### Process the array that the spectra so the the there are regularly spaced units of mV, and convolved
        spec_mV_array = numpy.array(sweep_pwr)
        # put the mV data on the 2D array of pwr(mV,freq) so that it can be sorted
        mV_len   = len(spec_mV_array[:,0])
        freq_len = len(spec_mV_array[0,:])
        data_matrix = numpy.zeros((mV_len,freq_len+1))
        data_matrix[:,0]  = sweep_mV_mean
        data_matrix[:,1:] = spec_mV_array

        # Process the matrix in mV
        data_matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix \
            = ProcessMatrix(data_matrix, mono_switcher_mV, do_regrid_mV, do_conv_mV, regrid_mesh_mV,
                            min_cdf_mV, sigma_mV, verbose)
        new_mV_list   = list(data_matrix[:,0])
        new_mV_len    = len(new_mV_list)
        spec_mV_array = data_matrix[:,1:]
        ### Do a convolution of the matrix in frequency
        if do_freq_conv:
            spec_mV_array_transpose = numpy.matrix.transpose(spec_mV_array)
            # put the frequency data on the 2D array of spec_mV_array_transpose so that it can be convolved in the
            # expected format
            data_matrix = numpy.zeros((freq_len,new_mV_len+1))
            data_matrix[:,0]  = sweep_freqs
            data_matrix[:,1:] = spec_mV_array_transpose
            freq_mesh = abs(sweep_freqs[1] - sweep_freqs[0])
            conv_matrix, status = conv(data_matrix, freq_mesh, min_cdf_freq, sigma_GHz, verbose)

            # transpose the data back to maintain a constant format
            spec_mV_array = numpy.matrix.transpose(conv_matrix[:,1:])

        ### save the results in three arrays for plotting
        #X
        freq_pre_array = []
        for n in range(new_mV_len):
            freq_pre_array.append(sweep_freqs)
        freq_array = numpy.array(freq_pre_array)
        numpy.save(specdataname+"_freq.npy",freq_array)

        #Y
        mV_pre_array = []
        for n in range(freq_len):
            mV_pre_array.append(new_mV_list)
        mV_array = numpy.matrix.transpose(numpy.array(mV_pre_array))
        numpy.save(specdataname+"_mV.npy",mV_array)

        #Z
        numpy.save(specdataname+"_pwr.npy",spec_mV_array)
    else:
        if verbose:
            print "Data from the spectrum analyser was not found"

    return specsweep_found


def SweepPro(datadir, proparamsfile, prodataname_fast, prodataname_unpump, prodataname_ast, specdataname,
             mono_switcher_mV=True, do_regrid_mV=True, do_conv_mV=False, regrid_mesh_mV=0.01, min_cdf_mV=0.90, sigma_mV=0.03,
             do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90,
             sigma_GHz=0.05,verbose=False):

    ###### Make the parameters file
    params_found, standSISdata_found, standmagdata_found =                     \
    ProParmsFiles(datadir, proparamsfile, verbose)
    
    ###### Processing fastIV data (data taken using the bais computer's sweep command)
    fastIV_filename = datadir + 'fastsweep.csv'
    fastIV_found \
        = ProFastIV(fastIV_filename,  prodataname_fast, mono_switcher_mV, do_regrid_mV, do_conv_mV,
                    regrid_mesh_mV, min_cdf_mV, sigma_mV, verbose)
    
    ###### Processing unpumped IV data (data taken using the bais computer's sweep command)
    #unpumped_found
    unpumped_filename  = datadir + 'unpumpedsweep.csv'
    unpumped_found \
        = ProFastIV(unpumped_filename,  prodataname_unpump, mono_switcher_mV, do_regrid_mV, do_conv_mV,
                    regrid_mesh_mV, min_cdf_mV, sigma_mV, verbose)

    ### get the astronomy quality sweep data for this Y sweep
    astrosweep_found, sweep_mV_mean, sweep_TP_mean \
        = AstroDataPro(datadir, prodataname_ast, mono_switcher_mV, do_regrid_mV, do_conv_mV, regrid_mesh_mV, min_cdf_mV,
                 sigma_mV, verbose)

    ### get and process the spectra when available
    specsweep_found \
        = GetSpecData(datadir, specdataname, do_norm=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                      mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, do_conv_mV=do_conv_mV,
                      regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                      do_freq_conv=do_freq_conv, min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz, verbose=verbose)

    return params_found, standSISdata_found, standmagdata_found, fastIV_found, unpumped_found, astrosweep_found, \
           specsweep_found, sweep_mV_mean, sweep_TP_mean


def SweepDataPro(datadir, verbose=False, search_4Sweeps=True, search_str='Y', Snums=[],
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=False, sigma_mV=0.03, min_cdf_mV=0.95,
                 do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90, sigma_GHz=0.05):
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
        specdataname       = prodatadir + 'specdata'
        
        params_found, standSISdata_found, standmagdata_found, fastIV_found, unpumped_found, astrosweep_found,          \
        specsweep_found, sweep_mV_mean, sweep_TP_mean \
            = SweepPro(sweepdir, proparamsfile, prodataname_fast, prodataname_unpump, prodataname_ast, specdataname,
             mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, do_conv_mV=do_conv_mV,
             regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
             do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band, do_freq_conv=do_freq_conv,
             min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)

    return

def YdataPro(datadir, verbose=False, search_4Ynums=True, search_str='Y', Ynums=[], useOFFdata=False, Off_datadir='',
             mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=False, sigma_mV=0.03, min_cdf_mV=0.95,
             do_normspectra=False, norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90,
             sigma_GHz=0.05):
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
        hotspecdataname       = prodatadir + 'hotspecdata'
        
        hotparams_found, hotstandSISdata_found, hotstandmagdata_found, fastIVhot_found, hotunpumped_found, \
        astrosweephot_found, hotspecsweep_found, hot_sweep_mV_mean,hot_sweep_TP_mean \
            = SweepPro(hotdir, hotproparamsfile, hotprodataname_fast, hotprodataname_unpump, hotprodataname_ast,
                       hotspecdataname, mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV,
                       do_conv_mV=do_conv_mV, regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                       do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                       do_freq_conv=do_freq_conv,min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)
        
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
        coldspecdataname       = prodatadir + 'coldspecdata'
        
        coldparams_found, coldstandSISdata_found, coldstandmagdata_found, fastIVcold_found, coldunpumped_found,        \
        astrosweepcold_found, coldspecsweep_found, cold_sweep_mV_mean,cold_sweep_TP_mean                                                    \
            = SweepPro(colddir, coldproparamsfile, coldprodataname_fast, coldprodataname_unpump, coldprodataname_ast,
                       coldspecdataname, mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV,
                       do_conv_mV=do_conv_mV, regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                       do_normspectra=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                       do_freq_conv=do_freq_conv,min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)
        
        ####################################
        ###### The Yfactor calulation ######
        ####################################
        off_tp = 0 # need to fix this in the future
        if (astrosweephot_found and astrosweepcold_found):
            if verbose:
                print "doing Y factor calculation"
            mV_Yfactor, Yfactor, status = data2Yfactor(hot_sweep_mV_mean, cold_sweep_mV_mean, off_tp,
                                                       hot_sweep_TP_mean, cold_sweep_TP_mean, regrid_mesh_mV, verbose)
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
#verbose=True # True or False (default is False)

##### location of IV and TP parameter files, the data files
#setnum  = 3
#datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'

#if platform == 'win32':
#    datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\set" +str(setnum) + "\\"
#    #datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\warmmag\\"
#elif platform == 'darwin':
#    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'
#    #datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'

#
# search_4Ynums = True # (the default is True)
# search_str = 'Y' # default is 'Y'
# Ynums=['Y0001'] # make a list array separate array values with commas like Ynums = ['Y01', 'Y02'] (defult is empty set [])
#
# useOFFdata = False # True or False
# Off_datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'
#
# ###########################################
# ######### Data Processing Options #########
# ###########################################
#
# mono_switcher = True # makes data monotonic in mV (default = True)
#
# do_regrid     = True # regrids data to uniform spacing (default = True)
# regrid_mesh   = 0.01 # in mV (default = 0.01)
#
# do_conv = True # does a gaussian convolution of the data after regridding (default is False)
# sigma   = 0.03 # in mV (default = 0.03)
# min_cdf = 0.95 # fraction of Gaussian used in kernel calculation (default = 0.95)

#YdataPro(datadir, verbose=True)
#SweepDataPro(datadir, verbose=True, search_4Sweeps=True, Snums=['00001'], do_normspectra=True, do_conv_mV=True, do_freq_conv=True)