def Yfac_plotter(dir,wide_lineW, narrow_lineW, mV_Yfactor, start_Yrange, end_Yrange, max_Yfactor, mV_max_Yfactor, mV_min_Yfactor, min_Yfactor, mean_Yfactor, Ynums, LO_val, IFband_val, magpot_val, UCA_val, wide_missing, narrow_missing, do_yfactor, do_regrid, mono_switcher, save_plots, wide_off_uA, wide_hot_uA, wide_cold_uA, narrow_off_uA, narrow_hot_uA, narrow_cold_uA, wide_off_tp, wide_hot_tp, wide_cold_tp, narrow_off_tp, narrow_hot_tp, narrow_cold_tp,Yfactor,wide_off_mV,wide_hot_mV,wide_cold_mV,narrow_off_mV,narrow_hot_mV,narrow_cold_mV):
    # import time
    import matplotlib as plt
    from pylab import *
    
    pubplot = True
    verbose = False
    status = False
    plt.clf()
    if ((not wide_missing) and (not narrow_missing) and (do_yfactor)and (do_regrid) and (mono_switcher)):
        yaxis_top=max(max(wide_off_uA),max(wide_hot_uA),max(wide_cold_uA),max(narrow_off_uA),max(narrow_hot_uA),max(narrow_cold_uA),max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp),max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp),max(Yfactor))
        yaxis_bot=min(min(wide_off_uA),min(wide_hot_uA),min(wide_cold_uA),min(narrow_off_uA),min(narrow_hot_uA),min(narrow_cold_uA),min(wide_off_tp),min(wide_hot_tp),min(wide_cold_tp),min(narrow_off_tp),min(narrow_hot_tp),min(narrow_cold_tp),min(Yfactor))
        
        xaxis_max=max(max(wide_off_mV),max(wide_hot_mV),max(wide_cold_mV),max(narrow_off_mV),max(narrow_hot_mV),max(narrow_cold_mV))
        xaxis_min=min(min(wide_off_mV),min(wide_hot_mV),min(wide_cold_mV),min(narrow_off_mV),min(narrow_hot_mV),min(narrow_cold_mV))
        xaxis_size=xaxis_max-xaxis_min
       
        tp_scale=yaxis_top/max(max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp),max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))
        
        yaxis_size=yaxis_top-yaxis_bot
        yaxis_max=yaxis_top + 0.2*yaxis_size
        yaxis_min=yaxis_bot - 0.1*yaxis_size
        Ymax = max(Yfactor)
        Y_scale=(yaxis_top +0.1*yaxis_size)/Ymax
        
    elif ((not wide_missing) and (not narrow_missing)):
        yaxis_top=max(max(wide_off_uA),max(wide_hot_uA),max(wide_cold_uA),max(narrow_off_uA),max(narrow_hot_uA),max(narrow_cold_uA),max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp),max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))
        yaxis_bot=min(min(wide_off_uA),min(wide_hot_uA),min(wide_cold_uA),min(narrow_off_uA),min(narrow_hot_uA),min(narrow_cold_uA),min(wide_off_tp),min(wide_hot_tp),min(wide_cold_tp),min(narrow_off_tp),min(narrow_hot_tp),min(narrow_cold_tp))
        xaxis_max=max(max(wide_off_mV),max(wide_hot_mV),max(wide_cold_mV),max(narrow_off_mV),max(narrow_hot_mV),max(narrow_cold_mV))
        xaxis_min=min(min(wide_off_mV),min(wide_hot_mV),min(wide_cold_mV),min(narrow_off_mV),min(narrow_hot_mV),min(narrow_cold_mV))
        xaxis_size=xaxis_max-xaxis_min
       
        tp_scale=yaxis_top/max(max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp),max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))
        
        yaxis_size=yaxis_top-yaxis_bot
        yaxis_max=yaxis_top + 0.2*yaxis_size
        yaxis_min=yaxis_bot - 0.1*yaxis_size
        
    elif (not wide_missing and (do_yfactor)):
        yaxis_top=max(max(wide_off_uA),max(wide_hot_uA),max(wide_cold_uA),max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp))
        yaxis_bot=min(min(wide_off_uA),min(wide_hot_uA),min(wide_cold_uA),min(wide_off_tp),min(wide_hot_tp),min(wide_cold_tp))
        xaxis_max=max(max(wide_off_mV),max(wide_hot_mV),max(wide_cold_mV))
        xaxis_min=min(min(wide_off_mV),min(wide_hot_mV),min(wide_cold_mV))
        xaxis_size=xaxis_max-xaxis_min
       
        tp_scale=yaxis_top/max(max(wide_off_tp),max(wide_hot_tp),max(wide_cold_tp))
        
        yaxis_size=yaxis_top-yaxis_bot
        yaxis_max=yaxis_top + 0.2*yaxis_size
        yaxis_min=yaxis_bot - 0.1*yaxis_size
        Y_scale=(yaxis_top +0.1*yaxis_size)/max(Yfactor)
        
    elif (not narrow_missing and do_yfactor):
        yaxis_top=max(max(narrow_off_uA),max(narrow_hot_uA),max(narrow_cold_uA),max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))
        yaxis_bot=min(min(narrow_off_uA),min(narrow_hot_uA),min(narrow_cold_uA),min(narrow_off_tp),min(narrow_hot_tp),min(narrow_cold_tp))
        xaxis_max=max(max(narrow_off_mV),max(narrow_hot_mV),max(narrow_cold_mV))
        xaxis_min=min(min(narrow_off_mV),min(narrow_hot_mV),min(narrow_cold_mV))
        xaxis_size=xaxis_max-xaxis_min
       
        tp_scale=yaxis_top/max(max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))
        
        yaxis_size=yaxis_top-yaxis_bot
        yaxis_max=yaxis_top + 0.2*yaxis_size
        yaxis_min=yaxis_bot - 0.1*yaxis_size
        Ymax=max(Yfactor)
        Y_scale=(yaxis_top +0.1*yaxis_size)/Ymax

    if pubplot:
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        
        lns1 = ax1.plot(wide_hot_mV, wide_hot_uA         , linewidth=narrow_lineW, color = 'red'   , label='IV Sweep')
        ax1.set_xlabel('Voltage (mV)')
        ax1.set_ylabel('Current (uA)', color='red')
        for tl in ax1.get_yticklabels():
            tl.set_color('red')
            
        ax2 = ax1.twinx()
        lns2 = ax2.plot(mV_Yfactor, Yfactor*((yaxis_top +0.1*yaxis_size)/2), linewidth=narrow_lineW, color = 'green', label='Y factor')
        ax2.set_ylabel('Y factor', color='green')
        
        labels = [item.get_text() for item in ax2.get_xticklabels()]
        #print labels
        labels[1] = '0.0'
        labels[2] = '0.5'
        labels[3] = '1.0'
        labels[4] = '1.5'
        labels[len(labels)-2] = '2.0'
        ax2.set_yticklabels(labels)
        for tl in ax2.get_yticklabels():
            tl.set_color('green')
            
        tp_scale=max(wide_hot_uA)/max(max(narrow_off_tp),max(narrow_hot_tp),max(narrow_cold_tp))     
        
        lns3 = plt.plot(narrow_hot_mV, narrow_hot_tp*tp_scale,   linewidth=narrow_lineW, color = 'purple', label='300K Total Power')
        lns4 = plt.plot(narrow_cold_mV, narrow_cold_tp*tp_scale, linewidth=narrow_lineW, color = 'blue'  , label='77K Total Power')
        lns5 = plt.plot(narrow_off_mV, narrow_off_tp*tp_scale,   linewidth=narrow_lineW, color = 'orange', label='Total Power Offset')
        
        plt.plot(wide_off_mV, wide_off_tp*tp_scale, linewidth=wide_lineW, color = 'orange', linestyle = ':')
        
        plt.plot(wide_hot_mV, wide_hot_tp*tp_scale, linewidth=wide_lineW, color = 'purple', linestyle = ':')
        plt.plot(wide_cold_mV, wide_cold_tp*tp_scale, linewidth=wide_lineW, color = 'blue'      , linestyle = ':')
        
        lns = lns1+lns2+lns3+lns4+lns5
        labs = [l.get_label() for l in lns]
        #ax.legend(lns, labs, loc=0)
                    
        rcParams['legend.fontsize'] = 10
        plt.legend(lns, labs, loc=4)
        
       


    if (not narrow_missing):
        
        if not pubplot:
            plt.plot(narrow_off_mV, narrow_off_uA         , linewidth=narrow_lineW, color = 'yellow', label='narrow off IV')
            plt.plot(narrow_off_mV, narrow_off_tp*tp_scale, linewidth=narrow_lineW, color = 'orange', label='narrow off TP')
            plt.plot(narrow_hot_mV, narrow_hot_uA         , linewidth=narrow_lineW, color = 'red'   , label='narrow hot IV ')
            plt.plot(narrow_hot_mV, narrow_hot_tp*tp_scale, linewidth=narrow_lineW, color = 'purple', label='narrow hot TP ')
            plt.plot(narrow_cold_mV, narrow_cold_uA        , linewidth=narrow_lineW, color = 'dodgerblue', label='narrow cold IV ')
            plt.plot(narrow_cold_mV, narrow_cold_tp*tp_scale, linewidth=narrow_lineW, color = 'blue'      , label='narrow cold TP ')

    if (not wide_missing):
        if not pubplot:
            plt.plot(wide_off_mV, wide_off_uA         , linewidth=wide_lineW, color = 'yellow', linestyle = ':', label='wide off IV')
            plt.plot(wide_off_mV, wide_off_tp*tp_scale, linewidth=wide_lineW, color = 'orange', linestyle = ':', label='wide off TP')
    
            plt.plot(wide_hot_mV, wide_hot_uA         , linewidth=wide_lineW, color = 'red'   , linestyle = ':', label='wide hot IV ')
            plt.plot(wide_hot_mV, wide_hot_tp*tp_scale, linewidth=wide_lineW, color = 'purple', linestyle = ':', label='wide hot TP ')
            plt.plot(wide_cold_mV, wide_cold_uA        , linewidth=wide_lineW, color = 'dodgerblue', linestyle = ':', label='wide cold IV ')
            plt.plot(wide_cold_mV, wide_cold_tp*tp_scale, linewidth=wide_lineW, color = 'blue'      , linestyle = ':', label='wide cold TP ')
    if ((do_yfactor==True) and (do_regrid == True) and (mono_switcher==True)):
        if not pubplot:
        
            plt.plot([start_Yrange,start_Yrange], [yaxis_min,yaxis_max], linewidth=1, color = 'black', label='Y range:(%03.2f,%03.2f)mV' % (start_Yrange, end_Yrange))
            plt.plot([end_Yrange,end_Yrange],     [yaxis_min,yaxis_max], linewidth=1, color = 'black') 
       
            plt.text(xaxis_min+xaxis_size*0.35,yaxis_bot-yaxis_size*0.09, "Max  Y factor: "+str('%2.3f' % max_Yfactor)+" at "+str('%2.3f' % mV_max_Yfactor)+" mV", fontsize=10)
            plt.text(xaxis_min+xaxis_size*0.35,yaxis_bot-yaxis_size*0.05, "Mean Y factor: "+str('%2.3f' % mean_Yfactor), fontsize=10)
            plt.text(xaxis_min+xaxis_size*0.35,yaxis_bot-yaxis_size*0.01, "Min  Y factor: "+str('%2.3f' % min_Yfactor)+" at "+str('%2.3f' % mV_min_Yfactor)+" mV", fontsize=10)
        
        
            plt.plot([mV_max_Yfactor,mV_max_Yfactor], [yaxis_min,yaxis_max], linewidth=1, color = 'red', label='max Y factor')
            plt.plot([xaxis_min,xaxis_max], [max_Yfactor*Y_scale,max_Yfactor*Y_scale], linewidth=1, color = 'red')
        
       
            
            plt.plot([start_Yrange,end_Yrange],[mean_Yfactor*Y_scale, mean_Yfactor*Y_scale], linewidth=1, color = 'purple', label='mean Y factor')
            
            plt.plot([mV_min_Yfactor,mV_min_Yfactor], [yaxis_min,yaxis_max], linewidth=1, color = 'blue', label='min Y factor')
            plt.plot([xaxis_min,xaxis_max], [min_Yfactor*Y_scale,min_Yfactor*Y_scale], linewidth=1, color = 'blue')
            plt.plot(mV_Yfactor, Yfactor*Y_scale, linewidth=1, color = 'green', label='Y factor')
    
    plt.xlim(xaxis_min,xaxis_max)
    plt.ylim(yaxis_min,yaxis_max)
    if not pubplot:
        rcParams['legend.fontsize'] = 8
        plt.legend(loc=4)
        plt.xlabel('Voltage (mV)')
        plt.ylabel('Current (uA)')
    if pubplot:
        plt.title("Y Factor from Total Power")
    else:
        if ((do_yfactor==True) and (do_regrid == True) and (mono_switcher==True)):
            plt.title("Y-Factor:"+str('%2.3f' % max_Yfactor)+" LO"+str(LO_val)+" IFband"+str(IFband_val)+" magpot"+str(magpot_val)+" UCA:"+str(UCA_val))
            #plt.title("Y-Factor:"+str('%2.3f' % max_Yfactor)+" LO"+LO_val+" IFband"+str('%1.3f' % IFband_val)+" magpot"+str('%06.f' % magpot_str)+" UCA:"+str('%1.3f' % UCA_val))
        else:
            plt.title(" LO"+str(LO_val)+" IFband"+str(IFband_val)+" magpot"+str(magpot_val)+" UCA:"+str(UCA_val))
    #plt.show()
    #time.sleep(1)
    if save_plots:
        if pubplot:
            saveplotdir  = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/pubplots/'
            saveplotname = saveplotdir + 'plot.png'
            savefig(saveplotname)
        else:
            savefig(dir+'plots/'+Ynums+".png")
        if verbose:
            print "plot saved to: "+dir+'plots/'+Ynums+".png"
        
    status = True
    return status