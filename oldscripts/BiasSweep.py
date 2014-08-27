def biasSweep(sweeptype):

    import time
    import numpy
    import sys
    import os

    # Import this is the directory that has my scripts
    func_dir='/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)

    from control import LabJackU3_DAQ0, LJ_streamTP, measmag, setmagI, setmag_only, setfeedback
    from control import measSIS, setSIS_only, setSIS_Volt, setLOI, setSIS_TP, measSIS_TP, zeropots
    from StepperControl import initialize, GoForth, DisableDrive
    from email_sender   import email_caleb
    from fastSISsweep   import fastSISsweep
    if sweeptype == 'initialize':
        from BiasSweep_config_initialize import do_fastsweep,do_unpumpedsweep, fastsweep_feedback, SweepStart_feedTrue, SweepStop_feedTrue, SweepStep_feedTrue, SweepStart_feedFalse, SweepStop_feedFalse, SweepStep_feedFalse
        from BiasSweep_config_initialize import sweepShape, do_sisVsweep, do_sisisweep, do_magisweep, sisvsweep_min, sisvsweep_max, sisvsweep_step, sisi_magpot
        from BiasSweep_config_initialize import K_array, LOfreq_array, IFband_array, makeparamslist_Rec, Ynum
        from BiasSweep_config_initialize import high_res_min, high_res_max, high_res_meas, datadir, sweepNstart, feedback, verbose, verboseTop, careful
        from BiasSweep_config_initialize import UCA_set_pot, UCA_meas_after_set, sisi_cheat_num, mag_meas_after_set
        from BiasSweep_config_initialize import FinishedEmail, FiveMinEmail, PeriodicEmail, seconds_per_email, TPSampleFrequency, TPSampleTime
    elif sweeptype == 'standard':
        #from GetFileNameData import GetFileNameData
        from BiasSweep_config import do_fastsweep,do_unpumpedsweep, fastsweep_feedback, SweepStart_feedTrue, SweepStop_feedTrue, SweepStep_feedTrue, SweepStart_feedFalse, SweepStop_feedFalse, SweepStep_feedFalse
        from BiasSweep_config import sweepShape, do_sisVsweep, do_sisisweep, do_magisweep, sisvsweep_min, sisvsweep_max, sisvsweep_step, sisi_magpot
        from BiasSweep_config import K_array, LOfreq_array, IFband_array, makeparamslist_Rec, Ynum
        from BiasSweep_config import high_res_min, high_res_max, high_res_meas, datadir, sweepNstart, feedback, verbose, verboseTop, careful
        from BiasSweep_config import UCA_set_pot, UCA_meas_after_set, sisi_cheat_num, mag_meas_after_set
        from BiasSweep_config import FinishedEmail, FiveMinEmail, PeriodicEmail, seconds_per_email, TPSampleFrequency, TPSampleTime
    else:
        print "Sweeptype is not set properly in BiasSweep.py, last time this message was updated the option were:"
        print "'standard' which reads from the 'BiasSweep_config.py' file"
        print "'initialize' which reads from the 'BiasSweep_config_initialize.py' file"
        print "exiting script"
        sys.exit()

    ###### START SCRIPT ######
    # does the datadir exist? If not, we will make it!
    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    if not os.path.isdir(datadir+'rawdata/'):
        os.makedirs(datadir+'rawdata/')
    LOrefdir = datadir + "rawdata/LOpowerSettings/"
    if not os.path.isdir(LOrefdir):
        os.makedirs(LOrefdir)
    
    # huge wrapper file(s) to make the parameter lists for the run 
    if sweepShape == "rectangular":
        Emag_list, LOpow_list, K_list, LOfreq_list, IFband_list = makeparamslist_Rec(K_array, LOfreq_array, IFband_array)
    
    list_len = len(Emag_list)
    
    # Voltage sweeping
    if do_sisVsweep:
        sisv_list   = list(numpy.arange(sisvsweep_min, sisvsweep_max,sisvsweep_step))
        sispot_list = []
    else:
        if feedback:
            SweepStart    = SweepStart_feedTrue
            SweepStop     = SweepStop_feedTrue
            SweepStep     = SweepStep_feedTrue
        elif not feedback:
            SweepStart    = SweepStart_feedFalse
            SweepStop     = SweepStop_feedFalse
            SweepStep     = SweepStep_feedFalse
        else:
            print "feedback not set to True or False"
            sys.exit()
        sispot_list = list(numpy.arange(SweepStart, SweepStop, SweepStep))
        sisv_list   = []
    
    
    # if 300 K and 77 K measurments are being made, give files a Y number to make them easy to find as pairs
    if ( (min(K_list) < 90) and (250 < max(K_list)) ):
        do_Ynum = True
        initialize() # To start the chopper
        Y_trigger = K_list[0]
        
    else:
        do_Ynum = False
    
    
    ####### START CONTROL SEQUENCE #######
    # feedback is turned on of off here
    status = setfeedback(feedback)
    if status == False:
        print "The function setfeedback failed, exiting this script"
        sys.exit()
        
    magpot_last = -999999
    mag_last    = -999999
    UCA_last    = -999999
    sisi_last   = -999999
    LOfreq_last = -999999
    IFband_last = -999999
    K_last      = -999999
    first_loopi = True
    Ynum_str   = ''
    EmailTrigger = False
    sweepN = sweepNstart
    for i in range(list_len):
        sweepN = sweepN + 1
        
        # Move the chopper K_list (if needed)
        K_current = K_list[i]
        if not K_current == K_last:
            if do_Ynum:
                GoForth()
            K_last = K_current
        
        # Set the LO frequency (if needed)
        LOfreq_current = LOfreq_list[i]
        if not LOfreq_current == LOfreq_last:
            LOfreq_last = LOfreq_current
            
        # Set the LO attentuation (if needed)      
        if do_sisisweep:
            sisi_current = LOpow_list[i]
            if not sisi_current == sisi_last:
                if (verbose or verboseTop):
                    print "Setting SIS current: " + str(sisi_current) + " uA"
                uA_user = sisi_current
                setmag_only(sisi_magpot)
                #mV_sis, uA_sis, sisi_cheat_num  = setSIS_Volt(UCA_set_voltage, verbose, careful, sisi_cheat_num)
                setSIS_only(UCA_set_pot, feedback, verbose, careful)
                mV_sis, uA_sis, pot_sis, UCA_val = setLOI(uA_user, verbose, careful)
                mV_sis, uA_sis, pot_sis = measSIS(verbose)
                reset_val = pot_sis
                sisi_last = sisi_current
                UCA_voltage = UCA_val
                # Get acurrate SIS current and voltage meaurment for every sweep
    
                n = open(LOrefdir + str(sisi_current) + "uA.csv", 'w')
                n.write('mV, uA, tp, pot_sis, sisi_magpot, time \n')
                for k in range(UCA_meas_after_set):
                    mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(pot_sis, feedback, verbose, careful)
                    n.write(str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) +  ',' + str(pot_sis) + ','+ str(sisi_magpot) + ',' + str(time_stamp) + '\n')
                n.close()
        else:
            UCA_current = LOpow_list[i]
            if not UCA_current == UCA_last:
                if (verbose or verboseTop):
                    print "Setting UCA voltage: " + str(UCA_current) + " V"
                UCA_voltage = UCA_current
                #mV_sis, uA_sis, sisi_cheat_num  = setSIS_Volt(UCA_set_voltage, verbose, careful, sisi_cheat_num)
                setSIS_only(UCA_set_pot, feedback, verbose, careful)
                reset_val = sisi_cheat_num
                status = LabJackU3_DAQ0(UCA_voltage)
                UCA_last = UCA_current
                mV_sis, uA_sis, pot_sis = measSIS(verbose)
                
        # Set magnet (if needed)
        if do_magisweep:
            mag_current = Emag_list[i]
            if not mag_current == mag_last:
                if (verbose or verboseTop):
                    print "Setting magnet current: " + str(mag_current) + " mA"
                mA_user     = mag_current
                if (first_loopi):
                    set = {}
                    map(set.__setitem__, Emag_list, [])
                    UniqueEmag_list = set.keys()
                    magpots = numpy.zeros(len(UniqueEmag_list)) + 65100
                    for magpot_index in range(len(UniqueEmag_list)):
                        V_mag, mA_mag, pot_mag = setmagI(UniqueEmag_list[magpot_index], verbose, careful)
                        magpots[magpot_index] = pot_mag
                for magpot_index in range(len(UniqueEmag_list)):
                    if UniqueEmag_list[magpot_index] == mag_current:
                        magpot = magpots[magpot_index]
                        setmag_only(magpot)
                mag_last    = mag_current
        else:
            magpot_current = Emag_list[i]
            if not magpot_current == magpot_last:
                if (verbose or verboseTop):
                    print "Setting magnet potentiometer position: " + str(magpot_current)
                magpot = magpot_current
                setmag_only(magpot)
                magpot_last    = magpot_current  
            
        # Set IFband (if needed)
        IFband_current = IFband_list[i]
        if not IFband_current == IFband_last:
            #IFband_str = "IFband" + str(IFband_list[i])
            #IFband_str = "IFband" + str(IFband_list[i])
            IFband_last = IFband_current
                                                        
        # open and name the file where we will write data
        rawdir = datadir +"rawdata/"
        sweepN_str = str('%05.f' % sweepN)
        if do_Ynum:
            if Y_trigger == K_list[i]:
                Ynum     = Ynum + 1
                Ynum_str = 'Y' + str('%04.f' % Ynum)
            filepath = rawdir + Ynum_str + '/'
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
            if 250 < K_list[i]:
                filepath = filepath + 'hot/'    
            else:
                filepath = filepath + 'cold/'
            if not os.path.isdir(filepath):
                os.makedirs(filepath) 
        else:
            filepath = rawdir + sweepN_str + '/' 
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
        
        params_filename  = filepath + "params.csv"
        magdata_filename = filepath + "magdata.csv"
        sisdata_filename = filepath + "sisdata.csv"
        SweepPath        = filepath + 'sweep/'
        
        sweep_str = ''
        # record the parameters of every sweep
        n = open(params_filename, 'w')
        n.write('param, value\n')
        n.write('temp,' + str(K_list[i]) + '\n')
        sweep_str = sweep_str + 'temp=' + str(K_list[i]) + ', '
        if do_magisweep:
            n.write('magisweep,True\n')
            n.write('magiset,' +  str(Emag_list[i]) + '\n')
            n.write('magpot,'  +  str(magpot)       + '\n')
            sweep_str = sweep_str + 'magisweep=True' + ', ' + 'magiset=' + str(Emag_list[i]) + ', ' + 'magpot='  +  str(magpot) + ', '
        else:
            n.write('magisweep,False\n')
            n.write('magpot,' +  str(Emag_list[i]) + '\n')
            sweep_str = sweep_str + 'magisweep=True' + ', ' + 'magpot=' + str(Emag_list[i]) + ', '
        if do_sisisweep:
            n.write('sisisweep,True\n')
            n.write('sisiset,'  + str(LOpow_list[i]) + '\n')
            n.write('UCA_volt,' + str(UCA_voltage)   + '\n')
            sweep_str = sweep_str + 'sisisweep=True' + ', ' + 'sisiset='  + str(LOpow_list[i]) + ', ' + 'UCA_volt=' + str(UCA_voltage) + ', ' 
        else:
            n.write('sisisweep,False\n')
            n.write('UCA_volt,' + str(LOpow_list[i]) + '\n')
            sweep_str = sweep_str + 'sisisweep=True' + ', ' + 'UCA_Volt='  + str(LOpow_list[i]) + ', '
        n.write('LOfreq,' + str(LOfreq_list[i]) + '\n')
        sweep_str = sweep_str + 'LOfreq=' + str(LOfreq_list[i]) + ', '
        n.write('IFband,' + str(IFband_list[i]) + '\n')
        sweep_str = sweep_str + 'IFband=' + str(IFband_list[i])
        n.close()
        
        
        # Get acurrate  magnet current and voltage meaurment for every sweep  
        n = open(magdata_filename, 'w')
        n.write('V, mA, pot \n')
        for k in range(mag_meas_after_set):
            V_mag, mA_mag, pot_mag = measmag(verbose)
            n.write(str(V_mag) + ',' + str(mA_mag) + ',' + str(pot_mag) +  '\n')
        n.close()
        
        # Get acurrate SIS current and voltage meaurment for every sweep
        n = open(sisdata_filename, 'w')
        n.write('mV, uA, tp, pot, time \n')
        for k in range(UCA_meas_after_set):
            mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(pot_sis, feedback, verbose, careful)
            n.write(str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) +  ',' + str(pot_sis) + ',' + str(time_stamp) + '\n')
        n.close()
            
        # Things should be set now, lets start doing some kind of mearsurment
        if (do_sisVsweep):
            # Try to find the pot positions, using algorithims, for each Voltage in sisv_list
            if (first_loopi):
                if (verbose or verboseTop):
                    print "doing one time sis V searching to determine the SIS pot value"
                sisv_cheat_num = 65100
                sisvsweep_pot = []
                for k in range(len(sisv_list)):
                    if (verbose or verboseTop):
                        print "sis V searcher, search " + str(k+1) + ' of ' + str(len(sisv_list)) + ', V = ' + str(sisv_list[k]) + " mV"
                    mV_sis, uA_sis, pot_sis = setSIS_Volt(sisv_list[k], verbose, careful, sisv_cheat_num)
                    sisv_cheat_num = pot_sis
                    sisvsweep_pot.append(pot_sis)
                    sisvsweep_pot.sort
            
            # Do the Sweep for sisv_list
            if (verbose or verboseTop):
                print " "
                print "Doing sweep for: " + sweep_str
            for j in range(len(sisv_list)):
                step_num = str(1 + j)
                if not os.path.isdir(SweepPath):
                    os.makedirs(SweepPath)
                n = open(SweepPath + step_num + ".csv", 'w')
                n.write('mV, uA, tp, pot, time \n')
                time_sis = time.time()
                mV_sis, uA_sis, tp_sis, pot_sis = setSIS_TP(sisvsweep_pot[j], feedback, verbose, careful)
                # write date to file
                meas_line = str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) + ',' + str(pot_sis) + ',' + str(time_sis) +'\n'
                n.write(meas_line)
                if verbose:
                    print meas_line
                # Now that the pot is set we can do some addtional measuements
                if ((high_res_min <= sisv_list[j]) and (sisv_list[j] <= high_res_max)):
                    if verbose:
                        print " "
                        print "doing high resolution measument: " + str(high_res_meas) + " measurments"
                        print " "
                    for l in range(high_res_meas):
                        mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(sisvsweep_pot[j], feedback, verbose, careful)
                        meas_line = str(mV_sis) + ',' + str(uA_sis) + ',' + str(tp_sis) + ',' + str(pot_sis) + ',' + str(time_stamp) +'\n'
                        n.write(meas_line)
                        if verbose:
                            print meas_line
                            
                # Now we do the total power measurement with the LabJack
                LJ_streamTP(SweepPath + 'TP' + step_num + ".csv", TPSampleFrequency, TPSampleTime, verbose)
                n.close()
            setmag_only(reset_val)
            pot_sis = reset_val
        
        if do_fastsweep:
            status = setfeedback(fastsweep_feedback)
            if status == False:
                print "The function setfeedback failed, exiting this script"
                sys.exit()
            
            if fastsweep_feedback:
                SweepStart = SweepStart_feedTrue
                SweepStop  = SweepStop_feedTrue
                SweepStep  = SweepStep_feedTrue
            elif not fastsweep_feedback:
                SweepStart = SweepStart_feedFalse
                SweepStop  = SweepStop_feedFalse
                SweepStep  = SweepStep_feedFalse
            else:
                print "fastsweep_feedback is not set to 'True' or 'False', check BiasSweep_config.py and try again"
                print "killing the script"
                sys.exit()
            fastSISsweep(SweepStart, SweepStop, SweepStep, filepath + "fastsweep.csv", verbose)
            
            status = setfeedback(feedback)
            if status == False:
                print "The function setfeedback failed, exiting this script"
                sys.exit()
                
        if do_unpumpedsweep:
            status = setfeedback(fastsweep_feedback)
            if status == False:
                print "The function setfeedback failed, exiting this script"
                sys.exit()
            
            if fastsweep_feedback:
                SweepStart = SweepStart_feedTrue
                SweepStop  = SweepStop_feedTrue
                SweepStep  = SweepStep_feedTrue
            elif not fastsweep_feedback:
                SweepStart = SweepStart_feedFalse
                SweepStop  = SweepStop_feedFalse
                SweepStep  = SweepStep_feedFalse
            else:
                print "fastsweep_feedback is not set to 'True' or 'False', check BiasSweep_config.py search for do_unpumpedsweep and try again"
                print "killing the script"
                sys.exit()
            status = LabJackU3_DAQ0(5)
            fastSISsweep(SweepStart, SweepStop, SweepStep, filepath + "unpumpedsweep.csv", verbose)
            status = LabJackU3_DAQ0(UCA_voltage)
            status = setfeedback(feedback)
            if status == False:
                print "The function setfeedback failed, exiting this script"
                sys.exit()
        if first_loopi:
            StartTime = time.time()
            EmailTime = StartTime
            first_loopi = False
        else:
            NowTime       = time.time()
            ElapsedTime   = NowTime - StartTime
            RemainingTime = (ElapsedTime/(i))*(list_len-(i+1))
            
            if (verbose or verboseTop):
                r_hours = numpy.floor(RemainingTime/3600)
                r_secs  = numpy.mod(RemainingTime,3600)
                r_mins  = numpy.floor(RemainingTime/60)
                r_secs  = numpy.mod(RemainingTime,60)
                r_str   = str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time \n '
                print "estimated time remaining: " + r_str
    
            # Email Options
            if FiveMinEmail:
                if 5 <= numpy.floor(ElapsedTime/60):
                    EmailTrigger = True
                    FiveMinEmail = False
                    
            if PeriodicEmail:
                ElapsedEmailTime = NowTime - EmailTime
                if seconds_per_email < ElapsedEmailTime:
                    EmailTrigger = True
    
            if EmailTrigger:
                e_hours = numpy.floor(ElapsedTime/3600)
                e_secs  = numpy.mod(ElapsedTime,3600)
                e_mins  = numpy.floor(e_secs/60)
                e_secs  = numpy.mod(ElapsedTime,60)        
                e_str   = str('%02.f' % e_hours)+' hrs  '+str('%02.f' % e_mins)+' mins  '+str('%02.f' % e_secs)+' secs  is the elapsed time \n '
                
                r_hours = numpy.floor(RemainingTime/3600)
                r_secs  = numpy.mod(RemainingTime,3600)
                r_mins  = numpy.floor(r_secs/60)
                r_secs  = numpy.mod(RemainingTime,60)
                r_str   = str('%02.f' % r_hours)+' hrs  '+str('%02.f' % r_mins)+' mins  '+str('%02.f' % r_secs)+' secs  is the estimated remaining time \n '
                email_caleb('Bias Sweep Update', e_str + r_str)
                
                EmailTrigger = False
                EmailTime = NowTime
    
    # turn things off after a run
    DisableDrive()
    zeropots(verbose)
    if FinishedEmail:
        NowTime       = time.time()
        ElapsedTime   = NowTime - StartTime
        e_hours = numpy.floor(ElapsedTime/3600)
        e_secs  = numpy.mod(ElapsedTime,3600)
        e_mins  = numpy.floor(e_secs/60)
        e_secs  = numpy.mod(ElapsedTime,60)        
        e_str   = str('%02.f' % e_hours)+' hrs  '+str('%02.f' % e_mins)+' mins  '+str('%02.f' % e_secs)+' secs  is the elapsed time \n '
        email_caleb('Bias Sweep Finished', "The program BaisSweep.py has reached its end, congratulations! \n " + e_str)
    if (verbose or verboseTop):
        print " "
        print "The program BaisSweep.py has reached its end, congratulations!"
    return
    
sweeptype = 'initialize'
biasSweep(sweeptype)
        