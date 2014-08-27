def conv(data, mesh, min_cdf, sigma, verbose):
    import numpy as np
    import scipy.stats
    import math
    status = False
    if ((not verbose == 'Y') or (not verbose == 'T') or (verbose == True)):
        print 'Doing convolution of data cdf = ' + str(min_cdf) + '  sigma = ' +str(sigma)
    sigmaSteps=math.ceil(sigma/mesh) # unitless, rounded up to nearest interger
    # Normal Kernal Caluation
    n=0
    finished=False
    mV_len=len(data[:,0])
    while not finished:
        n=n+1
        Xnorm=range(-n,n+1)
        norm=scipy.stats.norm(0, sigmaSteps).pdf(Xnorm)
        cdf=sum(norm)
        if cdf>=min_cdf:
            finished=True
    Xnorm=range(-n,n+1)
    norm=scipy.stats.norm(0, sigmaSteps).pdf(Xnorm)
    normMatrix=np.zeros((mV_len,mV_len+len(norm)-1),dtype=float)
    
    # matrix kernal for convolution
    for m in range(0,mV_len):
        tempVec=np.zeros((mV_len+len(norm)-1),dtype=float)
        tempVec[m:m+2*n+1]=norm
        normMatrix[m,]=tempVec
    normMatrix2=normMatrix[:,n:len(normMatrix[0,:])-n]
    # here is the point where the actual convolution takes place
    weight=np.sum(normMatrix2,axis=1)
    for p in range(len(data[0,:])-1):        
        data[:,p+1] = np.dot(data[:,p+1], normMatrix2)/weight
        status = True
    return data, status