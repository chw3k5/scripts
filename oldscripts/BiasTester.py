import sys
from setbias        import setbias
from setmag         import setmag
from setfeedback    import setfeedback
from zeropots       import zeropots 

verbose    = True

coldmeas   = False
dummydewar = False
dummypixel = False

domag      = True

feedback   = False

status = setfeedback(feedback)
if status == False:
    print "The function setfeedback failed, exiting this script"
    sys.exit()
  
#################### For the dummy dewar ######################
if (not coldmeas and dummydewar and not dummypixel):
    print " "
    potpos1=62000
    potpos2=68000
    status, uA_bias1, mV_bias1 = setbias(potpos1)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    status, uA_bias2, mV_bias2 = setbias(potpos2)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    sisRes=1000*(mV_bias2 - mV_bias1)/(uA_bias2 - uA_bias1)
    print "For a dummy dewar at 300K"
    print str('%2.2f' % sisRes) + " Ohms is SIS bias resistance"
    print "20 Ohms is nominal"
    print ' '
    if verbose:
        print str('%2.4f' % mV_bias1) + ' mV, '+str('%2.4f' % uA_bias1) +' uA at pot position '+str(potpos1)
        print str('%2.4f' % mV_bias2) + ' mV, '+str('%2.4f' % uA_bias2) +' uA at pot position '+str(potpos2)
        print ' '
    
    status, mA_mag1, V_mag1 = setmag(50000)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    status, mA_mag2, V_mag2 = setmag(80000)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    magRes = 1000*(V_mag2 - V_mag1)/(mA_mag2 - mA_mag1)
    print str('%2.3f' % magRes) + " Ohms is the magnet resistance"
    print "1.9 Ohms is nominal"
    print ' '

#################### For the dummy pixel ###################### 
if (not coldmeas and dummypixel and not dummydewar):
    print " "
    potpos1=62000
    potpos2=68000
    status, uA_bias1, mV_bias1 = setbias(potpos1)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    status, uA_bias2, mV_bias2 = setbias(potpos2)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    sisRes=1000*(mV_bias2 - mV_bias1)/(uA_bias2 - uA_bias1)
    print "For a dummy pixel at 300K"
    print str('%2.2f' % sisRes) + " Ohms is SIS bias resistance"
    print "180 Ohms is nominal"
    print ' '
    if verbose:
        print str('%2.4f' % mV_bias1) + ' mV, '+str('%2.4f' % uA_bias1) +' uA at pot position '+str(potpos1)
        print str('%2.4f' % mV_bias2) + ' mV, '+str('%2.4f' % uA_bias2) +' uA at pot position '+str(potpos2)
        print ' '
    
    status, mA_mag1, V_mag1 = setmag(60000)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    status, mA_mag2, V_mag2 = setmag(70000)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    magRes = 1000*(V_mag2 - V_mag1)/(mA_mag2 - mA_mag1)
    print str('%2.3f' % magRes) + " Ohms is the magnet resistance"
    print "46 Ohms is nominal"
    print ' '
    
#################### For the 300K Real Pixel ######################
if (not coldmeas and not dummydewar and not dummypixel):
    print " "
    potpos1=62000
    potpos2=66000
    status, uA_bias1, mV_bias1 = setbias(potpos1)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    status, uA_bias2, mV_bias2 = setbias(potpos2)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    sisRes=1000*(mV_bias2 - mV_bias1)/(uA_bias2 - uA_bias1)
    print "For the real Pixel at 300K"
    print str('%2.2f' % sisRes) + " Ohms is SIS bias resistance"
    print "180 Ohms is nominal"
    print ' '
    if verbose:
        print str('%2.4f' % mV_bias1) + ' mV, '+str('%2.4f' % uA_bias1) +' uA at pot position '+str(potpos1)
        print str('%2.4f' % mV_bias2) + ' mV, '+str('%2.4f' % uA_bias2) +' uA at pot position '+str(potpos2)
        print ' '
    
    if domag:
        status, mA_mag1, V_mag1 = setmag(60000)
        if status == False:
            print "The function setmag failed, exiting this script"
            sys.exit()
        status, mA_mag2, V_mag2 = setmag(70000)
        if status == False:
	    print "The function setmag failed, exiting this script"
            sys.exit()
        magRes = 1000*(V_mag2 - V_mag1)/(mA_mag2 - mA_mag1)
        print str('%2.3f' % magRes) + " Ohms is the magnet resistance"
        print "44 Ohms is nominal"
    	print ' '   
    
    
    
zeropots()
print "The script is completed"