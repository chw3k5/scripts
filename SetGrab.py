import sys
from sys import platform

from profunc import getproYdata, GetProDirsNames, getproparams


### Options ###
search_4Ynums = True
Ynums = ''


### All the sets of data to collect the processed data from
setnames = []
setnames.append('LOfreq')
setnames.append('LOfreq2')
allSweeps = []

def getfullpath(setname):
    if platform == 'darwin':
        fullpath = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/' + setname + '/'
    elif platform == 'win32':
        fullpath = '' + setname + '/'
    else:
        fullpath = []
    return fullpath



### Get the Y sweeps from the raw data folder
class Ysweeps():
    def __init__(self,setname,Ynum):  #You must always define the self, here with
        fullpath = getfullpath(setname)
        proYdatadir = fullpath + 'prodata/' + Ynum + '/'

        self.name = setname  + Ynum # This is a unique identifier for each sweep
        self.fullpath = fullpath

        # Processed Parameters Data
        paramsfile = proYdatadir + 'proparams.csv'
        self.K_val, self.magisweep, self.magiset, self.magpot, self.meanmag_V, self.stdmag_V, self.meanmag_mA, \
        self.stdmag_mA, self.LOuAsweep, self.LOuAset, self.UCA_volt, self.LOuA_set_pot, self.LOuA_magpot, \
        self.meanSIS_mV, self.stdSIS_mV, self.meanSIS_uA, self.stdSIS_uA, self.meanSIS_tp, self.stdSIS_tp, \
        self.SIS_pot, self.del_time, self.LOfreq, self.IFband, self.TP_int_time \
            = getproparams(paramsfile)

        # Astro Processed Data
        self.Yfactor, self.mV, self.hot_mV_std, self.cold_mV_std, self.hot_uA_mean, self.cold_uA_mean,    \
        self.hot_uA_std, self.cold_uA_std, self.hot_TP_mean, self.cold_TP_mean, self.hot_TP_std,            \
        self.cold_TP_std, self.hot_TP_num, self.cold_TP_num, self.hot_TP_freq, self.cold_TP_freq,           \
        self.hot_time_mean, self.cold_time_mean, self.hot_pot, self.cold_pot,                          \
        self.hot_meas_num, self.cold_meas_num = getproYdata(proYdatadir)

        #self.abundances = []   #A call to a smaller class, used as a sub-class


    def longDescription(self):
        description = "name = %s\n" % self.name
        description += ("Yfactor = %.2f \n" % self.Yfactor[0] )
        return description

### Get all the names of the raw data files ###

for setname in setnames:
    fullpath = getfullpath(setname)
    Ynums, prodatadir, plotdir = GetProDirsNames(fullpath, search_4Ynums, Ynums)
    for Ynum in Ynums:
        sweep = Ysweeps(setname, Ynum)
        allSweeps.append(sweep)
        print sweep.longDescription()



