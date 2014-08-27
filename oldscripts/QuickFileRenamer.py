from renamer import renamer
import glob

dir = '/Users/chw3k5/Documents/Grad_School/Kappa/NA38/IVsweep/set1/'
search_str = '*.csv'

csvfiles = []
for files in glob.glob(dir+search_str):
    csvfiles.append(files)

renamer(csvfiles)