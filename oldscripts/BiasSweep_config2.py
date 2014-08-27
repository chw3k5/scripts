###############################
####### General Options #######
###############################

verbose     = True
verboseTop  = True
careful     = False


datadir     = '/Users/chw3k5/Dropbox/kappa_data/NA38/IVsweep/set4/'
sweepNstart = 0   # (defult = 0) starts on number after this, changes every sweep to be unique for each sweep
Ynum        = 0   # (defult = 0) starts on number after this, changes every sweep to be unique for each sweep

#############################
####### Sweep Options #######
#############################

sisV_feedback    = True

# sis mV sweep
do_sisVsweep = True # set to 'True', I never wrote the part of the code that lets this be False

high_res_meas = 10 # number of measurments while sisVsweep is ocurring

TPSampleFrequency = 100 # samples per second
TPSampleTime      =   5 # seconds  

sisvsweep_min  = -0.1 # mV, -6 mV min
sisvsweep_max  = 2.3 # mV,  6 mV max
sisvsweep_step = 0.05 # mV

do_fastsweep         = True
do_unpumpedsweep     = True
fastsweep_feedback   = False # also used by unpumpedsweep
SweepStart_feedTrue  = 65000  # defult is 65000 for feedback on
SweepStop_feedTrue   = 52000  # defult is 52000 for feedback on
SweepStep_feedTrue   = 100     # defult is 50

SweepStart_feedFalse = 65100  # defult is 65100 for feedback off 
SweepStop_feedFalse  = 57000  # defult is 62000 for feedback off
SweepStep_feedFalse  = 100     # defult is 50

# 0 changes the most often, the higher the axis the less common switching becomes
Kaxis      = 0 # should be set to 0 always
magaxis    = 1
LOpowaxis  = 2
LOfreqaxis = 3
IFbandaxis = 4

K_array       = [296, 80] # Kelvin, [77], [300], [77, 300], or [300, 77]
LOfreq_array  = [672]     # in GHz, must be singular for now
IFband_array  = [1.42]    # in GHz,  must be singular for now

do_magisweep   = True
mag_meas_after_set = 20 # measurments

magisweep_min  = 36.0 # mA, -42 in min 
magisweep_max  = 23.0 # mA,  42 is max
magisweep_step = -0.2 # mA

magpotsweep_min  = 100000 # potentiometer position,       0 is min 
magpotsweep_max  = 100001 # potentiometer position, 1279797 is max
magpotsweep_step =   5000 # potentiometer position


do_sisisweep   = True
UCA_set_pot    = 56800 # mV
UCA_meas_after_set = 20 # measurments

sisisweep_min  = 14.0 # uA
sisisweep_max  =  4.0 # uA
sisisweep_step = -1.0 # uA
sisi_magpot    = 103323
sisi_cheat_num = 56666 # pot position

UCAsweep_min  = 3.45
UCAsweep_max  = 3.46
UCAsweep_step = 0.05

#########################
###### Sweep Shape ######
#########################

sweepShape  = "rectangular" # rectangular,

#############################
####### Email Options #######
#############################
FinishedEmail   = True
FiveMinEmail    = True
PeriodicEmail   = True
seconds_per_email = 20*60 # seconds (60 s = 1 min, 3600 s = 1 hour ) 

#########################
###### Definitions ######
#########################

# Some definitions I used to make the parapameter arrays, this can get pretty hairy
def makeparamslist_Rec(K_array, LOfreq_array, IFband_array):
    import numpy
    # some if statments to determine what state the code will run in 
    # Magnet, LO power
    list_len = 1
    axis_num = 0
    K_array = numpy.array(K_array)
    LOfreq_array = numpy.array(LOfreq_array)
    IFband_array = numpy.array(IFband_array)
    
    if sweepShape == "rectangular":
        #### Make 1D arrays
        
        # For the temperature measurements    
        K_array_len = len(K_array)
        list_len    = list_len*K_array_len
	axis_num    = axis_num + 1
        
        # Electromagnet
        if do_magisweep:
            mag_array      = numpy.arange(magisweep_min, magisweep_max, magisweep_step)
            Emag_array_len = len(mag_array)
            list_len       = list_len*Emag_array_len
            Emag_array     = mag_array
            magpot_array   = [] 
            axis_num       = axis_num +1
        else:
            magpot_array   = numpy.arange(magpotsweep_min, magpotsweep_max, magpotsweep_step)
            Emag_array_len = len(magpot_array)
            list_len       = list_len*Emag_array_len
            Emag_array     = magpot_array
            mag_array      = []
            axis_num       = axis_num +1
            
        # LO power
        if do_sisisweep:
            sisi_array      = numpy.arange(sisisweep_min, sisisweep_max, sisisweep_step)
            list_len        = list_len*len(sisi_array)
            LOpow_array_len = len(sisi_array)
            LOpow_array     = sisi_array
            UCA_array       = []
            axis_num        = axis_num +1
        else:
            UCA_array       = numpy.arange(UCAsweep_min, UCAsweep_max, UCAsweep_step)
            list_len        = list_len*len(UCA_array)
	    LOpow_array_len = len(UCA_array)
            LOpow_array     = UCA_array
            sisi_array      = []
            axis_num        = axis_num +1
            
        # LOfreq_array
        LOfreq_array_len = len(LOfreq_array)
        list_len         = list_len*LOfreq_array_len
        axis_num         = axis_num + 1
        
        # IFband_array
        IFband_array_len = len(IFband_array)
        list_len         = list_len*IFband_array_len
        axis_num         = axis_num + 1
        
        zero_array   = []
        zero_len     = []
        first_array  = []
        first_len    = []
        second_array = []
        second_len   = []
        third_array  = []
        third_len    = []
        forth_array  = []
        forth_len    = []
        
        axis0 = magaxis 
        ass0_array     = Emag_array
        ass0_array_len = Emag_array_len
        
        axis1 = LOpowaxis
        ass1_array     = LOpow_array
        ass1_array_len = LOpow_array_len
        
        axis2 = Kaxis
        ass2_array     = K_array
        ass2_array_len = K_array_len
        
        axis3 = LOfreqaxis
        ass3_array     = LOfreq_array
        ass3_array_len = LOfreq_array_len
        
        axis4 = IFbandaxis
        ass4_array     = IFband_array
        ass4_array_len = IFband_array_len
        
        zero_array, zero_len, first_array, first_len, second_array, second_len, third_array, third_len, forth_array, forth_len = arrayMapperTO(axis0, ass0_array, ass0_array_len, axis1, ass1_array, ass1_array_len, axis2, ass2_array, ass2_array_len, axis3, ass3_array, ass3_array_len, axis4, ass4_array, ass4_array_len)


        # make the list make runns of different sets of parameters
        zero_array, first_array, zero_len, first_len = param_array(zero_array, first_array, zero_len, first_len)
        
        second_array_temp = second_array
        second_len_temp   = second_len
        zero_array,  second_array, zero_len,  second_len = param_array(zero_array,  second_array_temp, zero_len,  second_len_temp)
        first_array, second_array, first_len, second_len = param_array(first_array, second_array_temp, first_len, second_len_temp)
        
        third_array_temp = third_array
        third_len_temp   = third_len
        zero_array,   third_array, zero_len,   third_len = param_array(zero_array,   third_array_temp, zero_len,   third_len_temp)
        first_array,  third_array, first_len,  third_len = param_array(first_array,  third_array_temp, first_len,  third_len_temp)
        second_array, third_array, second_len, third_len = param_array(second_array, third_array_temp, second_len, third_len_temp)
        
        forth_array_temp = forth_array
        forth_len_temp   = forth_len
        zero_array,   forth_array, zero_len,   forth_len = param_array(zero_array,   forth_array_temp, zero_len,   forth_len_temp)
        first_array,  forth_array, first_len,  forth_len = param_array(first_array,  forth_array_temp, first_len,  forth_len_temp)
        second_array, forth_array, second_len, forth_len = param_array(second_array, forth_array_temp, second_len, forth_len_temp)  
        third_array, forth_array,  third_len,  forth_len = param_array(third_array,  forth_array_temp, third_len, forth_len_temp) 
        
        #zero_list   = list(zero_array)
        #first_list  = list(first_array)
        #second_list = list(second_array)
        #third_list  = list(third_array)
        #forth_list  = list(forth_array)
        
        if magaxis == 0:
            Emag_array = zero_array
        elif magaxis == 1:
            Emag_array = first_array
        elif magaxis == 2:
            Emag_array = second_array
        elif magaxis == 3:
            Emag_array = third_array
        elif magaxis == 4:
            Emag_array = forth_array
            
        if LOpowaxis == 0:
            LOpow_array = zero_array
        elif LOpowaxis == 1:
            LOpow_array = first_array
        elif LOpowaxis == 2:
            LOpow_array = second_array
        elif LOpowaxis == 3:
            LOpow_array = third_array
        elif LOpowaxis == 4:
            LOpow_array = forth_array
            
        if Kaxis == 0:
            K_array = zero_array
        elif Kaxis == 1:
            K_array = first_array
        elif Kaxis == 2:
            K_array = second_array
        elif Kaxis == 3:
            K_array = third_array
        elif Kaxis == 4:
            K_array = forth_array
            
        if LOfreqaxis == 0:
            LOfreq_array = zero_array
        elif LOfreqaxis == 1:
            LOfreq_array = first_array
        elif LOfreqaxis == 2:
            LOfreq_array = second_array
        elif LOfreqaxis == 3:
            LOfreq_array = third_array
        elif LOfreqaxis == 4:
            LOfreq_array = forth_array
            
        if IFbandaxis == 0:
            IFband_array = zero_array
        elif IFbandaxis == 1:
            IFband_array = first_array
        elif IFbandaxis == 2:
            IFband_array = second_array
        elif IFbandaxis == 3:
            IFband_array = third_array
        elif IFbandaxis == 4:
            IFband_array = forth_array
    
    Emag_list    = list(Emag_array)
    LOpow_list   = list(LOpow_array)
    K_list       = list(K_array)
    LOfreq_list  = list(LOfreq_array)
    IFband_list  = list(IFband_array)
            
    return Emag_list, LOpow_list, K_list, LOfreq_list, IFband_list
    
def param_array(zero_array, first_array, zero_len, first_len):
    import numpy
    loop_over = (first_len) - 1
    temp0_array = zero_array
    new_len = zero_len*first_len
    for n in range(loop_over):
        temp0_array = numpy.vstack((temp0_array, zero_array))
    zero_array = temp0_array
    zero_array = numpy.reshape(zero_array, new_len)
    
    loop_over = (zero_len) - 1
    temp1_array = first_array
    for n in range(loop_over):
        temp1_array = numpy.vstack((temp1_array, first_array))
    first_array = numpy.transpose(temp1_array)
    first_array = numpy.reshape(first_array, new_len)
    zero_len    = new_len
    first_len   = new_len
    return zero_array, first_array, zero_len, first_len
    
def arrayMapperTO(axis0, ass0_array, ass0_array_len, axis1, ass1_array, ass1_array_len, axis2, ass2_array, ass2_array_len, axis3, ass3_array, ass3_array_len, axis4, ass4_array, ass4_array_len):
    if axis0 == 0:
        zero_array   = ass0_array
        zero_len     = ass0_array_len
    elif axis0 == 1:
        first_array  = ass0_array
        first_len    = ass0_array_len
    elif axis0 == 2:
        second_array = ass0_array
        second_len   = ass0_array_len 
    elif axis0 == 3:
        third_array  = ass0_array
        third_len    = ass0_array_len
    elif axis0 == 4:
        forth_array  = ass0_array
        forth_len    = ass0_array_len
        
    if axis1 == 0:
        zero_array   = ass1_array
        zero_len     = ass1_array_len
    elif axis1 == 1:
        first_array  = ass1_array
        first_len    = ass1_array_len
    elif axis1 == 2:
        second_array = ass1_array
        second_len   = ass1_array_len 
    elif axis1 == 3:
        third_array  = ass1_array
        third_len    = ass1_array_len
    elif axis1 == 4:
        forth_array  = ass1_array
        forth_len    = ass1_array_len
        
    if axis2 == 0:
        zero_array   = ass2_array
        zero_len     = ass2_array_len
    elif axis2 == 1:
        first_array  = ass2_array
        first_len    = ass2_array_len
    elif axis2 == 2:
        second_array = ass2_array
        second_len   = ass2_array_len 
    elif axis2 == 3:
        third_array  = ass2_array
        third_len    = ass2_array_len
    elif axis2 == 4:
        forth_array  = ass2_array
        forth_len    = ass2_array_len

    if axis3 == 0:
        zero_array   = ass3_array
        zero_len     = ass3_array_len
    elif axis3 == 1:
        first_array  = ass3_array
        first_len    = ass3_array_len
    elif axis3 == 2:
        second_array = ass3_array
        second_len   = ass3_array_len 
    elif axis3 == 3:
        third_array  = ass3_array
        third_len    = ass3_array_len
    elif axis3 == 4:
        forth_array  = ass3_array
        forth_len    = ass3_array_len

    if axis4 == 0:
        zero_array   = ass4_array
        zero_len     = ass4_array_len
    elif axis4 == 1:
        first_array  = ass4_array
        first_len    = ass4_array_len
    elif axis4 == 2:
        second_array = ass4_array
        second_len   = ass4_array_len 
    elif axis4 == 3:
        third_array  = ass4_array
        third_len    = ass4_array_len
    elif axis4 == 4:
        forth_array  = ass4_array
        forth_len    = ass4_array_len
        
    return zero_array, zero_len, first_array, first_len, second_array, second_len, third_array, third_len, forth_array, forth_len
