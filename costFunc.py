__author__ = 'chwheele'


from profunc import windir, local_copy, merge_dicts
from datapro import raw2Yfactor, ParamsProcessing
import numpy, os, atpy

def readCostFile(costFilename):
    with open(costFilename) as f:
        costData = f.readlines()
    costDict = {}
    for singleLine in costData:
        (function,value)=singleLine.split(',')
        value = value.replace('\n','')
        costDict[function]=value
    return costDict

def writeCostFile(costDict,file2write):
    h = open(file2write, 'w')
    for key in costDict.keys():
        h.write(key+','+str(costDict[key])+'\n')
    h.close()
    return
def generateFilenames(dataDir,Ynum):
    try:Ynum_str = 'Y'+str('%04.f' % float(Ynum))
    except:Ynum_str = Ynum
    localdir=local_copy(dataDir)
    proYdir = windir(localdir+'prodata/'+Ynum_str+'/')
    if not os.path.exists(proYdir):os.makedirs(proYdir)
    coldRawDir = windir(dataDir+'rawdata/'+Ynum_str+'/cold/')
    hotRawDir = windir(dataDir+'rawdata/'+Ynum_str+'/hot/')
    return hotRawDir, coldRawDir, proYdir


def cost4Y(popMember,datadir,Y2get=1.8,verbose=False):
    costY_str = 'costY'
    Ynum = popMember['Ynum']

    # read and write the Y factor data
    hotdir, colddir, prodata_Ydir = generateFilenames(datadir,Ynum)
    if verbose:
        print "doing Y factor calculation"
    Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror\
            =raw2Yfactor(coldDir=colddir,hotDir=hotdir,verbose=verbose)
    Yfile = open(prodata_Ydir + 'Ydata.csv', 'w')
    Yfile.write('Yfactor,yerror,y_pot,y_mV,y_mVerror,y_uA,y_uAerror,y_TP,y_TPerror\n')
    for yindex in range(len(Yfactor)):
        Yfile.write(str(Yfactor[yindex])+','+str(yerror[yindex])+','+str(y_pot[yindex])\
                    +','+str(y_mV[yindex])+','+str(y_mVerror[yindex])+','+\
                    str(y_uA[yindex])+','+str(y_uAerror[yindex])+','+str(y_TP[yindex])\
                    +','+str(y_TPerror[yindex])+'\n')
    Yfile.close()

    # here is the actual cost function
    diff = Y2get-numpy.max(numpy.array(Yfactor))
    if diff < 0:
        foundYcost = 0
    else:
        foundYcost=diff**2

    # read ans write the processed parameters files
    coldParamsFile = prodata_Ydir+'coldproparams.csv'
    if not os.path.isfile(coldParamsFile):ParamsProcessing(dirname=colddir, proparamsfile=coldParamsFile, verbose=verbose)
    hotParamsFile = prodata_Ydir+'hotproparams.csv'
    if not os.path.isfile(hotParamsFile):ParamsProcessing(dirname=hotdir, proparamsfile=hotParamsFile, verbose=verbose)
    costFile = prodata_Ydir+'costFunctionResults.csv'
    readCostFile(hotParamsFile)

    # write the cost files or append to the cost file
    if os.path.isfile(costFile):
        costDict = readCostFile(costFile)
    else:
        costDict = {costY_str:foundYcost}
    writeCostFile(costDict,costFile)

    popMember = merge_dicts(popMember,costDict)

    return popMember


