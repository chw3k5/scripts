def LabJackU3_DAQ0(UCA_voltage):
    # I have to install
    # libusb=1.0 from http://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.18/
    # LabJackPython-10-22-2012.zip from http://github.com/labjack/exodriver 
    import u3
    status = False
    if (0 <= UCA_voltage) and (UCA_voltage <= 5):
        lj = u3.U3()
        lj.writeRegister(5000, UCA_voltage)
        lj.close()
        status = True
    else:
        print "UCA_voltage was not set properly, it was either greater than 5, less than 0, or not a number. UCA_voltage = "+str(UCA_voltage)+". Returning Status false" 
    return status