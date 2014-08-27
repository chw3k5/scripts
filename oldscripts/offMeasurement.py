def offMeasurement(doWide, doNarrow, N, datadir, LO_off, IFband_off, magpot_off, mA_mag, UCA_vOff, Offnum, WideSweepStart, WideSweepStop, WideSweepStep, NarrowSweepStart, NarrowSweepStop, NarrowSweepStep):
    import sys
    from setfeedback import setfeedback
    from IVsweeps import IVsweeps
    if doWide:
        # turn feedback off for the wide band measuement
        feedback=False
        status = setfeedback(feedback)
        if status == False:
            print "The function setfeedback failed, exiting this script"
            sys.exit()  
        sweepType = 'W'
        sweepTemp='Off'
        fullname=datadir+'LO'+str('%3.f' % LO_off)+'_IFband'+str('%1.3f' % IFband_off)+'_magpot'+str('%06.f' % magpot_off)+str('%02.3f' % mA_mag)+'_UCA'+str('%1.3f' % UCA_vOff)+'_'+sweepType+sweepTemp+'_OFF'+str('%03.f' % Offnum)+'_'+str('%04.f' % N)

        # do the sweep
        status, mV, uA, tp = IVsweeps(WideSweepStart, WideSweepStop, WideSweepStep, feedback, fullname)
        if status == False:
            print "The function IVsweeps failed, exiting this script"
            sys.exit()
        N = N + 1
        # end of wide band Off measurement 
        
    if doNarrow:
        # turn feedback on for the narrow band measuement
        feedback=True
        status = setfeedback(feedback)
        if status == False:
            print "The function setfeedback failed, exiting this script"
            sys.exit()  
        sweepType = 'N'
        sweepTemp = 'Off'
        fullname=datadir+'LO'+str('%3.f' % LO_off)+'_IFband'+str('%1.3f' % IFband_off)+'_magpot'+str('%06.f' % magpot_off)+str('%02.3f' % mA_mag)+'_UCA'+str('%1.3f' % UCA_vOff)+'_'+sweepType+sweepTemp+'_OFF'+str('%03.f' % Offnum)+'_'+str('%04.f' % N)

        # do the sweep
        status, mV, uA, tp = IVsweeps(NarrowSweepStart, NarrowSweepStop, NarrowSweepStep, feedback, fullname)
        if status == False:
            print "The function IVsweeps failed, exiting this script"
            sys.exit()
        N = N + 1
        # end of narrow band Off measurement
        return N