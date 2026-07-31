import sys
import math
import numpy as np

# Function for the evaluation of the function values at location xneu
# for a given data table (x, fvonx) by linear interpolation.
# Author: Thomas Seifert
# Date: 30.6.2012
# Input: fvonx - array of function values at x
#        x - array of locations at which the function values are given
#        xneu- scalar at which a function value is computed by linear interpolation
# Output: Interpolated function value f_int and slope in the respective interval.

def Interpolate(fvonx, x, xneu):

    f_int = 0.
    df_int = 0.
    if xneu < min(x):
        f_int = fvonx[0]
        df_int = 0.
        return f_int, df_int
    elif xneu >= max(x):
        f_int = fvonx[len(fvonx)-1]
        df_int = 0.
        return f_int, df_int
    else:
        for k in range(len(x)-1):
            if xneu < x[k+1] and xneu >= x[k]:
                df_int = (fvonx[k+1] - fvonx[k])/(x[k+1]-x[k])
                f_int = fvonx[k] + df_int *(xneu-x[k])
                return f_int, df_int






# Function for the evaluation of the function values at location xneu
# for two given data tables (x, fvonx1) and (x, fvonx2) by linear interpolation.
# The function memorieses the interval of the last function call in the
# last entry of fvonx1 and fvonx2.
# Author: Thomas Seifert
# Date: 30.6.2012
# Input: fvonx1, fvonx2 - arrays of function values at x
#        x - array of locations at which the function values are given
#        xneu- scalar at which a function value is computed by linear interpolation
# Output: Interpolated function values f_int1 and fint2 and slope in the respective interval.
#         The last entry in fvonx1 and fvonx2 is modified in this routine.

def Interpolate2ArgumentsWithMemory(fvonx1, fvonx2, x, xneu):

    f_int1 = 0.
    df_int1 = 0.
    f_int2 = 0.
    df_int2 = 0.

    # if location out of the range of x (lower)
    if xneu <= x[0]:
        f_int1 = fvonx1[0]
        df_int1 = 0.
        f_int2 = fvonx2[0]
        df_int2 = 0.
        # remember the last interval
        fvonx1[-1] = 0.
        fvonx2[-1] = 0.
        return f_int1, df_int1, f_int2, df_int2

    # if location out of the range of x
    elif xneu > x[-1]:
        f_int1 = fvonx1[len(fvonx1)-2]
        df_int1 = 0.
        f_int2 = fvonx2[len(fvonx2)-2]
        df_int2 = 0.
        # remember the last interval
        fvonx1[-1] = len(fvonx1)-1.
        fvonx2[-1] = len(fvonx2)-1.
        return f_int1, df_int1, f_int2, df_int2

    # identify interval in which xnew is located and compute linear interpolation
    else:
        # recover last interval. index may not be below zero
        # (****)
        iStart = (max(int(0.),int(fvonx1[-1])-200))
        for k in range(iStart,len(x)-1):
            if xneu <= x[k+1] and xneu > x[k]:
                df_int1 = (fvonx1[k+1] - fvonx1[k])/(x[k+1]-x[k])
                f_int1 = fvonx1[k] + df_int1 *(xneu-x[k])
                df_int2 = (fvonx2[k+1] - fvonx2[k])/(x[k+1]-x[k])
                f_int2 = fvonx2[k] + df_int2 *(xneu-x[k])
                # remember the last interval
                fvonx1[-1] = k
                fvonx2[-1] = k
                return f_int1, df_int1, f_int2, df_int2

    # emergency stop if xnew is not in an interval from which the interval search is started. In this case, increase the number in (****) from which the interval search is started.
    print("ERROR in Interpolate2ArgumentsWithMemory: ", iStart, x[iStart], xneu)
    sys.exit()

    return
    
    




