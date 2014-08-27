import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import atpy

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

filename = '/Users/chw3k5/Documents/Grad_School/Kappa/NB37/IV/set7/data/set7data.csv'
xpoints=100
ypoints=100

data=atpy.Table(filename, type="ascii", delimiter=",")


#data.start_Yrange
#data.end_Yrange
#data.max_Yfactor
#data.mV_max_Yfactor
#data.min_Yfactor
#data.mV_min_Yfactor
z=np.array(data.mean_Yfactor)
#data.Ynum
#data.LO_val
#data.IFband_val
#data.magpot_pos
x=np.array(data.mag_mA)
y=np.array(data.UCA_val)

data=np.zeros((len(x),2))
data[:,0]=x
data[:,1]=y

#interpol = scipy.interpolate.griddata(data, z, xi, method='linear', fill_value=nan)[source]
#interpol = scipy.interpolate.LinearNDInterpolator(data, z, fill_value=1)

xmin   = min(x)
xmax   = max(x)
ymin   = min(y)
ymax   = max(y)
xspace = (xmax-xmin)/xpoints
yspace = (ymax-ymin)/ypoints

xnew = np.arange(xmin, xmax+xspace, xspace)
ynew = np.arange(ymin, ymax+yspace, yspace)

xmesh, ymesh = np.meshgrid(xnew, ynew)

interpol = scipy.interpolate.griddata(data, z, (xmesh,ymesh), method='linear', fill_value=np.nan)

xdata=np.reshape(xmesh,(xpoints+1)*(ypoints+1))
ydata=np.reshape(ymesh,(xpoints+1)*(ypoints+1))

zdata = interpol(xdata, ydata)
#zdata = np.reshape(interpol (xdata, ydata), (xpoints+1,ypoints+1))



interpol_data = np.zeros((len(zdata),3))
interpol_data[:,0] = xdata
interpol_data[:,1] = ydata
interpol_data[:,2] = zdata

array2D_data=np.reshape(zdata, (xpoints+1,ypoints+1))

array3D_data=np.reshape(interpol_data, (xpoints+1,ypoints+1,3))

plt.clf()

plt.imshow(array2D_data)
plt.gray()
plt.show()

