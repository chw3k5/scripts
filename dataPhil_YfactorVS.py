import sys
from datapro import local_copy, windir


#######################################
###### Yfactor versus everything ######
#######################################
do_Yfactor_versus_LO_freq = True
do_Yfactor_versus_magpot  = True
do_Yfactor_versus_UCA    = True
do_Yfactor_versus_SISpot = True
do_Yfactor_versus_IFband = True

### Y factor related options
# analysis options
do_max_Yfactor = True # False uses the average value for a bandwidth (spectral data), True uses the maximum
min_Y_factor = 0.3
spec_bands = [0,1,2,3,4,5]#[1.39,1.45]#1.39,1.45]#,4,5]

# plot options
plot_ylim_list_Yfactor_vs = [0.5, 2.5] # None or list of two [1.0, 3.0]
ylabel_str_Yfactor_vs     = "Y Factor"

Y_pm_color    = 'DarkOrchid'
Y_spec_colors = ['Crimson','Olive','GoldenRod','RoyalBlue','SaddleBrown','Red','Salmon','SandyBrown','Sienna',
                 'SkyBlue','SlateBlue','SlateGrey','BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate',
                 'Coral','CornflowerBlue','Crimson','Cyan']


### dependent variable options
# LOfreq
Y_LOfreq_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_LOfreq/'))
Y_LOfreq_xlim_list_Yfactor_versus = [645, 695] # None or list of two [645, 695]
Y_LOfreq_xlabel_str_Yfactor_versus="LO frequency (GHz)"

Y_LOfreq_ls = ""
Y_LOfreq_linw = 3
Y_LOfreq_fmt = 'o'
Y_LOfreq_markersize = 5
Y_LOfreq_alpha = 0.3

Y_LOfreq_legend_size = 10
Y_LOfreq_legend_num_of_points = 3
Y_LOfreq_legend_loc = 3

# magpot
Y_magpot_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_magpot/'))
Y_magpot_xlim_list_Yfactor_versus = None# [65100, 90000] # None or list of two [645, 695]
Y_magpot_xlabel_str_Yfactor_versus="electromagnet potentiometer"

Y_magpot_ls = ""
Y_magpot_linw = 3
Y_magpot_fmt = 'o'
Y_magpot_markersize = 5
Y_magpot_alpha = 0.3

Y_magpot_legend_size = 10
Y_magpot_legend_num_of_points = 3
Y_magpot_legend_loc = 3

# UCA_volt
Y_UCA_volt_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_UCA_volt/'))
Y_UCA_volt_xlim_list_Yfactor_versus = None# [65100, 90000] # None or list of two [645, 695]
Y_UCA_volt_xlabel_str_Yfactor_versus="LO User Controlled Attenuation (volts)"

Y_UCA_volt_ls = ""
Y_UCA_volt_linw = 3
Y_UCA_volt_fmt = 'o'
Y_UCA_volt_markersize = 5
Y_UCA_volt_alpha = 0.3

Y_UCA_volt_legend_size = 10
Y_UCA_volt_legend_num_of_points = 3
Y_UCA_volt_legend_loc = 3

# SISpot
Y_SISpot_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_SISpot/'))
Y_SISpot_xlim_list_Yfactor_versus = None# [65100, 90000] # None or list of two [645, 695]
Y_SISpot_xlabel_str_Yfactor_versus="SIS potentiometer position"

Y_SISpot_ls = ""
Y_SISpot_linw = 3
Y_SISpot_fmt = 'o'
Y_SISpot_markersize = 5
Y_SISpot_alpha = 0.3

Y_SISpot_legend_size = 10
Y_SISpot_legend_num_of_points = 3
Y_SISpot_legend_loc = 3

# SISpot
Y_IFband_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/Y_IFband/'))
Y_IFband_xlim_list_Yfactor_versus = None# [65100, 90000] # None or list of two [645, 695]
Y_IFband_xlabel_str_Yfactor_versus="IF band - voltage on YIG"

Y_IFband_ls = ""
Y_IFband_linw = 3
Y_IFband_fmt = 'o'
Y_IFband_markersize = 5
Y_IFband_alpha = 0.3

Y_IFband_legend_size = 10
Y_IFband_legend_num_of_points = 3
Y_IFband_legend_loc = 3


########################################
###### Anything verses Everything ######
########################################
do_LOuA_LOmV_AvsE= True
do_LOmV_LOfreq_AvsE = True
do_LOuA_LOfreq_AvsE = True
do_UCA_LOfreq_AvsE = True
do_IFband_LOfreq_AvsE = True

neutral_color_AvsE='Green'
hot_color_AvsE='firebrick'
cold_color_AvsE='blue'

show_pairs_AvsE = True
pair_color_AvsE = 'black'
pair_AvsE_ls = '-'
pair_AvsE_linw = 1
pair_AvsE_alpha = 0.5

show_error_AvsE = True
error_marker_AvsE = '|'
error_capsize_AvsE = 1
error_ls_AvsE = 'None'
error_linw_AvsE = 1

### dependent variable options
# LOuA_LOmV
LOuA_LOmV_AvsE_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/LOuA_LOmV/'))

LOuA_LOmV_AvsE_xlim_list = None#[1.2, 1.4] # None or list of two [645, 695]
LOuA_LOmV_AvsE_xlabel_str="Voltage (mV)"

LOuA_LOmV_AvsE_ylim_list = None#[0, 25] # None or list of two [645, 695]
LOuA_LOmV_AvsE_ylabel_str="Current (uA)"

LOuA_LOmV_AvsE_ls = ""
LOuA_LOmV_AvsE_linw = 3
LOuA_LOmV_AvsE_fmt = 'o'
LOuA_LOmV_AvsE_markersize = 5
LOuA_LOmV_AvsE_alpha = 0.7

LOuA_LOmV_AvsE_legend_size = 10
LOuA_LOmV_AvsE_legend_num_of_points = 3
LOuA_LOmV_AvsE_legend_loc = 0


# LOmV_LOfreq
LOmV_LOfreq_AvsE_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/LOmV_LOfreq/'))

LOmV_LOfreq_AvsE_xlim_list = None#[1.2, 1.4] # None or list of two [645, 695]
LOmV_LOfreq_AvsE_xlabel_str="LO frequency (GHz)"

LOmV_LOfreq_AvsE_ylim_list = None#[0, 25] # None or list of two [645, 695]
LOmV_LOfreq_AvsE_ylabel_str="Current (uA)"

LOmV_LOfreq_AvsE_ls = ""
LOmV_LOfreq_AvsE_linw = 3
LOmV_LOfreq_AvsE_fmt = 'o'
LOmV_LOfreq_AvsE_markersize = 5
LOmV_LOfreq_AvsE_alpha = 0.7

LOmV_LOfreq_AvsE_legend_size = 10
LOmV_LOfreq_AvsE_legend_num_of_points = 3
LOmV_LOfreq_AvsE_legend_loc = 0


# LOuA_LOfreq
LOuA_LOfreq_AvsE_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/LOuA_LOfreq/'))

LOuA_LOfreq_AvsE_xlim_list = None#[1.2, 1.4] # None or list of two [645, 695]
LOuA_LOfreq_AvsE_xlabel_str="LO frequency (GHz)"

LOuA_LOfreq_AvsE_ylim_list = None#[0, 25] # None or list of two [645, 695]
LOuA_LOfreq_AvsE_ylabel_str="Current (uA)"

LOuA_LOfreq_AvsE_ls = ""
LOuA_LOfreq_AvsE_linw = 3
LOuA_LOfreq_AvsE_fmt = 'o'
LOuA_LOfreq_AvsE_markersize = 5
LOuA_LOfreq_AvsE_alpha = 0.7

LOuA_LOfreq_AvsE_legend_size = 10
LOuA_LOfreq_AvsE_legend_num_of_points = 3
LOuA_LOfreq_AvsE_legend_loc = 0



# UCA_LOfreq
UCA_LOfreq_AvsE_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/UCA_LOfreq/'))

UCA_LOfreq_AvsE_xlim_list = None#[1.2, 1.4] # None or list of two [645, 695]
UCA_LOfreq_AvsE_xlabel_str="LO frequency (GHz)"

UCA_LOfreq_AvsE_ylim_list = None#[0, 25] # None or list of two [645, 695]
UCA_LOfreq_AvsE_ylabel_str="UCA (volts)"

UCA_LOfreq_AvsE_ls = ""
UCA_LOfreq_AvsE_linw = 3
UCA_LOfreq_AvsE_fmt = 'o'
UCA_LOfreq_AvsE_markersize = 5
UCA_LOfreq_AvsE_alpha = 0.7

UCA_LOfreq_AvsE_legend_size = 10
UCA_LOfreq_AvsE_legend_num_of_points = 3
UCA_LOfreq_AvsE_legend_loc = 0

# IFband_LOfreq
IFband_LOfreq_AvsE_plotdir = local_copy(windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/IFband_LOfreq/'))

IFband_LOfreq_AvsE_xlim_list = None#[1.2, 1.4] # None or list of two [645, 695]
IFband_LOfreq_AvsE_xlabel_str="LO frequency (GHz)"

IFband_LOfreq_AvsE_ylim_list = None#[0, 25] # None or list of two [645, 695]
IFband_LOfreq_AvsE_ylabel_str="IFband (volts)"

IFband_LOfreq_AvsE_ls = ""
IFband_LOfreq_AvsE_linw = 3
IFband_LOfreq_AvsE_fmt = 'o'
IFband_LOfreq_AvsE_markersize = 5
IFband_LOfreq_AvsE_alpha = 0.7

IFband_LOfreq_AvsE_legend_size = 10
IFband_LOfreq_AvsE_legend_num_of_points = 3
IFband_LOfreq_AvsE_legend_loc = 0





def isNum(testVar):
    try:
        float(testVar)
        return True
    except:
        return False



def return_variable(variable_str, Ysweep):
    variable = False
    variable_std = False
    if variable_str == 'LOfreq':
        variable = Ysweep.LOfreq
        variable_std = None
    elif  variable_str == 'magpot':
        variable = Ysweep.magpot
        variable_std = None
    elif variable_str == 'SIS_mV':
            variable = Ysweep.meanSIS_mV
            variable_std = Ysweep.stdSIS_mV
    elif variable_str == 'SIS_uA':
            variable = Ysweep.meanSIS_uA
            variable_std = Ysweep.stdSIS_uA
    elif variable_str == 'UCA_volt':
        variable = Ysweep.UCA_volt
    elif variable_str == 'SISpot':
        maxYfactor = max(Ysweep.Yfactor)
        maxYfactorIndex = Ysweep.Yfactor.index(maxYfactor)
        maxYfactor_SISpot = Ysweep.y_pot[maxYfactorIndex]
        variable=maxYfactor_SISpot
    elif variable_str == 'IFband':
        variable = Ysweep.IFband
    return variable, variable_std

def split_variable(K_vals,variables,variables_std=None):
    [K_val1,K_val2] = K_vals
    if variables is None:
        var1=None
        var2=None
    else:
        [var1,var2] = variables
    if variables_std is None:
        var1_std = None
        var2_std = None
    else:
        [var1_std,var2_std] = variables_std

    if ((250 < K_val1) and (K_val2 <= 250)):
        variable_hot = var1
        variable_std_hot = var1_std
        variable_cold = var2
        variable_std_cold = var2_std
    elif ((K_val1 < 250) and (250 <= K_val2)):
        variable_hot = var2
        variable_std_hot = var2_std
        variable_cold = var1
        variable_std_cold = var1_std
    else:
        print "something is wrong with the hot/cold data assignment"
        print 'script killed'
        sys.exit()
    return variable_hot, variable_std_hot, variable_cold, variable_std_cold





#######################################
###### Yfactor versus everything ######
#######################################
def Yfactor_vs(dependent_variable_str,
               Y_dependent_variable_plotdir,
               plot_xlim_list=None,
               xlabel_str=None,
               Y_dependent_variable_ls = "-",
               Y_dependent_variable_linw = 3,
               Y_dependent_variable_fmt = 'o',
               Y_dependent_variable_markersize = 5,
               Y_dependent_variable_alpha = 1.0,
               Y_dependent_variable_legend_size = 10,
               Y_dependent_variable_legend_num_of_points = 3,
               Y_dependent_variable_legend_loc = 3):
    if not os.path.isdir(Y_dependent_variable_plotdir): os.mkdir(Y_dependent_variable_plotdir)
    testmode = True
    leglines  = []
    leglabels = []

    fig, ax1 = plt.subplots()
    if xlabel_str is not None:
        ax1.set_xlabel(xlabel_str)
    if ylabel_str_Yfactor_vs is not None:
        ax1.set_ylabel(ylabel_str_Yfactor_vs)
    if plot_xlim_list is not None:
        ax1.set_xlim(plot_xlim_list)
    if plot_ylim_list_Yfactor_vs is not None:
        ax1.set_ylim(plot_ylim_list_Yfactor_vs)

    # get and plot the power meter data
    pm_max_Yfactors = []
    pm_max_y_mVs = []
    pm_max_Yfactor_dependent_variable = []
    for Ysweep in Ysweeps:
        (pm_max_Yfactor, pm_max_y_error, pm_max_y_mV,
         pm_max_y_mVerror, pm_max_y_uA,pm_max_y_uAerror,
         pm_max_y_TP, pm_max_y_TPerror, pm_max_y_pot)\
            = Ysweep.find_max_yfactor_pm()

        # get the dependent variable
        dependent_variable, dependent_variable_std = return_variable(dependent_variable_str, Ysweep)

        if min_Y_factor <= pm_max_Yfactor:
            pm_max_Yfactors.append(pm_max_Yfactor)
            pm_max_y_mVs.append(pm_max_y_mV)
            pm_max_Yfactor_dependent_variable.append(dependent_variable)
        if testmode:
            print  pm_max_Yfactor,':',dependent_variable,':'+dependent_variable_str+' :', pm_max_y_mV,' mV '+\
                   '  UCA:',Ysweep.UCA_volt,':  Ynum:',Ysweep.Ynum


    # Sort all the data to make monotonic lines in the domain of LO frequency
    list_of_lists = [pm_max_Yfactor_dependent_variable,pm_max_Yfactors,pm_max_y_mVs]
    sorted_list_of_lists = make_monotonic(list_of_lists,reverse=False)
    [pm_max_Yfactor_dependent_variable,pm_max_Yfactors,pm_max_y_mVs] = sorted_list_of_lists

    x_vector = pm_max_Yfactor_dependent_variable
    y_vector = pm_max_Yfactors


    ax1.plot(x_vector, y_vector,
             linestyle=Y_dependent_variable_ls,
             color=Y_pm_color,
             linewidth=Y_dependent_variable_linw,
             marker=Y_dependent_variable_fmt,
             markersize=Y_dependent_variable_markersize,
             markerfacecolor=Y_pm_color, alpha=Y_dependent_variable_alpha)
    leglines.append(plt.Line2D(range(10), range(10),
                               color=Y_pm_color,
                               ls=Y_dependent_variable_ls,
                               linewidth=Y_dependent_variable_linw,
                               marker=Y_dependent_variable_fmt,
                               markersize=Y_dependent_variable_markersize,
                               markerfacecolor=Y_pm_color,
                               alpha=Y_dependent_variable_alpha))
    leglabels.append("PM data")



    len_spec_colors = len(Y_spec_colors)
    # get and plot the spectrum analyzer data
    for band_index in range(len(spec_bands)-1):
        low_freq = spec_bands[band_index]
        high_freq = spec_bands[band_index+1]

        sa_Yfactors = []
        sa_Yfactor_mVs = []
        sa_Yfactor_freqs = []
        sa_Yfactor_dependent_variables = []
        for (index_Y,Ysweep) in list(enumerate(Ysweeps)):
            if Ysweep.spec_data_found:
                sa_max_Yfactor, sa_max_Yfactor_mV, sa_Yfactor_freq, sa_ave_Yfactor \
                    = Ysweep.find_max_yfactor_spec(min_freq=low_freq,max_freq=high_freq)

                # get the dependent variable
                dependent_variable, dependent_variable_std = return_variable(dependent_variable_str, Ysweep)

                if do_max_Yfactor:
                    sa_Yfactor = sa_max_Yfactor
                else:
                    sa_Yfactor = sa_ave_Yfactor
                if ((min_Y_factor <= sa_Yfactor)
                    and (Ysweep.fullpath !=windir('/Users/chw3k5/Google Drive/Kappa/NA38/IVsweep/LOfreq/'))):

                    sa_Yfactors.append(sa_Yfactor)
                    sa_Yfactor_mVs.append(sa_max_Yfactor_mV)
                    sa_Yfactor_freqs.append(sa_Yfactor_freq)
                    sa_Yfactor_dependent_variables.append(dependent_variable)

                if testmode:
                    print 'sa_Yfactor:',sa_Yfactor, '  max_Yfactor_dependent_variable:',dependent_variable,\
                        '  max_Yfactor_mV:',sa_max_Yfactor_mV, '  Yfactor_freq:',sa_Yfactor_freq
                    #print index_Y," Y index", Ysweep.name
                    #print len(Ysweep.spec_freq_list[1]),'length of self.spec_freq_list[1]'
        if sa_Yfactors != []:
            # Sort all the data to make monotonic lines in the domain of LO frequency
            list_of_lists = [sa_Yfactor_dependent_variables,sa_Yfactors,sa_Yfactor_mVs,sa_Yfactor_freqs]
            sorted_list_of_lists = make_monotonic(list_of_lists,reverse=False)
            [sa_Yfactor_dependent_variables,sa_Yfactors,sa_Yfactor_mVs,sa_Yfactor_freqs] = sorted_list_of_lists

            x_vector = sa_Yfactor_dependent_variables
            y_vector = sa_Yfactors
            color = Y_spec_colors[band_index % len_spec_colors]

            ax1.plot(x_vector, y_vector,
                     linestyle=Y_dependent_variable_ls,
                     color=color,
                     linewidth=Y_dependent_variable_linw,
                     marker=Y_dependent_variable_fmt,
                     markersize=Y_dependent_variable_markersize,
                     markerfacecolor=color,
                     alpha=Y_dependent_variable_alpha)
            leglines.append(plt.Line2D(range(10), range(10),
                                       color=color,
                                       ls=Y_dependent_variable_ls,
                                       linewidth=Y_dependent_variable_linw,
                                       marker=Y_dependent_variable_fmt,
                                       markersize=Y_dependent_variable_markersize,
                                       markerfacecolor=color,
                                       alpha=Y_dependent_variable_alpha))
            leglabels.append("SA data "+str(low_freq)+"-"+str(high_freq)+" GHz IF band")


    # stuff to make the final plot look good
    matplotlib.rcParams['legend.fontsize'] = Y_dependent_variable_legend_size
    plt.legend(tuple(leglines),tuple(leglabels),
               numpoints=Y_dependent_variable_legend_num_of_points,
               loc=Y_dependent_variable_legend_loc)

    plt.savefig(Y_dependent_variable_plotdir+"Yfactor_versus_"+dependent_variable_str+".png")
    plt.close('all')
    return


if any([do_Yfactor_versus_LO_freq, do_Yfactor_versus_magpot, do_Yfactor_versus_UCA,do_Yfactor_versus_SISpot,
        do_Yfactor_versus_IFband]):
    if do_Yfactor_versus_LO_freq:
        Yfactor_vs(dependent_variable_str='LOfreq',
                   Y_dependent_variable_plotdir=Y_LOfreq_plotdir,
                   plot_xlim_list=Y_LOfreq_xlim_list_Yfactor_versus,
                   xlabel_str=Y_LOfreq_xlabel_str_Yfactor_versus,
                   Y_dependent_variable_ls = Y_LOfreq_ls,
                   Y_dependent_variable_linw = Y_LOfreq_linw,
                   Y_dependent_variable_fmt = Y_LOfreq_fmt,
                   Y_dependent_variable_markersize = Y_LOfreq_markersize,
                   Y_dependent_variable_alpha = Y_LOfreq_alpha,
                   Y_dependent_variable_legend_size = Y_LOfreq_legend_size,
                   Y_dependent_variable_legend_num_of_points = Y_LOfreq_legend_num_of_points,
                   Y_dependent_variable_legend_loc = Y_LOfreq_legend_loc)
    if do_Yfactor_versus_magpot:
        Yfactor_vs(dependent_variable_str='magpot',
                   Y_dependent_variable_plotdir=Y_magpot_plotdir,
                   plot_xlim_list=Y_magpot_xlim_list_Yfactor_versus,
                   xlabel_str=Y_magpot_xlabel_str_Yfactor_versus,
                   Y_dependent_variable_ls = Y_magpot_ls,
                   Y_dependent_variable_linw = Y_magpot_linw,
                   Y_dependent_variable_fmt = Y_magpot_fmt,
                   Y_dependent_variable_markersize = Y_magpot_markersize,
                   Y_dependent_variable_alpha = Y_magpot_alpha,
                   Y_dependent_variable_legend_size = Y_magpot_legend_size,
                   Y_dependent_variable_legend_num_of_points = Y_magpot_legend_num_of_points,
                   Y_dependent_variable_legend_loc = Y_magpot_legend_loc)

    if do_Yfactor_versus_UCA:
        Yfactor_vs(dependent_variable_str='UCA_volt',
                   Y_dependent_variable_plotdir=Y_UCA_volt_plotdir,
                   plot_xlim_list=Y_UCA_volt_xlim_list_Yfactor_versus,
                   xlabel_str=Y_UCA_volt_xlabel_str_Yfactor_versus,
                   Y_dependent_variable_ls = Y_UCA_volt_ls,
                   Y_dependent_variable_linw = Y_UCA_volt_linw,
                   Y_dependent_variable_fmt = Y_UCA_volt_fmt,
                   Y_dependent_variable_markersize = Y_UCA_volt_markersize,
                   Y_dependent_variable_alpha = Y_UCA_volt_alpha,
                   Y_dependent_variable_legend_size = Y_UCA_volt_legend_size,
                   Y_dependent_variable_legend_num_of_points = Y_UCA_volt_legend_num_of_points,
                   Y_dependent_variable_legend_loc = Y_UCA_volt_legend_loc)
    if do_Yfactor_versus_SISpot:
        Yfactor_vs(dependent_variable_str='SISpot',
                   Y_dependent_variable_plotdir=Y_SISpot_plotdir,
                   plot_xlim_list=Y_SISpot_xlim_list_Yfactor_versus,
                   xlabel_str=Y_SISpot_xlabel_str_Yfactor_versus,
                   Y_dependent_variable_ls = Y_SISpot_ls,
                   Y_dependent_variable_linw = Y_SISpot_linw,
                   Y_dependent_variable_fmt = Y_SISpot_fmt,
                   Y_dependent_variable_markersize = Y_SISpot_markersize,
                   Y_dependent_variable_alpha = Y_SISpot_alpha,
                   Y_dependent_variable_legend_size = Y_SISpot_legend_size,
                   Y_dependent_variable_legend_num_of_points = Y_SISpot_legend_num_of_points,
                   Y_dependent_variable_legend_loc = Y_SISpot_legend_loc)

    if do_Yfactor_versus_IFband:
        Yfactor_vs(dependent_variable_str='IFband',
                   Y_dependent_variable_plotdir=Y_IFband_plotdir,
                   plot_xlim_list=Y_IFband_xlim_list_Yfactor_versus,
                   xlabel_str=Y_IFband_xlabel_str_Yfactor_versus,
                   Y_dependent_variable_ls = Y_IFband_ls,
                   Y_dependent_variable_linw = Y_IFband_linw,
                   Y_dependent_variable_fmt = Y_IFband_fmt,
                   Y_dependent_variable_markersize = Y_IFband_markersize,
                   Y_dependent_variable_alpha = Y_IFband_alpha,
                   Y_dependent_variable_legend_size = Y_IFband_legend_size,
                   Y_dependent_variable_legend_num_of_points = Y_IFband_legend_num_of_points,
                   Y_dependent_variable_legend_loc = Y_IFband_legend_loc)





########################################
###### Anything versus everything ######
########################################

def anything_vs(independent_variable_str,
                dependent_variable_str,
                plotdir,
                plot_xlim_list=None,
                xlabel_str=None,
                plot_ylim_list=None,
                ylabel_str=None,
                dVar_ls = "-",
                dVar_linw = 3,
                dVar_fmt = 'o',
                dVar_markersize = 5,
                dVar_alpha = 1.0,
                dVar_legend_size = 10,
                dVar_legend_num_of_points = 3,
                dVar_legend_loc = 3):
    if not os.path.isdir(plotdir): os.mkdir(plotdir)
    leglines  = []
    leglabels = []

    fig, ax1 = plt.subplots()
    if xlabel_str is not None:
        ax1.set_xlabel(xlabel_str)
    if ylabel_str is not None:
        ax1.set_ylabel(ylabel_str)
    if plot_xlim_list is not None:
        ax1.set_xlim(plot_xlim_list)
    if plot_ylim_list is not None:
        ax1.set_ylim(plot_ylim_list)


    independent_variable_hot = []
    independent_variable_std_hot = []
    independent_variable_cold = []
    independent_variable_std_cold = []

    independent_variable = []
    independent_variable_std = []

    dependent_variable_hot = []
    dependent_variable_std_hot = []
    dependent_variable_cold = []
    dependent_variable_std_cold = []

    dependent_variable = []
    dependent_variable_std = []

    for Ysweep in Ysweeps:
        # get the independent variable information
        indi_vari, indi_vari_std = return_variable(independent_variable_str, Ysweep)

        # there is different beauvoir is the variable has one value or two values (one for hot and one for cold)
        if isNum(indi_vari):
            if indi_vari is not None:
                independent_variable.append(indi_vari)
                if indi_vari_std is not None:
                    independent_variable_std.append(indi_vari_std)
        else:
            variable_hot, variable_std_hot, variable_cold, variable_std_cold \
                = split_variable(Ysweep.K_val,indi_vari,variables_std=indi_vari_std)
            if ((variable_hot is not None) and (variable_cold is not None)):
                independent_variable_hot.append(variable_hot)
                independent_variable_cold.append(variable_cold)
                if variable_std_hot is not None:
                    independent_variable_std_hot.append(variable_std_hot)
                if variable_std_cold is not None:
                    independent_variable_std_cold.append(variable_std_cold)


        # get the dependent variable information
        di_vari, di_vari_std = return_variable(dependent_variable_str, Ysweep)

        # there is different beauvoir is the variable has one value or two values (one for hot and one for cold)
        if isNum(di_vari):
            if di_vari is not None:
                dependent_variable.append(di_vari)
                if di_vari_std is not None:
                    dependent_variable_std.append(di_vari_std)
        else:
            variable_hot, variable_std_hot, variable_cold, variable_std_cold \
                = split_variable(Ysweep.K_val,di_vari,variables_std=di_vari_std)
            if ((variable_hot is not None) and (variable_cold is not None)):
                dependent_variable_hot.append(variable_hot)
                dependent_variable_cold.append(variable_cold)
                if variable_std_hot is not None:
                    dependent_variable_std_hot.append(variable_std_hot)
                if variable_std_cold is not None:
                    dependent_variable_std_cold.append(variable_std_cold)



    if ((independent_variable != []) and (dependent_variable != [])):
        x_vector = dependent_variable
        y_vector = independent_variable
        ax1.plot(x_vector, y_vector,
                 linestyle=dVar_ls,
                 color=neutral_color_AvsE,
                 linewidth=dVar_linw,
                 marker=dVar_fmt,
                 markersize=dVar_markersize,
                 markerfacecolor=neutral_color_AvsE, alpha=dVar_alpha)
        if dependent_variable_std != []:
            x_error = dependent_variable_std
            ax1.errorbar(x_vector, y_vector, xerr=x_error,
                             marker='|',color=color, capsize=1, linestyle='None', elinewidth=dVar_linw)

        leglines.append(plt.Line2D(range(10), range(10),
                                   color=neutral_color_AvsE,
                                   ls=dVar_ls,
                                   linewidth=dVar_linw,
                                   marker=dVar_fmt,
                                   markersize=dVar_markersize,
                                   markerfacecolor=neutral_color_AvsE,
                                   alpha=dVar_alpha))
        leglabels.append(independent_variable_str+"_"+dependent_variable_str)
    else:
        ### HOT ###
        if (dependent_variable != []):
            x_vectorHot = dependent_variable
            if dependent_variable_std == []:
                x_error_hot = None
            else:
                x_error_hot = dependent_variable_std
        else:
            x_vectorHot = dependent_variable_hot
            if dependent_variable_std_hot == []:
                x_error_hot = None
            else:
                x_error_hot = dependent_variable_std_hot

        if (independent_variable != []):
            y_vectorHot = independent_variable
            if independent_variable_std == []:
                y_error_hot = None
            else:
                y_error_hot = independent_variable_std
        else:
            y_vectorHot = independent_variable_hot
            if independent_variable_std_hot == []:
                y_error_hot = None
            else:
                y_error_hot = independent_variable_std_hot
        ax1.plot(x_vectorHot, y_vectorHot,
                 linestyle=dVar_ls,
                 color=hot_color_AvsE,
                 linewidth=dVar_linw,
                 marker=dVar_fmt,
                 markersize=dVar_markersize,
                 markerfacecolor=hot_color_AvsE, alpha=dVar_alpha)

        if (((y_error_hot is not None) or (x_error_hot is not None)) and (show_error_AvsE)):
            ax1.errorbar(x_vectorHot, y_vectorHot,
                         xerr=x_error_hot,yerr=y_error_hot,
                         marker=error_marker_AvsE,
                         color=cold_color_AvsE,
                         capsize=error_capsize_AvsE,
                         linestyle=error_ls_AvsE,
                         elinewidth=error_linw_AvsE)

        leglines.append(plt.Line2D(range(10), range(10),
                                   color=hot_color_AvsE,
                                   ls=dVar_ls,
                                   linewidth=dVar_linw,
                                   marker=dVar_fmt,
                                   markersize=dVar_markersize,
                                   markerfacecolor=hot_color_AvsE,
                                   alpha=dVar_alpha))
        leglabels.append(independent_variable_str+" vs "+dependent_variable_str+' hot')

        ### COLD ###
        if (dependent_variable != []):
            x_vectorCold = dependent_variable
            if dependent_variable_std == []:
                x_error_cold = None
            else:
                x_error_cold = dependent_variable_std
        else:
            x_vectorCold = dependent_variable_cold
            if dependent_variable_std_cold == []:
                x_error_cold = None
            else:
                x_error_cold = dependent_variable_std_cold

        if (independent_variable != []):
            y_vectorCold = independent_variable
            if independent_variable_std == []:
                y_error_cold = None
            else:
                y_error_cold = independent_variable_std
        else:
            y_vectorCold = independent_variable_cold
            if independent_variable_std_cold == []:
                y_error_cold = None
            else:
                y_error_cold = independent_variable_std_cold
        ax1.plot(x_vectorCold, y_vectorCold,
                 linestyle=dVar_ls,
                 color=cold_color_AvsE,
                 linewidth=dVar_linw,
                 marker=dVar_fmt,
                 markersize=dVar_markersize,
                 markerfacecolor=cold_color_AvsE, alpha=dVar_alpha)

        if (((y_error_cold is not None) or (x_error_cold is not None)) and (show_error_AvsE)):
            ax1.errorbar(x_vectorCold, y_vectorCold,
                         xerr=x_error_cold,yerr=y_error_cold,
                         marker=error_marker_AvsE,
                         color=hot_color_AvsE,
                         capsize=error_capsize_AvsE,
                         linestyle=error_ls_AvsE,
                         elinewidth=error_linw_AvsE)
        leglines.append(plt.Line2D(range(10), range(10),
                                   color=cold_color_AvsE,
                                   ls=dVar_ls,
                                   linewidth=dVar_linw,
                                   marker=dVar_fmt,
                                   markersize=dVar_markersize,
                                   markerfacecolor=cold_color_AvsE,
                                   alpha=dVar_alpha))
        leglabels.append(independent_variable_str+" vs "+dependent_variable_str+' cold')

        if show_pairs_AvsE:
            list_len = len(x_vectorHot)
            for index in range(list_len):
                hotX = x_vectorHot[index]
                hotY = y_vectorHot[index]
                coldX = x_vectorCold[index]
                coldY = y_vectorCold[index]
                ax1.plot([hotX,coldX], [hotY,coldY],
                         linestyle=pair_AvsE_ls,
                         color=pair_color_AvsE,
                         linewidth=pair_AvsE_linw,
                         alpha=pair_AvsE_alpha)
            leglines.append(plt.Line2D(range(10), range(10),
                                       color=pair_color_AvsE,
                                       ls=pair_AvsE_ls,
                                       linewidth=pair_AvsE_linw,
                                       alpha=pair_AvsE_alpha))
            leglabels.append(independent_variable_str+" vs "+dependent_variable_str+' pair line')







    # stuff to make the final plot look good
    matplotlib.rcParams['legend.fontsize'] = dVar_legend_size
    plt.legend(tuple(leglines),tuple(leglabels),
               numpoints=dVar_legend_num_of_points,
               loc=dVar_legend_loc)

    plt.savefig(plotdir+independent_variable_str+"_"+dependent_variable_str+".png")
    plt.close('all')
    return





if any([do_LOuA_LOmV_AvsE,do_LOmV_LOfreq_AvsE,do_LOuA_LOfreq_AvsE,do_UCA_LOfreq_AvsE,do_IFband_LOfreq_AvsE]):
    if do_LOuA_LOmV_AvsE:
        anything_vs(independent_variable_str='SIS_uA',
                    dependent_variable_str='SIS_mV',
                    plotdir=LOuA_LOmV_AvsE_plotdir,
                    plot_xlim_list=LOuA_LOmV_AvsE_xlim_list,
                    xlabel_str=LOuA_LOmV_AvsE_xlabel_str,
                    plot_ylim_list=LOuA_LOmV_AvsE_ylim_list,
                    ylabel_str=LOuA_LOmV_AvsE_ylabel_str,
                    dVar_ls = LOuA_LOmV_AvsE_ls,
                    dVar_linw = LOuA_LOmV_AvsE_linw,
                    dVar_fmt = LOuA_LOmV_AvsE_fmt,
                    dVar_markersize = LOuA_LOmV_AvsE_markersize,
                    dVar_alpha = LOuA_LOmV_AvsE_alpha,
                    dVar_legend_size = LOuA_LOmV_AvsE_legend_size,
                    dVar_legend_num_of_points = LOuA_LOmV_AvsE_legend_num_of_points,
                    dVar_legend_loc = LOuA_LOmV_AvsE_legend_loc)
    if do_LOmV_LOfreq_AvsE:
        anything_vs(independent_variable_str='SIS_mV',
                    dependent_variable_str='LOfreq',
                    plotdir=LOmV_LOfreq_AvsE_plotdir,
                    plot_xlim_list=LOmV_LOfreq_AvsE_xlim_list,
                    xlabel_str=LOmV_LOfreq_AvsE_xlabel_str,
                    plot_ylim_list=LOmV_LOfreq_AvsE_ylim_list,
                    ylabel_str=LOmV_LOfreq_AvsE_ylabel_str,
                    dVar_ls = LOmV_LOfreq_AvsE_ls,
                    dVar_linw = LOmV_LOfreq_AvsE_linw,
                    dVar_fmt = LOmV_LOfreq_AvsE_fmt,
                    dVar_markersize = LOmV_LOfreq_AvsE_markersize,
                    dVar_alpha = LOmV_LOfreq_AvsE_alpha,
                    dVar_legend_size = LOmV_LOfreq_AvsE_legend_size,
                    dVar_legend_num_of_points = LOmV_LOfreq_AvsE_legend_num_of_points,
                    dVar_legend_loc = LOmV_LOfreq_AvsE_legend_loc)


    if do_LOuA_LOfreq_AvsE:
        anything_vs(independent_variable_str='SIS_uA',
                    dependent_variable_str='LOfreq',
                    plotdir=LOuA_LOfreq_AvsE_plotdir,
                    plot_xlim_list=LOuA_LOfreq_AvsE_xlim_list,
                    xlabel_str=LOuA_LOfreq_AvsE_xlabel_str,
                    plot_ylim_list=LOuA_LOfreq_AvsE_ylim_list,
                    ylabel_str=LOuA_LOfreq_AvsE_ylabel_str,
                    dVar_ls = LOuA_LOfreq_AvsE_ls,
                    dVar_linw = LOuA_LOfreq_AvsE_linw,
                    dVar_fmt = LOuA_LOfreq_AvsE_fmt,
                    dVar_markersize = LOuA_LOfreq_AvsE_markersize,
                    dVar_alpha = LOuA_LOfreq_AvsE_alpha,
                    dVar_legend_size = LOuA_LOfreq_AvsE_legend_size,
                    dVar_legend_num_of_points = LOuA_LOfreq_AvsE_legend_num_of_points,
                    dVar_legend_loc = LOuA_LOfreq_AvsE_legend_loc)

    if do_UCA_LOfreq_AvsE:
        anything_vs(independent_variable_str='UCA_volt',
                    dependent_variable_str='LOfreq',
                    plotdir=UCA_LOfreq_AvsE_plotdir,
                    plot_xlim_list=UCA_LOfreq_AvsE_xlim_list,
                    xlabel_str=UCA_LOfreq_AvsE_xlabel_str,
                    plot_ylim_list=UCA_LOfreq_AvsE_ylim_list,
                    ylabel_str=UCA_LOfreq_AvsE_ylabel_str,
                    dVar_ls = UCA_LOfreq_AvsE_ls,
                    dVar_linw = UCA_LOfreq_AvsE_linw,
                    dVar_fmt = UCA_LOfreq_AvsE_fmt,
                    dVar_markersize = UCA_LOfreq_AvsE_markersize,
                    dVar_alpha = UCA_LOfreq_AvsE_alpha,
                    dVar_legend_size = UCA_LOfreq_AvsE_legend_size,
                    dVar_legend_num_of_points = UCA_LOfreq_AvsE_legend_num_of_points,
                    dVar_legend_loc = UCA_LOfreq_AvsE_legend_loc)

    if do_IFband_LOfreq_AvsE:
        anything_vs(independent_variable_str='IFband',
                    dependent_variable_str='LOfreq',
                    plotdir=IFband_LOfreq_AvsE_plotdir,
                    plot_xlim_list=IFband_LOfreq_AvsE_xlim_list,
                    xlabel_str=IFband_LOfreq_AvsE_xlabel_str,
                    plot_ylim_list=IFband_LOfreq_AvsE_ylim_list,
                    ylabel_str=IFband_LOfreq_AvsE_ylabel_str,
                    dVar_ls = IFband_LOfreq_AvsE_ls,
                    dVar_linw = IFband_LOfreq_AvsE_linw,
                    dVar_fmt = IFband_LOfreq_AvsE_fmt,
                    dVar_markersize = IFband_LOfreq_AvsE_markersize,
                    dVar_alpha = IFband_LOfreq_AvsE_alpha,
                    dVar_legend_size = IFband_LOfreq_AvsE_legend_size,
                    dVar_legend_num_of_points = IFband_LOfreq_AvsE_legend_num_of_points,
                    dVar_legend_loc = IFband_LOfreq_AvsE_legend_loc)
