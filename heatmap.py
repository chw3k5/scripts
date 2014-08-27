def map4setdata(show_plots, save_plots, saveplotname, grideges4charlen, near_neigh, char_len_x,char_len_y, x, y, z, levels, x_handle, y_handle, plottitle):
    import sys        
    import atpy
    import numpy
    import math
    from operator import itemgetter
    import matplotlib.pyplot as plt
    import pylab
      
    # find x and y min and max
    xmax = numpy.max(x)
    xmin = numpy.min(x)
    xlen = xmax - xmin
    ymax = numpy.max(y)
    ymin = numpy.min(y)
    ylen = ymax - ymin
    
    
    
    # find the number size of the 2D array to cover the x and y space        
    xgridlen = numpy.array(round(grideges4charlen*((xlen)/char_len_x))+1)
    ygridlen = numpy.array(round(grideges4charlen*((ylen)/char_len_y))+1)
    xgridlen.astype(int)
    ygridlen.astype(int)
    
    xpoints = numpy.arange(xmin, xmax+0.1*xlen/xgridlen, xlen/(xgridlen-1))
    ypoints = numpy.arange(ymin, ymax+0.1*ylen/ygridlen, ylen/(ygridlen-1))
    
    #grid_total = xgridlen*ygridlen
    #print str('%4.0f' % grid_total)+" is the number of grid points"
    
    # map data to the grid
    xtemp = (x - xmin)*(xgridlen)/xlen
    ytemp = (y - ymin)*(ygridlen)/ylen
    
    z_grid = numpy.zeros((xgridlen,ygridlen))
    
    for m in range(xgridlen):
    #for m in range(1):
        print 'doing step ' + str(m+1) + ' of ' + str(xgridlen)
        xshift = xtemp - m
        for n in range(ygridlen):
        #for n in range(2):
            yshift = ytemp - n
            R = (xshift**2) + (yshift**2)
            data = numpy.zeros((len(R),2))
            data[:,0] = R
            data[:,1] = z
            sort_data = numpy.asarray(sorted(data, key=itemgetter(0)))
            if sort_data[0,0] == 0:
                finished = False
                count    = 0
                summer   = sort_data[0,1]
                while not finished:
                    count = count + 1
                    if sort_data[count, 0] == 0:
                        summer = summer + data[count, 1]
                    else:
                        finished = True
                z_grid[m,n]=summer/count
            else:
                if not near_neigh:
                    scale_factor = (1/(sort_data[:,0]**2))
                    norm_factor  = sum(scale_factor)
                    z_grid[m,n]  = numpy.dot((scale_factor/norm_factor),sort_data[:,1])
                else:
                    scale_factor = (1/(sort_data[0:near_neigh,0]**2))
                    norm_factor  = sum(scale_factor)
                    z_grid[m,n]  = numpy.dot((scale_factor/norm_factor),sort_data[0:near_neigh,1])
                    
            if math.isnan(z_grid[m,n]):
                print 'i got a NaN value, something when wrong'
                sys.exit()
    
    plt.clf()
    #pylab.title(plottitle)

    plt.contourf(xpoints,ypoints,numpy.transpose(z_grid), levels=levels, cmap=plt.cm.jet)
    plt.colorbar()
    
    pylab.xlabel(x_handle)
    pylab.ylabel(y_handle)
    
    if show_plots:
        plt.draw()
        plt.show()
        
    if save_plots:
        pylab.savefig(saveplotname)
    #print "the heapmap script has reached the end"
    return 