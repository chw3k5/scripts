############################################################################
# Connect to the Parker Gemini 6K controller, microstepping drive, and
#     stepper motor via serial port.
# Required Python packages:  visa
# Linda Kuenzi (lkuenzi@asu.edu)
# Last updated 02/13/2014 by caleb
#
# I had to install stuff to make USB to Serial stuff work on my mac
# download at http://www.xbsd.nl/pub/osx-pl2303.kext.tgz
# 
# Then follow the instructions at http://robpickering.com/2013/12/enabling-a-usb-to-serial-port-adapter-under-os-x-10-9-mavericks-1623
# which are:
# shell$ tar zxvf osx-pl2303.kext.tgz
# shell$ sudo mv osx-pl2303.kext /System/Library/Extensions/
# shell$ cd /System/Library/Extensions/
# shell$ sudo chmod -R 755 osx-pl2303.kext/
# shell$ sudo chown -R root:wheel osx-pl2303.kext/
# shell$ sudo kextload ./osx-pl2303.kext
# shell$ sudo kextcache -system-cache
#
# then use shell$ ls /dev/cu* to display the device name after you plug it in.
#
# Some commands
#x = stepper.read()          # read one byte
#s = stepper.read(10)        # read up to ten bytes (timeout)
#line = stepper.readline()   # read a '\n' terminated line


#
###########################################################################
## GENERAL SETTINGS: Movement and Scaling
import os
import sys
import serial
import time

serial_port = ''
platform = sys.platform
if platform == 'win32':
    serial_port = 'COM4'
elif platform == 'darwin':
    test_serial_port = '/dev/cu.PL2303-0000103D'
    if os.path.lexists(test_serial_port):
        serial_port = test_serial_port
    else:
        test_serial_port = '/dev/cu.usbserial-000011FD'
        if os.path.lexists(test_serial_port):
            serial_port = test_serial_port
        else:
            test_serial_port = '/dev/cu.usbserial-000031FD'
            if os.path.lexists(test_serial_port):
                serial_port = test_serial_port
            else:
                test_serial_port = '/dev/cu.usbserial-001014FA'
                if os.path.lexists(test_serial_port):
                    serial_port = test_serial_port
                else:
                    test_serial_port = '/dev/cu.usbserial-001014FD'
                    if os.path.lexists(test_serial_port):
                        serial_port = test_serial_port
if serial_port == '':
    print 'The serial device that you are trying to use in StepperControl.py was NOT found under the expected paths.'
    print "check the device paths with 'ls /dev/cu*' and make sure the device is plugged." 
    print "When adding new device locations they will need to be added to this script"
    print 'killing the script'
    sys.exit()
SleepTime = 0.5

def DisableDrive():
    # Disable drive
    status = False
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'DRIVE0\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#    
def SetResolution():
    # Set drive resolution to 25,000 microsteps 
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'DRES25000\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#    
def SetScaling():
    # Set scaling so that '1' represents 1 revolution
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'SCLD25000\n')
        time.sleep(SleepTime)
        stepper.write(b'SCLV25000\n')
        time.sleep(SleepTime)
        stepper.write(b'SCLA25000\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def EnableScaling():
    # Enable Scaling
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'SCALE1\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status    
#
def DefineAxis(AxisNum=0):
    # Define axis:  0 = stepper, 1 = servo # 0 is defult
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (AxisNum == 0 or AxisNum == 1):
            stepper.write(b'AXSDEF'+str(AxisNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "AxisNum should be a 0 or 1, a number not a string. AxisNum = " +str(AxisNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def HardwareLimits(HardwareLimitNum=0):
    # Hardware End-of-Travel Limit:
    # 0 = disable limits (0 is default)
    # 1-3 = enable motion restrictions in certain directions
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (HardwareLimitNum == 0 or HardwareLimitNum == 1 or HardwareLimitNum == 2 or HardwareLimitNum == 3):
            stepper.write(b'LH'+str(HardwareLimitNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "HardwareLimitNum  should be a 0, 1, 2, or 3 a number not a string. HardwareLimitNum = " +str(HardwareLimitNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def StopBehavior(StopBehavoirNum=1):
    # Behavior on stop input or Stop command (!S):
    # 0 = discard commands in buffer and terminate program execution
    # 1 = pause command execution, continue with !C command (1 is default)
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (StopBehavoirNum == 0 or StopBehavoirNum == 1):
            stepper.write(b'COMEXS'+str(StopBehavoirNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "StopBehavoirNum  should be a 0 or 1, a number not a string. StopBehavoirNum = " +str(StopBehavoirNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def ContinuousCmdMode(ContinuousCmdNum=0):
    # Continuous command processing mode:  0 = disable (pause until motion is complete) (0 is default), 1 = enable
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (ContinuousCmdNum == 0 or ContinuousCmdNum == 1):
            stepper.write(b'COMEXC'+str(ContinuousCmdNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "ContinuousCmdNum  should be a 0 or 1, a number not a string. ContinuousCmdNum = " +str(ContinuousCmdNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def DistOrVelMode(DistOrVelNum=0):
    # Preset mode (0) = move specified distance (0 is default)
    # Continuous mode (1) = move at specified velocity
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (DistOrVelNum == 0 or DistOrVelNum == 1):
            stepper.write(b'MC'+str(DistOrVelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "DistOrVelNum  should be a 0 or 1, a number not a string. DistOrVelNumm = " +str(DistOrVelNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def IncementOrAbsolute(IncementOrAbsoluteNum=0):
    # Incremental mode (0) = move w.r.t. position at start of move (0 is default)
    # Absolute mode (1) = move w.r.t. absolute zero
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (IncementOrAbsoluteNum == 0 or IncementOrAbsoluteNum == 1):
            stepper.write(b'MA'+str(IncementOrAbsoluteNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "IncementOrAbsoluteNum  should be a 0 or 1, a number not a string. IncementOrAbsoluteNum = " +str(IncementOrAbsoluteNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def SetZero():
    # Set current position as 0
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'PSET0\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
###########################################################################
## MOTION SETTINGS:  Including: Acceleration, Velocity   
def SetAccel(AccelNum):
    # Acceleration (revolutions/s^2)
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (AccelNum <= 1):
            stepper.write(b'A'+str(AccelNum)+'\n')
            time.sleep(SleepTime)
            stepper.write(bAD+str(AccelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "AccelNum should be less than 1 and a number not a string. AccelNum = " +str(AccelNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def SetVel(VelNum):
    # Velocity (rev/s)
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (VelNum <= 1):
            stepper.write(b'V'+str(VelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "VelNum should be less than 1 and a number not a string. VelNum = " +str(VelNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def Rotate(RotateNum):
    # Set rotation distance
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        if (RotateNum <= 5):
            stepper.write(b'D'+str(RotateNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "RotateNum should be less than 5 and a number not a string. RotateNum = " +str(RotateNum)+" . Returning status = False"
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status   
#
def QuarterTurn():
    # rotation of a 1/4 turn.
    status = False    
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1)
    time.sleep(SleepTime)
    if stepper.isOpen():
        stepper.write(b'D0.25\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def initialize():
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)
    time.sleep(SleepTime)
    if stepper.isOpen():
        # Disable drive
        stepper.write(b'DRIVE0\n')
        time.sleep(SleepTime)
        # Erase any existing programs
        stepper.write(b'ERASE\n')
        time.sleep(SleepTime)
        # Set drive resolution
        stepper.write(b'DRES25000\n')
        time.sleep(SleepTime)
        # Set scaling
        stepper.write(b'SCLD25000\n')        
        time.sleep(SleepTime)
        stepper.write(b'SCLV25000\n')        
        time.sleep(SleepTime)
        stepper.write(b'SCLA25000\n')        
        time.sleep(SleepTime)
        # Enable scaling
        stepper.write(b'SCALE1\n')        
        time.sleep(SleepTime)
        # Define axis as stepper
        stepper.write(b'AXDEF0\n')
        time.sleep(SleepTime)
        # Disable hardware end-of-travel limits
        stepper.write(b'LH0\n')
        time.sleep(SleepTime)
        # Pause command execution on stop command
        stepper.write(b'COMEXS1\n')
        time.sleep(SleepTime)
        # Disable continuous command processing mode
        stepper.write(b'COMEXC0\n')
        time.sleep(SleepTime)
        # Set preset/continuous mode
        stepper.write(b'MC0\n')
        time.sleep(SleepTime)
        # Set absolute/incremental mode
        stepper.write(b'MA0\n')
        time.sleep(SleepTime)
        # Set current position as 0
        stepper.write(b'PSET0\n')
        time.sleep(SleepTime)

        # Set acceleration
        stepper.write(b'A0.5\n')
        time.sleep(SleepTime)
        # Set deceleration
        stepper.write(b'AD0.5\n')
        time.sleep(SleepTime)
        # Set velocity
        stepper.write(b'V0.5\n')
        time.sleep(SleepTime)
        # Set distance
        stepper.write(b'D0.25\n')
        time.sleep(SleepTime)
        # Enable drive
        stepper.write(b'DRIVE1\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    stepper.close()
    return status
#
def GoForth():
    status = False
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)
    time.sleep(SleepTime)
    if stepper.isOpen():
        # Set distance
        stepper.write(b'D0.25\n')
        time.sleep(SleepTime)
        # send the go command
        stepper.write(b'GO1\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"  
    return status
#
def GoBack():
    status = False
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)
    #time.sleep(SleepTime)
    if stepper.isOpen():
        # Set distance
        stepper.write(b'D-0.25\n')
        time.sleep(SleepTime)
        # send the go command
        stepper.write(b'GO1\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, return in status False"
    return status

# make commands to be executed every time the controller is started
def startup():
    status = False
    stepper = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)
    if stepper.isOpen():
        # clear the old start up program
        stepper.write(b'STARTP CLR\n')

        writestr=''
        # Define the setup function
        writestr=writestr+b'DEF SETUP\n'
        # Set drive resolution
        writestr=writestr+b'DRES25000\n'
        # Set scaling
        writestr=writestr+b'SCLD25000\n'
        writestr=writestr+b'SCLV25000\n'
        writestr=writestr+b'SCLA25000\n'
        # Enable scaling
        writestr=writestr+b'SCALE1\n'
        # Define axis as stepper
        writestr=writestr+b'AXDEF0\n'
        # Disable hardware end-of-travel limits
        writestr=writestr+b'LH0\n'
        # Pause command execution on stop command
        writestr=writestr+b'COMEXS1\n'
        # Disable continuous command processing mode
        writestr=writestr+b'COMEXC0\n'
        # Set preset/continuous mode
        writestr=writestr+b'MC0\n'
        # Set absolute/incremental mode
        writestr=writestr+b'MA0\n'
        # Set current position as 0
        writestr=writestr+b'PSET0\n'
        time.sleep(SleepTime)

        # Set acceleration
        writestr=writestr+b'A0.5\n'
        # Set deceleration
        writestr=writestr+b'AD0.5\n'
        # Set velocity
        writestr=writestr+b'V0.5\n'
        time.sleep(SleepTime)
        # Set distance
        writestr=writestr+b'D0.25\n'

        # End of the Setup program
        writestr=writestr+b'END\n'
        stepper.write(writestr)
        time.sleep(SleepTime)
        print writestr
        # Assign the program SETUP as the startup program
        stepper.write(b'STARTP SETUP\n')
        time.sleep(SleepTime)

        # reset the the controller to execute the program that was just written
        stepper.write(b'RESET\n')
        time.sleep(SleepTime)
    else:
        print "The port is not open, return in status False"
    stepper.close()



    return

def test_func():
    startup()
    time.sleep(5)
    GoForth()
    time.sleep(5)
    DisableDrive()
    return

def test2():
    initialize()
    GoForth()
    time.sleep(20)
    DisableDrive()
    return

test2()