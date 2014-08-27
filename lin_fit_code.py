def linfit(X, Y, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, verbose):
    import numpy
    matrix = numpy.zeros((len(X),2))
    matrix[:,0] = X
    matrix[:,1] = Y                
                        
    from profunc import do_derivative                     
    from domath import findlinear, resfitter                          
    der1, der2 = do_derivative(matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose)
    #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
    #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
    
    status, lin_start, lin_end = findlinear(der2[:,0], der2[:,1], linif, verbose)
    slopes, intercepts, bestfits_X, bestfits_Y = resfitter(X, Y, lin_start, lin_end)
    
return
    
    import matplotlib        
    from matplotlib import pyplot as plt
    matplotlib.rc('text', usetex=True)
            
    plt.clf()
    matplotlib.rcParams['legend.fontsize'] = 10.0
    IV_color = 'blue'
    TP_color = 'red'
    shot_color = 'green'
    fig, ax1 = plt.subplots()
    ax1.plot(uA_unpumpedhot, tp_unpumpedhot, color=TP_color, linewidth=5)
    ax1.set_xlabel("current ($\mu$$A$)")
    ax1.set_ylabel('Receiver Power', color=TP_color)
    for tl in ax1.get_yticklabels():
        tl.set_color(TP_color)
    for n in range(len(bestfits_tp[0,:])):
        ax1.plot(bestfits_uA[:,n], bestfits_tp[:, n], color="black", linewidth=2)
    n = len(bestfits_tp[0,:])-1
    shot_line_uA = []
    shot_line_tp = []
    
    print 
    dark_current = intercepts[n]/slopes[n]
    #shot_line_uA.append(-1*dark_current)
    shot_line_uA.append(bestfits_uA[0,n])
    shot_line_uA.append(bestfits_uA[1,n])
    
    #shot_line_tp.append(0)
    shot_line_tp.append(bestfits_tp[0,n])
    shot_line_tp.append(bestfits_tp[1,n])
    
    ax1.plot(shot_line_uA,shot_line_tp, color=shot_color, linewidth=3)
    #ax1.plot([-1*dark_current, -1*dark_current],[0,max(tp_unpumpedhot)], color='firebrick', linewidth = 3)
    plt.text(30, 0.068, "L$\cdot$$T_{IF} = 51$K", fontsize=16, color=shot_color)
    plt.text(30, 0.06, "with $T_{IF}$ $=$ $10$K, L$ = 7$dB", fontsize=16, color=shot_color)
    
    B = 60.0e6 # MHz
    e = 1.60217657e-19 # Columbs (electron charge)
    I = dark_current*1.0e-6
    P = 2.0*e*I*B
    fP = P*1.0e15
    #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.7, str('%2.2f' % fP) + " $fW = 2eI_0$$B = P_0$", fontsize=16, color="firebrick")
    
    kb = 1.3806488e-23
    T = (2.0*e*I)/(kb)
    mT = T*1.0e3
    #print T
    
    
    #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.6, str('%2.2f' % T) + " $K = T_0$", fontsize=16, color="firebrick")
    
    #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.5, str(slopes[n]) + " = slope, " + str(intercepts[n]) +" = Y(0)", fontsize=16, color="firebrick")
    ax2 = ax1.twinx()
    ax2.plot(uA_unpumpedhot, mV_unpumpedhot, color=IV_color, linewidth=5)   
    ax2.set_ylabel('Voltage ($mV$)', color=IV_color)
    for tl in ax2.get_yticklabels():
        tl.set_color(IV_color)
    
    plt.savefig("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/shotplots/" + Ynum + ".eps")
    plt.close('all')