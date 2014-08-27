def formatRandS_ZVA24(filename):
    from numpy import genfromtxt
    
    #filename="/Users/chw3k5/Documents/Grad_School/Kappa/Sprarm/WBA25/Dec_12_13/data/test.csv"
    data = genfromtxt(filename,dtype=None, delimiter=',', skip_header=2)
    if str(data[0,0]) == 'freq[Hz]':
        #print "This file is edited past this point"
        #plfile = open("/Users/chw3k5/Documents/Grad_School/Kappa/Sprarm/WBA25/Dec_9_13/14K/data/test2.csv",'w')
        plfile = open(filename,'w')
        plfile.write("Hz, dB \n")
        for n in range(len(data[:,0])-1):
            plfile.write(data[n+1,0]+','+data[n+1,1]+'\n' )  
        plfile.close()
        print filename+' was formated'
        
        return True
      
    else: 
        print filename+' may already be formated'
        return False
        