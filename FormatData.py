import shutil, os, time

def formatRandS_ZVA24(filename,headsize=3):
    with open(filename) as f:
        lines_after_3 = f.readlines()[headsize:]
    temp_filename = 'Delete_Me.csv'
    plfile = open(temp_filename,'w')
    plfile.write("Hz,dB\n")

    for line_num in range(len(lines_after_3)):
        new_line = lines_after_3[line_num].replace(';',',',1)
        new_line = new_line.replace(';','')
        plfile.write(new_line)
    time.sleep(1)
    shutil.copy(temp_filename, filename)
    os.remove(temp_filename)
    return


