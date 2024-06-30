#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_quantum
#   '.src/lundquist_3_var/constr_default.py'
#   Function for default constraints. Called if user does not pass in 
#       constraints for objective function or problem being optimized. 
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 28, 2024
##--------------------------------------------------------------------\



import numpy as np

def constr_default(X):
    return True