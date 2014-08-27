def data2Yfactor2(off_mV, hot_mV, cold_mV, off_tp, hot_tp, cold_tp, start_Yrange, end_Yrange, mesh, verbose):
    import numpy
    status = False
    off=numpy.mean(off_tp)
    count_max=100000
    finished1=False
    finished2=False
    finished3=False
    loopfinished=False
    begin_mV = max(off_mV[0], hot_mV[0], cold_mV[0])
    count=0
    while ((not ((finished1) and (finished2) and (finished3))) and (not loopfinished)):
        if round(off_mV[count]/mesh) == round(begin_mV/mesh):
            off_mV_index_start  = count
            finished1=True
        if round(hot_mV[count]/mesh) == round(begin_mV/mesh):
            hot_mV_index_start  = count
            finished2=True
        if round(cold_mV[count]/mesh) == round(begin_mV/mesh):
            cold_mV_index_start  = count
            finished3=True
        if count >= count_max:
            loopfinished=True
        count = count +1
        
    finished1=False
    finished2=False
    finished3=False
    loopfinished=False
    end_mV = min(off_mV[len(off_mV)-1], hot_mV[len(hot_mV)-1], cold_mV[len(cold_mV)-1])
    count=0
    while ((not ((finished1) and (finished2) and (finished3))) and (not loopfinished)):
        if round(off_mV[len(off_mV)-1-count]/mesh) == round(end_mV/mesh):
            off_mV_index_end  = len(off_mV)-1-count
            finished1=True
        if round(hot_mV[len(hot_mV)-1-count]/mesh) == round(end_mV/mesh):
            hot_mV_index_end  = len(hot_mV)-1-count
            finished2=True
        if round(cold_mV[len(cold_mV)-1-count]/mesh) == round(end_mV/mesh):
            cold_mV_index_end  = len(cold_mV)-1-count
            finished3=True
        if count >= count_max:
            loopfinished=True
        count = count +1
        
    len_mV_off  = off_mV_index_end-off_mV_index_start
    len_mV_hot  = hot_mV_index_end-hot_mV_index_start
    len_mV_cold = cold_mV_index_end-cold_mV_index_start
    mV_Yfactor = numpy.zeros((len_mV_off))
    Yfactor    = numpy.zeros((len_mV_off))
    if ((len_mV_off == len_mV_hot) and (len_mV_off == len_mV_cold)):
        mV_Yfactor=off_mV[off_mV_index_start:off_mV_index_end+1]
        off=numpy.mean(off_tp[off_mV_index_start:off_mV_index_end+1])
        Yfactor=(hot_tp[hot_mV_index_start:hot_mV_index_end+1]-off)/(cold_tp[cold_mV_index_start:cold_mV_index_end+1]-off)
        
        summer=0
        count=0
        max_Yfactor=-1
        mV_max_Yfactor=-999999
        min_Yfactor=999999
        mV_min_Yfactor=-999999
        for n in range(len(Yfactor)):
            if ((mV_Yfactor[n] >= start_Yrange) and (mV_Yfactor[n] <= end_Yrange)):
                count=count+1
                summer=summer+Yfactor[n]
                if max_Yfactor < Yfactor[n]:
                    max_Yfactor = Yfactor[n]
                    mV_max_Yfactor = mV_Yfactor[n]
                if min_Yfactor > Yfactor[n]:
                    min_Yfactor = Yfactor[n]
                    mV_min_Yfactor = mV_Yfactor[n]
        if count==0:
            count=1
        mean_Yfactor=summer/count
        if ((mV_max_Yfactor==-999999) or (max_Yfactor==-1)):
            status=False
            print "The was a problem finding the mV of the max Yfactor"
        if ((mV_min_Yfactor==-999999) or (min_Yfactor==999999)):
            status=False
            print "The was a problem finding the mV of the min Yfactor"
        status = True
    return mV_Yfactor, Yfactor, mV_max_Yfactor, max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, status