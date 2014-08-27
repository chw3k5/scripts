def checkbias():
    import telnetlib
    import time
    import os
    import atpy
    
    uA_bias=''
    mV_bias=''
    status=False
    
    #set the pot position of the magnet and recound the current and volage
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    tn.write("setbias 0 \n")
    time.sleep(1)
    out1 = tn.read_very_eager()
    out2 = out1.replace('sis 0 ', '')
    out3 = out2.replace(' = ', ',')
    f = open('temp.txt', 'w')
    f.write('type, number \n')
    f.write(out3)
    f.close()        
    tn.close()

    # reordering the data from the setbias command
    putty = atpy.Table('temp.txt', type='ascii', delimiter=',')
    pee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='p']
    vee = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='v']
    eye = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='i']
    eph = [putty.number[ii] for ii, v in enumerate(putty.type) if v=='f']
    
    n = open('temp.csv', 'w')
    n.write('pot, mV, uA, f \n')
    for jj in range(len(pee)):
        #print jj
        n.write(str(pee[jj])+','+str(vee[jj])+','+str(eye[jj])+','+str(eph[jj])+'\n')
    n.close()
    
    # read data into convienent variables 
    data = atpy.Table('temp.csv', type="ascii", delimiter=",")
    uA_bias  = float(data.uA)
    mV_bias  = float(data.mV)
    pot_bias = float(data.pot)
    if (uA_bias != '' and mV_bias != ''):
        status=True
    else:
        print "no current/voltage was reported, There may be problem with the THz bias computer. Returning Status=False"
    
    #print 'magnet current is ' +str(mA_mag)+ ' mA'
    
    temp_str='rm temp.txt temp.csv'
    os.system(temp_str)
    
    return status, uA_bias, mV_bias, pot_bias