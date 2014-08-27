def find_Ynums(myfiles, verbose): # finds the Y numbers
    # Having more than one 'Y' in the filename will return bad results
    # However, having any number of 'Y's in the directory path is fine
    Ynums=[]
    loop_ebrake=False
    for n in range(len(myfiles)):
        flag=True
        finished1=False
        position=0
        next_position=0
        string=myfiles[n]
        loop_max=1000
        loop_count=0
        
        while not finished1:
            loop_count=loop_count+1
            if loop_count >= loop_max:
                print 'An infinite loop was just stopped in find_Ynums'
                finished1=True
                loop_ebrake=True
                status=False
                  
            next_position=string.find('/',position+1)
            if not next_position == -1:
                position=next_position
            else:
                finished1=True
        string2=string[position+1:]
        
        position2=string2.find('Y')
        end_position=string2.find('_', position2)
        if not Ynums:
            Ynums.append(string2[position2:end_position])
        else:
            for k in range(len(Ynums)):
                if Ynums[k] == string2[position2:end_position]:
                    flag=False
            if flag:
                Ynums.append(string2[position2:end_position])
    if not loop_ebrake:
        status = True
    if not verbose == 'N':
        print "The Y numbers that were found are:"
        print Ynums
    return (Ynums, status)