def GetFileNameData(csvfile):
    # The function is expecting a single name of a csv file
    import sys
    import os.path
    
    ### Some brief error checking 
    if not csvfile:
        print "The csv file sent to GetFileNameData was empty, killing this script"
        sys.exit()
    if not os.path.isfile(csvfile):
        print "The csv file sent to GetFileNameData does not exist, make sure you have the full path name for that file, killing this script"
        sys.exit()
    
    
    ### Here we get rid of all the path information and just isolate the filename
    finished = False
    position=0
    loop_count = 0
    loop_count_max = 100 # max number of folders (ie '/') to look for in a 
                         # single file before declaring this program to be 
                         # stuck in an infinite loop
    while not finished:
            loop_count=loop_count+1
            if loop_count >= loop_count_max:
                print 'An infinite loop was just stopped in Y_jobs or the number of folders in the csv filename was greater than ' + str(loop_count_max)
                finished=True                  
            next_position=csvfile.find('/',position+1)
            if not next_position == -1:
                position=next_position
            else:
                finished=True
    Full_FileName=csvfile[position+1:]
    
    # now I get rid of the .csv file extention or any file extention
    finished = False
    position=0
    loop_count = 0
    loop_count_max = 100 # max number of folders (ie '/') to look for in a 
                         # single file before declaring this program to be 
                         # stuck in an infinite loop
    if Full_FileName.find('.',0) == -1:
        position = len(Full_FileName) - 1
    else:
        while not finished:
                loop_count=loop_count+1
                if loop_count >= loop_count_max:
                    print "An infinite loop was just stopped in Y_jobs or the number of '.' in the csv filename was greater than " + str(loop_count_max)
                    finished=True                  
                next_position=Full_FileName.find('.',position+1)
                if not next_position == -1:
    	            position=next_position
                else:
                    finished=True
    FileName=Full_FileName[:position + 1]
    
    ### Now we dice the FileName into its component strings seporated by an 
    #### underscore '_' and match them to the correct data type
    str_num         = FileName.count('_') + 1 # if there are now underscores than strnum=1
    start_position  = 0
    data_type       = ['LO', 'IFband', 'magpot', 'mag_mA', 'UCA','sweeptype', 'loadtemp', 'Ynum','Offnum','other']
    data_val        = ['null']*len(data_type)
    data_val[len(data_type)-1] = ''
    for n in range(str_num):
        end_position=FileName.find('_', start_position)
        string=FileName[start_position:end_position]
        start_position=end_position + 1
        if not string:
            None
        elif string[0:2]    == 'LO':
            data_val[0]   = string[2:]
        elif string[0:6]  == 'IFband':
            data_val[1]   = string[6:]
        elif string[0:6]  == 'magpot':
            data_val[2]   = string[6:12]
            data_val[3]   = string[12:]
        elif string[0:3]  == 'UCA':
            data_val[4]   = string[3:]
        elif (string[0]   == 'N' or string[0] == 'W'):
            data_val[5]   = string[0]
            data_val[6]   = string[1:]
        elif string[0]    == 'Y':
            data_val[7]   = string[1:]
        elif string[0:3]  == 'OFF':
            data_val[8]   = string[3:]
        else:
            data_val[len(data_type)-1] = data_val[len(data_type)-1]+string

    return data_type, data_val
