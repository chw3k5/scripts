from subprocess import call
import glob
start_dir ='/Users/chw3k5/Documents/untitled folder/'
end_dir='/Users/chw3k5/Documents/untitled folder/dump/JPEG/'
search_str='*'
appender='.jpg'


numbers=[]

for n in range(8):

    dir = start_dir+"1024watermarked "+str(n+26)+"/"
    print dir
    filenames=[]
    count=0
    for files in glob.glob(dir+search_str):
       count=count+1
       filenames.append(files)
       print files
       call(["mv", files, end_dir+"watermarked"+str(n+26)+"_"+str(count)+appender])