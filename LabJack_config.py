#########################
###### LJ_streamTP ######
#########################

NumChannels = 1
# The number of times each second that each channel will be sampled

#SampleFrequency = 5000

Resolution = 0 # 0,1,2, or 3 () is highest resolution, 3 is the lowest)

# Where the data will be written
#filename = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test/data.txt'

# Put a list of strings with the names you would like associated with
# chan0, chan1, ... Example: wavenames = ['sync', 'V_in', 'V_out']
# If left blank, it will be filled with ['wave0', 'wave1', ...]
wavenames = ['tp']

# max measurments
loop_max = 3600 # in loop number, bige set of data have to be broken into several packets per time 


