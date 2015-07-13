import matplotlib, sys, numpy
from matplotlib import pyplot as plt
from domath import linfit, properrors
from profunc import getmultiParams
from datapro import local_copy, windir
from dataPhil_functions import DataTrimmer, Params_2_str

colors = ['BlueViolet','Brown','CadetBlue','Chartreuse', 'Chocolate','Coral','CornflowerBlue','Crimson','Cyan',
          'DarkBlue','DarkCyan','DarkGoldenRod', 'DarkGreen','DarkMagenta','DarkOliveGreen','DarkOrange',
          'DarkOrchid','DarkRed','DarkSalmon','DarkSeaGreen','DarkSlateBlue','DodgerBlue','FireBrick','ForestGreen',
          'Fuchsia','Gold','GoldenRod','Green','GreenYellow','HotPink','IndianRed','Indigo','LawnGreen',
          'LightCoral','Lime','LimeGreen','Magenta','Maroon', 'MediumAquaMarine','MediumBlue','MediumOrchid',
          'MediumPurple','MediumSeaGreen','MediumSlateBlue','MediumTurquoise','MediumVioletRed','MidnightBlue',
          'Navy','Olive','OliveDrab','Orange','OrangeRed','Orchid','PaleVioletRed','Peru','Pink','Plum','Purple',
          'Red','RoyalBlue','SaddleBrown','Salmon','SandyBrown','Sienna','SkyBlue','SlateBlue','SlateGrey',
          'SpringGreen','SteelBlue','Teal','Tomato','Turquoise','Violet','Yellow','YellowGreen']

color_len = len(colors)

#####################
###### Options ######
#####################
# This fraction is added to the total size of the curves on the axis to make a margin
x_margin_right = 0.
x_margin_left  = 0.
y_margin_top   = 0.5
y_margin_bot   = 0.


ax1_scaling = ('mV','tp')
ax2_scaling = ('mV','Yf')

### Plot Options ###
# Astro Data
hotmVuA_color = 'red'
hotmVuA_linw  = 5
hotmVuA_ls    = 'solid'

hotmVtp_color = 'blue'
hotmVtp_linw  = 3
hotmVtp_ls    = 'solid'

coldmVuA_color = 'coral'
coldmVuA_linw  = 4
coldmVuA_ls    = 'solid'

coldmVtp_color = 'dodgerblue'
coldmVtp_linw  = 2
coldmVtp_ls    = 'solid'

# Fast Data
hotfast_mVuA_color = 'green'
hotfast_mVuA_linw  = 2
hotfast_mVuA_ls    = 'solid'

hotfast_mVtp_color = 'gold'
hotfast_mVtp_linw  = 2
hotfast_mVtp_ls    = 'solid'

hotfast_mVpot_color = 'black'
hotfast_mVpot_linw  = 2
hotfast_mVpot_ls    = 'solid'

coldfast_mVuA_color = 'forestgreen'
coldfast_mVuA_linw  = 1
coldfast_mVuA_ls    = 'solid'

coldfast_mVtp_color = 'yellow'
coldfast_mVtp_linw  = 1
coldfast_mVtp_ls    = 'solid'

coldfast_mVpot_color = 'black'
coldfast_mVpot_linw  = 1
coldfast_mVpot_ls    = 'solid'

# Unpumped Data
hotunpump_mVuA_color = 'purple'
hotunpump_mVuA_linw  = 2
hotunpump_mVuA_ls    = 'solid'

hotunpump_mVtp_color = 'orange'
hotunpump_mVtp_linw  = 2
hotunpump_mVtp_ls    = 'solid'

hotunpump_mVpot_color = 'black'
hotunpump_mVpot_linw  = 1
hotunpump_mVpot_ls    = 'solid'

coldunpump_mVuA_color = 'magenta'
coldunpump_mVuA_linw  = 1
coldunpump_mVuA_ls    = 'solid'

coldunpump_mVtp_color = 'darkorange'
coldunpump_mVtp_linw  = 1
coldunpump_mVtp_ls    = 'solid'

coldunpump_mVpot_color = 'black'
coldunpump_mVpot_linw  = 1
coldunpump_mVpot_ls    = 'solid'

raw_linw       = 1
raw_fmt        = 'o'
raw_markersize = 10
raw_alpha      = 0.5
raw_capsize    = 2

hotrawmVuA_color  = hotmVuA_color
coldrawmVuA_color = coldmVuA_color
hotrawmVtp_color  = hotmVtp_color
coldrawmVtp_color = coldmVtp_color

# Calculate noise temperature instead
Yfactor_color = 'green'
Yfactor_linw  = 3
Yfactor_ls    = '-'
Yfactor_label = 'Y factor'

std_ls    = 'dotted'
std_linw  = 1

lin_color = 'black'
lin_linw  = 6
lin_ls    = '-'

### Labels ###
hot_labelPrefix  = '300K '
cold_labelPrefix = ' 77K '
fast_label       = 'fast '
unpump_label     = 'LOoff '

# Y-axis
ylimL2 =   0
ylimR2 =  10
yscale = abs(ylimR2 - ylimL2)

### Legend ###
legendsize = 8
legendloc  = 4

### Parameter Colors
K_val_color       = 'firebrick'
LOpwr_color       = 'dodgerblue'
mag_color         = 'coral'
LOfreq_color      = 'DarkOrchid'
IFband_color      = 'aquamarine'
TP_int_time_color = 'darkgreen'

hotrawmVuA_label  = hot_labelPrefix  + 'error mVuA'
coldrawmVuA_label = cold_labelPrefix + 'error mVuA'

hotrawmVtp_label  = hot_labelPrefix  + 'error mVtp'
coldrawmVtp_label = cold_labelPrefix + 'error mVtp'

ax1_xlabel = 'Voltage (' + str(ax1_scaling[0]) + ')'
if str(ax1_scaling[1]) == 'uA':
    ax1_ylabel = 'Current (uA)'
elif str(ax1_scaling[1]) == 'tp':
    ax1_ylabel = 'Total Power (uW)'
else:
    ax1_ylabel = '('+str(ax1_scaling[1])+')'
ax2_ylabel = 'Y-Factor'



def xyplotgen(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[],
              color='black', linw=1, ls='-', scale_str='' ):
    plot_list.append((x_vector, y_vector, color, linw, ls, scale_str))
    leglines.append((color,ls,linw))
    leglabels.append(label)
    return plot_list, leglines, leglabels

# plot_list, leglines, leglabels \
#   = xyplotgen2(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[],
#                color='black', linw=1, ls='-', alpha=1.0, scale_str='', leg_on=True )
def xyplotgen2(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[],
               color='black', linw=1, ls='-', alpha=1.0, scale_str='', leg_on=True ):
    plot_list.append((x_vector, y_vector, color, linw, ls, alpha, scale_str))
    if leg_on:
        leglines.append((color,ls,linw,alpha))
        leglabels.append(label)
    return plot_list, leglines, leglabels

def xyerrorplotgen(x_vector, y_vector, x_error=None, y_error=None,
                   label='', raw_plot_list=[], raw_leglines=[], raw_leglabels=[],
                   color='black', linw=1, fmt='o', markersize=10, alpha=1.0, capsize=1, scale_str=''):
    raw_plot_list.append((x_vector, y_vector, x_error, y_error, color,
                          linw, fmt, markersize, alpha, capsize, scale_str))
    raw_leglines.append((color,'-',linw))
    raw_leglabels.append(label)

    return raw_plot_list, raw_leglines, raw_leglabels

def stdaxplotgen(x_vector, y_vector, y_std, std_num=1, label='',
                 plot_list=[], leglines=[], leglabels=[],
                 color='black', linw=1, ls='-', scale_str=''):
    # Positive sigma
    plot_list.append((x_vector, y_vector+(y_std*std_num), color, linw, ls, scale_str))
    leglines.append(None)
    leglabels.append(None)
    # Negative sigma
    plot_list.append((x_vector, y_vector-(y_std*std_num), color, linw, ls, scale_str))
    leglines.append((color, ls, linw))

    leglabels.append(label)
    return plot_list, leglines, leglabels

def linifxyplotgen(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[],
                   color='black', linw=1, ls='-', scale_str='', linif=0.3,
                   der1_int=1, do_der1_conv=False, der1_min_cdf=0.90, der1_sigma=0.05, der2_int=1,
                   do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):
    slopes, intercepts, bestfits_x, bestfits_y \
                =  linfit(x_vector, y_vector, linif, der1_int, do_der1_conv, der1_min_cdf, der1_sigma, der2_int,
                          do_der2_conv, der2_min_cdf, der2_sigma, verbose)
    if slopes is not None:
        for n in range(len(bestfits_x[0,:])):
            plot_list.append((bestfits_x[:,n], bestfits_y[:, n], color, linw, ls, scale_str))
            leglines.append((color, ls, linw))
            resist = 1000*(1.0/slopes[n])
            if label is None:
                leglabels.append(None)
            else:
                leglabels.append(str('%3.1f' % resist)+label)
    return plot_list, leglines, leglabels


def extractval(val_list, val_index, defualt_val):
    try:
        val = val_list[val_index]
    except:
        val = defualt_val
    return val

def listplotgen(x_vector, y_vector_list, plot_list=[], leglines=[], leglabels=[],
                label_list=[], color_list=[], linw_list=[], ls_list=[], scale_str_list=[]):
    for y_index in range(len(y_vector_list)):
        y_vector  = y_vector_list[y_index]
        label     = extractval(label_list,     y_index, ''     )
        color     = extractval(color_list,     y_index, 'black')
        linw      = extractval(linw_list,      y_index, '1'    )
        ls        = extractval(ls_list,        y_index, '-'    )
        scale_str = extractval(scale_str_list, y_index, ''     )
        plot_list, leglines, leglabels = xyplotgen(x_vector, y_vector, label=label,
                                                   plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                                                   color=color, linw=linw, ls=ls, scale_str=scale_str )

    return plot_list, leglines, leglabels

def allstarplotgen(x_vector, y_vector, y_std=None, std_num=1, plot_list=[], leglines=[], leglabels=[],
                   show_std=False, find_lin=False,
                   label='', std_label='', lin_label='',
                   color='red', lin_color='black',
                   linw=1, std_linw=1, lin_linw=1,
                   ls='-', std_ls='dotted', lin_ls='-',
                   scale_str='', linif=0.3,
                   der1_int=1, do_der1_conv=False, der1_min_cdf=0.9, der1_sigma=0.05,
                   der2_int=1, do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):
    plot_list, leglines, leglabels = xyplotgen(x_vector=x_vector, y_vector=y_vector, label=label,
                                               plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                                               color=color, linw=linw, ls=ls, scale_str=scale_str )
    if (show_std and (y_std is not None)):
        std_label = str(std_num)+" sigma"
        plot_list, leglines, leglabels \
        = stdaxplotgen(x_vector, y_vector, y_std, std_num=std_num, label=std_label,
                       plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                       color=color, linw=std_linw, ls=std_ls, scale_str=scale_str)
    if find_lin:
        plot_list, leglines, leglabels \
            = linifxyplotgen(x_vector, y_vector, label=lin_label, plot_list=plot_list, leglines=leglines, leglabels=leglabels,
               color=lin_color, linw=lin_linw, ls=lin_ls, scale_str=scale_str, linif=linif,
               der1_int=der1_int, do_der1_conv=do_der1_conv, der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
               der2_int=der2_int, do_der2_conv=do_der2_conv, der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
               verbose=verbose)
    return plot_list, leglines, leglabels

def astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                     mV_min, mV_max,
                     plot_list=[], leglines=[], leglabels=[],
                     yscale_info=[],
                     plot_mVuA=False, plot_mVtp=False,
                     show_standdev=False, std_num=1,
                     find_lin_mVuA=False, find_lin_mVtp=False, find_lin_uAtp=False,
                     mVuA_color='blue', mVtp_color='red', uAtp_color='purple', lin_color='black',
                     mVuA_linw=1, mVtp_linw=1, uAtp_linw=1, std_linw=1, lin_linw=1,
                     mVuA_ls = '-', mVtp_ls='-', uAtp_ls='-', std_ls='dotted', lin_ls='-',
                     labelPrefix='',
                     linif=0.3, der1_int=1, do_der1_conv=False, der1_min_cdf=0.9, der1_sigma=0.05,
                     der2_int=1,do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1, verbose=False):

    if 1 < len(list(mV)):
        trim_list = [mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx]
        # The trimming part of the script for mV values on the X-axis
        if ((mV_min is None) and (mV_max is None)):
            if verbose:
                print "Data trimming is not selected"
                print "the plot X-axis min and max will depend on the lines being plotted"
        else:
            status, mV, trimmed_list = DataTrimmer(mV_min, mV_max, mV, trim_list)
            if not status:
                print "The program failed the Data trimming"
                print "killing the script"
                sys.exit()

            [mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx] = trimmed_list


    # (Xdata, Y_data, color, linewidth, linestyle, scales-like-'TP'or'uA'or'')
    if plot_mVuA:
        label       = labelPrefix+'Astro IV'
        std_label   = ' sigma'
        lin_label   = ' Ohms'
        x_vector    = mV
        y_vector    = uA
        y_std       = uA_std
        scale_str   = 'uA'
        find_lin    = find_lin_mVuA
        color       = mVuA_color
        linw        = mVuA_linw
        ls          = mVuA_ls
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))
        plot_list, leglines, leglabels \
            = allstarplotgen(x_vector, y_vector, y_std=y_std, std_num=std_num,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=show_standdev, find_lin=find_lin,
                             label=label, std_label=std_label, lin_label=lin_label,
                             color=color, lin_color=lin_color,
                             linw=linw, std_linw=std_linw, lin_linw=lin_linw,
                             ls=ls, std_ls=std_ls, lin_ls=lin_ls,
                             scale_str=scale_str, linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv,
                             der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv,
                             der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)

    if plot_mVtp:
        label     = labelPrefix+'Astro TP'
        std_label = ' sigma'
        lin_label = ''
        x_vector  = mV
        y_vector  = TP
        y_std     = TP_std
        scale_str = 'tp'
        find_lin  = find_lin_mVtp
        color     = mVtp_color
        linw      = mVtp_linw
        ls        = mVtp_ls
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))
        plot_list, leglines, leglabels \
            = allstarplotgen(x_vector, y_vector, y_std=y_std, std_num=std_num,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=show_standdev, find_lin=find_lin,
                             label=label, std_label=std_label, lin_label=lin_label,
                             color=color, lin_color=lin_color,
                             linw=linw, std_linw=std_linw, lin_linw=lin_linw,
                             ls=ls, std_ls=std_ls, lin_ls=lin_ls,
                             scale_str=scale_str, linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv,
                             der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv,
                             der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)

    return plot_list, leglines, leglabels, yscale_info

def fastplotgen(mV,uA,tp,pot,
                mV_min=None,mV_max=None,
                plot_list=[], leglines=[], leglabels=[],
                xscale_info=[],yscale_info=[],
                labelPrefix='',type_label='',
                plot_mVuA=False, plot_mVtp=False, plot_mVpot=False,
                find_lin_mVuA=False,
                mVuA_color='blue', mVtp_color='red',mVpot_color='black', find_lin_color='black',
                mVuA_ls='solid', mVtp_ls='solid', mVpot_ls='solid', find_lin_ls='solid',
                mVuA_linw=1, mVtp_linw=1, mVpot_linw=1, find_lin_linw=1,
                linif=0.3,
                der1_int=1, do_der1_conv=False, der1_min_cdf=0.9, der1_sigma=0.05,
                der2_int=1, do_der2_conv=False, der2_min_cdf=0.9, der2_sigma=0.1,
                verbose=False):
    # The trimming part of the script for mV values on the X-axis
    if ((mV_min is None) and (mV_max is None)):
        if verbose:
            print "Data trimming is not selected"
            print "the plot X-axis min and max will depend on the lines being plotted"
    else:

        trim_list = [uA,tp,pot]
        status, mV, trimmed_list = DataTrimmer(mV_min, mV_max, mV, trim_list)
        if not status:
            print "The program failed the Data trimming"
            print "killing the script"
            sys.exit()
        if verbose:
            print "Data has been trimmed"
        [uA,tp,pot] = trimmed_list


    xscale_str = 'mV'
    x_vector = mV
    xscale_info.append((xscale_str,min(x_vector),max(x_vector)))

    y_vector_list  = []
    label_list     = []
    color_list     = []
    linw_list      = []
    ls_list        = []
    scale_str_list = []
    if plot_mVuA:
        scale_str = 'uA'
        y_vector  = uA
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))
        #y_vector_list.append(list(y_vector))
        #label_list.append(labelPrefix+' '+type_label+' '+scale_str)
        #color_list.append(mVuA_color)
        #linw_list.append(mVuA_linw)
        #ls_list.append(mVuA_ls)
        #scale_str_list.append(scale_str)


        plot_list, leglines, leglabels \
            = allstarplotgen(x_vector, y_vector, y_std=None, std_num=1,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=False, find_lin=find_lin_mVuA,
                             label=labelPrefix+' '+type_label+' '+scale_str, std_label='', lin_label=' Ohms',
                             color=mVuA_color, lin_color=find_lin_color,
                             linw=mVuA_linw, std_linw=1, lin_linw=find_lin_linw,
                             ls=mVuA_ls, std_ls='dotted', lin_ls=find_lin_ls,
                             scale_str=scale_str, linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv,
                             der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv,
                             der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)


    if plot_mVtp:
        scale_str = 'tp'
        y_vector  = tp
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))

        y_vector_list.append(list(y_vector))
        label_list.append(labelPrefix+' '+type_label+' '+scale_str)
        color_list.append(mVtp_color)
        linw_list.append(mVtp_linw)
        ls_list.append(mVtp_ls)
        scale_str_list.append(scale_str)
    if plot_mVpot:
        scale_str = 'pot'
        y_vector  = pot
        yscale_info.append((scale_str, min(y_vector), max(y_vector)))

        y_vector_list.append(list(y_vector))
        label_list.append(labelPrefix+' '+type_label+' '+scale_str)
        color_list.append(mVpot_color)
        linw_list.append(mVpot_linw)
        ls_list.append(mVpot_ls)
        scale_str_list.append(scale_str)

    plot_list, leglines, leglabels\
        = listplotgen(x_vector, y_vector_list, plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                      label_list=label_list, color_list=color_list,
                      linw_list=linw_list, ls_list=ls_list, scale_str_list=scale_str_list)
    return plot_list, leglines, leglabels, xscale_info, yscale_info

def finddatalims(scale_info):
    min_val =  999999
    max_val = -999999
    overall_scale = []
    scale_types   = []
    for scale in scale_info:
        test1_scale_str = scale[0]
        test1_min_val   = scale[1]
        test1_max_val   = scale[2]
        try:
            # test to see if the reference exists
            scale_types_index = scale_types.index(test1_scale_str)
            # if it it exists, then we figure out whos maxes and mins are bigger
            oscale = overall_scale[scale_types_index]
            test2_scale_str = oscale[0]
            test2_min_val   = oscale[1]
            test2_max_val   = oscale[2]
            min_val = min(test1_min_val, test2_min_val)
            max_val = max(test1_max_val, test2_max_val)
            # get rid of the old reference
            scale_types.pop(scale_types_index)
            overall_scale.pop(scale_types_index)
            # append the new reference
            overall_scale.append((test1_scale_str,min_val,max_val))
            scale_types.append(test1_scale_str)
        except ValueError:
            # append the new reference
            overall_scale.append((test1_scale_str,test1_min_val,test1_max_val))
            scale_types.append(test1_scale_str)

    return overall_scale

def determine_scales(scale_str, scale_maxmins):
    scales = []
    for scale_maxmin in scale_maxmins:
        test_scale_str = scale_maxmin[0]
        if test_scale_str == scale_str:
            prime_scale_min = scale_maxmin[1]
            prime_scale_max = scale_maxmin[2]
            abs_prime_scale_max = max(abs(prime_scale_max),abs(prime_scale_min))
            scales.append((scale_str, 1))
    for scale_maxmin in scale_maxmins:
        test_scale_str = scale_maxmin[0]
        if test_scale_str == scale_str:
            None
        else:
            divisor_scale_min = scale_maxmin[1]
            divisor_scale_max = scale_maxmin[2]
            abs_divisor_scale_max = max(abs(divisor_scale_max), abs(divisor_scale_min))
            scale_factor = abs_prime_scale_max/abs_divisor_scale_max
            scales.append((test_scale_str, scale_factor))
    return scales

def findscaling(scale_str,scales):
    scale_factor = None
    for scale in scales:
        test_str = scale[0]
        if test_str == scale_str:
            scale_factor = float(scale[1])
            break
    return scale_factor

def findscalemaxmin(scale_str,scales):
    scale_min = None
    scale_max = None
    for scale in scales:
        test_str = scale[0]
        if test_str == scale_str:
            scale_min = scale[1]
            scale_max = scale[2]
            break
    return scale_min, scale_max




def sweepPlotter(Ysweep,
                 verbose=False, mV_min=None, mV_max=None,
                 Y_mV_min=None, Y_mV_max=None,
                 plot_rawhot_mVuA=False, plot_rawhot_mVtp=False,
                 plot_rawcold_mVuA=False, plot_rawcold_mVtp=False,
                 show_standdev=True, std_num=1, display_params=True,
                 show_plot=False, save_plot=True, do_eps=True,
                 plot_mVuA=True, plot_mVtp=True, plot_Yfactor=False, plot_Ntemp=False,
                 plot_fastmVuA=False, plot_fastmVtp=False, plot_fastmVpot=False,
                 hotfast_find_lin_mVuA=False, coldfast_find_lin_mVuA=False,
                 plot_unpumpmVuA=False, plot_unpumpmVtp=False, plot_unpumpmVpot=False,
                 hotunpumped_find_lin_mVuA=False, coldunpumped_find_lin_mVuA=False,
                 find_lin_mVuA=False, find_lin_mVtp=False, find_lin_Yf=False,
                 linif=0.3,
                 der1_int=1, do_der1_conv=True, der1_min_cdf=0.95, der1_sigma=0.03,
                 der2_int=1, do_der2_conv=True, der2_min_cdf=0.95, der2_sigma=0.05,
                 do_xkcd=False
                 ):



    ### Axis Limits ###
    # X-axis
    if mV_min is not None:
        xlimL = mV_min
    else:
        xlimL = 999999.
    if mV_max is not None:
        xlimR = mV_max
    else:
        xlimR = -999999.


    if verbose:
        print "ploting for "+Ysweep.longDescription()

    proYdatadir  = Ysweep.proYdatadir

    ax1_plot_list   = []
    ax2_plot_list   = []
    raw_plot_list   = []
    leglines        = []
    leglabels       = []
    xscale_info     = []
    ax1_yscale_info = []
    ax2_yscale_info = []

    if Ysweep.hotdatafound:
        #Solid line Plots
        labelPrefix = hot_labelPrefix
        mV       = Ysweep.hot_mV_mean
        mV_std   = Ysweep.hot_mV_std
        uA       = Ysweep.hot_uA_mean
        uA_std   = Ysweep.hot_uA_std
        TP       = Ysweep.hot_TP_mean
        TP_std   = Ysweep.hot_TP_std
        time_apx = Ysweep.hot_time_mean
        pot_apx  = Ysweep.hot_pot
        xscale_str = 'mV'
        mVuA_color = hotmVuA_color
        mVtp_color = hotmVtp_color
        mVuA_linw  = hotmVuA_linw
        mVtp_linw  = hotmVtp_linw
        mVuA_ls    = hotmVuA_ls
        mVtp_ls    = hotmVtp_ls

        xscale_info.append((xscale_str,min(mV),max(mV)))
        ax1_plot_list, leglines, leglabels, yax1_scale_info \
            = astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                              mV_min, mV_max,
                              plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                              yscale_info=ax1_yscale_info,
                              plot_mVuA=plot_mVuA, plot_mVtp=plot_mVtp,
                              show_standdev=show_standdev, std_num=std_num,
                              find_lin_mVuA=find_lin_mVuA, find_lin_mVtp=find_lin_mVtp,
                              mVuA_color=mVuA_color, mVtp_color=mVtp_color, lin_color=lin_color,
                              mVuA_linw=mVuA_linw, mVtp_linw=mVtp_linw, std_linw=std_linw, lin_linw=lin_linw,
                              mVuA_ls=mVuA_ls, mVtp_ls=mVtp_ls, std_ls=std_ls, lin_ls=lin_ls,
                              labelPrefix=labelPrefix,
                              linif=linif,
                              der1_int=der1_int, do_der1_conv=do_der1_conv,
                              der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                              der2_int=der2_int, do_der2_conv=do_der2_conv,
                              der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                              verbose=verbose)

    if Ysweep.hotrawdatafound:
        # Raw data with error bar plots
        if plot_rawhot_mVuA:
            xscale_str = 'mV'
            yscale_str = 'uA'
            mV       = Ysweep.hotraw_mV_mean
            mV_std   = Ysweep.hotraw_mV_std
            uA       = Ysweep.hotraw_uA_mean
            uA_std   = Ysweep.hotraw_uA_std
            xscale_info.append((xscale_str,min(mV),max(mV)))
            yax1_scale_info.append((yscale_str,min(uA),max(uA)))
            raw_plot_list, leglines, leglabels \
                = xyerrorplotgen(mV, uA, x_error=mV_std, y_error=uA_std,
                                 label='error mVuA', raw_plot_list=raw_plot_list,
                                 raw_leglines=leglines, raw_leglabels=leglabels,
                                 color=hotrawmVuA_color, linw=raw_linw,  fmt=raw_fmt, markersize=raw_markersize,
                                 alpha=raw_alpha, capsize=raw_capsize, scale_str=yscale_str)

        if plot_rawhot_mVtp:
            xscale_str = 'mV'
            yscale_str = 'tp'
            mV       = Ysweep.hotraw_mV_mean
            mV_std   = Ysweep.hotraw_mV_std
            tp       = Ysweep.hotraw_TP_mean
            tp_std   = Ysweep.hotraw_TP_std
            xscale_info.append((xscale_str,min(mV),max(mV)))
            yax1_scale_info.append((yscale_str,min(tp),max(tp)))
            raw_plot_list, leglines, leglabels \
                = xyerrorplotgen(mV, tp, x_error=mV_std, y_error=tp_std,
                                 label='error mVtp', raw_plot_list=raw_plot_list,
                                 raw_leglines=leglines, raw_leglabels=leglabels,
                                 color=hotrawmVtp_color, linw=raw_linw,  fmt=raw_fmt, markersize=raw_markersize,
                                 alpha=raw_alpha, capsize=raw_capsize, scale_str=yscale_str)



    if Ysweep.colddatafound:
        labelPrefix = cold_labelPrefix
        mV       = Ysweep.cold_mV_mean
        mV_std   = Ysweep.cold_mV_std
        uA       = Ysweep.cold_uA_mean
        uA_std   = Ysweep.cold_uA_std
        TP       = Ysweep.cold_TP_mean
        TP_std   = Ysweep.cold_TP_std
        time_apx = Ysweep.cold_time_mean
        pot_apx  = Ysweep.cold_pot
        xscale_str = 'mV'
        mVuA_color = coldmVuA_color
        mVtp_color = coldmVtp_color
        mVuA_linw  = coldmVuA_linw
        mVtp_linw  = coldmVtp_linw
        mVuA_ls    = coldmVuA_ls
        mVtp_ls    = coldmVtp_ls

        xscale_info.append((xscale_str,min(mV),max(mV)))
        ax1_plot_list, leglines, leglabels, yax1_scale_info \
            = astroplodatagen(mV, mV_std, uA, uA_std, TP, TP_std, time_apx, pot_apx,
                              mV_min, mV_max,
                              plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                              yscale_info=ax1_yscale_info,
                              plot_mVuA=plot_mVuA, plot_mVtp=plot_mVtp,
                              show_standdev=show_standdev, std_num=std_num,
                              find_lin_mVuA=find_lin_mVuA, find_lin_mVtp=find_lin_mVtp,
                              mVuA_color=mVuA_color, mVtp_color=mVtp_color, lin_color=lin_color,
                              mVuA_linw=mVuA_linw, mVtp_linw=mVtp_linw, std_linw=std_linw, lin_linw=lin_linw,
                              mVuA_ls=mVuA_ls, mVtp_ls=mVtp_ls, std_ls=std_ls, lin_ls=lin_ls,
                              labelPrefix=labelPrefix,
                              linif=linif,
                              der1_int=der1_int, do_der1_conv=do_der1_conv,
                              der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                              der2_int=der2_int, do_der2_conv=do_der2_conv,
                              der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                              verbose=verbose)

    if Ysweep.coldrawdatafound:
        # Raw data with error bar plots
        if plot_rawcold_mVuA:
            xscale_str = 'mV'
            yscale_str = 'uA'
            mV       = Ysweep.coldraw_mV_mean
            mV_std   = Ysweep.coldraw_mV_std
            uA       = Ysweep.coldraw_uA_mean
            uA_std   = Ysweep.coldraw_uA_std
            xscale_info.append((xscale_str,min(mV),max(mV)))
            yax1_scale_info.append((yscale_str,min(uA),max(uA)))
            raw_plot_list, leglines, leglabels \
                = xyerrorplotgen(mV, uA, x_error=mV_std, y_error=uA_std,
                                 label='error mVuA', raw_plot_list=raw_plot_list,
                                 raw_leglines=leglines, raw_leglabels=leglabels,
                                 color=coldrawmVuA_color, linw=raw_linw,  fmt=raw_fmt, markersize=raw_markersize,
                                 alpha=raw_alpha, capsize=raw_capsize, scale_str=yscale_str)

        if plot_rawcold_mVtp:
            xscale_str = 'mV'
            yscale_str = 'tp'
            mV       = Ysweep.coldraw_mV_mean
            mV_std   = Ysweep.coldraw_mV_std
            tp       = Ysweep.coldraw_TP_mean
            tp_std   = Ysweep.coldraw_TP_std
            xscale_info.append((xscale_str,min(mV),max(mV)))
            yax1_scale_info.append((yscale_str,min(tp),max(tp)))
            raw_plot_list, leglines, leglabels \
                = xyerrorplotgen(mV, tp, x_error=mV_std, y_error=tp_std,
                                 label='error mVtp', raw_plot_list=raw_plot_list,
                                 raw_leglines=leglines, raw_leglabels=leglabels,
                                 color=coldrawmVtp_color, linw=raw_linw,  fmt=raw_fmt, markersize=raw_markersize,
                                 alpha=raw_alpha, capsize=raw_capsize, scale_str=yscale_str)


    if ((Ysweep.Ydatafound) and (plot_Yfactor)):
        if ((Y_mV_min is not None) or (Y_mV_max is not None)):
            status, trim_mV_Yfactor, trimmed_list = DataTrimmer(Y_mV_min, Y_mV_max, Ysweep.y_mV, [Ysweep.Yfactor])
            trim_Yfactor = trimmed_list[0]
        else:
            trim_mV_Yfactor = Ysweep.y_mV
            trim_Yfactor    = Ysweep.Yfactor


        if show_standdev:
            y_std = properrors(Ysweep.cold_TP_mean,Ysweep.cold_TP_std,
                               Ysweep.hot_TP_mean,Ysweep.hot_TP_std,Ysweep.Yfactor)
        else:
            y_std = None
        Yfactor_min = min(trim_Yfactor)
        Yfactor_max = max(trim_Yfactor)
        mV_Yfactor_min = trim_mV_Yfactor[list(trim_Yfactor).index(Yfactor_min)]
        mV_Yfactor_max = trim_mV_Yfactor[list(trim_Yfactor).index(Yfactor_max)]

        if ax2_scaling[1] == 'Yf':
            ax2_yscale_info.append(('Yf', Yfactor_min, Yfactor_max))
            plot_list = ax2_plot_list
        else:
            ax1_yscale_info.append(('Yf', Yfactor_min, Yfactor_max))
            plot_list = ax1_plot_list

        xscale_info.append((xscale_str,mV_Yfactor_min,mV_Yfactor_max))
        plot_list, leglines, leglabels \
            = allstarplotgen(Ysweep.y_mV, Ysweep.Yfactor, y_std=y_std, std_num=std_num,
                             plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                             show_std=show_standdev, find_lin=find_lin_Yf,
                             label=Yfactor_label, std_label=' sigma', lin_label='',
                             color=Yfactor_color, lin_color=lin_color,
                             linw=Yfactor_linw, std_linw=Yfactor_linw, lin_linw=lin_linw,
                             ls=Yfactor_ls, std_ls=std_ls, lin_ls=lin_ls,
                             scale_str='Yf', linif=linif,
                             der1_int=der1_int, do_der1_conv=do_der1_conv,
                             der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                             der2_int=der2_int, do_der2_conv=do_der2_conv,
                             der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                             verbose=verbose)
        plot_list, leglines_junk, leglabels_junk \
            = xyplotgen(Ysweep.y_mV, numpy.ones(len(Ysweep.y_mV)), label='',
                         plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                        color=Yfactor_color, linw=1, ls='-', scale_str='Yf' )
        if ax2_scaling[1] == 'Yf':
            ax2_plot_list = plot_list
        else:
            ax1_plot_list =  plot_list

    ##################################
    ###### Fast Bias Sweep Data ######
    ##################################

    if Ysweep.hot_fastprodata_found:
        type_label = 'fast'
        ax1_plot_list, leglines, leglabels, xscale_info, ax1_yscale_info \
            = fastplotgen(Ysweep.hot_mV_fast,Ysweep.hot_uA_fast,Ysweep.hot_tp_fast,Ysweep.hot_pot_fast,
                          mV_min=mV_min,mV_max=mV_max,
                          plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                          xscale_info=xscale_info, yscale_info=ax1_yscale_info,
                          labelPrefix=hot_labelPrefix,type_label=type_label,
                          plot_mVuA=plot_fastmVuA, plot_mVtp=plot_fastmVtp, plot_mVpot=plot_fastmVpot,
                          find_lin_mVuA=hotfast_find_lin_mVuA,
                          mVuA_color=hotfast_mVuA_color, mVtp_color=hotfast_mVtp_color,
                          mVpot_color=hotfast_mVpot_color, find_lin_color=lin_color,
                          mVuA_ls=hotfast_mVuA_ls, mVtp_ls=hotfast_mVtp_ls,
                          mVpot_ls=hotfast_mVpot_ls, find_lin_ls=lin_ls,
                          mVuA_linw=hotfast_mVuA_linw, mVtp_linw=hotfast_mVtp_linw,
                          mVpot_linw=hotfast_mVpot_linw, find_lin_linw=lin_linw,
                          linif=linif,
                          der1_int=der1_int, do_der1_conv=do_der1_conv,
                          der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                          der2_int=der2_int, do_der2_conv=do_der2_conv,
                          der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                          verbose=verbose)

    if Ysweep.cold_fastprodata_found:
        type_label = 'fast'
        ax1_plot_list, leglines, leglabels, xscale_info, ax1_yscale_info \
            = fastplotgen(Ysweep.cold_mV_fast,Ysweep.cold_uA_fast,Ysweep.cold_tp_fast,Ysweep.cold_pot_fast,
                          mV_min=mV_min,mV_max=mV_max,
                          plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                          xscale_info=xscale_info, yscale_info=ax1_yscale_info,
                          labelPrefix=cold_labelPrefix,type_label=type_label,
                          plot_mVuA=plot_fastmVuA, plot_mVtp=plot_fastmVtp, plot_mVpot=plot_fastmVpot,
                          find_lin_mVuA=coldfast_find_lin_mVuA,
                          mVuA_color=coldfast_mVuA_color, mVtp_color=coldfast_mVtp_color,
                          mVpot_color=coldfast_mVpot_color, find_lin_color=lin_color,
                          mVuA_ls=coldfast_mVuA_ls, mVtp_ls=coldfast_mVtp_ls,
                          mVpot_ls=coldfast_mVpot_ls, find_lin_ls=lin_ls,
                          mVuA_linw=coldfast_mVuA_linw, mVtp_linw=coldfast_mVtp_linw,
                          mVpot_linw=coldfast_mVpot_linw, find_lin_linw=lin_linw,
                          linif=linif,
                          der1_int=der1_int, do_der1_conv=do_der1_conv,
                          der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                          der2_int=der2_int, do_der2_conv=do_der2_conv,
                          der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                          verbose=verbose)

    if Ysweep.hot_unpumpedprodata_found:
        type_label = 'unpumped'
        ax1_plot_list, leglines, leglabels, xscale_info, ax1_yscale_info \
            = fastplotgen(Ysweep.hot_mV_unpumped,Ysweep.hot_uA_unpumped,Ysweep.hot_tp_unpumped,Ysweep.hot_pot_unpumped,
                          mV_min=mV_min,mV_max=mV_max,
                          plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                          xscale_info=xscale_info, yscale_info=ax1_yscale_info,
                          labelPrefix=hot_labelPrefix,type_label=type_label,
                          plot_mVuA=plot_unpumpmVuA, plot_mVtp=plot_unpumpmVtp, plot_mVpot=plot_unpumpmVpot,
                          find_lin_mVuA=hotunpumped_find_lin_mVuA,
                          mVuA_color=hotunpump_mVuA_color, mVtp_color=hotunpump_mVtp_color,
                          mVpot_color=hotunpump_mVpot_color, find_lin_color=lin_color,
                          mVuA_ls=hotunpump_mVuA_ls, mVtp_ls=hotunpump_mVtp_ls,
                          mVpot_ls=hotunpump_mVpot_ls, find_lin_ls=lin_ls,
                          mVuA_linw=hotunpump_mVuA_linw, mVtp_linw=hotunpump_mVtp_linw,
                          mVpot_linw=hotunpump_mVpot_linw, find_lin_linw=lin_linw,
                          linif=linif,
                          der1_int=der1_int, do_der1_conv=do_der1_conv,
                          der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                          der2_int=der2_int, do_der2_conv=do_der2_conv,
                          der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                          verbose=verbose)

    if Ysweep.cold_unpumpedprodata_found:
        type_label = 'unpumped'
        ax1_plot_list, leglines, leglabels, xscale_info, ax1_yscale_info \
            = fastplotgen(Ysweep.cold_mV_unpumped,Ysweep.cold_uA_unpumped,
                          Ysweep.cold_tp_unpumped,Ysweep.cold_pot_unpumped,
                          mV_min=mV_min,mV_max=mV_max,
                          plot_list=ax1_plot_list, leglines=leglines, leglabels=leglabels,
                          xscale_info=xscale_info, yscale_info=ax1_yscale_info,
                          labelPrefix=cold_labelPrefix,type_label=type_label,
                          plot_mVuA=plot_unpumpmVuA, plot_mVtp=plot_unpumpmVtp, plot_mVpot=plot_unpumpmVpot,
                          find_lin_mVuA=coldunpumped_find_lin_mVuA,
                          mVuA_color=coldunpump_mVuA_color, mVtp_color=coldunpump_mVtp_color,
                          mVpot_color=coldunpump_mVpot_color, find_lin_color=lin_color,
                          mVuA_ls=coldunpump_mVuA_ls, mVtp_ls=coldunpump_mVtp_ls,
                          mVpot_ls=coldunpump_mVpot_ls, find_lin_ls=lin_ls,
                          mVuA_linw=coldunpump_mVuA_linw, mVtp_linw=coldunpump_mVtp_linw,
                          mVpot_linw=coldunpump_mVpot_linw, find_lin_linw=lin_linw,
                          linif=linif,
                          der1_int=der1_int, do_der1_conv=do_der1_conv,
                          der1_min_cdf=der1_min_cdf, der1_sigma=der1_sigma,
                          der2_int=der2_int, do_der2_conv=do_der2_conv,
                          der2_min_cdf=der2_min_cdf, der2_sigma=der2_sigma,
                          verbose=verbose)

    ############################
    ###### Parameter Data ######
    ############################

    ### Get the Processed Parameters of the Sweep
    paramsfile_list = []
    paramsfile_list.append(proYdatadir + 'hotproparams.csv')
    paramsfile_list.append(proYdatadir + 'coldproparams.csv')
    K_val, magisweep, magiset, magpot, meanmag_V, stdmag_V, meanmag_mA, stdmag_mA, LOuAsearch, LOuAset, UCA_volt,\
    LOuA_set_pot, LOuA_magpot,meanSIS_mV, stdSIS_mV, meanSIS_uA, stdSIS_uA, meanSIS_tp, stdSIS_tp, SIS_pot, \
    del_time, LOfreq, IFband, meas_num, TP_int_time, TP_num, TP_freq, mag_chan \
        = getmultiParams(paramsfile_list)


    #############################################
    ###### Analyze the scaling information ######
    #############################################

    # Unify xscale string list then compress mins and maxes to a list that size.
    # Axis X scaling
    xscale_str = ax1_scaling[0]
    xscale_maxmin = finddatalims(xscale_info)

    if mV_min is None:
        for xscale_type in xscale_maxmin:
            type_str = xscale_type[0]
            if xscale_str == type_str:
                xlimL = xscale_type[1]
    else:
        xlimL = mV_min
    if mV_max is None:
        for xscale_type in xscale_maxmin:
            type_str = xscale_type[0]
            if xscale_str == type_str:
                xlimR = xscale_type[2]
    else:
        xlimR = mV_max

    xscales = determine_scales(xscale_str, xscale_maxmin)
    # Y Axis 1 scaling
    ax1_yscale_str    = ax1_scaling[1]
    ax1_yscale_maxmin = finddatalims(ax1_yscale_info)
    ax1_yscales       = determine_scales(ax1_yscale_str, ax1_yscale_maxmin)
    ylimL1, ylimR1    = findscalemaxmin(ax1_yscale_str,ax1_yscale_maxmin)

    # Y Axis 2 scaling
    ax2_yscale_str    = ax2_scaling[1]
    ax2_yscale_maxmin = finddatalims(ax2_yscale_info)
    ax2_yscales       = determine_scales(ax2_yscale_str, ax2_yscale_maxmin)
    ylimL2, ylimR2    = findscalemaxmin(ax2_yscale_str,ax2_yscale_maxmin)

    #####################################
    ###### Plot the Collected Data ######
    #####################################
    plt.clf()

    if do_xkcd:
        plt.xkcd(scale=1, length=100,randomness=2)

    ##############
    ### AXIS 1 ###
    ##############
    fig, ax1 = plt.subplots()
    if (ax1_plot_list != []):
        for plot_obj in ax1_plot_list:
            (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
            scale_factor = findscaling(scale_str,ax1_yscales)
            scale_x_vector = numpy.array(x_vector)
            scale_y_vector = numpy.array(y_vector)*scale_factor
            if verbose:
                print 'ax1', scale_str, scale_factor, color, linw, ls, numpy.shape(scale_x_vector), numpy.shape(scale_y_vector)
            ax1.plot(scale_x_vector, scale_y_vector, color=color, linewidth=linw, ls=ls)

        for plot_obj in raw_plot_list:
            (x_vector, y_vector, x_error, y_error, color, linw, fmt, markersize, alpha, capsize, scale_str) = plot_obj
            scale_factor = findscaling(scale_str,ax1_yscales)
            scale_x_vector = numpy.array(x_vector)
            scale_y_vector = numpy.array(y_vector)*scale_factor
            if verbose:
                print 'raw_ax1', scale_str, scale_factor, color, linw, fmt, numpy.shape(scale_x_vector), numpy.shape(scale_y_vector)
            ax1.plot(scale_x_vector, scale_y_vector, linestyle='None',color=color,
                     marker=fmt, markersize=markersize, markerfacecolor=color, alpha=alpha)
            ax1.errorbar(scale_x_vector, scale_y_vector, xerr=x_error, yerr=y_error,
                         marker='|',color=color, capsize=capsize, linestyle='None', elinewidth=linw)

            #ax1.plot(scale_x_vector, scale_y_vector, color='DarkSalmon', marker='o', linewidth=linw)
            #ax1.plot(scale_x_vector, scale_y_vector, xerr=x_error, fmt=fmt, linewidth=linw)
        ### Axis Labels ###
        ax1.set_xlabel(ax1_xlabel)
        ax1.set_ylabel(ax1_ylabel)
        ### Axis Limits
        if str(ax1_scaling[1]) == 'tp':
            ylimL1 = min(0,ylimL1)

        xsize = abs(xlimL-xlimR)
        y1size = abs(ylimL1-ylimR1)

    ##############
    ### AXIS 2 ###
    ##############
    ax2 = ax1.twinx()
    if (ax2_plot_list != []):
        for plot_obj in ax2_plot_list:
            (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
            scale_factor = findscaling(scale_str,ax2_yscales)
            scale_x_vector = numpy.array(x_vector)
            scale_y_vector = numpy.array(y_vector)*scale_factor
            if verbose:
                print 'ax2', scale_str, scale_factor, color, linw, ls, numpy.shape(x_vector), numpy.shape(y_vector)

            ax2.plot(scale_x_vector, scale_y_vector, color=color, linewidth=linw, ls=ls)
        #for tl in ax2.get_yticklabels():
        #    tl.set_color(Yfactor_color)

        if ax2_scaling[1] == 'Yf':
            ### Axis Labels ###
            ax2.set_ylabel(ax2_ylabel, color=Yfactor_color)
            ### Axis Limits
            ylimL2 = 0
        else:
            ### Axis Labels ###
            ax2.set_ylabel(ax2_ylabel)
        y2size = abs(ylimR2-ylimL2)


        ### Axis Limits
        if str(ax1_scaling[1]) == 'tp':
            ax1_ylim0 = 0-y1size*y_margin_bot
        else:
            ax1_ylim0 = ylimL1-y1size*y_margin_bot
        ax1_ylim1 = ylimR1+y1size*y_margin_top

        ax1_xlim0 = xlimL-xsize*x_margin_left
        ax1_xlim1 = xlimR+xsize*x_margin_right

        ax2_ylim0 = ylimL2-y2size*y_margin_bot
        ax2_ylim1 = ylimR2+y2size*y_margin_top


        ax1.set_xlim([ax1_xlim0, ax1_xlim1])
        ax1.set_ylim([ax1_ylim0, ax1_ylim1])
        ax2.set_ylim([ax2_ylim0, ax2_ylim1])

    ###############################################
    ###### Things to Make the Plot Look Good ######
    ###############################################

    ### Legend ###
    final_leglines  = []
    final_leglabels = []
    for indexer in range(len(leglines)):
        if ((leglines[indexer] != None) and (leglabels[indexer] != None)):
            final_leglabels.append(leglabels[indexer])
            legline_data = leglines[indexer]
            color = legline_data[0]
            ls    = legline_data[1]
            linw  = legline_data[2]
            final_leglines.append(plt.Line2D(range(10), range(10), color=color, ls=ls, linewidth=linw))
    matplotlib.rcParams['legend.fontsize'] = legendsize
    plt.legend(tuple(final_leglines),tuple(final_leglabels), numpoints=1, loc=legendloc)


    ######################################################
    ###### Put Sweep ParameterS on the Plot as Text ######
    ######################################################
    if display_params:
        ################
        ### Column 1 ###
        ################
        xpos = xlimL + (4.0/18.0)*xsize
        yincrement = (y2size*(1+(y_margin_top+y_margin_bot)))/25.0
        if ax2_plot_list != []:
            ypos = ylimR2+y_margin_top*y2size - yincrement
        else:
            ypos = ylimR1+y_margin_top*y1size  - yincrement
        if K_val is not None:
            K_val_str = Params_2_str(K_val, '%3.0f')
            plt.text(xpos, ypos, K_val_str + " K", color = K_val_color)
            ypos -= yincrement
        if LOuAset is not None:
            LOuAset_str = Params_2_str(LOuAset, '%2.3f')
            plt.text(xpos, ypos, LOuAset_str + " uA LO", color = LOpwr_color)
            ypos -= yincrement
        if UCA_volt is not None:
            UCA_volt_str = Params_2_str(UCA_volt, '%1.5f')
            plt.text(xpos, ypos, UCA_volt_str + " V  UCA", color = LOpwr_color)
            ypos -= yincrement
        if meanSIS_mV is not None:
            meanSIS_mV_str = Params_2_str(meanSIS_mV, '%2.3f')
            if stdSIS_mV is not None:
                stdSIS_mV_str = Params_2_str(stdSIS_mV, '%2.2f', 'round')
                plt.text(xpos, ypos, meanSIS_mV_str + " " + stdSIS_mV_str + " mV", color = LOpwr_color)
            else:
                plt.text(xpos, ypos, str('%1.3f' % meanSIS_mV) + " mV", color = LOpwr_color)
            ypos -= yincrement
        if meanSIS_uA is not None:
            meanSIS_uA_str = Params_2_str(meanSIS_uA, '%2.2f')
            if stdSIS_uA is not None:
                stdSIS_uA_str = Params_2_str(stdSIS_uA, '%2.2f', 'round')
                plt.text(xpos, ypos, meanSIS_uA_str + " " + stdSIS_uA_str+ " uA", color = LOpwr_color)
            else:
                plt.text(xpos, ypos, str('%2.2f' % meanSIS_uA) + " uA", color = LOpwr_color)
            ypos -= yincrement
        if LOuA_set_pot is not None:
            LOuA_set_pot_str = Params_2_str(LOuA_set_pot, '%06.f')
            plt.text(xpos, ypos, "@" + LOuA_set_pot_str + " SIS bias pot", color = LOpwr_color)
            ypos -= yincrement
        if LOuA_magpot is not None:
            LOuA_magpot_str = Params_2_str(LOuA_magpot, '%06f')
            plt.text(xpos, ypos, "@" + LOuA_magpot_str + "  Magnet pot", color = LOpwr_color)
            ypos -= yincrement
        if ((Ysweep.Ydatafound) and (plot_Yfactor)):
            Yfactor_max_str = Params_2_str(Ysweep.Yfactor_max, '%1.2f')
            mV_Yfactor_max_str = Params_2_str(Ysweep.y_mV_max, '%1.2f')
            plt.text(xpos, ypos, 'max Y-factor ' +Yfactor_max_str + ' @ '+mV_Yfactor_max_str+' mV', color = Yfactor_color)
            ypos -= yincrement
            if Y_mV_min is None:
                Y_mV_range_min = min(Ysweep.y_mV)
            else:
                 Y_mV_range_min = Y_mV_min
            if Y_mV_max is None:
                Y_mV_range_max = max(Ysweep.y_mV)
            else:
                 Y_mV_range_max = Y_mV_max
            Y_mV_range_min_str = Params_2_str(Y_mV_range_min, '%1.2f')
            Y_mV_range_max_str = Params_2_str(Y_mV_range_max, '%1.2f')
            plt.text(xpos, ypos, 'in range [' + Y_mV_range_min_str + ',' + Y_mV_range_max_str + '] mV', color = Yfactor_color)
            ax2.plot([Ysweep.y_mV_max, Ysweep.y_mV_max],[ylimL2, ylimR2], color=Yfactor_color)
            ypos -= yincrement


        ################
        ### Column 2 ###
        ################
        xpos = xlimL + (12.0/18.0)*xsize
        if ax2_plot_list != []:
            ypos = ylimR2+y_margin_top*y2size - yincrement
        else:
            ypos = ylimR1+y_margin_top*y1size - yincrement

        if magiset is not None:
            plt.text(xpos, ypos,"magnet set value", color = mag_color)
            ypos -= yincrement
            magiset_str = Params_2_str(magiset, '%2.4f')
            plt.text(xpos, ypos, magiset_str + " mA" , color=mag_color)
            ypos -= yincrement
        if meanmag_mA is not None:
            plt.text(xpos, ypos,"magnet meas value", color = mag_color)
            ypos -= yincrement
            meanmag_mA_str = Params_2_str(meanmag_mA, '%2.4f')
            stdmag_mA_str = Params_2_str(stdmag_mA, '%2.4f', 'round')
            plt.text(xpos, ypos, meanmag_mA_str +  " " + stdmag_mA_str + " mA", color = mag_color)
            ypos -= yincrement
        if magpot is not None:
            magpot_str = Params_2_str(magpot, '%06.f')
            plt.text(xpos, ypos, magpot_str + " mag pot", color = mag_color)
            ypos -= yincrement
        if LOfreq is not None:
            LOfreq_str = Params_2_str(LOfreq, '%3.2f')
            plt.text(xpos, ypos, LOfreq_str + " GHz", color = LOfreq_color)
            ypos -= yincrement
        if IFband is not None:
            IFband_str = Params_2_str(IFband, '%1.3f')
            plt.text(xpos, ypos, IFband_str + " GHz", color = IFband_color)
            ypos -= yincrement
        if TP_int_time is not None:
            TP_int_time_str = Params_2_str(TP_int_time, '%1.3f')
            plt.text(xpos, ypos, TP_int_time_str + " secs", color = TP_int_time_color)
            ypos -= yincrement

    ##################
    ### Save Plots ###
    ##################
    plotdir = Ysweep.fullpath+'plots/'
    Ynum = Ysweep.Ynum

    if save_plot:
        if do_eps:
            filename = local_copy(windir(plotdir+Ynum+".eps"))
            if verbose:
                print "saving EPS file:", filename
            plt.savefig(filename)
        else:
            filename = plotdir+str(Ysweep.LOfreq)+"_LOfreq_"+Ynum+".png"
            if verbose:
                print "saving PNG file:", filename
            plt.savefig(filename)

    ##################
    ### Show Plots ###
    ##################
    if show_plot:
        plt.show()
        plt.draw()
    else:
        plt.close("all")

    if verbose:
        print " "

    plt.close("all")
    return
