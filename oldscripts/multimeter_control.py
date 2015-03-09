__author__ = 'chwheele'
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


###########################################################################
## GENERAL SETTINGS: Movement and Scaling
from sys import platform
import os
import serial
import time

serial_port = ''
if platform == 'win32':
    serial_port = 'COM9'
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
    raise NameError("no serial port specified")
SleepTime = 1.3
initialize_sleep = 5

multimeter = serial.Serial(port=serial_port, baudrate=9600, parity='E', bytesize=7, stopbits=2, timeout=2, rtscts=True)


def measureI():
    if not multimeter.isOpen():
        multimeter.open()

    #print 'here2'
    # Reset the device
    #multimeter.write("*RST\n")
    #time.sleep(0.2)

    #print 'here3'
    # Device Clear
    #multimeter.write("*abort\n")
    #time.sleep(0.2)


    # Configure the device
    #print 'here5'
    #multimeter.write("CONFIGURE:CURR:DC\n")
    #time.sleep(0.2)

    #function = "CURRENT"
    #print 'here5'
    #multimeter.write("FUNCTION " + "\"" + function + "\""+"\n")
    #time.sleep(0.2)


    #multimeter.write("VOLT:IMP:AUTO ON\n")
    #time.sleep(1)
    #print 'here5'
    multimeter.write("SYST:REM\n")
    time.sleep(0.2)
    print 'here6'
    multimeter.write("MEAS:VOLT:DC?\n")
    print 'here7'
    time.sleep(0.5)


    return_string = multimeter.readline()
    print return_string,' return string'
    return_string = multimeter.readline()
    print return_string,' return string'

    #mutimeter.write(b'TRIG:SOUR IMM\n')
    #multimeter.write(b'read?\n')
    #print 'here'

    multimeter.close()
    return

print 'here1'
measureI()
print "finished"


