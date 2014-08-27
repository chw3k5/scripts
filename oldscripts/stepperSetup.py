###########################################################################
# Connect to the Parker Gemini 6K controller, microstepping drive, and
#     stepper motor via serial port.
# Required Python packages:  visa
# Linda Kuenzi (lkuenzi@asu.edu)
# Last updated 11/8/2013

###########################################################################
## SETUP: Communicate with Controller and Drive

from visa import *
print "Connecting to stepper controller...\n"

# Create stepper object (with correct serial port)
stepper = SerialInstrument("COM4",baud_rate = 9600, data_bits = 8, stop_bits = 1)
    # COM2 = USB on front panel of desktop lab computer
    # COM3 = right serial port at bottom of lab computer back panel
    # COM4 = left serial port
time.sleep(1)
# Set time to wait before sending commands (seconds)
stepper.delay = 0.2

###########################################################################
## GENERAL SETTINGS: Movement and Scaling

# Disable drive
stepper.write('DRIVE0')

# Set drive resolution to 25,000 microsteps
stepper.write('DRES25000')

# Set scaling so that '1' represents 1 revolution
stepper.write('SCLD25000')
stepper.write('SCLV25000')
stepper.write('SCLA25000')

# Enable scaling
stepper.write('SCALE1')          

# Define axis:  0 = stepper, 1 = servo
stepper.write('AXSDEF0')

# Hardware End-of-Travel Limit:
	# 0 = disable limits
	# 1-3 = enable motion restrictions in certain directions
stepper.write('LH0')

# Behavior on stop input or Stop command (!S):
	# 0 = discard commands in buffer and terminate program execution
	# 1 = pause command execution, continue with !C command
stepper.write('COMEXS1')

# Continuous command processing mode:  0 = disable (pause until motion is complete), 1 = enable
stepper.write('COMEXC0')

# Preset mode (0) = move specified distance
# Continuous mode (1) = move at specified velocity
stepper.write('MC0')

# Incremental mode (0) = move w.r.t. position at start of move
# Absolute mode (1) = move w.r.t. absolute zero
stepper.write('MA0')

# Set current position as 0
stepper.write('PSET0')

###########################################################################
## MOTION SETTINGS:  Acceleration, Velocity

# Change/update values here:
stepper.write('A1')      # Acceleration (revolutions/s^2)
stepper.write('AD1')     # Deceleration (rev/s^2)
stepper.write('V1')      # Velocity (rev/s)

# Set distance to 1/4th turn
stepper.write('D0.25')

###########################################################################
## MAKE THINGS GO IN CIRCLES

# stepper.write('DRIVE1')
# stepper.write('GO1')