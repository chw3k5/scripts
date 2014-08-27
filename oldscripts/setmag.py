def setmag(magpot):
    import telnetlib
    import time
    import os
    import atpy
    
    mA_mag=''
    V_mag=''
    status=False

    #set the pot position of the magnet and recound the current and volage
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    if (magpot > 0 and magpot < 65100):
         tn.write("setbias 9 0 \n")
    elif  magpot < 129750:
        tn.write("setbias 9 129750 \n")
    time.sleep(3)
    
    tn.write("setbias 9 "+str(magpot) + " \n")
    time.sleep(1)
    tn.write("setbias 9 \n")
    time.sleep(1)
    out1 = tn.read_very_eager()
    out2 = out1.replace('mag 1 ', '')
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
    n.write('pot, V, mA, f \n')
    for jj in range(len(pee)):
        #print jj
        n.write(str(pee[jj])+','+str(vee[jj])+','+str(eye[jj])+','+str(eph[jj])+'\n')
    n.close()
    
    # read data into convienent variables 
    data = atpy.Table('temp.csv', type="ascii", delimiter=",")
    mA_mag=float(data.mA)
    V_mag=float(data.V)
    if (mA_mag != '' and V_mag != ''):
        status=True
    else:
        print "no current/voltage was reported, There may be problem with the THz bias computer. Returning Status=False"
    
    #print 'magnet current is ' +str(mA_mag)+ ' mA'
    
    temp_str='rm temp.txt temp.csv'
    os.system(temp_str)
    
    return status, mA_mag, V_mag