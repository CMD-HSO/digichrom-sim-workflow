import sys
import math
import numpy as np
import random

import Interpolate_CMDHSO_260731 as Interpolate

class sParameterStucture:
    def __init__(self):
        self.SamplePnts   = 0
        self.AllNames     = 0
        self.AllValue     = 0
        self.AllLen       = 0
        self.AllMin       = 0
        self.AllMax       = 0
        self.AllTypical   = 0
        self.AtSamplePnt  = 0
        self.DerivWrtTemp = 0
        self.OptIndex     = 0
        self.OptNames     = 0
        self.OptValue     = 0
        self.OptLen       = 0
        self.OptMin       = 0
        self.OptMax       = 0
        self.OptTypical   = 0



    def MapMatPropFit2All(self):

        # mapping of the material properties of aMatPropAll to aMatPropFit
        # loop over number of temperatures
        for i in range(len(self.AllValue)):
            # loop over all properties
            for j in range(len(self.AllValue[:][0])):
                # loop over all properties to fit
                for k in range(len(self.OptIndex[:][0])):

                    if j == self.OptIndex[i][k]:
                        self.AllValue[i][j] = self.OptValue[i*len(self.OptIndex[:][0])+k]



    def MapMatPropAll2Fit(self):
 
        self.OptNames   = []
        self.OptValue   = np.zeros( len(self.OptIndex)*len(self.OptIndex[:][0]) )
        self.OptMin     = np.zeros( len(self.OptIndex)*len(self.OptIndex[:][0]) )
        self.OptMax     = np.zeros( len(self.OptIndex)*len(self.OptIndex[:][0]) )
        self.OptTypical = np.zeros( len(self.OptIndex)*len(self.OptIndex[:][0]) )

        self.OptLen = len(self.OptValue)

        # mapping of the material properties of aMatPropAll to aMatPropFit
        # loop over number of temperatures
        for i in range(len(self.AllValue)):
            # loop over all properties
            for j in range(len(self.AllValue[:][0])):
                # loop over all properties to fit
                for k in range(len(self.OptIndex[:][0])):

                        if j == self.OptIndex[i][k]:
                            self.OptNames.append(self.AllNames[i][j])
                            self.OptValue[i*len(self.OptIndex[:][0])+k]   = self.AllValue[i][j]
                            self.OptMin[i*len(self.OptIndex[:][0])+k]     = self.AllMin[i][j]
                            self.OptMax[i*len(self.OptIndex[:][0])+k]     = self.AllMax[i][j]
                            self.OptTypical[i*len(self.OptIndex[:][0])+k] = self.AllTypical[i][j]



    def Interpolate(self, nTemperature):

        self.AtSamplePnt = np.zeros(len(self.AllValue[:][0]))
        self.DerivWrtTemp = np.zeros(len(self.AllValue[:][0]))

        # interpolate material properties
        aMatPropX = np.zeros(len(self.AllValue))
        aMatPropCurrent  = np.zeros(len(self.AllValue[:][0]))
        DaMatPropCurrent  = np.zeros(len(self.AllValue[:][0]))
        for i in range(len(self.AllValue[:][0])):
            for j in range(len(self.AllValue)):
                aMatPropX[j] = self.AllValue[j][i]
            self.AtSamplePnt[i], self.DerivWrtTemp[i] = Interpolate.Interpolate(aMatPropX, self.SamplePnts, nTemperature)



    def checkConstraintViolated(self, iParameter):

        # check if constraint is violated
        if self.OptValue[iParameter] <= self.OptMin[iParameter] or self.OptValue[iParameter] >= self.OptMax[iParameter]:
            return 1
        else:
            return 0



    def projectParameterOnDesignSpace(self):

        # projection onto the design space
        for iParameter in range(self.OptLen):
            if self.OptValue[iParameter] < self.OptMin[iParameter]:
                print("###    %s = OptValue[%i] = %.8e < Min = %.8e"%(self.OptNames[iParameter],iParameter, self.OptValue[iParameter], self.OptMin[iParameter]), "--> project parameter on parameter space boundary")
            if self.OptValue[iParameter] > self.OptMax[iParameter]:
                print("###    %s = OptValue[%i] = %.8e > Max = %.8e"%(self.OptNames[iParameter],iParameter, self.OptValue[iParameter], self.OptMax[iParameter]), "--> project parameter on parameter space boundary")
            self.OptValue[iParameter] = min(max(self.OptMin[iParameter],self.OptValue[iParameter]),self.OptMax[iParameter])



    def generateVariationGauss(self, nRelativeStandardDeviation):

        aParameterVariationGauss = self.CopyParameterStructure()

        for iParameter in range(self.OptLen):
            nStandardDeviation = nRelativeStandardDeviation * self.OptValue[iParameter]

            while 1:

                aParameterVariationGauss.OptValue[iParameter] = random.gauss(self.OptValue[iParameter], nStandardDeviation)

                # check if contraints are fulfilled (should be since design variable is generated with the limits)
                if 0 == aParameterVariationGauss.checkConstraintViolated(iParameter):
                    break

        aParameterVariationGauss.MapMatPropFit2All()
            
        return aParameterVariationGauss
        


    def Print(self):

        self.MapMatPropFit2All()
        for iParameter in range(len(self.AllValue)):
            # loop over all properties
            for jParameter in range(len(self.AllValue[:][0])):
                # loop over all properties to fit
                for kParameter in range(len(self.OptIndex[:][0])):

                        if jParameter == self.OptIndex[iParameter][kParameter]:

                            print("###   %s: OptValue[%i] = AllValue[%i][%i] = %.8e"%(self.OptNames[iParameter*len(self.OptIndex[:][0])+kParameter], iParameter*len(self.OptIndex[:][0])+kParameter, iParameter, jParameter, self.OptValue[iParameter*len(self.OptIndex[:][0])+kParameter]))
#                            print("###   %s: AllValue[%i][%i] = %.8e"%(AllNames[iParameter][jParameter], iParameter, jParameter, self.AllValue[iParameter][jParameter]))

        print("###")
        
        # loop over number of temperatures
        print('##AllValue = ['),
        for iTemperature in range(len(self.AllValue)):
            print('\n##    ['),
            # loop over all properties
            for iParameter in range(len(self.AllValue[:][0])):
                print('%.6e,'%self.AllValue[iTemperature][iParameter]),
            print(' ],'),
        print('\n##] \n'),

        print("###")



    def CopyParameterStructure(self):

        aParameterCopy = sParameterStucture()

        aParameterCopy.SamplePnts   = np.copy(self.SamplePnts)
        aParameterCopy.AllNames     = self.AllNames
        aParameterCopy.AllValue     = np.copy(self.AllValue)
        aParameterCopy.AllMin       = np.copy(self.AllMin)
        aParameterCopy.AllMax       = np.copy(self.AllMax)
        aParameterCopy.AllTypical   = np.copy(self.AllTypical)
        aParameterCopy.AtSamplePnt  = np.copy(self.AtSamplePnt)
        aParameterCopy.DerivWrtTemp = np.copy(self.DerivWrtTemp)
        aParameterCopy.OptLen       = self.OptLen
        aParameterCopy.OptIndex     = np.copy(self.OptIndex)
        aParameterCopy.OptNames     = self.OptNames
        aParameterCopy.OptValue     = np.copy(self.OptValue)
        aParameterCopy.OptMin       = np.copy(self.OptMin)
        aParameterCopy.OptMax       = np.copy(self.OptMax)
        aParameterCopy.OptTypical   = np.copy(self.OptTypical)

        return aParameterCopy
