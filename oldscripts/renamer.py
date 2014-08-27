def renamer(csvfiles):
    import sys
    import os
    import glob
    from GetFileNameData import GetFileNameData
    
    for n in range(len(csvfiles)):
        csvfile = csvfiles[n]       
#        print "the csvfile is "+csvfile
        
        ### Here we save the path information
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
        FileDir=csvfile[:position+1]
        
        # now I find the .csv file extention or any file extention
        finished = False
        position=0
        loop_count = 0
        loop_count_max = 100 # max number of folders (ie '/') to look for in a 
                            # single file before declaring this program to be 
                            # stuck in an infinite loop
        if csvfile.find('.',0) == -1:
            position = len(csvfile)
        else:
            while not finished:
                    loop_count=loop_count+1
                    if loop_count >= loop_count_max:
                        print "An infinite loop was just stopped in Y_jobs or the number of '.' in the csv filename was greater than " + str(loop_count_max)
                        finished=True                  
                    next_position=csvfile.find('.',position+1)
                    if not next_position == -1:
           	            position=next_position
                    else:
                        finished=True
        FileExtention=csvfile[position:]
        
        
        ### here we get all the information in the file header
        data_type, data_val = GetFileNameData(csvfile)
        #data_type       = [  0 ,   1     ,    2     ,    3   ,   4  ,    5      ,    6      ,   7   ,    8   ,   9   ]
        #data_type       = ['LO', 'IFband', 'magpot', 'mag_mA', 'UCA','sweeptype', 'loadtemp', 'Ynum','Offnum','other']
        
        ### this is the catch to make sure files have the right information before they are remaned
        if (data_val[0] != 'null' and data_val[0] != 'null' and data_val[1] != 'null' and data_val[2] != 'null' and data_val[3] != 'null' and data_val[4] != 'null' and data_val[5] != 'null' and data_val[6] != 'null'):
            if data_val[8] == 'null':
                NewFileName = data_val[len(data_type)-1] + '_' + 'Y'   + str('%04.0f' % float(data_val[7])) + '_' + data_type[0] + data_val[0]+ '_' + data_type[1] + data_val[1]+ '_' + data_type[2] + data_val[2] + data_val[3]+ '_' + data_type[4] + data_val[4]+ '_' + data_val[5] + data_val[6] + FileExtention
            else:
                NewFileName = data_val[len(data_type)-1] + '_' + 'OFF' + str('%02.0f' % float(data_val[8])) + '_' + data_type[0] + data_val[0]+ '_' + data_type[1] + data_val[1]+ '_' + data_type[2] + data_val[2] + data_val[3]+ '_' + data_type[4] + data_val[4]+ '_' + data_val[5] + data_val[6] + FileExtention   
            os.rename(csvfile, FileDir+NewFileName)
        else:
            print "the catch to the file names contain the correct inforamtion before they are renamed was tripped, killing the script."
            print "The file that caused this trip is:"
            print csvfile
            sys.exit()
    return