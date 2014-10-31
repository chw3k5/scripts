import sys
import serial

serial_port = None
test_serial_ports = ['/dev/cu.usbserial-fa141',
                     '/dev/cu.usbserial-fd131']
for test_serial_port in test_serial_ports:
    if os.path.lexists(test_serial_port):
        serial_port = test_serial_port
        break

if serial_port is None:
    print "agilent_multimeter.py did not find the serial instrument at the ports:", test_serial_ports
    print "Use 'ls /dev/cu*' to see what devices you have plugged in to this computer vs what device this computer was looking for."
    print "Killing the program"
    sys.exit()

