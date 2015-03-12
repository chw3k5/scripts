# from matplotlib import *
# from pylab      import *
# from zeropots   import zeropots
import time
import numpy
from control import LabJackU3_DAQ0, measSIS, setSIS_TP, setSIS_Volt, setmagI
from control import setSIS_only, setmag_only, measSIS_TP, zeropots, setfeedback, opentelnet, closetelnet
from LOinput import setfreq, RFon, RFoff

verbose = True
careful = True
feedback = True

start_stats =  5 # after x loops
total_loops = 100
sleep_time  =  1.0

reset       = True # there is no need to keep adjusting the magnet, sis voltage, and UCA voltage if you are doing multiple runs
turn_off    = False
magpot      = 90000 # pot position
pot_sis     =  56500 # pot position
UCA_voltage =  0 # in Volts
RFin        =   680 # in GHz

uA_list  = []
mV_list  = []
pot_list = []
tp_list  = []

mV_local_mean_str  = ''
mV_local_STD_str   = ''
mV_local_SEM_str   = ''
mV_local_max_str   = ''

uA_local_mean_str  = ''
uA_local_STD_str   = ''
uA_local_SEM_str   = ''
uA_local_max_str   = ''

pot_local_mean_str = ''
pot_local_STD_str  = ''
pot_local_SEM_str  = ''
pot_local_max_str  = ''

tp_local_mean_str  = ''
tp_local_STD_str   = ''
tp_local_SEM_str   = ''
tp_local_max_str   = ''

opentelnet()
RFon()
if reset:        
    setmag_only(magpot)
    status = setfeedback(feedback)
    setSIS_only(pot_sis, feedback, verbose, careful)
    status = LabJackU3_DAQ0(abs(UCA_voltage))
    setfreq(RFin)
else:
    mV_sis, uA_sis, pot_sis = measSIS(verbose)

for n in range(total_loops):

    mV_sis, uA_sis, tp_sis, pot_sis, time_stamp = measSIS_TP(pot_sis, feedback, verbose, careful)
    # do stats on all the readings
    uA_list.append(uA_sis)
    mV_list.append(mV_sis)
    pot_list.append(pot_sis)
    tp_list.append(tp_sis)
    
    uA_array  = numpy.array(uA_list)
    mV_array  = numpy.array(mV_list)
    pot_array = numpy.array(pot_list)
    tp_array  = numpy.array(tp_list)
    
    mV_run_mean  = numpy.mean(mV_array)
    uA_run_mean  = numpy.mean(uA_array)
    pot_run_mean = numpy.mean(pot_array)
    tp_run_mean  = numpy.mean(tp_array)
    
    mV_run_STD  = numpy.std(mV_array)
    uA_run_STD  = numpy.std(uA_array)
    pot_run_STD = numpy.std(pot_array)
    tp_run_STD  = numpy.std(tp_array)
    
    sqrter = numpy.sqrt(n+1)
    mV_run_SEM  = mV_run_STD/sqrter
    uA_run_SEM  = uA_run_STD/sqrter
    pot_run_SEM = pot_run_STD/sqrter
    tp_run_SEM  = tp_run_STD/sqrter
    
    mV_run_mean_str  = " Rmean:" + str('%02.3f' % mV_run_mean) + " "
    mV_run_STD_str   = " RSTD:" + str('%02.3f' % mV_run_STD) + " "
    mV_run_SEM_str   = " RSEM:" + str('%02.3f' % mV_run_SEM) + " "
    uA_run_mean_str  = " Rmean:" + str('%02.3f' % uA_run_mean) + " "
    uA_run_STD_str   = " RSTD:" + str('%02.3f' % uA_run_STD) + " "
    uA_run_SEM_str   = " RSEM:" + str('%02.3f' % uA_run_SEM) + " "
    pot_run_mean_str = " Rmean:" + str('%02.3f' % pot_run_mean) + " "
    pot_run_STD_str  = " RSTD:" + str('%02.3f' % pot_run_STD) + " "
    pot_run_SEM_str  = " RSEM:" + str('%02.3f' % pot_run_SEM) + " "
    tp_run_mean_str  = " Rmean:" + str('%02.3f' % tp_run_mean) + " "
    tp_run_STD_str   = " RSTD:" + str('%02.3f' % tp_run_STD) + " "
    tp_run_SEM_str   = " RSEM:" + str('%02.3f' % tp_run_SEM) + " "
    
    if n >= start_stats - 1:
        start_position = len(uA_list) - start_stats
        
        uA_array_local  = numpy.array(uA_list[start_position:])
        mV_array_local  = numpy.array(mV_list[start_position:])
        pot_array_local = numpy.array(pot_list[start_position:])
        tp_array_local  = numpy.array(tp_list[start_position:])
        
        mV_local_max  = numpy.max(mV_array_local)
        uA_local_max  = numpy.max(uA_array_local)
        pot_local_max = numpy.max(pot_array_local)
        tp_local_max  = numpy.max(tp_array_local)
        
        mV_local_mean  = numpy.mean(mV_array_local)
        uA_local_mean  = numpy.mean(uA_array_local)
        pot_local_mean = numpy.mean(pot_array_local)
        tp_local_mean  = numpy.mean(tp_array_local)
        
        mV_local_STD  = numpy.std(mV_array_local)
        uA_local_STD  = numpy.std(uA_array_local)
        pot_local_STD = numpy.std(pot_array_local)
        tp_local_STD  = numpy.std(tp_array_local)
        
        sqrter = numpy.sqrt(len(mV_array_local))
        mV_local_SEM  = mV_local_STD/sqrter
        uA_local_SEM  = uA_local_STD/sqrter
        pot_local_SEM = pot_local_STD/sqrter
        tp_local_SEM  = tp_local_STD/sqrter
        
        
        mV_local_mean_str  = str('%05.4f' % mV_local_mean)
        mV_local_STD_str   = str('%05.4f' % mV_local_STD)
        mV_local_SEM_str   = str('%05.4f' % mV_local_SEM)
        mV_local_max_str   = str('%05.4f' % mV_local_max)
        
        uA_local_mean_str  = str('%05.4f' % uA_local_mean)
        uA_local_STD_str   = str('%05.4f' % uA_local_STD)
        uA_local_SEM_str   = str('%05.4f' % uA_local_SEM) 
        uA_local_max_str   = str('%05.4f' % uA_local_max)
        
        pot_local_mean_str = str('%06.0f' % pot_local_mean) 
        pot_local_STD_str  = str('%02.4f' % pot_local_STD) 
        pot_local_SEM_str  = str('%02.4f' % pot_local_SEM)
        pot_local_max_str  = str('%02.4f' % pot_local_max)
        
        tp_local_mean_str  = str('%05.5f' % tp_local_mean) 
        tp_local_STD_str   = str('%05.5f' % tp_local_STD) 
        tp_local_SEM_str   = str('%05.5f' % tp_local_SEM)
        tp_local_max_str   = str('%05.5f' % tp_local_max)
    
    # print the measuement and stats
    meas = str('%02.4f' % uA_sis)  + " uA, " + str('%02.4f' % mV_sis) + " mV, " + str('%02.5f' % tp_sis) + " tp, " + str('%06.0f' % pot_sis)+" pot"
    ave  =       uA_local_mean_str + " uA, " + mV_local_mean_str      + " mV, " + tp_local_mean_str      + " tp " + " local mean: "+str(start_stats) + " measurments" 
    STD  =       uA_local_STD_str  + " uA, " + mV_local_STD_str       + " mV, " + tp_local_STD_str       + " tp " + " local  STD: "+str(start_stats) + " measurments"
    SED  =       uA_local_SEM_str  + " uA, " + mV_local_SEM_str       + " mV, " + tp_local_SEM_str       + " tp " + " local  SEM: "+str(start_stats) + " measurments"
    MAX  =       uA_local_max_str  + " uA, " + mV_local_max_str       + " mV, " + tp_local_max_str       + " tp " + " local  MAX: "+str(start_stats) + " measurments"
    
    #I=str('%02.2f' % uA_sis)+" uA " + uA_local_mean_str + uA_local_STD_str + uA_local_SEM_str + uA_run_mean_str + uA_run_STD_str + uA_local_SEM_str
    #V=str('%02.3f' % mV_sis)+" mV" + mV_local_mean_str + mV_local_STD_str + mV_local_SEM_str + mV_run_mean_str + mV_run_STD_str + mV_local_SEM_str
    #P=str('%06.0f' % pot_sis)+" pot" + pot_local_mean_str + pot_local_STD_str + pot_local_SEM_str + pot_run_mean_str + pot_run_STD_str + pot_local_SEM_str
    #T=str('%02.3f' % tp_sis)+" tp" + tp_local_mean_str + tp_local_STD_str + tp_local_SEM_str + tp_run_mean_str + tp_run_STD_str + tp_local_SEM_str
    
    #mV_sis, uA_sis, tp_sis, pot_sis
    print meas
    print ave
    print STD
    print SED
    print MAX
    print " "
    time.sleep(sleep_time)
closetelnet()

if turn_off:
    RFoff()
    zeropots()
print("End of script reached")
# zeropots()