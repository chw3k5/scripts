def mono_switch(data,max_loop,mono_mesh,max_equal,verbose):

    if not verbose == 'N':
        print " "
        print 'Making data monotonic by swithing data around'
    # my monotinic function likes data to be in one 2D-array with 
    # data[:,0] to be the data that is being made monotonic
    # note: data that is nearly () equal is left alone
    # equal points are better handled by my regridding program
    

        
    n=0
    equal_count=0
    loop_count=0
    finished=False
    status=False
    while not finished:
        diff=(data[n,0] - data[n+1,0])/mono_mesh
        if verbose == 'T':
            print 'n is ' + str(n)
            print 'loop_count is '+str(loop_count)
            print 'diff = '+ str(diff)
            
        loop_count=loop_count+1
        if loop_count > max_loop:
            finished=True
            print 'max loop count for monotonic switching was exceeded:'+str(loop_count)
            print "I set uA, tp, and pot to zero to force you to fix this problem"
        
        if diff <= 0:
            n=n+1
        elif diff > 0:
            hold=data[n,:]
            data[n,:]=data[n+1,:]
            data[n+1,:]=hold
            hold=0            
            if n==0:
                n=n+1
            else:
                n=n-1               
        if diff == 0:
            if (verbose =='T'):
                print 'Warning: there was a set of mV piont that were equal n='+str(n)+" diff="+str(diff) 
                print 'I the code ignored those points and is letting them be handle by regidding program'           
            equal_count=equal_count+1
        if n == -1:
            print "For some freaky reason the script tryied to set n=-1 and assign a data to a negitive index"
            finished=True            
        if equal_count >= max_equal:
            finished=True
            print "There were too many points ("+str(equal_count)+ ") that were equal,"
            print "check your data bro, or increase the max_equal variable"
            print "(:I mean bro in the genderless way, like friend:)"
        if n == len(data[:,0])-1:
            finished=True
            status=True
            if not verbose == 'N':
                print "monotonic switching finished clean"
                print "the number of points that were equal: "+str(equal_count)
                print "It took "+ str(loop_count)+ " loops to reorder "+str(len(data[:,0]))+" data points" 
    mono_data = data
    return mono_data, status