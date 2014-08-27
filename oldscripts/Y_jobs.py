def Y_jobs(Y_csvfiles): # this is a lot of if statment to determine what job each file does
                        # improperly formated files cannot be detected ;( 
                        # below are examples of proberly formated files, hopefully.
                        # UCA3.55_077K_Y01_N_sweep0107.csv, LNA_off_300K_Y01_W_sweep0105.csv'
    wide_off_csv    = []
    wide_hot_csv    = []
    wide_cold_csv   = []
    narrow_off_csv  = []
    narrow_hot_csv  = []
    narrow_cold_csv = []
    UCA_val         = []
    status=False
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
        
        if string1[0:3] == 'LNA':
            if string5 == 'W':
                wide_off_csv=Y_csvfiles[n]
            elif string5 == 'N':
                narrow_off_csv=Y_csvfiles[n]
            else:
                print file_name+" is not properly formated, N or W needs to be the 5th item seporated by _ (underscores)"
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
        elif string1[0:3] == 'UCA':
            if not UCA_val:
                UCA_val=string1[3:]
            elif UCA_val != string1[3:]:
                print "It seems that are two diffent UCA values for the same Y number "+UCA_val+" and "+string1[3:]
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
            
            if string2 == '300K':
                if string4 == 'W':
                    wide_hot_csv=Y_csvfiles[n]
                elif string4 == 'N':
                    narrow_hot_csv=Y_csvfiles[n]
                else:
                    print file_name+" is not properly formated, N or W needs to be the 4th item seporated by _ (underscores)"
                    print "this function Y_jobs, will now return status=False, this may exit a script"
                    flag=False
            elif string2 == '077K':
                if string4 == 'W':
                    wide_cold_csv=Y_csvfiles[n]
                elif string4 == 'N':
                    narrow_cold_csv=Y_csvfiles[n]
                else:
                    print file_name+" is not properly formated, N or W needs to be the 4th item seporated by _ (underscores)"
                    print "this function Y_jobs, will now return status=False, this may exit a script"
                    flag=False
            else:
                print file_name+" is not properly formated, 077K or 300K needs to be the 2nd item seporated by _ (underscores)"
                print "this function Y_jobs, will now return status=False, this may exit a script"
                flag=False
        else:
            print file_name+" is not properly formated, LNA or UCA need to be the first three letters of items seporated by _ (underscores)"
            print "this function Y_jobs, will now return status=False, this may exit a script"
            flag=False   
        
    if ((not loop_ebrake) and (not flag)):
        status = True
    
    return wide_off_csv, wide_hot_csv, wide_cold_csv, narrow_off_csv, narrow_off_csv, narrow_hot_csv, narrow_cold_csv, UCA_val, status