__author__ = 'chwheele'

"""
This is program created by Caleb Wheeler and Trevor Toland to help with the searching of the parameter space of THz
test receivers. This program is the top level of control code that took 2 years to develop. The idea is that his code
will save a graduate student (or other unsavory worker) from some of the effort needed in making decisions about how
to search the parameter spaces of test receivers. The program is named Alice after Alice in Wonderland. Alice's dream
is to be the greatest graduate student of all time.
"""

### map your parameter and watch them dance around the parameters plane


import numpy, random
rangeList=[(0,1),(-1,1)]
dimSize = len(rangeList) # number of dimensions

popNumber = 10*dimSize # active breeding population
iterMax = 1000 # maximu iterations
F = 0.5 # DE step size [0,2]
CR = 0.7 #  crossover probabililty  [0, 1]
VTR = 1.e-6 # VTR		"Value To Reach" (stop when ofunc < VTR)

population=numpy.zeros((popNumber,dimSize))
for dimIndex in range(dimSize):
    (dimMax,dimMin)=rangeList[dimIndex]
    for popIndex in range(popNumber):
        population[popIndex,dimIndex]=(random.random()*abs(dimMin-dimMax))+min([dimMin,dimMax])

print population