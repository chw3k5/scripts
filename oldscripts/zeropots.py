def zeropots():
    import time
    import telnetlib
    #set the pot position of the magnet and recound the current and volage
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    time.sleep(1)
    tn.write('zeropots \n')
    time.sleep(1)
    tn.close()