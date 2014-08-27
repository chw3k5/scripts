def SetDataPro(setNums, sisi_voltage, Begin_start_Yrange, End_end_Yrange, step_Yrange, verbose):
    import sys
    import atpy
    import numpy
    import os
    import shutil
    
    # This is the location of the Kappa Scripts on Caleb's Mac
    func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)
    # Now I import the scripts functions and programs that I have made to make my life easier
    from profunc import getparams
    
    Yranges = numpy.arange(Begin_start_Yrange,End_end_Yrange,step_Yrange)
    
    for Yrange_index in range(len(Yranges)):
        Yrange = Yranges[Yrange_index]
        if verbose:
            print 'getting set data for the Y factor at: ' + str('%1.2f' % Yrange) + ' mV,  all other parameters (including SIS current) are measured at: ' + str('%1.2f' % sisi_voltage) + ' mV.'
        for ii in range(len(setNums)):
            ##### location of IV and TP parameter files, the data files
            setnum = setNums[ii]
            if (Yrange_index == 0):
                datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'
                setdatadir = datadir + '/setdata/'
                if os.path.isdir(setdatadir):
                    shutil.rmtree(setdatadir)
                os.makedirs(setdatadir)
            
            setfile = setdatadir + 'Y' + str('%1.2f' % Yrange) +'mV.csv'
            prodatadir = datadir + 'prodata/'
            
            # read in y factor curves
            # get the Y numbers from the directory names in the datadir directory
            alldirs = []
            for root, dirs, files in os.walk(prodatadir):
                alldirs.append(dirs)
                Ynums = alldirs[0]
            
            n = open(setfile, 'w')
            n.write('Ynum,sisi_voltage,magpot,magi,mV,hot_mV_std,hot_uA_mean,hot_uA_std,hot_TP_mean,hot_TP_std,hot_TP_num,hot_TP_freq,hot_time_mean,hot_pot,hot_meas_num,cold_mV_std,cold_uA_mean,cold_uA_std,cold_TP_mean,cold_TP_std,cold_TP_num,cold_TP_freq,cold_time_mean,cold_pot,cold_meas_num,Yfactor,YmV\n')
            
            for Ynum_index in range(len(Ynums)):
                Ynum = Ynums[Ynum_index]
                ### get the hot Y factor data
                hotdir = datadir + 'rawdata/' + str(Ynum) + '/hot/'
                paramsfile = hotdir + 'params.csv'
                # load the parametes of the data
                hot_K_val, hot_magisweep, hot_magiset, hot_magpot, hot_sisisweep, hot_sisiset, hot_UCA_volt, hot_LOfreq, hot_IFband = getparams(paramsfile)
                magpot = hot_magpot
                magi   = hot_magiset            
                
                hotdatafile  = prodatadir + Ynum + '/hotdata.csv'
                colddatafile = prodatadir + Ynum + '/colddata.csv'
                Ydatafile    = prodatadir + Ynum + '/Ydata.csv'
            
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
                #min_len    = min(len_hot, len_cold, len_Y)
                
                last_hot   = hot_mV_mean[len_hot-1]
                last_cold  = cold_mV_mean[len_cold-1]
                last_Y     = mV_Yfactor[len_Y-1]
                #min_last   = min(last_hot, last_cold, last_Y)
                
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
                
                #mV_max_Yfactor, max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, status = Ydata_stats(mV_Yfactor, Yfactor, start_Yrange, end_Yrange)
                
                sisi_voltage_index = -1
                Yrange_index       = -1
                mindiff = 999999
                minYdiff = 999999
                for meas_index in range(len(mV)):
                    diff = abs(sisi_voltage - mV[meas_index])
                    if diff < mindiff:
                        mindiff = diff
                        sisi_voltage_index = meas_index
                    diff = abs(Yrange - mV[meas_index])
                    if diff < minYdiff:
                        minYdiff = diff
                        Yrange_index = meas_index
                        
    
                write_str = str(Ynum) + ',' + str(sisi_voltage) + ',' 
                write_str = write_str + str(magpot) + ',' + str(magi) + ',' + str(hot_mV_std[sisi_voltage_index]) + ',' + str(mV[sisi_voltage_index]) + ',' 
                write_str = write_str + str(hot_uA_mean[sisi_voltage_index]) + ',' + str(hot_uA_std[sisi_voltage_index]) + ',' + str(hot_TP_mean[sisi_voltage_index]) + ',' 
                write_str = write_str + str(hot_TP_std[sisi_voltage_index]) + ',' + str(hot_TP_num[sisi_voltage_index]) + ',' + str(hot_TP_freq[sisi_voltage_index]) + ',' 
                write_str = write_str + str(hot_time_mean[sisi_voltage_index]) + ',' + str(hot_pot[sisi_voltage_index]) + ',' + str(hot_meas_num[sisi_voltage_index]) + ',' 
                write_str = write_str + str(cold_mV_std[sisi_voltage_index]) + ',' + str(cold_uA_mean[sisi_voltage_index]) + ',' + str(cold_uA_std[sisi_voltage_index]) + ',' 
                write_str = write_str + str(cold_TP_mean[sisi_voltage_index]) + ',' + str(cold_TP_std[sisi_voltage_index]) + ',' + str(cold_TP_num[sisi_voltage_index]) + ',' 
                write_str = write_str + str(cold_TP_freq[sisi_voltage_index]) + ',' + str(cold_time_mean[sisi_voltage_index]) + ',' + str(cold_pot[sisi_voltage_index]) + ',' 
                write_str = write_str + str(cold_meas_num[sisi_voltage_index]) + ',' + str(Yfactor[Yrange_index]) + ',' + str(Yrange) +'\n'
                n.write(write_str)
            n.close()

    return
    
##############################
###### Set Data Options ######
##############################

setNums  = [3]
sisi_voltage = 1.8 # mV

Begin_start_Yrange = 1.75 # in mV
End_end_Yrange     = 2.21 # in mV
step_Yrange        = 0.05 # in mV
verbose = True

SetDataPro(setNums, sisi_voltage, Begin_start_Yrange, End_end_Yrange, step_Yrange, verbose)


      