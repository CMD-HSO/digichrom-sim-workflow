import sys
import math
import numpy as np
import os
import subprocess
import shutil

def CalcModelSum_DispCntr(aParameter, aExperimentInfos, aTime, aMeasExp, aCntrExp, aTempExp, sOutputFile, iprint):

    # write parameter: initial temperature
    hOutputPara = open("indent_para.inp", "w")
    hOutputPara.write("*Parameter\n")
    hOutputPara.write(" TempIni = %.10e\n"%(aTempExp[0]))
    hOutputPara.write(" TimeIncIni = %.10e\n"%((aTime[1]-aTime[0])/2.)) # on the basis of the initial time increment
    hOutputPara.write(" TimeStep = %.10e\n"%(aTime[-1]-aTime[0]))
    hOutputPara.write(" TimeIncMin = %.10e\n"%(np.min(np.diff(aTime))/100.))  # on the basis of the smallest time increment
    hOutputPara.write(" TimeIncMax = %.10e\n"%(np.max(np.diff(aTime)))) # max. time increment
    hOutputPara.close()

    # write amplitudes and time points based on experimental data
    hOutputAmpl = open("indent_ampl.inp", "w")
    hOutputAmpl.write("*Amplitude, name=A-disp, time=TOTAL TIME\n")
    iCount = 0
    for i in range(len(aTime)):
        hOutputAmpl.write(' %.10e, %.10e,\t'%(aTime[i]-aTime[0], aCntrExp[i]))
        iCount = iCount+1
        if 4 == iCount:
            hOutputAmpl.write('\n')
            iCount = 0
    if 0 != iCount:
        hOutputAmpl.write("\n")
    hOutputAmpl.write("**\n")
    hOutputAmpl.write("*Amplitude, name=A-temp, time=TOTAL TIME\n")
    iCount = 0
    for i in range(len(aTime)):
        hOutputAmpl.write(' %.10e, %.10e,\t'%(aTime[i]-aTime[0], aTempExp[i]))
        iCount = iCount+1
        if 4 == iCount:
            hOutputAmpl.write('\n')
            iCount = 0
    if 0 != iCount:
        hOutputAmpl.write("\n")
    hOutputAmpl.write("**\n")
    hOutputAmpl.write("*Time Points, name=TimePoints\n")
    iCount = 0
    for i in range(len(aTime)):
        hOutputAmpl.write(' %.10e,'%(aTime[i]-aTime[0]))
        iCount = iCount+1
        if 8 == iCount:
            hOutputAmpl.write('\n')
            iCount = 0
    if 0 != iCount:
        hOutputAmpl.write("\n")
    hOutputAmpl.close()

    # write material card with current material properties
    hOutputPROPS = open("indent_mat.inp", "w")
    hOutputPROPS.write("*MATERIAL, NAME=PLASTIC\n")
    hOutputPROPS.write("**\n")
    hOutputPROPS.write("*ELASTIC\n")
    hOutputPROPS.write("**E, nue\n")
    for i in range(len(aParameter.SamplePnts)):
        hOutputPROPS.write(' %.6e, %.6e, %.6e\n'%(aParameter.AllValue[i][0], aParameter.AllValue[i][1], aParameter.SamplePnts[i]))  
    hOutputPROPS.write("**\n")
    hOutputPROPS.write("*PLASTIC, HARDENING=COMBINED, DATA TYPE=PARAMETERS\n")
    hOutputPROPS.write("**Re, C, gamma\n")
    for i in range(len(aParameter.SamplePnts)):
        hOutputPROPS.write(' %.6e, %.6e, %.6e, %.6e\n'%(aParameter.AllValue[i][4], aParameter.AllValue[i][8], aParameter.AllValue[i][8]/aParameter.AllValue[i][7], aParameter.SamplePnts[i]))  
    hOutputPROPS.write("**\n")
    hOutputPROPS.write("*CYCLIC HARDENING, PARAMETERS\n")
    hOutputPROPS.write("**Re, qinf, b\n")
    for i in range(len(aParameter.SamplePnts)):
        hOutputPROPS.write(' %.6e, %.6e, %.6e, %.6e\n'%(aParameter.AllValue[i][4], aParameter.AllValue[i][5], aParameter.AllValue[i][6], aParameter.SamplePnts[i]))  
    hOutputPROPS.close()

    # write output definition
    hOutputOutp = open("indent_outp.inp", "w")
    if 1 == iprint:
        hOutputOutp.write("*Output, field, time points=TimePoints\n")
        hOutputOutp.write("*ELEMENT OUTPUT, POSITION=INTEGRATION POINTS\n")
        hOutputOutp.write(" S, E, PE, PEEQ\n")
        hOutputOutp.write("*NODE OUTPUT\n")
        hOutputOutp.write(" U, RF\n")
        hOutputOutp.write("**\n")
    hOutputOutp.write("*Output, history, time points=TimePoints\n")
    hOutputOutp.write("*NODE OUTPUT, NSET=sphere\n")
    hOutputOutp.write(" U, RF\n")
    hOutputOutp.close()

    # copy global input file
    sAbaJob = "aba_" + aExperimentInfos[0]
    shutil.copy2("indent_glob.inp", sAbaJob+".inp")

    if os.path.exists(sAbaJob+"_N-RP.rpt"):
        os.remove(sAbaJob+"_N-RP.rpt")

    # run ABAQUS job
    subprocess.call('abaqus job=%s interactive ask_delete=OFF'%(sAbaJob), shell=True)

#   ich habe google drive sync gestoppt. vielleicht hilft das.
##    # hilft das um Abbrueche zu vermeiden?
##    time.sleep(1)
##    while os.path.exists(sAbaJob+".lck"):
##        time.sleep(1)
    
    # postprocessing of ABAQUS results --> load-displacement data
    subprocess.call('abaqus cae noGUI=_postProc_IndPlast_CMDHSO_260731.py -- %s'%(sAbaJob), shell=True)

##    if 1 != iprint:
##        os.remove("%s.com"%(sAbaJob))
##        os.remove("%s.dat"%(sAbaJob))
##        os.remove("%s.mdl"%(sAbaJob))
##        os.remove("%s.msg"%(sAbaJob))
##        os.remove("%s.odb"%(sAbaJob))
##        os.remove("%s.par"%(sAbaJob))
##        os.remove("%s.pes"%(sAbaJob))
##        os.remove("%s.pmg"%(sAbaJob))
##        os.remove("%s.prt"%(sAbaJob))
##        os.remove("%s.res"%(sAbaJob))
##        os.remove("%s.sim"%(sAbaJob))
##        os.remove("%s.sta"%(sAbaJob))
##        os.remove("%s.stt"%(sAbaJob))

    # read data form file
    aData = np.genfromtxt(sAbaJob+"_N-RP.rpt", skip_header=3, comments="#")
    aMeasSim = -2.*aData[:,2]  # factor of two considered since 2D axisymmetric model is used --> should be checked e.g. by comparing with 3D model

    if len(aMeasSim) != len(aMeasExp):
        print("ERROR: len(aMeasSim) != len(aMeasExp)",len(aMeasSim), len(aMeasExp))
        sys.exit()

    if 1 == iprint:
        hOutput = open(sOutputFile, "w")
        hOutput.write("#aTime 0" + "\t" + "aMeasExp 1" + "\t" + "aMeasSim 2" + "\t" + "aCntrExp 3" + "\t" + "- 4" + "\t" + "aTempExp 5" + "\n")
    
    # evaluate least square sum
    nModelSum = 0.
    for i in range(len(aMeasSim)):
        
        if 1 == iprint:
            hOutput.write(str(aTime[i]) + "\t" + str(aMeasExp[i]) + "\t" + str(aMeasSim[i]) + "\t" + str(aCntrExp[i]) + "\t" + "    -    " + "\t" + str(aTempExp[i]) + "\n")

        nStandardDeviation = max(10.,0.1*abs(aMeasExp[i]))
        nStandardDeviation = 1.
        nModelSum = nModelSum + 0.5*( (aMeasSim[i] - aMeasExp[i] ) / nStandardDeviation )**2.
    if 1 == iprint:
        hOutput.close()

    return nModelSum



def CalcModelAll(aParameter, aExperimentInfos, aTimeAll, aMeasExpAll, aCntrExpAll, aTempExpAll, iprint):
    
    aParameter.MapMatPropFit2All()

    nModelSumAll = 0.

    nModelSums = []

    for iExp in range(len(aExperimentInfos)):
        if iprint == 1:
            print("###   nModelSum of " + aExperimentInfos[iExp][0] + " (" + aExperimentInfos[iExp][3] + "):"),

        sOutputFile = aExperimentInfos[iExp][0] + ".out"

        if aExperimentInfos[iExp][2] == "disp":
            nModelSum  = CalcModelSum_DispCntr(aParameter, aExperimentInfos[iExp], aTimeAll[iExp], aMeasExpAll[iExp], aCntrExpAll[iExp], aTempExpAll[iExp], sOutputFile, iprint)
            
        else:
            print("aExperimentInfos[2] not known:",aExperimentInfos[2])
            sys.exit()

        nWeight = aExperimentInfos[iExp][1]

        nModelSumAll = nModelSumAll + nWeight * nModelSum

        if iprint == 1:
            print(nModelSum, ", weight:", nWeight)

        nModelSums.append(nModelSum)

    if iprint == 1:
        print("###")

    return nModelSumAll
