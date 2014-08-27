def IVsweeps(SweepStart, SweepStop, SweepStep, feedback, fullname):
    import telnetlib
    import time
    import os
    import atpy
    
    status = False
    
    if SweepStart > SweepStop:
        SweepPot      = range(SweepStart, SweepStop-SweepStep, -1*SweepStep)
        num_of_points = len(SweepPot)+1
    else:
        SweepPot      = range(SweepStart, SweepStop+SweepStep,  SweepStep)
        num_of_points = len(SweepPot)+1
    
    SweepStop  = SweepPot[num_of_points-2]
    sweepsleep = round(num_of_points/10)+10 # 50 secs for 500 points
    print "The sweep sleep time is "+str(sweepsleep)+" secounds"
        
#    if not feedback:
    if True:
        #Sweep   = "sweep 0 65100 52600 500 \n"
        SweepCMD = "sweep 0 "+str('%06.f' % SweepStart)+" "+str('%06.f' % SweepStop)+" "+str('%06.f' % num_of_points)+" \n" # don't forget the \n
        maxloops = 3
        finished = False
        loopIndex = 0
        while not finished:
            if loopIndex >= maxloops:
                finished = True
                print "the increasing of the sweepsleep was stopped after "+str(maxloops)+ " loops. Returning status = False"
            loopIndex =loopIndex+1
            
            tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
            tn.write(SweepCMD)
            time.sleep(sweepsleep)
            out1 = tn.read_very_eager()
            out2 = out1.replace('sis 0 ', '')
            out3 = out2.replace(' = ', ',')
            f = open('temp.txt', 'w')
            f.write('type, number \n')
            f.write(out3)
            f.close()
            tn.close()
            
            # reordering the data from the sweep command
            putty = atpy.Table('temp.txt', type='ascii', delimiter=',')
            pee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='p']
            vee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='v']
            eye = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='i']
            tee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='t']
            
            n = open(fullname+'.csv', 'w')
            n.write('pot, mV, uA, tp \n')
            for jj in range(len(pee)):
                #print jj
                n.write(str(pee[jj])+','+str(vee[jj])+','+str(eye[jj])+','+str(tee[jj])+'\n')
            n.close()
            
            temp_str='rm temp.txt'
            os.system(temp_str)
                                        
            # read data into convienent variables 
            data = atpy.Table(fullname+'.csv', type="ascii", delimiter=",")
            
            mV=data.mV
            uA=data.uA
            tp=data.tp
            
            if len(mV) >= num_of_points:
                finished = True
                status   = True
            else:
                sweepsleep= sweepsleep+round((num_of_points-len(mV))/10)+5
                print "We did not get all the points, redoing the sweep with more points"
                
                
#    elif feedback:
#        waitTime1=0.2
#        waitTime2=0.2
#        for x in range(len(SweepPot)):
#            print "x is "+str(x)+" of "+str(len(SweepPot))
#            if x==0:
#                # connect to the THz bias computer
#                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
#                # this is the file header for the data output
#                f = open('temp.txt', 'w')
#                f.write('type, number \n')
#            
#            SweepCMD = "sweep 0 "+str('%06.f' % SweepPot[x])+" "+str('%06.f' % SweepPot[x])+" 1 \n" # don't forget the \n
#            print SweepCMD
#            tn.write(SweepCMD)
#            time.sleep(waitTime1)
#            tn.write('setbias 0 \n')
#            time.sleep(waitTime2)
#            out1 = tn.read_very_eager()
#            out2 = out1.replace('sis 0 ', '')
#            out3 = out2.replace(' = ', ',')
#            f.write(out3)
#               
#        f.close()       
#        tn.close()   
#        
#        n = open(fullname+'.csv', 'w')
#        n.write('pot, mV, uA, tp \n')
#        # reordering the data from the sweep command
#        putty = atpy.Table('temp.txt', type='ascii', delimiter=',')
#        pee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='p']
#        vee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='v']
#        eye = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='i']
#        tee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='t']
#        
#        for jj in range(len(pee)):
#            #print jj
#            n.write(str(pee[jj])+','+str(vee[jj])+','+str(eye[jj])+','+str(tee[jj])+'\n')
#        n.close()
#        
#        temp_str='rm temp.txt'
#        os.system(temp_str)
                                   
        # read data into convienent variables 
#        data = atpy.Table(fullname+'.csv', type="ascii", delimiter=",")
        
#        mV=data.mV
#        uA=data.uA
#        tp=data.tp
#        status=True
        
    return status, mV, uA, tp