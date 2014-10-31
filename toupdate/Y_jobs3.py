from oldscripts import GetFileNameData


def Y_jobs3(Y_csvfiles):
    # This program is expecting 3 to 6 CSV files

    status = True
    
    wide_off_csv    = []
    wide_hot_csv    = []
    wide_cold_csv   = []
    narrow_off_csv  = []
    narrow_hot_csv  = []
    narrow_cold_csv = []
    
    LO_val          = []
    IFband_val      = []
    magpot_val      = []
    UCA_val         = []
  
    for n in range(len(Y_csvfiles)):
        isOffdata = False
        csvfile = Y_csvfiles[n]
        data_type, data_val = GetFileNameData(csvfile)
        
        #data_type       = [  0 ,   1     ,    2     ,    3   ,   4  ,    5      ,    6      ,   7   ,    8   ,   9   ]
        #data_type       = ['LO', 'IFband', 'magpot', 'mag_mA', 'UCA','sweeptype', 'loadtemp', 'Ynum','Offnum','other']
        for u in range(len(data_type)):
            if data_type[u] == 'Offnum':
                if data_val[u] != 'null':
                    isOffdata  = True
                
        for m in range(len(data_type)):
            if data_type[m] == 'sweeptype':
                if data_val[m] == 'W':
                    for p in range(len(data_type)):
                        if data_type[p] == 'loadtemp':
                            if data_val[p] == '300K':
                                wide_hot_csv = csvfile
                            elif data_val[p] == '077K':
                                wide_cold_csv = csvfile
                            elif data_val[p] == 'Off':
                                wide_off_csv = csvfile
                            else:
                                print "It seems that the the loadtemp of this csv file was not 300K, 077K, or Off."
                                print "loadtemp value: "+str(data_val[p])
                                print "Returning status=False"
                                print "The csvfile is:"
                                print csvfile
                                status=False
                elif data_val[m] == 'N':
                    for p in range(len(data_type)):
                        if data_type[p] == 'loadtemp':
                            if data_val[p] == '300K':
                                narrow_hot_csv = csvfile
                            elif data_val[p] == '077K':
                                narrow_cold_csv = csvfile
                            elif data_val[p] == 'Off':
                                narrow_off_csv = csvfile
                            else:
                                print "It seems that the the loadtemp of this csv file was not 300K, 077K, or Off."
                                print "loadtemp value: "+str(data_val[p])
                                print "Returning status=False"
                                print "The csvfile is:"
                                print csvfile
                                status=False
                else:
                    print "It seems that the the sweeptype of this csv file was not N or W."
                    print "sweeptype value: "+str(data_val[p])
                    print "Returning status=False"
                    print "The csvfile is:"
                    print csvfile
                    status=False
            elif data_type[m] == 'LO':
                if not isOffdata:
                    if not LO_val:
                        LO_val = data_val[m]
                    else:
                        if not LO_val == data_val[m]:
                            print "It seems that are two diffent LO values for the same Y number "+LO_val+" and "+data_val[m]
                            print "this function, Y_jobs3, will now return status=False, this may exit a script"
                            status = False
            elif data_type[m] == 'IFband':
                if not isOffdata:
                    if not IFband_val:
                        IFband_val = data_val[m]
                    else:
                        if not IFband_val == data_val[m]:
                            print "It seems that are two diffent IFband values for the same Y number "+IFband_val+" and "+data_val[m]
                            print "this function, Y_jobs3, will now return status=False, this may exit a script"
                            print "The csvfile is:"
	                    print csvfile
                            status = False
            elif data_type[m] == 'magpot':
                if not isOffdata:
                    if not magpot_val:
                        magpot_val = data_val[m]
                    else:
                        if not magpot_val == data_val[m]:
                            print "It seems that are two diffent magpot values for the same Y number "+magpot_val+" and "+data_val[m]
                            print "this function, Y_jobs3, will now return status=False, this may exit a script"
                            print "The csvfile is:"
                            print csvfile
                	    status = False
            elif data_type[m] == 'UCA':
                if not isOffdata:
                    if not UCA_val:
                        UCA_val = data_val[m]
                    else:
                        if not UCA_val == data_val[m]:
                            print "It seems that are two diffent UCA values for the same Y number "+UCA_val+" and "+data_val[m]
                            print "this function, Y_jobs3, will now return status=False, this may exit a script"
                            print "The csvfile is:"
                            print csvfile
                            status = False
                            
    return wide_off_csv, wide_hot_csv, wide_cold_csv, narrow_off_csv, narrow_hot_csv, narrow_cold_csv, LO_val, IFband_val, magpot_val, UCA_val, status
