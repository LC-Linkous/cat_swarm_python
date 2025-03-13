#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_python
#   './cat_swarm_python/src/main_test.py'
#   Test function/example for using the 'swarm' class in cat_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: March 13, 2025
##--------------------------------------------------------------------\


import pandas as pd

from cat_swarm import swarm

# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
import himmelblau.configs_F as func_configs         # single objective, 2D input
#import lundquist_3_var.configs_F as func_configs     # multi objective function


if __name__ == "__main__":
    # swarm variables
    NO_OF_PARTICLES = 8          # Number of particles in swarm
    WEIGHTS = [2]                # Update vector weights. Used as C1 constant in tracing mode.
    VLIM = 1.5                   # Initial velocity limit
    TOL = 10 ** -4               # Convergence Tolerance
    MAXIT = 10000                # Maximum allowed iterations
    BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                 #              3 = absorbing,   4 = invisible 
    
    
    # Objective function dependent variables
    LB = func_configs.LB                    # Lower boundaries, [[0.21, 0, 0.1]]
    UB = func_configs.UB                    # Upper boundaries, [[1, 1, 0.5]]
    IN_VARS = func_configs.IN_VARS          # Number of input variables (x-values)   
    OUT_VARS = func_configs.OUT_VARS        # Number of output variables (y-values)
    TARGETS = func_configs.TARGETS          # Target values for output

    # Objective function dependent variables
    func_F = func_configs.OBJECTIVE_FUNC  # objective function
    constr_F = func_configs.CONSTR_FUNC   # constraint function

    
    
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

    # Constant variables
    opt_params = {'NO_OF_PARTICLES': [NO_OF_PARTICLES],     # Number of particles in swarm
                'BOUNDARY': [BOUNDARY],                     # int boundary 1 = random,      2 = reflecting
                                                            #              3 = absorbing,   4 = invisible
                'WEIGHTS': [WEIGHTS],                       # Update vector weights
                'VLIM':  [VLIM],                            # Initial velocity limit
                'MR': [MR],                                 # Mixture Ratio (MR). Small value for tracing population %.
                'SMP': [SMP],                               # Seeking memory pool. Num copies of cats made.
                'SRD': [SRD],                               # Seeking range of the selected dimension. 
                'CDC': [CDC],                               # Counts of dimension to change. mutation.
                'SPC': [SPC]}                                # self-position consideration. boolean.

    opt_df = pd.DataFrame(opt_params)
    mySwarm = swarm(LB, UB, TARGETS, TOL, MAXIT,
                            func_F, constr_F,
                            opt_df,
                            parent=parent)     


    # instantiation of particle swarm optimizer 
    while not mySwarm.complete():

        # step through optimizer processing
        # update_velocity, will change the particle location
        mySwarm.step(suppress_output)

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer

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

