def is_number(value):
    try:
        float(value)
        return True
    except ValueError:    
        return False

def getspec(filename, verbose=False, linear_sc=True, freq_start=0, freq_stop=6, sweep_time='AUTO', video_band=10,
            resol_band=30, attenu=0):
    import visa
    import numpy
    import time
        
    #datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/spectra/'
    #filename = 'C:\\Users\\MtDewar\\Documents\\Kappa\0\NA38\\test\\SpecTest.csv'
    
    sa = visa.instrument("GPIB0::5::INSTR")
    extra_sleep_fraction = 0.05 # fraction of the total sweep time to add to waiting time for a singe sweep
    extra_sleep_float    = 1.0  # seconds added to total sweep time, allows for IF switching in the Spectrum Analyzer
    
    #verbose    = True
    #linear_sc  = False # linear of logarithmic power scaling
    #freq_start = 0 # in GHz
    #freq_stop  = 12 # in GHz
    #sweep_time = 75 # in seconds
    #video_band = 10 # in MHz
    #resol_band = 10 # in MHz
    #attenu     = 0     # in dB form 0-70 in increments of 10
    
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
    ###############################
    ### make the frequency List ###
    ###############################
    freq_list=list(numpy.arange(freq_start, freq_stop,((freq_stop-freq_start)/600.0)))
    freq_list.append(freq_stop)
    
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
    sa.write("VAVG 1")
    #set the scale
    if linear_sc:
        sa.write("LN")
        # Reference Level
        sa.write("RL 400 uV")
    else:
        sa.write("LG 10DB")
    # put the 'trace data format' of returned values as real numbers, option P
    sa.write('tdf P')
    
    if is_number(sweep_time):
        sweep_time_float = float(sweep_time)
    else:
        sa.write('ST ?')
        sweep_time_float = float(sa.read())
    #################
    ### The Sweep ###
    #################
    # trigger a new sweep to start
    sa.write('clrw tra')
    extra_sleep = sweep_time_float*extra_sleep_fraction + extra_sleep_float
    sweep_sleep = sweep_time_float+extra_sleep
    if verbose:
        print "sweeping..."
        print "sleeping for " + str('%2.3f' % sweep_sleep) + "s"
    # let the script sleep while the sweep is being preformed
    time.sleep(sweep_sleep)

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
    n = open(filename, 'w')
    if linear_sc:
        n.write('GHz,pwr\n')
    else:
        n.write('GHz,dB\n')
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


def getspecPlusTP(spec_filename, TP_filename, TPSampleFrequency, verbose=False, linear_sc=True,
                  freq_start=0, freq_stop=6, sweep_time='AUTO', video_band=10, resol_band=30, attenu=0):
    import visa
    import numpy
    import time
    from control import LJ_streamTP

    #datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/spectra/'
    #filename = 'C:\\Users\\MtDewar\\Documents\\Kappa\0\NA38\\test\\SpecTest.csv'

    sa = visa.instrument("GPIB0::5::INSTR")
    extra_sleep_fraction = 0.05 # fraction of the total sweep time to add to waiting time for a singe sweep
    extra_sleep_float    = 1.0  # seconds added to total sweep time, allows for IF switching in the Spectrum Analyzer

    #verbose    = True
    #linear_sc  = False # linear of logarithmic power scaling
    #freq_start = 0 # in GHz
    #freq_stop  = 12 # in GHz
    #sweep_time = 75 # in seconds
    #video_band = 10 # in MHz
    #resol_band = 10 # in MHz
    #attenu     = 0     # in dB form 0-70 in increments of 10

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
    ###############################
    ### make the frequency List ###
    ###############################
    freq_list=list(numpy.arange(freq_start, freq_stop,((freq_stop-freq_start)/600.0)))
    freq_list.append(freq_stop)

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
    sa.write("VAVG 1")
    #set the scale
    if linear_sc:
        sa.write("LN")
        # Reference Level
        sa.write("RL 400 uV")
    else:
        sa.write("LG 10DB")
    # put the 'trace data format' of returned values as real numbers, option P
    sa.write('tdf P')

    if is_number(sweep_time):
        sweep_time_float = float(sweep_time)
    else:
        sa.write('ST ?')
        sweep_time_float = float(sa.read())
    #################
    ### The Sweep ###
    #################
    # trigger a new sweep to start
    sa.write('clrw tra')
    extra_sleep = sweep_time_float*extra_sleep_fraction + extra_sleep_float
    sweep_sleep = sweep_time_float+extra_sleep
    if verbose:
        print "sweeping..."
        print "Getting total power from the LabJack while sweeping for " + str('%2.3f' % sweep_sleep) + "s"
    # let the LabJack get total power data while the spectral sweep is taking place
    LJ_streamTP(TP_filename, TPSampleFrequency, sweep_sleep, verbose)
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
    n = open(spec_filename, 'w')
    if linear_sc:
        n.write('GHz,pwr\n')
    else:
        n.write('GHz,dB\n')
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

    return
#getspec('C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\test\\SpecTest.csv')