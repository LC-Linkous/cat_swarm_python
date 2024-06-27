#! /usr/bin/python3

##--------------------------------------------------------------------\
#   sweep_python
#   './sweep_python/src/func_F.py'
#   Function for objective function evaluation.
#   Has checks for floating point error, but these should never trigger
#       if constraints have been properly applied.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: May 30, 2024
##--------------------------------------------------------------------\

import numpy as np
import time
def func_F(X, NO_OF_OUTS=2):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        F[0] = (X[0]-0.5) ** 2 + (X[1]-0.1) ** 2
        F[1] = (X[2]-0.2) ** 4
        
    except:
        noErrors = False
    
    return F, noErrors
