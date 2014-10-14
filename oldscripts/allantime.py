def allentime(filename, SampleFrequency, SampleTime, get_newdata, tau_min, verbose):
    from domath import AllanVar
    from control import LJ_streamTP
    import numpy
    
    if get_newdata:
        LJ_streamTP(filename, SampleFrequency, SampleTime, verbose)
    
    mod_val = 10
    n = open(filename, 'r')
    
    first_line = n.readline()
    temp1 = first_line.split('=')
    temp2 = temp1[1].split('\n')
    frequency = float(temp2[0])
    tau = mod_val/frequency
    
    second_line = n.readline()
    #temp1 = second_line.split('\n')
    #data_handle = temp1[0]
    
    data = []
    count = 0
    for line in n:
        count = count + 1
        if count % mod_val == 0:
            temp1 = line.split('\n')
            data.append(float(temp1[0]))
    data = numpy.array(data)
    
    #data = data[:1000]
    if verbose:
        print str(len(data)) + ' is the data length'
    Variance = AllanVar(data, tau_min, verbose)        
    
    return Variance, tau
    
filename = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/allan/time/test.txt'
SampleFrequency = 100 # samples per second
SampleTime      = 60*60 # seconds of sampling

get_newdata = False # True or False

tau_min = 10

verbose         = True # True or False
Variance, tau = allentime(filename, SampleFrequency, SampleTime, get_newdata, tau_min, verbose)

from matplotlib import pyplot as plt
from numpy import sqrt
plt.close("all")
plt.clf()
#plt.plot(mean(Variance,0))
taus = range(len(Variance))
maxdata = len(taus)
plt.plot(taus[0:maxdata], Variance[0:maxdata])
plt.show()
plt.draw()