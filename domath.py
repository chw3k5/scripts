####################
###### regrid ######
####################

def regrid(data, mesh, verbose):
    import numpy
    # my regrid function likes data to be in one 2D-array with 
    # data[:,0] to be the data that is being made to have even spacing.
    # My regridding function requires that the data be monotonic when compared
    # to the regrid_mesh
    status=False
    if (verbose or verbose == 'T'):
        print 'regridding data, mesh = ' +str(mesh) + ' unit'

    
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


##################
###### conv ######
##################

def conv(data, mesh, min_cdf, sigma, verbose):
    import numpy as np
    import scipy.stats
    import math
    status = False
    if ((not verbose == 'Y') or (not verbose == 'T') or (verbose == True)):
        print 'Doing convolution of data cdf = ' + str(min_cdf) + '  sigma = ' +str(sigma)
    sigmaSteps=math.ceil(sigma/mesh) # unitless, rounded up to nearest integer
    # Normal Kernel Calculation
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

 
#######################
###### derivaive ######
#######################

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


########################
###### findlinear ######
########################

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
  

#######################
###### resfitter ######
#######################

def resfitter(x, y, lin_start, lin_end):
    # this reports the slopes and the data for the bestfit lines for linear regions
    import numpy
    big=-1
    Y=numpy.zeros((2,len(lin_end)))
    X=numpy.zeros((2,len(lin_end)))
    slopes=numpy.zeros(len(lin_end))
    intercepts = numpy.zeros(len(lin_end))
    for ii in range(len(lin_end)):
        size=lin_end[0]-lin_start[0]
        if (size>big):
            big=size
        if lin_start[ii] != lin_end[ii]:
            slope,intercept = numpy.polyfit(x[lin_start[ii]+1:lin_end[ii]+1], y[lin_start[ii]+1:lin_end[ii]+1],1)
            Y[0,ii] = slope*x[lin_start[ii]+1]+intercept
            Y[1,ii] = slope*x[lin_end[ii]+1]+intercept
        
            X[0,ii] = x[lin_start[ii]+1]
            X[1,ii] = x[lin_end[ii]+1]        
            slopes[ii]        = slope
            intercepts[ii]    = intercept
    
    return slopes, intercepts, X, Y
    
def linfit(X, Y, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, verbose):
    import numpy
    from profunc import do_derivative  
    matrix = numpy.zeros((len(X),2))
    matrix[:,0] = X
    matrix[:,1] = Y                
    regrid_mesh = abs(X[1]-X[0])
                                                                                 
    der1, der2 = do_derivative(matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose)
    #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
    #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
    
    status, lin_start, lin_end = findlinear(der2[:,0], der2[:,1], linif, verbose)
    slopes, intercepts, bestfits_X, bestfits_Y = resfitter(X, Y, lin_start, lin_end)
    
    return slopes, intercepts, bestfits_X, bestfits_Y
      
############################
###### Allan Variance ######
############################

def AllanVar(data, tau, verbose):
    import numpy
    data_len = len(data)
    T_max = int(numpy.floor(float(data_len)/(tau*4.0)))
    Variance = numpy.zeros(T_max)
    T_vector = numpy.arange(tau,T_max+1,tau)
    count = 0
    for T in T_vector:
        if verbose:
            print str(T) + ' of ' + str(T_max) + ' loops completed' 
        inner_loop_len = data_len - T + 1
        X_vector = numpy.zeros(inner_loop_len)
        for n in range(inner_loop_len):
            one_over_T = 1.0/T
            X_vector[n] = one_over_T * sum(data[n:n+T])
        X1_vector = X_vector[0:inner_loop_len-1]
        X2_vector = X_vector[1:inner_loop_len  ]
        #X1_mean = numpy.mean(X1_vector)
        #X2_mean = numpy.mean(X2_vector)
        #X1_var  = numpy.mean((X1_vector - X1_mean)**2)
        #X2_var  = numpy.mean((X2_vector - X2_mean)**2)

        #TOP = numpy.mean((X1_vector - X1_mean)*(X2_vector - X2_mean))
        #BOT = numpy.sqrt(X1_var*X2_var)
        #G = TOP/BOT
        
        #Variance[T-1] = (X1_var + X2_var)/2 - numpy.sqrt(X1_var*X2_var)*G
        
        diff_vector     = X1_vector-X2_vector
        diff_mean       = numpy.mean(diff_vector)
        Variance[count] = numpy.mean((diff_vector - diff_mean)**2)/2
        
        count = count +1
        
    return Variance

###################################################
###### M sample Allan Variance (not working) ######
###################################################

def AllanVarM(data, M, verbose):
    import numpy
    #from matplotlib import pyplot as plt   
    tau_max = int(numpy.round(float(len(data))/float(3)))
    
    
    MminusOne = M - 1
    #Variance = numpy.zeros((len(data), tau_max))
    Variance = numpy.zeros(tau_max)
    for Tee in range(tau_max):
        tau = Tee + 1
        sum1 = 0
        sum2 = 0
        mV_len = len(data)
        #for bigT in range(len(regrid_data[:,0])-1):
        Yit = data[0:mV_len-M*tau]
        for i in range(M):
            I = i*tau
            YitplusTau = data[tau+I:mV_len + I - tau]
            frac = (YitplusTau  - Yit)/tau
            sum1 = (frac)**2 + sum1            
            sum2 = frac + sum2
            
            if verbose:
                print str(tau) + "  is the tau value"
                print str(YitplusTau[0]) + " is the YitplusTau[0] value"
                print str(Yit[0]) + " is the Yit[0] value"
                print str(frac[0]) + " is the frac[0] value"
                print str(sum1[0]) + " is the sum1[0] value"
                print str(sum2[0]) + " is the sum2[0] value"
                print " "
            #Variance[:len(sum1),Tee] = (1/MminusOne)*(sum1 - (1/M)*(sum2**2))
            Variance[Tee] = numpy.mean((1/MminusOne)*(sum1 - (1/M)*(sum2**2)))
            
            #plt.clf()
            #plt.plot(numpy.mean(Variance,0))
            #plt.show()
            #plt.draw()
    return Variance


##########################
###### data2Yfactor ######
##########################
    
def data2Yfactor(hot_mV, cold_mV, off_tp, hot_tp, cold_tp, mesh, verbose):
    import numpy
    status=True
    # the first thing that we need to do is find the over lap in the mV range for off, hot and cold
    off=numpy.mean(off_tp)
    count_hot=0
    count_cold=0
    loop_count=0
    loop_count_max=len(hot_mV)+len(cold_mV)-1
    finished=False
    
    hot_test=hot_mV/mesh
    cold_test=cold_mV/mesh
    
    while not finished:
        if round(hot_test[count_hot])==round(cold_test[count_cold]):
            finished=True
        elif round(hot_test[count_hot])<round(cold_test[count_cold]):
            count_hot=count_hot+1
        else:
            count_cold=count_cold+1
        loop_count=loop_count+1
        if loop_count > loop_count_max:
            print "The loop has gone on long enough to exceed the length of both cold_mV and hot_mV, something is wrong maybe with the regridding. Status=False"
            status=False
            mV_Yfactor=0 
            Yfactor= 0
        if ((count_hot>=len(hot_mV)-1) or (count_cold>=len(cold_mV)-1)):
            finished=True
            print "It seems the mV values of cold and hot do not overlap, ruturning status=False"
            status=False
            mV_Yfactor=0 
            Yfactor= 0
            
    if status:
        len_mV=min(len(hot_mV[count_hot:]),len(cold_mV[count_cold:]))
        mV_Yfactor = numpy.zeros((len_mV))
        Yfactor    = numpy.zeros((len_mV))
    	
        for x in range(min(len(hot_mV[count_hot:]),len(cold_mV[count_cold:]))):
            mV_Yfactor[x]=hot_mV[count_hot+x]
            Yfactor[x]=((hot_tp[x]-off)/(cold_tp[x]-off))
        # this feature is now found in the function Ydatastats
        #max_Yfactor=-1
        #mV_max_Yfactor=-999999
        #min_Yfactor=999999
        #mV_min_Yfactor=-999999
        #count=0
        #summer=0
        #for x in range(len(Yfactor)):
        #    if ((mV_Yfactor[x] >= start_Yrange) and (mV_Yfactor[x] <= end_Yrange)):
        #        count=count+1
        #        summer=summer+Yfactor[x]
        #        if max_Yfactor < Yfactor[x]:
        #            max_Yfactor = Yfactor[x]
        #            mV_max_Yfactor = mV_Yfactor[x]
        #       if min_Yfactor > Yfactor[x]:
        #            min_Yfactor = Yfactor[x]
        #            mV_min_Yfactor = mV_Yfactor[x]
        #mean_Yfactor=summer/count
        #if ((mV_max_Yfactor==-999999) or (max_Yfactor==-1)):
        #    status=False
        #    print "The was a problem finding the mV of the max Yfactor"
        #if ((mV_min_Yfactor==-999999) or (min_Yfactor==999999)):
        #    status=False
        #    print "The was a problem finding the mV of the min Yfactor"

    return mV_Yfactor, Yfactor, status


#########################
###### Ydata_stats ######
#########################
    
def Ydata_stats(mV_Yfactor, Yfactor, start_Yrange, end_Yrange):
    status = True
    max_Yfactor=-1
    mV_max_Yfactor=-999999
    min_Yfactor=999999
    mV_min_Yfactor=-999999
    count=0
    summer=0
    for x in range(len(Yfactor)):
        if ((mV_Yfactor[x] >= start_Yrange) and (mV_Yfactor[x] <= end_Yrange)):
            count=count+1
            summer=summer+Yfactor[x]
            if max_Yfactor < Yfactor[x]:
                max_Yfactor = Yfactor[x]
                mV_max_Yfactor = mV_Yfactor[x]
            if min_Yfactor > Yfactor[x]:
                min_Yfactor = Yfactor[x]
                mV_min_Yfactor = mV_Yfactor[x]
    mean_Yfactor=summer/count
    if ((mV_max_Yfactor==-999999) or (max_Yfactor==-1)):
        status=False
        print "The was a problem finding the mV of the max Yfactor"
    if ((mV_min_Yfactor==-999999) or (min_Yfactor==999999)):
        status=False
        print "The was a problem finding the mV of the min Yfactor"
    return mV_max_Yfactor, max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, status 