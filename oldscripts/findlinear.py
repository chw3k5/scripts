def findlinear(x, ydprime, linif, verbose):
    import numpy
    status = True
    if len(x) == len(ydprime):
        status = True
    else:
        status =False
        print "In the function findlinear the dependent and independent variables do not have the same length, returning statuse false"
    linMask      = numpy.zeros(len(x))
    dataMax      = max(abs(ydprime))
    normal_data  = abs(ydprime/dataMax)
    numpy.putmask(linMask, normal_data < linif, 1)
    lin_start=[]
    lin_end=[]
    for n in range(len(x)):                        
        if n == 0:
            if (linMask[n]==1):
                lin_start.append(n)      
        else:
            if (linMask[n-1]==1 and linMask[n] == 0 ):
                lin_end.append(n-1)
            elif (linMask[n-1] == 0 and linMask[n] == 1):
                lin_start.append(n)
            elif (n == len(x)-1 and linMask[n] == 1):
                lin_end.append(n)                                        
    if verbose != 'N':
        print str(len(lin_end))+" linear regions were found:"
        print
    return status, lin_start, lin_end