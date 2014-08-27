def derivative(data, deriv_int):
    import numpy
    # y'=df(mV)/dmV
    # y'=d(data[:,1:])/d(data[:,0])
    last_index = len(data[:,0])
    lenF       = len(data[0,1:])
    deriv      = numpy.zeros((last_index-deriv_int,len(data[0,:])))
    
    Fdata1     = data[:last_index-deriv_int,1:]
    Fdata2     = data[deriv_int:,1:]
    Xdata1     = data[:last_index-deriv_int,0]
    Xdata2     = data[deriv_int:,0]

    Fdiff      = Fdata2 - Fdata1
    Xdiff      = Xdata2 - Xdata1
    for n in range(lenF):
        deriv[:,n+1] = Fdiff[:,n]/Xdiff
    deriv[:,0] = (Xdata1+Xdata2)/2
    status = True
    return status, deriv