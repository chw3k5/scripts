# This script was written by Hamdi Mani, and then reworked by Caleb Wheeler,
# Caleb left some thing in because he didn't know what they did or how they 
# were controlled. Sorry in advance.
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
###############################################################################
# Monitor Temperatures
#Clear All variables
def clearall():
    all = [var for var in globals() if var[0] != "_"]
    for var in all:
        del globals()[var]
clearall()
###############################################################################
import serial, signal, time, os, sys, atpy, numpy, matplotlib
from matplotlib import pyplot as plt
from email_sender   import email_caleb, email_groppi, text_caleb

###############################################################################
# User  settings
###############################################################################
platform = sys.platform

serial_port = ''

if platform == 'win32':
    serial_port = 'COM3'
elif platform == 'darwin':
    test_serial_port = '/dev/cu.usbserial-000032FD'
    if os.path.lexists(test_serial_port):
        serial_port = test_serial_port
    else:
        test_serial_port = '/dev/cu.usbserial-000012FD'
        if os.path.lexists(test_serial_port):
            serial_port = test_serial_port
        else:
            test_serial_port = '/dev/cu.usbserial-002013FD'
            if os.path.lexists(test_serial_port):
                serial_port = test_serial_port
            else:
                test_serial_port = '/dev/cu.usbserial-002014FA'
                if os.path.lexists(test_serial_port):
                    serial_port = test_serial_port
if serial_port == '':
    print 'The serial device that you are trying to use in monitor_temp.py was Not found under the expected paths.'
    print "check the device paths with 'ls /dev/cu*' and make sure the device is plugged." 
    print "When adding new device locations they will need to be added to this script"
    print 'killing the script'
    sys.exit()
    
verbose = True
# Data Folder
if platform == 'win32':
    folder = 'C:\\Users\\MtDewar\\Documents\\Kappa\\temperatureData\\'
elif platform == 'darwin':
    folder ='/Users/chw3k5/Documents/Grad_School/Kappa/temperatureData/'
#Date File Name
filename = 'temperatures5.csv'

max_count = 5 # in loops (set to -1 to set to infinity)
max_time  = 60 # in seconds (set to -1 to set to infinity)

monitor_time  = 3*7*24*60*60 # in seconds (This is the total time that is scrip will monitor temperatures from the lakeshore)
monitor_sleep = 5*60   # in seconds

Nsecs        =  24*60*60 # in second (look at data and do statistics on the last Nhours of data collection)

PeriodicEmail = True
seconds_per_email = 9*60*60 #12*60*60 # in seconds

high_alarm_temperature = 4.3 # in Kelvin
low_alarm_temperature  = 0 # in Kelvin

meas_period      = 7.0 # in seconds
rest_time        = 0.5 # in seconds
num_of_temp2read = 6   # 
sleep_per_meas   = meas_period - 2*rest_time*num_of_temp2read
if sleep_per_meas <= 0:
    sleep_per_meas = 0
    print 'Warning: measurement period, ' + str(meas_period) +' ,is less than the time needed measure ' + str(num_of_temp2read) + ' tempertures'
    print 'with a total rest time of ' + str(rest_time*2) + ' equal to 2 times the rest_time=' + str(rest_time)
    print 'Measuring temperature and fast as the other parameters allow, see monitor_temp.py to change parameters'
testing = False


###############################################################################
###### Start the giant while loop that periodically measures temperature ######
###############################################################################
alarm = False
monitoring = True
start_monitor_time = time.time()
Email_time = start_monitor_time
EmailTrigger = True
while monitoring:
    current_time = time.time()
    if monitor_time < current_time - start_monitor_time:
        monitoring = False
    else:
        ###############################################################################
        # Connect and Configure the Instrument
        ###############################################################################
        # configure the serial connections
        lakeshore = serial.Serial(port=serial_port, baudrate='9600', bytesize =7, stopbits =1, parity = 'O', timeout= 5) # use null modem cable 
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
            if verbose:
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
            
        # turn all of this into a function
        def checkTemps():
            # Open and create the file if necessary
            if os.path.lexists(folder+filename):
                writefile=open(folder+filename, 'a')
            else:
                writefile=open(folder+filename, 'w')
                line2write = "time,temp2,temp3,temp4"
                writefile.write(line2write + '\n')
            ###############################################################################
            # Read Temperatures and append them to the data file
            ###############################################################################
            with GracefulInterruptHandler() as h:
                finished = False
                count = 0
                start_time = time.time()
                while not finished:
                    run_time = time.time() - start_time
                    count = count + 1
                    temp2 = get_temp(2)
                    temp3 = get_temp(3)
                    temp4 = get_temp(4)
            
                    time.sleep(sleep_per_meas)

                    line2write = str(time.time()) + ',' + str(temp2) + ',' + str(temp3) + ',' + str(temp4) \

                    if verbose:
                        print line2write
                    writefile.write(line2write + '\n')
                    if h.interrupted:
                        print " Interrupted ... Exiting gracefully"
                        terminate()
                        finished = True
                    elif ((max_count <= count) and (max_count != -1)):
                        if verbose:
                            print " max_count = "+str(max_count) + " has been exceeded, exiting the script"
                        #terminate()
                        finished = True
                    elif ((max_time < run_time) and (max_time != -1)):
                        if verbose:
                            print " max_time = " + str(max_time) + " seconds has been exceeded, exiting the measurment loop"
                        #terminate()
                        finished = True
            writefile.close()
            if h.interrupted == False:
                terminate()
            return
        
        ### now the definitions are over, the fun starts now
        checkTemps()
        Nhours = float(Nsecs)/3600.0
        data  = atpy.Table(folder + filename, type="ascii", delimiter=",")
        Ttime = data.time
        temp2 = data.temp2
        temp3 = data.temp3
        temp4 = data.temp4

        # cut data to the last Nsecs
        start_last_Nsecs = 0
        current_time = time.time()
        for time_index in reversed(range(len(Ttime))):
            if current_time - Ttime[time_index] <= Nsecs:
                start_last_Nsecs = time_index
        
        # make the start time of the data be 0 hours
        Ttime = Ttime - Ttime[0]
        
        # divide Ttime to change units from seconds to hours
        Ttime = Ttime/(3600.0)
        totalhours = float(Ttime[len(Ttime)-1])
        # get the time of the last Necs and set that value to zero for those plots
        Time_Nsecs = Ttime[start_last_Nsecs:] - Ttime[start_last_Nsecs]

        temp2_mean    = numpy.mean(temp2)
        Nsecs_mean2   = numpy.mean(temp2[start_last_Nsecs:])
        temp2_std     = numpy.std(temp2)
        Nsecs_std2    = numpy.std(temp2)
        current_temp2 = temp2[len(temp2)-1]
        
        temp3_mean    = numpy.mean(temp3)
        Nsecs_mean3   = numpy.mean(temp3[start_last_Nsecs:])
        temp3_std     = numpy.std(temp3)
        Nsecs_std3    = numpy.std(temp3)
        current_temp3 = temp3[len(temp3)-1]
        
        temp4_mean    = numpy.mean(temp4)
        Nsecs_mean4   = numpy.mean(temp4[start_last_Nsecs:])
        temp4_std     = numpy.std(temp4)
        Nsecs_std4    = numpy.std(temp4)
        current_temp4 = temp4[len(temp4)-1]

        
        if high_alarm_temperature < current_temp4:
            alarm = True
        if current_temp4 < low_alarm_temperature:
            alarm = True
        else:
            alarm = False
        ###################
        ### send emails ###
        ###################
        if PeriodicEmail:
            ElapsedEmailTime = current_time - Email_time
            if seconds_per_email < ElapsedEmailTime:
                EmailTrigger = True
        if alarm:
            alarm_subject = "CRYOSTAT ALARM - " + str('%2.3f' % current_temp4) + "K"
            print alarm_subject
            
            alarm_body_text = ''
            alarm_body_text = alarm_body_text + "RECEIVER TEMP = " + str('%2.3f' % current_temp4) + "K\nlast " \
            + str('%2.2f' % Nhours) + " hours (mean, std) = (" + str('%2.3f' % Nsecs_mean4) + 'K, ' + str('%2.3f' % Nsecs_std4) + "K)\n" \
            + "all measurements " + str('%3.2f' % totalhours) + " hours (mean, std) = (" + str('%2.3f' % temp4_mean) \
            + 'K, ' + str('%2.3f' % temp4_std) + "K)\n\n" \
            + "INNER SHIELD = " + str('%2.3f' % current_temp2) + "K\nlast " \
            + str('%2.2f' % Nhours) +" hours (mean, std) = (" + str('%2.3f' % Nsecs_mean2) + 'K, ' + str('%2.3f' % Nsecs_std2) \
            + "K)\nall measurements " + str('%3.2f' % totalhours) + " hours (mean, std) = (" + str('%2.3f' % temp2_mean) \
            + 'K, ' + str('%2.3f' % temp2_std) + "K)\n\n" \
            + "OUTER SHIELD = " + str('%2.3f' % current_temp3) + "K\nlast " + str('%2.2f' % Nhours) +" hours (mean, std) = ("\
            + str('%2.3f' % Nsecs_mean3) + 'K, ' + str('%2.3f' % Nsecs_std3) + "K)\nall measurements " + str('%3.2f' % totalhours)\
            + " hours (mean, std) = (" + str('%2.3f' % temp3_mean) + 'K, ' + str('%2.3f' % temp3_std) + "K)\n\n" 
            
            email_caleb(alarm_subject, alarm_body_text)
            text_caleb(alarm_subject)
            #email_groppi(alarm_subject, alarm_body_text)
        else:
            if EmailTrigger:
                subject = "periodic cryostat update - " + str('%2.3f' % current_temp4) + "K"            
                body_text = ''
                body_text = body_text + "Receiver temp = " + str('%2.3f' % current_temp4) + "K\nlast " 
                body_text = body_text + str('%2.2f' % Nhours) +" hours (mean, std) = ("
                body_text = body_text + str('%2.3f' % Nsecs_mean4) + 'K, ' + str('%2.3f' % Nsecs_std4)
                body_text = body_text + "K)\nall measurements " + str('%3.2f' % totalhours) 
                body_text = body_text + " hours (mean, std) = (" + str('%2.3f' % temp4_mean) 
                body_text = body_text + 'K, ' + str('%2.3f' % temp4_std) + "K)\n\n" 
            
                body_text = body_text + "Inner shield = " + str('%2.3f' % current_temp2) + "K\nlast " 
                body_text = body_text + str('%2.2f' % Nhours) +" hours (mean, std) = (" 
                body_text = body_text + str('%2.3f' % Nsecs_mean2) + 'K, ' + str('%2.3f' % Nsecs_std2) 
                body_text = body_text + "K)\nall measurements " + str('%3.2f' % totalhours) 
                body_text = body_text + " hours (mean, std) = (" + str('%2.3f' % temp2_mean) 
                body_text = body_text + 'K, ' + str('%2.3f' % temp2_std) + "K)\n\n" 
                
                body_text = body_text + "Outer shield = " + str('%2.3f' % current_temp3) + "K\nlast " 
                body_text = body_text + str('%2.2f' % Nhours) +" hours (mean, std) = (" 
                body_text = body_text + str('%2.3f' % Nsecs_mean3) + 'K, ' + str('%2.3f' % Nsecs_std3) 
                body_text = body_text + "K)\nall measurements " + str('%3.2f' % totalhours) 
                body_text = body_text + " hours (mean, std) = (" + str('%2.3f' % temp3_mean) 
                body_text = body_text + 'K, ' + str('%2.3f' % temp2_std) + "K)\n\n"
                
                email_caleb(subject, body_text)
                Email_time = current_time
                EmailTrigger = False
            
        
        #######################
        ### make some plots ###
        #######################
        # Caleb's data, all the data
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = 10.0
        fig, ax1 = plt.subplots()
        
        plotcolor = "blue"
        ax1.plot(Ttime, temp4, color=plotcolor, linewidth=3)
        line1 = plt.Line2D(range(10), range(10), color=plotcolor)
        plotcolor = "green"
        ax1.plot(Ttime, temp3, color=plotcolor, linewidth=3)
        line2 = plt.Line2D(range(10), range(10), color=plotcolor)
        plotcolor = "red"
        ax1.plot(Ttime, temp2 , color=plotcolor, linewidth=3)
        line3 = plt.Line2D(range(10), range(10), color=plotcolor)
        
        ax1.set_xlabel('hours since start')
        ax1.set_ylabel('Temperature (K)')
        plt.legend((line1,line2, line3),('receiver','Inner shield', 'Outer shield'),numpoints=1, loc=2)
        plt.savefig(folder + "Alltempdata_Caleb.png")
        
        
        # Caleb's data, last Nsecs
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = 10.0
        fig, ax1 = plt.subplots()
        plotcolor = "blue"
        ax1.plot(Time_Nsecs, temp4[start_last_Nsecs:], color=plotcolor, linewidth=3)
        line1 = plt.Line2D(range(10), range(10), color=plotcolor)
        plotcolor = "green"
        ax1.plot(Time_Nsecs, temp3[start_last_Nsecs:], color=plotcolor, linewidth=3)
        line2 = plt.Line2D(range(10), range(10), color=plotcolor)
        plotcolor = "red"
        ax1.plot(Time_Nsecs, temp2[start_last_Nsecs:] , color=plotcolor, linewidth=3)
        line3 = plt.Line2D(range(10), range(10), color=plotcolor)
        
        ax1.set_xlabel('The last ' + str('%2.2f' % Nhours) + ' hours')
        ax1.set_ylabel('Temperature (K)')
        plt.legend((line1,line2, line3),('receiver','Inner shield', 'Outer shield'),numpoints=1, loc=2)
        plt.savefig(folder + str(Nsecs) +"secs_Caleb.png")
        
        # Caleb's receiver data, all the data
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = 10.0
        fig, ax1 = plt.subplots()
        plotcolor = "blue"
        ax1.plot(Ttime, temp4, color=plotcolor, linewidth=3)
        ax1.set_xlabel('hours since start')
        ax1.set_ylabel('Temperature (K)')
        plt.savefig(folder + "receiverdata_Caleb.png")
        
        # Caleb's receiver data, last Nsecs
        plt.clf()
        matplotlib.rcParams['legend.fontsize'] = 10.0
        fig, ax1 = plt.subplots()
        plotcolor = "blue"
        ax1.set_xlabel('The last ' + str('%2.2f' % Nhours) + ' hours')
        ax1.set_ylabel('Temperature (K)')
        ax1.plot(Time_Nsecs, temp4[start_last_Nsecs:], color=plotcolor, linewidth=3)
        plt.savefig(folder + str(Nsecs) +"secs_receiver.png")
        
        plt.close("all")
        ### end plotting
        
        time.sleep(monitor_sleep)
    
    