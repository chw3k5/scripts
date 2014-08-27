def setfeedback(feedback):
    import telnetlib
    import time
    
    status=False
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    if feedback:
        tn.write("feedback 1 \n")
        time.sleep(1)
    else:
        tn.write("feedback 0 \n")
        time.sleep(1)
    out1 = tn.read_very_eager()
    if feedback:
        if out1 == 'Enabling SIS feedback loop (V-mode)\n':
            status=True
        else:
            print "the feedback command did not get the expected string <Enabling SIS feedback loop (V-mode)\n>. Check the connection to the THz bias computer"
    elif not feedback:
        if out1 == 'Disabling SIS feedback loop (R-mode)\n':
            status=True
        else:
            print "the feedback command did not get the expected string <Disabling SIS feedback loop (R-mode)\n>. Check the connection to the THz bias computer"
    else:
        print 'The variable feedback can only be True or False. Returning status=False'    
    tn.close()
    
    return status 