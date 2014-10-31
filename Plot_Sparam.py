import atpy, os, shutil, time, matplotlib
from matplotlib import pyplot as plt


def formatRandS_ZVA24(filename,headsize=3):
    with open(filename) as f:
        lines_after_3 = f.readlines()[headsize:]
    temp_filename = 'Delete_Me.csv'
    plfile = open(temp_filename,'w')
    plfile.write("Hz, dB \n")

    for line_num in range(len(lines_after_3)):
        new_line = lines_after_3[line_num].replace(';',',',1)
        new_line = new_line.replace(';','')
        plfile.write(new_line)
    time.sleep(1)
    shutil.copy(temp_filename, filename)
    os.remove(temp_filename)
    return


def xyplotgen(x_vector, y_vector, label='', plot_list=[], leglines=[], leglabels=[], color='black', linw=1, ls='-', scale_str='' ):
    plot_list.append((x_vector, y_vector, color, linw, ls, scale_str))
    leglines.append((color,ls,linw))
    leglabels.append(label)
    return plot_list, leglines, leglabels

class Sparamdata():
    def __init__(self,fullpath,keys,params,name):
        self.filenameprefix = fullpath+name
        params = list(params)
        for param_index in range(len(params)):
            test_key = keys[param_index]
            parameter = params[param_index]
            # set any default here
            self.color = 'black'

            if test_key == 'name':
                self.name = parameter
            elif test_key == 'mA':
                self.mA = parameter
            elif test_key == 'mA1':
                self.mA1 = parameter
            elif test_key == 'mA2':
                self.mA2 = parameter
            elif test_key == 'V':
                self.V = parameter
            elif test_key == 'V1':
                self.V1 = parameter
            elif test_key == 'V2':
                self.V2 = parameter
            elif test_key == 'source':
                self.source = parameter
            elif test_key == 'power':
                self.power = parameter
            elif test_key == 'temp':
                self.temp = parameter
            elif test_key == 'color':
                self.color = parameter
        return
    def getS11(self):
        S11_file = self.filenameprefix+'S11.csv'
        if os.path.exists(S11_file):
            S11_data = atpy.Table(S11_file, type="ascii", delimiter=",")
            if len(S11_data.keys()) == 1:
                formatRandS_ZVA24(S11_file)
                S11_data = atpy.Table(S11_file, type="ascii", delimiter=",")
            self.S11 = (S11_data.Hz, S11_data.dB)
        else:
            self.S11 = None
        return
    def getS12(self):
        S12_file = self.filenameprefix+'S12.csv'
        if os.path.exists(S12_file):
            S12_data = atpy.Table(S12_file, type="ascii", delimiter=",")
            if len(S12_data.keys()) == 1:
                formatRandS_ZVA24(S12_file)
                S12_data = atpy.Table(S12_file, type="ascii", delimiter=",")
            self.S12 = (S12_data.Hz, S12_data.dB)
        else:
            self.S21 = None
        return
    def getS21(self):
        S21_file = self.filenameprefix+'S21.csv'
        self.S21_file = S21_file
        if os.path.exists(S21_file):
            S21_data = atpy.Table(S21_file, type="ascii", delimiter=",")
            if len(S21_data.keys()) == 1:
                formatRandS_ZVA24(S21_file)
                S21_data = atpy.Table(S21_file, type="ascii", delimiter=",")
            self.S21 = (S21_data.Hz, S21_data.dB)
        else:
            self.S21 = None
            print "I can't find file", S21_file
        return
    def getS22(self):
        S22_file = self.filenameprefix+'S22.csv'
        if os.path.exists(S22_file):
            S22_data = atpy.Table(S22_file, type="ascii", delimiter=",")
            if len(S22_data.keys()) == 1:
                formatRandS_ZVA24(S22_file)
                S22_data = atpy.Table(S22_file, type="ascii", delimiter=",")
            self.S22 = (S22_data.Hz, S22_data.dB)
        else:
            self.S22 = None
        return



plot_S11 = False
plot_S12 = False
plot_S21 = True
plot_S22 = False


save_plot  = True
do_eps     = True
show_plots = False

legendsize = 9
legendloc  = 4

parentdir  = '/Users/chw3k5/Documents/Grad_School/Kappa/Sprarm/'
Sparamdirs = ['Single_Pix_IF/Oct30_14/', 'WBA25/Dec_9_13/14K/data/']

fullpaths = []
Sparams   = []

for Sparamdir in Sparamdirs[:]:
    # print Sparamdir
    fullpath = parentdir + Sparamdir
    paramsfile = fullpath + 'params.csv'
    if os.path.exists(paramsfile):
        params = atpy.Table(paramsfile, type="ascii", delimiter=",")
        keys   = params.keys()
    else:
        keys = []

    if keys == []:
        param_row = []
        name = ''
        Sparamdata(fullpath, keys, param_row, name)
    else:
        for Sparam_num in range(len(params)):
            # print Sparam_num
            param_row = params.row(Sparam_num)
            if 'name' in keys:
                temp = params['name']
                name = str(temp[Sparam_num]) + '_'
            else:
                name = ''
            the_sparams = Sparamdata(fullpath, keys, param_row, name)
            Sparams.append(the_sparams)



if plot_S11:
    for Sparam in Sparams:
        Sparam.getS11()
if plot_S12:
    for Sparam in Sparams:
        Sparam.getS12()

# print len(Sparams)

if plot_S21:
    plot_list = []
    leglines  = []
    leglabels = []
    for Sparam in Sparams:
        Sparam.getS21()
        print Sparam.S21_file
        S_label = ''
        try:
            S_label += str(Sparam.mA) + ' mA @ ' + str(Sparam.V) + ' V '
        except AttributeError:
            S_label += str(Sparam.mA1) + ' mA @ ' + str(Sparam.V1) + ' V, ' + str(Sparam.mA2) + ' mA @ ' + str(Sparam.V2) + ' V '
        try:
            S_label += str(Sparam.power) + ' '
        except AttributeError:
            pass
        try:
            S_label += str(Sparam.temp) + ' K '
        except AttributeError:
            pass
        if Sparam.S21 is not None:
            plot_list, leglines, leglabels \
                = xyplotgen(Sparam.S21[0]/(10.**9), Sparam.S21[1], label=S_label,
                            plot_list=plot_list, leglines=leglines, leglabels=leglabels,
                            color=Sparam.color, linw=2, ls='-', scale_str='' )

    # print len(plot_list)
    for plot_obj in plot_list:
        (x_vector, y_vector, color, linw, ls, scale_str) = plot_obj
        plt.plot(x_vector, y_vector, color=color, linewidth=linw, ls=ls)

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

    plt.xlabel('GHz')
    plt.ylabel('dBm')
    if show_plots:
        plt.draw()
        plt.show()

    if save_plot:
        plotdir = parentdir + 'plots/'
        if not os.path.exists(plotdir):
            os.mkdir(plotdir)
        if do_eps:
            plotname = plotdir + "S21.eps"
            print "saving EPS file:", plotname
        else:
            plotname = plotdir + "S21.png"
            print "saving PNG file: ", plotname
        plt.savefig(plotname)

if plot_S22:
    for Sparam in Sparams:
        Sparam.getS22()


