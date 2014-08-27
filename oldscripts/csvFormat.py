def csvFormat(dir, search_str, verbose ):    # The program formats data from double space to 
                                             # delimited comma delimited. Also it adds a header that 
                                             # is used as a column handle.

    import numpy as np
    import glob
    from numpy import genfromtxt
    from is_number import is_number

    csvfiles = []
    for files in glob.glob(dir+search_str):
        csvfiles.append(files)
    
    csvfiles_2edit = []
    for p in range(len(csvfiles)):
        data = genfromtxt(csvfiles[p], delimiter='  ')
        if str(data[0]) == 'nan':
            if not verbose == 'N': 
                print csvfiles[p]+' is already formated or atlest not double space delimited'
        elif is_number(data[0,0]):
            csvfiles_2edit.append(csvfiles[p])
            
        else:
            if not verbose == 'N': 
                print csvfiles[p]+' is not in an anticipated formated'
            
    for k in range(len(csvfiles_2edit)):
        
        data = genfromtxt(csvfiles_2edit[k], delimiter='  ')
        plfile = open(csvfiles_2edit[k],'w')
        plfile.write("mV, uA, tp, pot\n")
        
        for n in range(len(data[:,0])):
            plfile.write(str('%4.6f' % data[n,0])+','+str('%4.6f' % data[n,1])+','+str('%4.6f' % data[n,2])+','+str('%6.0f' % data[n,3])+'\n' )  
        plfile.close()
        if not verbose == 'N': 
            print csvfiles_2edit[k]+' was formated'
    if not verbose == 'N': 
        print 'end csvFormat.py'
        print ' '
    return True