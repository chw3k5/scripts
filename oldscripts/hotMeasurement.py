def hotMeasurement(doWide, doNarrow, N, datadir, LO, IFband, magpot, mA_mag, UCA_voltage, Ynum, Offnum, WideSweepStart, WideSweepStop, WideSweepStep, NarrowSweepStart, NarrowSweepStop, NarrowSweepStep):
    import sys
    from setfeedback import setfeedback
    from IVsweeps import IVsweeps
    ########## Start 300 K measuments
    ### Wide
    if doWide == True:
        # turn feedback off for the wide band measuement
        feedback=False
        status = setfeedback(feedback)
        if status == False:
            print "The function setfeedback failed, exiting this script"
            sys.exit()  
        sweepType = 'W'
        sweepTemp = '300K'
        fullname=datadir+'LO'+str('%3.f' % LO)+'_IFband'+str('%1.3f' % IFband)+'_magpot'+str('%06.f' % magpot)+str('%02.3f' % mA_mag)+'_UCA'+str('%1.3f' % UCA_voltage)+'_'+sweepType+sweepTemp+'_Y'+str('%03.f' % Ynum)+'_'+str('%04.f' % N)
        # do the sweep
        status, mV, uA, tp = IVsweeps(WideSweepStart, WideSweepStop, WideSweepStep, feedback, fullname)
        if status == False:
            print "The function IVsweeps failed, exiting this script"
            sys.exit()
    N = N + 1
    # end of wide band 300K measurement 
    ### Narrow
    if doNarrow == True:
        # turn feedback on for the narrow band measuement
        feedback=True
        status = setfeedback(feedback)
        if status == False:
            print "The function setfeedback failed, exiting this script"
            sys.exit()  
        sweepType = 'N'
        sweepTemp = '300K'
        fullname=datadir+'LO'+str('%3.f' % LO)+'_IFband'+str('%1.3f' % IFband)+'_magpot'+str('%06.f' % magpot)+str('%02.3f' % mA_mag)+'_UCA'+str('%1.3f' % UCA_voltage)+'_'+sweepType+sweepTemp+'_Y'+str('%03.f' % Ynum)+'_'+str('%04.f' % N)
        # do the sweep
        status, mV, uA, tp = IVsweeps(NarrowSweepStart, NarrowSweepStop, NarrowSweepStep, feedback, fullname)
        if status == False:
            print "The function IVsweeps failed, exiting this script"
            sys.exit()
        N = N + 1
    # end of narrow band 300K measurement
    return N