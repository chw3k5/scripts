############################################
###### measmag # setmag # setmag_only ######
############################################

SleepPerMes  = 0.5 # in seconds

sleep_list = [0.3, 0.7, 2, 5, 10, 30, 60, 120]
    

######################
####### setmagI ######
######################

rail_meas = 5 # number of measurment to detemine the rail current

# Values not to exceed for the electromagnet pot position
max_pot_pos = 129797 # found by testing values by hand 
min_pot_pos = 0
    
# For Slope Estimation
high_pot_pos = 120000 # things can get funky around the rail positions
low_pot_pos = 10000

# The Searching Algorithm
loop1_thresh      = 0.005 # in mA estimated current change to user destination, under this value the algorithm is consider finished
pot_diff_thresh   = 8     # estimated post postion to user destination, under this value the algorithm is consider finished
loop1_max         = 25   # number of loops allowed; when carful is set
loop1_restar_max  = 10 # number of loops restarts for over shots allowed;, always on

# when the values get close to the user choosen position we measue more times to increase accuracy
subloop_max = 20  
subloop_min = 5

# this makes the step size finer as we get closer to the user specified currnet (mA) 
def step_decision(pot_diff, loop1_restar):
    if pot_diff <= 30:
        loop1_frac = 0.3
        subloop = True
        subloop_min = 10
    elif pot_diff <= 100:
        loop1_frac = 0.4
        subloop = True
        subloop_min = 5
    elif 1 <= loop1_restar:
        loop1_frac = 0.4
        subloop = False
        subloop_min = 5   
    elif pot_diff <= 500:
        loop1_frac = 0.6
        subloop = False
        subloop_min = 5
    else:
        loop1_frac = 0.9
        subloop = False
        subloop_min = 5
    return loop1_frac, subloop, subloop_min
    