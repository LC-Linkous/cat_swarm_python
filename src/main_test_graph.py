#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_python
#   './cat_swarm_python/src/main_test_graph.py'
#   Test function/example for using the 'swarm' class in cat_swarm.py.
#       This has been modified from the original pso_python to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#       This version builds from 'main_test_details.py' to include a 
#       matplotlib plot of particle location
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 14, 2024
##--------------------------------------------------------------------\


import numpy as np
import time
import matplotlib.pyplot as plt
from cat_swarm import swarm
import configs_F as func_configs



class TestGraph():
    def __init__(self):
        self.ctr = 0

        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function
        LB = func_configs.LB              # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB              # Upper boundaries, [[1, 1, 0.5]]   
        OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS    # Target values for output

        # swarm variables
        NO_OF_PARTICLES = 25         # Number of particles in swarm
        WEIGHTS = [[2, 2.2, 2]]      # Update vector weights. Used as C1 constant in tracing mode.
        VLIM = 1.5                   # Initial velocity limit
        E_TOL = 10 ** -4             # Convergence Tolerance
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
        parent = self                 # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        detailedWarnings = False      # Optional boolean for detailed feedback


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
                                        # (Can be set on each iteration to allow 
                                        # for when control flow can be returned 
                                        # to multiglods)


        self.mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, VLIM, OUT_VARS, TARGETS,
                        E_TOL, MAXIT, BOUNDARY, func_F, constr_F, 
                        MR=MR, SMP=SMP, SRD=SRD, CDC=CDC, SPC=SPC,
                        parent=parent, detailedWarnings=detailedWarnings)  


        # Matplotlib setup
        self.targets = TARGETS
        self.fig = plt.figure(figsize=(10, 5))#(figsize=(14, 7))
        # position
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax1.set_title("Particle Location, Iteration: " + str(self.ctr))
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_zlabel('Z')
        self.scatter1 = None
        # fitness
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        self.ax2.set_title("Fitness Relation to Target")
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_zlabel('Z')
        self.scatter2 = None

    def debug_message_printout(self, txt):
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
         

    def update_plot(self, m_coords, f_coords, targets, showTarget, clearAx=True, setLimts=False):
        # if self.scatter is None:
        if clearAx == True:
            self.ax1.clear() #use this to git rid of the 'ant tunnel' trails
            self.ax2.clear()
        if setLimts == True:
            self.ax1.set_xlim(-5, 5)
            self.ax1.set_ylim(-5, 5)
            self.ax1.set_zlim(-5, 5)
            
            self.ax2.set_xlim(-5, 5)
            self.ax2.set_ylim(-5, 5)
            self.ax2.set_zlim(-5, 5)
        
        # MOVEMENT PLOT
        if np.shape(m_coords)[0] == 2: #2-dim func
            self.ax1.set_title("Particle Location, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.scatter = self.ax1.scatter(m_coords[0, :], m_coords[1, :], edgecolors='b')

        elif np.shape(m_coords)[0] == 3: #3-dim func
            self.ax1.set_title("Particle Location, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("$x_3$")
            self.scatter = self.ax1.scatter(m_coords[0, :], m_coords[1, :], m_coords[2, :], edgecolors='b')


        # FITNESS PLOT
        if np.shape(f_coords)[0] == 2: #2-dim obj func
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x,y)$")
            self.ax2.set_ylabel("$F_{2}(x,y)$")
            self.scatter = self.ax2.scatter(f_coords[0, :], f_coords[1, :], marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(f_coords)[0] == 3: #3-dim obj fun
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x,y)$")
            self.ax2.set_ylabel("$F_{2}(x,y)$")
            self.ax2.set_zlabel("$F_{3}(x,y)$")
            self.scatter = self.ax2.scatter(f_coords[0, :], f_coords[1, :], f_coords[2, :], marker='o', s=40, facecolor="none", edgecolors="k")


        if showTarget == True: # plot the target point
            if len(targets) == 1:
                self.scatter = self.ax2.scatter(targets[0], 0, marker='*', edgecolors='r')
            if len(targets) == 2:
                self.scatter = self.ax2.scatter(targets[0], targets[1], marker='*', edgecolors='r')
            elif len(targets) == 3:
                self.scatter = self.ax2.scatter(targets[0], targets[1], targets[2], marker='*', edgecolors='r')


        plt.pause(0.0001)  # Pause to update the plot
        self.ctr = self.ctr + 1



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
            m_coords = self.mySwarm.M  #get x,y,z coordinate locations
            f_coords = self.mySwarm.F_Gb # global best of set
            self.update_plot(m_coords, f_coords, self.targets, showTarget=True, clearAx=True) #update matplot

        print("Optimized Solution")
        print(self.mySwarm.get_optimized_soln())
        print("Optimized Outputs")
        print(self.mySwarm.get_optimized_outs())

        time.sleep(15)

if __name__ == "__main__":
    pso = TestGraph()
    pso.run()
