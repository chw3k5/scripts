def SingleSpectraPlotter(datadir, search_4Snums=False, Snums='', verbose=False, standdev=True,
                    show_plot=False, save_plot=True, do_eps=False):
    import sys
    import os
    import shutil
    import numpy
    from mpl_toolkits.mplot3d import axes3d
    from matplotlib import pyplot as plt
    from matplotlib import cm
    platform = sys.platform
    #if platform == 'darwin':
    #    matplotlib.rc('text', usetex=True)

    # Import this is the directory that has my scripts

    if platform == 'win32':
        func_dir = 'C:\\Users\\MtDewar\\Documents\\Kappa\\scripts'
    elif platform == 'darwin':
        func_dir = '/Users/chw3k5/Documents/Grad_School/Kappa/scripts'
    func_dir_exists=False
    for n in range(len(sys.path)):
        if sys.path[n] == func_dir:
            func_dir_exists=True
    if not func_dir_exists:
        sys.path.append(func_dir)

    from profunc import getproparams,  getproSweep, get_fastIV
    from domath  import linfit

    ##############################
    ###### Start the Script ######
    ##############################
    fastprodata_found         = False
    unpumpedprodatacold_found = False

    if platform == 'win32':
        prodatadir = datadir + 'prodata\\'
        plotdir    = datadir + 'plots\\'
    elif platform == 'darwin':
        prodatadir = datadir + 'prodata/'
        plotdir    = datadir + 'plots/'
    if os.path.isdir(plotdir):
        # remove old processed data
        shutil.rmtree(plotdir)
        # make a folder for new processed data
        os.makedirs(plotdir)
    else:
        # make a folder for new processed data
        os.makedirs(plotdir)

    if search_4Snums:
        # get the Y numbers from the directory names in the datadir directory
        alldirs = []
        for root, dirs, files in os.walk(prodatadir):
            alldirs.append(dirs)
        Snums = alldirs[0]

    for Snum in Snums:

        if verbose:
            print "ploting Spectra for Snum: " + str(Snum)

        if platform == 'win32':
            proSdatadir  = prodatadir + Snum + '\\'
        elif platform == 'darwin':
            proSdatadir  = prodatadir + Snum + '/'

        X_file = proSdatadir + "specdata_freq.npy"
        Y_file = proSdatadir + "specdata_mV.npy"
        Z_file = proSdatadir + "specdata_pwr.npy"

        fig = plt.figure()
        ax = fig.gca(projection='3d')


        X = numpy.load(X_file)
        Y = numpy.load(Y_file)
        Z = numpy.load(Z_file)

        X_max = numpy.max(X)
        Y_max = numpy.max(Y)
        Z_max = numpy.max(Z)

        X_min = numpy.min(X)
        Y_min = numpy.min(Y)
        Z_min = numpy.min(Z)

        X_ran = X_max-X_min
        Y_ran = Y_max-Y_min
        Z_ran = Z_max-Z_min

        offset_scale = 0.1

        X_offset = X_min - X_ran*offset_scale
        Y_offset = Y_max + Y_ran*offset_scale
        Z_offset = Z_min - Z_ran*0.4

        num_of_lines = 20.0

        cs = int(numpy.round(len(X[:,0])/num_of_lines))
        rs = int(numpy.round(len(X[0,:])/num_of_lines))

        ax.plot_surface(X, Y, Z, rstride=rs, cstride=cs, alpha=0.3)
        cset = ax.contour(X, Y, Z, zdir='z', offset=Z_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='x', offset=X_offset, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='y', offset=Y_offset, cmap=cm.coolwarm)


        ax.set_xlabel('IF Frequency (GHz)')
        ax.set_xlim(X_min, X_max)
        ax.set_ylabel('Bias Voltage (mV)')
        ax.set_ylim(Y_min, Y_max)
        ax.set_zlabel('Recieved Power')
        ax.set_zlim(Z_min, Z_max)


        if show_plot:
            #plt.ylabel('Current ($\mu$A)')
            plt.show()
            plt.draw()

        if save_plot:
            if do_eps:
                if verbose:
                    print "saving EPS file"
                plt.savefig(plotdir+Snum+"_spec.eps")
            else:
                if verbose:
                    print "saving PNG file"
                plt.savefig(plotdir+Snum+"_spec.png")

        if verbose:
            print " "
    plt.close("all")

    return

from sys import platform
if platform == 'win32':
    datadir = "C:\\Users\\MtDewar\\Documents\\Kappa\\NA38\\warmmag\\"
elif platform == 'darwin':
    datadir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/warmmag/'
SingleSpectraPlotter(datadir, search_4Snums=True, Snums=['00001'])