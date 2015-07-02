__author__ = 'chwheele'
import numpy, random
from profunc import merge_dicts

def randRagneArray(arrayLen):
    list2shuffle=range(arrayLen)
    random.shuffle(list2shuffle)
    randArray=numpy.array(list2shuffle)
    return randArray

def differentialEvolution(parentPop,rangeList,crossOverProb=0.5,strategy=1,F=0.8):
    mutantPopMatrix = None
    mutantPop = None
    popNum = len(parentPop)
    parameterNum = len(rangeList)



    # convert the parent population list to matrix form
    parameterKeys = rangeList.keys()
    popMatrix=numpy.zeros((popNum,parameterNum))
    for (popIndex,popMember) in list(enumerate(parentPop)):
        for (paramIndex,parameter) in list(enumerate(parameterKeys)):
            try:
                popMatrix[popIndex,paramIndex]=popMember[parameter]
            except:
                singleTonList=popMember[parameter]
                popMatrix[popIndex,paramIndex]=singleTonList[0]

    # convert the best member (expected to be the first value of parentPop)
    # to a population matrix of only the best member (is is good to be king)
    popOfOnlyBestMember=numpy.zeros((popNum,parameterNum))
    bestMember=parentPop[0]
    for popIndex in range(popNum):
        for (paramIndex,parameter) in list(enumerate(parameterKeys)):
            try:
               popOfOnlyBestMember[popIndex,paramIndex]=bestMember[parameter]
            except:
                singleTonList=bestMember[parameter]
                popOfOnlyBestMember[popIndex,paramIndex]=singleTonList[0]

    parentDictKeys=bestMember.keys()
    # This gets vector math intensive so we will initialize some variables here
    popMemberList1=numpy.zeros((popNum,parameterNum))
    popMemberList2=numpy.zeros((popNum,parameterNum))
    popMemberList3=numpy.zeros((popNum,parameterNum))
    popMemberList4=numpy.zeros((popNum,parameterNum))
    popMemberList5=numpy.zeros((popNum,parameterNum))
    intermediateVectors=numpy.zeros((popNum,parameterNum))
    maskIntermediateVectors=numpy.zeros((popNum,parameterNum))
    maskIntermediateVectors2=numpy.zeros((parameterNum,popNum))
    maskIntermediateVectors3=numpy.zeros((parameterNum,popNum))
    maskIntermediateVectors4=numpy.zeros((popNum,parameterNum))
    mask4oldPop=numpy.zeros((popNum,parameterNum))
    rotatingPopArray=numpy.arange(popNum)
    rotatingParamArray=numpy.arange(parameterNum)
    someOtherRotators = numpy.zeros(popNum)
    rotatingArray4ExponentialCrossover=numpy.zeros(parameterNum)
    indexArray1=numpy.zeros(popNum)
    indexArray2=numpy.zeros(popNum)
    indexArray3=numpy.zeros(popNum)
    indexArray4=numpy.zeros(popNum)
    indexArray5=numpy.zeros(popNum)
    indexPointerArray=numpy.zeros(4)

    iterationNum=1

    # This is where Trevor's loop starts

    # make some arrays to shuffle the population matrix around,
    # these shuffled arrays switch around the 'breeding partners'
    # for the members of population matrix
    indexPointerArray=randRagneArray(4)
    indexArray1=randRagneArray(popNum)
    someOtherRotators = numpy.mod(rotatingPopArray+indexPointerArray[0],popNum)
    indexArray2=indexArray1[someOtherRotators]
    someOtherRotators = numpy.mod(rotatingPopArray+indexPointerArray[1],popNum)
    indexArray3=indexArray2[someOtherRotators]
    someOtherRotators = numpy.mod(rotatingPopArray+indexPointerArray[2],popNum)
    indexArray4=indexArray3[someOtherRotators]
    someOtherRotators = numpy.mod(rotatingPopArray+indexPointerArray[3],popNum)
    indexArray5=indexArray4[someOtherRotators]

    popMemberList1=popMatrix[indexArray1,:]
    popMemberList2=popMatrix[indexArray2,:]
    popMemberList3=popMatrix[indexArray3,:]
    popMemberList4=popMatrix[indexArray4,:]
    popMemberList5=popMatrix[indexArray5,:]

    # Now we will make the cross over matrix

    maskIntermediateVectors=numpy.random.rand(popNum,parameterNum) < crossOverProb
    maskIntermediateVectors = maskIntermediateVectors.astype(int)

    if (5 < strategy):
        st=strategy-5
    else:
        st=strategy
        maskIntermediateVectors2=numpy.transpose(numpy.sort(maskIntermediateVectors))
        for popIndex in range(popNum):
            randInt=random.randrange(parameterNum)
            if 0 < randInt:
                rotatingArray4ExponentialCrossover = numpy.mod(rotatingParamArray+randInt,parameterNum)
                maskIntermediateVectors3[:,popIndex]\
                    = maskIntermediateVectors2[rotatingArray4ExponentialCrossover,popIndex]
        maskIntermediateVectors4 = numpy.transpose(maskIntermediateVectors3)
        maskIntermediateVectors=maskIntermediateVectors4

    # this makes the inverse mask to maskIntermediateVector
    mask4oldPop = maskIntermediateVectors < 0.5
    mask4oldPop = mask4oldPop.astype(int)

    if (st == 1):                  # DE/best/1
        mutantPopMatrix = popOfOnlyBestMember + F*(popMemberList1 - popMemberList2) # differential variation
        mutantPopMatrix = popMatrix*mask4oldPop + mutantPopMatrix*maskIntermediateVectors # crossover
    elif (st == 2):                  # DE/rand/1
        mutantPopMatrix = popMemberList3 + F*(popMemberList1 - popMemberList2) # differential variation
        mutantPopMatrix = popMatrix*mask4oldPop + mutantPopMatrix*maskIntermediateVectors # crossover
    elif (st == 3):                  # DE/rand-to-best/1
        mutantPopMatrix = popMatrix + F*(popOfOnlyBestMember-popMatrix) + F*(popMemberList1 - popMemberList2)
        mutantPopMatrix = popMatrix*mask4oldPop + mutantPopMatrix*maskIntermediateVectors # crossover
    elif (st == 4):                  # DE/best/2
        mutantPopMatrix = popOfOnlyBestMember + F*(popMemberList1 - popMemberList2 + popMemberList3 - popMemberList4) # differential variation
        mutantPopMatrix = popMatrix*mask4oldPop + mutantPopMatrix*maskIntermediateVectors # crossover
    elif (st == 5):                  # DE/rand/2
        mutantPopMatrix = popMemberList5 + F*(popMemberList1 - popMemberList2 + popMemberList3 - popMemberList4) # differential variation
        mutantPopMatrix = popMatrix*mask4oldPop + mutantPopMatrix*maskIntermediateVectors # crossover

    #
    parameterMinList=[]
    parameterMaxList=[]
    for (paramIndex,parameter) in list(enumerate(parameterKeys)):
        (parameterMin,parameterMax) = rangeList[parameter]
        parameterMinList.append(min([parameterMin,parameterMax]))
        parameterMaxList.append(max([parameterMin,parameterMax]))

    mutantPop = []
    for popIndex in range(popNum):
        popMember = {}
        memberParams=mutantPopMatrix[popIndex,:]
        for (paramIndex,parameter) in list(enumerate(parameterKeys)):
            # make sure the parameters are in the range specified by 'rangeList'
            parameter2test = memberParams[paramIndex]
            parameterMin = parameterMinList[paramIndex]
            parameterMax = parameterMaxList[paramIndex]
            if parameter2test < parameterMin:
                diff = abs(parameter2test < parameterMin)
                parameter2test = parameterMin+1.5*diff
            elif parameterMax < parameter2test:
                diff = abs(parameter2test-parameterMax)
                parameter2test = parameterMax-1.5*diff
            popMember[parameter]= parameter2test
        mutantPop.append(popMember)

    cleanedParentPop=[] # this version of the population has gotten rid of singleton lists
    for popIndex in range(popNum):
        popMember = {}
        memberParams=popMatrix[popIndex,:]
        for (paramIndex,parameter) in list(enumerate(parameterKeys)):
            popMember[parameter]=memberParams[paramIndex]
        cleanedParentPop.append(popMember)

    combinedParentPop = []
    for popIndex in range(popNum):
        oldParentPopMember = parentPop[popIndex]
        cleanedParentPopMember = cleanedParentPop[popIndex]

        combinedParentPop.append(merge_dicts(oldParentPopMember,cleanedParentPopMember))


    return mutantPop, combinedParentPop