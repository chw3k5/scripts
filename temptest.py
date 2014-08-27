# Monitor Temperatures
#Clear All variables
def clearall():
    all = [var for var in globals() if var[0] != "_"]
    for var in all:
        del globals()[var]
clearall()
###############################################################################
import serial, signal, time, os, sys, numpy
###############################################################################
# User  settings
###############################################################################
serial_port = ''
test_serial_port = '/dev/cu.usbserial-000032FD'
if os.path.lexists(test_serial_port):
    serial_port = test_serial_port
else:
    test_serial_port = '/dev/cu.usbserial-000012FD' 
    if os.path.lexists(test_serial_port):
        serial_port = test_serial_port

if serial_port == '':
    print 'The serial device that you are trying to use in monitor_temp.py was found under the expected paths.'
    print "check the device paths with 'ls /dev/cu*' and make sure the device is plugged." 
    print "When adding new device locations they will need to be added to this script"
    print 'killing the script'
    sys.exit()
# Data Folder
folder ='/Users/chw3k5/Documents/Grad_School/Kappa/temperatureData/'
#Date File Name
filename = 'Temp_cryo.csv'

max_count = 20 # in loops (set to -1 to set to infinity)
max_time  = 60 # in seconds (set to -1 to set to infinity)

meas_period      = 5.0 # in seconds
rest_time        = 0.5 # in seconds
num_of_temp2read = 3   # 
sleep_per_meas   = meas_period - 2*rest_time*num_of_temp2read
if sleep_per_meas <= 0:
    sleep_per_meas = 0
    print 'Warning: measurment period, ' + str(meas_period) +' ,is less than the time needed measure ' + str(num_of_temp2read) + ' tempertures'
    print 'with a total rest time of 2 time the rest_time=' + str(rest_time)
    print 'Measuring temperture and fast as the other parameters allow, see monitor_temp.py to change parameters'
testing = False
###############################################################################
# Connect and Configure the Instrument
###############################################################################
# configure the serial connections
lakeshore = serial.Serial(port=serial_port,
                          baudrate='9600',
                          bytesize =7 ,
                          stopbits =1, 
                          parity = 'O',                       
                          timeout= 5) # use null modem cable 
lakeshore.isOpen()
###############################################################################
# Interrupt handler 
###############################################################################
class GracefulInterruptHandler(object):
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig
    def __enter__(self):
        self.interrupted = False
        self.released = False
        self.original_handler = signal.getsignal(self.sig)
        def handler(signum, frame):
            self.release()
            self.interrupted = True
        signal.signal(self.sig, handler)
        return self
    def __exit__(self, type, value, tb):
        self.release()
    def release(self):
        if self.released:
            return False
        signal.signal(self.sig, self.original_handler)
        self.released = True
def terminate():
    print "Closing Instrument ..." 
    lakeshore.close()
###############################################################################
# Acquire Data function 
###############################################################################
def get_temp(n):
     lakeshore.write(b'KRDG? ' + str(n) + '\n')
     #wait some time before reading output.
     time.sleep(rest_time)
     #pdata = ''
     data  = ''
     while (lakeshore.inWaiting() > 0) :
         data   +=  lakeshore.read(1)
         #leybold.write('COM,1\r\n')
     time.sleep(rest_time)
     #print data
     if ( len(data)  > 2) or (data != '') :
         data  = data.rsplit(',')
         data  = data[0].split('+')
         data  = data[1].split('\r\n')
         temp  = data[0]#numpy.float(data[1])    	
     else:
         temp = 0
     return temp 
###############################################################################
# Initialize Data File
###############################################################################

#start new file
datafile=open(folder+filename ,'w')
line2write = "time,temp2,temp3,temp4"
datafile.write(line2write + '\n')

###############################################################################
# Measurement Loop
###############################################################################
with GracefulInterruptHandler() as h:
    finished = False
    count = 0
    start_time = time.time()
    alldata = []
    while not finished:
        run_time = time.time() - start_time
        count = count + 1
        if testing:
            n=2
            lakeshore.write(b'KRDG? ' + str(n) + '\n')
            #wait some time before reading output.
            time.sleep(rest_time)
            #pdata = ''
            data1  = ''
            while (lakeshore.inWaiting() > 0) :
                data1   +=  lakeshore.read(1)
                #leybold.write('COM,1\r\n')
                time.sleep(rest_time)
                #print data
                alldata.append(data1)
            if ( len(data1)  > 2) or (data1 != '') :
                data2  = data1.rsplit(',')
                data3  = data2[0].split('+')
                data4  = data3[1].split('\r\n')
                temp   = data4[0]#numpy.float(data[1])    	
            else:
                temp = 0
            temp2 = temp
            temp3 = 99
            temp4 = 999 
        else:
            temp2 = get_temp(2)
            temp3 = get_temp(3)
            temp4 = get_temp(4)
        
        time.sleep(sleep_per_meas)
        #print "%s  %s   %f %f %f"%(time.time(),time.strftime("%a, %d %b %Y %H:%M:%S "),temp2, temp3, temp4) #,pressure)
        #datafile.write("%s %s  %f %f %f \n"%(time.time(),time.strftime("%a, %d %b %Y %H:%M:%S "),temp2,temp3,temp4)) #,pressure))
        line2write = str(time.time()) + ',' + str(temp2) + ',' + str(temp3) + ',' + str(temp4)
        print line2write
        datafile.write(line2write + '\n')
        if h.interrupted:
            print " Interrupted ... Exiting gracefully"
            terminate()
            #break # Break the loop
            finished = True
        elif ((max_count < count) and (max_count != -1)):
            print " max_count = "+str(max_count) + "  has been exceeded, exiting the script"
            terminate()
            #break # Break the loop
            finished = True
        elif ((max_time < run_time) and (max_time != -1)):
            print " max_time = " + str(max_time) + "  has been exceeded, exiting the script"
            terminate()
            #break # Break the loop
            finished = True
            
if h.interrupted == False:
    terminate()