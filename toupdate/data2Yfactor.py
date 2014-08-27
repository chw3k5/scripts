def data2Yfactor(hot_mV, cold_mV, off_tp, hot_tp, cold_tp, start_Yrange, end_Yrange, mesh, verbose):
    import numpy
    status=True
    # the first thing that we need to do is find the over lab in the mV range for off, hot and cold
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
            mV_max_Yfactor=0
            max_Yfactor=0
        if ((count_hot>=len(hot_mV)-1) or (count_cold>=len(cold_mV)-1)):
            finished=True
            print "I seems the mV values of cold and hot do not over lap, ruturning status=False"
            status=False
            mV_Yfactor=0 
            Yfactor= 0
            max_Yfactor=0
            mV_max_Yfactor=0
            
    if status:
        len_mV=min(len(hot_mV[count_hot:]),len(cold_mV[count_cold:]))
        mV_Yfactor = numpy.zeros((len_mV))
        Yfactor    = numpy.zeros((len_mV))
    	
        for x in range(min(len(hot_mV[count_hot:]),len(cold_mV[count_cold:]))):
            mV_Yfactor[x]=hot_mV[count_hot+x]
            Yfactor[x]=((hot_tp[x]-off)/(cold_tp[x]-off))
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

    return mV_Yfactor, Yfactor, mV_max_Yfactor, max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, status
    
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