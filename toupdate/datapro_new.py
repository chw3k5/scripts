import os

# list the derectories where sets of data are found 
setnumbers = [1,2]
rootdir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/'

# get the Y numbers from the directory names in the datadir directory
 
class dataset(object):
    """
    This is the docstring
    """
    def __init__(self, setname):
        self.name = setname
        setdir = rootdir + str(setname) + '/'
        if os.path.isdir(setdir):
            self.setdir = setdir
            rawdir = self.setdir + 'rawdata/'
            if os.path.isdir(rawdir):
                self.rawdir    = rawdir
                self.Yraw_dirs = [dirname for dirname in os.listdir(rawdir) if dirname[0] == 'Y']
            else:
                self.rawdir    = []
                self.Yraw_dirs = []
        else:
            self.setdir = []

        
class rawYdata(dataset):
    def __init__(self, Yname):
        dataset.Yname = Yname
        print Yname

        
set1 = dataset('set1')
rawY = [rawYdata(Ynum) for Ynum in set1.Yraw_dirs]