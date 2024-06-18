#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_quantum
#   './cat_swarm_quantum/src/configs_F.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 4, 2024
##--------------------------------------------------------------------\
import sys

from func_F import func_F
from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "cat_swarm_quantum.func_F"
CONSTR_FUNC_NAME = "cat_swarm_quantum.constr_F"

# problem dependent variables
LB = [[0.21, 0, 0.1]]       # Lower boundaries for input
UB = [[1, 1, 0.5]]          # Upper boundaries for input
IN_VARS = 3                 # Number of input variables (x-values)
OUT_VARS = 2                # Number of output variables (y-values)
TARGETS = [0, 0]            # Target values for output