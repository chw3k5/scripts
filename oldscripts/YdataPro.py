def YdataPro(verbose, datadir, search_4Ynums, search_str, Ynums, useOFFdata, Off_datadir, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf):
    import sys
    import glob
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

    from profunc import getparams, getSISdata, get_fastIV, getmagdata, getLJdata, getYnums, ProcessMatrix, do_derivative
    from domath import data2Yfactor, findlinear, resfitter
    
    der1_int     = 1
    do_der1_conv = True
    der1_min_cdf = 0.90
    der1_sigma   = 0.03
    
    der2_int     = 1
    do_der2_conv = True
    der2_min_cdf = 0.90
    der2_sigma   = 0.05
    
    linif         = 0.0005
    
    hotparams_found        = False
    hotstandSISdata_found  = False
    hotstandmagdata_found  = False
    fastIVhot_found        = False
    unpumpedhot_found      = False
    astrosweephot_found    = False
    
    coldparams_found       = False
    coldstandSISdata_found = False
    coldstandmagdata_found = False
    fastIVcold_found       = False
    unpumpedcold_found     = False
    astrosweepcold_found   = False
    
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
        # make the directory where this data goes
        prodatadir = datadir + "prodata/" + Ynum + '/'
        if not os.path.isdir(prodatadir):
            os.makedirs(prodatadir)
        ###################################
        #### Start Hot data Processing ####
        ###################################
        hotdir = Ydatadir + 'hot/'
        ###### Processing Params file ######
        hotparamsfile = hotdir + 'params.csv'
        if os.path.isfile(hotparamsfile):
            hotparams_found  = True
            # load the params file for the hot data
            hot_K_val, hot_magisweep, hot_magiset, hot_magpot, hot_sisisweep, hot_sisiset, hot_UCA_volt, hot_LOfreq, hot_IFband = getparams(hotparamsfile)
        
        ###### Processing Standard SIS bias measurments ######
        hotstandSISdatafile = hotdir + 'sisdata.csv'
        if os.path.isfile(hotstandSISdatafile):
            hotstandSISdata_found  = True
            # load the standard SIS bias measurments for the hot data
            hot_standSISdata_mV, hot_standSISdata_uA, hot_standSISdata_tp, hot_standSISdata_pot, hot_standSISdata_time = getSISdata(hotstandSISdatafile)
        
        ###### Processing Standard eletromagnet measurments ######
        hotstandmagdatafile = hotdir + 'magdata.csv'
        if os.path.isfile(hotstandmagdatafile):
            hotstandmagdata_found  = True
            # load the standard electromagnet measurments for the hot data
            hot_standmagdata_V, hot_standmagdata_mA, hot_standmagdata_pot = getmagdata(hotstandmagdatafile)
        
        ### hot processed parameter file (uses at most 'params.csv', 'sisdata.csv', 'magdata.csv')
        proparamsfile = prodatadir + 'prohotparams.csv'
        # record the parameters of every sweep
        n = open(proparamsfile, 'w')
        if hotparams_found:
            n.write('param, value\n')
            n.write('temp,' + str(hot_K_val) + '\n')
            if hot_magisweep == True:
                n.write('magisweep,True\n')
                n.write('magiset,' +  str(hot_magiset) + '\n')
                n.write('magpot,'  +  str(numpy.round(hot_magpot))       + '\n')
            else:
                n.write('magisweep,False\n')
                n.write('magpot,' +  str(hot_magpot) + '\n')
        if hotstandmagdata_found:
            n.write('meanmag_V,'  + str(numpy.mean(hot_standmagdata_V))  + '\n')
            n.write('stdmag_V,'   + str(numpy.std(hot_standmagdata_V))   + '\n')
            n.write('meanmag_mA,' + str(numpy.mean(hot_standmagdata_mA)) + '\n')
            n.write('stdmag_mA,'  + str(numpy.std(hot_standmagdata_mA))  + '\n')
        if hotparams_found:
            if hot_sisisweep == True:
                n.write('sisisweep,True\n')
                n.write('sisiset,'  + str(hot_sisiset)    + '\n')
                n.write('UCA_volt,' + str(hot_UCA_volt)   + '\n')
            else:
                n.write('sisisweep,False\n')
                n.write('UCA_volt,' + str(hot_UCA_volt) + '\n')
        if hotstandSISdata_found:
            n.write('meanSIS_mV,' + str(numpy.mean(hot_standSISdata_mV)) + '\n')
            n.write('stdSIS_mV,'  + str(numpy.std(hot_standSISdata_mV))  + '\n')
            n.write('meanSIS_uA,' + str(numpy.mean(hot_standSISdata_uA)) + '\n')
            n.write('stdSIS_uA,'  + str(numpy.std(hot_standSISdata_uA))  + '\n')
            n.write('meanSIS_tp,' + str(numpy.mean(hot_standSISdata_tp)) + '\n')
            n.write('stdSIS_tp,'  + str(numpy.std(hot_standSISdata_tp))  + '\n')
            n.write('SIS_pot,'    + str(hot_standSISdata_pot[0])         + '\n')
            n.write('del_time,'   + str(numpy.max(hot_standSISdata_time) - numpy.min(hot_standSISdata_time))  + '\n')
        if hotparams_found:
            n.write('LOfreq,' + str(hot_LOfreq) + '\n')
            n.write('IFband,' + str(hot_IFband) + '\n')
        n.close()
        
        
        ###### Processing fastIV data (data taken using the bais computer's sweep command)
        hotfastIV_filename = hotdir + 'fastsweep.csv'
        if os.path.isfile(hotfastIV_filename):
            fastIVhot_found = True
            # load the fast IV data
            mV_fastIVhot, uA_fastIVhot, tp_fastIVhot, pot_fastIVhot = get_fastIV(hotfastIV_filename)
            # put the data into a matrix for processing    
            fasthot_matrix = numpy.zeros((len(mV_fastIVhot), 4))
            fasthot_matrix[:,0] = mV_fastIVhot
            fasthot_matrix[:,1] = uA_fastIVhot
            fasthot_matrix[:,2] = tp_fastIVhot
            fasthot_matrix[:,3] = pot_fastIVhot
            # process the matrix
            fasthot_matrix, fasthot_raw_matrix, fasthot_mono_matrix, fasthot_regrid_matrix, fasthot_conv_matrix = ProcessMatrix(fasthot_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
            # put the information back into 1-D arrays
            mV_fasthot  = fasthot_matrix[:,0]
            uA_fasthot  = fasthot_matrix[:,1]
            tp_fasthot  = fasthot_matrix[:,2]
            pot_fasthot = fasthot_matrix[:,3]
            # save fastIV hot processed data
            n = open(prodatadir + 'hotfastIV.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_fasthot)):
                writeline = str(mV_fasthot[mV_index]) + ',' + str(uA_fasthot[mV_index]) + ',' + str(tp_fasthot[mV_index]) + ',' + str(pot_fasthot[mV_index]) + '\n'
                n.write(writeline)
            n.close()
            
        ###### Processing unpumped IV data (data taken using the bais computer's sweep command)
        hotunpumped_filename = hotdir + 'unpumpedsweep.csv'
        if os.path.isfile(hotunpumped_filename):
            unpumpedhot_found = True
            # load the fast IV data
            mV_unpumpedhot, uA_unpumpedhot, tp_unpumpedhot, pot_unpumpedhot = get_fastIV(hotunpumped_filename)
            # put the data into a matrix for processing
            unpumpedhot_matrix = numpy.zeros((len(mV_unpumpedhot), 4))
            unpumpedhot_matrix[:,0] = mV_unpumpedhot
            unpumpedhot_matrix[:,1] = uA_unpumpedhot
            unpumpedhot_matrix[:,2] = tp_unpumpedhot
            unpumpedhot_matrix[:,3] = pot_unpumpedhot
            # process the matrix
            unpumpedhot_matrix, unpumpedhot_raw_matrix, unpumpedhot_mono_matrix, unpumpedhot_regrid_matrix, unpumpedhot_conv_matrix = ProcessMatrix(unpumpedhot_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
            # put the information back into 1-D arrays
            mV_unpumpedhot  = unpumpedhot_matrix[:,0]
            uA_unpumpedhot  = unpumpedhot_matrix[:,1]
            tp_unpumpedhot  = unpumpedhot_matrix[:,2]
            pot_unpumpedhot = unpumpedhot_matrix[:,3]
            # save unpumped hot processed data
            n = open(prodatadir + 'hotunpumped.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_unpumpedhot)):
                writeline = str(mV_unpumpedhot[mV_index]) + ',' + str(uA_unpumpedhot[mV_index]) + ',' + str(tp_unpumpedhot[mV_index]) + ',' + str(pot_unpumpedhot[mV_index]) + '\n'
                n.write(writeline)
            n.close()
            # do derivatives to find linear regions
            shot_matrix = numpy.zeros((len(uA_unpumpedhot),3))
            shot_matrix[:,0] = uA_unpumpedhot
            shot_matrix[:,1] = mV_unpumpedhot
            shot_matrix[:,2] = tp_unpumpedhot
            der1, der2 = do_derivative(shot_matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose)
            #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
            #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
            
            status, lin_start_uAtp, lin_end_uAtp = findlinear(der2[:,0], der2[:,2], linif, verbose)
            slopes, intercepts, bestfits_uA, bestfits_tp = resfitter(uA_unpumpedhot, tp_unpumpedhot, lin_start_uAtp, lin_end_uAtp)
            
            import matplotlib        
            from matplotlib import pyplot as plt
            matplotlib.rc('text', usetex=True)
            
            plt.clf()
            matplotlib.rcParams['legend.fontsize'] = 10.0
            IV_color = 'blue'
            TP_color = 'red'
            shot_color = 'green'
            fig, ax1 = plt.subplots()
            ax1.plot(uA_unpumpedhot, tp_unpumpedhot, color=TP_color, linewidth=5)
            ax1.set_xlabel("current ($\mu$$A$)")
            ax1.set_ylabel('Receiver Power', color=TP_color)
            for tl in ax1.get_yticklabels():
                tl.set_color(TP_color)
            for n in range(len(bestfits_tp[0,:])):
                ax1.plot(bestfits_uA[:,n], bestfits_tp[:, n], color="black", linewidth=2)
            n = len(bestfits_tp[0,:])-1
            shot_line_uA = []
            shot_line_tp = []
            
            print 
            dark_current = intercepts[n]/slopes[n]
            #shot_line_uA.append(-1*dark_current)
            shot_line_uA.append(bestfits_uA[0,n])
            shot_line_uA.append(bestfits_uA[1,n])
            
            #shot_line_tp.append(0)
            shot_line_tp.append(bestfits_tp[0,n])
            shot_line_tp.append(bestfits_tp[1,n])
            
            ax1.plot(shot_line_uA,shot_line_tp, color=shot_color, linewidth=3)
            #ax1.plot([-1*dark_current, -1*dark_current],[0,max(tp_unpumpedhot)], color='firebrick', linewidth = 3)
            plt.text(30, 0.068, "L$\cdot$$T_{IF} = 51$K", fontsize=16, color=shot_color)
            plt.text(30, 0.06, "with $T_{IF}$ $=$ $10$K, L$ = 7$dB", fontsize=16, color=shot_color)
            
            B = 60.0e6 # MHz
            e = 1.60217657e-19 # Columbs (electron charge)
            I = dark_current*1.0e-6
            P = 2.0*e*I*B
            fP = P*1.0e15
            #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.7, str('%2.2f' % fP) + " $fW = 2eI_0$$B = P_0$", fontsize=16, color="firebrick")
            
            kb = 1.3806488e-23
            T = (2.0*e*I)/(kb)
            mT = T*1.0e3
            #print T
            
            
            #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.6, str('%2.2f' % T) + " $K = T_0$", fontsize=16, color="firebrick")
            
            #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.5, str(slopes[n]) + " = slope, " + str(intercepts[n]) +" = Y(0)", fontsize=16, color="firebrick")
            ax2 = ax1.twinx()
            ax2.plot(uA_unpumpedhot, mV_unpumpedhot, color=IV_color, linewidth=5)   
            ax2.set_ylabel('Voltage ($mV$)', color=IV_color)
            for tl in ax2.get_yticklabels():
                tl.set_color(IV_color)
            
            plt.savefig("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/shotplots/" + Ynum + ".eps")
            plt.close('all')
            
            
            
        ### get the astronomy quality sweep data for this Y sweep
        sweepdir = hotdir + 'sweep/'
        TP_list = glob.glob(sweepdir + "TP*.csv")
        if not TP_list == []:
            astrosweephot_found = True
            hot_sweep_pot       = []
            hot_sweep_meas_num  = []
            hot_sweep_mV_mean   = []
            hot_sweep_mV_std    = []
            hot_sweep_uA_mean   = []
            hot_sweep_uA_std    = []
            hot_sweep_TP_mean   = []
            hot_sweep_TP_std    = []
            hot_sweep_TP_num    = []
            hot_sweep_TP_freq   = []
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
            # put the data into a matrix for processing
            hot_matrix  = numpy.zeros((len(hot_sweep_mV_mean), 11))
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
            # process the matrix
            hot_matrix, hot_raw_matrix, hot_mono_matrix, hot_regrid_matrix, hot_conv_matrix = ProcessMatrix(hot_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
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
            ### save the results of this calulations
            n = open(prodatadir + 'hotdata.csv', 'w')
            n.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,TP_num,TP_freq,time_mean,pot,meas_num\n')
            for sweep_index in range(len(hot_sweep_mV_mean)):
                n.write(str(hot_sweep_mV_mean[sweep_index]) + ',' + str(hot_sweep_mV_std[sweep_index]) + ',' + str(hot_sweep_uA_mean[sweep_index]) + ',' + str(hot_sweep_uA_std[sweep_index]) + ',' + str(hot_sweep_TP_mean[sweep_index]) + ',' + str(hot_sweep_TP_std[sweep_index]) + ',' + str(hot_sweep_TP_num[sweep_index]) + ',' + str(hot_sweep_TP_freq[sweep_index]) + ',' + str(hot_sweep_time_mean[sweep_index]) + ',' + str(hot_sweep_pot[sweep_index]) + ',' + str(hot_sweep_meas_num[sweep_index]) +'\n')
            n.close()
            
        ####################################
        #### Start Cold data Processing ####
        ####################################
        colddir = Ydatadir + 'cold/'
        ###### Processing Params file ######
        coldparamsfile = colddir + 'params.csv'
        if os.path.isfile(coldparamsfile):
            coldparams_found  = True
            # load the params file for the cold data
            cold_K_val, cold_magisweep, cold_magiset, cold_magpot, cold_sisisweep, cold_sisiset, cold_UCA_volt, cold_LOfreq, cold_IFband = getparams(coldparamsfile)
        
        ###### Processing Standard SIS bias measurments ######
        coldstandSISdatafile = colddir + 'sisdata.csv'
        if os.path.isfile(coldstandSISdatafile):
            coldstandSISdata_found  = True
            # load the standard SIS bias measurments for the cold data
            cold_standSISdata_mV, cold_standSISdata_uA, cold_standSISdata_tp, cold_standSISdata_pot, cold_standSISdata_time = getSISdata(coldstandSISdatafile)
        
        ###### Processing Standard eletromagnet measurments ######
        coldstandmagdatafile = colddir + 'magdata.csv'
        if os.path.isfile(coldstandmagdatafile):
            coldstandmagdata_found  = True
            # load the standard electromagnet measurments for the cold data
            cold_standmagdata_V, cold_standmagdata_mA, cold_standmagdata_pot = getmagdata(coldstandmagdatafile)
        
        ### cold processed parameter file (uses at most 'params.csv', 'sisdata.csv', 'magdata.csv')
        proparamsfile = prodatadir + 'procoldparams.csv'
        # record the parameters of every sweep
        n = open(proparamsfile, 'w')
        if coldparams_found:
            n.write('param, value\n')
            n.write('temp,' + str(cold_K_val) + '\n')
            if cold_magisweep == True:
                n.write('magisweep,True\n')
                n.write('magiset,' +  str(cold_magiset) + '\n')
                n.write('magpot,'  +  str(numpy.round(cold_magpot))       + '\n')
            else:
                n.write('magisweep,False\n')
                n.write('magpot,' +  str(cold_magpot) + '\n')
        if coldstandmagdata_found:
            n.write('meanmag_V,'  + str(numpy.mean(cold_standmagdata_V))  + '\n')
            n.write('stdmag_V,'   + str(numpy.std(cold_standmagdata_V))   + '\n')
            n.write('meanmag_mA,' + str(numpy.mean(cold_standmagdata_mA)) + '\n')
            n.write('stdmag_mA,'  + str(numpy.std(cold_standmagdata_mA))  + '\n')
        if coldparams_found:
            if cold_sisisweep == True:
                n.write('sisisweep,True\n')
                n.write('sisiset,'  + str(cold_sisiset)    + '\n')
                n.write('UCA_volt,' + str(cold_UCA_volt)   + '\n')
            else:
                n.write('sisisweep,False\n')
                n.write('UCA_volt,' + str(cold_UCA_volt) + '\n')
        if coldstandSISdata_found:
            n.write('meanSIS_mV,' + str(numpy.mean(cold_standSISdata_mV)) + '\n')
            n.write('stdSIS_mV,'  + str(numpy.std(cold_standSISdata_mV))  + '\n')
            n.write('meanSIS_uA,' + str(numpy.mean(cold_standSISdata_uA)) + '\n')
            n.write('stdSIS_uA,'  + str(numpy.std(cold_standSISdata_uA))  + '\n')
            n.write('meanSIS_tp,' + str(numpy.mean(cold_standSISdata_tp)) + '\n')
            n.write('stdSIS_tp,'  + str(numpy.std(cold_standSISdata_tp))  + '\n')
            n.write('SIS_pot,'    + str(cold_standSISdata_pot[0])         + '\n')
            n.write('del_time,'   + str(numpy.max(cold_standSISdata_time) - numpy.min(cold_standSISdata_time))  + '\n')
        if coldparams_found:
            n.write('LOfreq,' + str(cold_LOfreq) + '\n')
            n.write('IFband,' + str(cold_IFband) + '\n')
        n.close()
        
        
        ###### Processing fastIV data (data taken using the bais computer's sweep command)
        coldfastIV_filename = colddir + 'fastsweep.csv'
        if os.path.isfile(coldfastIV_filename):
            fastIVcold_found = True
            # load the fast IV data
            mV_fastIVcold, uA_fastIVcold, tp_fastIVcold, pot_fastIVcold = get_fastIV(coldfastIV_filename)
            # put the data into a matrix for processing    
            fastcold_matrix = numpy.zeros((len(mV_fastIVcold), 4))
            fastcold_matrix[:,0] = mV_fastIVcold
            fastcold_matrix[:,1] = uA_fastIVcold
            fastcold_matrix[:,2] = tp_fastIVcold
            fastcold_matrix[:,3] = pot_fastIVcold
            # process the matrix
            fastcold_matrix, fastcold_raw_matrix, fastcold_mono_matrix, fastcold_regrid_matrix, fastcold_conv_matrix = ProcessMatrix(fastcold_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
            # put the information back into 1-D arrays
            mV_fastcold  = fastcold_matrix[:,0]
            uA_fastcold  = fastcold_matrix[:,1]
            tp_fastcold  = fastcold_matrix[:,2]
            pot_fastcold = fastcold_matrix[:,3]
            # save fastIV cold processed data
            n = open(prodatadir + 'coldfastIV.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_fastcold)):
                writeline = str(mV_fastcold[mV_index]) + ',' + str(uA_fastcold[mV_index]) + ',' + str(tp_fastcold[mV_index]) + ',' + str(pot_fastcold[mV_index]) + '\n'
                n.write(writeline)
            n.close()
            
        ###### Processing unpumped IV data (data taken using the bais computer's sweep command)
        coldunpumped_filename = colddir + 'unpumpedsweep.csv'
        if os.path.isfile(coldunpumped_filename):
            unpumpedcold_found = True
            # load the fast IV data
            mV_unpumpedcold, uA_unpumpedcold, tp_unpumpedcold, pot_unpumpedcold = get_fastIV(coldunpumped_filename)
            # put the data into a matrix for processing
            unpumpedcold_matrix = numpy.zeros((len(mV_unpumpedcold), 4))
            unpumpedcold_matrix[:,0] = mV_unpumpedcold
            unpumpedcold_matrix[:,1] = uA_unpumpedcold
            unpumpedcold_matrix[:,2] = tp_unpumpedcold
            unpumpedcold_matrix[:,3] = pot_unpumpedcold
            # process the matrix
            unpumpedcold_matrix, unpumpedcold_raw_matrix, unpumpedcold_mono_matrix, unpumpedcold_regrid_matrix, unpumpedcold_conv_matrix = ProcessMatrix(unpumpedcold_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
            # put the information back into 1-D arrays
            mV_unpumpedcold  = unpumpedcold_matrix[:,0]
            uA_unpumpedcold  = unpumpedcold_matrix[:,1]
            tp_unpumpedcold  = unpumpedcold_matrix[:,2]
            pot_unpumpedcold = unpumpedcold_matrix[:,3]
            # save unpumped cold processed data
            n = open(prodatadir + 'coldunpumped.csv', 'w')
            n.write('mV,uA,tp,pot\n')
            for mV_index in range(len(mV_unpumpedcold)):
                writeline = str(mV_unpumpedcold[mV_index]) + ',' + str(uA_unpumpedcold[mV_index]) + ',' + str(tp_unpumpedcold[mV_index]) + ',' + str(pot_unpumpedcold[mV_index]) + '\n'
                n.write(writeline)
            n.close()
            
        ### get the astronomy quality sweep data for this Y sweep
        sweepdir = colddir + 'sweep/'
        TP_list = glob.glob(sweepdir + "TP*.csv")
        if not TP_list == []:
            astrosweepcold_found = True
            cold_sweep_pot       = []
            cold_sweep_meas_num  = []
            cold_sweep_mV_mean   = []
            cold_sweep_mV_std    = []
            cold_sweep_uA_mean   = []
            cold_sweep_uA_std    = []
            cold_sweep_TP_mean   = []
            cold_sweep_TP_std    = []
            cold_sweep_TP_num    = []
            cold_sweep_TP_freq   = []
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
            # put the data into a matrix for processing
            cold_matrix  = numpy.zeros((len(cold_sweep_mV_mean), 11))
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
            # process the matrix
            cold_matrix, cold_raw_matrix, cold_mono_matrix, cold_regrid_matrix, cold_conv_matrix = ProcessMatrix(cold_matrix, mono_switcher, do_regrid, do_conv, regrid_mesh, min_cdf, sigma, verbose)
            # put the information back into 1-D arrays
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
            ### save the results of this calulations
            n = open(prodatadir + 'colddata.csv', 'w')
            n.write('mV_mean,mV_std,uA_mean,uA_std,TP_mean,TP_std,TP_num,TP_freq,time_mean,pot,meas_num\n')
            for sweep_index in range(len(cold_sweep_mV_mean)):
                n.write(str(cold_sweep_mV_mean[sweep_index]) + ',' + str(cold_sweep_mV_std[sweep_index]) + ',' + str(cold_sweep_uA_mean[sweep_index]) + ',' + str(cold_sweep_uA_std[sweep_index]) + ',' + str(cold_sweep_TP_mean[sweep_index]) + ',' + str(cold_sweep_TP_std[sweep_index]) + ',' + str(cold_sweep_TP_num[sweep_index]) + ',' + str(cold_sweep_TP_freq[sweep_index]) + ',' + str(cold_sweep_time_mean[sweep_index]) + ',' + str(cold_sweep_pot[sweep_index]) + ',' + str(cold_sweep_meas_num[sweep_index]) +'\n')
            n.close()
        
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

verbose=True # True or False

##### location of IV and TP parameter files, the data files
setnum  = 6
datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set'+str(setnum)+'/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set' + str(setnum) + '/'
#datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/initialize/'
#datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set2/'

search_4Ynums = True
search_str = 'Y'
Ynums=['Y0011'] # make a list array seporate array values with commas like Ynums = ['Y01', 'Y02']

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

YdataPro(verbose, datadir, search_4Ynums, search_str, Ynums, useOFFdata, Off_datadir, mono_switcher, do_regrid, regrid_mesh, do_conv, sigma, min_cdf)