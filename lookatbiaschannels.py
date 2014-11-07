__author__ = 'chwheele'
from control import attempt_meas, opentelnet, closetelnet
sleep_time = 0.5
flag_Achannels = []
flag_As       = []
flag_Vchannels = []
flag_Vs       = []
opentelnet()
for channel in range(8):
    redo = True
    while redo:
       redo, V, A, pot = attempt_meas(sleep_time, channel)
    print 'channel =',channel, 'V =', V,'A =',A,'pot =',pot
    if 100 < abs(A):
        flag_Achannels.append(channel)
        flag_As.append(A)
    if 10 < abs(V):
        flag_Vchannels.append(channel)
        flag_Vs.append(V)
closetelnet()
print ''
print "Flags for Current"
for n in range(len(flag_Achannels)):
    print flag_Achannels[n], flag_As[n]

print ''
print "Flags for Voltage"
for n in range(len(flag_Vchannels)):
    print flag_Vchannels[n], flag_Vs[n]