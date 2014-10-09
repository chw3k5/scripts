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
###############################################################################



def clearall():
    all = [var for var in globals() if var[0] != "_"]
    for var in all:
        del globals()[var]
clearall()

def GenEmailText(temp_data, Nhours, totalhours):


    hours_format_str = '%3.1f'
    temps_format_str = '%2.3f'

    body_text = ''

    for single_data in temp_data:
        monitor_num   = single_data[0]
        current_temp  = single_data[1]
        alldata_mean  = single_data[2]
        alldata_std   = single_data[3]
        Nsecdata_mean = single_data[4]
        Nsecdata_std  = single_data[5]

        if monitor_num == 4:
            body_text += "Receiver temp = "
        elif monitor_num == 3:
            body_text += "Outer shield  = "
        elif monitor_num == 2:
            body_text += "Inner shield  = "
        else:
            body_text += "Monitor " + str(monitor_num) + " = "

        current_temp_str = str(temps_format_str % current_temp) + "K\n"

        Nhours_temp_str  = "Over the last " + str(hours_format_str % Nhours) + " hours:\n"
        Nhours_temp_str += str(temps_format_str % Nsecdata_mean) + " K  (" + str(temps_format_str % Nsecdata_std) + ") K\n"

        all_temp_str  = "Over the length of the temperature file " + str(hours_format_str % totalhours) + " hours:\n"
        all_temp_str += str(temps_format_str % alldata_mean) + " K  (" + str(temps_format_str % alldata_std) + ") K\n"

        body_text += current_temp_str + Nhours_temp_str + all_temp_str + '\n'


    return body_text



###############################################################################
# User  settings
###############################################################################
from sys import platform
import serial, signal, time, os, sys, atpy, numpy, matplotlib
from matplotlib import pyplot as plt
from email_sender   import email_caleb, email_groppi, text_caleb
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
    folder = 'C:\\Users\\MtDewar\\Documents\\Kappa\\temperatureData\\Sep06_2014\\'
elif platform == 'darwin':
    folder ='/Users/chw3k5/Documents/Grad_School/Kappa/temperatureData/Sep06_2014\\'


monitor_type = 'cold' # options: 'coolpumpon', 'coolpumpoff', 'LN2fill', 'LHefill', 'almostcold', 'cold', 'fastwarm', 'slowwarm'
meas_period      = 7.0 # in seconds
rest_time        = 0.5 # in seconds
channels = [4,2,3]


if monitor_type=='coolpumpon':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 1*24*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 5*60   # in seconds
    Nsecs        =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email = 20*60 #12*60*60 # in seconds
    alarm_channel = 2
    high_alarm_temperature = 300. # in Kelvin
    low_alarm_temperature  = 80. # in Kelvin
elif monitor_type=='coolpumpoff':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 1*24*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 5*60   # in seconds
    Nsecs        =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email = 60*60 #12*60*60 # in seconds
    alarm_channel = 4
    high_alarm_temperature = 300. # in Kelvin
    low_alarm_temperature  =  80. # in Kelvin
elif monitor_type == 'LN2fill':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 6*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 2*60   # in seconds
    Nsecs         =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = False
    PeriodicEmail = False
    seconds_per_email      = 20*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 300. # in Kelvin
    low_alarm_temperature  =  80. # in Kelvin
elif monitor_type == 'LHefill':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 6*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 2*60   # in seconds
    Nsecs         =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = False
    PeriodicEmail = False
    seconds_per_email      = 20*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 110. # in Kelvin
    low_alarm_temperature  =   3. # in Kelvin
elif monitor_type == 'almostcold':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 7*24*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 10*60   # in seconds
    Nsecs         =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email      = 1*60*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 4.500 # in Kelvin
    low_alarm_temperature  = 3. # in Kelvin
elif monitor_type == 'cold':
    filename      = monitor_type+'.csv'
    make_plots    = False
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 4*24*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 10*60   # in seconds
    Nsecs         =  1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email      = 4*60*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 4.300 # in Kelvin
    low_alarm_temperature  = 3. # in Kelvin
elif monitor_type == 'fastwarm':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 1*25*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 5*60   # in seconds
    Nsecs         = 1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email      = 8*60*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 300. # in Kelvin
    low_alarm_temperature  =  80. # in Kelvin
elif monitor_type == 'slowwarm':
    filename      = monitor_type+'.csv'
    make_plots    = True
    max_count     = 5 # in loops (set to -1 to set to infinity)
    max_time      = 60 # in seconds (set to -1 to set to infinity)
    monitor_time  = 4*24*60*60 # in seconds (This is the total time that is script will monitor temperatures from the Lakeshore monitor)
    monitor_sleep = 10*60   # in seconds
    Nsecs         = 1*60*60 # in second (look at data and do statistics on the last Nhours of data collection)
    start_email   = True
    PeriodicEmail = True
    seconds_per_email      = 8*60*60 #12*60*60 # in seconds
    alarm_channel          = 4
    high_alarm_temperature = 300. # in Kelvin
    low_alarm_temperature  =  80. # in Kelvin



num_of_temp2read = len(channels) #
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

# make the directory for the temperature data
if not os.path.isdir(folder):
    os.makedirs(folder)

monitoring = True
start_monitor_time = time.time()
Email_time = start_monitor_time
if start_email:
    EmailTrigger = True
else:
    EmailTrigger = False

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
        def checkTemps(channels):
            # Open and create the file if necessary
            if os.path.lexists(folder+filename):
                writefile=open(folder+filename, 'a')
            else:
                writefile=open(folder+filename, 'w')
                line2write = "time,"
                for chan_index in range(len(channels)-1):
                    line2write += "temp"+str(channels[chan_index])+","
                line2write += "temp"+str(channels[-1])
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
                    temps = []
                    for channel in channels:
                        temp = get_temp(channel)
                        temps.append(temp)
                    time.sleep(sleep_per_meas)

                    line2write = str(time.time()) + ','
                    for temp_index in range(len(temps)-1):
                        line2write += str(temps[temp_index]) + ','
                    line2write += str(temps[-1])

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
        checkTemps(channels)
        Nhours = float(Nsecs)/3600.0
        data  = atpy.Table(folder + filename, type="ascii", delimiter=",")
        Ttime = data.time

        temps = []
        for channel in channels:
            if channel == 1:
                temp = (1,data.temp1)
            elif channel == 2:
                temp = (2,data.temp2)
            elif channel == 3:
                temp = (3,data.temp3)
            elif channel == 4:
                temp = (4,data.temp4)
            elif channel == 5:
                temp = (5,data.temp5)
            elif channel == 6:
                temp = (6,data.temp6)
            elif channel == 7:
                temp = (7,data.temp7)
            elif channel == 8:
                temp = (8,data.temp8)
            else:
                print "channels can only be integers 1-8"
                print "this was not expected:", channel
                print "Killing script"
                sys.exit()
            temps.append(temp)


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
        temps_wstats = []
        alarm_monitor = None
        for temp in temps:
            channel   = temp[0]
            temp_data = temp[1]

            current_temp = temp_data[-1]
            if channel == alarm_channel:
                alarm_monitor = current_temp

            temp_mean    = numpy.mean(temp_data)
            temp_std     = numpy.std(temp_data)

            Nsecs_temp_data = temp_data[start_last_Nsecs:]
            Nsecs_mean   = numpy.mean(Nsecs_temp_data)
            Nsecs_std    = numpy.std(Nsecs_temp_data)

            temps_wstats.append((channel,current_temp, temp_mean, temp_std, Nsecs_mean, Nsecs_std))

        alarm = False
        if alarm_monitor is None:
            print "The selected alarm channel", alarm_channel, "is not on an actively be processed by this code."
            print "killing script"
            sys.exit()
        else:
            if high_alarm_temperature <= alarm_monitor:
                alarm = True
                alarm_msg = "High alarm Temperature of " + str(high_alarm_temperature) + " K  has been reached.\n"
            if alarm_monitor <= low_alarm_temperature:
                alarm = True
                alarm_msg = "Low alarm Temperature of " + str(low_alarm_temperature) + " K  has been reached.\n"

        ###################
        ### send emails ###
        ###################
        if PeriodicEmail:
            ElapsedEmailTime = current_time - Email_time
            if seconds_per_email < ElapsedEmailTime:
                EmailTrigger = True

        if alarm:
            alarm_subject = "CRYOSTAT ALARM - " + str('%2.3f' % alarm_monitor) + "K"
            print alarm_subject
            body_text = GenEmailText(temps_wstats, Nhours, totalhours)

            alarm_body_text = alarm_msg + body_text
            email_caleb(alarm_subject, alarm_body_text)
            text_caleb(alarm_subject)
            #email_groppi(alarm_subject, alarm_body_text)

            Email_time = current_time
            EmailTrigger = False

        else:
            if EmailTrigger:
                subject = "periodic cryostat update - " + str('%2.3f' % alarm_monitor) + "K"
                body_text = GenEmailText(temps_wstats, Nhours, totalhours)
                
                email_caleb(subject, body_text)
                Email_time = current_time
                EmailTrigger = False
            
        
        #######################
        ### make some plots ###
        #######################
        # Caleb's data, all the data
        if make_plots:
            plt.clf()
            matplotlib.rcParams['legend.fontsize'] = 10.0
            fig, ax1 = plt.subplots()

            plotcolors = ["blue", "green", "red", "coral", "dodgerblue", "gold", "forest", "purple"]
            lines = []
            names = []
            for temp_index in range(len(temps)):
                temp = temps[temp_index]
                plotcolor = plotcolors[temp_index]
                channel = temp[0]
                data    = temp[1]
                ax1.plot(Ttime, data, color=plotcolor, linewidth=3)
                line = plt.Line2D(range(10), range(10), color=plotcolor)
                lines.append(line)
                if channel == 4:
                    names.append("Receiver")
                elif channel == 3:
                    names.append("Outer Shield")
                elif channel == 2:
                    names.append("Inner Shield")
                else:
                    names.append("Channel " + str(channel))

            ax1.set_xlabel('hours since start')
            ax1.set_ylabel('Temperature (K)')
            plt.legend(tuple(lines),tuple(names),numpoints=1, loc=2)
            plt.savefig(folder +  monitor_type+"_Allchannels.png")


            # Caleb's data, last Nsecs
            plt.clf()
            matplotlib.rcParams['legend.fontsize'] = 10.0
            fig, ax1 = plt.subplots()

            lines = []
            names = []
            for temp_index in range(len(temps)):
                temp = temps[temp_index]
                plotcolor = plotcolors[temp_index]
                channel = temp[0]
                data    = temp[1]
                data    = data[start_last_Nsecs:]
                ax1.plot(Ttime[start_last_Nsecs:], data, color=plotcolor, linewidth=3)
                line = plt.Line2D(range(10), range(10), color=plotcolor)
                lines.append(line)
                if channel == 4:
                    names.append("Receiver")
                elif channel == 3:
                    names.append("Outer Shield")
                elif channel == 2:
                    names.append("Inner Shield")
                else:
                    names.append("Channel " + str(channel))

            ax1.set_xlabel('The last ' + str('%2.2f' % Nhours) + ' hours')
            ax1.set_ylabel('Temperature (K)')
            plt.legend(tuple(lines),tuple(names),numpoints=1, loc=2)
            plt.savefig(folder +  monitor_type+'_'+str(Nsecs) +"_secs_Allchannels.png")

            # Caleb's receiver data, all the data
            plt.clf()
            matplotlib.rcParams['legend.fontsize'] = 10.0
            fig, ax1 = plt.subplots()

            for temp_index in range(len(temps)):
                temp = temps[temp_index]
                channel = temp[0]
                data    = temp[1]
                plotcolor = plotcolors[temp_index]
                if channel == alarm_channel:
                    ax1.plot(Ttime, data, color=plotcolor, linewidth=3)
                    ax1.set_xlabel('hours since start')
                    ax1.set_ylabel('Temperature (K)')
                    plt.savefig(folder +  monitor_type+"_channel" + str(channel) + ".png")


            # Caleb's receiver data, last Nsecs
            plt.clf()
            matplotlib.rcParams['legend.fontsize'] = 10.0
            fig, ax1 = plt.subplots()
            for temp_index in range(len(temps)):
                temp = temps[temp_index]
                channel = temp[0]
                data    = temp[1]
                plotcolor = plotcolors[temp_index]
                if channel == alarm_channel:
                    ax1.set_xlabel('The last ' + str('%2.2f' % Nhours) + ' hours')
                    ax1.set_ylabel('Temperature (K)')
                    ax1.plot(Time_Nsecs, data[start_last_Nsecs:], color=plotcolor, linewidth=3)
                    plt.savefig(folder + monitor_type+'_'+str(Nsecs) +"_secs_channel" + str(channel) + ".png")

            plt.close("all")
        ### end plotting
        
        time.sleep(monitor_sleep)
    
    