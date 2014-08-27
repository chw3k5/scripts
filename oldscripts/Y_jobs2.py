def Y_jobs2(Y_csvfiles): # this is a lot of if statment to determine what job each file does
                        # improperly formated files cannot be detected ;( 
                        # below are examples of proberly formated files, hopefully.
                        # LO672_IFband1.42_magpot65100_UCA0.00_W300K_Y01_0150.csv
                        # LO672_IFband1.42_magpot65100_UCA0.00_WOff_Y01_0154.csv
                        # UCA3.55_077K_Y01_N_sweep0107.csv, LNA_off_300K_Y01_W_sweep0105.csv'
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
    
    status=False
    #print str(len(Y_csvfiles))+' is the number of CSV files in Y_jobs2'
    
    loop_ebrake=False
    
    if len(Y_csvfiles) == 0:
        flag        = False
        loop_ebrake = False 
    
    for n in range(len(Y_csvfiles)):
        string=Y_csvfiles[n]
        flag=False
        finished1=False
        position=0
        next_position=0
        loop_max=1000
        loop_count=0
        loop_ebrake=False
        while not finished1:
            loop_count=loop_count+1
            if loop_count >= loop_max:
                print 'An infinite loop was just stopped in Y_jobs'
                finished1=True
                loop_ebrake=True
                  
            next_position=string.find('/',position+1)
            if not next_position == -1:
                position=next_position
            else:
                finished1=True
        file_name=string[position+1:]
        end_position1=file_name.find('_', 0)
        string1=file_name[0:end_position1]
        
        end_position2=file_name.find('_', end_position1+1)
        string2=file_name[end_position1+1:end_position2]
        
        end_position3=file_name.find('_', end_position2+1)
        string3=file_name[end_position2+1:end_position3]
        
        end_position4=file_name.find('_', end_position3+1)
        string4=file_name[end_position3+1:end_position4]
        
        end_position5=file_name.find('_', end_position4+1)
        string5=file_name[end_position4+1:end_position5]
        
        end_position6=file_name.find('_', end_position5+1)
        string6=file_name[end_position5+1:end_position6]
        
        end_position7=file_name.find('_', end_position6+1)
        string7=file_name[end_position6+1:]
        
        #print "string 1 is " + str(string1)
        #print "string 2 is " + str(string2)
        #print "string 3[6:12] is " + str(string3[6:12])
        #print "string 4 is " + str(string4)
        #print "string 5 is " + str(string5)
        #print "string 6 is " + str(string6)
        #print "string 7 is " + str(string7)

        
        if string5[1:4] == 'Off':
            if string5[0:1] == 'W':
                wide_off_csv=Y_csvfiles[n]
            elif string5[0:1] == 'N':
                narrow_off_csv=Y_csvfiles[n]
            else:
                print file_name+" is not properly formated, N or W needs to be the fist letter in the 5th item seporated by _ (underscores)"
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
        elif ((string5[1:4] == '300') or (string5[1:4] == '077')):
            if not UCA_val:
                UCA_val=string4[3:]
            elif round(float(UCA_val)*1000) != round(float(string4[3:])*1000):
                print "It seems that are two diffent UCA values for the same Y number "+UCA_val+" and "+string4[3:]
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
            print "UCA_val = " + str(UCA_val)    
            if not LO_val:
                LO_val=string1[2:]
            elif round(float(LO_val)*1000) != round(float(string1[2:])*1000):
                print "It seems that are two diffent LO values for the same Y number "+LO_val+" and "+string1[2:]
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
            
            if not IFband_val:
                IFband_val=string2[6:]
            elif round(float(IFband_val)*1000) != round(float(string4[6:])*1000):
                print "It seems that are two diffent UCA values for the same Y number "+IFband_val+" and "+string4[6:]
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
                
            if not magpot_val:
                magpot_val=string3[6:12]
            elif round(float(magpot_val)*100000) != round(float(string3[6:12])*100000):
                print "It seems that are two diffent UCA values for the same Y number "+magpot_val+" and "+string3[6:]
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
            
            if string5[1:4] == '300':
                if string5[0:1] == 'W':
                    wide_hot_csv=Y_csvfiles[n]
                elif string5[0:1] == 'N':
                    narrow_hot_csv=Y_csvfiles[n]
                else:
                    print file_name+" is not properly formated, N or W needs to be the first letter in 5th item seporated by _ (underscores)"
                    print "this function Y_jobs, will now return status=False, this may exit a script"
                    flag=False
            elif string5[1:4] == '077':
                if string5[0:1] == 'W':
                    wide_cold_csv=Y_csvfiles[n]
                elif string5[0:1] == 'N':
                    narrow_cold_csv=Y_csvfiles[n]
                else:
                    print file_name+" is not properly formated, N or W needs to be the fistt letter of the 5th item seporated by _ (underscores)"
                    print "this function Y_jobs, will now return status=False, this may exit a script"
                    flag=False
            else:
                print file_name+" is not properly formated, str5[1:4] = 077 or 300 needs where str5 is the 5th string seporated by _ (underscores)"
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
        else:
            print file_name+" is not properly formated, in the 5th string str5[1,4] = 'Off' or '077' or '300' strings are seporated by _ (underscores)"
            print "this function Y_jobs, will now return status=False, this may exit a script"
            flag=False   
        
    if ((not loop_ebrake) and (not flag)):
        status = True
    
    return wide_off_csv, wide_hot_csv, wide_cold_csv, narrow_off_csv, narrow_hot_csv, narrow_cold_csv, LO_val, IFband_val, magpot_val, UCA_val, status
def ReadInSettings1(csvfile):
    # for the files created by the bias_sweep_only script.
    LO_val          = []
    IFband_val      = []
    magpot_val      = []
    mag_mA          = []
    UCA_val         = []
    
    string=csvfile
    flag=False
    finished1=False
    position=0
    next_position=0
    loop_max=1000
    loop_count=0
    loop_ebrake=False
    while not finished1:
        loop_count=loop_count+1
        if loop_count >= loop_max:
            print 'An infinite loop was just stopped in Y_jobs'
            finished1=True
            loop_ebrake=True
              
        next_position=string.find('/',position+1)
        if not next_position == -1:
            position=next_position
        else:
            finished1=True
    file_name=string[position+1:]
    end_position1=file_name.find('_', 0)
    string1=file_name[0:end_position1]
    
    end_position2=file_name.find('_', end_position1+1)
    string2=file_name[end_position1+1:end_position2]
    
    end_position3=file_name.find('_', end_position2+1)
    string3=file_name[end_position2+1:end_position3]
    
    end_position4=file_name.find('_', end_position3+1)
    string4=file_name[end_position3+1:end_position4]
    
    end_position5=file_name.find('_', end_position4+1)
    string5=file_name[end_position4+1:end_position5]
    
    end_position6=file_name.find('_', end_position5+1)
    string6=file_name[end_position5+1:end_position6]
    
    end_position7=file_name.find('_', end_position6+1)
    string7=file_name[end_position6+1:end_position7]
    
    end_position8=file_name.find('_', end_position7+1)
    string8=file_name[end_position7+1:end_position8]
    
    
    LO_val          = string1[2:]
    IFband_val      = string2[6:]
    magpot_val      = string3[6:]
    #mag_mA          = string4[3:len(string4)-2]
    UCA_val         = string4[3:]
    temp            = string5
    sweepNum        = string7[:len(string7)-3]
    
    if ((not loop_ebrake) and (not flag)):
        status = True
    
    return  LO_val, IFband_val, magpot_val, UCA_val, temp, sweepNum, status