from profunc import getparams, getSISdata, getmagdata, get_fastIV, ProcessMatrix, \
    getLJdata, readspec, renamespec, windir, local_copy
from domath import conv, spike_removal, regrid
from calibration import fetchoffset
import os, numpy, sys, glob, shutil
from sys import platform
import pickle

def ParamsProcessing(dirnames, proparamsfile, verbose):
    params_found        = False
    standSISdata_found  = False
    standmagdata_found  = False
    ###### Processing Params file ######
    paramsfile = dirnames + 'params.csv'
    if os.path.isfile(paramsfile):
        params_found  = True
        # load the params file for the data
        K_val, magisweep, magiset, magpot, LOuAsearch, LOuAset, UCA_volt, LOuA_set_pot, LOuA_magpot, LOfreq, IFband, mag_chan \
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
        ########
        m_magoffset, b_magoffset = fetchoffset(filename=str(mag_chan)+'mA_biascom-mA_meas.csv', mag_channel=mag_chan, path=dirnames)
        n.write('mag_chan,'   + str(mag_chan)                    + '\n')
        n.write('meanmag_V,'  + str((numpy.mean(standmagdata_V)*m_magoffset)+b_magoffset) + '\n')
        n.write('stdmag_V,'   + str((numpy.std(standmagdata_V)*m_magoffset)+b_magoffset)   + '\n')
        n.write('meanmag_mA,' + str((numpy.mean(standmagdata_mA)*m_magoffset)+b_magoffset) + '\n')
        n.write('stdmag_mA,'  + str((numpy.std(standmagdata_mA)*m_magoffset)+b_magoffset)  + '\n')

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
    fastIV_found = False
    if os.path.isfile(fastIV_filename):
        fastIV_found = True
        # load the fast IV data
        mV_fastIV, uA_fastIV, tp_fastIV, pot_fastIV = get_fastIV(fastIV_filename)
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

def BasicDataPro(sweepdir, prodataname, is_SIS_data=True, mono_switcher=True, do_regrid=True,
                 do_conv=False, regrid_mesh=0.01, min_cdf=0.9, sigma=0.05,
                 verbose=False):
    BasicDataFound = False
    if platform == 'win32':
        sweepdir = windir(sweepdir)
    if is_SIS_data:
        data_list = glob.glob(sweepdir + "SIS*.csv")
    else:
        data_list = glob.glob(sweepdir + "MAG*.csv")

    if not data_list == []:
        BasicDataFound  = True
        len_data_list   = len(data_list)
        P_sweep        = []
        V_mean_sweep   = []
        V_std_sweep    = []
        I_mean_sweep   = []
        I_std_sweep    = []
        # read in SIS data for each sweep step
        for sweep_index in range(len_data_list):
            if is_SIS_data:
                temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(sweepdir + 'SIS' + str(sweep_index + 1) + '.csv')
                V = temp_mV
                I = temp_uA
                P = temp_pot
            else:
                V, mA, pot = getmagdata(sweepdir + 'MAG' + str(sweep_index + 1) + '.csv')
                I = mA
                P = pot

            P_sweep.append(P[0])
            V_mean_sweep.append(numpy.mean(V))
            V_std_sweep.append(numpy.std(V))
            I_mean_sweep.append(numpy.mean(I))
            I_std_sweep.append(numpy.std(I))


        # put the data into a matrix for processing
        matrix  = numpy.zeros((len_data_list, 5))
        matrix[:,0]  = V_mean_sweep
        matrix[:,1]  = V_std_sweep
        matrix[:,2]  = I_mean_sweep
        matrix[:,3]  = I_std_sweep
        matrix[:,4]  = P_sweep
        # process the matrix
        matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix \
            = ProcessMatrix(matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
        # put the information back into 1-D arrays
        V_mean_sweep   = matrix[:,0]
        V_std_sweep    = matrix[:,1]
        I_mean_sweep   = matrix[:,2]
        I_std_sweep    = matrix[:,3]
        P_sweep        = matrix[:,4]
        len_pro_data_list = len(P_sweep)
        ### save the results of this calculations
        if platform == 'win32':
            prodataname = windir(prodataname)
        n = open(prodataname, 'w')
        if is_SIS_data:
            n.write('mV_mean,mV_std,uA_mean,uA_std,pot\n')
        else:
            n.write('V_mean,V_std,mA_mean,mA_std,pot\n')

        for sweep_index in range(len_pro_data_list):
            n.write(
                str(V_mean_sweep[sweep_index]) + ',' +
                str(V_std_sweep[sweep_index]) + ',' +
                str(I_mean_sweep[sweep_index]) + ',' +
                str(I_std_sweep[sweep_index]) + ',' +
                str(P_sweep[sweep_index]) +'\n'
            )
        n.close()
    else:
        if verbose:
            if is_SIS_data:
                print "No SIS data was found in ", sweepdir
            else:
                print "No Magnet data was found in ", sweepdir
    return BasicDataFound

def getrawdata(sweepdir, verbose=False):
    astrosweep_found = False
    sweep_pot, sweep_mV_mean, sweep_mV_std,\
    sweep_uA_mean, sweep_uA_std, sweep_TP_mean, \
    sweep_TP_std, sweep_time_mean, \
    TP_int_time, meas_num, TP_num, TP_freq \
        = None, None, None, None, None, None, None, None, None, None, None, None
    TP_list = glob.glob(windir(sweepdir) + "TP*.csv")
    if verbose:
        print "Fetching raw data in:", sweepdir

    if not TP_list == []:
        astrosweep_found = True
        (sweep_pot, sweep_mV_mean, sweep_mV_std,
        sweep_uA_mean, sweep_uA_std, sweep_TP_mean,
        sweep_TP_std, sweep_time_mean) = ([],[],[],[],[],[],[],[])
        for sweep_index in range(len(TP_list)):
            # read in SIS data for each sweep step
            thefilename = sweepdir + str(sweep_index + 1) + '.csv'
            temp_mV, temp_uA, temp_tp, temp_pot, temp_time = getSISdata(thefilename)
            sweep_pot.append(temp_pot[0])
            sweep_mV_mean.append(numpy.mean(temp_mV))
            sweep_mV_std.append(numpy.std(temp_mV))
            sweep_uA_mean.append(numpy.mean(temp_uA))
            sweep_uA_std.append(numpy.std(temp_uA))
            sweep_time_mean.append(numpy.mean(temp_time))
            temp_TP, TP_freq, PM_range = getLJdata(sweepdir + "TP" + str(sweep_index + 1) + '.csv')
            if sweep_index == 0:
                TP_int_time    = len(temp_TP)/TP_freq
                meas_num = len(temp_mV)
                TP_num   = len(temp_TP)
                TP_freq  = TP_freq
            sweep_TP_mean.append(numpy.mean(temp_tp))
            sweep_TP_std.append(numpy.std(temp_tp))

    return astrosweep_found, sweep_pot, sweep_mV_mean, sweep_mV_std,\
           sweep_uA_mean, sweep_uA_std, sweep_TP_mean, sweep_TP_std, sweep_time_mean,\
           TP_int_time, meas_num, TP_num, TP_freq



def AstroDataPro(datadir, proparamsfile, rawdataname, prodataname, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose):

    sweepdir = datadir + 'sweep/'

    astrosweep_found, sweep_pot, sweep_mV_mean, sweep_mV_std,\
    sweep_uA_mean, sweep_uA_std, sweep_TP_mean, sweep_TP_std, sweep_time_mean,\
    TP_int_time, meas_num, TP_num, TP_freq\
        = getrawdata(sweepdir, verbose=verbose)

    # Some Parts of the Parameter file are written here
    n = open(proparamsfile, 'a')
    if meas_num is not None:n.write('meas_num,' + str(meas_num) + '\n')
    if TP_int_time is not None:n.write('TP_int_time,' + str(TP_int_time) + '\n')
    if TP_num is not None:n.write('TP_num,' + str(TP_num) + '\n')
    if TP_freq is not None:n.write('TP_freq,' + str(TP_freq) + '\n')
    n.close()

    if astrosweep_found:
        # Write the minimally processed data to a file
        rawfile = open(rawdataname, 'w')
        rawfile.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std\n')
        for sweep_index in range(len(sweep_mV_mean)):
            rawfile.write(str(sweep_mV_mean[sweep_index]) + ',' +
                    str(sweep_mV_std[sweep_index])  + ',' +
                    str(sweep_uA_mean[sweep_index]) + ',' +
                    str(sweep_uA_std[sweep_index])  + ',' +
                    str(sweep_TP_mean[sweep_index]) + ',' +
                    str(sweep_TP_std[sweep_index])  + '\n'
                    )
        rawfile.close()


        if 1 < len(sweep_mV_mean):
            # put the data into a matrix for processing
            matrix  = numpy.zeros((len(sweep_mV_mean), 11))
            matrix[:,0]  = sweep_mV_mean
            matrix[:,1]  = sweep_mV_std
            matrix[:,2]  = sweep_uA_mean
            matrix[:,3]  = sweep_uA_std
            matrix[:,4]  = sweep_TP_mean
            matrix[:,5]  = sweep_TP_std
            matrix[:,6]  = sweep_time_mean
            matrix[:,7]  = sweep_pot
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
            sweep_time_mean = matrix[:,6]
            sweep_pot       = matrix[:,7]


        ### save the results of this calculations
        n = open(prodataname, 'w')
        n.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,time_mean,pot\n')
        for sweep_index in range(len(sweep_mV_mean)):
            n.write(str(sweep_mV_mean[sweep_index]) + ',' +                    \
            str(sweep_mV_std[sweep_index])    + ',' +                          \
            str(sweep_uA_mean[sweep_index])   + ',' +                          \
            str(sweep_uA_std[sweep_index])    + ',' +                          \
            str(sweep_TP_mean[sweep_index])   + ',' +                          \
            str(sweep_TP_std[sweep_index])    + ',' +                          \
            str(sweep_time_mean[sweep_index]) + ',' +                          \
            str(sweep_pot[sweep_index]) +'\n')
        n.close()
    else:
        print "No total Power data was found in ", datadir
        print "Killing Script"
        sys.exit()

    return astrosweep_found, sweep_mV_mean, sweep_TP_mean, TP_int_time



def GetSpecData(datadir, specdataname, remove_spikes=False,
                 do_norm=True,  norm_freq=1.42, norm_band=0.060,
                 mono_switcher_mV=True,
                 do_regrid_mV=True, regrid_mesh_mV_spec=None,
                 do_conv_mV=False,  min_cdf_mV=0.90, sigma_mV=0.03,
                 do_freq_conv=False, min_cdf_freq=0.90, sigma_GHz=0.05,
                 verbose=False):
    do_renamespec = False
    specsweep_found = False
    sweepdir = datadir + 'sweep/'
    sweepdir = windir(sweepdir)

    spec_list = glob.glob(sweepdir + "spec*.csv")

    norm_radius = norm_band/2.0
    spikes_inband = None
    if not spec_list == []:
        specsweep_found = True

        # Just reading in the data and putting that data into a list of tuple
        spec_data_list = []
        for sweep_index in range(len(spec_list)):
            # read in SIS data for each sweep step
            biasfilename = sweepdir + str(sweep_index + 1) + '.csv'
            temp_mV, temp_uA, temp_tp, temp_pot_array, temp_time = getSISdata(biasfilename)

            temp_pot = temp_pot_array[0]
            temp_mV_mean = numpy.mean(temp_mV)

            # read in the spectral data
            specfilename = sweepdir + "spec" +str(sweep_index + 1) + '.csv'
            temp_freq, temp_pwr = readspec(specfilename)
            spike_list = []

            # this is an option I once needed to replace a bad header for the spectral data file
            if do_renamespec:
                renamespec(specfilename)

            spec_data_list.append((temp_freq,temp_pwr,temp_pot,temp_mV_mean,temp_tp,spike_list,spikes_inband,sweep_index))


        # Checking to make sure the frequencies of this set of spectra are the same
        sweep_freqs = []
        normfreq_indexes = []
        for (temp_freq,temp_pwr,temp_pot,temp_mV_mean,temp_tp,spike_list,spikes_inband,sweep_index) in spec_data_list:
            ### First loop only checking if normalization of the spectral data and the power meter is possible###
            # start to process the spectral data, normalize it and put it in a 2D list
            if sweep_freqs == []:
                sweep_freqs = temp_freq
            ### After first loop, this makes sure the frequencies of all spectra in a given set of sweeps line up
            elif not ((abs(sweep_freqs[0] - temp_freq[0]) < 0.0001) and (abs(sweep_freqs[-1] - temp_freq[-1]) < 0.0001)):
                print "Somehow the sweep start and stop frequencies in the sweep dir ", datadir
                print "are not the same for sweep 1 and sweep ", sweep_index
                print "Killing script"
                sys.exit()

        ###############
        ###### Data Processing of spectra in the frequency Domain
        ###############

        # spike removal, this detects and deletes spikes in a data set.
        data_to_clean = []
        if remove_spikes:

            spike_data_temp = []
            for (freq,pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index) in spec_data_list:
                data_to_clean.append((freq,pwr))
            # everything happens in this function, res of this is just book keeping
            clean_data, spike_lists_for_spectra, spike_list_for_set = spike_removal(data_to_clean)

            # find out if spikes are in the normalization band and set a flag if they are
            for (old_freq,old_pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index) in spec_data_list:
                (freq,pwr) = clean_data[sweep_index]
                spike_list.extend(spike_lists_for_spectra[sweep_index])
                spike_list.extend(spike_list_for_set)

                for (f_index,spike_freq) in list(enumerate(spike_list)):
                    spikes_inband = False
                    if abs(spike_freq-norm_freq) <= norm_radius:
                        spikes_inband = True
                spike_data_temp.append((freq,pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index))
            spec_data_list = spike_data_temp

        spec_data_list_temp = []
        for (freq,pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index) in spec_data_list:
            ### Regrid the spectra to fix any holes or over lap.
            # This part makes a dictionary of the length of frequency steps in a spectrum and its occurrences
            # and set the frequency mesh for regridding
            step_vector = list(numpy.array(freq[1:])-numpy.array(freq[:-1]))
            step_dict = {element:step_vector.count(element) for element in step_vector}
            max_occurrence_finder = 0
            freq_mesh=0.001
            for step_freq, occurrences in step_dict.iteritems():
                if max_occurrence_finder < occurrences:
                    freq_mesh=step_freq
                    max_occurrence_finder = occurrences

            # send the data to the regridding function
            data_matrix = numpy.zeros((len(freq),2))
            data_matrix[:,0]=freq
            data_matrix[:,1]=pwr
            regrid_data, status = regrid(data_matrix, freq_mesh, verbose)
            freq = regrid_data[:,0]
            pwr  = regrid_data[:,1]



            if do_freq_conv:
                data_matrix = numpy.zeros((len(freq),2))
                data_matrix[:,0]=freq
                data_matrix[:,1]=pwr
                conv_data, status = conv(data_matrix, freq_mesh, min_cdf_freq, sigma_GHz, verbose)
                freq = conv_data[:,0]
                pwr  = conv_data[:,1]

                        ### Normalization of spectrum analyzer data to that of the filtered power meter.
            if do_norm:
                inband_spec_pwr = []
                # Find normalization band indexes
                freqs_out_of_band = True
                for (f_index,f_element) in list(enumerate(freq)):
                    if abs(f_element-norm_freq) <= norm_radius:
                        inband_spec_pwr.append(pwr[f_index])
                        freqs_out_of_band = False
                if freqs_out_of_band:
                    print "No frequencies were for the center frequency of ", norm_freq, " GHz"
                    print "for the band_with of ", norm_band, "GHz"
                    print "In the directory ", datadir, " for sweep 1"
                    print "do normalization is set to False "

                if ((not freqs_out_of_band)):# and (not spikes_inband)):
                    ave_inband_spec_pwr = numpy.mean(inband_spec_pwr)
                    norm_scale = numpy.mean(tp)/ave_inband_spec_pwr
                    pwr=(pwr*norm_scale)

            spec_data_list_temp.append((freq,pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index))
            # save this processed data for analysis and plotting
            save_filename = specdataname+"_"+str(sweep_index+1)+".npy"
            if verbose:
                print "saving spectral data:",save_filename
            the_can = (freq,pwr,pot,mV_mean,tp,spike_list,spikes_inband,sweep_index)
            data_str = pickle.dumps(the_can)
            with open(save_filename, 'w') as f:
                f.write(data_str)



        ###############
        ###### Below (still working) is the part of the code that does the my normal data processing
        ###############



        # if regrid_mesh_mV_spec is not None:
        #     ### Process the array that the spectra so the the there are regularly spaced units of mV, and convolved
        #     spec_mV_array = numpy.array(sweep_pwr)
        #     # put the mV data on the 2D array of pwr(mV,freq) so that it can be sorted
        #     mV_len   = len(spec_mV_array[:,0])
        #     freq_len = len(spec_mV_array[0,:])
        #     data_matrix = numpy.zeros((mV_len,freq_len+1))
        #     data_matrix[:,0]  = sweep_mV_mean
        #     data_matrix[:,1:] = spec_mV_array
        #
        #     # Process the matrix in mV
        #     data_matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix \
        #         = ProcessMatrix(data_matrix, mono_switcher_mV, do_regrid_mV, do_conv_mV, regrid_mesh_mV_spec,
        #                         min_cdf_mV, sigma_mV, verbose)
        #     new_mV_list   = list(data_matrix[:,0])
        #     new_mV_len    = len(new_mV_list)
        #     spec_mV_array = data_matrix[:,1:]
        # else:
        #     spec_mV_array = sweep_pwr
        #
        # ### Do a convolution of the matrix in frequency
        # if do_freq_conv:
        #     spec_mV_array_transpose = numpy.matrix.transpose(spec_mV_array)
        #     # put the frequency data on the 2D array of spec_mV_array_transpose so that it can be convolved in the
        #     # expected format
        #     data_matrix = numpy.zeros((freq_len,new_mV_len+1))
        #     data_matrix[:,0]  = sweep_freqs
        #     data_matrix[:,1:] = spec_mV_array_transpose
        #     freq_mesh = abs(sweep_freqs[1] - sweep_freqs[0])
        #     conv_matrix, status = conv(data_matrix, freq_mesh, min_cdf_freq, sigma_GHz, verbose)
        #
        #     # transpose the data back to maintain a constant format
        #     spec_mV_array = numpy.matrix.transpose(conv_matrix[:,1:])
        #
        # ### save the results in three arrays for plotting
        # #X
        # freq_pre_array = []
        # for n in range(new_mV_len):
        #     freq_pre_array.append(sweep_freqs)
        # freq_array = numpy.array(freq_pre_array)
        # numpy.save(specdataname+"_freq.npy",freq_array)
        #
        # #Y
        # mV_pre_array = []
        # for n in range(freq_len):
        #     mV_pre_array.append(new_mV_list)
        # mV_array = numpy.matrix.transpose(numpy.array(mV_pre_array))
        # numpy.save(specdataname+"_mV.npy",mV_array)
        #
        # #Z
        # numpy.save(specdataname+"_pwr.npy",spec_mV_array)
    else:
        if verbose:
            print "Data from the spectrum analyser was not found"

    return specsweep_found





def GetSpecData_old(datadir, specdataname, remove_spikes=False, do_norm=True,  norm_freq=1.42, norm_band=0.060,  mono_switcher_mV=True,
                do_regrid_mV=True, do_conv_mV=False, regrid_mesh_mV_spec=None, min_cdf_mV=0.90, sigma_mV=0.03,
                do_freq_conv=False, min_cdf_freq=0.90, sigma_GHz=0.05, verbose=False):
    do_renamespec = False
    specsweep_found = False
    sweepdir = datadir + 'sweep/'
    if platform == 'win32':
        sweepdir = windir(sweepdir)

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


            # spike removal
            # if remove_spikes:
            #     temp_pwr = spike_removal(temp_pwr,verbose=verbose)

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
        if regrid_mesh_mV_spec is not None:
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
                = ProcessMatrix(data_matrix, mono_switcher_mV, do_regrid_mV, do_conv_mV, regrid_mesh_mV_spec,
                                min_cdf_mV, sigma_mV, verbose)
            new_mV_list   = list(data_matrix[:,0])
            new_mV_len    = len(new_mV_list)
            spec_mV_array = data_matrix[:,1:]
        else:
            spec_mV_array = sweep_pwr

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


def SweepPro(datadir, proparamsfile, prodataname_fast, prodataname_unpump, rawdataname_ast, prodataname_ast, specdataname,
             mono_switcher_mV=True, do_regrid_mV=True, do_conv_mV=False, regrid_mesh_mV=0.01, min_cdf_mV=0.90, sigma_mV=0.03,
             remove_spikes=False, do_normspectra=False,
             regrid_mesh_mV_spec=0.1, norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90,
             sigma_GHz=0.05,verbose=False):

    ###### Make the parameters file
    params_found, standSISdata_found, standmagdata_found =                     \
    ParamsProcessing(datadir, proparamsfile, verbose)
    
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
    astrosweep_found, sweep_mV_mean, sweep_TP_mean, TP_int_time \
        = AstroDataPro(datadir, proparamsfile, rawdataname_ast, prodataname_ast, mono_switcher_mV, do_regrid_mV, do_conv_mV, regrid_mesh_mV, min_cdf_mV,
                 sigma_mV, verbose)
    n = open(proparamsfile, 'a')
    n.write('TP_int_time,'  + str(TP_int_time)  + '\n')
    n.close()

    ### get and process the spectra when available
    specsweep_found \
        = GetSpecData(datadir, specdataname, remove_spikes=remove_spikes, do_norm=do_normspectra, norm_freq=norm_freq, norm_band=norm_band,
                      mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, do_conv_mV=do_conv_mV,
                      regrid_mesh_mV_spec=regrid_mesh_mV_spec, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                      do_freq_conv=do_freq_conv, min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz, verbose=verbose)

    return params_found, standSISdata_found, standmagdata_found, fastIV_found, unpumped_found, astrosweep_found, \
           specsweep_found, sweep_mV_mean, sweep_TP_mean


def SweepDataPro(datadir, verbose=False, search_4Sweeps=True, search_str='Y', Snums=[],
                 mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01, do_conv_mV=False, sigma_mV=0.03, min_cdf_mV=0.95,
                 remove_spikes=False, do_normspectra=False, regrid_mesh_mV_spec=0.1, norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90, sigma_GHz=0.05):


    from profunc import getSnums
    prodatadir = datadir + "prodata/"
    if platform == 'win32':
        prodatadir = windir(prodatadir)
    if os.path.isdir(prodatadir):
        # remove old processed data
        shutil.rmtree(prodatadir)
        # make a folder for new processed data
        os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)

    rawdatadir = datadir + "rawdata/"
    if platform == 'win32':
        rawdatadir = windir(rawdatadir)
    ### Find all the Y## directory if search_4Ynums = True
    if search_4Sweeps:
        Snums = getSnums(rawdatadir)                   
        
    ### step through all the Ynumbers and Process their files
    for Snum in Snums:
        sweepdir = rawdatadir + Snum + '/'
        if platform == 'win32':
            sweepdir = windir(sweepdir)
        if verbose:
            print 'reducing data in: ' + sweepdir
        # make the directory where this data goes
        prodatadir = datadir + "prodata/" + Snum + '/'
        if platform == 'win32':
            prodatadir = windir(prodatadir)
        if not os.path.isdir(prodatadir):
            os.makedirs(prodatadir)
        #####################################
        #### Start Sweep data Processing ####
        #####################################
        
        proparamsfile      = prodatadir + 'proparams.csv'
        prodataname_fast   = prodatadir + 'fastIV.csv'
        prodataname_unpump = prodatadir + 'unpumped.csv'
        rawdataname_ast    = prodatadir + 'raw_data.csv'
        prodataname_ast    = prodatadir + 'data.csv'
        specdataname       = prodatadir + 'specdata'
        
        params_found, standSISdata_found, standmagdata_found, fastIV_found, unpumped_found, astrosweep_found,          \
        specsweep_found, sweep_mV_mean, sweep_TP_mean \
            = SweepPro(sweepdir, proparamsfile, prodataname_fast, prodataname_unpump, rawdataname_ast, prodataname_ast, specdataname,
             mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV, do_conv_mV=do_conv_mV,
             remove_spikes=remove_spikes, regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
             do_normspectra=do_normspectra,regrid_mesh_mV_spec=regrid_mesh_mV_spec, norm_freq=norm_freq, norm_band=norm_band, do_freq_conv=do_freq_conv,
             min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)

    return

def addInQuad(list_of_numbers):
    quadSum = 0
    for number in list_of_numbers:
        quadSum += float(number)**2
    magnitude=numpy.sqrt(quadSum)
    return magnitude


def raw2Yfactor(coldDir,hotDir,verbose=False):
    hotDir = windir(hotDir+'sweep/')
    coldDir = windir(coldDir+'sweep/')

    hot_astrosweep_found, hot_sweep_pot, hot_sweep_mV_mean, hot_sweep_mV_std,\
           hot_sweep_uA_mean, hot_sweep_uA_std, hot_sweep_TP_mean, hot_sweep_TP_std, hot_sweep_time_mean,\
           hot_TP_int_time, hot_meas_num, hot_TP_num, hot_TP_freq = getrawdata(hotDir, verbose=verbose)

    cold_astrosweep_found, cold_sweep_pot, cold_sweep_mV_mean, cold_sweep_mV_std,\
           cold_sweep_uA_mean, cold_sweep_uA_std, cold_sweep_TP_mean, cold_sweep_TP_std, cold_sweep_time_mean,\
           cold_TP_int_time, cold_meas_num, cold_TP_num, cold_TP_freq = getrawdata(coldDir, verbose=verbose)

    Yfactor_len = len(cold_sweep_pot)

    Yfactor=[]
    yerror=[]
    y_pot=[]
    y_mV=[]
    y_mVerror=[]
    y_uA=[]
    y_uAerror=[]
    y_TP=[]
    y_TPerror=[]
    for yindex in range(Yfactor_len):
        Yfactor.append(hot_sweep_TP_mean[yindex]/cold_sweep_TP_mean[yindex])
        yerror.append(addInQuad([hot_sweep_TP_std[yindex],cold_sweep_TP_std[yindex]]))
        if hot_sweep_pot[yindex] == cold_sweep_pot[yindex]:
            y_pot.append(hot_sweep_pot[yindex])
        else:
            print 'Problem in raw2Yfactor in datapro.py. The cold and hot sweep pot position are different and they\n'+\
                  'must be the same. hot_sweep_pot[yindex] =', hot_sweep_pot[yindex],\
                  '    cold_sweep_pot[yindex] =', cold_sweep_pot[yindex]
            print 'This is a script killer, sys.exit()'
            sys.exit()
        y_mV.append(numpy.mean([hot_sweep_mV_mean[yindex], cold_sweep_mV_mean[yindex]]))
        y_mVerror.append(addInQuad([hot_sweep_mV_std[yindex], cold_sweep_mV_std[yindex]]))

        y_uA.append(numpy.mean([hot_sweep_uA_mean[yindex],cold_sweep_uA_mean[yindex]]))
        y_uAerror.append(addInQuad([hot_sweep_uA_std[yindex],cold_sweep_uA_std[yindex]]))

        y_TP.append(numpy.mean([hot_sweep_TP_mean[yindex],cold_sweep_TP_mean[yindex]]))
        y_TPerror.append(addInQuad([hot_sweep_TP_std[yindex],cold_sweep_TP_std[yindex]]))

    return  Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror




def YdataPro(datadir, verbose=False, search_4Ynums=True, removeOldProData=False,
             search_str='Y', Ynums=[], use_google_drive=True,
             useOFFdata=False, Off_datadir='',
             mono_switcher_mV=True, do_regrid_mV=True, regrid_mesh_mV=0.01,
             do_conv_mV=False, sigma_mV=0.03, min_cdf_mV=0.95,
             remove_spikes=False, do_normspectra=False, regrid_mesh_mV_spec=0.1,
             norm_freq=1.42, norm_band=0.060, do_freq_conv=False, min_cdf_freq=0.90,
             sigma_GHz=0.05):


    from profunc import getYnums
    from domath import data2Yfactor, Specdata2Yfactor

    prodatadir = datadir + "prodata/"
    if not use_google_drive:
        prodatadir = local_copy(prodatadir)
    prodatadir = windir(prodatadir)
    if os.path.isdir(prodatadir):
        if removeOldProData:
            # remove old processed data
            shutil.rmtree(prodatadir)
            # make a folder for new processed data
            os.makedirs(prodatadir)
    else:
        # make a folder for new processed data
        os.makedirs(prodatadir)

    rawdatadir = windir(datadir + "rawdata/")

    ### Find all the Y## directory if search_4Ynums = True
    if search_4Ynums:
        Ynums = getYnums(rawdatadir, search_str)                   
        
    ### step through all the Ynumbers and Process their files
    for Ynum_index in range(len(Ynums)):
        Ynum = Ynums[Ynum_index]

        Ydatadir = windir(rawdatadir + Ynum + '/')

        if verbose:
            print 'reducing data in: ' + Ydatadir
        # make the directory where this data goes
        prodata_Ydir = windir(prodatadir + Ynum + '/')
        if not os.path.isdir(prodata_Ydir): os.makedirs(prodata_Ydir)
            
        ###################################
        #### Start Hot data Processing ####
        ###################################
        hotdir            = windir(Ydatadir   + 'hot/')
        hotproparamsfile      = prodata_Ydir + 'hotproparams.csv'
        hotprodataname_fast   = prodata_Ydir + 'hotfastIV.csv'
        hotprodataname_unpump = prodata_Ydir + 'hotunpumped.csv'
        hotrawdataname_ast    = prodata_Ydir + 'hotraw_data.csv'
        hotprodataname_ast    = prodata_Ydir + 'hotdata.csv'
        hotspecdataname       = prodata_Ydir + 'hotspecdata'
        
        hotparams_found, hotstandSISdata_found, hotstandmagdata_found, fastIVhot_found, hotunpumped_found, \
        astrosweephot_found, hotspecsweep_found, hot_sweep_mV_mean,hot_sweep_TP_mean \
            = SweepPro(hotdir, hotproparamsfile, hotprodataname_fast, hotprodataname_unpump, hotrawdataname_ast, hotprodataname_ast,
                       hotspecdataname, mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV,
                       do_conv_mV=do_conv_mV, regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                       remove_spikes=remove_spikes,do_normspectra=do_normspectra, regrid_mesh_mV_spec=regrid_mesh_mV_spec, norm_freq=norm_freq, norm_band=norm_band,
                       do_freq_conv=do_freq_conv,min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)
        
        ####################################
        #### Start Cold data Processing ####
        ####################################
        colddir            = windir(Ydatadir   + 'cold/')
        coldproparamsfile      = prodata_Ydir + 'coldproparams.csv'
        coldprodataname_fast   = prodata_Ydir + 'coldfastIV.csv'
        coldprodataname_unpump = prodata_Ydir + 'coldunpumped.csv'
        coldrawdataname_ast    = prodata_Ydir + 'coldraw_data.csv'
        coldprodataname_ast    = prodata_Ydir + 'colddata.csv'
        coldspecdataname       = prodata_Ydir + 'coldspecdata'
        
        coldparams_found, coldstandSISdata_found, coldstandmagdata_found, fastIVcold_found, coldunpumped_found,\
        astrosweepcold_found, coldspecsweep_found, cold_sweep_mV_mean,cold_sweep_TP_mean \
            = SweepPro(colddir, coldproparamsfile, coldprodataname_fast, coldprodataname_unpump, coldrawdataname_ast, coldprodataname_ast,
                       coldspecdataname, mono_switcher_mV=mono_switcher_mV, do_regrid_mV=do_regrid_mV,
                       do_conv_mV=do_conv_mV, regrid_mesh_mV=regrid_mesh_mV, min_cdf_mV=min_cdf_mV, sigma_mV=sigma_mV,
                       remove_spikes=remove_spikes,do_normspectra=do_normspectra, regrid_mesh_mV_spec=regrid_mesh_mV_spec, norm_freq=norm_freq, norm_band=norm_band,
                       do_freq_conv=do_freq_conv,min_cdf_freq=min_cdf_freq, sigma_GHz=sigma_GHz,verbose=verbose)


        ####################################
        ###### The Yfactor Calculation ######
        ####################################
        off_tp = 0 # need to fix this in the future
        if (astrosweephot_found and astrosweepcold_found):
            if verbose:
                print "doing Y factor calculation"

            Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror\
                    =raw2Yfactor(coldDir=colddir,hotDir=hotdir,verbose=verbose)
            Yfile = open(prodata_Ydir + 'Ydata.csv', 'w')
            Yfile.write('Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror\n')
            for yindex in range(len(Yfactor)):
                Yfile.write(str(Yfactor[yindex])+','+str(yerror[yindex])+','+str(y_pot[yindex])\
                            +','+str(y_mV[yindex])+','+str(y_mVerror[yindex])+','+\
                            str(y_uA[yindex])+','+str(y_uAerror[yindex])+','+str(y_TP[yindex])\
                            +','+str(y_TPerror[yindex])+'\n')
            Yfile.close()

            ###### OLD Y factor calculation
            # mV_Yfactor, Yfactor, status \
            #     = data2Yfactor(hot_sweep_mV_mean, cold_sweep_mV_mean, off_tp,
            #                    hot_sweep_TP_mean, cold_sweep_TP_mean, regrid_mesh_mV, verbose)
            # # save the results of the Y factor calculation
            # o = open(prodata_Ydir + 'Ydata.csv', 'w')
            # o.write('mV_Yfactor,Yfactor\n')
            #
            # for sweep_index in range(len(mV_Yfactor)):
            #     o.write(str(mV_Yfactor[sweep_index]) + ',' + str(Yfactor[sweep_index]) + '\n')
            # o.close()

        if (hotspecsweep_found and coldspecsweep_found):
            if verbose:
                print "doing spectral Y factor calculation"
            status = Specdata2Yfactor(prodata_Ydir, verbose=verbose)

    if verbose:
        print "The YdataPro function has completed"
        
    return

