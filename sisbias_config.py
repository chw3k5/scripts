########################################################
###### measSIS # setSIS # setSIS_only # setSIS_TP ######
########################################################

SleepPerMes  = 0.3 # in seconds
# the below are not needed in setSIS_only
sleep_list = [0.3, 0.7, 2, 5, 10, 30, 60, 120]

#########################
###### setfeedback ######
#########################

SleepPerMes_feedback = 0.5 # in seconds


##################################
###### setSIS # setSIS_only ######
##################################

## Pot positions not to exceed
#feedback = True (on)
feedon_low  = 30000
feedon_high = 100000
# feedback = False (off)
feedoff_low = 53000
feedoff_high = 77000


#########################
###### setSIS_Volt ######
#########################

mV_max           =  6.5    # mV
mV_min           = -6.5    # mV

loop_thresh      = 0.004 # in mV estimated voltage change to user destination, under this value the first loop is consider finished
pot_diff_thresh  = 5     # estimated post position to user destination, under this value first loop is consider finished
loop_max         = 35    # number of loops allowed; when careful is set
loop_hard_max    = 40    # number of loops allowed; always on

SEM_user         = 0.100 # mV Standard error of the mean. Loop until we know the mean value of the voltage to this precision
subloop_min      = 5     # the subloop will run at least this many times
subloop_max      = 20    # number of loops allowed; when careful is set
subloop_hard_max = 30    # number of loops allowed; always on

SEM_user2      = 0.10    # mV Standard error of the mean. Loop until we know the mean value of the voltage to this precision
loop3_min      = 5       # the loop3 will run at least this many times
loop3_max      = 12      # number of loops allowed; when careful is set
loop3_hard_max = 30      # number of loops allowed; always on

high_pot_pos_defult = 85000 
low_pot_pos_defult  = 35000
    
check_radius  = 5
pot_per_check = 50
bound_diff = 0.01 # in mV This is the difference needed between the boundaries values in the check loop and the minimum value found
restart_count_max = 5 # Number of time the check part of the algorithm is allow to restart. if careful is on, the script will exit after this number
show_plot = True
    
min_cdf = 0.90 # fraction of gaussian computed
sigma   = 40    # in pot positions

intep_meas  = 5 # number of time to measure for the linear interpolation
unstick_max = 3

######################
###### zeropots ######
######################

zeropots_center_pos = 65100
zeropots_feedback   = False
zeropots_careful    = True

zeropots_max_count  = 5 # max number of retries to zero pots

zeropots_do_mag = True
zeropots_do_sis = True
zeropots_do_LO  = True

UCA_voltage     = 0 #in Volts. 0 is LO full on 5 is LO totally attenuated  