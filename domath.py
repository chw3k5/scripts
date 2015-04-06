import numpy
import scipy.stats
import math
import sys

####################
###### regrid ######
####################
def regrid(data, mesh, verbose):
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
    status = False
    if ((not verbose == 'Y') or (not verbose == 'T') or (verbose == True)):
        print 'Doing convolution of data cdf = ' + str(min_cdf) + '  sigma = ' +str(sigma)
    sigmaSteps=math.ceil(sigma/mesh) # unitless, rounded up to nearest integer
    # Normal Kernel Calculation
    n=0
    finished=False
    try:
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
        normMatrix=numpy.zeros((mV_len,mV_len+len(norm)-1),dtype=float)

        # matrix kernal for convolution
        for m in range(0,mV_len):
            tempVec=numpy.zeros((mV_len+len(norm)-1),dtype=float)
            tempVec[m:m+2*n+1]=norm
            normMatrix[m,]=tempVec

        normMatrix2=normMatrix[:,n:len(normMatrix[0,:])-n]
        # here is the point where the actual convolution takes place
        weight=numpy.sum(normMatrix2,axis=1)
        for p in range(len(data[0,:])-1):
            data[:,p+1] = numpy.dot(data[:,p+1], normMatrix2)/weight
            status = True
    except IndexError:
        status = False
    except TypeError:
        status = False
    return data, status


#######################
###### derivaive ######
#######################
def derivative(data, deriv_int):
    # y'=df(mV)/dmV
    # y'=d(data[:,1:])/d(data[:,0])
    last_index = len(data[:,0])
    try:
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
    except IndexError:
        status = False
        deriv = None
        print 'deriv =', deriv
    return status, deriv


###########################
###### DoDerivatives ######
###########################
def DoDerivatives(matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma,
                  der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh,
                  verbose):
    status, der1 = derivative(matrix, der1_int)
    if der1 is not None:
        if do_der1_conv:
            der1, status  = conv(der1,  regrid_mesh, der1_min_cdf, der1_sigma, verbose)
        status, der2 = derivative(der1, der2_int)
        if do_der2_conv:
            der2, status  = conv(der2,  regrid_mesh, der2_min_cdf, der2_sigma, verbose)
    else:
        der2 = None
        print "der1 = ", der1
        print "der2 = ", der2
    return der1, der2


########################
###### findlinear ######
########################

def findlinear(x, ydprime, linif, verbose):
    status = True
    if len(x) == len(ydprime):
        status = True
    else:
        status =False
        print "In the function findlinear the dependent and independent variables do not have the same length,\n"+\
              " returning statuse false"
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
    if verbose:
        print str(len(lin_end))+" linear regions were found:"
    return status, lin_start, lin_end 
  

#######################
###### resfitter ######
#######################

def resfitter(x, y, lin_start, lin_end):
    # this reports the slopes and the data for the bestfit lines for linear regions
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
    
def linfit(X, Y, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma,
           der2_int, do_der2_conv, der2_min_cdf, der2_sigma,
           verbose):
    matrix = numpy.zeros((len(X),2))
    matrix[:,0] = X
    matrix[:,1] = Y
    try:
        regrid_mesh = abs(X[1]-X[0])
    except IndexError:
        regrid_mesh = 0.01
    der1, der2 = DoDerivatives(matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma,
                               der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh,
                               verbose)
    #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
    #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
    try:
       # print der1 != [], der1
        status, lin_start, lin_end = findlinear(der2[:,0], der2[:,1], linif, verbose)
        slopes, intercepts, bestfits_X, bestfits_Y = resfitter(X, Y, lin_start, lin_end)
    except TypeError:
         slopes     = None
         intercepts = None
         bestfits_X = None
         bestfits_Y = None
    
    return slopes, intercepts, bestfits_X, bestfits_Y
      
############################
###### Allan Variance ######
############################

def AllanVar(data, tau, verbose):
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
def allan_var(totpow, tau, tau_max=1000):
    sig_tau   = []
    tau       = int(tau)
    tau_max   = min(tau_max, int(float(len(totpow))/(2.1*tau)))
    for i in range(1,tau_max+1):
        M_x   = len(totpow)
        norm  = max(totpow)                      # normalization factor
        x_l   = totpow[0:M_x-2*i-1]/norm
        x_m   = totpow[i:M_x-i-1]/norm
        x_u   = totpow[2*i:M_x-1]/norm
        print i, len(x_l), len(x_m), len(x_u)
        coeff = 1.0/((2*(i*float(tau))**2)*(len(x_l)-2*i))
        y2    = (x_u - 2*x_m + x_l)^2
        total_y2   = sum(y2)
        sig_tau.append(coeff*total_y2)
    return sig_tau


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


#########################
###### FindOverlap ######
#########################
def FindOverlap(X, Y, mesh):
    X = list(X)
    Y = list(Y)
    status   = True
    finished = False
    count_X        = 0
    count_Y        = 0
    loop_count     = 0
    loop_count_max = len(X)+len(Y)-1

    X_test = [int(numpy.round(x/mesh)) for x in X]
    Y_test = [int(numpy.round(y/mesh)) for y in Y]


    while not finished:
        if X_test[count_X]==Y_test[count_Y]:
            finished=True
        elif X_test[count_X] < Y_test[count_Y]:
            count_X += 1
        else:
            count_Y += 1
        loop_count=loop_count+1
        if loop_count > loop_count_max:
            print "The loop has gone on long enough to exceed the length of both Y_mV and X_mV, \n"+\
                  "something could be wrong with the regridding. Status=False"
            status=False
        if ((count_X>=len(X)-1) or (count_Y>=len(Y)-1)):
            finished=True
            print "It seems the mV values of Y and X do not overlap, returning status=False"
            status=False
    if status:
        length  = min(len(X[count_X:]),len(Y[count_Y:]))
    else:
        length  = None

    return status, count_X, count_Y, length

##########################
###### data2Yfactor ######
##########################
def data2Yfactor(hot_mV, cold_mV, off_tp, hot_tp, cold_tp, mesh, verbose):
    status=True
    # the first thing that we need to do is find the over lap in the mV range for off, hot and cold
    off=numpy.mean(off_tp)
    hot_mV  = list(hot_mV)
    cold_mV = list(cold_mV)
    hot_tp  = list(hot_tp)
    cold_tp = list(cold_tp)

    Yfactor    = []
    if ((1 < len(hot_mV)) or (1 < len(cold_mV))):
        status, start_index_hot, start_index_cold, len_mV = FindOverlap(hot_mV, cold_mV, mesh)
        if status:
            mV_Yfactor = hot_mV[start_index_hot:start_index_hot+len_mV]
            # The Y-Factor calculation
            for x in range(len_mV):
                Yfactor.append((hot_tp[x]-off)/(cold_tp[x]-off))
        else:
            mV_Yfactor = None
            Yfactor    = None
            print "data2Yfactor failed"
    else:
        mV_Yfactor = [numpy.mean([numpy.mean(hot_mV),numpy.mean(cold_mV)])]
        len_mV = 1



    return mV_Yfactor, Yfactor, status


##############################
###### Specdata2Yfactor ######
##############################
def Specdata2Yfactor(prodatadir, verbose=False):
    hot_freqs_file  = prodatadir + "hotspecdata_freq.npy"
    hot_mVs_file    = prodatadir + "hotspecdata_mV.npy"
    hot_pwr_file    = prodatadir + "hotspecdata_pwr.npy"
    cold_freqs_file = prodatadir + "coldspecdata_freq.npy"
    cold_mVs_file   = prodatadir + "coldspecdata_mV.npy"
    cold_pwr_file   = prodatadir + "coldspecdata_pwr.npy"

    hot_freqs  = numpy.load(hot_freqs_file)
    hot_mVs    = numpy.load(hot_mVs_file)
    hot_pwr    = numpy.load(hot_pwr_file)
    cold_freqs = numpy.load(cold_freqs_file)
    cold_mVs   = numpy.load(cold_mVs_file)
    cold_pwr   = numpy.load(cold_pwr_file)

    if len(hot_freqs) < 2:
        hot_freqs  = numpy.array(hot_freqs[0])
        hot_mVs    = numpy.array(hot_mVs[0])
        hot_pwr    = numpy.array(hot_pwr[0])
        cold_freqs = numpy.array(cold_freqs[0])
        cold_mVs   = numpy.array(cold_mVs[0])
        cold_pwr   = numpy.array(cold_pwr[0])

        # Find the Overlap of the hot and cold Matrices in frequency
        freq_mesh      = abs(hot_freqs[1]  - hot_freqs[0])
        freq_mesh_test = abs(cold_freqs[1] - cold_freqs[0])
        if not ((freq_mesh - freq_mesh_test) < 0.0001):
            print "The freq mesh of the hot and cold spectral frequency surface do not match in the directory:"
            print prodatadir
            print freq_mesh, " is the hot freq mesh"
            print freq_mesh_test, " is the cold freq mesh"
            sys.exit()


        status, start_index_hot_freq, start_index_cold_freq, len_freq = FindOverlap(hot_freqs, cold_freqs, freq_mesh)
        if status:
            end_index_hot_freq  = start_index_hot_freq+len_freq
            end_index_cold_freq = start_index_cold_freq+len_freq
            hot_freqs  = hot_freqs[start_index_hot_freq:end_index_hot_freq]
            hot_mVs    = hot_mVs[start_index_hot_freq:end_index_hot_freq]
            hot_pwr    = hot_pwr[start_index_hot_freq:end_index_hot_freq]
            cold_freqs = cold_freqs[start_index_cold_freq:end_index_cold_freq]
            cold_mVs   = cold_mVs[start_index_cold_freq:end_index_cold_freq]
            cold_pwr   = cold_pwr[start_index_cold_freq:end_index_cold_freq]
        status = True
    else:

        mV_mesh = abs(hot_mVs[1,0] - hot_mVs[0,0])
        mV_mesh_test = abs(cold_mVs[1,0] - cold_mVs[0,0])
        if not ((mV_mesh - mV_mesh_test) < 0.0001):
            print "The mV mesh of the hot and cold spectral frequency surface do not match in the directory:"
            print prodatadir
            print mV_mesh, " is the hot mV mesh"
            print mV_mesh_test, " is the cold mV mesh"
            sys.exit()

        # Find the Overlap of the hot and cold Matrices in mV
        hot_mV  =  hot_mVs[:,0]
        cold_mV = cold_mVs[:,0]
        status, start_index_hot_mV, start_index_cold_mV, len_mV = FindOverlap(hot_mV, cold_mV, mV_mesh)
        if status:
            end_index_hot_mV  = start_index_hot_mV+len_mV
            end_index_cold_mV = start_index_cold_mV+len_mV
            hot_freqs  = hot_freqs[start_index_hot_mV:end_index_hot_mV,:]
            hot_mVs    = hot_mVs[start_index_hot_mV:end_index_hot_mV,:]
            hot_pwr    = hot_pwr[start_index_hot_mV:end_index_hot_mV,:]
            cold_freqs = cold_freqs[start_index_cold_mV:end_index_cold_mV,:]
            cold_mVs   = cold_mVs[start_index_cold_mV:end_index_cold_mV,:]
            cold_pwr   = cold_pwr[start_index_cold_mV:end_index_cold_mV,:]

            # Find the Overlap of the hot and cold Matrices in frequency
            freq_mesh      = abs(hot_freqs[0,1]  - hot_freqs[0,0])
            freq_mesh_test = abs(cold_freqs[0,1] - cold_freqs[0,0])
            if not ((freq_mesh - freq_mesh_test) < 0.0001):
                print "The freq mesh of the hot and cold spectral frequency surface do not match in the directory:"
                print prodatadir
                print freq_mesh, " is the hot freq mesh"
                print freq_mesh_test, " is the cold freq mesh"
                sys.exit()

            hot_freq  =  hot_freqs[0,:]
            cold_freq = cold_freqs[0,:]
            status, start_index_hot_freq, start_index_cold_freq, len_freq = FindOverlap(hot_freq, cold_freq, freq_mesh)
            if status:
                end_index_hot_freq  = start_index_hot_freq+len_freq
                end_index_cold_freq = start_index_cold_freq+len_freq
                hot_freqs  = hot_freqs[:,start_index_hot_freq:end_index_hot_freq]
                hot_mVs    = hot_mVs[:,start_index_hot_freq:end_index_hot_freq]
                hot_pwr    = hot_pwr[:,start_index_hot_freq:end_index_hot_freq]
                cold_freqs = cold_freqs[:,start_index_cold_freq:end_index_cold_freq]
                cold_mVs   = cold_mVs[:,start_index_cold_freq:end_index_cold_freq]
                cold_pwr   = cold_pwr[:,start_index_cold_freq:end_index_cold_freq]


    if status:
        YspecmV = hot_pwr/cold_pwr
        numpy.save(prodatadir + "Y.npy",YspecmV)
        numpy.save(prodatadir + "Y_freq.npy",hot_freqs)
        numpy.save(prodatadir + "Y_mV.npy",hot_mVs)
    else:
        print "The Specdata2Yfactor failed in the directory:"
        print prodatadir
        print "Killing the script"
        sys.exit()

    return status


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