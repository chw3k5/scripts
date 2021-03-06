import numpy as np
import os
from sys import platform
from datapro import YdataPro, getrawdata, get_fastIV
from profunc import getproYdata, GetProDirsNames, getproparams, getmultiParams, getproSweep, windir, ProcessMatrix
from profunc import getpro_spec
from Plotting import GetAllTheProFastSweepData
import copy


def getYsweeps(fullpaths, Ynums=None, verbose=False):
    class Ysweeps():
        def __init__(self,fullpath,Ynum):  #You must always define the self, here with
            proYdatadir = windir(fullpath + 'prodata/' + Ynum + '/')
            self.proYdatadir=proYdatadir
            self.Ynum = Ynum
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
            self.tp_num, self.tp_freq, self.mag_chan\
                = getmultiParams(paramsfile_list)

            # Astro Processed Data
            self.Yfactor,self.yerror,self.y_pot,self.y_mV,self.y_mVerror,\
            self.y_uA,self.y_uAerror,self.y_TP,self.y_TPerror,\
            self.hot_mV_mean, self.cold_mV_mean, self.mV, \
            self.hot_mV_std, self.cold_mV_std, self.hot_uA_mean, self.cold_uA_mean, \
            self.hot_uA_std, self.cold_uA_std, self.hot_TP_mean, self.cold_TP_mean, self.hot_TP_std, self.cold_TP_std,\
            self.hot_time_mean,self.cold_time_mean, self.hot_pot, self.cold_pot,\
            self.hotdatafound, self.colddatafound,self.Ydatafound\
                = getproYdata(proYdatadir,findTheOverLap=False)

            # old version of how I recorded this data
            self.mV_Yfactor=self.y_mV

            # this get populated when it is first called for findmaxpm
            (self.max_Yfactor, self.max_y_error, self.max_y_mV, self.max_y_mVerror, self.max_y_uA, self.max_y_uAerror,
            self.max_y_TP, self.max_y_TPerror, self.max_y_pot) \
                = (None,None,None,None,None,None,
                    None,None,None)

            # Old version of this function
            # self.Yfactor, self.mV_Yfactor, self.hot_mV_mean, self.cold_mV_mean, self.mV, \
            # self.hot_mV_std, self.cold_mV_std, self.hot_uA_mean, self.cold_uA_mean, \
            # self.hot_uA_std, self.cold_uA_std, self.hot_tp_mean, self.cold_tp_mean,\
            # self.hot_tp_std, self.cold_tp_std,\
            # self.hot_time_mean, self.cold_time_mean, self.hot_pot, self.cold_pot,\
            # self.hotdatafound, self.colddatafound, self.Ydatafound\
            #     = getproYdata(proYdatadir)

            # Processed spectrometer data
            self.spec_data_found, self.spec_freq_list,self.spec_Yfactor_list,\
            self.spec_hot_pwr_list,self.spec_hot_pot_list,self.spec_hot_mV_mean_list,self.spec_hot_tp_list,\
            self.spec_hot_spike_list_list,self.spec_hot_spikes_inband_list,self.spec_hot_sweep_index_list,\
            self.spec_cold_pwr_list,self.spec_cold_pot_list,self.spec_cold_mV_mean_list,self.spec_cold_tp_list,\
            self.spec_cold_spike_list_list,self.spec_cold_spikes_inband_list,self.spec_cold_sweep_index_list \
                = getpro_spec(proYdatadir)


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

        def get_raw_data(self):
            ### Get the raw data
            rawdatadir  = self.fullpath + 'rawdata/' + Ynum + '/'
            hot_dir = rawdatadir + 'hot/'
            cold_dir = rawdatadir + 'cold/'

            ### Hot ###
            self.hot_raw_astros_found, self.hot_raw_pot, self.hot_raw_mV_mean, self.hot_raw_mV_std,\
            self.hot_raw_uA_mean, self.hot_raw_uA_std, self.hot_raw_TP_mean, self.hot_raw_TP_std, self.hot_raw_time_mean,\
            hot_raw_TP_int_time, hot_raw_meas_num, hot_raw_TP_num, hot_raw_TP_freq\
                = getrawdata(hot_dir+'sweep/', verbose=verbose)

            fast_file = hot_dir+"fastsweep.csv"
            if os.path.isfile(fast_file):
                self.raw_hot_fast_found=True
                self.hot_raw_fast_mV, self.hot_raw_fast_uA, self.hot_raw_fast_tp, self.hot_raw_fast_pot \
                    = get_fastIV(fast_file)
            else:
                self.raw_hot_fast_found=False

            unpumped_file = hot_dir+"unpumpedsweep.csv"
            if os.path.isfile(fast_file):
                self.raw_hot_unpumped_found=True
                self.hot_raw_unpumped_mV, self.hot_raw_unpumped_uA, self.hot_raw_unpumped_tp, self.hot_raw_unpumped_pot \
                    = get_fastIV(unpumped_file)
            else:
                self.raw_hot_unpumped_found=False

            ### Cold ###
            self.cold_raw_astros_found, self.cold_raw_pot, self.cold_raw_mV_mean, self.cold_raw_mV_std,\
            self.cold_raw_uA_mean, self.cold_raw_uA_std, self.cold_raw_TP_mean, self.cold_raw_TP_std, self.cold_raw_time_mean,\
            cold_raw_TP_int_time, cold_raw_meas_num, cold_raw_TP_num, cold_raw_TP_freq\
                = getrawdata(cold_dir+'sweep/', verbose=verbose)

            fast_file = cold_dir+"fastsweep.csv"
            if os.path.isfile(fast_file):
                self.raw_cold_fast_found=True
                self.cold_raw_fast_mV, self.cold_raw_fast_uA, self.cold_raw_fast_tp, self.cold_raw_fast_pot \
                    = get_fastIV(fast_file)
            else:
                self.raw_cold_fast_found=False

            unpumped_file = cold_dir+"unpumpedsweep.csv"
            if os.path.isfile(fast_file):
                self.raw_cold_unpumped_found=True
                self.cold_raw_unpumped_mV, self.cold_raw_unpumped_uA, self.cold_raw_unpumped_tp, self.cold_raw_unpumped_pot \
                    = get_fastIV(unpumped_file)
            else:
                self.raw_cold_unpumped_found=False

        def longDescription(self):
            description = "name = %s\n" % self.name
            description += ("Yfactor = %.2f \n" % self.Yfactor[0] )
            return description


        def find_max_yfactor_pm(self):
            if self.max_Yfactor is None:
                (max_Yfactor, max_y_error, max_y_mV,
                 max_y_mVerror, max_y_uA,max_y_uAerror,
                 max_y_TP, max_y_TPerror, max_y_pot) \
                    = (None,None,None,
                       None,None,None,
                       None,None,None)
                if self.Ydatafound:
                    max_Yfactor = max(np.array(self.Yfactor))
                    maxIndex=self.Yfactor.index(max_Yfactor)
                    if self.yerror is not None:
                        max_y_error = self.yerror[maxIndex]
                    if self.y_mV is not None:
                        max_y_mV = self.y_mV[maxIndex]
                    if self.y_mVerror is not None:
                        max_y_mVerror = self.y_mVerror[maxIndex]
                    if self.y_uA is not None:
                        max_y_uA = self.y_uA[maxIndex]
                    if self.y_uAerror is not None:
                        max_y_uAerror = self.y_uAerror[maxIndex]
                    if self.y_TP is not None:
                        max_y_TP = self.y_TP[maxIndex]
                    if self.y_TPerror is not None:
                        max_y_TPerror = self.y_TPerror[maxIndex]
                    if self.y_pot is not None:
                        max_y_pot = self.y_pot[maxIndex]
            else:
                (max_Yfactor, max_y_error, max_y_mV,
                 max_y_mVerror, max_y_uA,max_y_uAerror,
                 max_y_TP, max_y_TPerror, max_y_pot) \
                    = (self.max_Yfactor, self.max_y_error, self.max_y_mV,
                       self.max_y_mVerror, self.max_y_uA, self.max_y_uAerror,
                       self.max_y_TP, self.max_y_TPerror, self.max_y_pot)


            return (max_Yfactor, max_y_error, max_y_mV,
                    max_y_mVerror, max_y_uA,max_y_uAerror,
                    max_y_TP, max_y_TPerror, max_y_pot)

        def find_max_yfactor_spec(self,min_freq=None,max_freq=None):
            max_Yfactor      = None
            max_Yfactor_mV   = None
            max_Yfactor_freq = None
            ave_Yfactor      = None
            image_of_spec_Yfactor_list      = self.spec_Yfactor_list[:]
            image_of_spec_freq_list         = self.spec_freq_list[:]
            image_of_spec_hot_mV_mean_list  = self.spec_hot_mV_mean_list[:]
            image_of_spec_cold_mV_mean_list = self.spec_cold_mV_mean_list[:]

            if self.spec_data_found:
                max_Yfactor      = -1
                max_Yfactor_mV   = -1
                max_Yfactor_freq = -1
                ave_Yfactor      = -1
                if min_freq is not None:
                    for list_index in range(len(image_of_spec_freq_list[:])):
                        spec_Yfactor  = image_of_spec_Yfactor_list[list_index]
                        spec_freqs    = image_of_spec_freq_list[list_index]
                        spec_hot_mV   = image_of_spec_hot_mV_mean_list[list_index]
                        spec_cold_mV  = image_of_spec_cold_mV_mean_list[list_index]

                        spec_freq_temp = []
                        spec_Yfactor_temp = []
                        spec_hot_mV_temp = None
                        spec_cold_mV_temp = None
                        for (f_index,freq) in list(enumerate(spec_freqs)):
                            if min_freq <= freq:
                                spec_freq_temp.append(freq)
                                spec_Yfactor_temp.append(spec_Yfactor[f_index])
                                if spec_hot_mV_temp is None:
                                    spec_hot_mV_temp  = spec_hot_mV
                                    spec_cold_mV_temp = spec_cold_mV

                        image_of_spec_freq_list[list_index]         = spec_freq_temp
                        image_of_spec_Yfactor_list[list_index]      = spec_Yfactor_temp
                        image_of_spec_hot_mV_mean_list[list_index]  = spec_hot_mV_temp
                        image_of_spec_cold_mV_mean_list[list_index] = spec_cold_mV_temp


                if max_freq is not None:
                    for list_index in range(len(image_of_spec_freq_list[:])):
                        spec_freqs     = image_of_spec_freq_list[list_index]
                        spec_Yfactor  = image_of_spec_Yfactor_list[list_index]
                        spec_hot_mV   = image_of_spec_hot_mV_mean_list[list_index]
                        spec_cold_mV  = image_of_spec_cold_mV_mean_list[list_index]

                        spec_freq_temp = []
                        spec_Yfactor_temp = []
                        spec_hot_mV_temp = None
                        spec_cold_mV_temp = None
                        for (f_index,freq) in list(enumerate(spec_freqs)):
                            if freq <= max_freq:
                                spec_freq_temp.append(freq)
                                spec_Yfactor_temp.append(spec_Yfactor[f_index])
                                if spec_hot_mV_temp is None:
                                    spec_hot_mV_temp  = spec_hot_mV
                                    spec_cold_mV_temp = spec_cold_mV

                        image_of_spec_freq_list[list_index]         = spec_freq_temp
                        image_of_spec_Yfactor_list[list_index]      = spec_Yfactor_temp
                        image_of_spec_hot_mV_mean_list[list_index]  = spec_hot_mV_temp
                        image_of_spec_cold_mV_mean_list[list_index] = spec_cold_mV_temp

                list_of_max_Yfactors     = []
                list_of_max_Yfactor_freq = []
                list_of_max_Yfactor_mV   = []
                list_of_ave_Yfactors     = []

                for list_index in range(len(image_of_spec_freq_list[:])):
                    spec_Yfactor         = list(image_of_spec_Yfactor_list[list_index])
                    Yfactor_freq         = list(image_of_spec_freq_list[list_index])
                    local_max_Yfactor_mV = (image_of_spec_hot_mV_mean_list[list_index] + image_of_spec_cold_mV_mean_list[list_index])/2.0

                    local_max_Yfactor      = max(spec_Yfactor)
                    index_of_max_Yfactor   = spec_Yfactor.index(local_max_Yfactor)
                    local_max_Yfactor_freq = Yfactor_freq[index_of_max_Yfactor]
                    local_ave_Yfactor      = np.mean(spec_Yfactor)

                    if max_Yfactor < local_max_Yfactor:
                        max_Yfactor    = local_max_Yfactor
                        max_Yfactor_mV = local_max_Yfactor_mV
                        max_Yfactor_freq   = local_max_Yfactor_freq

                    if ave_Yfactor < local_ave_Yfactor:
                        ave_Yfactor = local_ave_Yfactor

                    list_of_max_Yfactors.append(local_max_Yfactor)
                    list_of_max_Yfactor_freq.append(local_max_Yfactor_freq)
                    list_of_max_Yfactor_mV.append(local_max_Yfactor_mV)
                    list_of_ave_Yfactors.append(ave_Yfactor)

                return max_Yfactor, max_Yfactor_mV, max_Yfactor_freq, ave_Yfactor

        def intersecting_line_mV(self,mV_center=2.0,mV_plus_minus=0.05):
            def find_ave_Y4X(y_list,x_list,x_center,x_plus_minus):
                y_to_average = []
                diff_min = 999999999999999.0
                y_closest = None
                x_closest = None
                for index in range(len(x_list)):
                    x = x_list[index]
                    x_diff = abs(x-x_center)
                    if x_diff < diff_min:
                        diff_min = x_diff
                        y_closest = y_list[index]
                        x_closest = x_list[index]
                    if x_diff <= x_plus_minus:
                        y_to_average.append(y_list[index])
                if y_to_average == []:
                    y_to_average = [y_closest]
                y_average = np.mean(y_to_average)
                return y_average, x_closest

            hot_mV_list = self.hot_mV_mean
            hot_tp_list = self.hot_tp_mean
            tp_hot, mV_hot = find_ave_Y4X(y_list=hot_tp_list,x_list=hot_mV_list,x_center=mV_center,x_plus_minus=mV_plus_minus)

            cold_mV_list = self.cold_mV_mean
            cold_tp_list = self.cold_tp_mean
            tp_cold, mV_cold = find_ave_Y4X(y_list=cold_tp_list,x_list=cold_mV_list,x_center=mV_center,x_plus_minus=mV_plus_minus)

            temperatures = self.K_val
            temp_cold = min(temperatures)
            temp_hot  = max(temperatures)

            m = (tp_hot-tp_cold)/(temp_hot-temp_cold)
            self.intersectingL_m = m
            self.intersectingL_b = tp_hot-m*temp_hot
            return


        def intersecting_line_Ymax(self,mV_plus_minus=0.05):
            max_mV_Yfactor, max_Yfactor = self.find_max_yfactor_pm()
            self.intersecting_line_mV(mV_center=max_mV_Yfactor, mV_plus_minus=mV_plus_minus)

            return

        def shotnoise_test(self, min_uA=80,max_uA=None, mono_switcher=True, do_regrid=False, do_conv=False, regrid_mesh=0.1, min_cdf=0.95, sigma=5, verbose=False):
            self.get_raw_data()
            hot_gain, hot_noise_power = None, None
            uA_shot, TP_shot = [],[]
            shotnoise_test_failed = False
            unpumped_found = self.raw_hot_unpumped_found
            if unpumped_found:
                unpumped_uA = self.hot_raw_unpumped_uA
                unpumped_tp = self.hot_raw_unpumped_tp
            if self.hot_raw_astros_found:
                uAs=self.hot_raw_uA_mean
                TPs=self.hot_raw_TP_mean
                for index in range(len(uAs)):
                    uA = uAs[index]
                    TP = TPs[index]
                    if ((min_uA is None) or (min_uA <= uA)):
                        if ((max_uA is None) or (uA <= max_uA)):
                            uA_shot.append(uA)
                            TP_shot.append(TP)
            if ((uA_shot == []) or (len(uA_shot)<=1)):
                if verbose:
                    print 'The astro data does not contain enough current measurements in the range (',min_uA,',',max_uA,')'
                    print 'checking to to if unpumped data is available.'
                if not unpumped_found:
                    print 'no data was found in for the unpumped measurement'
                    shotnoise_test_failed = True
                else:
                    for index in range(len(unpumped_uA)):
                        uA = unpumped_uA[index]
                        TP = unpumped_tp[index]
                        if ((min_uA is None) or (min_uA <= uA)):
                            if ((max_uA is None) or (uA <= max_uA)):
                                uA_shot.append(uA)
                                TP_shot.append(TP)
                    if ((uA_shot == []) or (len(uA_shot)<=1)):
                        print 'The unpumped data does not contain enough current measurements in the range (',min_uA,',',max_uA,')'
                        print 'The shot noise function has failed.'
                        shotnoise_test_failed = True

            if shotnoise_test_failed:
                gain = None
                input_noise = None
                T = None
                pro_uA = None
                pro_TP = None
            else:
                raw_matrix = np.zeros((len(uA_shot),2))
                raw_matrix[:,0]=uA_shot
                raw_matrix[:,1]=TP_shot
                #print uA_shot,TP_shot
                matrix, raw_matrix, mono_matrix, regrid_matrix, conv_matrix\
                    = ProcessMatrix(raw_matrix, mono_switcher=mono_switcher, do_regrid=do_regrid,
                                    do_conv=do_conv, regrid_mesh=regrid_mesh, min_cdf=min_cdf,
                                    sigma=sigma, verbose=False)

                pro_uA = matrix[:,0]
                pro_TP = matrix[:,1]
                z = np.polyfit(pro_uA, pro_TP, 1)
                gain = z[0]
                noise_power = z[1] # power in recorder output in volts
                input_noise = noise_power/gain # power in uA

                e = 1.60217657e-19 # Columbs (electron charge)
                I = input_noise*1.0e-6 # dark current in Amps
                kT = 2.0*e*I
                #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.7, str('%2.2f' % fP) + " $fW = 2eI_0$$B = P_0$", fontsize=16, color="firebrick")

                kb = 1.3806488e-23
                T = kT/(kb)


            self.hot_shotnoise_test = (not shotnoise_test_failed)
            self.hot_shotnoise_shot_uA = pro_uA
            self.hot_shotnoise_shot_tp = pro_TP
            self.hot_shotnoise_gain = gain
            self.hot_shotnoise_input_noise = input_noise
            self.hot_shotnoise_T = T

            print "Gain (V/uA), noise power (V), input noise (uA), input noise temperature (K)"
            print gain, noise_power, input_noise, T

            return


    allYsweeps = []
    search_4Ynums = True
    Ynums = None
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
            self.tp_int_time, self.tp_num, self.tp_freq, self.mag_chan \
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
            description = "name = %s" % self.name
            description += ("K_val = %.2f" % self.K_val )
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








