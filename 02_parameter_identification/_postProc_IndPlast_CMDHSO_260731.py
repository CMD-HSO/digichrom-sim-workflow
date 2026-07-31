#
# Abaqus/CAE Release 6.11-2 replay file
# Internal Version: 2011_07_12-15.51.58 111859
# Run by ADMIN on Fri Aug 24 11:26:05 2012
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...

from abaqus import *
from abaqusConstants import *

from caeModules import *
from driverUtils import executeOnCaeStartup

import math
import os
import numpy as np


print(' ')
print("sys.argv",sys.argv)
print(' ')

print >> sys.__stdout__, "sys.argv",sys.argv

# RESEARCH LICENCE of ABAQUS
#sys.argv [
#0 'C:\\SIMULIA\\EstProducts\\2023\\win_b64\\code\\bin\\ABQvwrK.exe',
#1 '-cae',
#2 '-noGUI',
#3 '_postProc_IndPlast_CMDHSO_260731.py',
#4 '-lmlog',
#5 'ON',
#6 '-tmpdir',
#7 'C:\\Users\\...\\AppData\\Local\\Temp',
#8 'aba_data_indent']

# TEACHING LICENCE of ABAQUS
#sys.argv [
#0 'C:\\SIMULIA\\EstProducts\\2023\\win_b64\\code\\bin\\ABQcaeK.exe', 
#1 '-cae',
#2 '-noGUI',
#3 '_postProc_IndPlast_CMDHSO_260731.py',
#4 '-lmlog',
#5 'ON',
#6 '-tmpdir',
#7 'C:\\Users\\..\\AppData\\Local\\Temp',
#8 '-academic',
#9 'TEACHING',
#10 'aba_data_indent']

# read arguments
if len(sys.argv) < 11:
    print(' ')
    print('Arguments are missing.')
    print(' ')
    sys.exit(1)
else:
    args = []
    for i in range(len(sys.argv)):
        args.append(str(sys.argv[i]))
    sJobName = args[10]
    print(" ")
    print("Used arguments:")
    print("sJobName  ", sJobName)
    
sWorkDir = "./"

os.chdir(sWorkDir)
print "change sWorkDir: ", sWorkDir
   
sOdbFile = sWorkDir + sJobName + '.odb'

session.openOdb(sOdbFile)
odb = session.odbs[sOdbFile]

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=300., height=150.)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(curveRefinementLevel=FINE)

# set font
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*', 
    titleFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*', 
    stateFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*',
    legendMinMax=ON)
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(otherSymbolSize=14)

sRptFile = sWorkDir + sJobName + '_N-RP.rpt'
xy_result = session.XYDataFromHistory(name='U', odb=odb, outputVariableName='Spatial displacement: U2 PI: PART-1-1 Node 9000000 in NSET SPHERE')
xy_result = session.XYDataFromHistory(name='RF', odb=odb, outputVariableName='Reaction force: RF2 PI: PART-1-1 Node 9000000 in NSET SPHERE')
session.writeXYReport(fileName=sRptFile, appendMode=OFF, xyData=(session.xyDataObjects['U'],
                                                                 session.xyDataObjects['RF']))

















