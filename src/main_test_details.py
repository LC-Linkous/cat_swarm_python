#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_python
#   './cat_swarm_python/src/main_test_details.py'
#   Test function/example for using the 'swarm' class in cat_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: August 18, 2024
##--------------------------------------------------------------------\


import numpy as np
import time
from cat_swarm import swarm


# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
import himmelblau.configs_F as func_configs         # single objective, 2D input
#import lundquist_3_var.configs_F as func_configs     # multi objective function


class TestDetails():
    def __init__(self):
        # swarm variables
        NO_OF_PARTICLES = 8          # Number of particles in swarm
        WEIGHTS = 2                  # Update vector weights. Used as C1 constant in tracing mode.
        VLIM = 1.5                   # Initial velocity limit
        E_TOL = 10 ** -4             # Convergence Tolerance
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

        # Swarm vars
        self.best_eval = 1            # Starting eval value

        parent = self                 # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        self.suppress_output = True   # Suppress the console output of particle swarm

        detailedWarnings = False      # Optional boolean for detailed feedback
                                        # (Independent of suppress output. 
                                        #  Includes error messages and warnings)

        self.allow_update = True      # Allow objective call to update state 



        self.mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, VLIM, OUT_VARS, TARGETS,
                        E_TOL, MAXIT, BOUNDARY, func_F, constr_F,
                        MR=MR, SMP=SMP, SRD=SRD, CDC=CDC, SPC=SPC,
                        parent=parent, detailedWarnings=detailedWarnings)


    def updateStatusText(self, txt):
        if txt is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(txt)
        print(msg)


    def record_params(self):
        # this function is called from particle_swarm.py to trigger a write to a log file
        # running in the AntennaCAT GUI to record the parameter iteration that caused an error
        pass
         

    def run(self):

        # instantiation of particle swarm optimizer 
        while not self.mySwarm.complete():

            # step through optimizer processing
            self.mySwarm.step(self.suppress_output)

            # call the objective function, control 
            # when it is allowed to update and return 
            # control to optimizer
            self.mySwarm.call_objective(self.allow_update)
            iter, eval = self.mySwarm.get_convergence_data()
            if (eval < self.best_eval) and (eval != 0):
                self.best_eval = eval
            if self.suppress_output:
                if iter%100 ==0: #print out every 100th iteration update
                    print("Iteration")
                    print(iter)
                    print("Best Eval")
                    print(self.best_eval)

        print("Optimized Solution")
        print(self.mySwarm.get_optimized_soln())
        print("Optimized Outputs")
        print(self.mySwarm.get_optimized_outs())



if __name__ == "__main__":
    pso = TestDetails()
    pso.run()
