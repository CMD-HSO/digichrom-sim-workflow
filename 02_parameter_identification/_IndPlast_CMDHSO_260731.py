import os
import sys
import numpy as np
import time

import DriveModel_CMDHSO_260731 as DriveModel
import PlotResults_CMDHSO_260731 as PlotResults

import scipy.optimize as opt
from scipy.optimize import minimize

import ParameterStructure_CMDHSO_260731 as ParameterStructure

# set working directory to the directory of the script
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)

aParameter = ParameterStructure.sParameterStucture()

# temperature sample points for material properties
aParameter.SamplePnts = [ 20. ]

#                          0           , 1           , 2           , 3           , 4           , 5           , 6           , 7           ,8
aParameter.AllNames   = [[ "E_________", "nue_______", "alpha_____", "Tref______", "Re________", "Qinf______", "b_________", "Cinf1_____", "C1________",]]
aParameter.AllValue   = [[ 210000.0    , 0.3         , 0.          , 20.         ,  300.0      , 100.        , 50.         ,  500.       ,  10000.0    ,]]
# org: aParameter.AllValue   = [[ 210000.0    , 0.3         , 0.          , 20.         ,  400.0      , 300.        , 20.         ,  909.09     ,  50000.0    ,]]

# typical values of the parameters
aParameter.AllTypical = [[ 210000.0    , 0.3         , 0.          , 20.         ,  300.0      , 100.        , 50.         ,  500.       ,  10000.0    ,]]

aParameter.SamplePntsLen = len(aParameter.AllValue)
aParameter.AllLen = len(aParameter.AllValue[:][0])        

# Min and Max values that define the admissible parameter space. The values should be chosen such that they are still sensitive. Then it is possible that the optimizer gets away from the boundary. 
aParameter.AllMin     = [[ 100000.0    , -999999.    , -999999.    , -999999.    , 100.        , 50.         , 10.         , 100.        , 1000.       ,]]
aParameter.AllMax     = [[ 300000.0    , +999999.    , +999999.    , +999999.    , 1000.       , 500.        , 100.        , 1000.       , 100000.     ,]]

iOptimize = 1

# material properties to optimize, only one temperature can be considered
aParameter.OptIndex = [[ 4,5,6,7,8 ]]

if len(aParameter.OptIndex) != len(aParameter.AllValue):
    print("ERROR: len(aParameter.OptIndex) != len(aParameter.AllValue)")
    sys.exit()

print('###   Parameters considered for analysis ')
aParameter.MapMatPropAll2Fit()
aParameter.Print()


#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------


print("###")
print("###")
print("###   =========================================================================")
print("###   ===== read experimental data")
print("###   =========================================================================")
print("###")

sDataDir = "./"
sWorkDir = "./"

aExperimentInfos = [
#     name of data          , weight, control, type  
    [ "data_indent"     , 1.    , "disp" , "ind" ],
]

aTimeAll    = []
aMeasExpAll = []
aMeasSimAll = []
aCntrExpAll = []
aTempExpAll = []

for iExperiment in range(len(aExperimentInfos)):

    sInputFile  = sDataDir + aExperimentInfos[iExperiment][0] + ".txt"

    print("###   Experiment: " + aExperimentInfos[iExperiment][0], ", sInputFile: " + sInputFile)

    aData = np.genfromtxt(sInputFile, usecols=[0,1,2,3], comments="#")

    aTimeAll.append(aData[:,0])
    aMeasExpAll.append(aData[:,1])
    aCntrExpAll.append(aData[:,2])
    aTempExpAll.append(aData[:,3])

    
#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------


print("###")
print("###")
print("###   =========================================================================")
print("###   ===== calculate model")
print("###   =========================================================================")
print("###")

iprint = 1
aParameter.Print()
nFuncValue = DriveModel.CalcModelAll(aParameter, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint)
PlotResults.plotResults(aExperimentInfos,"0")
iprint = 0


#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------


if iOptimize == 1:

    print("###")
    print("###")
    print("###   =========================================================================")
    print("###   ===== optimize material proproperties")
    print("###   =========================================================================")
    print("###")

    aParameterNew = aParameter.CopyParameterStructure()

    start_time = time.perf_counter()

    print("###")
    print("###")
    print("###   =========================================================================")
    print("###   ===== scipy SQP gradient based")
    print("###")

    import scipy as sp

    # the wrapper function uses the parameter vector instead of the parameter class and can be used in conjunction with optimizers of python libraries
    def Wrapper(aOptValue, aParameter, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint):

        for i in range(len(aOptValue)):
            aParameter.OptValue[i] = aOptValue[i]*aParameter.OptTypical[i]
    
        print("### aOptValue =    [", end="")
        for iParameter in range(aParameter.OptLen):
            print("%.5e ," % (aParameter.OptValue[iParameter]), end="")
        print("]"   ),
    
        nFuncValueSQP = DriveModel.CalcModelAll(aParameter, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint)

        print("### nFuncValueSQP", nFuncValueSQP)

        return nFuncValueSQP

    # arguments for function Wrapper
    oArgs = (aParameterNew, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint)

    # upper and lower bounds stored as tuples
    aBounds = []
    for i in range(len(aParameter.OptIndex[0][:])):
        aBounds.append( (aParameter.OptMin[i]/aParameterNew.OptTypical[i], aParameter.OptMax[i]/aParameterNew.OptTypical[i]), )

    aParameterOptValue = np.zeros(len(aParameterNew.OptValue))
    for i in range(len(aParameterOptValue)):
        aParameterOptValue[i] = aParameterNew.OptValue[i]/aParameterNew.OptTypical[i]

    # step size for computation of numerical derivatives with finite differences
    nStepSizeNumDerivative = 1.e-02 # result_0.01.txt
    nStepSizeNumDerivative = 1.e-03 # result_0.001.txt
    nStepSizeNumDerivative = 1.e-04
        
    # call SQP optimization algorithm using the wrapper of least square function with the constaint on Re and Qinf defined in function ieqConstraints
    aOptValue = opt.fmin_slsqp(Wrapper, aParameterOptValue, eqcons=(), f_eqcons=None, ieqcons=(), f_ieqcons=None, bounds=aBounds, fprime=None, fprime_eqcons=None, fprime_ieqcons=None, args=oArgs, iter=100, acc=1e-06, iprint=2, disp=None, full_output=0, epsilon=nStepSizeNumDerivative)

    aParameterNewSQP = aParameterNew.CopyParameterStructure()
    for i in range(len(aOptValue)):
        aParameterNewSQP.OptValue[i] = aOptValue[i]*aParameterNew.OptTypical[i]

    aParameterNewSQP.MapMatPropFit2All()
    aParameterNewSQP.Print()

    # compute least square sum
    iprint = 1
    nFuncValueNewSQP = DriveModel.CalcModelAll(aParameterNewSQP, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint)
    PlotResults.plotResults(aExperimentInfos,"SQP")
    iprint = 0

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("elapsed time:", elapsed_time)

