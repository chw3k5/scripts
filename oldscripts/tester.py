import glob

from renamer import renamer


#csvfile = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set7/LO672_IFband1.420_magpot030000-23.935_UCA3.880_N077K_Y117_0470.csv'




dir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/test/'
search_str = '*.csv'

csvfiles = []
for files in glob.glob(dir+search_str):
    csvfiles.append(files)

renamer(csvfiles)