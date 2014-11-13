import sys
from sys import platform

from datapro import YdataPro
from profunc import getproYdata, GetProDirsNames, getproparams, getmultiParams, getproSweep, windir
from Plotting import GetAllTheProFastSweepData



def getYsweeps(fullpaths, Ynums=None, verbose=False):
    class Ysweeps():
        def __init__(self,fullpath,Ynum):  #You must always define the self, here with
            proYdatadir = fullpath + 'prodata/' + Ynum + '/'

            self.name = fullpath + Ynum # This is a unique identifier for each sweep
            self.fullpath = fullpath

            ### Get the Processed Parameters of the Sweep
            paramsfile_list = []
            paramsfile_list.append(proYdatadir + 'hotproparams.csv')
            paramsfile_list.append(proYdatadir + 'coldproparams.csv')
            self.K_val, self.magisweep, self.magiset, self.magpot, self.meanmag_V, self.stdmag_V, self.meanmag_mA, \
            self.stdmag_mA, self.LOuAsearch, self.LOuAset, self.UCA_volt, self.LOuA_set_pot, self.LOuA_magpot, \
            self.meanSIS_mV, self.stdSIS_mV, self.meanSIS_uA, self.stdSIS_uA, self.meanSIS_tp, self.stdSIS_tp, \
            self.SIS_pot, self.del_time, self.LOfreq, self.IFband, self.meas_num, self.tp_int_time, \
            self.tp_num, self.tp_freq \
                = getmultiParams(paramsfile_list)

            # Astro Processed Data
            self.Yfactor, self.mV_Yfactor, self.hot_mV_mean, self.cold_mV_mean, self.mV, \
            self.hot_mV_std, self.cold_mV_std, self.hot_uA_mean, self.cold_uA_mean, \
            self.hot_uA_std, self.cold_uA_std, self.hot_tp_mean, self.cold_tp_mean,\
            self.hot_tp_std, self.cold_tp_std,\
            self.hot_time_mean, self.cold_time_mean, self.hot_pot, self.cold_pot,\
            self.hotdatafound, self.colddatafound, self.Ydatafound\
                = getproYdata(proYdatadir)

            ### Get the Hot Fast Processed Sweep Data
            self.hot_fastprodata_found, self.hot_unpumpedprodata_found, \
            self.hot_mV_fast, self.hot_uA_fast, self.hot_tp_fast, self.hot_pot_fast, \
            self.hot_mV_unpumped, self.hot_uA_unpumped, self.hot_tp_unpumped, self.hot_pot_unpumped \
                = GetAllTheProFastSweepData(proYdatadir+'hot')

            ### Get the Cold Fast Processed Sweep Data
            self.cold_fastprodata_found, self.cold_unpumpedprodata_found, \
            self.cold_mV_fast, self.cold_uA_fast, self.cold_tp_fast, self.cold_pot_fast, \
            self.cold_mV_unpumped, self.cold_uA_unpumped, self.cold_tp_unpumped, self.cold_pot_unpumped \
                = GetAllTheProFastSweepData(proYdatadir+'cold')
            #self.abundances = []   #A call to a smaller class, used as a sub-class


        def longDescription(self):
            description = "name = %s\n" % self.name
            description += ("Yfactor = %.2f \n" % self.Yfactor[0] )
            return description


    allYsweeps = []
    for fullpath in fullpaths:
        Ynums, prodatadir, plotdir = GetProDirsNames(fullpath, search_4Ynums, Ynums)
        for Ynum in Ynums:
            Ysweep = Ysweeps(fullpath, Ynum)
            allYsweeps.append(Ysweep)

    return allYsweeps


def getSweeps(fullpaths, verbose=False):
    class Sweep():
        def __init__(self,fullpath):
            if platform == 'win32':
                fullpath = windir(fullpath)
            self.name = fullpath
            self.fullpath = fullpath

            self.K_val, self.magisweep, self.magiset, self.magpot, self.meanmag_V, self.stdmag_V,\
            self.meanmag_mA, self.stdmag_mA, self.LOuAsearch, self.LOuAset, self.UCA_volt,\
            self.LOuA_set_pot, self.LOuA_magpot, self.meanSIS_mV, self.stdSIS_mV, self.meanSIS_uA, self.stdSIS_uA, \
            self.meanSIS_tp, self.stdSIS_tp, self.SIS_pot, self.del_time, self.LOfreq, self.IFband, self.meas_num, \
            self.tp_int_time, self.tp_num, self.tp_freq \
                = getproparams(fullpath + 'proparams.csv')

            ### Get The Astronomy Quality Processed Sweep Data
            self.mV_mean, self.mV_std, self.uA_mean,   self.uA_std, \
            self.tp_mean, self.tp_std, self.time_mean, self.pot, self.astroprodata_found \
                = getproSweep(fullpath)

            ### Get the Hot Fast Processed Sweep Data
            self.fastprodata_found, self.unpumpedprodata_found, \
            self.mV_fast, self.uA_fast, self.tp_fast, self.pot_fast, \
            self.mV_unpumped, self.uA_unpumped, self.tp_unpumped, self.pot_unpumped \
                = GetAllTheProFastSweepData(fullpath)

        def longDescription(self):
            description = "name = %s\n" % self.name
            description += ("K_val = %.2f \n" % self.K_val )
            return description


    allSweeps = []
    search_4Ynums = True
    Ynums = None
    for fullpath in fullpaths:
        Ynums, prodatadir, plotdir = GetProDirsNames(fullpath, search_4Ynums, Ynums)
        for Ynum in Ynums:
            proYdatadir = fullpath + 'prodata/' + Ynum + '/'
            proYdatadir_hot  = proYdatadir + 'hot'
            proYdatadir_cold = proYdatadir + 'cold'
            allSweeps.append(Sweep(proYdatadir_hot))
            allSweeps.append(Sweep(proYdatadir_cold))

    return allSweeps



### Do Cuts Based on Parameters
# total power integration time
def tp_int_cut(sweeps, min_tp_int=None, max_tp_int=None, verbose=False):
    tp_int_cut_sweeps = []
    if verbose:
        print 'cutting for total power integration time'
    for sweep in sweeps:
        tp_int_time = sweep.tp_int_time
        if ((min_tp_int is None) or (min_tp_int  <= tp_int_time)) and (
            (max_tp_int is None) or (tp_int_time <=  max_tp_int)):
            tp_int_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return tp_int_cut_sweeps

# LO pump power in uA (that my code attempt to set)
def LOuAset_cut(sweeps, min_LOuAset=None, max_LOuAset=None, verbose=False):
    LOuAset_cut_sweeps = []
    if verbose:
        print 'cutting the LO pump power that the code attempted to set'
    for sweep in sweeps:
        LOuAset = sweep.LOuAset
        if ((min_LOuAset is None) or (min_LOuAset  <= LOuAset)) and (
            (max_LOuAset is None) or (LOuAset <=  max_LOuAset)):
            LOuAset_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return LOuAset_cut_sweeps

# Cut if the difference between LO pump power and the standard measurement is too great
def LOuAdiff_cut(sweeps, max_diff=1.0, verbose=False):
    LOuAdiff_cut_sweeps = []
    if verbose:
        print 'cutting sweep with the difference of measured LO pump power and attempted setting of LO power greater then', max_diff, 'uA'
    for sweep in sweeps:
        LOuAset    = sweep.LOuAset
        meanSIS_uA = sweep.meanSIS_uA
        diff = abs(LOuAset - meanSIS_uA)
        if diff <= max_diff:
            LOuAdiff_cut_sweeps.append(sweep)
            if verbose:
                print sweep.longDescription()
    return LOuAdiff_cut_sweeps




