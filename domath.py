import numpy
import scipy.stats
import math
import sys
import glob
from operator import itemgetter
import pickle

###################################
###### filter_on_occurrences ######
###################################

#  unique_element_list = filter_on_occurrences(vector,min_occurrences=1,max_occurrences=None)
def filter_on_occurrences(vector,min_occurrences=1,max_occurrences=None):
    unique_element_list = []
    the_dict = {element:vector.count(element) for element in vector}
    for unique_element, occurrences in the_dict.iteritems():
        if (((min_occurrences <= occurrences) or (min_occurrences is None))
            and ((occurrences <= max_occurrences) or (max_occurrences is None))):
            unique_element_list.append(unique_element)
    if unique_element_list != []:
        unique_element_list.sort()
        unique_element_list.reverse()
    else:
        print 'The filter_on_occurrences definition has filtered out all responces,'
        print 'The min occurences are:',min_occurrences
        print 'The max occurences are:',max_occurrences
        print 'The dictionary is:',the_dict
    #print the_dict
    return unique_element_list


########################
###### properrors ######
########################

def properrors(x,delx,y,dely,z):
    z=numpy.array(z)
    x=numpy.array(x)
    delx=numpy.array(delx)
    y=numpy.array(y)
    dely=numpy.array(dely)
    normx=delx/x
    normy=dely/y
    delzOverz=numpy.sqrt((normx**2)+(normy**2))
    delz=z*delzOverz
    return delz


############################
###### make_monotonic ######
############################

def make_monotonic(list_of_lists,reverse=False):
    # the first list in the list_of_list should be the one for which the other lists are to be sorted
    # pack the data into the correct format
    sort_matrix = [list(x) for x in zip(*list_of_lists)]
    # sort
    sorted_martix_lists = sorted(sort_matrix, key=itemgetter(0))
    if reverse:
        sorted_martix_lists.reverse()
    sorted_martix = numpy.array(sorted_martix_lists)
    # Unpack and reverse
    sorted_list_of_lists = [list(x) for x in zip(*sorted_martix)]
    return sorted_list_of_lists


def make_monotonic_old(list_of_lists,reverse=False):
    # the first list in the list_of_list should be the one for which the other lists are to be sorted
    sorted_list_of_lists = []
    num_of_lists = len(list_of_lists)
    sort_list = list_of_lists[0]
    len_sort_list = len(sort_list)
    sort_matrix = numpy.zeros((len_sort_list,num_of_lists))
    for (list_index,alist) in list(enumerate(list_of_lists)):
        sort_matrix[:,list_index]=alist
    sorted_martix = numpy.array(sorted(sort_matrix, key=itemgetter(0)))
    if reverse:
        for list_index in range(num_of_lists):
            sorted_list_of_lists.append(list(sorted_martix[:,list_index]).reverse())
    else:
        for list_index in range(num_of_lists):
            sorted_list_of_lists.append(list(sorted_martix[:,list_index]))
    return sorted_list_of_lists



######################
###### uniquify ######
######################
def uniquify(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


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

    if regrid_start == regrid_end:
        regrid_data=numpy.array(data)
    else:
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
    if verbose:
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


##############################
###### find_occurrences ######
##############################


def find_occurrences(the_vector):
    occurrences_dict = {element:the_vector.count(element) for element in the_vector}
    max_occurrence_finder = 0
    max_element = None
    for element, occurrences in occurrences_dict.iteritems():
        if max_occurrence_finder < occurrences:
            max_element=element
            max_occurrence_finder = occurrences

    return occurrences_dict, max_element, max_occurrence_finder


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
    status   = True
    X_test = numpy.array(X)
    Y_test = numpy.array(Y)
    numpy.sort(X_test)
    numpy.sort(Y_test)
    X_test = numpy.round(X_test/mesh)
    Y_test = numpy.round(Y_test/mesh)
    # X_test = uniquify(X_test)
    # Y_test = uniquify(Y_test)
    lenX=len(X_test)
    lenY=len(Y_test)
    minX=X_test[0]
    minY=Y_test[0]
    maxX=X_test[-1]
    maxY=Y_test[-1]

    count_X = 0
    count_Y = 0
    length = lenX


    # truncate the start of each X and Y arrays until they overlap
    if minX < minY:
        # operate on the X vector
        if minY < maxX:
            print "It seems the mV values of Y and X do not overlap."
            print "minY:",minY, " is less than maxX:",maxX
            print "Returning status = False"
            status=False
        else:
            for xIndex in range(lenX):
                if minY <= X_test[xIndex]:
                    count_X = xIndex
                    break

    else:
        # operate on the Y vector
        if minX < maxY:
            print "It seems the mV values of Y and X do not overlap."
            print "minX:",minX, " is less than maxY:",maxY
            print "Returning status = False"
            status=False
        else:
            for yIndex in range(lenY):
                if minX <= Y_test[yIndex]:
                    count_Y = yIndex
                    break

    # truncate the ends of each X and Y arrays until they overlap
    new_minX = X_test[count_X]
    new_minY = Y_test[count_Y]
    if status:
        if maxX < maxY:
            # operate on the Y vector
            for yIndex in reversed(range(count_Y,lenY)):
                if maxX <= Y_test[yIndex]:
                    length = yIndex-count_Y+1
                    break
        else:
            # operate of the X vector
            for xIndex in reversed(range(count_X,lenX)):
                if maxY <= X_test[xIndex]:
                    length = xIndex-count_X+1
                    break





    # finished = False
    # while not finished:
    #     if ((lenX<=count_X) or (lenY<=count_Y)):
    #         print "It seems the mV values of Y and X do not overlap, returning status=False"
    #         status=False
    #         break
    #     elif X_test[count_X]==Y_test[count_Y]:
    #         break
    #
    #     elif X_test[count_X] < Y_test[count_Y]:
    #         count_X += 1
    #     else:
    #         count_Y += 1
    #
    #     loop_count=loop_count+1
    #     if loop_count_max < loop_count_max:
    #         print "The loop has gone on long enough to exceed the length of both Y_mV and X_mV, \n"+\
    #               "something could be wrong with the regridding. Status=False"
    #         status=False
    #         break
    #
    # if status:
    #     length  = min(len(X[count_X:]),len(Y[count_Y:]))
    # else:
    #     length  = None

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
    status = True

    # I only care about this list's length
    search_str = prodatadir + 'hotspecdata_*.npy'
    spec_list_len = len(glob.glob(search_str))


    for Y_index in range(spec_list_len):

        hotfilename  = prodatadir + 'hotspecdata_'+str(Y_index+1)+'.npy'
        coldfilename = prodatadir + 'coldspecdata_'+str(Y_index+1)+'.npy'
        with open(hotfilename, 'r') as f:
            the_hotcan = f.read()
        with open(coldfilename, 'r') as f:
            the_coldcan = f.read()
        (hot_freq,hot_pwr,hot_pot,hot_mV_mean,hot_tp,hot_spike_list,hot_spikes_inband,hot_sweep_index) = pickle.loads(the_hotcan)
        (cold_freq,cold_pwr,cold_pot,cold_mV_mean,cold_tp,cold_spike_list,cold_spikes_inband,cold_sweep_index) = pickle.loads(the_coldcan)

        if not (hot_sweep_index == cold_sweep_index):
            print "The hot and cold sweep indexes are different:",hot_sweep_index,',', cold_sweep_index
            print "there is some sort of nightmare problem in the part of the code that does that data processing"
            print "killing the script in the function Specdata2Yfactor in domath.py"
            sys.exit()

        # find the frequency mesh
        step_vector = list(numpy.array(hot_freq[1:])-numpy.array(hot_freq[:-1]))
        occurrences_dict, freq_mesh, max_occurrence_finder = find_occurrences(step_vector)
        if freq_mesh is None:
            freq_mesh = 0.001

        status, start_index_hot_freq, start_index_cold_freq, len_freq = FindOverlap(hot_freq, cold_freq, freq_mesh)
        end_index_hot_freq  = start_index_hot_freq  + len_freq
        end_index_cold_freq = start_index_cold_freq + len_freq
        freq     =  hot_freq[start_index_hot_freq:end_index_hot_freq]
        hot_pwr  =   hot_pwr[start_index_hot_freq:end_index_hot_freq]
        cold_pwr = cold_pwr[start_index_cold_freq:end_index_cold_freq]

        #Yfactor = (hot_pwr**2)/(cold_pwr**2)
        Yfactor = (hot_pwr)/(cold_pwr)
        Y_data_filename = prodatadir + "Y"+str(hot_sweep_index+1)+".npy"

        big_can = (freq,Yfactor,
                   hot_pwr ,hot_pot ,hot_mV_mean ,hot_tp ,hot_spike_list ,hot_spikes_inband ,hot_sweep_index,
                   cold_pwr,cold_pot,cold_mV_mean,cold_tp,cold_spike_list,cold_spikes_inband,cold_sweep_index)

        pickle_str = pickle.dumps(big_can)

        with open(Y_data_filename, 'w') as f:
            the_hotcan = f.write(pickle_str)

    return status


def Specdata2Yfactor_old(prodatadir, verbose=False):
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
        YspecmV = (hot_pwr**2)/(cold_pwr**2)
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

def find_neighbors(x_val, x_array,fx_array):
    distance_array=None
    value_array=None
    index_array=None
    finished = True

    x_val=float(x_val)
    x_array = numpy.array(x_array)
    f_list=list(x_array)
    fx_array = numpy.array(fx_array)
    x_len=len(x_array)
    fx_len=len(fx_array)

    # some brief error checking
    if not (x_len == fx_len):
        print "In the function 'find_neighbors' the x and f(x) arrays are not the same length, this is not allowed."
    else:
        if (x_len < 2 ):
             print "In the function 'find_neighbors' the length of the x array is less than 2. x_len="+str(x_len)+", this is not allowed."
        else:
            finished = False

    if not finished:
        old_index_array = numpy.arange(x_len)
        matrix = numpy.zeros((x_len, 3))
        matrix[:,0] = abs(x_val-x_array)
        matrix[:,1] = fx_array
        matrix[:,2] = old_index_array
        diff_array = abs(x_array-x_val)

        mono_matrix  = numpy.asarray(sorted(matrix,  key=itemgetter(0)))
        distance_array = mono_matrix[:,0]
        value_array = mono_matrix[:,1]
        index_array = mono_matrix[:,2]
        None
    return distance_array, value_array, index_array

def spike_function(x_array, fx_array, neighborhood=[2,4,8,16,32,64,128]):
    import time
    finished = True
    spike_array_norm = None

    x_array = numpy.array(x_array)
    fx_array = numpy.array(fx_array)

    n_len = len(neighborhood)
    x_len=len(x_array)
    fx_len=len(fx_array)
    spike_sum_array = numpy.zeros((x_len,n_len))
    spike_array_norm = numpy.zeros((x_len,n_len))
    spike_array_sqdiff_norm = numpy.zeros((x_len,n_len))
    # some brief error checking
    if not (x_len == fx_len):
        print "In the function 'find_neighbors' the x and f(x) arrays are not the same length, this is not allowed."
    else:
        if (x_len < 2 ):
             print "In the function 'find_neighbors' the length of the x array is less than 2. x_len="+str(x_len)+", this is not allowed."
        else:
            finished = False

    # this is a flag to skip the rest of the program if it is not possible to run
    if not finished:

        # this is the loop that uses the 'find neighbors' function to make an ordered
        # list of the values of each point's nearest neighbors
        for index in range(x_len):
            x_val = x_array[index]
            fx_val = fx_array[index]
            spike_sum = 0
            x_distance_array, fx_value_array, index_array = find_neighbors(x_val, x_array, fx_array)

            # this is the loop over the list of neighboring points that make up my spike function
            for (n_index, neighbors) in list(enumerate(neighborhood)):
                neighbors_to_check = min(x_len,neighbors)
                near_values = fx_value_array[:neighbors_to_check]
                spike_sum_array[index,n_index] = sum(fx_val-near_values)

        # normailize all the spike functions so that their average value is 1
        for n_index in range(n_len):
            spike_array_norm[:,n_index] = spike_sum_array[:,n_index]/numpy.mean(spike_sum_array[:,n_index])


        # the spike_array_norm has an average value of 1,
        # now we find the squared difference of that array
        # from the expectation value of 1 in that array
        spike_array_sqdiff = (1.0 - spike_array_norm)**2
        spike_array_sqdiff_norm = numpy.zeros(numpy.shape(spike_array_sqdiff))

        # Now we normalize squared difference function to have an expectation value of 1
        for n_index in range(len(neighborhood)):
            spike_array_sqdiff_norm[:,n_index] = spike_array_sqdiff[:,n_index]/numpy.mean(spike_array_sqdiff[:,n_index])


    return spike_array_sqdiff_norm, neighborhood

def spike_masker(family_of_arrays, min_flag_value=10,flag_number=1):
    family_of_arrays=abs(numpy.array(family_of_arrays))

    # some brief error checking to make sure flag number is set properly
    try:
        family_size = len(family_of_arrays[0,:])
    except:
        family_size = 1

    if flag_number < 1:
        flag_number = 1
    elif family_size<flag_number:
        flag_number=family_size


    mask_famliy = 1*(family_of_arrays>min_flag_value)
    stacked_masks = numpy.sum(mask_famliy,axis=1)

    final_mask = stacked_masks >= flag_number


    return final_mask





def spike_removal(data,verbose=False, neighbor_list=[2,4,8,16,32,64,128,256],min_flag_value=10,flag_number=3,
                  set_flag_fraction=0.3):
    list_len = len(data)
    set_flag_number = numpy.round(list_len*set_flag_fraction)
    spike_frequencies = []
    rinsed_data = []
    spike_lists_for_spectra = []
    spike_list_for_set = []
    for (freq,pwr) in data:
        # This function analyses the spectral data to make a function that makes spikes detectable
        spike_array_sqdiff_norm, neighborhood = spike_function(freq, pwr, neighborhood=neighbor_list)
        # This makes a mask of from the output of the function above
        spike_mask = spike_masker(spike_array_sqdiff_norm, min_flag_value=min_flag_value,flag_number=flag_number)

        # Now we delete the spikes in the data and make a list of all frequencies in this set that have spikes
        rinse_freq = []
        rinse_pwr = []

        spike_list = []
        for (s_index,spike_truth) in list(enumerate(spike_mask)):
            if spike_truth:
                spike_freq=freq[s_index]
                spike_list.append(spike_freq)
                spike_frequencies.append(spike_freq)
            else:
                rinse_freq.append(freq[s_index])
                rinse_pwr.append(pwr[s_index])
        spike_lists_for_spectra.append(spike_list)
        rinsed_data.append((rinse_freq,rinse_pwr))

    # Now we will remove some data from the whole set if there is a spike at that point for a fraction
    # greater than that of the variable 'set_flag_fraction'

    # This part makes a dictionary of the frequencies and there occurrences
    set_remove_freqs = []
    spike_dict = {element:spike_frequencies.count(element) for element in spike_frequencies}
    for spike_freq, occurences in spike_dict.iteritems():
        if set_flag_number < occurences:
            set_remove_freqs.append(spike_freq)
    spike_list_for_set = set_remove_freqs
    # now we loop through the set of data and get rid of data points with spikes access the entire set of spectra
    clean_data = []


    for (freq,pwr) in rinsed_data:
        # find the frequency mesh
        step_vector = list(numpy.array(freq[1:])-numpy.array(freq[:-1]))
        occurrences_dict, freq_mesh, max_occurrence_finder = find_occurrences(step_vector)
        if freq_mesh is None:
            freq_mesh = 0.001

        clean_freq = freq
        clean_pwr  = pwr
        for remove_freq in set_remove_freqs:

            try:
                remove_index = clean_freq.index(remove_freq)
                clean_freq.pop(remove_index)
                clean_pwr.pop(remove_index)
            except:
                spike_found = False
                search_radius = freq_mesh/2.0
                for (f_index,f_element) in list(enumerate(clean_freq[:])):
                    if abs(remove_freq - f_element) < search_radius:
                        clean_freq.pop(f_index)
                        clean_pwr.pop(f_index)
                        spike_found = True
                if not spike_found:
                    if verbose:
                        print "the frequency,",remove_freq,"GHz was not found in the frequency lists in the spike removal function"

        clean_data.append((clean_freq,clean_pwr))


    return clean_data, spike_lists_for_spectra, spike_list_for_set

def spike_removal_old(data_list,remove_threshold=10.0,verbose=False):
    list_len = len(data_list)
    data_array = numpy.array(data_list)
    diff_array = data_array[:-1]-data_array[1:]
    mean_diff = numpy.mean(diff_array)
    threshold_diff = mean_diff*remove_threshold
    try:
        right_diff = abs(diff_array[0])
        clean_data_list=data_list
        for index in range(1,list_len-1):
            left_diff  = right_diff
            right_diff = abs(diff_array[index])
            if ((threshold_diff < left_diff) and (threshold_diff < right_diff)):
                if verbose:
                    print "removing data spike, spike value:", data_list[index], "  left value:",data_list[index-1], "  right value:",data_list[index+1]
                clean_data_list[index]=(data_list[index-1]+data_list[index+1])/2.0
    except:
        clean_data_list = None

    return clean_data_list