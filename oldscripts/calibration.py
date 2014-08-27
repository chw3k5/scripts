def magcal(filename, potstep, MesPerPot):
    import telnetlib
    import time
    import numpy
    import sys 
    
    
    #filename   = "magcal.csv"
    #potstep    = 1000
    #MesPerPot  = 9 # should be an odd number for Median calulation
    filedir     = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/mag/"
    savefile    = filedir+filename
    sweep_vals  = range(0,129999,potstep)
    SleepPerMes = 0.5
    
    sweep_Num = len(sweep_vals)
    #V_mean    = numpy.zeros(len(sweep_vals)-1)
    #mA_mean   = numpy.zeros(len(sweep_vals)-1)
    #V_median  = numpy.zeros(len(sweep_vals)-1)
    #mA_median = numpy.zeros(len(sweep_vals)-1)
    #V_stdev   = numpy.zeros(len(sweep_vals)-1)
    #mA_stdev  = numpy.zeros(len(sweep_vals)-1)
    f = open(savefile, 'w')
    f.write('pot, V_mean, mA_mean, V_median, mA_median, V_stdev, mA_stdev \n')
    
    tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
    for n in range(sweep_Num):
        sweep_val=sweep_vals[n]
        V_mag  = numpy.zeros(MesPerPot)
        mA_mag = numpy.zeros(MesPerPot)
        
        #set the pot position of the magnet and recound the current and volage
        tn.write("setbias 9 "+str(sweep_val) + " \n")
        time.sleep(1)
        
        for m in range(MesPerPot):
            tn.write("setbias 9 \n")
            time.sleep(SleepPerMes)
            out1 = tn.read_very_eager()
            out2 = out1.replace('mag 1 ', '')
            out3 = out2.replace(' = ', ',')
            
            end_position1=out3.find('\n', 0)
            V_string=out3[0:end_position1]
            
            end_position2=out3.find('\n', end_position1+1)
            mA_string=out3[end_position1+1:end_position2]
            
            end_position3=out3.find('\n', end_position2+1)
            t_string=out3[end_position2+1:end_position3]
            
            end_position4=out3.find('\n', end_position3+1)
            pot_string=out3[end_position3+1:end_position4]
            
            V_start=V_string.find(',',0)
            mA_start=mA_string.find(',',0)
            
            V_mag_temp=V_string[V_start+1:]
            mA_mag_temp=mA_string[mA_start+1:]
            
            if (V_mag_temp == '' or mA_mag_temp == '' or t_string == '' or pot_string == ''):
                print "Had to wait extra time for the measurment to be returned"
                tn.write("setbias 9 \n")
                time.sleep(1)
                out1 = tn.read_very_eager()
                out2 = out1.replace('mag 1 ', '')
                out3 = out2.replace(' = ', ',')
                
                end_position1=out3.find('\n', 0)
                V_string=out3[0:end_position1]
            
                end_position2=out3.find('\n', end_position1+1)
                mA_string=out3[end_position1+1:end_position2]
                
                            
                end_position3=out3.find('\n', end_position2+1)
                t_string=out3[end_position2+1:end_position3]
            
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
            
                V_start=V_string.find(',',0)
                mA_start=mA_string.find(',',0)
            
                V_mag_temp=V_string[V_start+1:]
                mA_mag_temp=mA_string[mA_start+1:]
                
                if ((V_mag_temp == '' or mA_mag_temp == '' or t_string == '' or pot_string == '')):
                    print "Had to wait extra time for the measurment to be returned again"
                    tn.write("setbias 9 \n")
                    time.sleep(5)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('mag 1 ', '')
                    out3 = out2.replace(' = ', ',')
                
                    end_position1=out3.find('\n', 0)
                    V_string=out3[0:end_position1]
                
                    end_position2=out3.find('\n', end_position1+1)
                    mA_string=out3[end_position1+1:end_position2]
                               
                    end_position3=out3.find('\n', end_position2+1)
                    t_string=out3[end_position2+1:end_position3]
            
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                
                    V_start=V_string.find(',',0)
                    mA_start=mA_string.find(',',0)
                
                    V_mag_temp=V_string[V_start+1:]
                    mA_mag_temp=mA_string[mA_start+1:]
                    
                    if ((V_mag_temp == '' or mA_mag_temp == '' or t_string == '' or pot_string == '')):
                        print "Had to wait extra time for the measurment to be returned again x2"
                        print out3
                        print "V_mag_temp  ="+V_mag_temp
                        print "mA_mag_temp ="+mA_mag_temp
                        print "t_string    ="+t_string
                        print "pot_string  ="+pot_string
                        print " "
                        tn.close()
                        time.sleep(5)
                        tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                        time.sleep(5)
                        tn.write("setbias 9 \n")
                        time.sleep(15)
                        out1 = tn.read_very_eager()
                        out2 = out1.replace('mag 1 ', '')
                        out3 = out2.replace(' = ', ',')
                    
                        end_position1=out3.find('\n', 0)
                        V_string=out3[0:end_position1]
                    
                        end_position2=out3.find('\n', end_position1+1)
                        mA_string=out3[end_position1+1:end_position2]
                                   
                        end_position3=out3.find('\n', end_position2+1)
                        t_string=out3[end_position2+1:end_position3]
            
                        end_position4=out3.find('\n', end_position3+1)
                        pot_string=out3[end_position3+1:end_position4]
                    
                        V_start=V_string.find(',',0)
                        mA_start=mA_string.find(',',0)
                    
                        V_mag_temp=V_string[V_start+1:]
                        mA_mag_temp=mA_string[mA_start+1:]

                        
                        
                        if ((V_mag_temp == '' or mA_mag_temp == '' or t_string == '' or pot_string == '')):
                            print "Had to wait extra time for the measurment to be returned again x3"
                            print out3
                            print "V_mag_temp  ="+V_mag_temp
                            print "mA_mag_temp ="+mA_mag_temp
                            print "t_string    ="+t_string
                            print "pot_string  ="+pot_string
                            print " "
                            tn.close()
                            time.sleep(5)
                            tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                            time.sleep(5)
                            
                            tn.write("setbias 9 \n")
                            time.sleep(30)
                            out1 = tn.read_very_eager()
                            out2 = out1.replace('mag 1 ', '')
                            out3 = out2.replace(' = ', ',')
                        
                            end_position1=out3.find('\n', 0)
                            V_string=out3[0:end_position1]
                        
                            end_position2=out3.find('\n', end_position1+1)
                            mA_string=out3[end_position1+1:end_position2]
                            
                                       
                            end_position3=out3.find('\n', end_position2+1)
                            t_string=out3[end_position2+1:end_position3]
            
                            end_position4=out3.find('\n', end_position3+1)
                            pot_string=out3[end_position3+1:end_position4]
                        
                            V_start=V_string.find(',',0)
                            mA_start=mA_string.find(',',0)
                        
                            V_mag_temp=V_string[V_start+1:]
                            mA_mag_temp=mA_string[mA_start+1:]
                        
                            if (V_mag_temp == '' or mA_mag_temp == '' or t_string == '' or pot_string == ''):
                                print "The script had to wait to long to read a value of mV and uA"
	                        print "Killing the script"
	                        print out3
                                print "V_mag_temp  ="+V_mag_temp
                                print "mA_mag_temp ="+mA_mag_temp
                                print "t_string    ="+t_string
                                print "pot_string  ="+pot_string
                                print " "
        	                sys.exit()
            
            V_mag[m]=float(V_string[V_start+1:])
            mA_mag[m]=float(mA_string[mA_start+1:])
            
        # End of MesPerPot loop
        f.write(str(sweep_val)+','+str(numpy.mean(V_mag))+','+str(numpy.mean(mA_mag))+','+str(numpy.median(V_mag))+','+str(numpy.median(mA_mag))+','+str(numpy.std(V_mag))+','+str(numpy.std(mA_mag))+'\n')   
        print str(n+1)+' of '+str(sweep_Num)+ ' magnet calibration measurments have been completed'   
    # End of Mag sweeping loop   
    tn.write("setbias 9 65100 \n")
    time.sleep(2)
    tn.close()
    f.close()
    return
    
def LOcal(filenotes, biaspot_feedoff, biaspot_feedon, UCAs, NumOfMeasu, IF_band, LO_val):
    import telnetlib
    import time
    import numpy
    import sys
    from setfeedback    import setfeedback
    from LabJackU3_DAQ0 import LabJackU3_DAQ0
    from zeropots       import zeropots
    
    #LO_val          = 672
    #biaspot_feedoff = range(63000, 58000, -1000)
    #biaspot_feedon  = range(60000, 54000, -1000) 
    #UCAs            = numpy.arange(3.00, 4.501, 0.01)  
    #filenotes   = "1"
    #NumOfMeasu  = 9 # should be an odd number for Median calulation
    filedir     = "/Users/chw3k5/Documents/Grad_School/Kappa/NA38/calibration/LO/"
    SleepPerMes = 0.5
    
    sNum_feedoff = len(biaspot_feedoff)
    sNum_feedon  = len(biaspot_feedon)
    sNum_UCA     = len(UCAs)
    
    print sNum_feedoff
    print sNum_feedon
    print sNum_UCA
    print NumOfMeasu
    
    for q in range(sNum_feedoff):
        status = setfeedback(False) 
        ### Start feedback off cal    
        savefile    = filedir + "LOcal_LO"+str(LO_val)+"_IF"+str(IF_band)+"_biaspot"+str(biaspot_feedoff[q])+"_feedbackOFF"+"_notes"+filenotes+".csv"
        f = open(savefile, 'w')
        f.write('UCA, mV_mean, uA_mean, mV_median, uA_median, nV_stdev, uA_stdev \n')
        
        #set the pot position of the of the SIS bias
        tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
        tn.write("setbias 0 "+str(biaspot_feedoff[q]) + " \n")
        time.sleep(1)
        
        for n in range(sNum_UCA):
            UCA=UCAs[n]
            mV_mag  = numpy.zeros(NumOfMeasu)
            uA_mag = numpy.zeros(NumOfMeasu)
            
            # Set the UCA voltage for the LO
            status = LabJackU3_DAQ0(UCA)
            time.sleep(1)
            if not status:
                print "The program LabJackU3_DAQ0 returned status=False"
                print "filename="+savefile
                sys.exit()
            
            for m in range(NumOfMeasu):
                tn.write("setbias 0 \n")
                time.sleep(SleepPerMes)
                out1 = tn.read_very_eager()
                out2 = out1.replace('sis 0 ', '')
                out3 = out2.replace(' = ', ',')
                
                end_position1=out3.find('\n', 0)
                mV_string=out3[0:end_position1]
                
                end_position2=out3.find('\n', end_position1+1)
                uA_string=out3[end_position1+1:end_position2]
                
                end_position3=out3.find('\n', end_position2+1)
                t_string=out3[end_position2+1:end_position3]
                
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
                
                mV_start=mV_string.find(',',0)
                uA_start=uA_string.find(',',0)
                
                mV_mag_temp=mV_string[mV_start+1:]
                uA_mag_temp=uA_string[uA_start+1:]
                
                if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                    print "Had to wait extra time for the measurment to be returned"
                    tn.write("setbias 0 \n")
                    time.sleep(1)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('sis 0 ', '')
                    out3 = out2.replace(' = ', ',')
                    
                    end_position1=out3.find('\n', 0)
                    mV_string=out3[0:end_position1]
                    
                    end_position2=out3.find('\n', end_position1+1)
                    uA_string=out3[end_position1+1:end_position2]
                    
                    end_position3=out3.find('\n', end_position2+1)
                    t_string=out3[end_position2+1:end_position3]
                    
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                    
                    mV_start=mV_string.find(',',0)
                    uA_start=uA_string.find(',',0)
                    
                    mV_mag_temp=mV_string[mV_start+1:]
                    uA_mag_temp=uA_string[uA_start+1:]
                    
                    if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                        print "Had to wait extra time for the measurment to be returned again"
                        tn.write("setbias 0 \n")
                        time.sleep(5)
                        out1 = tn.read_very_eager()
                        out2 = out1.replace('sis 0 ', '')
                        out3 = out2.replace(' = ', ',')
                        
                        end_position1=out3.find('\n', 0)
                        mV_string=out3[0:end_position1]
                        
                        end_position2=out3.find('\n', end_position1+1)
                        uA_string=out3[end_position1+1:end_position2]
                        
                        end_position3=out3.find('\n', end_position2+1)
                        t_string=out3[end_position2+1:end_position3]
                        
                        end_position4=out3.find('\n', end_position3+1)
                        pot_string=out3[end_position3+1:end_position4]
                        
                    	mV_start=mV_string.find(',',0)
                        uA_start=uA_string.find(',',0)
                        
                        mV_mag_temp=mV_string[mV_start+1:]
                        uA_mag_temp=uA_string[uA_start+1:]
                        
                        if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                            print "Had to wait extra time for the measurment to be returned again x2"
                            tn.close()
                            time.sleep(5)
                            tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                            time.sleep(5)
                            tn.write("setbias 0 \n")
                            time.sleep(15)
                            out1 = tn.read_very_eager()
                            out2 = out1.replace('sis 0 ', '')
                            out3 = out2.replace(' = ', ',')
                            
                            end_position1=out3.find('\n', 0)
                            mV_string=out3[0:end_position1]
                        	
                            end_position2=out3.find('\n', end_position1+1)
                            uA_string=out3[end_position1+1:end_position2]
                            
                            end_position3=out3.find('\n', end_position2+1)
                            t_string=out3[end_position2+1:end_position3]
                            
                            end_position4=out3.find('\n', end_position3+1)
                            pot_string=out3[end_position3+1:end_position4]
                            
                    	    mV_start=mV_string.find(',',0)
                            uA_start=uA_string.find(',',0)
                            
                            mV_mag_temp=mV_string[mV_start+1:]
                            uA_mag_temp=uA_string[uA_start+1:]
                            
                            if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                                print "Had to wait extra time for the measurment to be returned again x3"
                                tn.close()
                                time.sleep(5)
                                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                                time.sleep(5)
                                tn.write("setbias 0 \n")
                                time.sleep(30)
                                out1 = tn.read_very_eager()
                                out2 = out1.replace('sis 0 ', '')
                                out3 = out2.replace(' = ', ',')
                                
                                end_position1=out3.find('\n', 0)
                                mV_string=out3[0:end_position1]
                        	   
                                end_position2=out3.find('\n', end_position1+1)
                                uA_string=out3[end_position1+1:end_position2]
                                
                                end_position3=out3.find('\n', end_position2+1)
                                t_string=out3[end_position2+1:end_position3]
                                
                                end_position4=out3.find('\n', end_position3+1)
                                pot_string=out3[end_position3+1:end_position4]
                            
                    	        mV_start=mV_string.find(',',0)
                                uA_start=uA_string.find(',',0)
                            
                                mV_mag_temp=mV_string[mV_start+1:]
                                uA_mag_temp=uA_string[uA_start+1:]
                                
                                if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                                    print "The script had to wait to long to read a value of mV and uA"
	                            print "Killing the script"
        	                    sys.exit()
                
                mV_mag[m]=float(mV_string[mV_start+1:])
                uA_mag[m]=float(uA_string[uA_start+1:])
            
            # End of NumOfMeasu loop
            f.write(str(UCA)+','+str(numpy.mean(mV_mag))+','+str(numpy.mean(uA_mag))+','+str(numpy.median(mV_mag))+','+str(numpy.median(uA_mag))+','+str(numpy.std(mV_mag))+','+str(numpy.std(uA_mag))+'\n')      
        # end of UCA sweep loop
        f.close()
        print "Calibration Sweep "+str(q+1)+" of "+str(sNum_feedoff+sNum_feedon)+ " is complete"
    # End of Feedback OFF SIS bias sweeping loop

    
    
    for q in range(sNum_feedon):
        ### Start feedback on cal   
        
        status = setfeedback(True) 
        savefile    = filedir + "LOcal_LO"+str(LO_val)+"_IF"+str(IF_band)+"_biaspot"+str(biaspot_feedon[q])+"_feedbackON"+"_notes"+filenotes+".csv"
        f = open(savefile, 'w')
        f.write('UCA, mV_mean, uA_mean, mV_median, uA_median, nV_stdev, uA_stdev \n')
        
        #set the pot position of the of the SIS bias
        tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
        tn.write("setbias 0 "+str(biaspot_feedoff[q]) + " \n")
        time.sleep(1)
        
        for n in range(sNum_UCA):
            UCA=UCAs[n]
            mV_mag  = numpy.zeros(NumOfMeasu)
            uA_mag = numpy.zeros(NumOfMeasu)
            
            # Set the UCA voltage for the LO
            status = LabJackU3_DAQ0(UCA)
            if not status:
                print "The program LabJackU3_DAQ0 returned status=False"
                print "filename="+savefile
                sys.exit()
            
            for m in range(NumOfMeasu):
                tn.write("setbias 0 \n")
                time.sleep(SleepPerMes)
                out1 = tn.read_very_eager()
                out2 = out1.replace('sis 0 ', '')
                out3 = out2.replace(' = ', ',')
                
                end_position1=out3.find('\n', 0)
                mV_string=out3[0:end_position1]
                
                end_position2=out3.find('\n', end_position1+1)
                uA_string=out3[end_position1+1:end_position2]
                
                end_position3=out3.find('\n', end_position2+1)
                t_string=out3[end_position2+1:end_position3]
                
                end_position4=out3.find('\n', end_position3+1)
                pot_string=out3[end_position3+1:end_position4]
                
                mV_start=mV_string.find(',',0)
                uA_start=uA_string.find(',',0)
                
                mV_mag_temp=mV_string[mV_start+1:]
                uA_mag_temp=uA_string[uA_start+1:]
                
                if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                    print "Had to wait extra time for the measurment to be returned"
                    tn.write("setbias 0 \n")
                    time.sleep(1)
                    out1 = tn.read_very_eager()
                    out2 = out1.replace('sis 0 ', '')
                    out3 = out2.replace(' = ', ',')
                    
                    end_position1=out3.find('\n', 0)
                    mV_string=out3[0:end_position1]
                    
                    end_position2=out3.find('\n', end_position1+1)
                    uA_string=out3[end_position1+1:end_position2]
                    
                    end_position3=out3.find('\n', end_position2+1)
                    t_string=out3[end_position2+1:end_position3]
                    
                    end_position4=out3.find('\n', end_position3+1)
                    pot_string=out3[end_position3+1:end_position4]
                    
                    mV_start=mV_string.find(',',0)
                    uA_start=uA_string.find(',',0)
                    
                    mV_mag_temp=mV_string[mV_start+1:]
                    uA_mag_temp=uA_string[uA_start+1:]
                    
                    if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                        print "Had to wait extra time for the measurment to be returned again"
                        tn.write("setbias 0 \n")
                        time.sleep(5)
                        out1 = tn.read_very_eager()
                        out2 = out1.replace('sis 0 ', '')
                        out3 = out2.replace(' = ', ',')
                        
                        end_position1=out3.find('\n', 0)
                        mV_string=out3[0:end_position1]
                        
                        end_position2=out3.find('\n', end_position1+1)
                        uA_string=out3[end_position1+1:end_position2]
                        
                        end_position3=out3.find('\n', end_position2+1)
                        t_string=out3[end_position2+1:end_position3]
                        
                        end_position4=out3.find('\n', end_position3+1)
                        pot_string=out3[end_position3+1:end_position4]
                        
                    	mV_start=mV_string.find(',',0)
                        uA_start=uA_string.find(',',0)
                        
                        mV_mag_temp=mV_string[mV_start+1:]
                        uA_mag_temp=uA_string[uA_start+1:]
                        
                        if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                            print "Had to wait extra time for the measurment to be returned again x2"
                            tn.close()
                            time.sleep(5)
                            tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                            time.sleep(5)
                            tn.write("setbias 0 \n")
                            time.sleep(15)
                            out1 = tn.read_very_eager()
                            out2 = out1.replace('sis 0 ', '')
                            out3 = out2.replace(' = ', ',')
                            
                            end_position1=out3.find('\n', 0)
                            mV_string=out3[0:end_position1]
                        	
                            end_position2=out3.find('\n', end_position1+1)
                            uA_string=out3[end_position1+1:end_position2]
                            
                            end_position3=out3.find('\n', end_position2+1)
                            t_string=out3[end_position2+1:end_position3]
                            
                            end_position4=out3.find('\n', end_position3+1)
                            pot_string=out3[end_position3+1:end_position4]
                            
                    	    mV_start=mV_string.find(',',0)
                            uA_start=uA_string.find(',',0)
                            
                            mV_mag_temp=mV_string[mV_start+1:]
                            uA_mag_temp=uA_string[uA_start+1:]
                            
                            if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                                print "Had to wait extra time for the measurment to be returned again x3"
                                tn.close()
                                time.sleep(5)
                                tn = telnetlib.Telnet('thzbias.sese.asu.edu', 9001)
                                time.sleep(5)
                                tn.write("setbias 0 \n")
                                time.sleep(30)
                                out1 = tn.read_very_eager()
                                out2 = out1.replace('sis 0 ', '')
                                out3 = out2.replace(' = ', ',')
                                
                                end_position1=out3.find('\n', 0)
                                mV_string=out3[0:end_position1]
                        	   
                                end_position2=out3.find('\n', end_position1+1)
                                uA_string=out3[end_position1+1:end_position2]
                                
                                end_position3=out3.find('\n', end_position2+1)
                                t_string=out3[end_position2+1:end_position3]
                                
                                end_position4=out3.find('\n', end_position3+1)
                                pot_string=out3[end_position3+1:end_position4]
                            
                    	        mV_start=mV_string.find(',',0)
                                uA_start=uA_string.find(',',0)
                            
                                mV_mag_temp=mV_string[mV_start+1:]
                                uA_mag_temp=uA_string[uA_start+1:]
                                
                                if (mV_mag_temp == '' or uA_mag_temp == '' or t_string == '' or pot_string == ''):
                                    print "The script had to wait to long to read a value of mV and uA"
	                            print "Killing the script"
        	                    sys.exit()
                
                mV_mag[m]=float(mV_string[mV_start+1:])
                uA_mag[m]=float(uA_string[uA_start+1:])     
            # End of NumOfMeasu loop
            f.write(str(UCA)+','+str(numpy.mean(mV_mag))+','+str(numpy.mean(uA_mag))+','+str(numpy.median(mV_mag))+','+str(numpy.median(uA_mag))+','+str(numpy.std(mV_mag))+','+str(numpy.std(uA_mag))+'\n')   
        # end of UCA sweep loop
        f.close()
        print "Calibration Sweep "+str(q+1+sNum_feedoff)+" of "+str(sNum_feedoff+sNum_feedon)+ " is complete"
    # End of Feedback ON SIS bias sweeping loop
    zeropots()
    return