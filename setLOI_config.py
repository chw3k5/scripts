####################
###### setLOI ######
####################

sleep_time = 1 # in seconds (time between setting the UCA value and first measuring the responce in the SIS bias)

# min and max accepted values
uA_max = 40
uA_min = 1

# Algoirthm Options
max_meas_per_loop = 12 # max numer of measurments that can be made for a single LO ajustmest before the program gives up and moves on.
scan_count_max    = 20 # max number of LO ajustments before the program gives up and moves on.
count_min         = 3  # min times to measure before a loop can be called complete
