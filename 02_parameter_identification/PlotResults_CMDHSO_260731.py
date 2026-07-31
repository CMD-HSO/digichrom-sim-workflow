import numpy as np
import matplotlib.pyplot as plt

def plotResults(aExperimentInfos,sExtension):

    print("###")
    print("###   ===== generate figures of model results")
    print("###")

    aTimeAll    = []
    aMeasExpAll = []
    aMeasSimAll = []
    aCntrExpAll = []
    aTempExpAll = []

    for iExperiment in range(len(aExperimentInfos)):

        sOutputFile = aExperimentInfos[iExperiment][0] + ".out"
        print("###   Experiment: " + aExperimentInfos[iExperiment][0], ", sOutputFile: " + sOutputFile)

        # generate figures
        aData = np.genfromtxt(sOutputFile, usecols=[0,1,2,3,4,5], comments="#")
        
        aTimeAll.append(aData[:,0])
        aMeasExpAll.append(aData[:,1])
        aMeasSimAll.append(aData[:,2])
        aCntrExpAll.append(aData[:,3])
        aTempExpAll.append(aData[:,5])

    for i in range(len(aExperimentInfos)):

        sOutputFile = aExperimentInfos[i][0] + ".out"
#        print "###   Experiment: " + aExperimentInfos[i][0], ", sOutputFile: " + sOutputFile

        plt.plot(aCntrExpAll[i], aMeasExpAll[i], 'k-+', mfc='none' )
        plt.plot(aCntrExpAll[i], aMeasSimAll[i], 'r--' )
        plt.xlabel("displacement in mm", fontsize=18)
        plt.ylabel("load in N", fontsize=18)

        plt.legend( ("experiment", "model"), loc='lower right')
        sFigName = "Fig_" + aExperimentInfos[i][3] + "_" + aExperimentInfos[i][0] + "_" + sExtension + "_load-disp.png"
        plt.savefig(sFigName, dpi=600)
        plt.close()

        plt.plot(aTimeAll[i], aCntrExpAll[i], 'b-')
        plt.xlabel("time in s", fontsize=18)
        plt.ylabel("displacement in mm", fontsize=18)

        sFigName = "Fig_" + aExperimentInfos[i][3] + "_" + aExperimentInfos[i][0] + "_" + sExtension + "_disp-time.png"
        plt.savefig(sFigName, dpi=600)
        plt.close()

        plt.plot(aTimeAll[i], aMeasExpAll[i], 'k-+', mfc='none' )
        plt.plot(aTimeAll[i], aMeasSimAll[i], 'r--' )
        plt.xlabel("time in s", fontsize=18)
        plt.ylabel("load in N", fontsize=18)

        plt.legend( ("experiment", "model"), loc='lower right')
        sFigName = "Fig_" + aExperimentInfos[i][3] + "_" + aExperimentInfos[i][0] + "_" + sExtension + "_load-time.png"
        plt.savefig(sFigName, dpi=600)
        plt.close()

        SMALL_SIZE = 9
        MEDIUM_SIZE = 11
        BIGGER_SIZE = 12

        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize

        plt.subplot(212)
        plt.plot(aCntrExpAll[i], aMeasExpAll[i], 'k-+', mfc='none' )
        plt.plot(aCntrExpAll[i], aMeasSimAll[i], 'r--' )
        plt.xlabel("displacement in mm")
        plt.ylabel("load in N")
        plt.legend( ("experiment", "model"), loc='lower right')

        plt.subplot(221)
        plt.plot(aTimeAll[i], aCntrExpAll[i], 'b-')
        plt.xlabel("time in s")
        plt.ylabel("displacement in mm")

        plt.subplot(222)
        plt.plot(aTimeAll[i], aMeasExpAll[i], 'k-+', mfc='none' )
        plt.plot(aTimeAll[i], aMeasSimAll[i], 'r-x' )
        plt.xlabel("time in s")
        plt.ylabel("load in N")
        plt.legend( ("experiment", "model"), loc='lower right')

        #plt.tight_layout()
        sFigName = "Fig_" + aExperimentInfos[i][3] + "_" + aExperimentInfos[i][0] + "_" + sExtension + "_ALL.png"
        plt.savefig(sFigName, dpi=600)
        plt.close()


    return

