def setfreq(freq=14):
    import visa
    import sys
    #freq = 0.0 # in GHz
    low_freq  = 13.541 # in GHz
    high_freq = 14.417 # in GHz
    ampl = 11.9 # in dBm
    
    low_LOfreq  = 650.0 # in GHz
    high_LOfreq = 692.0 # in GHz
    
    LOfreq_multiplier = 48.0
    # some error checking
    try:
        freq = float(freq)
    except ValueError:
        print "The frequency variable 'freq' was not a number. Killing script."
        sys.exit()
    
    # For frequencies specified in the range of the LO Output
    if ((low_LOfreq <= freq) and (freq <= high_LOfreq)):
        freq = freq/LOfreq_multiplier
    elif ((high_freq*2.0 <= freq) and (freq < low_LOfreq)):
        print "The frequency variable 'freq'=" + str(freq) + "GHz was a larger \
        value than the software maximum of 'high_freq'=" + str(high_freq) + \
        "GHz for the LO input and software minimuim of 'low_LOfreq'=" + \
        str(low_LOfreq) + "GHz for the LO output. Setting 'freq='" + \
        str(high_freq) + "GHz at the LO input for an LO output of ." + \
        str(high_freq*LOfreq_multiplier) + "GHz."
        freq = high_freq
    elif (high_LOfreq < freq):
        print "The frequency variable 'freq'=" + str(freq) + "GHz was a larger \
        value than the software maximum of 'high_LOfreq'=" + str(high_LOfreq) + \
        "GHz for the LO output. Setting 'freq='" + \
        str(high_freq) + "GHz at the LO input for an LO output of ." + \
        str(high_freq*LOfreq_multiplier) + "GHz."
        freq = high_freq
    else:
        # For frequencies specified in the range of the LO Input
        if high_freq < freq:
            print "The frequency variable 'freq'=" + str(freq) + " was a larger value than \
            the software maximum of 'high_freq'=" + str(high_freq) + ". Setting 'freq='" + str(high_freq) + "." 
            freq = high_freq
        else: # freq <= high_freq
            if freq < low_freq:
                print "The frequency variable 'freq'=" + str(freq) + " was a smaller value than \
                the software minimum of 'low_freq'=" + str(low_freq) + ". Setting 'freq='" + str(low_freq) + "." 
                freq = low_freq
    
    # set the insturments
    sa = visa.instrument("GPIB0::2::INSTR")
    sa.write('CF0 ' + str(freq) + ' GH')
    sa.write('L1 '  + str(ampl) + ' DM')
    return
    
def RFon():
    import visa
    sa = visa.instrument("GPIB0::2::INSTR")
    sa.write('RF1')
    return
    
def RFoff():
    import visa
    sa = visa.instrument("GPIB0::2::INSTR")
    sa.write('RF0')
    return
    
def rfon():
    RFon()
    return
    
def rfoff():
    RFoff()
    return