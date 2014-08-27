import atpy
from matplotlib import pyplot as plt
from pylab import *
filename = ""

data = atpy.Table(filename, type="ascii", delimiter=",")

plt.clf()
plt.plot(data.header1, data.header2)

rcParams['legend.fontsize'] = 8
plt.legend(loc=4)
plt.xlabel('Voltage (mV)')
plt.ylabel('Current (uA)')
plt.title("Y Factor from Total Power")
plt.show()
plt.draw()

save_file = False

if save_file:
    saveplotdir  = ""
    saveplotname = saveplotdir + 'plot.png'
    savefig(saveplotname)