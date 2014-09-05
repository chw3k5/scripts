def fastSISsweep(SweepStart, SweepStop, SweepStep, fullname, verbose):
    import telnetlib
    import time
    import os
    import atpy
    
    if SweepStart > SweepStop:
        SweepPot      = range(SweepStart, SweepStop-SweepStep, -1*SweepStep)
        num_of_points = len(SweepPot)+1
    else:
        SweepPot      = range(SweepStart, SweepStop+SweepStep,  SweepStep)
        num_of_points = len(SweepPot)+1
    
    SweepStop  = SweepPot[num_of_points-2]
    sweepsleep = round(num_of_points/10)+5 # 50 secs for 500 points
    if verbose:
        print "The sweep sleep time is "+str(sweepsleep)+" seconds"
        
#    if not feedback:
    if True:
        #Sweep   = "sweep 0 65100 52600 500 \n"
        SweepCMD = "sweep 0 "+str('%06.f' % SweepStart)+" "+str('%06.f' % SweepStop)+" "+str('%06.f' % num_of_points)+" \n" # don't forget the \n

            
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
        
        n = open(fullname, 'w')
        n.write('pot, mV, uA, tp \n')
        for jj in range(len(pee)):
            n.write(str(pee[jj])+','+str(vee[jj])+','+str(eye[jj])+','+str(tee[jj])+'\n')
        n.close()
        os.remove('temp.txt')
    return
    
def getfastSISsweep(SweepStart, SweepStop, SweepStep, verbose):
    import telnetlib
    import time
    import os
    import atpy
    
    if SweepStart > SweepStop:
        SweepPot      = range(SweepStart, SweepStop-SweepStep, -1*SweepStep)
        num_of_points = len(SweepPot)+1
    else:
        SweepPot      = range(SweepStart, SweepStop+SweepStep,  SweepStep)
        num_of_points = len(SweepPot)+1
    
    SweepStop  = SweepPot[num_of_points-2]
    sweepsleep = round(num_of_points/10)+5 # 50 secs for 500 points
    if verbose:
        print "The sweep sleep time is "+str(sweepsleep)+" seconds"
        
#    if not feedback:
    if True:
        #Sweep   = "sweep 0 65100 52600 500 \n"
        SweepCMD = "sweep 0 "+str('%06.f' % SweepStart)+" "+str('%06.f' % SweepStop)+" "+str('%06.f' % num_of_points)+" \n" # don't forget the \n

            
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
        pot = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='p']
        mV  = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='v']
        uA  = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='i']
        tp  = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='t']
        os.remove('temp.txt')

    return pot, mV, uA, tp