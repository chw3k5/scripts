__author__ = 'chwheele'

rangeSet = [0,1,2,3,4,5]
calRanges = [(1,0.001),(2,0.01),(3,0.1),(4,1.0),(5,10)]

def openHailingFrequencies():
    import visa
    global HP437B
    HP437B = visa.instrument("GPIB0::13::INSTR")
    return

def closeHailingFrequencies():
    HP437B.close()
    return

def range2uW(inputRange):
    mWcoeff = None
    for (testRange,testmWcoeff) in calRanges:
        if testRange == inputRange:
            mWcoeff = testmWcoeff

    if mWcoeff is None:
        mWcoeff = 1000
    return mWcoeff

def setRange(rangeNum=0,verbose=False):

    # 0 : Auto range -70dBm to -20dBm
    # 1 : -70dBm - -60 dmB
    # 2 : -60dBm - -50 dmB
    # 3 : -50dBm - -40 dmB
    # 4 : -40dBm - -30 dmB
    # 5 : -30dBm - -20 dmB
    if rangeNum in rangeSet:
        HP437B.write('RM'+str(rangeNum)+'EN')
        if rangeNum == 0:
            if verbose: print "Range of HP437B Power meter set to range 0: Auto range -70dBm to -20dBm"
        elif rangeNum == 1:
            if verbose: print "Range of HP437B Power meter set to range 1: -70dBm to -60 dmB"
        elif rangeNum == 2:
            if verbose: print "Range of HP437B Power meter set to range 1: -60dBm to -50 dmB"
        elif rangeNum == 3:
            if verbose: print "Range of HP437B Power meter set to range 1: -50dBm to -40 dmB"
        elif rangeNum == 4:
            if verbose: print "Range of HP437B Power meter set to range 1: -40dBm to -30 dmB"
        elif rangeNum == 5:
            if verbose: print "Range of HP437B Power meter set to range 1: -30dBm to -20 dmB"
    else:
        HP437B.write('RM0EN')
        print 'your selection of a range of rangeNum=',rangeNum
        print 'is not in the set of acceptable ranges for the HP437B power meter:',rangeSet
        print "Range of HP437B Powermeter set to range 0: Auto range -60dBm to -10dBm"


    return

if __name__ == '__main__':
    openHailingFrequencies()
    setRange(2,verbose=True)
    closeHailingFrequencies()