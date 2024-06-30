#! /usr/bin/python3

##-------------------------------------------------------------------------------\
#   sand_cat_python
#   '.src/himmelblau/func_F.py'
#   objective function for function compatable with project optimizers
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: May 28, 2024
##-------------------------------------------------------------------------------\

import numpy as np

def func_F(X, NO_OF_OUTS=1):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        x = X[0]
        y = X[1]   
        F[0] = (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    except:
        noErrors = False

    return F, noErrors
