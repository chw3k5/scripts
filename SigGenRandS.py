__author__ = 'chwheele'
# try:
#     import visa
#     RandS_SMB100A = visa.instrument("TCPIP::192.168.1.101::hislip0::INSTR")
# except:
#     pass
#     print "There was some problem with VISA or communicating with the spectrum analyzer, look in LOinput.py"

from time import sleep
import visa
RandS_SMB100A = visa.instrument("TCPIP::192.168.1.101::hislip0::INSTR")
RandS_SMB100A.write('FREQ:MODE CW')
RandS_SMB100A.write('SOUR:FREQ 13.9GHz')
RandS_SMB100A.write('SOUR:POW:LEV:IMM:AMPL -40')

RandS_SMB100A.write('OUTP ON')
sleep(3)
RandS_SMB100A.write('OUTP OFF')

# FREQ:MODE CW
# SOUR:FREQ:CENT 14 GH
# SOUR:POW:LEV:IMM:AMPL 0