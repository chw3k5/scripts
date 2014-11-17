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
#x = st.read()          # read one byte
#s = st.read(10)        # read up to ten bytes (timeout)
#line = st.readline()   # read a '\n' terminated line


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
    serial_port = 'COM7'
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
    print 'The serial device that you are trying to use in stControl.py was NOT found under the expected paths.'
    print "check the device paths with 'ls /dev/cu*' (mac only) and make sure the device is plugged into the computer."
    print "When adding new device locations they will need to be added to this script"
    print 'killing the script'
    sys.exit()
SleepTime = 1.3
initialize_sleep = 5

st = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)


##################################
###### Standard Definitions ######
##################################

def DisableDrive():
    # Disable drive
    status = False
    if st.isOpen():
        st.write(b'DRIVE0\n')
        status = True
    else:
        print "The port is not open, returning status False"
    return status

def initialize(vel=1, accel=0.5, verbose=True):
    if st.isOpen():
        write_str = ''
        # Set drive resolution
        write_str += 'DRES25000\n'
        # Enable scaling
        write_str += 'SCALE1\n'
        # Set scaling
        write_str += 'SCLD25000\n'
        write_str += 'SCLV25000\n'
        write_str += 'SCLA25000\n'

        # Define axis as st
        write_str += 'AXDEF0\n'
        # Disable hardware end-of-travel limits
        write_str += 'LH0\n'
        # Pause command execution on stop command
        write_str += 'COMEXS1\n'
        # Disable continuous command processing mode
        write_str += 'COMEXC0\n'

        # Set preset/continuous mode
        #write_str += 'MC0\n'
        # Set absolute/incremental mode
        #write_str += 'MA0\n'
        # Set current position as 0
        #write_str += 'PSET0\n'

        ### Set Accelerations ###
        accel_str = str(accel)
        half_accel_str = str(accel/2.0)
        if verbose:
            print accel_str, '= acceleration string'
            print half_accel_str, '= half acceleration string'

        # acceleration
        write_str += 'A' + accel_str + '\n'
        # average acceleration (to determine 'S' curve shape)
        write_str += 'AA' + half_accel_str + '\n'
        # Set deceleration
        write_str += 'AD' + accel_str + '\n'
        # set average decoration
        write_str += 'ADA' + half_accel_str + '\n'

        ### Set Velocity ###
        vel_str = str(vel)
        write_str += 'V' + vel_str + '\n'
        if verbose:
            print vel, '= velocity string'

        # Enable drive
        #write_str = write_str + 'DRIVE1\n'
        st.write(write_str)
        time.sleep(initialize_sleep)

        status = True
    else:
        print "The port is not open, returning status False"
        status = False
    return status
#
def GoForth(dist='0.25'):
    status = False
    if st.isOpen():
        write_str = ''
        # Enable drive
        write_str += 'DRIVE1\n'
        # Set distance
        write_str += 'D'+str(dist)+'\n'
        # send the go command
        write_str += 'GO1\n'
        st.write(write_str)
        time.sleep(SleepTime)
        status = DisableDrive()
    else:
        print "The port is not open, returning status False"
    return status
#
def GoBack(dist='0.25'):
    status = False
    #time.sleep(SleepTime)
    if st.isOpen():
        write_str = ''
        # Enable drive
        write_str += 'DRIVE1\n'
        # Set distance
        write_str += 'D-'+str(dist)+'\n'
        # send the go command
        write_str += 'GO1\n'
        st.write(write_str)
        time.sleep(SleepTime)
        status = DisableDrive()
    else:
        print "The port is not open, returning status False"
    return status



def stepper_close():
    st.close()
    return

def reader():
    st.write(b'STARTP\n')
    char = 1
    string = ''
    while char:
        char = st.readline()
        string = string + char
        print string
    return



################################
###### Unused Definitions ######
################################

def SetResolution():
    # Set drive resolution to 25,000 microsteps 
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        st.write(b'DRES25000\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, returning status False"
    return status
#    
def SetScaling():
    # Set scaling so that '1' represents 1 revolution
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        st.write(b'SCLD25000\n')
        time.sleep(SleepTime)
        st.write(b'SCLV25000\n')
        time.sleep(SleepTime)
        st.write(b'SCLA25000\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, returning status False"
    return status
#
def EnableScaling():
    # Enable Scaling
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        st.write(b'SCALE1\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, returning status False"
    return status    
#
def DefineAxis(AxisNum=0):
    # Define axis:  0 = st, 1 = servo # 0 is defult
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (AxisNum == 0 or AxisNum == 1):
            st.write(b'AXSDEF'+str(AxisNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "AxisNum should be a 0 or 1, a number not a string. AxisNum = " +str(AxisNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def HardwareLimits(HardwareLimitNum=0):
    # Hardware End-of-Travel Limit:
    # 0 = disable limits (0 is default)
    # 1-3 = enable motion restrictions in certain directions
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (HardwareLimitNum == 0 or HardwareLimitNum == 1 or HardwareLimitNum == 2 or HardwareLimitNum == 3):
            st.write(b'LH'+str(HardwareLimitNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "HardwareLimitNum  should be a 0, 1, 2, or 3 a number not a string. HardwareLimitNum = " +str(HardwareLimitNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def StopBehavior(StopBehavoirNum=1):
    # Behavior on stop input or Stop command (!S):
    # 0 = discard commands in buffer and terminate program execution
    # 1 = pause command execution, continue with !C command (1 is default)
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (StopBehavoirNum == 0 or StopBehavoirNum == 1):
            st.write(b'COMEXS'+str(StopBehavoirNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "StopBehavoirNum  should be a 0 or 1, a number not a string. StopBehavoirNum = " +str(StopBehavoirNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def ContinuousCmdMode(ContinuousCmdNum=0):
    # Continuous command processing mode:  0 = disable (pause until motion is complete) (0 is default), 1 = enable
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (ContinuousCmdNum == 0 or ContinuousCmdNum == 1):
            st.write(b'COMEXC'+str(ContinuousCmdNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "ContinuousCmdNum  should be a 0 or 1, a number not a string. ContinuousCmdNum = " +str(ContinuousCmdNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def DistOrVelMode(DistOrVelNum=0):
    # Preset mode (0) = move specified distance (0 is default)
    # Continuous mode (1) = move at specified velocity
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (DistOrVelNum == 0 or DistOrVelNum == 1):
            st.write(b'MC'+str(DistOrVelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "DistOrVelNum  should be a 0 or 1, a number not a string. DistOrVelNumm = " +str(DistOrVelNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def IncementOrAbsolute(IncementOrAbsoluteNum=0):
    # Incremental mode (0) = move w.r.t. position at start of move (0 is default)
    # Absolute mode (1) = move w.r.t. absolute zero
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (IncementOrAbsoluteNum == 0 or IncementOrAbsoluteNum == 1):
            st.write(b'MA'+str(IncementOrAbsoluteNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "IncementOrAbsoluteNum  should be a 0 or 1, a number not a string. IncementOrAbsoluteNum = " +str(IncementOrAbsoluteNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def SetZero():
    # Set current position as 0
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        st.write(b'PSET0\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, returning status False"
    return status
###########################################################################
## MOTION SETTINGS:  Including: Acceleration, Velocity   
def SetAccel(AccelNum):
    # Acceleration (revolutions/s^2)
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (AccelNum <= 1):
            st.write(b'A'+str(AccelNum)+'\n')
            time.sleep(SleepTime)
            st.write(b'AD'+str(AccelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "AccelNum should be less than 1 and a number not a string. AccelNum = " +str(AccelNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def SetVel(VelNum):
    # Velocity (rev/s)
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (VelNum <= 1):
            st.write(b'V'+str(VelNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "VelNum should be less than 1 and a number not a string. VelNum = " +str(VelNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status
#
def Rotate(RotateNum):
    # Set rotation distance
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        if (RotateNum <= 5):
            st.write(b'D'+str(RotateNum)+'\n')
            time.sleep(SleepTime)
            status = True
        else:
            print "RotateNum should be less than 5 and a number not a string. RotateNum = " +str(RotateNum)+" . Returning status = False"
    else:
        print "The port is not open, returning status False"
    return status   
#
def QuarterTurn():
    # rotation of a 1/4 turn.
    status = False
    time.sleep(SleepTime)
    if st.isOpen():
        st.write(b'D0.25\n')
        time.sleep(SleepTime)
        status = True
    else:
        print "The port is not open, returning status False"
    return status
#


# make commands to be executed every time the controller is started
# def startup():
#     status = False
#     st = serial.Serial(port=serial_port, baudrate=9600, bytesize=8, stopbits=1, timeout=2)
#     if st.isOpen():
#         # clear the old start up program
#         st.write(b'STARTP CLR\n')
#
#         writestr=''
#         # Define the setup function
#         writestr=writestr+b'DEF SETUP\n'
#         # Set drive resolution
#         writestr=writestr+b'DRES25000\n'
#         # Set scaling
#         writestr=writestr+b'SCLD25000\n'
#         writestr=writestr+b'SCLV25000\n'
#         writestr=writestr+b'SCLA25000\n'
#         # Enable scaling
#         writestr=writestr+b'SCALE1\n'
#         # Define axis as st
#         writestr=writestr+b'AXDEF0\n'
#         # Disable hardware end-of-travel limits
#         writestr=writestr+b'LH0\n'
#         # Pause command execution on stop command
#         writestr=writestr+b'COMEXS1\n'
#         # Disable continuous command processing mode
#         writestr=writestr+b'COMEXC0\n'
#         # Set preset/continuous mode
#         writestr=writestr+b'MC0\n'
#         # Set absolute/incremental mode
#         writestr=writestr+b'MA0\n'
#         # Set current position as 0
#         writestr=writestr+b'PSET0\n'
#         time.sleep(SleepTime)
#
#         # Set acceleration
#         writestr=writestr+b'A0.1\n'
#         # Set deceleration
#         writestr=writestr+b'AD0.1\n'
#         # Set velocity
#         writestr=writestr+b'V0.1\n'
#         time.sleep(SleepTime)
#         # Set distance
#         writestr=writestr+b'D0.25\n'
#
#         # End of the Setup program
#         writestr=writestr+b'END\n'
#         st.write(writestr)
#         time.sleep(SleepTime)
#         print writestr
#         # Assign the program SETUP as the startup program
#         st.write(b'STARTP SETUP\n')
#         time.sleep(SleepTime)
#
#         # reset the the controller to execute the program that was just written
#         st.write(b'RESET\n')
#         time.sleep(SleepTime)
#     else:
#         print "The port is not open, returning status False"
#
#
#     return



def test(test_num=10,move_sleep=1, vel=0.2, accel=0.2,forth_dist='0.20',back_dist='0.30', verbose=True):
    initialize(vel=vel, accel=accel, verbose=verbose)
    for n in range(test_num):
        GoForth(dist=forth_dist)
        time.sleep(move_sleep)

        GoBack(dist=back_dist)
        time.sleep(move_sleep)
    stepper_close()
    return

#test(test_num=100, move_sleep=2, vel=0.5, accel=1, forth_dist='0.25',back_dist='0.25', verbose=True)

