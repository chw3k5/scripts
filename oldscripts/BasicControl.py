from LabJackU3_DAQ0 import LabJackU3_DAQ0
from setfeedback import setfeedback
from setmag import setmag
from zeropots import zeropots
from setbias import setbias
import StepperControl

import sys


UCA_voltage = 3.0
magpot=200
biaspot=56200
feedback=True

Enable = False
Disable = True

if Disable:
    # diable things that are already running
    status = StepperControl.DisableDrive()
    if status == False:
        print "The function StepperControlinitialize failed, exiting this script"
        sys.exit()
    status = LabJackU3_DAQ0(0)
    zeropots()

if Enable:
    # Enable the things you want to enable 
    status = LabJackU3_DAQ0(abs(UCA_voltage))
    if status == False:
        print "The function LabJackU3_DAQ0 failed, exiting this script"
        sys.exit()
    
    
    # feedback is turned on of off here
    status = setfeedback(feedback)
    if status == False:
        print "The function setfeedback failed, exiting this script"
        sys.exit()
	    
    status, mA_mag, V_mag = setmag(magpot)
    if status == False:
        print "The function setmag failed, exiting this script"
        sys.exit()
    
    status, uA_bias, mV_bias = setbias(biaspot)
    if status == False:
        print "The function setbias failed, exiting this script"
        sys.exit()
    
    print "The magnet is at pot position "+str(magpot)+" \n"+" "+str('%02.3f' % mA_mag)+" mA \n "+str('%01.4f' % V_mag)+ " V \n"
    print "The bias is at pot position "+str(biaspot)+" \n"+" "+str('%02.3f' % uA_bias)+" uA \n "+str('%01.4f' % mV_bias)+ " mV \n"