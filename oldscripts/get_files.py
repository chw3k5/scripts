def get_files(dir, search_str, load_params, verbose ):    # The program formats data from double space to 
    import glob
    import atpy
    
    myfiles = []
    if (load_params == True):
        # load the parameters file and read in the Device names and set parameters
        if not verbose == 'N':
            print 'loading parameters from file'       
        params=atpy.Table(dir+'params.csv', type="ascii", delimiter=",")
        for ii in range(len(params.name)):
            myfiles.append(dir+params.name[ii] + ".csv")
        if not verbose == 'N':
            print str(len(myfiles))+ " files found"
        status=True
        
    elif (load_params == False):
        # Find all of the files in the directory with a certin search string
        if not verbose == 'N':
            print 'searing for files in ' + str(dir)
        for files in glob.glob(dir+search_str):
            myfiles.append(files)
        if not verbose == 'N':
            print str(len(myfiles))+ " files found with search string: "+search_str
        status=True
        
    else:
        print "load_params was not set to True or False, returning status=False"
        status=False
    return (myfiles, status)