import numpy, time
from sys import platform
# Caleb's programs
import os
from profunc import windir
from LabJack_control import LJ_streamTP

extra_sleep_fraction = 0.05 # fraction of the total sweep time to add to waiting time for a singe sweep
extra_sleep_float    = 1.0  # seconds added to total sweep time
min_sleep_time       = 10

GPIB_str = "GPIB0::5::INSTR"

try:
    import visa
    sa = visa.instrument(GPIB_str)
except:
    pass


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:    
        return False


def start_spec_grab(spec_filename,
                    verbose=False, linear_sc=True,
                    freq_start=0.0, freq_stop=5.0,
                    sweep_time='AUTO', video_band=10, resol_band=30, attenu=0,
                    aveNum=1, lin_ref_lev=500):

    spec_filename = windir(spec_filename)

    #################################
    ### format numbers to strings ###
    #################################
    freq_start_str     = str('%1.3f' % freq_start) + " GHz"
    freq_stop_str      = str('%1.3f' % freq_stop ) + " GHz"
    if is_number(sweep_time):
        sweep_time_str = str('%3.1f' % sweep_time) + " S"
    else:
        sweep_time_str = sweep_time
    if is_number(video_band):
        video_band_str = str('%4.0f' % video_band ) + " kHz"
    else:
        video_band_str = video_band
    if is_number(resol_band):
        resol_band_str = str('%4.0f' % resol_band ) + " kHz"
    else:
        resol_band_str = resol_band
    attenu_str         = str(attenu)+"DB"




    #########################
    ### Set Sweep Options ###
    #########################
    # set the start frequency
    sa.write("FA " + freq_start_str)
    #set the stop frequency
    sa.write("FB " + freq_stop_str )
    # set the sweep time
    sa.write("ST " + sweep_time_str)
    # set the video bandwidth resolution
    sa.write("VB " + video_band_str)
    # set the video bandwidth resolution
    sa.write("RB " + resol_band_str)
    # set the attenuation on the input\
    sa.write("AT " +  attenu_str)
    # averaging is turned on or off here
    sa.write("VAVG " + str(aveNum))
    #set the scale
    if linear_sc:
        sa.write("LN")
        # Reference Level
        sa.write("RL " + str('%3.f' % lin_ref_lev) +" uV")
    else:
        sa.write("LG 10DB")
    # put the 'trace data format' of returned values as real numbers, option P
    sa.write('tdf P')


    sa.write('ST ?')
    sweep_time_float = float(sa.read())
    #print "sweep time float:", sweep_time_float
    #################
    ### The Sweep ###
    #################
    # trigger a new sweep to start
    sa.write('clrw tra')
    sweep_sleep = (sweep_time_float*aveNum)*(1+extra_sleep_fraction) + extra_sleep_float
    if sweep_sleep < min_sleep_time:
        sweep_sleep = min_sleep_time

    if verbose:
        print "spectrometer sweep, frequency start: "+ freq_start_str + '   frequency stop: '+freq_stop_str


    return sweep_sleep

def finish_spec_grab(spec_filename,freq_start=0., freq_stop=5., verbose=False, linear_sc=False):
    freq_list=list(numpy.arange(freq_start, freq_stop,((freq_stop-freq_start)/600.0)))
    freq_list.append(freq_stop)

    # get the trace data from the sweep that was just preformed
    sa.write('tra?')
    #count = 0
    #while True:
    #    if 5 <= count:
    #        break
    #    sa.write("DONE?")
    #    if sa.read() == '1':
    #        break
    #    else:
    #        time.sleep(1)
    #    count = count + 1
    raw_trace = sa.read()

    #####################################
    ### Save the trace data to a file ###
    #####################################
    trace_list = raw_trace.rsplit(',')
    if not os.path.isfile(spec_filename):
        n = open(spec_filename, 'w')
        if linear_sc:
            n.write('GHz,pwr\n')
        else:
            n.write('GHz,dB\n')
    else:
        n = open(spec_filename, 'a')
    for freq_index in range(len(freq_list)):
        write_line = str(freq_list[freq_index]) + "," + str(trace_list[freq_index]) + "\n"
        n.write(write_line)
    n.close()

    # check for errors
    sa.write('ERR?')
    error_code = sa.read()
    if error_code == '0':
        if verbose:
            print "no errors from spectrum analyzer"
    elif error_code == '112':
        print error_code, 'error code: unrecognized command'
    elif error_code == '109':
        print error_code, 'error code: Ctrl Fail, Analyzer was unable to take \
        control of the bus'
    else:
        print error_code, "error code"

    return

def getspec(spec_filename,
            verbose=False, linear_sc=True,
            freq_start=0.0, freq_stop=5.0,
            sweep_time='AUTO', video_band=10, resol_band=30, attenu=0,
            aveNum=1, lin_ref_lev=500):
    sweep_sleep = start_spec_grab(spec_filename=spec_filename,
                                  verbose=verbose, linear_sc=linear_sc,
                                  freq_start=freq_start, freq_stop=freq_stop,
                                  sweep_time=sweep_time, video_band=video_band,
                                  resol_band=resol_band, attenu=attenu,
                                  aveNum=aveNum, lin_ref_lev=lin_ref_lev)


    finish_spec_grab(spec_filename, freq_start=freq_start, freq_stop=freq_stop,
                     verbose=verbose, linear_sc=linear_sc)

    return


def getspecPlusTP(spec_filename, TP_filename, TPSampleFrequency, verbose=False, linear_sc=True,
                  freq_start=0.0, freq_stop=5.0, sweep_time='AUTO', video_band=10, resol_band=30, attenu=0,
                  aveNum=1, lin_ref_lev=500, get_total_power=True):
    sweep_sleep = start_spec_grab(spec_filename=spec_filename,
                                  verbose=verbose, linear_sc=linear_sc,
                                  freq_start=freq_start, freq_stop=freq_stop,
                                  sweep_time=sweep_time, video_band=video_band,
                                  resol_band=resol_band, attenu=attenu,
                                  aveNum=aveNum, lin_ref_lev=lin_ref_lev)
    if get_total_power:
        if verbose:
            print "Getting total power from the LabJack while sweeping for " + str('%2.3f' % sweep_sleep) + "s"
        # let the LabJack get total power data while the spectral sweep is taking place
        LJ_streamTP(TP_filename, TPSampleFrequency, sweep_sleep, verbose)

    finish_spec_grab(spec_filename, freq_start=freq_start, freq_stop=freq_stop,
                 verbose=verbose, linear_sc=linear_sc)

    return


def get_multi_band_spec(spec_filename, TP_filename, TPSampleFrequency, verbose=False, linear_sc=True,
                        spec_freq_vector=[], sweep_time='AUTO', video_band=10, resol_band=30, attenu=0,
                        aveNum=1, lin_ref_lev=500, get_total_power=True):

    len_spec_freq_vector = len(spec_freq_vector)
    if len_spec_freq_vector < 2:
        print "The frequency vector has less than 2 elements the function get_multi_band_specs requires a frequency\n"+\
              "vector with a length of 2 or greater. A length of 2 specifies a single band to sweep. This function\n"+\
              "return without doing anything. Bummer."
    else:
        for band_index in range(len_spec_freq_vector-1):
            getspecPlusTP(spec_filename=spec_filename, TP_filename=TP_filename,
                          TPSampleFrequency=TPSampleFrequency, verbose=verbose, linear_sc=linear_sc,
                          freq_start=spec_freq_vector[band_index], freq_stop=spec_freq_vector[band_index+1],
                          sweep_time=sweep_time, video_band=video_band, resol_band=resol_band, attenu=attenu,
                          aveNum=aveNum, lin_ref_lev=lin_ref_lev, get_total_power=get_total_power)



    return


def LOfreqSweep():
    from LOinput import setfreq
    from time import sleep
    from control import setmag_highlow, setSIS_only, setfeedback
    sleep_time = 10
    sisBias=59039
    sisShot=55000
    LOfreq_list = list(range(650,693))
    freq_vector = [0.4,1.0,1.6,2.2,2.8,3.4,4.0,4.6,5.2]
    test_dir = 'C:\\Users\\chwheele\\Google Drive\\Kappa\\NA38\\IVsweep\\IFsweep\\'

    setfeedback(True)
    setmag_highlow(100000)


    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    for LOfreq in LOfreq_list:
        setfreq(LOfreq)

        # biased SIS junction
        setSIS_only(sispot=sisBias,feedback=True)
        sleep(sleep_time)
        for freq_index in range(len(freq_vector)-1):
            getspecPlusTP(spec_filename=test_dir+str(LOfreq)+'spec_biased'+'.csv',
                          TP_filename=test_dir+str(LOfreq)+'_biased.csv',
                          TPSampleFrequency=100, verbose=True, linear_sc=True,
                          freq_start=freq_vector[freq_index], freq_stop=freq_vector[freq_index+1], sweep_time='AUTO', video_band=30, resol_band=30, attenu=0,
                          aveNum=16, lin_ref_lev=100)

        # normal SIS junction for shot noise source
        setSIS_only(sispot=sisShot,feedback=True)
        sleep(sleep_time)
        for freq_index in range(len(freq_vector)-1):
            getspecPlusTP(spec_filename=test_dir+str(LOfreq)+'spec_biased'+'.csv',
                          TP_filename=test_dir+str(LOfreq)+'_biased.csv',
                          TPSampleFrequency=100, verbose=True, linear_sc=True,
                          freq_start=freq_vector[freq_index], freq_stop=freq_vector[freq_index+1], sweep_time='AUTO', video_band=30, resol_band=30, attenu=0,
                          aveNum=16, lin_ref_lev=100)


    return
#######################
###### Test Area ######
#######################


if __name__ == "__main__":
    LOfreqSweep()



