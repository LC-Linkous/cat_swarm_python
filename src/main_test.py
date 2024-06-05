#! /usr/bin/python3

##--------------------------------------------------------------------\
#   pso_basic
#   './pso_basic/src/main_test.py'
#   Test function/example for using the 'swarm' class in cat_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 4, 2024
##--------------------------------------------------------------------\


import numpy as np
from cat_swarm import swarm
from func_F import func_F
from constr_F import constr_F


if __name__ == "__main__":
    # objective function boundaries
    LB = [[0.21, 0, 0.1]]        # Lower boundaries
    UB = [[1, 1, 0.5]]           # Upper boundaries
    OUT_VARS = 2                 # Number of output variables (y-values)
    TARGETS = [0, 0]             # Target values for output

    # swarm variables
    NO_OF_PARTICLES = 25         # Number of particles in swarm
    WEIGHTS = [[2, 2.2, 2]]      # Update vector weights. Used as C1 constant in tracing mode.
    VLIM = 1.5                   # Initial velocity limit
    E_TOL = 10 ** -6             # Convergence Tolerance
    MAXIT = 10000                # Maximum allowed iterations
    BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                 #              3 = absorbing,   4 = invisible

    # cat swarm specific
    MR = .02                    # Mixture Ratio (MR). Small value for tracing population %.
    SMP = 5                     # Seeking memory pool. Num copies of cats made.
    SRD = .45                   # Seeking range of the selected dimension. 
    CDC = 2                     # Counts of dimension to change. mutation.
    SPC = True                  # self-position consideration. boolean.


    # swarm setup
    best_eval = 1

    parent = None            # for the PSO_TEST ONLY

    suppress_output = True   # Suppress the console output of particle swarm

    allow_update = True      # Allow objective call to update state 
                            # (Can be set on each iteration to allow 
                            # for when control flow can be returned 
                            # to multiglods)

    mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                    WEIGHTS, VLIM, OUT_VARS, TARGETS,
                    E_TOL, MAXIT, BOUNDARY, func_F, constr_F,
                    MR=MR, SMP=SMP, SRD=SRD, CDC=CDC, SPC=SPC)  

    # instantiation of particle swarm optimizer 
    while not mySwarm.complete():

        # step through optimizer processing
        # update_velocity, will change the particle location
        mySwarm.step(suppress_output)

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer

        # for some objective functions, the function
        # might not evaluate correctly (e.g., under/overflow)
        # so when that happens, the function is not evaluated
        # and the 'step' fucntion will re-gen values and try again


        mySwarm.call_objective(allow_update)
        iter, eval = mySwarm.get_convergence_data()
        if (eval < best_eval) and (eval != 0):
            best_eval = eval
        if suppress_output:
            if iter%100 ==0: #print out every 100th iteration update
                print("Iteration")
                print(iter)
                print("Best Eval")
                print(best_eval)

    print("Optimized Solution")
    print(mySwarm.get_optimized_soln())
    print("Optimized Outputs")
    print(mySwarm.get_optimized_outs())
