def resfitter(x, y, lin_start, lin_end):
    # this reports the slopes and the data for the bestfit lines for linear regions
    import numpy
    big=-1
    bestfits_uA=numpy.zeros((2,len(lin_end)))
    bestfits_mV=numpy.zeros((2,len(lin_end)))
    slopes=numpy.zeros(len(lin_end))
    for ii in range(len(lin_end)):
        size=lin_end[0]-lin_start[0]
        if (size>big):
            big=size
        if lin_start[ii] != lin_end[ii]:
            slope,intercept = numpy.polyfit(x[lin_start[ii]+1:lin_end[ii]+1], y[lin_start[ii]+1:lin_end[ii]+1],1)
            bestfits_uA[0,ii] = slope*x[lin_start[ii]+1]+intercept
            bestfits_uA[1,ii] = slope*x[lin_end[ii]+1]+intercept
        
            bestfits_mV[0,ii] = x[lin_start[ii]+1]
            bestfits_mV[1,ii] = x[lin_end[ii]+1]        
            slopes[ii]=slope
    
    return slopes, bestfits_mV, bestfits_uA