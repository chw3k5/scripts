def regrid(data, mesh, verbose):
    #from matplotlib import *
    #from pylab import *
    import numpy
    # my regrid function likes data to be in one 2D-array with 
    # data[:,0] to be the data that is being made to have even spacing.
    # My regridding function requires that the data be monotonic when compared
    # to the regrid_mesh
    status=False
    if not verbose == 'N':
        print ' '
        print 'regridding data, mesh = ' +str(mesh) + 'mV'

    
    regrid_start=round(data[0,0]/mesh)*mesh
    regrid_end  =round(data[len(data[:,0])-1,0]/mesh)*mesh
    regrid_size=int(((regrid_end-regrid_start)/mesh)+1)
    
    regrid_data=numpy.zeros((regrid_size,len(data[0,:])))
    count=0
    n_last=len(regrid_data[:,0])-1
    for n in range(len(regrid_data[:,0])):
        regrid_data[n,0]=regrid_start+n*mesh
        if verbose == 'T':
            print 'n is ' + str(n)          
        if n == 0:
            if regrid_data[n,0] <= data[count,0]:
                regrid_data[n,1:] = data[count,1:]
                if verbose == 'T':
                    print 'n=0, case regrid point less than original data'
            else:
                finished=False
                summer=numpy.zeros(len(data[count,1:]))
                divisor=0                
                while not finished:
                    #bin_start = regrid_data[n,0]-mesh/2
                    bin_end   = regrid_data[n,0]+mesh/2
                    
                    if ((data[count,0] <= bin_end) and (count <= len(data[:,0])-2)):
                        summer=summer+data[count,1:]
                        divisor=divisor+1
                        count=count+1
                        if verbose == 'T':
                            print 'the count is ' + str(count)    
                    else:
                        if divisor <= 1:
                            if verbose == 'T':
                                print 'n=0, case interpolate'
                            
                            if data[count-1,0] >= regrid_data[n,0]:
                                inner_count=count-1
                            elif data[count,0] <= regrid_data[n,0]:
                                inner_count=count+1
                            else:
                                inner_count=count
                        
                            c1=abs(regrid_data[n,0]-data[inner_count-1,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                            c2=abs(data[inner_count,0]-regrid_data[n,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                            regrid_data[n,1:]=data[inner_count-1,1:]*c2+data[inner_count,1:]*c1
                            finished = True
                        else:
                            regrid_data[n,1:]=summer/divisor                            
                            finished = True
                            if verbose == 'T':
                                print 'n=0, case binning, points in bin = ' + str(divisor)
                        
        elif n==n_last: # for the last point
            if regrid_data[n,0] >= data[count,0]:
                regrid_data[n,1:]=data[count,1:]
                if verbose == 'T':
                    print 'n=n_last, case the last regrid point is greater than the last original data point'
            else:
                if verbose == 'T':
                    print 'n=n_last, case interpolate'               
                if data[count-1,0] >= regrid_data[n,0]:
                    inner_count=count-1
                elif data[count,0] <= regrid_data[n,0]:
                    inner_count=count+1
                else:
                    inner_count=count
                
                c1=abs(regrid_data[n,0]-data[inner_count-1,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                c2=abs(data[inner_count,0]-regrid_data[n,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                regrid_data[n,1:]=data[inner_count-1,1:]*c2+data[inner_count,1:]*c1
                finished = True            
        else: # for all the points that are not the first or the last points
            finished=False
            summer=numpy.zeros(len(data[count,1:]))
            divisor=0
            
            while not finished:
                #bin_start = regrid_data[n,0]-mesh/2
                bin_end   = regrid_data[n,0]+mesh/2
                
                if data[count,0] <= bin_end:
                    summer=summer+data[count,1:]
                    divisor=divisor+1
                    count=count+1
                    if verbose == 'T':
                        print 'the count is ' + str(count)
                else:
                    if divisor <= 1:
                        if verbose == 'T':
                            print 'case interpolate'
                        
                        if data[count-1,0] >= regrid_data[n,0]:
                            inner_count=count-1
                        elif data[count,0] <= regrid_data[n,0]:
                            inner_count=count+1
                        else:
                            inner_count=count
                        
                        c1=abs(regrid_data[n,0]-data[inner_count-1,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                        c2=abs(data[inner_count,0]-regrid_data[n,0])/abs(data[inner_count,0]-data[inner_count-1,0])
                        regrid_data[n,1:]=data[inner_count-1,1:]*c2+data[inner_count,1:]*c1                        
                        finished = True
                    else:
                        regrid_data[n,1:]=summer/divisor
                        finished = True
                        if verbose == 'T':
                            print 'case=binning, divisor = ' + str(divisor)
    status=True
    return regrid_data, status