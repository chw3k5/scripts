
    # I have to install
    # libusb=1.0 from http://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.18/
    # LabJackPython-10-22-2012.zip from http://github.com/labjack/exodriver
    # or http://labjack.com/support/linux-and-mac-os-x-drivers
    # then the python part
    # from http://labjack.com/support/labjackpython
    # download the link, for me it was: http://labjack.com/sites/default/files/2014/04/LabJackPython-4-24-2014.zip
    # the after unpaking the package, go to that folder and type: "sudo python setup.py install" in the asme directory as setup.py
    #


    #  lj.open(self, firstFound = True, serial = None, localId = None, devNumber = None, handleOnly = False, LJSocket = None)

    # configU3(self, LocalID = None, TimerCounterConfig = None, FIOAnalog = None, FIODirection = None, FIOState = None, EIOAnalog = None, EIODirection = None, EIOState = None, CIODirection = None, CIOState = None, DAC1Enable = None, DAC0 = None, DAC1 = None, TimerClockConfig = None, TimerClockDivisor = None, CompatibilityOptions = None )

    # getTemperature()

    # getAIN(self, posChannel, negChannel = 31, longSettle=False, quickSample=False)

    # binaryToCalibratedAnalogVoltage(self, bits, isLowVoltage = True, isSingleEnded = True, isSpecialSetting = False, channelNumber = 0)

    # getCalibrationData(self)

    #
    # AddRequestS(u3Handle,"LJ_ioGET_AIN", 0, 0.0, 0, 0.0)

    # AddRequest(ID, LJ_ioPUT_COUNTER_ENABLE,0,1,0,0)

##############################################
##############################################
########## Local Oscillator Control ##########
##############################################
##############################################
import u3, time
from sys import platform
# Caleb's programs
from LabJack_config import NumChannels, Resolution, wavenames, loop_max
from profunc import windir


############################
###### LabJackU3_DAQ0 ######
############################

def LabJackU3_DAQ0(UCA_voltage):
    status = False
    if (0 <= UCA_voltage) and (UCA_voltage <= 5):
        lj = u3.U3()
        lj.writeRegister(5000, UCA_voltage)
        lj.close()
        status = True
    else:
        print "UCA_voltage was not set properly, it was either greater than 5, less than 0, or not a number. UCA_voltage = "+str(UCA_voltage)+". Returning Status false"
    return status


############################
###### LabJackU3_ANI0 ######
############################

def LabJackU3_AIN0():
    lj = u3.U3()
    tp = lj.getAIN(0)
    lj.close()
    return tp


#########################
###### LJ_streamTP ######
#########################
def LJ_streamTP(filename, SampleFrequency, SampleTime, verbose):
    # Peter N. Saeta, 2013 November 11
    # is a genus

    # Caleb Wheeler found this code on the internet and used it like a
    # monkey. Modified May 20, 2014

    # This code uses the LabJack to record 1 or more voltages at a
    # regular cadence. It runs until you stop it with Ctrl-C.
    # Edit the values below (above the import u3 statement)
    # to match your requirements. Note that the Resolution parameter
    # sets the accuracy of the data. The smaller the number, the better
    # the accuracy, but the slower the sampling rate must be. See
    # http://labjack.com/support/u3/users-guide/3.2 for details.
    from LabJack_config import wavenames
    if platform == 'win32':
        filename = windir(filename)
    # Prepare the u3 interface for streaming

    d = u3.U3()        # initialize the interface; assumes a single U3 is plugged in to a USB port
    d.configU3()    # set default configuration
    d.configIO( FIOAnalog = 1 )        # ask for analog inputs

    # In case the stream was left running from a previous execution
    try: d.streamStop()
    except: pass


    d.streamConfig( NumChannels = NumChannels,
        PChannels = range(NumChannels),
        NChannels = [ 31 for x in range(NumChannels) ],
        Resolution = Resolution,
        SampleFrequency = SampleFrequency )

    #d.packetsPerRequest = 1000

    # Try to measure a data set.
    def measure():
        try:
            for r in d.streamData():
                if r is not None:
                    if r['errors'] or r['numPackets'] != d.packetsPerRequest or r['missed']:
                        print "error: errors = '%s', numpackets = %d, missed = '%s'" % (r['errors'], r['numPackets'], r['missed'])
                    break
        finally:
            pass
        return r

    # Write a set of data to the file
    def writeData( r ):
        chans = [ r['AIN%d' % (n)] for n in range(NumChannels) ]
        for i in range(len(chans[0])):
            f.write( "\t".join( ['%.6f' % c[i] for c in chans] ) + '\n' )

    with open(filename, 'w') as f:
        f.write( "frequency=%d\n" % SampleFrequency)
        if wavenames == []:
            wavenames = ['wave%d' % n for n in range(NumChannels)]
        f.write( '\t'.join(wavenames) + '\n')

    # start the stream
    d.streamStart()
    loop = 0

    try:
        finished = False
        start = time.time()
        while not finished:
            with open(filename, 'a') as f:
                writeData( measure() )
            loop += 1
            if loop_max < loop + 1 :
                finished = True
            diff_time = time.time() - start
            if SampleTime < diff_time:
                finished = True

            if verbose:
                print( "[%.4d %.2f s]" % (loop, diff_time))

    finally:
        d.streamStop()
        d.close()
    return

