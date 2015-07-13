import matplotlib
from matplotlib import pyplot as plt
from datapro import local_copy, windir
from profunc import makeORclear_plotdir


###########################################
###### Intersecting lines Parameters ######
###########################################
do_intersecting_lines    = False
int_lines_plotdir        = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/intersecting_lines/'))

intersecting_lines_behavior = 'Y_max' #'Y_max','Y_mV_band_ave'
int_lines_mV_centers     = [0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8]#list(numpy.arange(0.5,2.0,0.1))
int_lines_mV_plus_minus  = 0.05

# include_spec_data        = True
# IFband_vector            = [1,2,3,4,5]

show_popular_LOfreqs     = False
popular_LOfreqs_min_occurrences = 3 # integer or None for any
popular_LOfreqs_max_occurrences = None # integer or None for any

show_popular_meanmag_mA     = False
popular_meanmag_mA_min_occurrences = 5 # integer or None for any
popular_meanmag_mA_max_occurrences = None # integer or None for any

int_lines_sort_LOuA = True # True or False, sort by LO pump power (LOuA) just before making the plot


inter_lines_leg_on       = True
int_line_alpha = 1.0
int_line_linw  = 1
int_line_ls    = '-'


###################################
###### Shot Noise Parameters ######
###################################
do_shot_noise = False
shot_noise_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/shot_noise/'))






















################################
###### Intersecting Lines ######
################################
if do_intersecting_lines:
    great_data_list = []

    great_plot_list = []
    great_leglines  = []
    great_leglabels = []
    makeORclear_plotdir(int_lines_plotdir)
    fig, ax1 = plt.subplots()

    if intersecting_lines_behavior == 'Y_max':
        color_count = 0
        plot_title = 'Ymax'

        local_plot_list = []
        local_leglines  = []
        local_leglabels = []
        local_Ysweeps   = []
        for Ysweep in Ysweeps:
            color = colors[color_count % color_len]
            color_count+=1
            Ysweep.intersecting_line_Ymax(mV_plus_minus=int_lines_mV_plus_minus)

            m = Ysweep.intersectingL_m
            b = Ysweep.intersectingL_b
            temps=[-300,400]
            powers=[]
            for temp in temps:
                powers.append((temp*m)+b)
            local_plot_list, local_leglines, local_leglabels \
                = xyplotgen2(temps, powers, label=''+str('%2.2f' % numpy.mean(Ysweep.meanSIS_uA))+' uA',
                             plot_list=local_plot_list, leglines=local_leglines, leglabels=local_leglabels,
                             color=color, linw=int_line_linw,
                             ls= int_line_ls, alpha= int_line_alpha,
                             scale_str='', leg_on=True )
            local_Ysweeps.append(Ysweep)

        great_data_list.append((plot_title, local_Ysweeps, local_plot_list, local_leglines, local_leglabels))

    elif intersecting_lines_behavior == 'Y_mV_band_ave':
        for mV_center in int_lines_mV_centers:
            color_count = 0
            plot_title = str('%2.2f' % mV_center )+'mV'

            local_plot_list = []
            local_leglines  = []
            local_leglabels = []
            local_Ysweeps   = []


            for Ysweep in Ysweeps:
                color = colors[color_count % color_len]
                color_count+=1
                Ysweep.intersecting_line_mV(mV_center=mV_center,mV_plus_minus=int_lines_mV_plus_minus)

                m = Ysweep.intersectingL_m
                b = Ysweep.intersectingL_b
                temps=[-400,400]
                powers=[]
                for temp in temps:
                    powers.append((temp*m)+b)
                local_plot_list, local_leglines, local_leglabels \
                    = xyplotgen2(temps, powers, label=''+str(Ysweep.mV_Yfactor)+' mV',
                                 plot_list=local_plot_list, leglines=local_leglines, leglabels=local_leglabels,
                                 color=color, linw=int_line_linw,
                                 ls= int_line_ls, alpha= int_line_alpha,
                                 scale_str='', leg_on=True )
                local_Ysweeps.append(Ysweep)
            great_data_list.append((plot_title,local_Ysweeps, local_plot_list, local_leglines, local_leglabels))


    ### Now I take the data and subdivide it based on things like LO frequency or whatever I want to look at
    # LO freq
    if show_popular_LOfreqs:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            LOfreq_list = []
            for Ysweep in Ysweeps:
                LOfreq_list.append(Ysweep.LOfreq)

            unique_LOfreq_list \
                = filter_on_occurrences(LOfreq_list,min_occurrences=popular_LOfreqs_min_occurrences,
                                        max_occurrences=popular_LOfreqs_max_occurrences)

            for unique_LOfreq in unique_LOfreq_list:
                local_plot_list = []
                local_leglines  = []
                local_leglabels = []
                local_Ysweeps   = []
                new_plot_title=plot_title+' '+str(unique_LOfreq)+'GHz'
                for (sweep_index,Ysweep) in list(enumerate(Ysweeps)):

                    if unique_LOfreq == Ysweep.LOfreq:
                        local_plot_list.append(plot_list[sweep_index])
                        local_leglines.append(leglines[sweep_index])
                        local_leglabels.append(leglabels[sweep_index])
                        local_Ysweeps.append(Ysweep)

                new_great_data_list.append((new_plot_title, local_Ysweeps,
                                            local_plot_list, local_leglines, local_leglabels))
        great_data_list = new_great_data_list

    # meanmag_mA
    if show_popular_meanmag_mA:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            meanmag_mA_list = []
            for Ysweep in Ysweeps:
                ave_meanmag_mA = numpy.mean(Ysweep.meanmag_mA)
                meanmag_mA_list.append(numpy.round(ave_meanmag_mA))

            unique_meanmag_mA_list \
                = filter_on_occurrences(meanmag_mA_list,min_occurrences=popular_meanmag_mA_min_occurrences,
                                        max_occurrences=popular_meanmag_mA_max_occurrences)

            for unique_meanmag_mA in unique_meanmag_mA_list:
                local_plot_list = []
                local_leglines  = []
                local_leglabels = []
                local_Ysweeps   = []
                new_plot_title=plot_title+' '+str(unique_meanmag_mA)+'mA'
                for (sweep_index,Ysweep) in list(enumerate(Ysweeps)):

                    if unique_meanmag_mA == (numpy.round(numpy.mean(Ysweep.meanmag_mA))):
                        local_plot_list.append(plot_list[sweep_index])
                        local_leglines.append(leglines[sweep_index])
                        local_leglabels.append(leglabels[sweep_index])
                        local_Ysweeps.append(Ysweep)

                new_great_data_list.append((new_plot_title,local_Ysweeps,
                                            local_plot_list, local_leglines, local_leglabels))
        great_data_list = new_great_data_list







    if int_lines_sort_LOuA:
        new_great_data_list = []
        for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
            LOuA_Ysweep_sort_list = []
            for Ysweep in Ysweeps:
                 LOuA_Ysweep_sort_list.append(numpy.mean(Ysweep.meanSIS_uA))
            [new_LOuA_order,Ysweeps,plot_list, leglines, leglabels] \
                = make_monotonic([LOuA_Ysweep_sort_list,Ysweeps,plot_list, leglines, leglabels])
            new_great_data_list.append((plot_title, Ysweeps, plot_list, leglines, leglabels))
        great_data_list = new_great_data_list

    for (plot_title, Ysweeps, plot_list, leglines, leglabels) in great_data_list:
        ##############
        ### AXIS 1 ###
        ##############
        if (plot_list != []):
            fig, ax1 = plt.subplots()
            for plot_obj in plot_list:
                (x_vector, y_vector, color, linw, ls, alpha, scale_str) = plot_obj
                ax1.plot(x_vector, y_vector, color=color, linewidth=linw, ls=ls, alpha=alpha)

        plt.title(plot_title)
        plt.xlabel('temperature (K)')
        plt.ylabel('power recorder output (V)')

        leglines_plot_line = []
        for indexer in range(len(leglines)):
            (color,ls,linw,alpha) = leglines[indexer]
            leglines_plot_line.append(plt.Line2D(range(10), range(10), color=color,
                            ls=ls, linewidth=linw, alpha=alpha))
        if inter_lines_leg_on:
            matplotlib.rcParams['legend.fontsize'] = 12
            plt.legend(tuple(leglines_plot_line),tuple(leglabels), numpoints=1, loc=0)

        if show_plots:
            plt.show()
            plt.draw()

        if save_plots:
            plotfilename = int_lines_plotdir+'intersecting_lines_'+plot_title.replace(' ','_')
            if ((do_eps) and (not platform == 'win32')):
                if verbose:
                    print 'saving EPS file'
                plt.savefig(plotfilename+'.eps')
            else:
                if verbose:
                    print 'saving PNG file'
                plt.savefig(plotfilename+'.png')
            plt.close("all")








########################
###### Shot Noise ######
########################
if do_shot_noise:
    for Ysweep in Ysweeps:
        Ysweep.shotnoise_test(verbose=True)
        fig, ax1 = plt.subplots()

        if Ysweep.hot_shotnoise_test:
            gain = Ysweep.hot_shotnoise_gain
            input_noise = Ysweep.hot_shotnoise_input_noise
            unpumped_uA = Ysweep.hot_raw_unpumped_uA
            unpumped_tp = Ysweep.hot_raw_unpumped_tp
            raw_uA = Ysweep.hot_raw_uA_mean
            raw_tp = Ysweep.hot_raw_TP_mean
            uA = Ysweep.hot_uA_mean
            tp = Ysweep.hot_tp_mean
            shot_uA = Ysweep.hot_shotnoise_shot_uA
            shot_tp = Ysweep.hot_shotnoise_shot_tp
            ax1.plot(uA, tp)
            ax1.plot(unpumped_uA,unpumped_tp)
            ax1.plot(raw_uA,raw_tp)
            ax1.plot(shot_uA,shot_tp)
            ax1.plot(shot_uA,(shot_uA+input_noise)*gain)

        if show_plots:
            plt.show()
            plt.draw()

        if save_plots:
            plotfilename = shot_noise_plotdir+'shotnoise_'+Ysweep.Ynum
            if ((do_eps) and (not platform == 'win32')):
                if verbose:
                    print 'saving EPS file'
                plt.savefig(plotfilename+'.eps')
            else:
                if verbose:
                    print 'saving PNG file'
                plt.savefig(plotfilename+'.png')
            plt.close("all")


            # # do derivatives to find linear regions
            # shot_matrix = numpy.zeros((len(uA_unpumpedhot),3))
            # shot_matrix[:,0] = uA_unpumpedhot
            # shot_matrix[:,1] = mV_unpumpedhot
            # shot_matrix[:,2] = tp_unpumpedhot
            # der1, der2 = do_derivative(shot_matrix, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int, do_der2_conv, der2_min_cdf, der2_sigma, regrid_mesh, verbose)
            # #status, lin_start_uAmV, lin_end_uAmV = findlinear(der2[:,0], der2[:,1], linif, verbose)
            # #slopes, intercepts, bestfits_uA, bestfits_mV = resfitter(uA_unpumpedhot, mV_unpumpedhot, lin_start_uAmV, lin_end_uAmV)
            #
            # status, lin_start_uAtp, lin_end_uAtp = findlinear(der2[:,0], der2[:,2], linif, verbose)
            # slopes, intercepts, bestfits_uA, bestfits_tp = resfitter(uA_unpumpedhot, tp_unpumpedhot, lin_start_uAtp, lin_end_uAtp)
            #
            # import matplotlib
            # from matplotlib import pyplot as plt
            # matplotlib.rc('text', usetex=True)
            #
            # plt.clf()
            # matplotlib.rcParams['legend.fontsize'] = 10.0
            # IV_color = 'blue'
            # TP_color = 'red'
            # shot_color = 'green'
            # fig, ax1 = plt.subplots()
            # ax1.plot(uA_unpumpedhot, tp_unpumpedhot, color=TP_color, linewidth=5)
            # ax1.set_xlabel("current ($\mu$$A$)")
            # ax1.set_ylabel('Receiver Power', color=TP_color)
            # for tl in ax1.get_yticklabels():
            #     tl.set_color(TP_color)
            # for n in range(len(bestfits_tp[0,:])):
            #     ax1.plot(bestfits_uA[:,n], bestfits_tp[:, n], color="black", linewidth=2)
            # n = len(bestfits_tp[0,:])-1
            # shot_line_uA = []
            # shot_line_tp = []
            #
            # print
            # dark_current = intercepts[n]/slopes[n]
            # #shot_line_uA.append(-1*dark_current)
            # shot_line_uA.append(bestfits_uA[0,n])
            # shot_line_uA.append(bestfits_uA[1,n])
            #
            # #shot_line_tp.append(0)
            # shot_line_tp.append(bestfits_tp[0,n])
            # shot_line_tp.append(bestfits_tp[1,n])
            #
            # ax1.plot(shot_line_uA,shot_line_tp, color=shot_color, linewidth=3)
            # #ax1.plot([-1*dark_current, -1*dark_current],[0,max(tp_unpumpedhot)], color='firebrick', linewidth = 3)
            # plt.text(30, 0.068, "L$\cdot$$T_{IF} = 51$K", fontsize=16, color=shot_color)
            # plt.text(30, 0.06, "with $T_{IF}$ $=$ $10$K, L$ = 7$dB", fontsize=16, color=shot_color)
            #
            # B = 60.0e6 # MHz
            # e = 1.60217657e-19 # Columbs (electron charge)
            # I = dark_current*1.0e-6
            # P = 2.0*e*I*B
            # fP = P*1.0e15
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.7, str('%2.2f' % fP) + " $fW = 2eI_0$$B = P_0$", fontsize=16, color="firebrick")
            #
            # kb = 1.3806488e-23
            # T = (2.0*e*I)/(kb)
            # mT = T*1.0e3
            # #print T
            #
            #
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.6, str('%2.2f' % T) + " $K = T_0$", fontsize=16, color="firebrick")
            #
            # #plt.text(-1*dark_current*0.9, max(tp_unpumpedhot)*0.5, str(slopes[n]) + " = slope, " + str(intercepts[n]) +" = Y(0)", fontsize=16, color="firebrick")
            # ax2 = ax1.twinx()
            # ax2.plot(uA_unpumpedhot, mV_unpumpedhot, color=IV_color, linewidth=5)
            # ax2.set_ylabel('Voltage ($mV$)', color=IV_color)
            # for tl in ax2.get_yticklabels():
            #     tl.set_color(IV_color)
            #
            # plt.savefig("/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/shotplots/" + Ynum + ".eps")
            # plt.close('all')